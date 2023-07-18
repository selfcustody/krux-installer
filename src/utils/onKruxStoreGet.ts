import { Ref } from "vue"
import setMainData from './setMainData'
import messages from "./messages"

async function onGetResource (
  data: Ref<Record<string, any>>,
  result: Record<string, any>,
  options: Record<string, any>
): Promise<void> {

  let toCheck = ''
  if (options.resource.match(/^.*(zip|sha256.txt|sig|pem)$/g)){
    toCheck = options.resource.match(/^.*(zip|sha256.txt|sig|pem)$/g)[0]
  } else if (options.resource.match(/^.*(firmware|kboot|ktool).*$/g)) {
    toCheck = options.resource.split('/main/')[1]
  }

  await messages.add(data, `Checking ${toCheck}`)
  await window.api.invoke('krux:check:resource', {
    from: result.from,
    baseUrl: options.baseUrl,
    resource: options.resource
  })
}

/**
 * Setup `data` and/or redirects to a `page`, or invoke another api call;
 * 
 * ### KruxInstallerLogo
 * 
 * - When user start app
 *  
 * ### Main page
 * 
 * When `result.from` value is: 
 * - KruxInstallerLogo;
 * - SelectVersion;
 * - VerifiedOfficialRelease; or
 * - ErrorMsg
 * 
 * Set the `data` variable the following properties:
 * - `device`;
 * - `version`; and 
 * - `ktool`.
 * 
 * ### SelectDevice
 * 
 * When user selected device to be flashed;
 * 
 * It will need to decide wheather go to official release
 * or odudex's experimental release. After,it will need to check if the specific resource exist.
 * If not exist, redirect to download pages; if exist, redirect to warning page.
 * 
 * The likely cycles will be:
 * 
 *  * Official release:
 *    * SelectVersion
 *      * krux:check:resource for https://github.com/selfcustody/krux/releases/download/{{ version }}/krux-{{ version }}.zip:
 *        * if exists, then krux:change:page to WarningDownload:
 *          * proceed to krux:check:resource for https://github.com/selfcustody/krux/releases/download/{{ version }}/krux-{{ version }}.zip.sha256.txt
 *          * download again with krux:change:page to DownloadOfficialReleaseZip
 *          * back to krux:change:page GithubChecker
 *        * if not exists, then krux:change:page to DownloadOfficialReleaseZip
 *      * krux:check:resource for https://github.com/selfcustody/krux/releases/download/{{ version }}/krux-{{ version }}.zip.sha256.txt:
 *        * if exists, then krux:change:page to WarningDownload:
 *          * proceed to krux:check:resource for https://github.com/selfcustody/krux/releases/download/{{ version }}/krux-{{ version }}.zip.sig
 *          * download again with krux:change:page to DownloadOfficialReleaseSha256
 *          * back to krux:change:page GithubChecker
 *        * if not exists, then krux:change:page to DownloadOfficialReleaseSha256
 *      * krux:check:resource for https://github.com/selfcustody/krux/releases/download/{{ version }}/krux-{{ version }}.zip.sig:
 *        * if exists, then krux:change:page to WarningDownload:
 *          * proceed to krux:check:resource for https://raw.githubusercontent.com/selfcustody/krux/main/selfcustody.pem
 *          * download again with krux:change:page to DownloadOfficialReleaseSig
 *          * back to krux:change:page GithubChecker
 *        * if not exists, then krux:change:page to DownloadOfficialReleasePem
 *      * krux:check:resource for https://raw.githubusercontent.com/selfcustody/krux/main/selfcustody.pem:
 *        * if exists, then krux:change:page to WarningDownload:
 *          * proceed to krux:change:page for CheckVerifyOfficialRelease 
 *          * download again with krux:change:page to DownloadOfficialReleasePem
 *          * back to krux:change:page GithubChecker
 *        * if not exists, then krux:change:page to DownloadOfficialReleasePem
 * 
 * @param data 
 * @param options
 * @returns Promise<void>
 */
