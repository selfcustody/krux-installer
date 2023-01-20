import { expect as expectChai } from 'chai'
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
  describe('expand/unexpand selection list', () => {

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
    it('should click on arrow a second time and expand list', async () => {
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
      expectWDIO(SelectDevice.list_item_m5stickv).toBeDisplayed()
      expectWDIO(SelectDevice.list_item_m5stickv).toHaveText('maixpy_m5stickv')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_amigo_ips\' option', async () => {
      expectWDIO(SelectDevice.list_item_amigo_ips).toBeDisplayed()
      expectWDIO(SelectDevice.list_item_amigo_ips).toHaveText('maixpy_amigo_ips')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_amigo_tft\' option', async () => {
      expectWDIO(SelectDevice.list_item_amigo_tft).toBeDisplayed()
      expectWDIO(SelectDevice.list_item_amigo_tft).toHaveText('maixpy_amigo_tft')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_bit\' option', async () => {
      expectWDIO(SelectDevice.list_item_bit).toBeDisplayed()
      expectWDIO(SelectDevice.list_item_bit).toHaveText('maixpy_bit')
    })

    // eslint-disable-next-line no-undef
    it('should have \'maixpy_dock\' option', async () => {
      expectWDIO(SelectDevice.list_item_dock).toBeDisplayed()
      expectWDIO(SelectDevice.list_item_dock).toHaveText('maixpy_dock')
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'m5stickv\' option', () => {
  
    // eslint-disable-next-line no-undef
    it('should be selected', async () => { 
      await SelectDevice.list_item_m5stickv.click()
      await delay(1000)
      expectWDIO(SelectDevice.selected).toHaveText('maixpy_m5stickv')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should click \'select\' go out of SelectDevicePage', async () => { 
      await SelectDevice.selectButton.click()
      expectWDIO(SelectDevice.page).not.toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be in MainPage', async () => {  
      expectWDIO(Main.page).toBeDisplayed()
      expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should the \'select device\' changed to \'maixpy_m5stickv\'', async () => {  
      const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()    
      expectChai(deviceButtonText).not.to.be.equal(' SELECT_DEVICE')
      expectChai(deviceButtonText).to.be.equal(' MAIXPY_M5STICKV')
      await delay(1000)
    })
    
    // eslint-disable-next-line no-undef
    it('should back to SelectDevice page', async () => { 
      expectWDIO(SelectDevice.page).not.toBeDisplayed()
      await Main.selectDeviceButton.click()
      await delay(1000)
      expectWDIO(SelectDevice.page).toBeDisplayed()
      await delay(1000)
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'amigo_ips\' option', () => {
   
    // eslint-disable-next-line no-undef
    it('should click on arrow and expand list', async () => {
      expectWDIO(SelectDevice.formArrow).toBeDisplayed()
      expectWDIO(SelectDevice.formOverlayContainer).not.toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'false')
      await SelectDevice.formArrow.click()
      await delay(1000)
      expectWDIO(SelectDevice.formOverlayContainer).toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'true')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be selected', async () => {
      await SelectDevice.list_item_amigo_ips.click()
      await delay(1000)
      expectWDIO(SelectDevice.selected).toHaveText('maixpy_amigo_ips')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should click \'select\' go out of SelectDevicePage', async () => { 
      await SelectDevice.selectButton.click()
      expectWDIO(SelectDevice.page).not.toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be in MainPage', async () => {  
      expectWDIO(Main.page).toBeDisplayed()
      expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should the \'maixpy_m5stickv\' changed to \'maixpy_amigo_ips\'', async () => {  
      const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()    
      expectChai(deviceButtonText).not.to.be.equal(' MAIXPY_AMIGO_TFT')
      expectChai(deviceButtonText).to.be.equal(' MAIXPY_AMIGO_IPS')
      await delay(1000)
    })
    
    // eslint-disable-next-line no-undef
    it('should back to SelectDevice page', async () => { 
      expectWDIO(SelectDevice.page).not.toBeDisplayed()
      await Main.selectDeviceButton.click()
      await delay(1000)
      expectWDIO(SelectDevice.page).toBeDisplayed()
      await delay(1000)
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'amigo_tft\' option', () => {
   
    // eslint-disable-next-line no-undef
    it('should click on arrow and expand list', async () => {
      expectWDIO(SelectDevice.formArrow).toBeDisplayed()
      expectWDIO(SelectDevice.formOverlayContainer).not.toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'false')
      await SelectDevice.formArrow.click()
      await delay(1000)
      expectWDIO(SelectDevice.formOverlayContainer).toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'true')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be selected', async () => { 
      await SelectDevice.list_item_amigo_tft.click()
      await delay(1000)
      expectWDIO(SelectDevice.selected).toHaveText('maixpy_amigo_tft')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should click \'select\' go out of SelectDevicePage', async () => { 
      await SelectDevice.selectButton.click()
      expectWDIO(SelectDevice.page).not.toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be in MainPage', async () => {  
      expectWDIO(Main.page).toBeDisplayed()
      expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should the \'maixpy_amigo_ips\' changed to \'maixpy_amigo_tft\'', async () => {  
      const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()    
      expectChai(deviceButtonText).not.to.be.equal(' MAIXPY_AMIGO_IPS')
      expectChai(deviceButtonText).to.be.equal(' MAIXPY_AMIGO_TFT')
      await delay(1000)
    })
    
    // eslint-disable-next-line no-undef
    it('should back to SelectDevice page', async () => { 
      expectWDIO(SelectDevice.page).not.toBeDisplayed()
      await Main.selectDeviceButton.click()
      await delay(1000)
      expectWDIO(SelectDevice.page).toBeDisplayed()
      await delay(1000)
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'bit\' option', () => {
   
    // eslint-disable-next-line no-undef
    it('should click on arrow and expand list', async () => {
      expectWDIO(SelectDevice.formArrow).toBeDisplayed()
      expectWDIO(SelectDevice.formOverlayContainer).not.toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'false')
      await SelectDevice.formArrow.click()
      await delay(1000)
      expectWDIO(SelectDevice.formOverlayContainer).toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'true')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be selected', async () => { 
      await SelectDevice.list_item_bit.click()
      await delay(1000)
      expectWDIO(SelectDevice.selected).toHaveText('maixpy_bit')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should click \'select\' go out of SelectDevicePage', async () => { 
      await SelectDevice.selectButton.click()
      expectWDIO(SelectDevice.page).not.toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be in MainPage', async () => {  
      expectWDIO(Main.page).toBeDisplayed()
      expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should the \'maixpy_amigo_tft\' changed to \'maixpy_bit\'', async () => {  
      const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()    
      expectChai(deviceButtonText).not.to.be.equal(' MAIXPY_AMIGO_TFT')
      expectChai(deviceButtonText).to.be.equal(' MAIXPY_BIT')
      await delay(1000)
    })
    
    // eslint-disable-next-line no-undef
    it('should back to SelectDevice page', async () => { 
      expectWDIO(SelectDevice.page).not.toBeDisplayed()
      await Main.selectDeviceButton.click()
      await delay(1000)
      expectWDIO(SelectDevice.page).toBeDisplayed()
      await delay(1000)
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'dock\' option', () => {
   
    // eslint-disable-next-line no-undef
    it('should click on arrow and expand list', async () => { 
      expectWDIO(SelectDevice.formArrow).toBeDisplayed()
      expectWDIO(SelectDevice.formOverlayContainer).not.toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'false')
      await SelectDevice.formArrow.click()
      await delay(1000)
      expectWDIO(SelectDevice.formOverlayContainer).toBeDisplayed()
      SelectDevice.formArrowWrapper.toHaveAttr('aria-expanded', 'true')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be selected', async () => {
      await SelectDevice.list_item_dock.click()
      await delay(1000)
      expectWDIO(SelectDevice.selected).toHaveText('maixpy_dock')
    })

    // eslint-disable-next-line no-undef
    it('should click \'select\' go out of SelectDevicePage', async () => { 
      await SelectDevice.selectButton.click()
      expectWDIO(SelectDevice.page).not.toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should be in MainPage', async () => { 
      expectWDIO(Main.page).toBeDisplayed()
      expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should the \'maixpy_bit\' changed to \'maixpy_dock\'', async () => {  
      const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()    
      expectChai(deviceButtonText).not.to.be.equal(' MAIXPY_BIT')
      expectChai(deviceButtonText).to.be.equal(' MAIXPY_DOCK')
      await delay(1000)
    })  
  })

})
