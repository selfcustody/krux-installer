import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevicePage: page select \'dock\' option', () => {

  // eslint-disable-next-line no-undef
  before(async () => { 
    await Main.selectDeviceButton.click()
    await delay(1000)
    await SelectDevice.formArrow.click()
    await delay(1000)
    await SelectDevice.list_item_dock.waitForExist() 
    await delay(1000)  
    await SelectDevice.list_item_dock.click()
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
    await expectWDIO(SelectDevice.formSelected).toHaveText('maixpy_dock')
  })

  // eslint-disable-next-line no-undef
  it('should click \'select\' go out of SelectDevicePage', async () => {   
    await SelectDevice.formSelectButton.click()
    await delay(1000)
    await expectWDIO(SelectDevice.page).not.toBeDisplayed() 
  })

  // eslint-disable-next-line no-undef
  it('should the \'select device\' changed to \'maixpy_bit\'', async () => {   
    const deviceButtonContent = await Main.selectDeviceButton.$('span.v-btn__content')
    await expectWDIO(deviceButtonContent).not.toHaveText('SELECT_DEVICE')
    await expectWDIO(deviceButtonContent).toHaveText('MAIXPY_DOCK')
  })    
})
