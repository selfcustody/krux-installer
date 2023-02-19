import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: page select \'selfcustody/krux/releases/tag/v22.08.0\' option', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.click()
    await SelectVersion.formArrow.waitForExist()
    await SelectVersion.formArrow.click()
    await SelectVersion.list_item_22_08_0.waitForExist()
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should be selected', async () => {    
    await SelectVersion.list_item_22_08_0.click()
    await delay(1000)
    await expectWDIO(SelectVersion.formSelected).toHaveText('selfcustody/krux/releases/tag/v22.08.0')
    await delay(1000)
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
    await expectWDIO(deviceButtonContent).not.toHaveText('SELFCUSTODY/KRUX/RELEASES/TAG/V22.08.0')
  })
})
