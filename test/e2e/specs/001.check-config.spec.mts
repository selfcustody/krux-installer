import { expect } from 'chai'
import { browser } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'
const { version } = createRequire(import.meta.url)('../../../package.json')

describe('Check created configuration', () => {

  it('\'appVersion\' property should be equal to the value defined in package.json', async () => {
    const appVersion = await browser.electron.execute(function (electron) {
      return electron.app.getVersion()
    })
    expect(appVersion).to.equal(version)
  })

  it('\'resources\' property should be properly set for the platform', async () => {
    const resources = await browser.electron.execute(function (electron) {
      return electron.app.store.get('resources')
    })

    let regexp: RegExp

    if (process.env.CI && process.env.GITHUB_ACTION) {
      if (process.platform === 'linux') {
        regexp = new RegExp(`/home/[a-zA-Z0-9/]+`, 'g')
        expect(resources).to.match(regexp)
      }
      if (process.platform === 'win32') {
        regexp = /[A-Z]:[a-zA-Z\\-]+/g
        expect(resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'darwin') {
        regexp = new RegExp('/Users/[a-zA-Z0-9/-]+', 'g')
        expect(resources).to.match(regexp as RegExp)
      }
    } else {
      const docs = 'Documents|Documentos|Documenten|Documenti|Unterlagen' 
      if (process.platform === 'linux') {
        regexp = new RegExp(`/home/[a-zA-Z0-9/]+/(${docs})`, 'g')
        expect(resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'win32') {
        regexp = new RegExp(`[A-Z]:\\Users\\[a-zA-Z0-9]+\\(${docs})\\${name}`, 'g')
        expect(resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'darwin') {
        regexp = new RegExp(`/Users/[a-zA-Z0-9\/\-]+/(${docs})/${name}`, 'g')
        expect(resources).to.match(regexp as RegExp)
      }
    }
  })

  it('\'os\' property should be properly set for the platform', async () => {
    const os = await browser.electron.execute(function (electron) {
      return electron.app.store.get('os')
    })
    expect(os).to.equal(process.platform) 
  })

  it('\'versions\' property should be an Array with 0 elements', async () => {
    const versions = await browser.electron.execute(function (electron) {
      return electron.app.store.get('versions')
    })
    expect(versions).to.be.an('Array')
    expect(versions.length).to.equal(0)
  })

  it('\'version\' property should be equal to \'Select version\'', async () => {
    const version = await browser.electron.execute(function (electron) {
      return electron.app.store.get('version')
    })
    expect(version).to.equal('Select version')
  })

  it('\'device\' property should be equal to \'Select device\'', async () => {
    const device = await browser.electron.execute(function (electron) {
      return electron.app.store.get('device')
    })
    expect(device).to.equal('Select device')
  })

  it('\'device\' property should be equal to \'Select device\'', async () => {
    const showFlash = await browser.electron.execute(function (electron) {
      return electron.app.store.get('showFlash')
    })
    expect(showFlash).to.equal(false)
  })

})
