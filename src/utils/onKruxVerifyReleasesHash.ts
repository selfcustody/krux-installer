import { Ref } from "vue"

/**
 * Store result of sha256sum verification in `data` 
 * and invoke signature verification 
 * 
 * @param data 
 * @returns Function
 */
export default function (data: Ref<Record<string, any>>): Function {
  return async function (_: Event, result: Record<'name' | 'value', string>[]): Promise<void> {
    data.value.hash = result
    await window.api.invoke('krux:verify:releases:sign')
  }
}