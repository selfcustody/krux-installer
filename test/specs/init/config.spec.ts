import { exists, readFile } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { expect as expectChai } from 'chai'
import { name, version } from '../../../package.json'

const existsAsync = promisify(exists)
const readFileAsync = promisify(readFile)


// eslint-disable-next-line no-undef
describe('KruxInstaller configuration', () => {

  // eslint-disable-next-line no-undef
  it('should created a \'krux-installer\' folder in \'appData\' directory', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    expectChai(p).to.be.not.equal(undefined)
    expectChai(p).to.have.property('appData')
    expectChai(p.appData).to.be.a('string')

    const existsAppData = await existsAsync(p.appData)
    expectChai(existsAppData).to.be.equal(true)

    const kruxPath = join(p.appData, name)
    console.log(kruxPath)
    const existsKrux = await existsAsync(kruxPath)
    expectChai(existsKrux).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should created a config.json in \'krux-installer\' folder', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json')
    const configString = await readFileAsync(configPath, 'utf8')
    expectChai(configString).to.be.a('string')
  })

  // eslint-disable-next-line no-undef
  it('should config.json be initialized', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json') 
    const configString = await readFileAsync(configPath, 'utf8')
    const config = JSON.parse(configString) 
    expectChai(config).to.be.an('object')
  })

  // eslint-disable-next-line no-undef
  it('should config.json have \'appVersion\' property', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json')
    const configString = await readFileAsync(configPath, 'utf8')
    const config = JSON.parse(configString) 
    expectChai(config).to.have.property('appVersion', version)
  })

  // eslint-disable-next-line no-undef
  it('should config.json have \'resources\' property', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json')
    const configString = await readFileAsync(configPath, 'utf8')
    const config = JSON.parse(configString) 
    expectChai(config).to.have.property('resources')
   
    let regexp
    if (process.env.CI && process.env.GITHUB_ACTION) {
      if (process.platform === 'linux') {
        regexp = new RegExp(`/home/[a-zA-Z0-9/]+`, 'g')
      }
      if (process.platform === 'win32') {
        regexp = new RegExp(`[A-Z]:\\Users\\[a-zA-Z0-9]+`, 'g')
      }
      if (process.platform === 'darwin') {
        regexp = new RegExp(`/Users/[a-zA-Z0-9]+`, 'g')
      }
    } else {
      const docs = 'Documents|Documentos|Documenten|Documenti|Unterlagen' 
      if (process.platform === 'linux') {
        regexp = new RegExp(`/home/[a-zA-Z0-9/]+/(${docs})`, 'g')
      }
      if (process.platform === 'win32') {
        regexp = new RegExp(`[A-Z]:\\Users\\[a-zA-Z0-9]+\\(${docs})\\${name}`, 'g')
      }
      if (process.platform === 'darwin') {
        regexp = new RegExp(`/Users/[a-zA-Z0-9]+/(${docs})/${name}`, 'g')
      }
    }

    expectChai(config.resources).to.match(regexp)
    
  })

  // eslint-disable-next-line no-undef
  it('should config.json have \'os\' property', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json')
    const configString = await readFileAsync(configPath, 'utf8')
    const config = JSON.parse(configString) 
    expectChai(config).to.have.property('os', process.platform) 
  })

  // eslint-disable-next-line no-undef
  it('should config.json have \'versions\' property', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json')
    const configString = await readFileAsync(configPath, 'utf8')
    const config = JSON.parse(configString) 
    expectChai(config).to.have.property('versions')
    expectChai(config.versions).to.be.an('Array')
    expectChai(config.versions.length).to.equal(0)
  })

  // eslint-disable-next-line no-undef
  it('should config.json have \'version\' property', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json')
    const configString = await readFileAsync(configPath, 'utf8')
    const config = JSON.parse(configString) 
    expectChai(config).to.have.property('version', 'Select version')
  })

  // eslint-disable-next-line no-undef
  it('should config.json have \'device\' property', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json')
    const configString = await readFileAsync(configPath, 'utf8')
    const config = JSON.parse(configString) 
    expectChai(config).to.have.property('device', 'Select device')
  })

  // eslint-disable-next-line no-undef
  it('should config.json have \'sdcard\' property', async () => {
    // eslint-disable-next-line no-undef 
    const p = await browser.electronAPI()
    const configPath = join(p.appData, name, 'config.json') 
    const configString = await readFileAsync(configPath, 'utf8')
    const config = JSON.parse(configString) 
    expectChai(config).to.have.property('sdcard') 
  })
})
