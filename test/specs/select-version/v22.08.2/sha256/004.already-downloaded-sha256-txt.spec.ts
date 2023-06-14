import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../../pageobjects/check-resources-official-release-sha256.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: warn before download \'selfcustody/krux/releases/tag/v22.08.2.sha256.txt\' again', () => {
  
  // eslint-disable-next-line no-undef
  before(async () => {
    // eslint-disable-next-line no-undef
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
    await SelectVersion.list_item_22_08_2.waitForExist()
    await SelectVersion.list_item_krux_binaries.waitForExist()
    await delay(1000) 
    await SelectVersion.list_item_22_08_2.click()
    await SelectVersion.formSelectButton.waitForExist()
    await SelectVersion.formSelectButton.click()  
    await SelectVersion.page.waitForExist({ reverse: true }) 
    await CheckResourcesOfficialRelease.page.waitForExist() 
    await CheckResourcesOfficialRelease.cardTitleChecking.waitForExist()
    await CheckResourcesOfficialRelease.cardTitleChecking.waitForExist({ reverse: true }) 
    await CheckResourcesOfficialRelease.cardTitleChecked.waitForExist()
    await CheckResourcesOfficialRelease.cardSubtitleChecked.waitForExist()
    await CheckResourcesOfficialRelease.cardContentChecked.waitForExist()
    await CheckResourcesOfficialRelease.buttonDownload.waitForExist()
    await CheckResourcesOfficialRelease.buttonProceed.waitForExist()
    await CheckResourcesOfficialRelease.buttonProceed.click()
    await CheckResourcesOfficialRelease.page.waitForExist({ reverse: true })
    await CheckResourcesOfficialReleaseSHA256.page.waitForExist()
    await CheckResourcesOfficialReleaseSHA256.cardTitleChecking.waitForExist()
    await CheckResourcesOfficialReleaseSHA256.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesOfficialReleaseSHA256.cardTitleChecked.waitForExist()
    await CheckResourcesOfficialReleaseSHA256.cardSubtitleChecked.waitForExist()
    await CheckResourcesOfficialReleaseSHA256.cardContentChecked.waitForExist()
    await delay(1000)
  })

    
  // eslint-disable-next-line no-undef
  it('should card title be \'v22.08.2/krux-v22.08.2.zip.sha256.txt\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleaseSHA256.cardTitleChecked).toHaveText('v22.08.2/krux-v22.08.2.zip.sha256.txt')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'Already downloaded\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleaseSHA256.cardSubtitleChecked).toHaveText('Already downloaded')
  })

  // eslint-disable-next-line no-undef
  it('should card content be \'Click "Proceed" to proceed with the downloaded version or "Download the file again".\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleaseSHA256.cardContentChecked)
      .toHaveText('Click "Proceed" to proceed with the downloaded version or "Download the file again".')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'PROCEED\' button', async () => { 
    await expectWDIO(CheckResourcesOfficialReleaseSHA256.buttonProceed).toHaveText('PROCEED')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'DOWNLOAD THE FILE AGAIN\' button', async () => { 
    await expectWDIO(CheckResourcesOfficialReleaseSHA256.buttonDownload).toHaveText('DOWNLOAD THE FILE AGAIN')
  })
})
