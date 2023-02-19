import { exists, stat } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../../../package.json'
import formatBytes from '../../../format-bytes'

const existsAsync = promisify(exists)
const statAsync = promisify(stat)

// eslint-disable-next-line no-undef
describe('check downloaded v22.08.0 zip release on file system', () => {

  let api, dir, zip

  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
    api = await browser.electronAPI()
    dir = join(api.documents, name, 'v22.08.0') 
    zip = join(dir, 'krux-v22.08.0.zip')
  })
  
  // eslint-disable-next-line no-undef
  it('should have downloaded release zip file on disk', async () => {
    const zipExists = await existsAsync(zip)
    expectChai(zipExists).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should downloaded release zip file on disk have correct size', async () => {
    const zip = join(dir, 'krux-v22.08.0.zip')
    const zipStat = await statAsync(zip)
    const bytes = formatBytes(zipStat.size)
    expectChai(bytes).to.be.equal('44.0 MB')
  })
})
