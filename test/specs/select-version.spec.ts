import { expect as expectWDIO } from '@wdio/globals'
import delay from './delay'
import Main from '../pageobjects/main.page'
import SelectVersion from '../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersion page', () => {

  // eslint-disable-next-line no-undef
  describe('before change', () => {
    // eslint-disable-next-line no-undef
    it('should be in MainPage', async () => { 
      expectWDIO(Main.page).toBeDisplayed()
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should\'nt be in SelectVersionPage', async () => { 
      await delay(1000)
      expectWDIO(SelectVersion.page).not.toBeDisplayed()
      await delay(1000)
    })
  })

  // eslint-disable-next-line no-undef
  describe('on change', () => {

    // eslint-disable-next-line no-undef
    it('should click \'select version\' button', async () => {
      await delay(1000)
      await Main.selectVersionButton.click()
    })

    // eslint-disable-next-line no-undef
    it('should\'nt be in MainPage', () => {
      expectWDIO(Main.page).not.toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should be in SelectVersionPage', () => {
      expectWDIO(SelectVersion.page).toBeDisplayed()
    })
  })

  
  // eslint-disable-next-line no-undef
  describe('after change, but not clicking anything yet', () => {

    // eslint-disable-next-line no-undef
    it('should title be \'Checking...\'', async () => { 
      expectWDIO(SelectVersion.cardTitleChecking).toBeDisplayed() 
      expectWDIO(SelectVersion.cardTitleChecked).not.toBeDisplayed()
      expectWDIO(SelectVersion.cardTitleChecking).toHaveText('Checking...')
      await delay(3000)
    })

    // eslint-disable-next-line no-undef
    it('should title change to be \'Select between...\'', () => {  
      expectWDIO(SelectVersion.cardTitleChecking).not.toBeDisplayed() 
      expectWDIO(SelectVersion.cardTitleChecked).toBeDisplayed()
      expectWDIO(SelectVersion.cardTitleChecked).toHaveText('Select between selfcustody or odudex releases')
    })

    // eslint-disable-next-line no-undef
    it('should have a subtitle with \'Official: selfcustody/krux/releases/tag/v*\'', () => {  
      expectWDIO(SelectVersion.cardSubtitleOfficial).toBeDisplayed() 
      expectWDIO(SelectVersion.cardSubtitleOfficial).toHaveText('Official: selfcustody/krux/releases/tag/v*')
    })

    // eslint-disable-next-line no-undef
    it('should have a subtitle with \'Test: odudex/krux_binaries\'', () => {  
      expectWDIO(SelectVersion.cardSubtitleTest).toBeDisplayed() 
      expectWDIO(SelectVersion.cardSubtitleTest).toHaveText('Test: odudex/krux_binaries')
    })

    // eslint-disable-next-line no-undef
    it('should have a form to select versions, without select button', () => {   
      expectWDIO(SelectVersion.formSelect).toExist()
      expectWDIO(SelectVersion.formSelectLabel).toExist() 
      expectWDIO(SelectVersion.formSelectButton).not.toExist()
      expectWDIO(SelectVersion.formBackButton).toExist()
      expectWDIO(SelectVersion.formSelectLabel).toHaveText('Versions')
      expectWDIO(SelectVersion.formBackButton).toHaveText('BACK')
    })

    // eslint-disable-next-line no-undef
    it('should select \'down arrow\' to not be selected yet', async () => {
      expectWDIO(SelectVersion.formArrowContainer).toHaveAttr('class', 'v-input--horizontal')
      expectWDIO(SelectVersion.formArrowContainer).toHaveAttr('class', 'v-input--density-default')
      expectWDIO(SelectVersion.formArrowContainer).toHaveAttr('class', 'v-input--readonly')
      expectWDIO(SelectVersion.formArrowContainer).toHaveAttr('class', 'v-text-field')
      expectWDIO(SelectVersion.formArrowContainer).toHaveAttr('class', 'v-select')
      expectWDIO(SelectVersion.formArrowContainer).toHaveAttr('class', 'v-select-single')
      expectWDIO(SelectVersion.formArrowContainer).toHaveAttr('class', 'v-select-single--selected') 
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('class', 'v-field--active')
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('class', 'v-field--appended')
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('class', 'v-field--dirty')
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('class', 'v-field--variant-filled')
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('class', 'v-theme--light')
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('role', 'textbox')
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('aria-expanded', 'false')
    })
  })
})
