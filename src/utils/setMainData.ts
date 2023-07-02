import { Ref } from "vue"

export default function setMainData(
  data: Ref<Record<string,any>>,
  result: Record<'from' | 'key' | 'values', any>
): void {
  data.value.device = result.values.device
  data.value.version = result.values.version
  data.value.os = result.values.os
  data.value.isMac10 = result.values.isMac10
}