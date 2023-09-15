const { readdir, readFile } = require('fs/promises')
const { join } = require('path')
const expectChai = require('chai').expect
const { browser } = require('@wdio/globals')
const { describe, it } = require('mocha')
const { version } = require('../../../package.json')

describe('Check created configuration', () => {

  it('should \'appVersion\' property be equal to the defined in package.json', async () => {
    const api = await browser.electron.api() as Record<string, string>
    expectChai(api.store.appVersion).to.equal(version)
  })

  it('should \'resources\' property be properly set for the platform', async () => {
    const api = await browser.electron.api() as Record<string, string>
    let regexp: RegExp

    if (process.env.CI && process.env.GITHUB_ACTION) {
      if (process.platform === 'linux') {
        regexp = new RegExp(`/home/[a-zA-Z0-9/]+`, 'g')
        expectChai(api.store.resources).to.match(regexp)
      }
      if (process.platform === 'win32') {
        regexp = /[A-Z]:[a-zA-Z\\-]+/g
        expectChai(api.store.resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'darwin') {
        regexp = new RegExp('/Users/[a-zA-Z0-9/-]+', 'g')
        expectChai(api.store.resources).to.match(regexp as RegExp)
      }
    } else {
      const docs = 'Documents|Documentos|Documenten|Documenti|Unterlagen' 
      if (process.platform === 'linux') {
        regexp = new RegExp(`/home/[a-zA-Z0-9/]+/(${docs})`, 'g')
        expectChai(api.store.resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'win32') {
        regexp = new RegExp(`[A-Z]:\\Users\\[a-zA-Z0-9]+\\(${docs})\\${name}`, 'g')
        expectChai(api.store.resources).to.match(regexp as RegExp)
      }
      if (process.platform === 'darwin') {
        regexp = new RegExp(`/Users/[a-zA-Z0-9\/\-]+/(${docs})/${name}`, 'g')
        expectChai(api.store.resources).to.match(regexp as RegExp)
      }
    }
  })

  it('should \'os\' property be properly set for the platform', async () => {
    const api = await browser.electron.api() as Record<string, string>
    expectChai(api.store.os).to.equal(process.platform) 
  })

  it('should \'versions\' property to be an Array with 0 elements', async () => {
    const api = await browser.electron.api() as Record<string, string>
    expectChai(api.store.versions).to.be.an('Array')
    expectChai(api.store.versions.length).to.equal(0)
  })

  it('should \'version\' property to be equal \'Select version\'', async () => {
    const api = await browser.electron.api() as Record<string, string>
    expectChai(api.store.version).to.equal('Select version')
  })

  it('should \'device\' property to be equal \'Select device\'', async () => {
    const api = await browser.electron.api() as Record<string, string>
    expectChai(api.store.device).to.equal('Select device')
  })

  it('should \'sdcard\' property to be equal \'\'', async () => {
    const api = await browser.electron.api() as Record<string, string>
    expectChai(api.store.sdcard).to.equal('')
  })

  it('should \'showFlash\' property to be equal \'false\'', async () => {
    const api = await browser.electron.api() as Record<string, string>
    expectChai(api.store.showFlash).to.equal(false)
  })

})
