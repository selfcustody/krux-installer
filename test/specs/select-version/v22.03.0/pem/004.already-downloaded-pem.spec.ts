import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../../pageobjects/check-resources-official-release-sha256.page'
import CheckResourcesOfficialReleaseSig from '../../../../pageobjects/check-resources-official-release-sig.page'
import CheckResourcesOfficialReleasePem from '../../../../pageobjects/check-resources-official-release-pem.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: warn before download \'selfcustody.pem\' again', () => {
  
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
    await SelectVersion.list_item_22_03_0.click()
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
    await CheckResourcesOfficialReleaseSig.buttonProceed.waitForExist()
    await CheckResourcesOfficialReleaseSig.buttonProceed.click()
    await CheckResourcesOfficialReleaseSig.page.waitForExist({ reverse: true }) 
    await CheckResourcesOfficialReleasePem.page.waitForExist()
    await delay(1000)
  })

    
  // eslint-disable-next-line no-undef
  it('should card title be \'main/selfcustody.pem\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleasePem.cardTitleChecked).toHaveText('main/selfcustody.pem')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'Already downloaded\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleasePem.cardSubtitleChecked).toHaveText('Already downloaded')
  })

  // eslint-disable-next-line no-undef
  it('should card content be \'Click "Proceed" to proceed with the downloaded version or "Download the file again".\'', async () => {
    await expectWDIO(CheckResourcesOfficialReleasePem.cardContentChecked)
      .toHaveText('Click "Proceed" to proceed with the downloaded version or "Download the file again".')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'PROCEED\' button', async () => { 
    await expectWDIO(CheckResourcesOfficialReleasePem.buttonProceed).toHaveText('PROCEED')
  })

  // eslint-disable-next-line no-undef
  it('should have a \'DOWNLOAD THE FILE AGAIN\' button', async () => { 
    await expectWDIO(CheckResourcesOfficialReleasePem.buttonDownload).toHaveText('DOWNLOAD THE FILE AGAIN')
  })
})
