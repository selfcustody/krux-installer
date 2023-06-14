import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: page select \'selfcustody/krux/releases/tag/v22.08.2\' option', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.page.waitForExist()
    await Main.selectVersionButton.click()
    await Main.page.waitForExist({ reverse: true })
    await SelectVersion.page.waitForExist()
    await SelectVersion.formArrow.waitForExist()
    await SelectVersion.formArrow.click()
    await SelectVersion.formSelectContainer.waitForExist() 
    await SelectVersion.list_item_22_08_2.waitForExist() 
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should be selected', async () => {     
    await SelectVersion.list_item_22_08_2.click()
    await SelectVersion.formSelected.waitForExist()
    await expectWDIO(SelectVersion.formSelected).toHaveText('selfcustody/krux/releases/tag/v22.08.2')
  })

  // eslint-disable-next-line no-undef
  it('should click \'back\' go out of SelectVersionPage', async () => {   
    await SelectVersion.formBackButton.click()
    await Main.page.waitForExist()
    await expectWDIO(SelectVersion.page).not.toBeDisplayed()  
    await delay(1000)
  })
  
  // eslint-disable-next-line no-undef
  it('should the \'SELECT VERSION\' button not changed', async () => {  
    const deviceButtonContent = await Main.selectVersionButton.$('span.v-btn__content')    
    await expectWDIO(deviceButtonContent).toHaveText('SELECT VERSION')
    await expectWDIO(deviceButtonContent).not.toHaveText('SELFCUSTODY/KRUX/RELEASES/TAG/V22.08.2')
  })
})
