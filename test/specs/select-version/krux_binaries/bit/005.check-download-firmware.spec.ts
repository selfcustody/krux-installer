import { exists, stat } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../../../package.json'
import formatBytes from '../../../format-bytes'

const existsAsync = promisify(exists)
const statAsync = promisify(stat)

// eslint-disable-next-line no-undef
describe('check downloaded \'odudex/krux_binaries/raw/main/maixpy_bit/firmware.bin\' on file system', () => {

  let api, firmware

  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
    api = await browser.electronAPI()
    firmware = join(api.documents, name, 'odudex', 'krux_binaries', 'raw', 'main', 'maixpy_bit', 'firmware.bin') 
  })
  
  // eslint-disable-next-line no-undef
  it('should have downloaded firmware file on disk', async () => {
    const firmwareExists = await existsAsync(firmware)
    expectChai(firmwareExists).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should downloaded firmware file on disk have correct size', async () => {
    const firmwareStat = await statAsync(firmware)
    const bytes = formatBytes(firmwareStat.size)
    expectChai(bytes).to.be.equal('1.73 MB')
  })
})