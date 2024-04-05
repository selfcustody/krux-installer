import { Ref } from "vue"

/**
 * Generalized Procedure to redirects to ErrorMsg page
 * @param _ 
 * @param result 
 */
export default function (data: Ref<Record<string, any>>): Function {
  return async function (_: Event, result: Record<'name' | 'message' | 'stack', any>): Promise<void>  {
    data.value = {
      ...result,
      backTo: 'Main'
    }
    if (data.value.output) {
      data.value.output = ""
    }
    await window.api.invoke('krux:change:page', { page: 'ErrorMsg' })
  }
}
