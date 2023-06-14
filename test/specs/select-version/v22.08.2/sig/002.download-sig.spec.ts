import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../../pageobjects/check-resources-official-release-sha256.page'
import CheckResourcesOfficialReleaseSig from '../../../../pageobjects/check-resources-official-release-sig.page'
import DownloadOfficialReleaseSig from '../../../../pageobjects/download-official-release-sig.page'

// eslint-disable-next-line no-undef
describe('SelectVersionPage: download \'v22.08.2/krux-v22.08.2.zip.sig\' option', () => {

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
    await SelectVersion.list_item_22_08_2.waitForExist()
    await SelectVersion.list_item_krux_binaries.waitForExist()
    await delay(1000) 
    await SelectVersion.list_item_22_08_2.click()
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
    await CheckResourcesOfficialReleaseSig.page.waitForExist({ reverse: true })
    await DownloadOfficialReleaseSig.page.waitForExist()
    await delay(1000)
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Downloading...\'', async () => {  
    await DownloadOfficialReleaseSig.cardTitle.waitForExist()
    await expectWDIO(DownloadOfficialReleaseSig.cardTitle).toHaveText('Downloading...')
  })

  // eslint-disable-next-line no-undef
  it('should card subtitle be \'selfcustody/krux/releases/download/v22.08.2/krux-v22.08.2.zip.sig\'', async () => {  
    await DownloadOfficialReleaseSig.cardSubtitle.waitForExist()
    await expectWDIO(DownloadOfficialReleaseSig.cardSubtitle).toHaveText('selfcustody/krux/releases/download/v22.08.2/krux-v22.08.2.zip.sig...')
  })

  // TODO: the sig file is 
  // very tiny (65 Bytes)
  // In local tests this pass and,
  // in github-action, fail (probably because
  // the github-action have a faster network)
  // so, disable until fix this
  // eslint-disable-next-line no-undef 
  it('should download release signature file', async () => { 
    await DownloadOfficialReleaseSig.progressLinearText.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent !== 0
    }, {
      interval: 1
    })
    await DownloadOfficialReleaseSig.progressLinearText.waitForExist({ reverse: true })
  })
})
