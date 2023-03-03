import { readFile } from 'fs'
import { promisify } from 'util'
import { join } from 'path'
import { name } from '../../../../../package.json'
import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectDevice from '../../../../pageobjects/select-device.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResources from '../../../../pageobjects/check-resources.page'
import CheckResourcesTestFirmware from '../../../../pageobjects/check-resources-test-firmware.page'
import CheckResourcesTestKboot from '../../../../pageobjects/check-resources-test-kboot.page'
import CheckResourcesTestKtool from '../../../../pageobjects/check-resources-test-ktool.page'

const readFileAsync = promisify(readFile)

// eslint-disable-next-line no-undef
describe('SelectVersionPage: check for \'odudex/krux_binaries/raw/main/ktool-<linux|mac|mac-10|win.exe>\'', () => {
 
  let config

  // eslint-disable-next-line no-undef
  before(async () => {  
    // eslint-disable-next-line no-undef
    const api = await browser.electronAPI()
    const configPath = join(api.appData, name, 'config.json') 
    const configString = await readFileAsync(configPath, 'utf8')
    config = JSON.parse(configString) 

    await Main.selectDeviceButton.click()
    await delay(1000)
    await SelectDevice.formArrow.click()
    await delay(1000)
    await SelectDevice.list_item_m5stickv.waitForExist() 
    await delay(1000)
    await SelectDevice.list_item_m5stickv.click()
    await delay(1000) 
    await SelectDevice.formSelectButton.click()
    await SelectDevice.page.waitForExist({ reverse: true })
    await Main.page.waitForExist()
    await Main.selectVersionButton.waitForExist()
    await Main.selectVersionButton.click()
    await SelectVersion.cardTitleChecked.waitForExist()  
    await SelectVersion.cardSubtitleOfficial.waitForExist()  
    await SelectVersion.cardSubtitleTest.waitForExist()  
    await SelectVersion.formArrow.waitForExist()
    await SelectVersion.formBackButton.waitForExist()  
    await delay(1000)
    await SelectVersion.formArrow.click()
    await delay(1000)
    await SelectVersion.list_item_22_03_0.waitForExist()
    await SelectVersion.list_item_22_08_0.waitForExist()
    await SelectVersion.list_item_22_08_1.waitForExist()
    await SelectVersion.list_item_22_08_2.waitForExist()
    await SelectVersion.list_item_krux_binaries.waitForExist()
    await delay(1000) 
    await SelectVersion.list_item_krux_binaries.click()
    await delay(1000)
    await SelectVersion.formSelectButton.waitForExist()
    await SelectVersion.formSelectButton.click()   
    await CheckResources.page.waitForExist()
    await CheckResources.page.waitForExist({ reverse: true })
    await CheckResourcesTestFirmware.page.waitForExist()
    await CheckResourcesTestFirmware.cardTitleChecking.waitForExist()
    await CheckResourcesTestFirmware.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesTestFirmware.cardTitleChecked.waitForExist()
    await CheckResourcesTestFirmware.buttonProceed.click()
    await CheckResourcesTestFirmware.page.waitForExist({ reverse: true })
    await CheckResourcesTestKboot.page.waitForExist()
    await CheckResourcesTestKboot.cardTitleChecking.waitForExist()
    await CheckResourcesTestKboot.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesTestKboot.cardTitleChecked.waitForExist()
    await CheckResourcesTestKboot.buttonProceed.waitForExist()
    await CheckResourcesTestKboot.buttonProceed.click()
    await CheckResourcesTestKboot.page.waitForExist({ reverse: true })
    await CheckResourcesTestKtool.page.waitForExist()
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Checking for ktool-<linux|mac|mac-10|win.exe>...\'', async () => {
    if (config.os === 'linux') {
      await expectWDIO(CheckResourcesTestKtool.cardTitleChecking).toHaveText('Checking for ktool-linux...')
    }
    else if (config.os === 'win32') {
      await expectWDIO(CheckResourcesTestKtool.cardTitleChecking).toHaveText('Checking for ktool-win.exe...')
    }
    else if (config.os === 'darwin' && config.isMac10) {
      await expectWDIO(CheckResourcesTestKtool.cardTitleChecking).toHaveText('Checking for ktool-mac-10...')
    }
    else if (config.os === 'darwin' && !config.isMac10) {
      await expectWDIO(CheckResourcesTestKtool.cardTitleChecking).toHaveText('Checking for ktool-mac...')
    }
  })

})
