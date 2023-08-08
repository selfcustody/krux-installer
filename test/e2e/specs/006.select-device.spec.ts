const expectChai = require('chai').expect
const expectWDIO = require('@wdio/globals').expect
const { describe, it } = require('mocha')

const App = require('../pageobjects/app.page')

const SELECT_DEVICE_TEXT = 'Select device'
const SELECT_VERSION_TEXT = 'Select version'
const PLEASE_SELECT_VERSION_MESSAGE = 'Please click \'Select version\' to download sources'

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

  it('should click on \'Select device\' button and page change', async () => {
    await instance.mainSelectDeviceButton.click()
    await instance.mainPage.waitForExist({ reverse: true })
    await instance.selectDevicePage.waitForExist()
    await expectWDIO(instance.selectDevicePage).toBeDisplayed()
  })

  it('should \'maixpy_m5stickv\' button be displayed', async () => {
    await instance.selectMaixpyM5StickVButton.waitForExist()
    await expectWDIO(instance.selectMaixpyM5StickVButton).toBeDisplayed()
  })

  it('should \'maixpy_m5stickv\' button have \'maixpy_m5stickv\' text', async () => { 
    await instance.selectMaixpyM5StickVText.waitForExist()
    await expectWDIO(instance.selectMaixpyM5StickVText).toHaveText('maixpy_m5stickv')
  })

  it('should \'maixpy_amigo_ips\' button be displayed', async () => {
    await instance.selectMaixpyAmigoIpsButton.waitForExist()
    await expectWDIO(instance.selectMaixpyAmigoIpsButton).toBeDisplayed()
  })

  it('should \'maixpy_amigo_ips\' button have \'maixpy_amigo_ips\' text', async () => { 
    await instance.selectMaixpyAmigoIpsText.waitForExist()
    await expectWDIO(instance.selectMaixpyAmigoIpsText).toHaveText('maixpy_amigo_ips')
  })

  it('should \'maixpy_amigo_tft\' button be displayed', async () => {
    await instance.selectMaixpyAmigoTftButton.waitForExist()
    await expectWDIO(instance.selectMaixpyAmigoTftButton).toBeDisplayed()
  })

  it('should \'maixpy_amigo_tft\' button have \'maixpy_amigo_tft\' text', async () => { 
    await instance.selectMaixpyAmigoTftText.waitForExist()
    await expectWDIO(instance.selectMaixpyAmigoTftText).toHaveText('maixpy_amigo_tft')
  })

  it('should \'maixpy_bit\' button be displayed', async () => {
    await instance.selectMaixpyBitButton.waitForExist()
    await expectWDIO(instance.selectMaixpyBitButton).toBeDisplayed()
  })

  it('should \'maixpy_bit\' button have \'maixpy_bit\' text', async () => { 
    await instance.selectMaixpyBitText.waitForExist()
    await expectWDIO(instance.selectMaixpyBitText).toHaveText('maixpy_bit')
  })

  it('should \'maixpy_dock\' button be displayed', async () => {
    await instance.selectMaixpyDockButton.waitForExist()
    await expectWDIO(instance.selectMaixpyDockButton).toBeDisplayed()
  })

  it('should \'maixpy_dock\' button have \'maixpy_dock\' text', async () => { 
    await instance.selectMaixpyDockText.waitForExist()
    await expectWDIO(instance.selectMaixpyDockText).toHaveText('maixpy_dock')
  })

  it('should \'back\' button be displayed', async () => {
    await instance.selectBackButton.waitForExist()
    await expectWDIO(instance.selectBackButton).toBeDisplayed()
  })

  it('should \'back\' button have \'back\' text', async () => { 
    await instance.selectBackText.waitForExist()
    await expectWDIO(instance.selectBackText).toHaveText('Back')
  })
})
