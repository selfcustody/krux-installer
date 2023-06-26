import { Ref } from "vue"

/**
 * Setup `data` and/or redirects to a `page`, or invoke another api call;
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
 * ### CheckResources
 * 
 * When user click `Select version` button, it will need to decide wheather go to official release
 * or odudex's experimental release. After,it will need to check if the resource exist. If not exist,
 * redirect to download pages; if exist, redirect to warning page.
 * 
 * @param data 
 * @param options
 * @returns Promise<void>
 */
export default function onKruxStoreGet (data: Ref<Record<string, any>>): Function{
  return async function (_: Event, result: Record<'from' | 'key' | 'values', any>): Promise<void> {
    // # Main page
    if (
      result.from === 'KruxInstallerLogo' ||
      result.from === 'SelectVersion' || 
      result.from === 'VerifiedOfficialRelease' || 
      result.from === 'DownloadTestKtool' ||
      result.from === 'WarningDownload' || 
      result.from === 'ErrorMsg'
    ) {
      data.value.device = result.values.device
      data.value.version = result.values.version
      if (result.values.os === 'linux') {
        data.value.ktool === 'ktool-linux'
      }
      if (result.values.os === 'win32') {
        data.value.ktool === 'ktool-win.exe'
      }
      if (result.values.os === 'darwin' && !result.values.isMac10) {
        data.value.ktool === 'ktool-mac'
      }
      if (result.values.os === 'darwin' && result.values.isMac10) {
        data.value.ktool === 'ktool-mac-10'
      }
    }

    // ### CheckResources
    if (result.from === 'CheckResources') {
      let page = ''
      let checked = false
      if (result.values.version.match(/selfcustody\/.*/g)){
        checked = true
        page = 'CheckResourcesOfficialReleaseZip'
      }
      if (result.values.version.match(/odudex\/.*/g)){
        checked = true
        page = 'CheckResourcesTestFirmware'
      }
      if (!checked) {
        page = 'ErrorMsg'
      }
      await window.api.invoke('krux:change:page', { page: page })
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

    if (result.from === 'CheckVerifyOfficialRelease') {
      await window.api.invoke('krux:verify:releases:hash')
    }
  }
}