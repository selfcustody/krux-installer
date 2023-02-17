import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../delay'
import Main from '../../../pageobjects/main.page'
import BeforeFlash from '../../../pageobjects/before-flash.page'

// eslint-disable-next-line no-undef
describe('BeforeFlashToDevicePage: show warning without any device or version', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.page.waitForExist()
    await Main.selectFlashButton.waitForExist()
    await Main.selectFlashButton.click()
    await delay(1000)
    await BeforeFlash.page.waitForExist()
    await BeforeFlash.cardTitle.waitForExist() 
    await BeforeFlash.cardSubtitleVersion.waitForExist()
    await BeforeFlash.cardSubtitleDevice.waitForExist()
  })

  // eslint-disable-next-line no-undef
  it('should show a title', async () => {    
    await expectWDIO(BeforeFlash.cardTitle).toHaveText('Flash to device')
  })

  // eslint-disable-next-line no-undef
  it('should show an invalid device', async () => {   
    await expectWDIO(BeforeFlash.cardSubtitleVersion).toHaveText('version: Select version')
  })
  
  // eslint-disable-next-line no-undef
  it('should show an invalid version', async () => {   
    await expectWDIO(BeforeFlash.cardSubtitleDevice).toHaveText('device: Select device')
  })
})
