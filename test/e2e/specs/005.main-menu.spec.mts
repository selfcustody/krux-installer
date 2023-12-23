import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

const SELECT_DEVICE_TEXT = 'Select device'
const SELECT_VERSION_TEXT = 'Select version'

describe('KruxInstaller Main page', () => {

  let instance: any;

  before(async function () {
    instance = new App()
    await instance.app.waitForExist()
    await instance.main.waitForExist()
    await instance.logo.waitForExist()
    await instance.logo.waitForExist({ reverse: true })
    await instance.loadingDataMsg.waitForExist()
    await instance.verifyingOpensslMsg.waitForExist()
    if (process.platform === 'linux') {
      await instance.opensslForLinuxFound.waitForExist()
    } else if (process.platform === 'darwin') {
      await instance.opensslForDarwinFound.waitForExist()
    } else if (process.platform === 'win32') {
      await instance.opensslForWin32Found.waitForExist()
    }
    await instance.loadingDataMsg.waitForExist({ reverse: true })
    await instance.verifyingOpensslMsg.waitForExist({ reverse: true })
    await instance.opensslForLinuxFound.waitForExist({ reverse: true })
    await instance.mainPage.waitForExist()
    await instance.mainSelectDeviceButton.waitForExist()
    await instance.mainSelectVersionButton.waitForExist()
  })

  it('should main page appears', async () => {
    await expect(instance.mainPage).toBeDisplayed()
  })

  it('should message text not appears', async () => {
    await expect(instance.mainClickMessageText).not.toBeDisplayed()
  })

  it('should \'Select device\' button appears', async () => {
    await expect(instance.mainSelectDeviceButton).toBeDisplayed()
  })

  it('should \'Select version\' button appears', async () => {
    await expect(instance.mainSelectVersionButton).toBeDisplayed()
  })

  it('should \'Select device\' button have \'Select device\' text', async () => {
    await expect(instance.mainSelectDeviceText).toHaveText(SELECT_DEVICE_TEXT)
  })

  it('should \'Select version\' button have \'Select version\' text', async () => {
    await expect(instance.mainSelectVersionText).toHaveText(SELECT_VERSION_TEXT)
  })

  it('should \'Flash\' button not appears', async () => {
    await expect(instance.mainSelectFlashButton).not.toBeDisplayed()
  })
})
