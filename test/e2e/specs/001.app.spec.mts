import { createRequire } from 'module'
import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import {
  isAppReady,
  getAppName,
  getAppVersion
} from '../utils'

const { name, version } = createRequire(import.meta.url)('../../../package.json')
const { App } = createRequire(import.meta.url)('../pageobjects/app.page')

describe('KruxInstaller initialization', () => {

  it('should be ready', async () => {
    const isReady = await isAppReady()
    expectChai(isReady).to.be.equal(true)
  })

  it('should name be correct', async () => {
    const __name__ = await getAppName()
    expectChai(__name__).to.be.equal(name)
  })

  it('should version be correct', async () => {
    const __version__ = await getAppVersion()
    expectChai(__version__).to.be.equal(version)
  })

  it('should launch with correct title', async () => { 
    await expectWDIO(App.title).toHaveText(name)
  })
})