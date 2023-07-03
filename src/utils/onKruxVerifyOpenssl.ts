import { Ref } from "vue";
import messages from './messages'

export default function (data: Ref<Record<string, any>>): Function {
  return async function (_: Event, result: Record<'from' | 'message', any>): Promise<void> {
    if (result.from === 'KruxInstallerLogo') {
      await messages.add(data, result.message)
      await messages.close(data)
      await window.api.invoke('krux:change:page', { page: 'Main', from: result.from })
      messages.clean(data)
    }
  }
}