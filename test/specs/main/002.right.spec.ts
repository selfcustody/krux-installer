import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import Main from '../../pageobjects/main.page'

// eslint-disable-next-line no-undef
describe('Main page', () => {

  // eslint-disable-next-line no-undef
  it('should to be displayed', async () => {
    await expectWDIO(Main.page).toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  describe('\'Select device\' Menu', () => {
      
    // eslint-disable-next-line no-undef
    it('should to be displayed', async () => { 
      await expectWDIO(Main.selectDeviceCard).toBeDisplayed() 
      await expectWDIO(Main.selectDeviceCardSubtitle).toBeDisplayed() 
      await expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
    })

    // eslint-disable-next-line no-undef
    it('should subtitle have correct text', async () => { 
      await expectWDIO(Main.selectDeviceCardSubtitle).toHaveText(
        'Select between available devices (m5stickV, amigo, bit, dock)')
    })

    // eslint-disable-next-line no-undef
    it('should have a clickable button', async () => {
      await expectWDIO(Main.selectDeviceButton).toBeClickable()
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
    it('should to be displayed', async () => {
      await expectWDIO(Main.selectVersionCard).toBeDisplayed() 
      await expectWDIO(Main.selectVersionCardSubtitle).toBeDisplayed() 
      await expectWDIO(Main.selectVersionButton).toBeDisplayed() 
    })

    // eslint-disable-next-line no-undef
    it('should subtitle have correct text', async () => { 
      await expectWDIO(Main.selectVersionCardSubtitle).toHaveText(
        'Select between selfcustody (official) or odudex (test) releases')
    })

    // eslint-disable-next-line no-undef
    it('should have a clickable button', async () => {
      await expectWDIO(Main.selectVersionButton).toBeClickable()
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
    it('should to be displayed', async () => {
      await expectWDIO(Main.selectWriteCard).toBeDisplayed()
      await expectWDIO(Main.selectWriteCardSubtitle).toBeDisplayed()
      await expectWDIO(Main.selectFlashButton).toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should subtitle have correct initial text', async () => {
      if (process.platform === 'linux') {      
        await expectWDIO(Main.selectWriteCardSubtitle).toHaveText('Flash to device with ktool-linux')
      }
      if (process.platform === 'win32') {
        await expectWDIO(Main.selectWriteCardSubtitle).toHaveText('Flash to device with ktool-win.exe')
      }
      if (process.platform === 'darwin') {
        await expectWDIO(Main.selectWriteCardSubtitle).toHaveText('Flash to device with ktool-mac')
      }
    })
    
    // eslint-disable-next-line no-undef
    it('should have a clickable flash button', async () => {
      await expectWDIO(Main.selectFlashButton).toBeClickable()
    })

    // eslint-disable-next-line no-undef
    it('should button have correct initial text', async () => {
      const writeButtonText = await Main.selectFlashButton.$('span.v-btn__content').getText() 
      expectChai(writeButtonText).to.be.equal(' FLASH')
    })
  })
})
