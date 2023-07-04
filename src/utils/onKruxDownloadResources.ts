import { Ref } from "vue"
import delay from "./delay"

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
    await delay(2000)
    await window.api.invoke('krux:store:get', {
      from: result.from,
      keys: ['device', 'version', 'os', 'isMac10']
    })
  }
}