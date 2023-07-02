import { Ref } from "vue";
import addMessage from './addMessage'

export default function (data: Ref<Record<string, any>>): Function {
  return async function (_: Event, result: Record<'from' | 'message', any>): Promise<void> {
    if (result.from === 'KruxInstallerLogo') {
      await addMessage(data, result.message)
      await window.api.invoke('krux:change:page', { page: 'Main', from: result.from })
      data.value.messages = []
      data.value.indexes = [] 
    }
  }
}