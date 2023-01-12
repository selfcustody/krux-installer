import Logo from '../pageobjects/logo.page'

describe('KruxInstaller sided logo', () => {

  it('should have banner', () => {
    expect(Logo.banner).toBeDisplayed()
  })

  it('should have asciiart', () => {
    expect(Logo.asciiart).toBeDisplayed()
    expect(Logo.asciiart).toHaveText([ 
      "     ██        ",
      "     ██        ",
      "     ██        ",
      "   ██████      ",
      "     ██        ",
      "     ██  ██    ",
      "     ██ ██     ",
      "     ████      ",
      "     ██ ██     ",
      "     ██  ██    ",
      "     ██   ██   "
    ].join('\n'))
  })

  it('should have title text', () => {
    expect(Logo.title).toBeDisplayed()
    expect(Logo.title).toHaveText('Krux Installer')
  })

})
