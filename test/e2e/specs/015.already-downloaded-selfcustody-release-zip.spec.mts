import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

describe('KruxInstaller SelectVersion page (already downloaded release - show only)', () => {

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
  })

  it('should \'v23.09.1/krux-v23.09.1.zip found\' message appears', async () => {
    await instance.foundReleaseZipMsg.waitForExist()
    await expect(instance.foundReleaseZipMsg).toBeDisplayed()
    if (process.platform === 'linux' || process.platform === 'darwin') {
      await expect(instance.foundReleaseZipMsg).toHaveText('v23.09.1/krux-v23.09.1.zip found')
    } else if (process.platform === 'win32') {
      await expect(instance.foundReleaseZipMsg).toHaveText('v23.09.1\\krux-v23.09.1.zip found')
    }
  })

  it('should WarningDownload page should be displayed', async () => {
    await instance.warningDownloadPage.waitForExist()
    await expect(instance.warningDownloadPage).toBeDisplayed()
  }) 

  it('should \'v23.09.1/krux-v23.09.1.zip already downloaded\' message be displayed', async () => {
    await instance.warningAlreadyDownloadedText.waitForExist()
    await expect(instance.warningAlreadyDownloadedText).toBeDisplayed()
    if (process.platform === 'linux' || process.platform === 'darwin') {
      await expect(instance.warningAlreadyDownloadedText).toHaveText('v23.09.1/krux-v23.09.1.zip already downloaded')
    } else if (process.platform === 'win32') {
      await expect(instance.warningAlreadyDownloadedText).toHaveText('v23.09.1\\krux-v23.09.1.zip already downloaded')
    }
  })

  it('should \'Proceed with current file\' button be displayed', async () => {
    await instance.warningDownloadProceedButton.waitForExist()
    await instance.warningDownloadProceedButtonText.waitForExist()
    await expect(instance.warningDownloadProceedButton).toBeDisplayed()
    await expect(instance.warningDownloadProceedButtonText).toBeDisplayed()
    await expect(instance.warningDownloadProceedButtonText).toHaveText('Proceed with current file')
  })

  it('should \'Download it again\' button be displayed', async () => {
    await instance.warningDownloadAgainButton.waitForExist()
    await instance.warningDownloadAgainButtonText.waitForExist()
    await expect(instance.warningDownloadAgainButton).toBeDisplayed()
    await expect(instance.warningDownloadAgainButtonText).toBeDisplayed()
    await expect(instance.warningDownloadAgainButtonText).toHaveText('Download it again')
  })

  it('should \'Show details\' button be displayed', async () => {
    await instance.warningDownloadShowDetailsButton.waitForExist()
    await instance.warningDownloadShowDetailsButtonText.waitForExist()
    await expect(instance.warningDownloadShowDetailsButton).toBeDisplayed()
    await expect(instance.warningDownloadShowDetailsButtonText).toBeDisplayed()
    await expect(instance.warningDownloadShowDetailsButtonText).toHaveText('Show details')
  })

  it('should \'Back\' button be displayed', async () => {
    await instance.warningDownloadBackButton.waitForExist()
    await instance.warningDownloadBackButtonText.waitForExist()
    await expect(instance.warningDownloadBackButton).toBeDisplayed()
    await expect(instance.warningDownloadBackButtonText).toBeDisplayed()
    await expect(instance.warningDownloadBackButtonText).toHaveText('Back')
  })

})
