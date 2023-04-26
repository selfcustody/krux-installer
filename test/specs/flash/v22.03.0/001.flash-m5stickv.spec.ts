import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../delay'
import Main from '../../../pageobjects/main.page'
import SelectDevice from '../../../pageobjects/select-device.page'
import SelectVersion from '../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../pageobjects/check-resources-official-release-sha256.page'
import CheckResourcesOfficialReleaseSig from '../../../pageobjects/check-resources-official-release-sig.page'
import CheckResourcesOfficialReleasePem from '../../../pageobjects/check-resources-official-release-pem.page'
import VerifyOfficialRelease from '../../../pageobjects/verify-official-release.page'
import UnzipOfficialRelease from '../../../pageobjects/unzip-official-release.page'
import BeforeFlash from '../../../pageobjects/before-flash.page'
import WriteFirmwareToDevice from '../../../pageobjects/write-firmware-to-device.page'

// eslint-disable-next-line no-undef
describe('WriteToDevicePage: write firmware official v22.03.0 to m5stickv', () => {
 
  // eslint-disable-next-line no-undef
  before(async () => {
    // select device
    await Main.page.waitForExist()
    await Main.selectDeviceButton.waitForExist()
    await Main.selectDeviceButton.click()
    await delay(1000)
    await SelectDevice.formArrow.click()
    await delay(1000)
    await SelectDevice.list_item_m5stickv.waitForExist() 
    await delay(1000)
    await SelectDevice.list_item_m5stickv.click()
    await delay(1000)
    await SelectDevice.formSelected.waitUntil(async function() {
      return (await this.getText()) !== ''
    })
    await SelectDevice.formSelectButton.click()
    await SelectDevice.page.waitForExist({ reverse: true })
  
    // select version
    await Main.page.waitForExist()
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
    await delay(1000) 
    await SelectVersion.list_item_22_03_0.click()
    await SelectVersion.formSelectButton.waitForExist()
    await SelectVersion.formSelectButton.click()  
    await SelectVersion.page.waitForExist({ reverse: true }) 
    
    // Check resource release
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
    
    // Check resource sha256
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
    
    // Check resource Sig
    await CheckResourcesOfficialReleaseSig.page.waitForExist()
    await CheckResourcesOfficialReleaseSig.cardTitleChecking.waitForExist()
    await CheckResourcesOfficialReleaseSig.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesOfficialReleaseSig.cardTitleChecked.waitForExist()
    await CheckResourcesOfficialReleaseSig.cardSubtitleChecked.waitForExist()
    await CheckResourcesOfficialReleaseSig.cardContentChecked.waitForExist()
    await CheckResourcesOfficialReleaseSig.buttonProceed.waitForExist()
    await CheckResourcesOfficialReleaseSig.buttonProceed.click()
    await CheckResourcesOfficialReleaseSig.page.waitForExist({ reverse: true }) 
    
    // Check resource pem
    await CheckResourcesOfficialReleasePem.page.waitForExist() 
    await CheckResourcesOfficialReleasePem.cardTitleChecking.waitForExist()
    await CheckResourcesOfficialReleasePem.cardTitleChecking.waitForExist({ reverse: true })
    await CheckResourcesOfficialReleasePem.cardTitleChecked.waitForExist()
    await CheckResourcesOfficialReleasePem.cardSubtitleChecked.waitForExist()
    await CheckResourcesOfficialReleasePem.cardContentChecked.waitForExist() 
    await CheckResourcesOfficialReleasePem.buttonProceed.waitForExist()
    await CheckResourcesOfficialReleasePem.buttonDownload.waitForExist()
    await CheckResourcesOfficialReleasePem.buttonProceed.click()
    
    // verify
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
    
    // unzip
    await UnzipOfficialRelease.page.waitForExist()   
    await UnzipOfficialRelease.cardTitleUnzipping.waitForExist()  
    await UnzipOfficialRelease.cardSubtitleUnzipping.waitForExist()  
    await UnzipOfficialRelease.cardProgressLinearTextUnzipping.waitForExist()
    await UnzipOfficialRelease.buttonDone.waitForExist()
    await UnzipOfficialRelease.buttonBack.waitForExist()
    await UnzipOfficialRelease.buttonDone.click()
    await delay(1000)
    await UnzipOfficialRelease.page.waitForExist({ reverse: true })

    // flash
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
  it('should show subtitle \'version: selfcustody/krux/releases/tag/v22.03.0\'', async () => {   
    await expectWDIO(BeforeFlash.cardSubtitleVersion).toHaveText('version: selfcustody/krux/releases/tag/v22.03.0')
  })
  
  // eslint-disable-next-line no-undef
  it('should show subtitle \'device: maixpy_m5stickv\'', async () => {   
    await expectWDIO(BeforeFlash.cardSubtitleDevice).toHaveText('device: maixpy_m5stickv')
  })

  // eslint-disable-next-line no-undef
  describe('Flashing', () => {
    
    // eslint-disable-next-line no-undef
    before(async () => {
      BeforeFlash.flashButton.waitForExist()
      BeforeFlash.flashButton.click()
      BeforeFlash.page.waitForExist({ reverse: true })
      WriteFirmwareToDevice.page.waitForExist()
      WriteFirmwareToDevice.cardTitle.waitForExist()
      WriteFirmwareToDevice.cardSubtitle.waitForExist()
      WriteFirmwareToDevice.console.waitForExist()
    })


    // eslint-disable-next-line no-undef
    it('should show title \'Flashing...\'', async () => {   
      await expectWDIO(WriteFirmwareToDevice.cardTitle).toHaveText('Flashing...')
    })

    // eslint-disable-next-line no-undef
    it('should show subtitle \'Do not unplug device or shutdown computer!\'', async () => {   
      await expectWDIO(WriteFirmwareToDevice.cardSubtitle).toHaveText('Do not unplug device or shutdown computer!')
    })
  })
})
