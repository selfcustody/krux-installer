import { expect as expectWDIO } from '@wdio/globals'
import Main from '../pageobjects/main.page'
import SelectDevice from '../pageobjects/select-device.page'

const delay = (ms) => {
  return new Promise((resolve) => {
    setTimeout(resolve, ms)
  })
}

// eslint-disable-next-line no-undef
describe('SelectDevice page', () => {

  // eslint-disable-next-line no-undef
  describe('before change', () => {
    // eslint-disable-next-line no-undef
    it('should\'nt to be displayed', () => { 
      expectWDIO(Main.page).toBeDisplayed()
      expectWDIO(SelectDevice.page).not.toBeDisplayed()
    })
  })

  // eslint-disable-next-line no-undef
  describe('change', () => {
    // eslint-disable-next-line no-undef
    it('should click \'select device\' button and change page', async () => {
      await Main.selectDeviceButton.click()
      await delay(1000)
      expectWDIO(Main.page).not.toBeDisplayed()
      expectWDIO(SelectDevice.page).toBeDisplayed()
    })
  })


  // eslint-disable-next-line no-undef
  describe('after change, but not clicking yet', () => {

    // eslint-disable-next-line no-undef
    it('should card title have correct text', async () => {
      expectWDIO(SelectDevice.cardTitle).toHaveText('Choose the firmware\'s device that you want install')
    })


    // eslint-disable-next-line no-undef
    it('should have a form to select devices', async () => {
      expectWDIO(SelectDevice.cardContent).toExist()
      expectWDIO(SelectDevice.formSelect).toExist()
      expectWDIO(SelectDevice.formSelect).toExist()
      expectWDIO(SelectDevice.formSelectLabel).toExist() 
      expectWDIO(SelectDevice.selectButton).toExist()
      expectWDIO(SelectDevice.backButton).toExist()
      expectWDIO(SelectDevice.formSelectLabel).toHaveText('Device')
      expectWDIO(SelectDevice.selectButton).toHaveText('SELECT')
      expectWDIO(SelectDevice.backButton).toHaveText('BACK')
    })

    // eslint-disable-next-line no-undef
    it('should select \'down arrow\' to not be selected yet', async () => {
      expectWDIO(SelectDevice.formArrowContainer).toHaveAttr('class', 'v-input--horizontal')
      expectWDIO(SelectDevice.formArrowContainer).toHaveAttr('class', 'v-input--density-default')
      expectWDIO(SelectDevice.formArrowContainer).toHaveAttr('class', 'v-input--readonly')
      expectWDIO(SelectDevice.formArrowContainer).toHaveAttr('class', 'v-text-field')
      expectWDIO(SelectDevice.formArrowContainer).toHaveAttr('class', 'v-select')
      expectWDIO(SelectDevice.formArrowContainer).toHaveAttr('class', 'v-select-single')
      expectWDIO(SelectDevice.formArrowContainer).toHaveAttr('class', 'v-select-single--selected') 
      expectWDIO(SelectDevice.formArrowWrapper).toHaveAttr('class', 'v-field--active')
      expectWDIO(SelectDevice.formArrowWrapper).toHaveAttr('class', 'v-field--appended')
      expectWDIO(SelectDevice.formArrowWrapper).toHaveAttr('class', 'v-field--dirty')
      expectWDIO(SelectDevice.formArrowWrapper).toHaveAttr('class', 'v-field--variant-filled')
      expectWDIO(SelectDevice.formArrowWrapper).toHaveAttr('class', 'v-theme--light')
      expectWDIO(SelectDevice.formArrowWrapper).toHaveAttr('role', 'textbox')
      expectWDIO(SelectDevice.formArrowWrapper).toHaveAttr('aria-expanded', 'false')
    })
  })

  // eslint-disable-next-line no-undef
  describe('after change and backing to main menu without select anything', () => {
  
    // eslint-disable-next-line no-undef
    it('should click \'back\' and go to main page', async () => { 
      expectWDIO(Main.page).not.toBeDisplayed()
      expectWDIO(SelectDevice.page).toBeDisplayed()
      await SelectDevice.backButton.click()
      await delay(1000)
      expectWDIO(Main.page).toBeDisplayed()
      expectWDIO(SelectDevice.page).not.toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should click \'select device\' button and change page again', async () => {
      await Main.selectDeviceButton.click()
      await delay(1000)
      expectWDIO(Main.page).not.toBeDisplayed()
      expectWDIO(SelectDevice.page).toBeDisplayed()
    })
  })

  // eslint-disable-next-line no-undef
  describe('select expand/unexpand list', () => {

    // eslint-disable-next-line no-undef
    it('click on arrow first time and expand list', async () => {
      expectWDIO(SelectDevice.formArrow).toBeDisplayed()
      expectWDIO(SelectDevice.formOverlayContainer).not.toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'false')
      await SelectDevice.formArrow.click()
      await delay(1000)
      expectWDIO(SelectDevice.formOverlayContainer).toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'true')
    })

    // eslint-disable-next-line no-undef
    it('click on arrow first time and unexpand list', async () => {
      expectWDIO(SelectDevice.formArrow).toBeDisplayed() 
      expectWDIO(SelectDevice.formOverlayContainer).toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'true')
      await SelectDevice.formArrow.click()
      await delay(1000)
      expectWDIO(SelectDevice.formOverlayContainer).not.toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'false')
    })

    // eslint-disable-next-line no-undef
    it('click on arrow a second time and expand list', async () => {
      expectWDIO(SelectDevice.formArrow).toBeDisplayed()
      expectWDIO(SelectDevice.formOverlayContainer).not.toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'false')
      await SelectDevice.formArrow.click()
      await delay(1000)
      expectWDIO(SelectDevice.formOverlayContainer).toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'true')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_m5stickv\' option', async () => {
      const wrapper = await SelectDevice.formOverlayContainer.$('div')
      const m5stickv = await wrapper.$('*=maixpy_m5stickv') 
      expectWDIO(m5stickv).toBeDisplayed()
      expectWDIO(m5stickv).toHaveText('maixpy_m5stickv')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_amigo_ips\' option', async () => {
      const wrapper = await SelectDevice.formOverlayContainer.$('div')
      const amigo_ips = await wrapper.$('*=maixpy_amigo_ips') 
      expectWDIO(amigo_ips).toBeDisplayed()
      expectWDIO(amigo_ips).toHaveText('maixpy_amigo_ips')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_amigo_tft\' option', async () => {
      const wrapper = await SelectDevice.formOverlayContainer.$('div')
      const amigo_tft = await wrapper.$('*=maixpy_amigo_tft') 
      expectWDIO(amigo_tft).toBeDisplayed()
      expectWDIO(amigo_tft).toHaveText('maixpy_amigo_tft')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_bit\' option', async () => {
      const wrapper = await SelectDevice.formOverlayContainer.$('div') 
      const bit = await wrapper.$('*=maixpy_bit') 
      expectWDIO(bit).toBeDisplayed()
      expectWDIO(bit).toHaveText('maixpy_bit')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_dock\' option', async () => {
      const wrapper = await SelectDevice.formOverlayContainer.$('div') 
      const dock = await wrapper.$('*=maixpy_dock') 
      expectWDIO(dock).toBeDisplayed()
      expectWDIO(dock).toHaveText('maixpy_dock')
    })
  })

})
