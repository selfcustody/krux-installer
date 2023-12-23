import { readdir, readFile } from 'fs/promises'
import { join } from 'path'
import { expect } from 'chai'
import { browser } from '@wdio/globals'
import { describe, it } from 'mocha'

describe('KruxInstaller configuration', () => {
  
  it('\'appData\' property should be a path that exist within \'krux-installer\' directory', async () => {
    const appData = await browser.electron.execute(function (electron) {
      return electron.app.getPath('appData')
    })
    const list = await readdir(appData)
    expect(list.includes('krux-installer')).to.be.true
  })

  it('\'config.json\' file should exists inside \'krux-installer\' directory', async () => {
    const appData = await browser.electron.execute(function (electron) {
      return electron.app.getPath('appData')
    })
    const dir = join(appData, 'krux-installer')
    const list = await readdir(dir)
    expect(list.includes('config.json')).to.be.true
  })

  it('\'config.json\' should be a readable string', async () => {
    const appData = await browser.electron.execute(function (electron) {
      return electron.app.getPath('appData')
    })
    const filePath = join(appData, 'krux-installer', 'config.json')
    const file = await readFile(filePath, 'utf-8')
    expect(file).to.be.a('string')
  })

})
