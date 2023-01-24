import { expect as expectWDIO } from '@wdio/globals'
import Main from '../../pageobjects/main.page'
import SelectDevice from '../../pageobjects/select-device.page'

// eslint-disable-next-line no-undef
describe('SelectDevice page before change', () => {
  
  // eslint-disable-next-line no-undef
  it('should be in MainPage', async () => { 
    await expectWDIO(Main.page).toBeDisplayed()
  })

  // eslint-disable-next-line no-undef
  it('should not be in SelectDevicePage', async () => { 
    await expectWDIO(SelectDevice.page).not.toBeDisplayed()
  })
})
