import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../../delay'
import Main from '../../../../pageobjects/main.page'
import SelectVersion from '../../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../../pageobjects/check-resources-official-release-sha256.page'
import CheckResourcesOfficialReleaseSig from '../../../../pageobjects/check-resources-official-release-sig.page'
import CheckResourcesOfficialReleasePem from '../../../../pageobjects/check-resources-official-release-pem.page'
import VerifyOfficialRelease from '../../../../pageobjects/verify-official-release.page'
import UnzipOfficialRelease from '../../../../pageobjects/unzip-official-release.page'

// eslint-disable-next-line no-undef
describe('Unzip \'v22.03.0/krux-v22.03.0.zip\' release', () => {
  
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
    await CheckResourcesOfficialReleasePem.cardTitleChecking.waitForExist()
    await CheckResourcesOfficialReleasePem.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesOfficialReleasePem.cardTitleChecked.waitForExist()
    await CheckResourcesOfficialReleasePem.cardSubtitleChecked.waitForExist()
    await CheckResourcesOfficialReleasePem.cardContentChecked.waitForExist() 
    await CheckResourcesOfficialReleasePem.buttonProceed.waitForExist()
    await CheckResourcesOfficialReleasePem.buttonDownload.waitForExist()
    await CheckResourcesOfficialReleasePem.buttonProceed.click()
    await VerifyOfficialRelease.page.waitForExist()
    await VerifyOfficialRelease.cardTitleChecking.waitForExist() 
    await VerifyOfficialRelease.cardTitleChecking.waitForExist({ reverse: true })
    await VerifyOfficialRelease.cardTitleChecked.waitForExist() 
    await VerifyOfficialRelease.cardSubtitleSha256sumChecked.waitForExist()
    await VerifyOfficialRelease.cardSubtitleSigChecked.waitForExist()
    await VerifyOfficialRelease.cardContent.waitForExist()
    await VerifyOfficialRelease.cardContentFilenameTxt.waitForExist()
    await VerifyOfficialRelease.cardContentFilenameSha256.waitForExist()
    await VerifyOfficialRelease.chipHashTxt.waitForExist()
    await VerifyOfficialRelease.chipHashSha256.waitForExist()
    await VerifyOfficialRelease.consoleSignatureCommand.waitForExist()
    await VerifyOfficialRelease.chipSignatureResult.waitForExist()
    await VerifyOfficialRelease.cardActionWarn.waitForExist()
    await VerifyOfficialRelease.cardActionButtonUnzip.waitForExist()
    await VerifyOfficialRelease.cardActionButtonBack.waitForExist()
    await VerifyOfficialRelease.cardActionButtonUnzip.click()
    await VerifyOfficialRelease.page.waitForExist({ reverse: true })
    await UnzipOfficialRelease.page.waitForExist()   
    await UnzipOfficialRelease.cardTitleUnzipping.waitForExist()  
    await UnzipOfficialRelease.cardSubtitleUnzipping.waitForExist()  
    await UnzipOfficialRelease.cardProgressLinearTextUnzipping.waitForExist()
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Unzipping...\'', async () => {  
    await expectWDIO(UnzipOfficialRelease.cardTitleUnzipping).toHaveText('Unzipping...')
  })

  // eslint-disable-next-line no-undef
  it('should subtitle be \'file:\'', async () => { 
    await expectWDIO(UnzipOfficialRelease.cardSubtitleUnzipping).toHaveText('file:')
  })

  // eslint-disable-next-line no-undef
  it('should progress be \'0%\'', async () => {  
    await expectWDIO(UnzipOfficialRelease.cardProgressLinearTextUnzipping).toHaveText('0%')
  })
 
  // eslint-disable-next-line no-undef
  it('should unzip files', async () => {
    await UnzipOfficialRelease.cardProgressLinearTextUnzipping.waitUntil(async function () { 
      const progress = parseFloat(await this.getText())
      return progress !== 0
    }, {
      timeout: 120000,
      interval: 5
    })
    await UnzipOfficialRelease.cardTitleUnzipping.waitForExist({ reverse: true })
  })

  // eslint-disable-next-line no-undef
  it('should title be changed to \'Extracted files\'', async () => {
    await UnzipOfficialRelease.cardTitleUnzipped.waitForExist()
    await expectWDIO(UnzipOfficialRelease.cardTitleUnzipped).toHaveText('Extracted files')
  })

  // eslint-disable-next-line no-undef
  it('should subtitle be changed to \'Relative to: <some path>/krux-installer\'', async () => {
    // eslint-disable-next-line no-undef
    const api = await browser.electronAPI()
    await UnzipOfficialRelease.cardSubitleUnzipped.waitForExist()
    await expectWDIO(UnzipOfficialRelease.cardSubitleUnzipped).toHaveText(`Relative to: ${api.documents}/krux-installer`)
  })


  // eslint-disable-next-line no-undef
  describe('list items', () => {
    
    let childs

    // eslint-disable-next-line no-undef
    before(async () => {
      await UnzipOfficialRelease.cardContentTextUnzipped.waitForExist()
      childs = await UnzipOfficialRelease.cardContentTextUnzipped.$$('div')
    })

    // eslint-disable-next-line no-undef
    it('should have listed \'krux-v22.03.0/ktool-win.exe\'', async () => {
      await expectWDIO(childs[0]).toHaveText('krux-v22.03.0/ktool-win.exe')
    })

    // eslint-disable-next-line no-undef
    it('should have listed \'krux-v22.03.0/ktool-mac\'', async () => {
      await expectWDIO(childs[1]).toHaveText('krux-v22.03.0/ktool-mac')
    })

    // eslint-disable-next-line no-undef
    it('should have listed \'krux-v22.03.0/maixpy_m5stickv/firmware.bin.sig\'', async () => {
      await expectWDIO(childs[2]).toHaveText('krux-v22.03.0/maixpy_m5stickv/firmware.bin.sig')
    })

    // eslint-disable-next-line no-undef
    it('should have listed \'krux-v22.03.0/maixpy_m5stickv/firmware.bin\'', async () => {
      await expectWDIO(childs[3]).toHaveText('krux-v22.03.0/maixpy_m5stickv/firmware.bin')
    })

    // eslint-disable-next-line no-undef
    it('should have listed \'krux-v22.03.0/maixpy_m5stickv/kboot.kfpkg\'', async () => {
      await expectWDIO(childs[4]).toHaveText('krux-v22.03.0/maixpy_m5stickv/kboot.kfpkg')
    })

    // eslint-disable-next-line no-undef
    it('should have listed \'krux-v22.03.0/ktool-linux\'', async () => {
      await expectWDIO(childs[5]).toHaveText('krux-v22.03.0/ktool-linux')
    })
  })
 
  // eslint-disable-next-line no-undef
  describe('buttons', () => {

    // eslint-disable-next-line no-undef
    before(async () => {
      await UnzipOfficialRelease.buttonDone.waitForExist()
      await UnzipOfficialRelease.buttonBack.waitForExist()
    })

    // eslint-disable-next-line no-undef
    it('should have button \'DONE\'', async () => {
      await expectWDIO(UnzipOfficialRelease.buttonDone).toHaveText('DONE')
    })

    // eslint-disable-next-line no-undef
    it('should have button \'BACK\'', async () => {
      await expectWDIO(UnzipOfficialRelease.buttonBack).toHaveText('BACK')
    })
  })

  // eslint-disable-next-line no-undef
  describe('click \'DONE\' and verify button on MainPage', () => {

    // eslint-disable-next-line no-undef
    before(async () => {
      await UnzipOfficialRelease.buttonDone.click()
      await delay(1000)
      await UnzipOfficialRelease.page.waitForExist({ reverse: true })
      await Main.page.waitForExist()
      await Main.selectVersionButton.waitForExist()
    })

    // eslint-disable-next-line no-undef
    it('should button changed from \'SELECT VERSION\' to \'SELFCUSTODY/KRUX/RELEASE/TAG/V22.03.0\' on MainPage', async () => {
      await expectWDIO(Main.selectVersionButton).toHaveText('SELFCUSTODY/KRUX/RELEASES/TAG/V22.03.0')
    })
  })
})
