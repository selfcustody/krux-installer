import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectDevice from '../../../../pageobjects/select-device.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResources from '../../../../pageobjects/check-resources.page'
import CheckResourcesTestFirmware from '../../../../pageobjects/check-resources-test-firmware.page'
import CheckResourcesTestKboot from '../../../../pageobjects/check-resources-test-kboot.page'
import DownloadTestKboot from '../../../../pageobjects/download-test-kboot.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: download \'odudex/krux_binaries/raw/main/maixpy_amigo_ips/kboot.kfpkg\'', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {  
    await Main.selectDeviceButton.click()
    await delay(1000)
    await SelectDevice.formArrow.click()
    await delay(1000)
    await SelectDevice.list_item_amigo_ips.waitForExist() 
    await delay(1000)
    await SelectDevice.list_item_amigo_ips.click()
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
    await CheckResources.page.waitForExist({ reverse: true })*
    await CheckResourcesTestFirmware.page.waitForExist()
    await CheckResourcesTestFirmware.cardTitleChecking.waitForExist()
    await CheckResourcesTestFirmware.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesTestFirmware.cardTitleChecked.waitForExist()
    await CheckResourcesTestFirmware.buttonProceed.click()
    await CheckResourcesTestFirmware.page.waitForExist({ reverse: true })
    await CheckResourcesTestKboot.page.waitForExist()
    await CheckResourcesTestKboot.cardTitleChecking.waitForExist()
    await CheckResourcesTestKboot.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesTestKboot.page.waitForExist({ reverse: true })
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Downloading kboot.kfpkg...\'', async () => { 
    await DownloadTestKboot.page.waitForExist()
    await DownloadTestKboot.cardTitle.waitForExist()
    await expectWDIO(DownloadTestKboot.cardTitle).toHaveText('Downloading kboot.kfpkg...')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'device: maixpy_amigo_ips\'', async () => {  
    await DownloadTestKboot.cardSubtitle.waitForExist()
    await expectWDIO(DownloadTestKboot.cardSubtitle).toHaveText('device: maixpy_amigo_ips')
  })

  // eslint-disable-next-line no-undef
  it('should download kboot.kfpkg', async () => { 
    await DownloadTestKboot.progressLinearText.waitForExist()
    await DownloadTestKboot.progressLinearText.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent !== 0
    }, {
      timeout: 120000,
      interval: 1
    })
    await DownloadTestKboot.page.waitForExist({ reverse: true })
  })
})
