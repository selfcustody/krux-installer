import { exists, stat } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../package.json'
import formatBytes from '../format-bytes'

const existsAsync = promisify(exists)
const statAsync = promisify(stat)

// eslint-disable-next-line no-undef
describe('check downloaded zip release on file system', () => {

  let api, dir, sha256

  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
    api = await browser.electronAPI()
    dir = join(api.documents, name, 'v22.03.0') 
    sha256 = join(dir, 'krux-v22.03.0.zip.sha256.txt')
  })
  
  // eslint-disable-next-line no-undef
  it('should have downloaded release zip file on disk', async () => {
    const sha256Exists = await existsAsync(sha256)
    expectChai(sha256Exists).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should downloaded release zip file on disk have correct size', async () => {
    const sha256stat = await statAsync(sha256)
    const bytes = formatBytes(sha256stat.size)
    expectChai(bytes).to.be.equal('65 Bytes')
  })
})
