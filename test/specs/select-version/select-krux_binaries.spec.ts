import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectVersion from '../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: page select \'odudex/krux_binaries\' option', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.click()
    await SelectVersion.formArrow.waitForExist()
    await SelectVersion.formArrow.click()
    await SelectVersion.list_item_krux_binaries.waitForExist()
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should be selected', async () => {    
    await SelectVersion.list_item_krux_binaries.click()
    await delay(1000)
    await expectWDIO(SelectVersion.formSelected).toHaveText('odudex/krux_binaries')
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
    await expectWDIO(deviceButtonContent).not.toHaveText('ODUDEX/KRUX_BINARIES')
  })
})
