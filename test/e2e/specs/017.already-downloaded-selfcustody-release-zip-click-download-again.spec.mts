import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

describe('KruxInstaller SelectVersion page (already downloaded release - click download again button)', () => {

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
  })

  it ('should click \'Download again\' go out of WarningDownload page', async () => {
    await instance.warningDownloadAgainButton.click()
    await instance.warningDownloadPage.waitForExist({ reverse: true })
    await expect(instance.warningDownloadPage).not.toBeDisplayed()
  })

  it ('should be in DownloadOfficialRelease page', async () => {
    await instance.downloadOfficialReleaseZipPage.waitForExist()
    await expect(instance.downloadOfficialReleaseZipPage).toBeDisplayed()
  })

  it('should DownloadOfficialReleaseZip page have \'Downloading\' title', async () => {
    await instance.downloadOfficialReleaseZipTitle.waitForExist()
    await expect(instance.downloadOfficialReleaseZipTitle).toBeDisplayed()
    await expect(instance.downloadOfficialReleaseZipTitle).toHaveText('Downloading')
  })

  it('should DownloadOfficialReleaseZip page have \'https://github.com/selfcustody/krux/releases/download/v24.03.0/krux-v24.03.0.zip\' subtitle', async () => {
    await instance.downloadOfficialReleaseZipTitle.waitForExist()
    await expect(instance.downloadOfficialReleaseZipSubtitle).toBeDisplayed()
    await expect(instance.downloadOfficialReleaseZipSubtitle).toHaveText('https://github.com/selfcustody/krux/releases/download/v24.03.0/krux-v24.03.0.zip')
  })

  it('should DownloadOfficialReleaseZip page progress until 100%', async () => {
    await instance.downloadOfficialReleaseZipProgress.waitForExist()
    await expect(instance.downloadOfficialReleaseZipProgress).toBeDisplayed()
    await instance.downloadOfficialReleaseZipProgress.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent === 100.00
    }, {
      timeout: 600000,
      interval: 50
    })
  })

})
