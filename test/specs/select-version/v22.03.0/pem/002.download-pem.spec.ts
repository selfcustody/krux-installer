import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../../pageobjects/check-resources-official-release-sha256.page'
import CheckResourcesOfficialReleaseSig from '../../../../pageobjects/check-resources-official-release-sig.page'
import CheckResourcesOfficialReleasePem from '../../../../pageobjects/check-resources-official-release-pem.page'
import DownloadOfficialReleasePem from '../../../../pageobjects/download-official-release-pem.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: download \'selfcustody.pem\' option', () => {

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
    await SelectVersion.formSelectButton.waitForExist()
    await SelectVersion.formSelectButton.click()   
    await CheckResourcesOfficialRelease.page.waitForExist() 
    await CheckResourcesOfficialRelease.buttonProceed.waitForExist()
    await CheckResourcesOfficialRelease.buttonProceed.click()
    await CheckResourcesOfficialRelease.page.waitForExist({ reverse: true }) 
    await CheckResourcesOfficialReleaseSHA256.page.waitForExist()
    await CheckResourcesOfficialReleaseSHA256.cardTitleChecking.waitForExist()  
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
    await CheckResourcesOfficialReleaseSig.page.waitForExist({ reverse: true })
    await CheckResourcesOfficialReleasePem.page.waitForExist()
    await CheckResourcesOfficialReleasePem.page.waitForExist({ reverse: true })
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Downloading...\'', async () => {  
    await DownloadOfficialReleasePem.cardTitle.waitForExist()
    await expectWDIO(DownloadOfficialReleasePem.cardTitle).toHaveText('Downloading...')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'main/selfcustody.pem\'', async () => {  
    await DownloadOfficialReleasePem.cardSubtitle.waitForExist()
    await expectWDIO(DownloadOfficialReleasePem.cardSubtitle).toHaveText('main/selfcustody.pem...')
  })

  // TODO: the sha256.txt file is 
  // very tiny (70 Bytes)
  // In local tests this pass and,
  // in github-action, fail (probably because
  // the github-action have a faster network)
  // so, disable until fix this
  // eslint-disable-next-line no-undef 
  it('should download public key certificate file', async () => { 
    /*
     await DownloadOfficialReleasePem.progressLinearText.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent !== 0
    }, {
      interval: 5
    })
    */
    await DownloadOfficialReleasePem.progressLinearText.waitForExist({ reverse: true })
  })
})
