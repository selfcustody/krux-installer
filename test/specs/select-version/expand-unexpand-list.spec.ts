import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectVersion from '../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: expand/unexpand selection list', () => {

  // eslint-disable-next-line no-undef
  describe('preparation', () => {
  
    // eslint-disable-next-line no-undef
    before(async () => { 
      await Main.selectVersionButton.waitForExist()
      await delay(1000)
      await Main.selectVersionButton.click()
      await SelectVersion.formOverlayContainer.waitForExist() 
      await SelectVersion.formSelectFieldContainer.waitForExist()
      await SelectVersion.formArrow.waitForExist()
      await delay(1000)
    })

    // eslint-disable-next-line no-undef 
    it('should arrow to be not expanded yet', async () => { 
      await expectWDIO(SelectVersion.formSelectFieldContainer).toHaveAttribute('aria-expanded', 'false')
    })
  })

  // eslint-disable-next-line no-undef
  describe('expand/unexpand', () => {
   
    // eslint-disable-next-line no-undef
    beforeEach(async () => {
      await SelectVersion.formArrow.click()
      await SelectVersion.formSelectFieldContainer.waitForExist()
      await delay(1000)
    })

    // eslint-disable-next-line no-undef
    it('click on arrow first time and expand list', async () => { 
      await expectWDIO(SelectVersion.formSelectFieldContainer).toHaveAttribute('aria-expanded', 'true')
    })

    // eslint-disable-next-line no-undef
    it('click on arrow a second time and unexpand list', async () => { 
      await expectWDIO(SelectVersion.formSelectFieldContainer).toHaveAttr('aria-expanded', 'false')
    })
    
    // eslint-disable-next-line no-undef
    it('should click on arrow a third time and expand list', async () => {  
      await expectWDIO(SelectVersion.formSelectFieldContainer).toHaveAttribute('aria-expanded', 'true')
    }) 
  })

  // eslint-disable-next-line no-undef
  describe('have options', () => {

    // eslint-disable-next-line no-undef
    before(async () => {
      await SelectVersion.list_item_22_03_0.waitForExist()
      await SelectVersion.list_item_22_08_0.waitForExist()
      await SelectVersion.list_item_22_08_1.waitForExist()
      await SelectVersion.list_item_22_08_2.waitForExist() 
      await SelectVersion.list_item_krux_binaries.waitForExist()
    })
    
    // eslint-disable-next-line no-undef
    it('should have \'selfcustody/krux/releases/tag/v22.03.0\' option', async () => {
      await expectWDIO(SelectVersion.list_item_22_03_0).toHaveText('selfcustody/krux/releases/tag/v22.03.0')
    })

    // eslint-disable-next-line no-undef
    it('should have \'selfcustody/krux/releases/tag/v22.08.0\' option', async () => {
      await expectWDIO(SelectVersion.list_item_22_08_0).toHaveText('selfcustody/krux/releases/tag/v22.08.0')
    })

    // eslint-disable-next-line no-undef
    it('should have \'selfcustody/krux/releases/tag/v22.08.1\' option', async () => {
      await expectWDIO(SelectVersion.list_item_22_08_1).toHaveText('selfcustody/krux/releases/tag/v22.08.1')
    })

    // eslint-disable-next-line no-undef
    it('should have \'selfcustody/krux/releases/tag/v22.08.2\' option', async () => {
      await expectWDIO(SelectVersion.list_item_22_08_2).toHaveText('selfcustody/krux/releases/tag/v22.08.2')
    })

    // eslint-disable-next-line no-undef
    it('should have \'odudex/krux_binaries\' option', async () => {
      await expectWDIO(SelectVersion.list_item_krux_binaries).toHaveText('odudex/krux_binaries')
    })
  })
})
