import { Ref } from "vue"

export default function (data: Ref<Record<string, any>>): Function {
  return async function (
    _: Event,
    result: Record<'showFlash', any>
  ): Promise<void> {
    data.value.showFlash = result.showFlash
  }
}