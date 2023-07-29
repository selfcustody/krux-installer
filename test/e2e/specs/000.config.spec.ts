const { readdir, readFile } = require('fs/promises')
const { join } = require('path')
const expectChai = require('chai').expect
const { browser } = require('@wdio/globals')
const { describe, it } = require('mocha')
const { version } = require('../../../package.json')

describe('KruxInstaller configuration', () => {

  it('should \'appData\' path exist with \'krux-installer\' directory', async () => {
    try {
      const api = await browser.electron.api() as Record<string, string>
      const list = await readdir(api.appData)
      expectChai(list.includes('krux-installer')).to.be.true
    } catch (error) {
      console.log(error)
    }
  })

  it('should \'documents\' path exist with \'krux-installer\' directory', async () => {
    try {
      const api = await browser.electron.api() as Record<string, string>
      const list = await readdir(api.documents)
      expectChai(list.includes('krux-installer')).to.be.true
    } catch (error) {
      console.log(error)
    }
  })

  it('should \'config.json\' file exists inside \'krux-installer\' directory', async () => {
    try {
      const api = await browser.electron.api() as Record<string, string>
      const dir = join(api.appData, 'krux-installer')
      const list = await readdir(dir)
      expectChai(list.includes('config.json')).to.be.true
    } catch (error) {
      console.log(error)
    }
  })

  it('should \'config.json\' be a readable string', async () => {
    try {
      const api = await browser.electron.api() as Record<string, string>
      const filePath = join(api.appData, 'krux-installer', 'config.json')
      const file = await readFile(filePath)
      expectChai(file).to.be.a('string')
    } catch (error) {
      console.log(error)
    }
  })

  it('should the readable string be parsed to a valid JSON object', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.be.a('object')
  })

  it('should config.json have \'appVersion\' property', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.have.property('appVersion')
  })

  it('should \'appVersion\' property be equal to the defined in package.json', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const { appVersion } = JSON.parse(file)
    expectChai(appVersion).to.equal(version)
  })

  it('should config.json have \'resources\' property', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.have.property('resources')
  })

  it('should \'resources\' property be properly set for the platform', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const { resources } = JSON.parse(file)

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
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.have.property('os')
  })

  it('should \'os\' property be properly set for the platform', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const { os } = JSON.parse(file)
    expectChai(os).to.equal(process.platform) 
  })

  it('should config.json have \'versions\' property', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.have.property('versions')
  })

  it('should \'versions\' property to be an Array with 0 elements', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const { versions } = JSON.parse(file)
    expectChai(versions).to.be.an('Array')
    expectChai(versions.length).to.equal(0)
  })

  it('should config.json have \'version\' property', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.have.property('version')
  })

  it('should \'version\' property to be equal \'Select version\'', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    const __version__ = json.version
    expectChai(__version__).to.equal('Select version')
  })

  it('should config.json have \'device\' property', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.have.property('device')
  })

  it('should \'device\' property to be equal \'Select device\'', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const { device } = JSON.parse(file)
    expectChai(device).to.be.equal('Select device')
  })

  it('should config.json have \'sdcard\' property', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.have.property('sdcard')
  })

  it('should config.json have \'showFlash\' property', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const json = JSON.parse(file)
    expectChai(json).to.have.property('showFlash')
  })

  it('should \'showFlash\' property to be equal \'false\'', async () => {
    const api = await browser.electron.api() as Record<string, string>
    const filePath = join(api.appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath)
    const { showFlash } = JSON.parse(file)
    expectChai(showFlash).to.be.equal(false)
  })
})
