import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import {
  isAppReady,
  getAppName,
  getAppVersion
} from '../utils'
import { name, version } from '../../../package.json'
import App from '../pageobjects/app.page'

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