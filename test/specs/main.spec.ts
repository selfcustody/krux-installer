import Main from '../pageobjects/main.page'

// eslint-disable-next-line no-undef
describe('KruxInstaller MainPage', () => {

  // eslint-disable-next-line no-undef
  it('should to be displayed', () => {

    // eslint-disable-next-line no-undef
    expect(Main.page).toBeDisplayed()
  })


  // eslint-disable-next-line no-undef
  it('should display menu \'select device\'', () => { 
    
    // eslint-disable-next-line no-undef
    expect(Main.selectDeviceCard).toBeDisplayed() 
    
    // eslint-disable-next-line no-undef
    expect(Main.selectDeviceCardSubtitle).toBeDisplayed() 
    
    // eslint-disable-next-line no-undef
    expect(Main.selectDeviceCardSubtitle).toHaveText(
      'Select between available devices (m5stickV, amigo, bit, dock)')
  })


  // eslint-disable-next-line no-undef
  it('should display menu \'select version\'', () => {
    
    // eslint-disable-next-line no-undef
    expect(Main.selectVersionCard).toBeDisplayed() 
    
    // eslint-disable-next-line no-undef
    expect(Main.selectVersionCardSubtitle).toBeDisplayed() 
    
    // eslint-disable-next-line no-undef
    expect(Main.selectDeviceCardSubtitle).toHaveText(
      'Select between selfcustody (official) or odudex (test) releases')
  })


  // eslint-disable-next-line no-undef
  it('should display menu \'select write\'', () => {
    
    // eslint-disable-next-line no-undef
    expect(Main.selectWriteCard).toBeDisplayed()
    
    // eslint-disable-next-line no-undef
    expect(Main.selectWriteCardSubtitle).toBeDisplayed()
    if (process.platform === 'linux') {
      
      // eslint-disable-next-line no-undef
      expect(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-linux')
    }
    if (process.platform === 'win32') {
      
      // eslint-disable-next-line no-undef
      expect(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-win.exe')
    }
    if (process.platform === 'darwin') {
      
      // eslint-disable-next-line no-undef
      expect(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-mac')
    }
  })
})
