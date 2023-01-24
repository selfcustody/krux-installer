import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectVersion from '../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: page select \'selfcustody/krux/releases/tag/v22.03.0\' option', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.click()
    await SelectVersion.cardTitleChecked.waitForExist({ timeout: 5000 })
    await SelectVersion.formArrow.click()
    await SelectVersion.list_item_22_03_0.waitForExist({ timeout: 5000 })
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should be selected', async () => {    
    await SelectVersion.list_item_22_03_0.click()
    await expectWDIO(SelectVersion.formSelected).toHaveText('selfcustody/krux/releases/tag/v22.03.0')
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should click \'back\' go out of SelectVersionPage', async () => {   
    await SelectVersion.formBackButton.click()
    await Main.page.waitForExist({ timeout: 5000 })
    await expectWDIO(SelectVersion.page).not.toBeDisplayed()  
    await delay(1000)
  })
  
  // eslint-disable-next-line no-undef
  it('should the \'SELECT DEVICE\' button not changed', async () => {  
    const deviceButtonText = await Main.selectVersionButton.$('span.v-btn__content').getText()    
    expectChai(deviceButtonText).to.be.equal(' SELECT VERSION')
    expectChai(deviceButtonText).not.to.be.equal(' SELFCUSTODY/KRUX/RELEASES/TAG/V22.03.0')
  })
})
