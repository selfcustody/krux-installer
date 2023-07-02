import { Ref } from "vue"
import setMainData from './setMainData'

/**
 * Setup `data` for SelectDevice and SelectVersion Pages
 * @param data 
 * @returns 
 */
export default function (data: Ref<Record<string, any>>): Function {
  return async function (_: Event, result: Record<'from' | 'key' | 'value', any>) {
    if (result.from === 'SelectDevice') {
      await window.api.invoke('krux:store:get', { from: result.from, keys: ['device', 'version', 'os', 'isMac10'] })
    }
    if (result.from === 'SelectVersion') {
      await window.api.invoke('krux:store:get', { from: result.from, keys: ['device', 'version', 'os', 'isMac10'] })
    }
  }
}