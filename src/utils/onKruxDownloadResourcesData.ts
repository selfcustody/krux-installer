import { Ref } from "vue"

/**
 * Stream progress when download resources
 * 
 * @param data 
 * @returns Function
 */
export default function (data: Ref<Record<any, string>>): Function {
  return function (_: Event, result: string) {
   data.value.progress = result
 }
}