/**
 * Verify integrity of downloaded `zip`
 * with sha256sum and provided `sha256.txt` file
 * @param result 
 */
export default async function (result: Record<'from' | 'key' | 'values', any>): Promise<void> {
  if (result.from === 'CheckVerifyOfficialRelease') {
    await window.api.invoke('krux:verify:releases:hash')
  }
}