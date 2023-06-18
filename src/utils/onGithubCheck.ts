import { Ref } from "vue"

/**
 * Changes data of choosen component to those
 * that fit on GithubChecker page context and redirects 
 * the page to SelectVersion page
 * @param data 
 * @param result 
 */
export default async function (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'key' | 'value', any>
): Promise<void> {
  if (result.from === 'GithubChecker') {
    data.value = {
      versions: result.value
    }
    await window.api.invoke('krux:change:page', { page: 'SelectVersion' })
  }
}