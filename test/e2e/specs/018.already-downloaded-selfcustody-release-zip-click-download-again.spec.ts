const expectWDIO = require('@wdio/globals').expect
const { join } = require('path')
const { homedir } = require('os')
const { osLangSync } = require('os-lang')
const { describe, it } = require('mocha')

const App = require('../pageobjects/app.page')

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
    await expectWDIO(instance.warningDownloadPage).not.toBeDisplayed()
  })

  it ('should be in DownloadOfficialRelease page', async () => {
    await instance.downloadOfficialReleaseZipPage.waitForExist()
    await expectWDIO(instance.downloadOfficialReleaseZipPage).toBeDisplayed()
  })

  it('should DownloadOfficialReleaseZip page have \'Downloading\' title', async () => {
    await instance.downloadOfficialReleaseZipTitle.waitForExist()
    await expectWDIO(instance.downloadOfficialReleaseZipTitle).toBeDisplayed()
    await expectWDIO(instance.downloadOfficialReleaseZipTitle).toHaveText('Downloading')
  })

  it('should DownloadOfficialReleaseZip page have \'https://github.com/selfcustody/krux/releases/download/v22.08.2/krux-v22.08.2.zip\' subtitle', async () => {
    await instance.downloadOfficialReleaseZipTitle.waitForExist()
    await expectWDIO(instance.downloadOfficialReleaseZipSubtitle).toBeDisplayed()
    await expectWDIO(instance.downloadOfficialReleaseZipSubtitle).toHaveText('https://github.com/selfcustody/krux/releases/download/v22.08.2/krux-v22.08.2.zip')
  })

  it('should DownloadOfficialReleaseZip page progress until 100%', async () => {
    await instance.downloadOfficialReleaseZipProgress.waitForExist()
    await expectWDIO(instance.downloadOfficialReleaseZipProgress).toBeDisplayed()
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