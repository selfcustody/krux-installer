import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../delay'
import Main from '../../../pageobjects/main.page'
import SelectVersion from '../../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: click \'SELECT VERSION\' button', () => {

  // eslint-disable-next-line no-undef
  before(async () => { 
    await Main.selectVersionButton.waitForExist()
    await delay(1000)
    await Main.selectVersionButton.click()
  })
  
  // eslint-disable-next-line no-undef
  describe('transitional \'checking\'', () => {
 
    // eslint-disable-next-line no-undef
    before(async () => {
      await SelectVersion.cardTitleChecking.waitForExist() 
    })

    // eslint-disable-next-line no-undef 
    after(async () => {
      await SelectVersion.cardTitleChecking.waitForExist({ reverse: true })
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should \'checking\' card title be the text \'Checking...\'', async () => { 
      await expectWDIO(SelectVersion.cardTitleChecking).toHaveText('Checking...')
    })
  })

  // eslint-disable-next-line no-undef
  describe('\'checked\'', () => {

    // eslint-disable-next-line no-undef
    before(async () => {
      await SelectVersion.cardTitleChecked.waitForExist() 
      await SelectVersion.cardContent.waitForExist()  
      await SelectVersion.formSelectContainer.waitForExist()
      await SelectVersion.formSelectField.waitForExist()
      await SelectVersion.formSelectLabel.waitForExist()
      await SelectVersion.formArrowContainer.waitForExist()
      await SelectVersion.formArrow.waitForExist()
      await SelectVersion.formBackButton.waitForExist()
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('should title changed to be \'Select between...\'', async () => {  
      await expectWDIO(SelectVersion.cardTitleChecked).toHaveText('Select between selfcustody or odudex releases')
    })

    // eslint-disable-next-line no-undef
    it('should have the label that contain the \'Versions\' text', async () => {
      await expectWDIO(SelectVersion.formSelectLabel).toHaveText('Versions')
    })

    // eslint-disable-next-line no-undef
    it('should have a \'down arrow\' icon', async () => { 
      await expectWDIO(SelectVersion.formArrow).toHaveAttribute('class', 'mdi-menu-down mdi v-icon notranslate v-theme--light v-icon--size-default')
    })
  
    // eslint-disable-next-line no-undef
    it('should not have \'SELECT\' button', async () => { 
      await expectWDIO(SelectVersion.formSelectButton).not.toExist()
    })

    // eslint-disable-next-line no-undef
    it('should have \'BACK\' button', async () => { 
      await expectWDIO(SelectVersion.formBackButton).toHaveText('BACK')
    })
  })
})
