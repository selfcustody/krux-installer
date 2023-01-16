import { expect as expectWDIO } from '@wdio/globals'
import Logo from '../pageobjects/logo.page'

// eslint-disable-next-line no-undef
describe('Sided logo', () => {

  // eslint-disable-next-line no-undef
  it('should have banner', () => { 
    expectWDIO(Logo.banner).toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should have asciiart', () => { 
    expectWDIO(Logo.asciiart).toBeDisplayed()
    expectWDIO(Logo.asciiart).toHaveText([ 
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
    expectWDIO(Logo.title).toBeDisplayed()
    expectWDIO(Logo.title).toHaveText('Krux Installer')
  })
})
