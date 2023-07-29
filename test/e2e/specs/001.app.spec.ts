const { createRequire } = require('module')
const expectChai = require('chai').expect
const expectWDIO = require('@wdio/globals').expect
const { describe, it } = require('mocha')
const {
  isAppReady,
  getAppName,
  getAppVersion
} = require('../utils')

const $ = require('@wdio/globals').$
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

  it('should launch with correct title', async () => { 
    const title = $('title')
    await expectWDIO(title).toHaveText(`KruxInstaller v${pkg.version}`)
  })
})