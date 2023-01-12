import Logo from '../pageobjects/logo.page'

// eslint-disable-next-line no-undef
describe('KruxInstaller sided logo', () => {

  // eslint-disable-next-line no-undef
  it('should have banner', () => {
    
    // eslint-disable-next-line no-undef
    expect(Logo.banner).toBeDisplayed()
  })


  // eslint-disable-next-line no-undef
  it('should have asciiart', () => {
    
    // eslint-disable-next-line no-undef
    expect(Logo.asciiart).toBeDisplayed()
    

    // eslint-disable-next-line no-undef
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

  // eslint-disable-next-line no-undef
  it('should have title text', () => {
    
    // eslint-disable-next-line no-undef
    expect(Logo.title).toBeDisplayed()
    
    // eslint-disable-next-line no-undef
    expect(Logo.title).toHaveText('Krux Installer')
  })

})
