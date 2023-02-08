import { expect as expectWDIO } from '@wdio/globals'
import delay from '../../delay'
import Main from '../../../pageobjects/main.page'
import SelectVersion from '../../../pageobjects/select-version.page'
import CheckResourcesOfficialRelease from '../../../pageobjects/check-resources-official-release.page'
import CheckResourcesOfficialReleaseSHA256 from '../../../pageobjects/check-resources-official-release-sha256.page'
import CheckResourcesOfficialReleaseSig from '../../../pageobjects/check-resources-official-release-sig.page'
import CheckResourcesOfficialReleasePem from '../../../pageobjects/check-resources-official-release-pem.page'
import VerifyOfficialRelease from '../../../pageobjects/verify-official-release.page'

// eslint-disable-next-line no-undef
describe('Verified \'v22.08.1/krux-v22.08.1.zip\' release sucessfully', () => {
  
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
    await SelectVersion.list_item_22_08_1.click()
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
  })

  // eslint-disable-next-line no-undef
  it('should card title be \'Verified\'', async () => {
    await expectWDIO(VerifyOfficialRelease.cardTitleChecked).toHaveText('Verified')
  })

  // eslint-disable-next-line no-undef
  it('should card have a subtitle with \'sha256sum results:\'', async () => {
    await expectWDIO(VerifyOfficialRelease.cardSubtitleSha256sumChecked).toHaveText('sha256sum results:')
  })

  // eslint-disable-next-line no-undef
  it('should card have a subtitle with \'Openssl signature check:\'', async () => {
    await expectWDIO(VerifyOfficialRelease.cardSubtitleSigChecked).toHaveText('Openssl signature check:')
  })

  // eslint-disable-next-line no-undef
  it('should card have a text \'Filename: v22.08.1/krux-v22.08.1.zip.sha256.txt\'', async () => {
    console.log(await VerifyOfficialRelease.cardContentFilenameTxt.getText())
    await expectWDIO(VerifyOfficialRelease.cardContentFilenameTxt).toHaveText('Filename: v22.08.1/krux-v22.08.1.zip.sha256.txt')
  })

  // eslint-disable-next-line no-undef
  it('should card have a text \'Filename: v22.08.0/krux-v22.08.0.zip\'', async () => {
    await expectWDIO(VerifyOfficialRelease.cardContentFilenameSha256).toHaveText('Filename: v22.08.1/krux-v22.08.1.zip')
  })

  // eslint-disable-next-line no-undef
  it('should card have txt chip with correct hash', async () => {
    await expectWDIO(VerifyOfficialRelease.chipHashTxt).toHaveText('424e6975f24e29a6d8d7603221dd6cc461b5321da3583cbecfdf783f32f752b6')
  })

  // eslint-disable-next-line no-undef
  it('should card have sha256sum chip with correct hash', async () => {
    await expectWDIO(VerifyOfficialRelease.chipHashSha256).toHaveText('424e6975f24e29a6d8d7603221dd6cc461b5321da3583cbecfdf783f32f752b6')
  })

  // eslint-disable-next-line no-undef
  it('should card have a console with complete command used to verify', async () => {
    // eslint-disable-next-line no-undef
    const api = await browser.electronAPI()
    const docs = api.documents
    await expectWDIO(VerifyOfficialRelease.consoleSignatureCommand).toHaveText([
      '$>',
      'openssl',
      'sha256',
      `<${docs}/krux-installer/v22.08.1/krux-v22.08.1.zip`,
      '-binary',
      '|',
      'openssl',
      'pkeyutl',
      '-verify',
      '-pubin',
      '-inkey',
      `${docs}/krux-installer/main/selfcustody.pem`,
      '-sigfile',
      `${docs}/krux-installer/v22.08.1/krux-v22.08.1.zip.sig`
    ].join(' '))
  })

  // eslint-disable-next-line no-undef
  it('should card have a chip with \'Signature Verified Successfully\'', async () => {
    await expectWDIO(VerifyOfficialRelease.chipSignatureResult).toHaveText('Signature Verified Successfully')
  })

  // eslint-disable-next-line no-undef
  it('should card have the warning \'WARN: You need to UNZIP this release before flash\'', async () => {
    await expectWDIO(VerifyOfficialRelease.cardActionWarn).toHaveText('WARN: You need to UNZIP this release before flash')
  })

  // eslint-disable-next-line no-undef
  it('should card have a \'UNZIP\' button', async () => {
    await expectWDIO(VerifyOfficialRelease.cardActionButtonUnzip).toHaveText('UNZIP')
  })

  // eslint-disable-next-line no-undef
  it('should card have a \'BACK\' button', async () => {
    await expectWDIO(VerifyOfficialRelease.cardActionButtonBack).toHaveText('BACK')
  })
})
