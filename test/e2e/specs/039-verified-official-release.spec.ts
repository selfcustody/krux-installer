const expectWDIO = require('@wdio/globals').expect
const { join } = require('path')
const { homedir } = require('os')
const { osLangSync } = require('os-lang')
const { describe, it } = require('mocha')

const App = require('../pageobjects/app.page')

describe('KruxInstaller VerifiedOfficialRelease page (show and click back button)', () => {

  let instance: any;

  before(async function () {
    instance = new App()
    await instance.app.waitForExist()
    await instance.main.waitForExist()
    await instance.logo.waitForExist()
    await instance.logo.waitForExist({ reverse: true })
    await instance.loadingDataMsg.waitForExist()
    await instance.verifyingOpensslMsg.waitForExist()
    if (process.platform === 'linux') {
      await instance.opensslForLinuxFound.waitForExist()
    } else if (process.platform === 'darwin') {
      await instance.opensslForDarwinFound.waitForExist()
    } else if (process.platform === 'win32') {
      await instance.opensslForWin32Found.waitForExist()
    }
    await instance.loadingDataMsg.waitForExist({ reverse: true })
    await instance.verifyingOpensslMsg.waitForExist({ reverse: true })
    await instance.opensslForLinuxFound.waitForExist({ reverse: true })
    await instance.mainPage.waitForExist()
    await instance.mainSelectDeviceButton.waitForExist()
    await instance.mainSelectVersionButton.waitForExist()
    await instance.mainSelectVersionButton.click()
    await instance.mainPage.waitForExist({ reverse: true })
    await instance.githubOctocatCheckerLogo.waitForExist({ timeout: 3000 })
    await instance.selectVersionPage.waitForExist()
    await instance.selectVersionSelfcustodyButton.waitForExist()
    await instance.selectVersionSelfcustodyText.waitForExist()
    await instance.selectVersionOdudexButton.waitForExist()
    await instance.selectVersionOdudexText.waitForExist()
    await instance.selectVersionSelfcustodyButton.click()
    await instance.selectVersionPage.waitForExist({ reverse: true })
    await instance.checkingReleaseZipMsg.waitForExist()
    await instance.foundReleaseZipMsg.waitForExist()
    await instance.warningDownloadPage.waitForExist()
    await instance.warningAlreadyDownloadedText.waitForExist() 
    await instance.warningDownloadProceedButton.waitForExist()
    await instance.warningDownloadProceedButtonText.waitForExist()
    await instance.warningDownloadAgainButton.waitForExist()
    await instance.warningDownloadAgainButtonText.waitForExist()
    await instance.warningDownloadShowDetailsButton.waitForExist()
    await instance.warningDownloadShowDetailsButtonText.waitForExist()
    await instance.warningDownloadBackButton.waitForExist()
    await instance.warningDownloadBackButtonText.waitForExist()
    await instance.warningDownloadProceedButton.click()
    await instance.warningDownloadPage.waitForExist({ reverse: true })
    await instance.checkingReleaseZipSha256txtMsg.waitForExist()
    await instance.foundReleaseZipSha256txtMsg.waitForExist()
    await instance.warningDownloadPage.waitForExist()
    await instance.warningDownloadProceedButton.waitForExist()
    await instance.warningDownloadProceedButtonText.waitForExist()
    await instance.warningDownloadProceedButton.click()
    await instance.warningDownloadPage.waitForExist({ reverse: true })
    await instance.checkingReleaseZipSigMsg.waitForExist()
    await instance.foundReleaseZipSigMsg.waitForExist()
    await instance.warningDownloadPage.waitForExist()
    await instance.warningDownloadProceedButton.waitForExist()
    await instance.warningDownloadProceedButtonText.waitForExist()
    await instance.warningDownloadProceedButton.click()
    await instance.warningDownloadPage.waitForExist({ reverse: true })
    await instance.checkingReleasePemMsg.waitForExist()
    await instance.foundReleasePemMsg.waitForExist()
    await instance.warningDownloadPage.waitForExist()
    await instance.warningDownloadProceedButton.waitForExist()
    await instance.warningDownloadProceedButtonText.waitForExist()
    await instance.warningDownloadProceedButton.click()
    await instance.warningDownloadPage.waitForExist({ reverse: true })
    await instance.checkVerifyOfficialReleasePage.waitForExist({ timeout: 3000 })
    await instance.checkVerifyOfficialReleaseLenSassamanIsUsingOpenssl.waitForExist()
    await instance.checkVerifyOfficialReleaseLenSassamanIsUsingOpenssl.waitForExist({ reverse: true })
    await instance.checkVerifyOfficialReleasePage.waitForExist({ reverse: true })
  })

  it('should show VerifiedOfficialRelease page', async () => {
    await instance.verifiedOfficialReleasePage.waitForExist()
    await expectWDIO(instance.verifiedOfficialReleasePage).toBeDisplayed()
  })

  it('should show sha256sum intergrity title', async () => {
    await instance.verifiedOfficialReleasePageSha2256IntegrityTitle.waitForExist()
    await expectWDIO(instance.verifiedOfficialReleasePageSha2256IntegrityTitle).toBeDisplayed()     
    await expectWDIO(instance.verifiedOfficialReleasePageSha2256IntegrityTitle).toHaveText('Sha256sum integrity')
  })

  it('should show sha256sum intergrity sha256.txt', async () => {
    await instance.verifiedOfficialReleasePageSha2256IntegritySha256txt.waitForExist()
    await expectWDIO(instance.verifiedOfficialReleasePageSha2256IntegritySha256txt).toBeDisplayed()
    await expectWDIO(instance.verifiedOfficialReleasePageSha2256IntegritySha256txt).toHaveText('Expected result from file v23.09.0/krux-v23.09.0.zip.sha256.txt\n4a 8a a4 0b 71 f7 df 35 5b d1 54 ff ac 9c 9f 10 99 e8 7a 89 c0 53 32 58 7e bc 02 a2 15 92 ec 1b')
  })

  it('should show sha256sum intergrity sha256 summed result', async () => {
    await instance.verifiedOfficialReleasePageSha2256IntegritySha256.waitForExist()
    await expectWDIO(instance.verifiedOfficialReleasePageSha2256IntegritySha256).toBeDisplayed()
    await expectWDIO(instance.verifiedOfficialReleasePageSha2256IntegritySha256).toHaveText('Summed result of file v23.09.0/krux-v23.09.0.zip\n4a 8a a4 0b 71 f7 df 35 5b d1 54 ff ac 9c 9f 10 99 e8 7a 89 c0 53 32 58 7e bc 02 a2 15 92 ec 1b')
  })
  
  it('should show openssl authenticity title', async () => {
    await instance.verifiedOfficialReleasePageSignatureTitle.waitForExist()
    await expectWDIO(instance.verifiedOfficialReleasePageSignatureTitle).toBeDisplayed()     
    await expectWDIO(instance.verifiedOfficialReleasePageSignatureTitle).toHaveText('Signature authenticity')
  })

  it('should show openssl authenticity command', async () => {
    await instance.verifiedOfficialReleasePageSignatureCommand.waitForExist()
    await expectWDIO(instance.verifiedOfficialReleasePageSignatureCommand).toBeDisplayed()
    
    let resources = ''
    let openssl = ''
    if (process.env.CI && process.env.GITHUB_ACTION) {
      if (process.platform  === 'linux') {
        resources = '/home/runner/krux-installer'
        openssl = 'openssl'
      } else if (process.platform  === 'win32') {
        resources = 'C:\\Users\\runneradmin\\Documents\\krux-installer'
        openssl = 'openssl.exe'
      } else if (process.platform  === 'darwin') {
        resources = '/Users/runner/Documents/krux-installer'
        openssl = 'openssl'
      }
    } else {
      const lang = osLangSync()
      const home = homedir()
      if (process.platform  === 'linux' || process.platform === 'darwin') {
        openssl = 'openssl'
      } else if (process.platform  === 'win32') {
        openssl = 'openssl.exe'
      }
      if ( lang.match(/en-*/g)) {
        resources = join(home, 'Documents', 'krux-installer')
      } else if ( lang.match(/pt-*/g)) {
        resources = join(home, 'Documentos', 'krux-installer')
      } else {
        throw new Error(`${lang} not implemented. Please implement it with correct \'Documents\' folder name`)
      }
    }

    const resourceZip = join(resources, 'v23.09.0', 'krux-v23.09.0.zip')
    const resourcePem = join(resources, 'main', 'selfcustody.pem')
    const resourceSig = join(resources, 'v23.09.0', 'krux-v23.09.0.zip.sig')
    const command = [
      '$>',
      `${openssl} sha256 <${resourceZip}`,
      '-binary',
      '|',
      openssl,
      'pkeyutl',
      '-verify',
      '-pubin',
      '-inkey',
      resourcePem,
      '-sigfile',
      resourceSig
    ].join(' ')

    await expectWDIO(instance.verifiedOfficialReleasePageSignatureCommand).toHaveText(command)
  })

  it('should show openssl authenticity command result', async () => {
    await instance.verifiedOfficialReleasePageSignatureResult.waitForExist()
    await expectWDIO(instance.verifiedOfficialReleasePageSignatureResult).toBeDisplayed()     
    await expectWDIO(instance.verifiedOfficialReleasePageSignatureResult).toHaveText('Signature Verified Successfully')
  })

  it('should show back button', async () => {
    await instance.verifiedOfficialReleasePageBackButton.waitForExist()
    await expectWDIO(instance.verifiedOfficialReleasePageBackButton).toBeDisplayed()     
    await expectWDIO(instance.verifiedOfficialReleasePageBackButton).toHaveText('Back')
  })

  it('should click back button, exit from VerifiedOfficialRelease page', async () => {
    await instance.verifiedOfficialReleasePageBackButton.click()
    await instance.verifiedOfficialReleasePage.waitForExist({ reverse: true })
  })

  it('should be in Main page', async () => {
    await instance.verifiedOfficialReleasePageBackButton.click()
    await instance.mainPage.waitForExist()
    await expectWDIO(instance.mainPage).toBeDisplayed()
  })

})