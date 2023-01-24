import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectVersion from '../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: go to and check elements', () => {

  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.click()
  })

  // eslint-disable-next-line no-undef
  it('should not be in MainPage', async () => {
    await expectWDIO(Main.page).not.toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should be in SelectVersionPage', async () => {
    await expectWDIO(SelectVersion.page).toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  describe('transitional \'checking\'', () => {

    // eslint-disable-next-line no-undef
    after(async () => {
      await delay(3000)
    })

    // eslint-disable-next-line no-undef
    it('should have an \'checking\' card title', async () => {  
      await expectWDIO(SelectVersion.cardTitleChecking).toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should not have an \'checked\' card title', async () => {   
      await expectWDIO(SelectVersion.cardTitleChecked).not.toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should \'checking\' card title be the text \'Checking...\'', async () => { 
      await expectWDIO(SelectVersion.cardTitleChecking).toHaveText('Checking...')
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'checked\'', () => {

    // eslint-disable-next-line no-undef
    it('should not have an \'checking\' card title after some time', async () => {  
      await expectWDIO(SelectVersion.cardTitleChecking).not.toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should have an \'checked\' card title', async () => {   
      await expectWDIO(SelectVersion.cardTitleChecked).toBeDisplayed()
    })

    // eslint-disable-next-line no-undef
    it('should title changed to be \'Select between...\'', async () => {  
      await expectWDIO(SelectVersion.cardTitleChecked).toHaveText('Select between selfcustody or odudex releases')
    })


    // eslint-disable-next-line no-undef
    it('should have the card to select devices', async () => {
      await expectWDIO(SelectVersion.cardContent).toExist()
    })

    // eslint-disable-next-line no-undef
    it('should have the container that contain the select object', async () => {
      await expectWDIO(SelectVersion.formSelectContainer).toExist()
    })

    // eslint-disable-next-line no-undef
    it('should have the control that controls the select object', async () => {
      await expectWDIO(SelectVersion.formSelectField).toExist()
    })

    // eslint-disable-next-line no-undef
    it('should have the label that contain the \'Versions\' text', async () => {
      await expectWDIO(SelectVersion.formSelectLabel).toExist()
      await expectWDIO(SelectVersion.formSelectLabel).toHaveText('Versions')
    })

    // eslint-disable-next-line no-undef
    it('should have a container that contains the \'down arrow\'', async () => { 
      await expectWDIO(SelectVersion.formArrowContainer).toExist()
    })

    // eslint-disable-next-line no-undef
    it('should have a \'down arrow\'', async () => { 
      await expectWDIO(SelectVersion.formArrow).toExist()
      await expectWDIO(SelectVersion.formArrow).toHaveAttribute('class', 'mdi-menu-down mdi v-icon notranslate v-theme--light v-icon--size-default')
    })
  
    // eslint-disable-next-line no-undef
    it('should not have \'SELECT\' button', async () => { 
      await expectWDIO(SelectVersion.formSelectButton).not.toExists
    })

    // eslint-disable-next-line no-undef
    it('should have \'BACK\' button', async () => { 
      await expectWDIO(SelectVersion.formBackButton).toExists
      await expectWDIO(SelectVersion.formBackButton).toHaveText('BACK')
    })
  })
})
