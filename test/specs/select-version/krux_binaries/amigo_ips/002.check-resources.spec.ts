import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectDevice from '../../../../pageobjects/select-device.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResources from '../../../../pageobjects/check-resources.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: check if exists \'odudex/krux_binaries\' resources for \'amigo_ips\'', () => {
 
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
  })

  // eslint-disable-next-line no-undef
  it('\'odudex/krux_binaries\' should be selected', async () => {    
    await expectWDIO(SelectVersion.formSelected).toHaveText('odudex/krux_binaries')
  })

  // eslint-disable-next-line no-undef
  it('should check between official or test resources', async () => { 
    await SelectVersion.formSelectButton.waitForExist()
    await SelectVersion.formSelectButton.click()  
    await CheckResources.page.waitForExist() 
    await expectWDIO(CheckResources.cardTitle).toHaveText('Checking between official or test resources...')
    await CheckResources.page.waitForExist({ reverse: true }) 
  })

})
