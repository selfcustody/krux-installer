import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevicePage: expand/unexpand selection list', () => {

  // eslint-disable-next-line no-undef
  describe('preparation', () => {
  
    // eslint-disable-next-line no-undef
    before(async () => {
      await Main.selectDeviceButton.waitForExist()
      await delay(1000)
      await Main.selectDeviceButton.click()
      await SelectDevice.formOverlayContainer.waitForExist() 
      await SelectDevice.formSelectFieldContainer.waitForExist()
      await SelectDevice.formArrow.waitForExist()
      await delay(1000)
    })
    
    // eslint-disable-next-line no-undef 
    it('should arrow to be not expanded yet', async () => { 
      await expectWDIO(SelectDevice.formSelectFieldContainer).toHaveAttribute('aria-expanded', 'false')
    })
  })

  // eslint-disable-next-line no-undef
  describe('expand/unexpand', () => {
   
    // eslint-disable-next-line no-undef
    beforeEach(async () => { 
      await SelectDevice.formArrow.click() 
      await SelectDevice.formSelectFieldContainer.waitForExist()
      await delay(1000)   
    })

    // eslint-disable-next-line no-undef
    it('click on arrow first time and expand list', async () => { 
      await expectWDIO(SelectDevice.formSelectFieldContainer).toHaveAttribute('aria-expanded', 'true')
    })

    // eslint-disable-next-line no-undef
    it('click on arrow a second time and unexpand list', async () => { 
      await expectWDIO(SelectDevice.formSelectFieldContainer).toHaveAttr('aria-expanded', 'false')
    })
    
    // eslint-disable-next-line no-undef
    it('should click on arrow a third time and expand list', async () => {  
      await expectWDIO(SelectDevice.formSelectFieldContainer).toHaveAttribute('aria-expanded', 'true')
    })
  })

  // eslint-disable-next-line no-undef
  describe('options', () => {

    // eslint-disable-next-line no-undef
    before(async () => {
      await SelectDevice.list_item_m5stickv.waitForExist()
      await SelectDevice.list_item_amigo_ips.waitForExist()
      await SelectDevice.list_item_amigo_tft.waitForExist()
      await SelectDevice.list_item_bit.waitForExist()
      await SelectDevice.list_item_dock.waitForExist()
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_m5stickv\' option', async () => {
      await expectWDIO(SelectDevice.list_item_m5stickv).toHaveText('maixpy_m5stickv')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_amigo_ips\' option', async () => {
      await expectWDIO(SelectDevice.list_item_amigo_ips).toHaveText('maixpy_amigo_ips')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_amigo_tft\' option', async () => {
      await expectWDIO(SelectDevice.list_item_amigo_tft).toHaveText('maixpy_amigo_tft')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_bit\' option', async () => {
      await expectWDIO(SelectDevice.list_item_bit).toHaveText('maixpy_bit')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_dock\' option', async () => {
      await expectWDIO(SelectDevice.list_item_dock).toHaveText('maixpy_dock')
    })
  })
})
