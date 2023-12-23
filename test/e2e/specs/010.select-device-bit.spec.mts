import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

describe('KruxInstaller SelectDevice page selects \'maixpy_bit\' device', () => {

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
    await instance.mainSelectDeviceButton.click()
    await instance.mainPage.waitForExist({ reverse: true })
    await instance.selectDevicePage.waitForExist() 
    await instance.selectMaixpyBitButton.waitForExist() 
    await instance.selectMaixpyBitButton.click()
  })

  it('should change to Main page', async () => {
    await instance.selectDevicePage.waitForExist({ reverse: true })
    await expect(instance.selectDevicePage).not.toBeDisplayed()
    await instance.mainPage.waitForExist()
    await expect(instance.mainPage).toBeDisplayed()
  })

  it('should \'Select device\' button changed its text to \'Device: maixpy_bit\'', async () => {
    await expect(instance.mainSelectDeviceText).toHaveText('Device: maixpy_bit')
  })

})
