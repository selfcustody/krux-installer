/**
 * When user click `Select version` button,
 * it will need to decide wheather go to official release
 * or odudex's experimental release
 * @param result 
 */
export default async function (
  result: Record<'from' | 'key' | 'values', any>,
  options: Record<'match' | 'goto', RegExp | string | boolean>[] 
): Promise<void> {
  if (result.from === 'CheckResources') {
    let page = ''
    let checked = false
    options.forEach(function(o) {
      if (result.values.version.match(o.match)) {
        page = o.goto as string
        checked = true
      }
    })
    if (!checked) {
      page = 'ErrorMsg'
    }
    await window.api.invoke('krux:change:page', { page: page })
  }
}