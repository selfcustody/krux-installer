import { expect as expectWDIO } from '@wdio/globals'
import Main from '../pageobjects/main.page'
import SelectDevice from '../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevice page', () => {

  // eslint-disable-next-line no-undef
  it('should\'nt to be displayed', () => {
    expectWDIO(SelectDevice.page).not.toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should click \'select device\' button and change page', async () => {
    await Main.selectDeviceButton.click()
    expectWDIO(SelectDevice.page).toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should card title have correct text', async () => {
    expectWDIO(SelectDevice.cardTitle).toHaveText('Choose the firmware\'s device that you want install')
  })
})
