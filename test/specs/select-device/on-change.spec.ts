import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevicePage click \'SELECT DEVICE\' button', () => {

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
  it('should have the card to select devices', async () => {
    await expectWDIO(SelectDevice.cardContent).toExist()
  })

  // eslint-disable-next-line no-undef
  it('should card title have correct text', async () => {
    await expectWDIO(SelectDevice.cardTitle).toHaveText('Choose the firmware\'s device that you want install')
  })

  // eslint-disable-next-line no-undef
  it('should have the container that contain the select object', async () => {
    await expectWDIO(SelectDevice.formSelectContainer).toExist()
  })

  // eslint-disable-next-line no-undef
  it('should have the control that controls the select object', async () => {
    await expectWDIO(SelectDevice.formSelectField).toExist()
  })

  // eslint-disable-next-line no-undef
  it('should have the label that contain the \'Device\' text', async () => {
    await expectWDIO(SelectDevice.formSelectLabel).toExist()
    await expectWDIO(SelectDevice.formSelectLabel).toHaveText('Device')
  })

  // eslint-disable-next-line no-undef
  it('should have a container that contains the \'down arrow\'', async () => { 
    await expectWDIO(SelectDevice.formArrowContainer).toExist()
  })

  // eslint-disable-next-line no-undef
  it('should have a \'down arrow\'', async () => { 
    await expectWDIO(SelectDevice.formArrow).toExist()
    await expectWDIO(SelectDevice.formArrow).toHaveAttribute('class', 'mdi-menu-down mdi v-icon notranslate v-theme--light v-icon--size-default')
  })
  
  // eslint-disable-next-line no-undef
  it('should have \'SELECT\' button', async () => { 
    await expectWDIO(SelectDevice.formSelectButton).toExists
    await expectWDIO(SelectDevice.formSelectButton).toHaveText('SELECT')
  })

  // eslint-disable-next-line no-undef
  it('should have \'BACK\' button', async () => { 
    await expectWDIO(SelectDevice.formBackButton).toExists
    await expectWDIO(SelectDevice.formBackButton).toHaveText('BACK')
  })
})
