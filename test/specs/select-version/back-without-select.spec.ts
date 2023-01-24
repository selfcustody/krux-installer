import { expect as expectChai } from 'chai'
import { expect as expectWDIO } from '@wdio/globals'
import delay from '../delay'
import Main from '../../pageobjects/main.page'
import SelectVersion from '../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: go to and back to MainPage', () => {

  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.click()
    await delay(1000)
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
  it('should click \'BACK\' and go to main page', async () => { 
    await SelectVersion.formBackButton.click()
    await delay(1000)
    await expectWDIO(Main.page).toBeDisplayed()
    await expectWDIO(SelectVersion.page).not.toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should \'SELECT DEVICE\' in MainPage button did not changed', async () => {
    const deviceButtonText = await Main.selectDeviceButton.$('span.v-btn__content').getText()  
    expectChai(deviceButtonText).to.be.equal(' SELECT DEVICE')
  })
})
