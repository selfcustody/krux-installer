import { Ref } from "vue"

export default async function onCameFromWarningDownload (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>
): Promise<void> {

  if (result.from === 'WarningDownload') {
    data.value = {
      baseUrl: result.baseUrl,
      resourceFrom: result.resourceFrom,
      resourceTo: result.resourceTo,
      progress: 0.0
    }
    await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleaseZip' })
  }
}