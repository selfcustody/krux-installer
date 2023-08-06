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

})
