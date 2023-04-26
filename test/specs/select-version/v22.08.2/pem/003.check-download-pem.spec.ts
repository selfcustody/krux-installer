import { exists, stat, readFile } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../../../package.json'
import formatBytes from '../../../format-bytes'

const existsAsync = promisify(exists)
const statAsync = promisify(stat)
const readFileAsync = promisify(readFile)

// eslint-disable-next-line no-undef
describe('check downloaded public key certificate on file system', () => {

  let api, dir, pem

  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
    api = await browser.electron.api()
    dir = join(api.documents, name, 'main') 
    pem = join(dir, 'selfcustody.pem')
  })
  
  // eslint-disable-next-line no-undef
  it('should have downloaded public key certificate file on disk', async () => {
    const pemExists = await existsAsync(pem)
    expectChai(pemExists).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should downloaded public key certificate file on disk have correct size', async () => {
    const pemStat = await statAsync(pem)
    const bytes = formatBytes(pemStat.size)
    expectChai(bytes).to.be.equal('130 Bytes')
  })

  // eslint-disable-next-line no-undef
  it('should downloaded public key certificate file on disk have correct content', async () => {
    const pemContent = (await readFileAsync(pem, 'utf8')).split('\n')
    expectChai(pemContent[0]).to.be.equal('-----BEGIN PUBLIC KEY-----')
    expectChai(pemContent[1]).to.be.equal('MDYwEAYHKoZIzj0CAQYFK4EEAAoDIgADM56IMVfkWJHmHKnfTNO7iV7zLUdbjnk1')
    expectChai(pemContent[2]).to.be.equal('WeoQo2dmaJs=')
    expectChai(pemContent[3]).to.be.equal('-----END PUBLIC KEY-----')
  })
})
