import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevicePage: page select \'m5stickv\' option', () => {

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
    await SelectDevice.formSelected.waitUntil(async function() {
      return (await this.getText()) !== ''
    })
  })

  // eslint-disable-next-line no-undef
  after(async () => {
    await delay(1000)
  })
  
  // eslint-disable-next-line no-undef
  it('should be selected', async () => {    
    await expectWDIO(SelectDevice.formSelected).toHaveText('maixpy_m5stickv')
  })

  // eslint-disable-next-line no-undef
  it('should click \'select\' and go to MainPage', async () => {   
    await SelectDevice.formSelectButton.click()
    await SelectDevice.page.waitForExist({ reverse: true })
    await expectWDIO(Main.page).toBeDisplayed() 
  })

  // eslint-disable-next-line no-undef
  it('should the \'select device\' changed to \'maixpy_m5stickv\'', async () => {  
    const deviceButtonContent = await Main.selectDeviceButton.$('span.v-btn__content')
    await expectWDIO(deviceButtonContent).not.toHaveText('SELECT_DEVICE')
    await expectWDIO(deviceButtonContent).toHaveText('MAIXPY_M5STICKV')
  })    
})
