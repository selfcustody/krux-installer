import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectDevice from '../../../../pageobjects/select-device.page' 
import SelectVersion from '../../../../pageobjects/select-version.page' 
import CheckResources from '../../../../pageobjects/check-resources.page'
import CheckResourcesTestFirmware from '../../../../pageobjects/check-resources-test-firmware.page'
import DownloadTestFirmware from '../../../../pageobjects/download-test-firmware.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: download \'odudex/krux_binaries/raw/main/maixpy_m5stickv/firmware.bin\'', () => {

  // eslint-disable-next-line no-undef
  before(async () => { 
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
    await CheckResourcesTestFirmware.page.waitForExist({ reverse: true })
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Downloading firmware.bin...\'', async () => { 
    await DownloadTestFirmware.page.waitForExist()
    await DownloadTestFirmware.cardTitle.waitForExist()
    await expectWDIO(DownloadTestFirmware.cardTitle).toHaveText('Downloading firmware.bin...')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'device: maixpy_m5stickv\'', async () => {  
    await DownloadTestFirmware.cardSubtitle.waitForExist()
    await expectWDIO(DownloadTestFirmware.cardSubtitle).toHaveText('device: maixpy_m5stickv')
  })

  // eslint-disable-next-line no-undef
  it('should download firmware.bin', async () => { 
    await DownloadTestFirmware.progressLinearText.waitForExist()
    await DownloadTestFirmware.progressLinearText.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent !== 0
    }, {
      timeout: 120000,
      interval: 10
    })
    await DownloadTestFirmware.page.waitForExist({ reverse: true })
  })
})
