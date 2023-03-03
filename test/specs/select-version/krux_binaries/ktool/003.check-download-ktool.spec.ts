import { readFile } from 'fs'
import { exists, stat } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name } from '../../../../../package.json'
import formatBytes from '../../../format-bytes'

const readFileAsync = promisify(readFile)
const existsAsync = promisify(exists)
const statAsync = promisify(stat)

// eslint-disable-next-line no-undef
describe('check downloaded \'odudex/krux_binaries/raw/main/ktool-<linux|win.exe|mac-10|mac>\' on file system', () => {

  let api, ktool, config

  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
    api = await browser.electronAPI()
    const configPath = join(api.appData, name, 'config.json') 
    const configString = await readFileAsync(configPath, 'utf8')
    config = JSON.parse(configString) 
    
    if (config.os === 'linux') {
      ktool = join(api.documents, name, 'odudex', 'krux_binaries', 'raw', 'main', 'ktool-linux') 
    }

    if (config.os === 'win32') {
      ktool = join(api.documents, name, 'odudex', 'krux_binaries', 'raw', 'main', 'ktool-win.exe') 
    }

    if (config.os === 'darwin' && config.isMac10) {
      ktool = join(api.documents, name, 'odudex', 'krux_binaries', 'raw', 'main', 'ktool-mac-10') 
    }

    if (config.os === 'darwin' && !config.isMac10) {
      ktool = join(api.documents, name, 'odudex', 'krux_binaries', 'raw', 'main', 'ktool-mac') 
    }

  })
  
  // eslint-disable-next-line no-undef
  it('should have downloaded ktool file on disk', async () => {
    const ktoolExists = await existsAsync(ktool)
    expectChai(ktoolExists).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should downloaded ktool on disk have correct size', async () => {
    const ktoolStat = await statAsync(ktool)
    const bytes = formatBytes(ktoolStat.size)
    
    if (config.os === 'linux') {
      expectChai(bytes).to.be.equal('14.0 MB')
    }

    if (config.os === 'win32') {
      expectChai(bytes).to.be.equal('6.53 MB')
    }

    if (config.os === 'darwin') { 
      expectChai(bytes).to.be.equal('6.02 MB')
    }
  })
})
