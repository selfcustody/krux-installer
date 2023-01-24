import { expect as expectWDIO } from '@wdio/globals'
import Logo from '../../pageobjects/logo.page'

// eslint-disable-next-line no-undef
describe('Sided logo', () => {

  // eslint-disable-next-line no-undef
  it('should have banner', async () => { 
    await expectWDIO(Logo.banner).toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should have asciiart', async () => { 
    await expectWDIO(Logo.asciiart).toBeDisplayed()
  })

  
  // eslint-disable-next-line no-undef
  it('should asciiart be correct', async () => { 
    // TODO: investigate how 
    // asciimorph allocate characters
    // on html elements
    const logo = [
      "██        ",
      "     ██        ",
      "     ██        ",
      "   ██████      ",
      "     ██        ",
      "     ██  ██    ",
      "     ██ ██     ",
      "     ████      ",
      "     ██ ██     ",
      "     ██  ██    ",
      "     ██   ██"
    ].join('\n')
    await expectWDIO(Logo.asciiart).toHaveText(logo)
  })

  // eslint-disable-next-line no-undef
  it('should have title text', async () => {
    await expectWDIO(Logo.title).toBeDisplayed()
    await expectWDIO(Logo.title).toHaveText('Krux Installer')
  })
})
