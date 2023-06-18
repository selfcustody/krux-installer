import { Ref } from "vue";

const KTOOLS = [
  { os: 'linux', isMac10: false, ktool: 'ktool-linux' },
  { os: 'win32', isMac10: false, ktool: 'ktool-win.exe' },
  { os: 'darwin', isMac10: false, ktool: 'ktool-mac' },
  { os: 'darwin', isMac10: true, ktool: 'ktool-mac-10' },
] 

/**
 * Set the `data` variable appropriately on the Main page with  the `device`, `version` and `ktool` properties;
 * @example
 * ```
 * import onGetDataToMainPage from './utils/onGetDataToMainPage'
 * 
 * const data: Ref<Record<string, any>> = ref({})
 * 
 * window.api.onSuccess('krux:store:get', async (_: Event, result: Record<'from' | 'key' | 'values', any>) => {
 *  onGetDataToMainPage(data, result, {
 *     when: [ 'Pages List', 'that you want the', 'configuration to take place' ]
 *   ]
 * })
 * ```
 * @param data 
 * @param options
 */
export default function (
  data: Ref<Record<'device' | 'version' | 'ktool', string>>,
  result: Record<'from' | 'key' | 'values', any>,
  options: Record<'when', string[]>
): void {
  data.value = { device: '', version: '', ktool: ''}
  options.when.forEach(function (page) {
    if (result.from === page) {
      data.value.device = result.values.device
      data.value.version = result.values.version
      KTOOLS.forEach(function(k) {
        if ( result.values.os === k.os && result.values.isMac10 === k.isMac10) {
          data.value.ktool = k.ktool 
        }
      })
    }
  })
}