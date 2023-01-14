import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import { name, version } from '../../package.json'
import App from '../pageobjects/app.page'

const waitFor = (ms: number) =>
  new Promise<void>((resolve) => {
    setTimeout(resolve, ms);
  });

// eslint-disable-next-line no-undef
describe('KruxInstaller initialization', () => {

  // eslint-disable-next-line no-undef
  it('should be ready', async () => {
    // eslint-disable-next-line no-undef
    
    await waitFor(5000)
    const isReady = await browser.electronApp('isReady')
    expectChai(isReady).to.be.equal(true)
  })

  // eslint-disable-next-line no-undef
  it('should name be correct', async () => {

    // eslint-disable-next-line no-undef
    const n = await browser.electronApp('getName')
    expectChai(n).to.be.equal(name)
  })

  // eslint-disable-next-line no-undef
  it('should version be correct', async () => {
    // eslint-disable-next-line no-undef
    const v = await browser.electronApp('getVersion')
    expectChai(v).to.be.equal(version)
  })

  // eslint-disable-next-line no-undef
  it('should launch with correct title', () => { 
    expectWDIO(App.title).toHaveText(name)
  })
})


