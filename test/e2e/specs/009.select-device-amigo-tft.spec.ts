const expectChai = require('chai').expect
const expectWDIO = require('@wdio/globals').expect
const { describe, it } = require('mocha')

const App = require('../pageobjects/app.page')

describe('KruxInstaller SelectDevice page selects \'maixpy_amigo_tft\' device', () => {

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
    await instance.selectMaixpyAmigoTftButton.waitForExist() 
    await instance.selectMaixpyAmigoTftButton.click()
  })

  it('should change to Main page', async () => {
    await instance.selectDevicePage.waitForExist({ reverse: true })
    await expectWDIO(instance.selectDevicePage).not.toBeDisplayed()
    await instance.mainPage.waitForExist()
    await expectWDIO(instance.mainPage).toBeDisplayed()
  })

  it('should \'Select device\' button changed its text to \'Device: maixpy_amigo_tft\'', async () => {
    await expectWDIO(instance.mainSelectDeviceText).toHaveText('Device: maixpy_amigo_tft')
  })

})
