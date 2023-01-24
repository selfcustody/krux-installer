import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevice: expand/unexpand selection list', () => {

  // eslint-disable-next-line no-undef
  describe('prepare', () => {
  
    // eslint-disable-next-line no-undef
    before(async () => {
      await Main.selectDeviceButton.click()
      await delay(1000)
    })
  
    // eslint-disable-next-line no-undef 
    it('should have arrow', async () => { 
      await expectWDIO(SelectDevice.formArrow).toBeDisplayed()
    })

    // eslint-disable-next-line no-undef 
    it('should have an overlay without childs', async () => {  
      await expectWDIO(SelectDevice.formOverlayContainer).toBeDisplayed()
      const childs = await SelectDevice.formOverlayContainer.$$('//*')
      await expectWDIO(childs).not.toExist()
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
  describe('have options', () => {

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_m5stickv\' option', async () => {
      await expectWDIO(SelectDevice.list_item_m5stickv).toBeDisplayed()
      await expectWDIO(SelectDevice.list_item_m5stickv).toHaveText('maixpy_m5stickv')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_amigo_ips\' option', async () => {
      await expectWDIO(SelectDevice.list_item_amigo_ips).toBeDisplayed()
      await expectWDIO(SelectDevice.list_item_amigo_ips).toHaveText('maixpy_amigo_ips')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_amigo_tft\' option', async () => {
      await expectWDIO(SelectDevice.list_item_amigo_tft).toBeDisplayed()
      await expectWDIO(SelectDevice.list_item_amigo_tft).toHaveText('maixpy_amigo_tft')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_bit\' option', async () => {
      await expectWDIO(SelectDevice.list_item_bit).toBeDisplayed()
      await expectWDIO(SelectDevice.list_item_bit).toHaveText('maixpy_bit')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_dock\' option', async () => {
      await expectWDIO(SelectDevice.list_item_dock).toBeDisplayed()
      await expectWDIO(SelectDevice.list_item_dock).toHaveText('maixpy_dock')
    })
  })
})
