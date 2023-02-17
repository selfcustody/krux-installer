import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../../pageobjects/check-resources-official-release.page'
import DownloadOfficialRelease from '../../../../pageobjects/download-official-release.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: download \'selfcustody/krux/releases/tag/v22.03.0\' option', () => {

  // eslint-disable-next-line no-undef
  before(async () => {
    await Main.selectVersionButton.waitForExist()
    await delay(1000)
    await Main.selectVersionButton.click()
    await SelectVersion.cardTitleChecking.waitForExist()
    await delay(1000)
    await SelectVersion.cardTitleChecked.waitForExist()  
    await SelectVersion.cardSubtitleOfficial.waitForExist()  
    await SelectVersion.cardSubtitleTest.waitForExist()  
    await SelectVersion.formArrow.waitForExist()
    await SelectVersion.formBackButton.waitForExist()  
    await delay(1000)
    await SelectVersion.formArrow.click()
    await delay(1000)
    await SelectVersion.list_item_22_03_0.waitForExist()
    await SelectVersion.list_item_krux_binaries.waitForExist()
    await delay(1000) 
    await SelectVersion.list_item_22_03_0.click()
    await delay(1000)
    await SelectVersion.formSelectButton.waitForExist()
    await SelectVersion.formSelectButton.click()  
    await SelectVersion.page.waitForExist({ reverse: true }) 
    await CheckResourcesOfficialRelease.page.waitForExist() 
    await CheckResourcesOfficialRelease.page.waitForExist({ reverse: true })
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Downloading...\'', async () => { 
    await DownloadOfficialRelease.page.waitForExist()
    await DownloadOfficialRelease.cardTitle.waitForExist()
    await expectWDIO(DownloadOfficialRelease.cardTitle).toHaveText('Downloading...')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'selfcustody/krux/releases/download/v22.03.0/krux-v22.03.0.zip\'', async () => {  
    await DownloadOfficialRelease.cardSubtitle.waitForExist()
    await expectWDIO(DownloadOfficialRelease.cardSubtitle).toHaveText('selfcustody/krux/releases/download/v22.03.0/krux-v22.03.0.zip')
  })

  // eslint-disable-next-line no-undef
  it('should download release zip file', async () => { 
    await DownloadOfficialRelease.progressLinearText.waitForExist()
    await DownloadOfficialRelease.progressLinearText.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent !== 0
    }, {
      timeout: 120000,
      interval: 50
    })
    await DownloadOfficialRelease.page.waitForExist({ reverse: true, timeout: 120000 })
  })
})
