import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import Main from '../pageobjects/main.page'

// eslint-disable-next-line no-undef
describe('KruxInstaller MainPage', () => {

  // eslint-disable-next-line no-undef
  it('should to be displayed', () => {

    // eslint-disable-next-line no-undef
    expectWDIO(Main.page).toBeDisplayed()
  })


  // eslint-disable-next-line no-undef
  it('should display menu \'select device\'', () => { 
    
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectDeviceCard).toBeDisplayed() 
    
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectDeviceCardSubtitle).toBeDisplayed() 
  
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectDeviceButton).toBeDisplayed() 
  })

  // eslint-disable-next-line no-undef
  it('should display menu \'select version\'', () => {
    
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectVersionCard).toBeDisplayed() 
    
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectVersionCardSubtitle).toBeDisplayed() 
    
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectVersionButton).toBeDisplayed() 
  })


  // eslint-disable-next-line no-undef
  it('should display menu \'select write\'', () => {
    
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectWriteCard).toBeDisplayed()
   
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectWriteCardSubtitle).toBeDisplayed()
   
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectWriteButton).toBeDisplayed()
  })

  it('should subtitles have correct texts', () => {

    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectDeviceCardSubtitle).toHaveText(
      'Select between available devices (m5stickV, amigo, bit, dock)')
 
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectDeviceCardSubtitle).toHaveText(
      'Select between selfcustody (official) or odudex (test) releases')
  
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectWriteCardSubtitle).toBeDisplayed()
    if (process.platform === 'linux') {      
      // eslint-disable-next-line no-undef
      expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-linux')
    }
    if (process.platform === 'win32') {
      // eslint-disable-next-line no-undef
      expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-win.exe')
    }
    if (process.platform === 'darwin') {
      // eslint-disable-next-line no-undef
      expectWDIO(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-mac')
    }
  })

  // eslint-disable-next-line no-undef
  it('should \'select device\' to be clickable', () => {
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectDeviceButton).toBeClickable()
  })

  // eslint-disable-next-line no-undef
  it('should \'select version\' to be clickable', () => {
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectVersionButton).toBeClickable()
  })

  // eslint-disable-next-line no-undef
  it('should \'flash\' to be clickable', () => {
    // eslint-disable-next-line no-undef
    expectWDIO(Main.selectWriteButton).toBeClickable()
  })

  it('should \'select device\' button to be the correct initial text', async () => {
    const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText() 
    expectChai(deviceButtonText).to.be.equal(' SELECT DEVICE')
  })

  it('should \'select version\' button to be the correct initial text', async () => {
    const versionButtonText = await Main.selectVersionButton.$('span.v-btn__content').getText() 
    expectChai(versionButtonText).to.be.equal(' SELECT VERSION')
  })

  it('should \'flash\' button to be the correct initial text', async () => {
    const writeButtonText = await Main.selectWriteButton.$('span.v-btn__content').getText() 
    expectChai(writeButtonText).to.be.equal(' FLASH')
  })
})
