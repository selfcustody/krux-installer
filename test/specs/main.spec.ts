import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import Main from '../pageobjects/main.page'

// eslint-disable-next-line no-undef
describe('Main page', () => {

  // eslint-disable-next-line no-undef
  it('should to be displayed', () => {
    expectWDIO(Main.page).toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  describe('\'Select device\' Menu', () => {
      
    // eslint-disable-next-line no-undef
    it('should to be displayed', () => { 
      expectWDIO(Main.selectDeviceCard).toBeDisplayed() 
      expectWDIO(Main.selectDeviceCardSubtitle).toBeDisplayed() 
      expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
    })

    // eslint-disable-next-line no-undef
    it('should subtitle have correct text', () => { 
      expectWDIO(Main.selectDeviceCardSubtitle).toHaveText(
        'Select between available devices (m5stickV, amigo, bit, dock)')
    })

    // eslint-disable-next-line no-undef
    it('should have a clickable button', () => {
      expectWDIO(Main.selectDeviceButton).toBeClickable()
    })

    // eslint-disable-next-line no-undef
    it('should button have correct initial text', async () => {
      const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()  
      expectChai(deviceButtonText).to.be.equal(' SELECT DEVICE')
    })
  })


  // eslint-disable-next-line no-undef
  describe('\'Select version\' menu', () => {
    // eslint-disable-next-line no-undef
    it('should to be displayed', () => {
      expectWDIO(Main.selectVersionCard).toBeDisplayed() 
      expectWDIO(Main.selectVersionCardSubtitle).toBeDisplayed() 
      expectWDIO(Main.selectVersionButton).toBeDisplayed() 
    })

    // eslint-disable-next-line no-undef
    it('should subtitle have correct text', () => { 
      expectWDIO(Main.selectVersionCardSubtitle).toHaveText(
        'Select between selfcustody (official) or odudex (test) releases')
    })

    // eslint-disable-next-line no-undef
    it('should have a clickable button', () => {
      expectWDIO(Main.selectVersionButton).toBeClickable()
    })
    
    // eslint-disable-next-line no-undef
    it('should button have correct initial text', async () => {
      const versionButtonText = await Main.selectVersionButton.$('span.v-btn__content').getText() 
      expectChai(versionButtonText).to.be.equal(' SELECT VERSION')
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'Flash\' menu', () => {
      
    // eslint-disable-next-line no-undef
    it('should to be displayed', () => {
      expectWDIO(Main.selectWriteCard).toBeDisplayed()
      expectWDIO(Main.selectWriteCardSubtitle).toBeDisplayed()
      expectWDIO(Main.selectWriteButton).toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should subtitle have correct initial text', async () => {
      if (process.platform === 'linux') {      
        expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-linux')
      }
      if (process.platform === 'win32') {
        expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-win.exe')
      }
      if (process.platform === 'darwin') {
        expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-mac')
      }
    })
    
    // eslint-disable-next-line no-undef
    it('should have a clickable button', () => {
      expectWDIO(Main.selectWriteButton).toBeClickable()
    })

    // eslint-disable-next-line no-undef
    it('should button have correct initial text', async () => {
      const writeButtonText = await Main.selectWriteButton.$('span.v-btn__content').getText() 
      expectChai(writeButtonText).to.be.equal(' FLASH')
    })
  })
})
