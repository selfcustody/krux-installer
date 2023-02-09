import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevicePage: click \'SELECT DEVICE\' and back to MainPage', () => {

  // eslint-disable-next-line no-undef
  before(async () => { 
    await Main.selectDeviceButton.waitForExist()
    await delay(1000)
    await Main.selectDeviceButton.click()
    await delay(1000)
    await SelectDevice.formBackButton.waitForExist()
    await delay(1000)
    await SelectDevice.formBackButton.click()
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should \'SELECT DEVICE\' button did not changed', async () => {
    await expectWDIO(Main.selectDeviceButtonContent).toHaveText('SELECT DEVICE')
  })
})
