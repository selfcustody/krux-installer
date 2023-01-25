import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevicePage: click \'SELECT DEVICE\' button', () => {

  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectDeviceButton.waitForExist()
    await delay(1000)
    await Main.selectDeviceButton.click()
    await delay(1000)
    await SelectDevice.cardTitle.waitForExist() 
    await SelectDevice.cardContent.waitForExist() 
    await SelectDevice.formSelectContainer.waitForExist()
    await SelectDevice.formSelectField.waitForExist()
    await SelectDevice.formSelectLabel.waitForExist()
    await SelectDevice.formArrowContainer.waitForExist()
    await SelectDevice.formArrow.waitForExist()
    await SelectDevice.formSelectButton.waitForExist()
    await SelectDevice.formBackButton.waitForExist()
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should card title have correct text', async () => {
    await expectWDIO(SelectDevice.cardTitle).toHaveText('Choose the firmware\'s device that you want install')
  })

  // eslint-disable-next-line no-undef
  it('should have the label that contain the \'Device\' text', async () => {
    await expectWDIO(SelectDevice.formSelectLabel).toHaveText('Device')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'down arrow\' icon', async () => { 
    await expectWDIO(SelectDevice.formArrow).toHaveAttribute('class', 'mdi-menu-down mdi v-icon notranslate v-theme--light v-icon--size-default')
  })
  
  // eslint-disable-next-line no-undef
  it('should have \'SELECT\' button', async () => { 
    await expectWDIO(SelectDevice.formSelectButton).toHaveText('SELECT')
  })

  // eslint-disable-next-line no-undef
  it('should have \'BACK\' button', async () => { 
    await expectWDIO(SelectDevice.formBackButton).toHaveText('BACK')
  })
})
