import { Ref } from "vue"

export default function (data: Ref<Record<string, any>>): Function {
  return function (_: Event, result: Record<'showWipe', boolean>): void {
    data.value.showWipe = result.showWipe
  }
}
