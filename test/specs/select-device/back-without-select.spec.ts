import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevicePage: click \'SELECT DEVICE\' and back to MainPage', () => {

  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectDeviceButton.click()
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should not be in MainPage', async () => {
    await expectWDIO(Main.page).not.toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should be in SelectDevicePage', async () => {
    await expectWDIO(SelectDevice.page).toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should click \'back\' and go to main page', async () => { 
    await SelectDevice.formBackButton.click()
    await delay(1000)
    await expectWDIO(Main.page).toBeDisplayed()
    await expectWDIO(SelectDevice.page).not.toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should \'SELECT DEVICE\' button did not changed', async () => {
    const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()  
    expectChai(deviceButtonText).to.be.equal(' SELECT DEVICE')
  })
})
