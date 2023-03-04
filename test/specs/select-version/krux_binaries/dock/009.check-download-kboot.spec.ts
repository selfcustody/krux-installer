import { exists, stat } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../../../package.json'
import formatBytes from '../../../format-bytes'

const existsAsync = promisify(exists)
const statAsync = promisify(stat)

// eslint-disable-next-line no-undef
describe('check downloaded \'odudex/krux_binaries/raw/main/maixpy_dock/kboot.kfpkg\' on file system', () => {

  let api, kboot

  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
    api = await browser.electronAPI()
    kboot = join(api.documents, name, 'odudex', 'krux_binaries', 'raw', 'main', 'maixpy_dock', 'kboot.kfpkg') 
  })
  
  // eslint-disable-next-line no-undef
  it('should have downloaded kboot.kfpkg file on disk', async () => {
    const kbootExists = await existsAsync(kboot)
    expectChai(kbootExists).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should downloaded kboot file on disk have correct size', async () => {
    const kbootStat = await statAsync(kboot)
    const bytes = formatBytes(kbootStat.size)
    expectChai(bytes).to.be.equal('889.8 KB')
  })
})
