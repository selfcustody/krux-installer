import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectDevice from '../../../../pageobjects/select-device.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResources from '../../../../pageobjects/check-resources.page'
import CheckResourcesTestFirmware from '../../../../pageobjects/check-resources-test-firmware.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: warn before download \'odudex/krux_binaries/raw/main/maixpy_bit/firmware.bin\' again', () => {
  
  // eslint-disable-next-line no-undef
  before(async () => { 
    await Main.selectDeviceButton.click()
    await delay(1000)
    await SelectDevice.formArrow.click()
    await delay(1000)
    await SelectDevice.list_item_bit.waitForExist() 
    await delay(1000)
    await SelectDevice.list_item_bit.click()
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
  })

    
  // eslint-disable-next-line no-undef
  it('should card title be \'odudex/krux_binaries/raw/main/maixpy_bit/firmware.bin\'', async () => {
    await expectWDIO(CheckResourcesTestFirmware.cardTitleChecked).toHaveText('odudex/krux_binaries/raw/main/maixpy_bit/firmware.bin')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'Already downloaded\'', async () => {
    await expectWDIO(CheckResourcesTestFirmware.cardSubtitleChecked).toHaveText('Already downloaded')
  })

  // eslint-disable-next-line no-undef
  it('should card content be \'Click "Proceed" to proceed with the downloaded version or "Download the file again".\'', async () => {
    await expectWDIO(CheckResourcesTestFirmware.cardContentChecked)
      .toHaveText('Click "Proceed" to proceed with the downloaded version or "Download the file again".')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'PROCEED\' button', async () => { 
    await expectWDIO(CheckResourcesTestFirmware.buttonProceed).toHaveText('PROCEED')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'DOWNLOAD THE FILE AGAIN\' button', async () => { 
    await expectWDIO(CheckResourcesTestFirmware.buttonDownload).toHaveText('DOWNLOAD THE FILE AGAIN')
  })

})