export default function onKruxStoreGet (data: Ref<Record<string, any>>): Function {
  return async function (_: Event, result: Record<'from' | 'key' | 'values', any>): Promise<void> {

    // When user start app
    if ( result.from === 'KruxInstallerLogo') {
      data.value = {}
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'ConsoleLoad' })
      await messages.add(data, 'Loading data from storage')
      await messages.add(data, 'Verifying openssl')
      await window.api.invoke('krux:verify:openssl', { from: 'KruxInstallerLogo' })
      setMainData(data, result)
    }

    //

    // When user selected device to be flashed
    if (result.from === 'SelectDevice') {
      await setMainData(data, result)
      await window.api.invoke('krux:change:page', { page: 'Main' })
    }

    // When user selected back on SelectVersion
    if (result.from === 'Back::SelectVersion' ) {
      await setMainData(data, result)
      await window.api.invoke('krux:change:page', { page: 'Main' })
    }

    // When user selected between
    // official release version (.zip -> .zip.sha256.txt -> .zip.sig -> .pem files)
    // or test (.bin -> .kboot -> .kfpkg -> ktool)
    if (result.from === 'SelectVersion') {
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'ConsoleLoad' })
      
      // official release version (.zip -> .zip.sha256.txt -> .zip.sig -> .pem files)
      if (result.values.version.match(/selfcustody\/.*/g)){
        
        const domain = 'https://github.com'
        let baseUrl = result.values.version.replace(/tag/g, 'download')
        let version = baseUrl.split('download/')[1]
        baseUrl = baseUrl.split(`/${version}`)[0]

        await onGetResource(data, result, {
          baseUrl: `${domain}/${baseUrl}`,
          resource: `${version}/krux-${version}.zip`
        })
      }

      // or test (.bin -> .kboot -> .kfpkg -> ktool)
      if (result.values.version.match(/odudex\/krux_binaries/g)){

        await onGetResource(data, result, {
          baseUrl: 'https://raw.githubusercontent.com',
          resource: `${result.values.version}/main/${result.values.device}/firmware.bin`
        })
        
      }
      setMainData(data, result)
    }

    // ===========================
    // Official release life cycle
    // ===========================

    // When user came from:
    //  * .zip file
    //  * chacked it (and exists)
    //  * check for .zip.sha256.txt file
    if (
      result.from === 'DownloadOfficialReleaseZip' ||
      result.from.match(/^WarningDownload::.*.zip$/)
    ) {
      await setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'ConsoleLoad' })
      
      const domain = 'https://github.com'
      let baseUrl = result.values.version.replace(/tag/g, 'download')
      let version = baseUrl.split('download/')[1]
      baseUrl = baseUrl.split(`/${version}`)[0]

      await onGetResource(data, result, {
        baseUrl: `${domain}/${baseUrl}`,
        resource: `${version}/krux-${version}.zip.sha256.txt`
      })
    }

    // When user came from .zip.sha256.txt file and will check for .zip.sig file
    if (
      result.from === 'DownloadOfficialReleaseSha256' ||
      result.from.match(/^WarningDownload::.*.zip.sha256.txt$/)
    ) {
      await setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'ConsoleLoad' })
      
      const domain = 'https://github.com'
      let baseUrl = result.values.version.replace(/tag/g, 'download')
      let version = baseUrl.split('download/')[1]
      baseUrl = baseUrl.split(`/${version}`)[0]

      await onGetResource(data, result, {
        baseUrl: `${domain}/${baseUrl}`,
        resource: `${version}/krux-${version}.zip.sig`
      })  
    }

    // When user came from .zip.sig file and will check for .pem file
    if (
      result.from === 'DownloadOfficialReleaseSig' ||
      result.from.match(/^WarningDownload::.*.zip.sig$/)
    ) {
      await setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'ConsoleLoad' })

      await onGetResource(data, result, {
        baseUrl: 'https://raw.githubusercontent.com/selfcustody/krux',
        resource: 'main/selfcustody.pem'
      }) 
    }

    // When user came from .zip.sig file and will check for .pem file
    if (
      result.from === 'DownloadOfficialReleasePem' ||
      result.from.match(/^WarningDownload::.*.pem$/)
    ) {
      await setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'CheckVerifyOfficialRelease' })
    }

    if (result.from === 'CheckVerifyOfficialRelease') {
      await window.api.invoke('krux:verify:releases:hash')
    }

    if ( result.from === 'VerifiedOfficialRelease') {
      setMainData(data, result)
    }

    // =======================
    // Test release life cycle
    // =======================

    if (
      result.from === 'DownloadTestFirmware' ||
      result.from.match(/^WarningDownload::.*firmware.bin$/)
    ) {
      await setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'ConsoleLoad' })

      await onGetResource(data, result, {
        baseUrl: 'https://raw.githubusercontent.com',
        resource: `${result.values.version}/main/${result.values.device}/kboot.kfpkg`
      })  
      
    }

    if (
      result.from === 'DownloadTestKboot' ||
      result.from.match(/^WarningDownload::.*kboot.kfpkg$/)
    ) {
      await setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'ConsoleLoad' })

      let resource = ''

      if (result.values.os === 'linux') {
        resource = `main/ktool-linux`
      }
      else if (result.values.os === 'win32') {
        resource = `main/ktool-win.exe`
      }
      else if (result.values.os === 'darwin' && !result.values.isMac10) {
        resource = `main/ktool-mac`
      }
      else if (result.values.os === 'darwin' && result.values.isMac10) {
        resource = `main/ktool-mac-10`
      }

      await onGetResource(data, result, {
        baseUrl: 'https://raw.githubusercontent.com',
        resource: `${result.values.version}/${resource}`
      })
    }

    if (
      result.from === 'DownloadTestKtool' ||
      result.from.match(/^WarningDownload::.*ktool-(linux|win.exe|mac|mac-10)$/)
    ) {
      await setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'Main' })
    }

    if (result.from === 'Back::WarningDownload') {
      await setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'Main' })
    }

    if ( result.from === 'ErrorMsg') {
      await setMainData(data, result)
    }

    if (result.from === 'FlashToDevice') {
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'Main' })
      setMainData(data, result)
    }

  }
}