const PAGES = [
  { from: 'CheckResourcesOfficialReleaseZip',    extension: 'zip'},
  { from: 'CheckResourcesOfficialReleaseSha256', extension: 'zip.sha256.txt'},
  { from: 'CheckResourcesOfficialReleaseSig',    extension: 'zip.sig'}
]

/**
 * Before check an official resource, verify if
 * it is the `zip`, `sha256.txt`, `sig` or `pem` file.
 * 
 * - If its `zip`, `sha256.txt`, `sig`:
 *   * the main domain is `https://github.com`;
 *   * the base url is `selfcustody/krux`
 *   * the resource can be  `${version}/krux-${version}.<zip | zip.sha256.txt | zip.sig>`
 * - If its `pem`:
 *   * the main domain is `https://raw.githubusercontent.com`;
 *   * the base url is `selfcustody/krux`
 *   * the resource is `main/selfcustody.pem`
 * @param result 
 */
export default async function (
  result: Record<'from' | 'key' | 'values', any>,
): Promise<void> {
  let domain = ''
  let baseUrl = ''
  let resource = ''

  if (
    result.from === 'CheckResourcesOfficialReleaseZip' ||
    result.from === 'CheckResourcesOfficialReleaseSha256' ||
    result.from === 'CheckResourcesOfficialReleaseSig'
  ) {
    // https://github.com/selfcustody/krux/releases/download/{{ version }}/krux-{{ version }}.zip

    domain = 'https://github.com'

    baseUrl = result.values.version.replace(/tag/g, 'download')
    const version = baseUrl.split('download/')[1]
    baseUrl = baseUrl.split(`/${version}`)[0]

    if (result.from.match(/Zip$/g)) {
      resource =`${version}/krux-${version}.zip`
    }
    if (result.from.match(/Sha256$/g)) {
      resource =`${version}/krux-${version}.zip.sha256.txt`
    }
    if (result.from.match(/Sig$/g)) {
      resource =`${version}/krux-${version}.zip.sig`
    }
  }
  if (result.from === 'CheckResourcesOfficialReleasePem') {
    domain = 'https://raw.githubusercontent.com'
    baseUrl = 'selfcustody/krux'
    resource = 'main/selfcustody.pem'
  }
  await window.api.invoke('krux:check:resource', {
    from: result.from,
    baseUrl: `${domain}/${baseUrl}`,
    resource: resource
  })
}