import { exists, stat } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../../../package.json'
import formatBytes from '../../../format-bytes'

const existsAsync = promisify(exists)
const statAsync = promisify(stat)

// eslint-disable-next-line no-undef
describe('check downloaded odudex \'maixpy_m5stickv\' firmware on file system', () => {

  let api, firmware

  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
    api = await browser.electronAPI()
    firmware = join(api.documents, name, 'odudex', 'krux_binaries', 'raw', 'main', 'maixpy_m5stickv', 'firmware.bin') 
  })
  
  // eslint-disable-next-line no-undef
  it('should have downloaded release zip file on disk', async () => {
    const firmwareExists = await existsAsync(firmware)
    expectChai(firmwareExists).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should downloaded firmware file on disk have correct size', async () => {
    const firmwareStat = await statAsync(firmware)
    const bytes = formatBytes(firmwareStat.size)
    expectChai(bytes).to.be.equal('1.7 MB')
  })
})
