import { Ref } from "vue";

export default function (data: Ref<Record<string, any>>): Function {
  return function (_: Event, result: Record<'from' | 'message', any>): void {
    if (result.from === 'App') {
      data.value.opensslMsg = result.message
    }
  }
}