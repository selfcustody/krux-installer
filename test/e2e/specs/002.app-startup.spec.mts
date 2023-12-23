import { expect } from 'chai'
import { browser } from '@wdio/globals'
import { describe, it } from 'mocha'

describe('KruxInstaller start up', () => {

  it('should be ready', async () => {
    const isReady = await browser.electron.execute(function (electron) {
      return electron.app.isReady()
    })
    expect(isReady).to.be.equal(true)
  })

  it('application name should be correct', async () => {
    const name = await browser.electron.execute(function (electron) {
      return electron.app.getName()
    })
    expect(name).to.be.equal('krux-installer')
  })

  it('application version should be correct', async () => {
    const version = await browser.electron.execute(function (electron) {
      return electron.app.getVersion()
    })
    expect(version).to.be.equal('0.0.1')
  })

})
