import { Ref } from "vue"

/**
 * Setup `data` for SelectDevice and SelectVersion Pages
 * @param data 
 * @returns 
 */
export default function (data: Ref<Record<string, any>>): Function {
  return function (_: Event, result: Record<'from' | 'key' | 'value', any>) {
    if (
      result.from === 'SelectDevice'
    ) {
      data.value = {
        device: result.value,
        version: data.value.version,
        ktool: data.value.ktool
      }
    }
    if (
      result.from === 'SelectVersion'
    ) {
      data.value = {
        device: result.value,
        version: data.value.version,
        ktool: data.value.ktool
      }
    }
  }
}