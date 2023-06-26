import { Ref } from "vue"

/**
 * When download finishes, redirect it:
 * - DownloadOfficialReleaseZip --> CheckResourcesOfficialReleaseSha256
 * - DownloadOfficialReleaseSha256 --> CheckResourcesOfficialReleaseSig
 * - DownloadOfficialReleaseSig --> CheckResourcesOfficialReleasePem
 * - DownloadOfficialReleasePem --> VerifyOfficialRelease
 * - DownloadTestFirmware --> CheckResourcesTestKboot
 * - DownloadTestKboot --> CheckResourcesTestKtool
 * - DownloadTestKtool --> Main
 * @param data 
 * @returns Function
 */
export default function (data: Ref<Record<any,string>>): Function {
  return async function (_: Event, result: Record<'from', string>): Promise<void> {
    let toPage = ''
    if (result.from === 'DownloadOfficialReleaseZip') {
      toPage = 'CheckResourcesOfficialReleaseSha256'
    }
    else if (result.from === 'DownloadOfficialReleaseSha256') {
      toPage = 'CheckResourcesOfficialReleaseSig'
    }
    else if (result.from === 'DownloadOfficialReleaseSig') {
      toPage = 'CheckResourcesOfficialReleasePem'
    }
    else if (result.from === 'DownloadOfficialReleasePem') {
      toPage = 'CheckVerifyOfficialRelease'
    }
    else if (result.from === 'DownloadTestFirmware') {
      toPage = 'CheckResourcesTestKboot'
    }
    else if (result.from === 'DownloadTestKboot') {
      toPage = 'CheckResourcesTestKtool'
    }
    else if (result.from === 'DownloadTestKtool') {
      await window.api.invoke('krux:store:get', {
        from: 'DownloadTestKtool',
        keys: ['device', 'version', 'os', 'isMac10']
      })
      toPage = 'Main'
    }
    else {
      throw new Error(`Not valid page: ${result.from}`); 
    }
    await window.api.invoke('krux:change:page', { page: toPage })
  }
}