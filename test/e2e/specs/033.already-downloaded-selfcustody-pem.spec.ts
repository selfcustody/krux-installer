const expectChai = require('chai').expect
const expectWDIO = require('@wdio/globals').expect
const { join } = require('path')
const { homedir } = require('os')
const { osLangSync } = require('os-lang')
const { describe, it } = require('mocha')

const App = require('../pageobjects/app.page')

describe('KruxInstaller SelectVersion page (already downloaded public key certificate - show only)', () => {

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
   
  it ('should \'main/selfcustody.pem found\' message appears', async () => {
    await instance.checkingReleasePemMsg.waitForExist()
    await expectWDIO(instance.checkingReleasePemMsg).toBeDisplayed()
    if (process.platform === 'linux' || process.platform === 'darwin') {
      await expectWDIO(instance.foundReleasePemMsg).toHaveText('main/selfcustody.pem found')
    } else if (process.platform === 'win32') {
      await expectWDIO(instance.foundReleasePemMsg).toHaveText('main/selfcustody.pem found')
    }
  })
  
  it('should WarningDownload page should be displayed', async () => {
    await instance.warningDownloadPage.waitForExist()
    await expectWDIO(instance.warningDownloadPage).toBeDisplayed()
  }) 

  it('should \'main/selfcustody.pem already downloaded\' message be displayed', async () => {
    await instance.warningAlreadyDownloadedText.waitForExist()
    await expectWDIO(instance.warningAlreadyDownloadedText).toBeDisplayed()
    if (process.platform === 'linux' || process.platform === 'darwin') {
      await expectWDIO(instance.warningAlreadyDownloadedText).toHaveText('main/selfcustody.pem already downloaded')
    } else if (process.platform === 'win32') {
      await expectWDIO(instance.warningAlreadyDownloadedText).toHaveText('main/selfcustody.pem already downloaded')
    }
  })

  it('should \'Proceed with current file\' button be displayed', async () => {
    await instance.warningDownloadProceedButton.waitForExist()
    await instance.warningDownloadProceedButtonText.waitForExist()
    await expectWDIO(instance.warningDownloadProceedButton).toBeDisplayed()
    await expectWDIO(instance.warningDownloadProceedButtonText).toBeDisplayed()
    await expectWDIO(instance.warningDownloadProceedButtonText).toHaveText('Proceed with current file')
  })
  
  it('should \'Download it again\' button be displayed', async () => {
    await instance.warningDownloadAgainButton.waitForExist()
    await instance.warningDownloadAgainButtonText.waitForExist()
    await expectWDIO(instance.warningDownloadAgainButton).toBeDisplayed()
    await expectWDIO(instance.warningDownloadAgainButtonText).toBeDisplayed()
    await expectWDIO(instance.warningDownloadAgainButtonText).toHaveText('Download it again')
  })
  
  it('should \'Show details\' button be displayed', async () => {
    await instance.warningDownloadShowDetailsButton.waitForExist()
    await instance.warningDownloadShowDetailsButtonText.waitForExist()
    await expectWDIO(instance.warningDownloadShowDetailsButton).toBeDisplayed()
    await expectWDIO(instance.warningDownloadShowDetailsButtonText).toBeDisplayed()
    await expectWDIO(instance.warningDownloadShowDetailsButtonText).toHaveText('Show details')
  })
  
  it('should \'Back\' button be displayed', async () => {
    await instance.warningDownloadBackButton.waitForExist()
    await instance.warningDownloadBackButtonText.waitForExist()
    await expectWDIO(instance.warningDownloadBackButton).toBeDisplayed()
    await expectWDIO(instance.warningDownloadBackButtonText).toBeDisplayed()
    await expectWDIO(instance.warningDownloadBackButtonText).toHaveText('Back')
  })
})
