import { Ref } from "vue"

export default async function (
  data: Ref<Record<string, any>>,
  result: Record<'name' | 'value', string>[]
): Promise<void> {
  data.value.hash = result
  await window.api.invoke('krux:verify:releases:sign')
}