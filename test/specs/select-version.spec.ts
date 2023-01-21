import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import delay from './delay'
import Main from '../pageobjects/main.page'
import SelectVersion from '../pageobjects/select-version.page'
import CheckResources from '../pageobjects/check-resources.page'
import CheckResourcesOfficialRelease from '../pageobjects/check-resources-official-release.page'
import DownloadOfficialRelease from '../pageobjects/download-official-release.page'

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

  // eslint-disable-next-line no-undef
  describe('after change, back to main menu without select anything', () => {
  
    // eslint-disable-next-line no-undef
    it('should click \'back\' and go to main page', async () => { 
      expectWDIO(Main.page).not.toBeDisplayed()
      expectWDIO(SelectVersion.page).toBeDisplayed()
      await SelectVersion.formBackButton.click()
      await delay(1000)
      expectWDIO(Main.page).toBeDisplayed()
      expectWDIO(SelectVersion.page).not.toBeDisplayed()
    })

    
    // eslint-disable-next-line no-undef
    it('should click \'select version\' button and change page again', async () => {
      await Main.selectVersionButton.click()
      await delay(1000)
      expectWDIO(Main.page).not.toBeDisplayed()
      expectWDIO(SelectVersion.page).toBeDisplayed()
      await delay(1000)
    })
  })

  // eslint-disable-next-line no-undef
  describe('expand/unexpand selection list', () => {

    // eslint-disable-next-line no-undef
    it('should arrow be displayed, but not clicked', async () => {
      expectWDIO(SelectVersion.formArrow).toBeDisplayed()
      expectWDIO(SelectVersion.formOverlayContainer).not.toBeDisplayed()
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('aria-expanded', 'false')
    })

    // eslint-disable-next-line no-undef
    it('should click on arrow first time and expand list', async () => {
      await SelectVersion.formArrow.click()
      await delay(1000)
      expectWDIO(SelectVersion.formOverlayContainer).toBeDisplayed()
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('aria-expanded', 'true')
    })

    // eslint-disable-next-line no-undef
    it('click on arrow second time and unexpand list', async () => {
      await SelectVersion.formArrow.click()
      await delay(1000)
      expectWDIO(SelectVersion.formOverlayContainer).not.toBeDisplayed()
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('aria-expanded', 'false')
    })

    // eslint-disable-next-line no-undef
    it('should click on arrow a third time and re-expand list', async () => {
      await SelectVersion.formArrow.click()
      await delay(1000)
      expectWDIO(SelectVersion.formOverlayContainer).toBeDisplayed()
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('aria-expanded', 'true')
    })

  })

  // eslint-disable-next-line no-undef
  describe('versions options', () => {

    // eslint-disable-next-line no-undef
    it('should have \'selfcustody/krux/releases/tag/v22.03.0\' option', async () => {
      expectWDIO(SelectVersion.list_item_22_03_0).toBeDisplayed()
      expectWDIO(SelectVersion.list_item_22_03_0).toHaveText('selfcustody/krux/releases/tag/v22.03.0')
    })

    // eslint-disable-next-line no-undef
    it('should have \'selfcustody/krux/releases/tag/v22.08.0\' option', async () => {
      expectWDIO(SelectVersion.list_item_22_08_0).toBeDisplayed()
      expectWDIO(SelectVersion.list_item_22_08_0).toHaveText('selfcustody/krux/releases/tag/v22.08.0')
    })

    // eslint-disable-next-line no-undef
    it('should have \'selfcustody/krux/releases/tag/v22.08.1\' option', async () => {
      expectWDIO(SelectVersion.list_item_22_08_1).toBeDisplayed()
      expectWDIO(SelectVersion.list_item_22_08_1).toHaveText('selfcustody/krux/releases/tag/v22.08.1')
    })

    // eslint-disable-next-line no-undef
    it('should have \'selfcustody/krux/releases/tag/v22.08.2\' option', async () => {
      expectWDIO(SelectVersion.list_item_22_08_2).toBeDisplayed()
      expectWDIO(SelectVersion.list_item_22_08_2).toHaveText('selfcustody/krux/releases/tag/v22.08.2')
    })

    // eslint-disable-next-line no-undef
    it('should have \'odudex/krux_binaries\' option', async () => {
      expectWDIO(SelectVersion.list_item_krux_binaries).toBeDisplayed()
      expectWDIO(SelectVersion.list_item_krux_binaries).toHaveText('odudex/krux_binaries')
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'selfcustody/krux/releases/tag/v22.03.0\' option', () => {
  
    // eslint-disable-next-line no-undef
    it('should be selected', async () => { 
      await SelectVersion.list_item_22_03_0.click()
      await delay(1000)
      expectWDIO(SelectVersion.selected).toHaveText('selfcustody/krux/releases/tag/v22.03.0')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should click \'back\' and go out ', async () => { 
      await SelectVersion.formBackButton.click()   
      expectWDIO(SelectVersion.page).not.toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should be in MainPage', async () => {
      expectWDIO(Main.page).toBeDisplayed()
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should button \'select version\' be unchanged', async () => {
      const deviceButtonText = await Main.selectVersionButton.$('span.v-btn__content').getText()     
      expectChai(deviceButtonText).to.be.equal(' SELECT VERSION')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should go back to SelectVersionPage', async () => { 
      await Main.selectVersionButton.click()
      await delay(1000) 
      expectWDIO(SelectVersion.page).toBeDisplayed() 
      await delay(1000) 
    })

    // eslint-disable-next-line no-undef
    it('should click on arrow and re-expand list', async () => {
      await SelectVersion.formArrow.click()
      await delay(1000)
      expectWDIO(SelectVersion.formOverlayContainer).toBeDisplayed()
      expectWDIO(SelectVersion.formArrowWrapper).toHaveAttr('aria-expanded', 'true')
    })

    // eslint-disable-next-line no-undef
    it('should be selected again', async () => { 
      await SelectVersion.list_item_22_03_0.click()
      await delay(1000)
      expectWDIO(SelectVersion.selected).toHaveText('selfcustody/krux/releases/tag/v22.03.0')
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should click \'select\' and go out of SelectVersionPage', async () => { 
      await SelectVersion.formSelectButton.click()   
      expectWDIO(SelectVersion.page).not.toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should be in CheckResourcesPage', async () => { 
      expectWDIO(CheckResources.page).toBeDisplayed()
      expectWDIO(CheckResources.page).toHaveText('Checking between official or test resources...')
      await delay(20)
    })

    // eslint-disable-next-line no-undef
    it('should be in CheckResourcesOfficialReleasePage (checking)', async () => { 
      expectWDIO(CheckResources.page).not.toBeDisplayed()
      expectWDIO(CheckResourcesOfficialRelease.page).toBeDisplayed()
      expectWDIO(CheckResourcesOfficialRelease.cardTitleChecking).toBeDisplayed()
      expectWDIO(CheckResourcesOfficialRelease.cardTitleChecking).toHaveText('Checking official release...')
      await delay(20)
    })

    // eslint-disable-next-line no-undef
    it('should be in DownloadOfficialReleasePage', async () => {  
      expectWDIO(CheckResourcesOfficialRelease.page).not.toBeDisplayed()
      expectWDIO(DownloadOfficialRelease.page).toBeDisplayed()
      expectWDIO(DownloadOfficialRelease.cardTitle).toBeDisplayed()
      expectWDIO(DownloadOfficialRelease.cardSubtitle).toBeDisplayed()
      expectWDIO(DownloadOfficialRelease.cardTitle).toHaveText('Downloading...')
      expectWDIO(DownloadOfficialRelease.cardTitle).toHaveText('selfcustody/v22.03.0/krux-v22.03.0.zip')
      await delay(10000)
    })
  })
})

