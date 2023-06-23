import { Ref } from "vue"

export default async function (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>,
  options: Record<'from' | 'proceedTo' | 'abbreviated' , string | boolean>
): Promise<void> {
  if (result.from === `CheckResourcesOfficialRelease${options.from}` ) {
    if (result.exists) {
      data.value = {
        baseUrl: result.baseUrl,
        resourceFrom: result.resourceFrom,
        resourceTo: result.resourceTo,
        proceedTo: options.abbreviated ? `CheckResourcesOfficialRelease${options.proceedTo}` : options.proceedTo, 
        backTo: 'GithubChecker'
      }
      await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
    } else {
      
      data.value = {
        baseUrl: result.baseUrl,
        resourceFrom: result.resourceFrom,
        resourceTo: result.resourceTo,
        progress: 0.0
      }
      await window.api.invoke('krux:change:page', { page: `DownloadOfficialRelease${options.from}`  })
    }
  }
}