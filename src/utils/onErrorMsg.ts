import { Ref } from "vue"

export default async function (
  data: Ref<Record<string, any>>,
  result: Record<'name' | 'message' | 'stack', any>
): Promise<void> {
  data.value = {
    ...result,
    backTo: 'Main'
  }
  await window.api.invoke('krux:change:page', { page: 'ErrorMsg' })
}