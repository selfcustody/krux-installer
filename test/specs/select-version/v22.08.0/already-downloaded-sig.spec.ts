import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../delay'
import Main from '../../../pageobjects/main.page'
import SelectVersion from '../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../pageobjects/check-resources-official-release-sha256.page'
import CheckResourcesOfficialReleaseSig from '../../../pageobjects/check-resources-official-release-sig.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: warn before download \'selfcustody/krux/releases/tag/v22.08.0.sig\' again', () => {
  
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
    await SelectVersion.list_item_22_03_0.waitForExist()
    await SelectVersion.list_item_22_08_0.waitForExist()
    await SelectVersion.list_item_22_08_1.waitForExist()
    await SelectVersion.list_item_22_08_2.waitForExist()
    await SelectVersion.list_item_krux_binaries.waitForExist()
    await delay(1000) 
    await SelectVersion.list_item_22_08_0.click()
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
    await CheckResourcesOfficialReleaseSHA256.buttonDownload.waitForExist()
    await CheckResourcesOfficialReleaseSHA256.buttonProceed.waitForExist()
    await CheckResourcesOfficialReleaseSHA256.buttonProceed.click()
    await CheckResourcesOfficialReleaseSHA256.page.waitForExist({ reverse: true })
    await CheckResourcesOfficialReleaseSig.page.waitForExist()
    await CheckResourcesOfficialReleaseSig.cardTitleChecking.waitForExist()
    await CheckResourcesOfficialReleaseSig.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesOfficialReleaseSig.cardTitleChecked.waitForExist()
    await CheckResourcesOfficialReleaseSig.cardSubtitleChecked.waitForExist()
    await CheckResourcesOfficialReleaseSig.cardContentChecked.waitForExist()
    await delay(1000)
  })

    
  // eslint-disable-next-line no-undef
  it('should card title be \'v22.08.0/krux-v22.08.0.zip.sig\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleaseSig.cardTitleChecked).toHaveText('v22.08.0/krux-v22.08.0.zip.sig')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'Already downloaded\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleaseSig.cardSubtitleChecked).toHaveText('Already downloaded')
  })

  // eslint-disable-next-line no-undef
  it('should card content be \'Click "Proceed" to proceed with the downloaded version or "Download the file again".\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleaseSig.cardContentChecked)
      .toHaveText('Click "Proceed" to proceed with the downloaded version or "Download the file again".')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'PROCEED\' button', async () => { 
    await expectWDIO(CheckResourcesOfficialReleaseSig.buttonProceed).toHaveText('PROCEED')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'DOWNLOAD THE FILE AGAIN\' button', async () => { 
    await expectWDIO(CheckResourcesOfficialReleaseSig.buttonDownload).toHaveText('DOWNLOAD THE FILE AGAIN')
  })
})
