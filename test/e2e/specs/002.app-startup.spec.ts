const expectChai = require('chai').expect
const { describe, it } = require('mocha')
const { browser } = require('@wdio/globals')
const pkg = require('../../../package.json')

describe('KruxInstaller start up', () => {

  it('should be ready', async () => {
    const isReady = await browser.electron.app('isReady') as boolean
    expectChai(isReady).to.be.equal(true)
  })

  it('should name be correct', async () => {
    const name = await browser.electron.app('getName') as string
    expectChai(name).to.be.equal(pkg.name)
  })

  it('should version be correct', async () => {
    const version = await browser.electron.app('getVersion') as string
    expectChai(version).to.be.equal(pkg.version)
  })

})
