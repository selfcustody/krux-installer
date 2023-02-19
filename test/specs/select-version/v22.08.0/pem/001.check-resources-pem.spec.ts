import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../../pageobjects/check-resources-official-release-sha256.page'
import CheckResourcesOfficialReleaseSig from '../../../../pageobjects/check-resources-official-release-sig.page'
import CheckResourcesOfficialReleasePem from '../../../../pageobjects/check-resources-official-release-pem.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: check if \'selfcustody.pem\' exists', () => {
 
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
    await SelectVersion.list_item_22_08_0.waitForExist()
    await SelectVersion.list_item_22_08_1.waitForExist()
    await SelectVersion.list_item_22_08_2.waitForExist()
    await SelectVersion.list_item_krux_binaries.waitForExist()
    await delay(1000) 
    await SelectVersion.list_item_22_08_0.click()
    await SelectVersion.formSelectButton.waitForExist()
    await SelectVersion.formSelectButton.click()
    await CheckResourcesOfficialRelease.page.waitForExist() 
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
    await CheckResourcesOfficialReleaseSig.buttonDownload.waitForExist()
    await CheckResourcesOfficialReleaseSig.buttonProceed.click()
  })

  // eslint-disable-next-line no-undef
  it('should check', async () => {   
    await expectWDIO(CheckResourcesOfficialReleasePem.cardTitleChecking)
      .toHaveText('Checking selfcustody public key certificate...')
  })

})