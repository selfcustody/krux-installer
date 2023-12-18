import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

describe('KruxInstaller SelectVersion page (already downloaded release sha256.txt - click download again button)', () => {

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
    await instance.warningDownloadAgainButton.waitForExist()
    await instance.warningDownloadAgainButtonText.waitForExist()
  })

  it ('should click \'Download again\' go out of WarningDownload page', async () => {
    await instance.warningDownloadAgainButton.click()
    await instance.warningDownloadPage.waitForExist({ reverse: true })
    await expect(instance.warningDownloadPage).not.toBeDisplayed()
  })

  it ('should be in DownloadOfficialReleaseZipSha256 page', async () => {
    await instance.downloadOfficialReleaseZipSha256txtPage.waitForExist()
    await expect(instance.downloadOfficialReleaseZipSha256txtPage).toBeDisplayed()
  })

  it('should DownloadOfficialReleaseZipSha256 page have \'Downloading\' title', async () => {
    await instance.downloadOfficialReleaseZipSha256txtPageTitle.waitForExist()
    await expect(instance.downloadOfficialReleaseZipSha256txtPageTitle).toBeDisplayed()
    await expect(instance.downloadOfficialReleaseZipSha256txtPageTitle).toHaveText('Downloading')
  })

  it('should DownloadOfficialReleaseZipSha256 page have \'https://github.com/selfcustody/krux/releases/download/v23.09.1/krux-v23.09.1.zip.sha256.txt\' subtitle', async () => {
    await instance.downloadOfficialReleaseZipSha256txtPageSubtitle.waitForExist()
    await expect(instance.downloadOfficialReleaseZipSha256txtPageSubtitle).toBeDisplayed()
    await expect(instance.downloadOfficialReleaseZipSha256txtPageSubtitle).toHaveText('https://github.com/selfcustody/krux/releases/download/v23.09.1/krux-v23.09.1.zip.sha256.txt')
  })

  it('should DownloadOfficialReleaseZipSha256 page progress until 100%', async () => {
    await instance.downloadOfficialReleaseZipSha256txtPageProgress.waitForExist()
    await expect(instance.downloadOfficialReleaseZipSha256txtPageProgress).toBeDisplayed()
    await instance.downloadOfficialReleaseZipSha256txtPageProgress.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent === 100.00
    }, {
      timeout: 600000,
      interval: 50
    })
  })
  
})
