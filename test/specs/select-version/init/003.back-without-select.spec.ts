import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../delay'
import Main from '../../../pageobjects/main.page'
import SelectVersion from '../../../pageobjects/select-version.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: click \'SELECT VERSION\' and back to MainPage', () => {

  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.waitForExist()
    await delay(1000)
    await Main.selectVersionButton.click()
    await delay(1000)
    await SelectVersion.formBackButton.waitForExist()
    await delay(1000)
    await SelectVersion.formBackButton.click()
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should \'SELECT VERSION\' in MainPage button did not changed', async () => {
    await expectWDIO(Main.selectVersionButtonContent).toHaveText('SELECT VERSION')
  })
})
