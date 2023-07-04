import { Ref } from "vue"
import setMainData from './setMainData'
import messages from "./messages"

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

    // When user selected device to be flashed
    if (result.from === 'SelectDevice') {
      setMainData(data, result)
      await window.api.invoke('krux:change:page', { page: 'Main' })
    }

    // When user selected between
    // official release version (.zip -> .zip.sha256.txt -> .zip.sig -> .pem files)
    // or test (.bin -> .kboot -> .kfpkg -> ktool)
    if (result.from === 'SelectVersion') {
      await window.api.invoke('krux:change:page', { page: 'ConsoleLoad' })
      messages.clean(data)

      // official release version (.zip -> .zip.sha256.txt -> .zip.sig -> .pem files)
      if (result.values.version.match(/selfcustody\/.*/g)){
        
        const domain = 'https://github.com'
        let baseUrl = result.values.version.replace(/tag/g, 'download')
        let version = baseUrl.split('download/')[1]
        baseUrl = baseUrl.split(`/${version}`)[0]
        const resource =`${version}/krux-${version}.zip`

        await messages.add(data, `Checking ${domain}/${baseUrl}/${resource}`)
        await window.api.invoke('krux:check:resource', {
          from: result.from,
          baseUrl: `${domain}/${baseUrl}`,
          resource: resource
        })
      }

      // or test (.bin -> .kboot -> .kfpkg -> ktool)
      if (result.values.version.match(/odudex\/krux_binaries/g)){
        
        const domain = 'https://raw.githubusercontent.com'
        let baseUrl = result.values.version
        const resource = `main/${result.values.device}/firmware.bin`

        await messages.add(data, `Checking ${domain}/${baseUrl}/${resource}`)
        await window.api.invoke('krux:check:resource', {
          from: result.from,
          baseUrl: domain,
          resource: `${baseUrl}/${resource}`
        })
      }
      setMainData(data, result)
    }

    // When user came from .zip file and will check for .zip.sha256.txt file
    if (result.from.match(/^WarningDownload::.*.zip$/)) {
      setMainData(data, result)
      messages.clean(data)
      const domain = 'https://github.com'
      let baseUrl = result.values.version.replace(/tag/g, 'download')
      let version = baseUrl.split('download/')[1]
      baseUrl = baseUrl.split(`/${version}`)[0]
      
      const resource =`${version}/krux-${version}.zip.sha256.txt`
      await messages.add(data, `Checking ${domain}/${baseUrl}/${resource}`)
      await window.api.invoke('krux:check:resource', {
        from: result.from,
        baseUrl: `${domain}/${baseUrl}`,
        resource: resource
      })   
    }

    // When user came from .zip.sha256.txt file and will check for .zip.sig file
    if (result.from.match(/^WarningDownload::.*.zip.sha256.txt$/)) {
      setMainData(data, result)
      messages.clean(data)
      const domain = 'https://github.com'
      let baseUrl = result.values.version.replace(/tag/g, 'download')
      let version = baseUrl.split('download/')[1]
      baseUrl = baseUrl.split(`/${version}`)[0]
      
      const resource =`${version}/krux-${version}.zip.sig`
      await messages.add(data, `Checking ${domain}/${baseUrl}/${resource}`)
      await window.api.invoke('krux:check:resource', {
        from: result.from,
        baseUrl: `${domain}/${baseUrl}`,
        resource: resource
      })   
    }

    // When user came from .zip.sig file and will check for .pem file
    if (result.from.match(/^WarningDownload::.*.zip.sig$/)) {
      setMainData(data, result)
      messages.clean(data)
      const domain = 'https://raw.githubusercontent.com'
      const baseUrl = 'selfcustody/krux'
      const resource = 'main/selfcustody.pem'

      await messages.add(data, `Checking ${domain}/${baseUrl}/${resource}`)
      await window.api.invoke('krux:check:resource', {
        from: result.from,
        baseUrl: `${domain}/${baseUrl}`,
        resource: resource
      })   
    }
    // When user came from .zip.sig file and will check for .pem file
    if (result.from.match(/^WarningDownload::.*.pem$/)) {
      setMainData(data, result)
      messages.clean(data)
      await window.api.invoke('krux:change:page', { page: 'CheckVerifyOfficialRelease' })
    }

    if (result.from === 'CheckVerifyOfficialRelease') {
      await window.api.invoke('krux:verify:releases:hash')
    }

    if ( result.from === 'VerifiedOfficialRelease') {
      setMainData(data, result)
    }

    if ( result.from === 'DownloadTestKtool') {
      setMainData(data, result)
    }

    

    if ( result.from === 'ErrorMsg') {
      setMainData(data, result)
    }

    if (result.from.match(/CheckResourcesOfficialRelease*/g)) {
      let domain, baseUrl, resource;
      if (
        result.from === 'CheckResourcesOfficialReleaseZip' ||
        result.from === 'CheckResourcesOfficialReleaseSha256' ||
        result.from === 'CheckResourcesOfficialReleaseSig'
      ) {
        // https://github.com/selfcustody/krux/releases/download/{{ version }}/krux-{{ version }}.zip
    
        domain = 'https://github.com'
    
        baseUrl = result.values.version.replace(/tag/g, 'download')
        const version = baseUrl.split('download/')[1]
        baseUrl = baseUrl.split(`/${version}`)[0]
    
        if (result.from.match(/Zip$/g)) {
          resource =`${version}/krux-${version}.zip`
        }
        if (result.from.match(/Sha256$/g)) {
          resource =`${version}/krux-${version}.zip.sha256.txt`
        }
        if (result.from.match(/Sig$/g)) {
          resource =`${version}/krux-${version}.zip.sig`
        }
      }
      if (result.from === 'CheckResourcesOfficialReleasePem') {
        domain = 'https://raw.githubusercontent.com'
        baseUrl = 'selfcustody/krux'
        resource = 'main/selfcustody.pem'
      }
      await window.api.invoke('krux:check:resource', {
        from: result.from,
        baseUrl: `${domain}/${baseUrl}`,
        resource: resource
      })
    }

    if (result.from.match(/CheckResourcesTest*/g)) {
      let resource;
      const domain = 'https://raw.githubusercontent.com'
      if (result.from === 'CheckResourcesTestFirmware') {
        if (!result.values.device) {
          data.value = { stack: new Error('Device not provided') }
          await window.api.invoke('krux:change:page', { page: 'ErrorMsg'})
        }
        resource = `${result.values.device}/firmware.bin`
      }
      if (result.from === 'CheckResourcesTestKboot') {
        if (!result.values.device) {
          data.value = { stack: new Error('Device not provided') }
          await window.api.invoke('krux:change:page', { page: 'ErrorMsg'})
        }
        resource = `${result.values.device}/kboot.kfpkg`
      }
      if (result.from === 'CheckResourcesTestKtool') {
        if (!result.values.os) {
          data.value = { stack: new Error('OS not provided') }
          await window.api.invoke('krux:change:page', { page: 'ErrorMsg'})
        }
        let ktool
        if (result.values.os === 'linux') {
          resource = `ktool-linux`
        }
        if (result.values.os === 'win32') {
          resource = `ktool-win.exe`
        }
        if (result.values.os === 'darwin') {
          if (result.values.isMac10) {
            resource = `ktool-mac-10`
          } else {
            resource = `ktool-mac`
          }
        }
      }
      await window.api.invoke('krux:check:resource', {
        from: result.from,
        baseUrl: `${domain}/${result.values.version}/main`,
        resource: resource
      })
    }
  }
}