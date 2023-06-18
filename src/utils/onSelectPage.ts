import { Ref } from "vue";

/**
 * Changes data of choosen component to those
 * that fit on SelectDevice | SelectVersion page context
 * @param data 
 * @param result 
 * @param option 
 */
export default function (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'key' | 'value', any>,
  option: Record<'page', 'SelectDevice' | 'SelectVersion'>
) {
  if (result.from === option.page) {
    data.value = {
      device: result.value,
      version: data.value.version,
      ktool: data.value.ktool
    }
  }
}