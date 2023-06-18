import { Ref } from "vue";

export default async function (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>
): Promise<void> {
  if (result.from === 'CheckVerifyOfficialRelease') {
    data.value = {}
  }
}