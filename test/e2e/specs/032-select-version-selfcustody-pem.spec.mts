import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

describe('KruxInstaller SelectVersion page (download public key certificate)', () => {

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
  })
   
  it ('should \'checking selfcustody.pem\' message appears', async () => {
    await instance.checkingReleasePemMsg.waitForExist()
    await expect(instance.checkingReleasePemMsg).toBeDisplayed()
  })

  it ('should \'main/selfcustody.pem not found\' message appears', async () => {
    await instance.notFoundReleasePemMsg.waitForExist()
    await expect(instance.notFoundReleasePemMsg).toBeDisplayed()
  })

  it('should go to DownloadOfficialReleasePem page', async () => {
    await instance.downloadOfficialReleasePemPage.waitForExist()
    await expect(instance.downloadOfficialReleasePemPage).toBeDisplayed()
  })

  it('should DownloadOfficialReleasePem page have \'Downloading\' title', async () => {
    await instance.downloadOfficialReleasePemTitle.waitForExist()
    await expect(instance.downloadOfficialReleasePemTitle).toBeDisplayed()
    await expect(instance.downloadOfficialReleasePemTitle).toHaveText('Downloading')
  })

  it('should DownloadOfficialReleasePem page have \'https://raw.githubusercontent.com/selfcustody/krux/main/selfcustody.pem\' subtitle', async () => {
    await instance.downloadOfficialReleasePemSubtitle.waitForExist()
    await expect(instance.downloadOfficialReleasePemSubtitle).toBeDisplayed()
    await expect(instance.downloadOfficialReleasePemSubtitle).toHaveText('https://raw.githubusercontent.com/selfcustody/krux/main/selfcustody.pem')
  })

  it('should DownloadOfficialReleasePem page progress until 100%', async () => {
    await instance.downloadOfficialReleasePemProgress.waitForExist()
    await expect(instance.downloadOfficialReleasePemProgress).toBeDisplayed()
    // TODO: Pem is so small that wdio cannot check progress 
    /*await instance.downloadOfficialReleasePemProgress.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent === 100.00
    }, {
      timeout: 60000,
      interval: 50
    })*/
  })

})
