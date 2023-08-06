const { createRequire } = require('module')
const expectChai = require('chai').expect
const expectWDIO = require('@wdio/globals').expect
const { describe, it } = require('mocha')
const {
  isAppReady,
  getAppName,
  getAppVersion
} = require('../utils')

const App = require('../pageobjects/app.page')
const pkg = require('../../../package.json')

describe('KruxInstaller initialization', () => {

  it('should be ready', async () => {
    const isReady = await isAppReady()
    expectChai(isReady).to.be.equal(true)
  })

  it('should name be correct', async () => {
    const __name__ = await getAppName()
    expectChai(__name__).to.be.equal(pkg.name)
  })

  it('should version be correct', async () => {
    const __version__ = await getAppVersion()
    expectChai(__version__).to.be.equal(pkg.version)
  })

  it('should launch correctly', async () => { 
    const instance = new App()
    await instance.app.waitForExist({ timeout: 5000 })
    await instance.main.waitForExist({ timeout: 5000 })
  })
})
