import { Ref } from "vue";
import delay from './delay'

export default function (data: Ref<Record<string, any>>): Function {
  return async function (_: Event, result: Record<'from' | 'message', any>): Promise<void> {
    if (result.from === 'KruxInstallerLogo') {
      data.value.messages.push(result.message)
      data.value.indexes.push(0)
      await delay(30)
      data.value.indexes[data.value.indexes.length - 1] += 1
      await delay(3000)
      delete data.value.messages
      await window.api.invoke('krux:change:page', { page: 'Main' })
      
    }
  }
}