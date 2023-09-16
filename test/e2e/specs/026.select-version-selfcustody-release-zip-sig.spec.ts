const expectChai = require('chai').expect
const expectWDIO = require('@wdio/globals').expect
const { join } = require('path')
const { homedir } = require('os')
const { osLangSync } = require('os-lang')
const { describe, it } = require('mocha')

const App = require('../pageobjects/app.page')

describe('KruxInstaller SelectVersion page (download release signature)', () => {

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
  })

  it ('should \'checking v23.09.0/krux-v23.09.0.zip.sig\' message appears', async () => {
    await instance.checkingReleaseZipSigMsg.waitForExist()
    await expectWDIO(instance.checkingReleaseZipSigMsg).toBeDisplayed()
  })

  it ('should \'v23.09.0/krux-v23.09.0.zip.sig not found\' message appears', async () => {
    await instance.notFoundReleaseZipSigMsg.waitForExist()
    await expectWDIO(instance.notFoundReleaseZipSigMsg).toBeDisplayed()
  })

  it('should go to DownloadOfficialReleaseZipSig page', async () => {
    await instance.downloadOfficialReleaseZipSigPage.waitForExist()
    await expectWDIO(instance.downloadOfficialReleaseZipSigPage).toBeDisplayed()
  })

  it('should DownloadOfficialReleaseZipSig page have \'Downloading\' title', async () => {
    await instance.downloadOfficialReleaseZipSigTitle.waitForExist()
    await expectWDIO(instance.downloadOfficialReleaseZipSigTitle).toBeDisplayed()
    await expectWDIO(instance.downloadOfficialReleaseZipSigTitle).toHaveText('Downloading')
  })

  it('should DownloadOfficialReleaseZipSig page have \'https://github.com/selfcustody/krux/releases/download/v23.09.0/krux-v23.09.0.zip.sig\' subtitle', async () => {
    await instance.downloadOfficialReleaseZipSigSubtitle.waitForExist()
    await expectWDIO(instance.downloadOfficialReleaseZipSigSubtitle).toBeDisplayed()
    await expectWDIO(instance.downloadOfficialReleaseZipSigSubtitle).toHaveText('https://github.com/selfcustody/krux/releases/download/v23.09.0/krux-v23.09.0.zip.sig')
  })

  it('should DownloadOfficialReleaseZipSig page progress until 100%', async () => {
    await instance.downloadOfficialReleaseZipSigProgress.waitForExist()
    await expectWDIO(instance.downloadOfficialReleaseZipSigProgress).toBeDisplayed()
    await instance.downloadOfficialReleaseZipSigProgress.waitUntil(async function () {
      const percentText = await this.getText()
      const percent = parseFloat(percentText.split('%')[0])
      return percent === 100.00
    }, {
      timeout: 60000,
      interval: 50
    })
  })
  
})
