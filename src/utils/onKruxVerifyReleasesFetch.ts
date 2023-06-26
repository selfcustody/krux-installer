import { Ref } from "vue"

export default function (data: Ref<Record<string, any>>): Function { 
  return async function (_event: Event, result: Record<'from' | 'key' | 'value', any>): Promise<void> {
    if (result.from === 'GithubChecker') {
      data.value = {
        versions: result.value
      }
      await window.api.invoke('krux:change:page', { page: 'SelectVersion' })
    }
  }
}