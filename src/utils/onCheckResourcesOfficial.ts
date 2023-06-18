const PAGES = [
  { from: 'CheckResourcesOfficialReleaseZip',    extension: 'zip'},
  { from: 'CheckResourcesOfficialReleaseSha256', extension: 'zip.sha256.txt'},
  { from: 'CheckResourcesOfficialReleaseSig',    extension: 'zip.sig'}
]

/**
 * Before check an official resource, verify if
 * it is the `zip`, `sha256.txt` or `sig`
 * @param result 
 */
export default async function (
  result: Record<'from' | 'key' | 'values', any>,
): Promise<void> {
  let baseUrl = ''
  let resource = ''

  PAGES.forEach(function(o) {
    if (result.from === o.from) {
      // https://github.com/selfcustody/krux/releases/download/{{ version }}/krux-{{ version }}.zip
      baseUrl = result.values.version.replace(/tag/g, 'download')
      const version = baseUrl.split('download/')[1]
      baseUrl = baseUrl.split(`/${version}`)[0]
      resource =`${version}/krux-${version}.${o.extension}`
    }
  })
  if (result.from === 'CheckResourcesOfficialReleasePem') {
    baseUrl = 'selfcustody/krux'
    resource = 'main/selfcustody.pem'
  }
  await window.api.invoke('krux:check:resource', {
    from: result.from,
    baseUrl: baseUrl,
    resource: resource
  })
}