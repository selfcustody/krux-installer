import { Ref } from "vue"

export default async function (
  data: Ref<Record<string, any>>,
  result: Record<'command' | 'sign', any>
): Promise<void> {
  data.value.command = result.command
  data.value.sign = result.sign
  await window.api.invoke('krux:change:page', { page: 'VerifiedOfficialRelease' })
}