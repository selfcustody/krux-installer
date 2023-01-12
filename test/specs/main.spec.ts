import Main from '../pageobjects/main.page'

describe('KruxInstaller MainPage', () => {

  it('should to be displayed', () => {
    expect(Main.page).toBeDisplayed()
  })

  it('should display menu \'select device\'', () => { 
    expect(Main.selectDeviceCard).toBeDisplayed() 
    expect(Main.selectDeviceCardSubtitle).toBeDisplayed() 
    expect(Main.selectDeviceCardSubtitle).toHaveText(
      'Select between available devices (m5stickV, amigo, bit, dock)')
  })

  it('should display menu \'select version\'', () => {
    expect(Main.selectVersionCard).toBeDisplayed() 
    expect(Main.selectVersionCardSubtitle).toBeDisplayed() 
    expect(Main.selectDeviceCardSubtitle).toHaveText(
      'Select between selfcustody (official) or odudex (test) releases')
  })

  it('should display menu \'select write\'', () => {
    expect(Main.selectWriteCard).toBeDisplayed()
    expect(Main.selectWriteCardSubtitle).toBeDisplayed()
    if (process.platform === 'linux') {
      expect(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-linux')
    }
    if (process.platform === 'win32') {
      expect(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-win.exe')
    }
    if (process.platform === 'darwin') {
      expect(Main.selectDeviceCardSubtitle).toHaveText('Flash to device with ktool-mac')
    }
  })
})
