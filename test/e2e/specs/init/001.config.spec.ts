import { expect as expectChai } from 'chai'
import createDebug from 'debug'
import { version } from '../../../../package.json';
import {
  existsAsync,
  getAPI,
  getAppDataPath,
  getAppDataNamePath,
  getConfigPath,
  getConfigString,
  getConfigObject
} from '../../utils'

const debug = createDebug('krux:wdio:e2e:config')


describe('KruxInstaller configuration', () => {

  it('should be able to get wdio API', async () => {
    const api = await getAPI()
    expectChai(api).to.be.not.equal(undefined)
    expectChai(api).to.have.property('appData')
    expectChai(api.appData).to.be.a('string')
  })

  it('should \'appData\' path exists', async () => {
    const apiDataPath = await getAppDataPath()
    const existsAppDataPath= await existsAsync(apiDataPath)
    expectChai(existsAppDataPath).to.be.equal(true)
  })

  it('should \'krux-installer\' directory exists inside \'appData\'', async () => {
    const apiDataNamePath = await getAppDataNamePath()
    const existsAppDataNamePath= await existsAsync(apiDataNamePath)
    expectChai(existsAppDataNamePath).to.be.equal(true)
  })

  it('should \'config.json\' file exists inside \'krux-installer\' directory', async () => {
    const configPath = await getConfigPath()
    debug(`Config:\n${configPath}`)
    const existsconfigPath= await existsAsync(configPath)
    expectChai(existsconfigPath).to.be.equal(true)
  })

  it('should \'config.json\' be a readable string', async () => {
    const configString = await getConfigString()
    expectChai(configString).to.be.a('string')
  })

  it('should the readable string be parsed to a valid JSON object', async () => {
    const configObject = await getConfigObject()
    debug(configObject)
    expectChai(configObject).to.be.a('object')
  })

  it('should config.json have \'appVersion\' property', async () => {
    const configObject = await getConfigObject()
    expectChai(configObject).to.have.property('appVersion')
  })

  it('should \'appVersion\' property be equal to the defined in package.json', async () => {
    const { appVersion } = await getConfigObject()
    expectChai(appVersion).to.equal(version)
  })

  it('should config.json have \'resources\' property', async () => {
    const configObject = await getConfigObject()
    expectChai(configObject).to.have.property('resources')
  })

  it('should \'resources\' property be properly set for the platform', async () => {
    const { resources } = await getConfigObject()

    let regexp: RegExp

    if (process.env.CI && process.env.GITHUB_ACTION) {
      if (process.platform === 'linux') {
        regexp = new RegExp(`/home/[a-zA-Z0-9/]+`, 'g')
        expectChai(resources).to.match(regexp)
      }
      if (process.platform === 'win32') {
        regexp = /[A-Z]:[a-zA-Z\\-]+/g
        expectChai(resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'darwin') {
        regexp = new RegExp(`/Users/[a-zA-Z0-9]+`, 'g')
        expectChai(resources).to.match(regexp as RegExp)
      }
    } else {
      const docs = 'Documents|Documentos|Documenten|Documenti|Unterlagen' 
      if (process.platform === 'linux') {
        regexp = new RegExp(`/home/[a-zA-Z0-9/]+/(${docs})`, 'g')
        expectChai(resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'win32') {
        regexp = new RegExp(`[A-Z]:\\Users\\[a-zA-Z0-9]+\\(${docs})\\${name}`, 'g')
        expectChai(resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'darwin') {
        regexp = new RegExp(`/Users/[a-zA-Z0-9]+/(${docs})/${name}`, 'g')
        expectChai(resources).to.match(regexp as RegExp)
      }
    }
  })

  it('should config.json have \'os\' property', async () => {
    const configObject = await getConfigObject()
    expectChai(configObject).to.have.property('os')
  })

  it('should \'os\' property be properly set for the platform', async () => {
    const { os } = await getConfigObject()
    expectChai(os).to.equal(process.platform) 
  })

  it('should config.json have \'versions\' property', async () => {
    const configObject = await getConfigObject()
    expectChai(configObject).to.have.property('versions')
  })

  it('should \'versions\' property to be an Array with 0 elements', async () => {
    const { versions } = await getConfigObject()
    expectChai(versions).to.be.an('Array')
    expectChai(versions.length).to.equal(0)
  })

  it('should config.json have \'version\' property', async () => {
    const configObject = await getConfigObject()
    expectChai(configObject).to.have.property('version')
  })

  it('should \'version\' property to be equal \'Select version\'', async () => {
    const configObject = await getConfigObject()
    const __version__ = configObject.version
    expectChai(__version__).to.equal('Select version')
  })

  it('should config.json have \'device\' property', async () => {
    const configObject = await getConfigObject()
    expectChai(configObject).to.have.property('device')
  })

  it('should \'device\' property to be equal \'Select device\'', async () => {
    const { device } = await getConfigObject()
    expectChai(device).to.have.property('device', 'Select device')
  })

  it('should config.json have \'sdcard\' property', async () => {
    const { sdcard } = await getConfigObject()
    expectChai(sdcard).to.have.property('sdcard')
  })
})
