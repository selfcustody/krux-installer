import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

describe('KruxInstaller SelectVersion page (download release)', () => {

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
  })

  it('should click on \'selfcustody/krux/tags/v23.09.1\' and go to ConsoleLoad page', async () => {
    await instance.selectVersionSelfcustodyButton.click()
    await instance.selectVersionPage.waitForExist({ reverse: true })
    await expect(instance.selectVersionPage).not.toBeDisplayed()
  })

  it('should \'Checking v23.09.1/krux-v23.09.1.zip\' message appears', async () => {
    await instance.checkingReleaseZipMsg.waitForExist()
    await expect(instance.checkingReleaseZipMsg).toBeDisplayed()
    await expect(instance.checkingReleaseZipMsg).toHaveText('Checking v23.09.1/krux-v23.09.1.zip')
  })

  it('should \'v23.09.1/krux-v23.09.1.zip not found\' message appears', async () => {
    await instance.notFoundReleaseZipMsg.waitForExist()
    await expect(instance.notFoundReleaseZipMsg).toBeDisplayed()
    if (process.platform === 'linux' || process.platform === 'darwin') {
      await expect(instance.notFoundReleaseZipMsg).toHaveText('v23.09.1/krux-v23.09.1.zip not found')
    } else if (process.platform === 'win32') {
      await expect(instance.notFoundReleaseZipMsg).toHaveText('v23.09.1\\krux-v23.09.1.zip not found')
    }
  })

  it('should go to DownloadOfficialReleaseZip page', async () => {
    await instance.downloadOfficialReleaseZipPage.waitForExist()
    await expect(instance.downloadOfficialReleaseZipPage).toBeDisplayed()
  })

  it('should DownloadOfficialReleaseZip page have \'Downloading\' title', async () => {
    await instance.downloadOfficialReleaseZipTitle.waitForExist()
    await expect(instance.downloadOfficialReleaseZipTitle).toBeDisplayed()
    await expect(instance.downloadOfficialReleaseZipTitle).toHaveText('Downloading')
  })

  it('should DownloadOfficialReleaseZip page have \'https://github.com/selfcustody/krux/releases/download/v23.09.1/krux-v23.09.1.zip\' subtitle', async () => {
    await instance.downloadOfficialReleaseZipTitle.waitForExist()
    await expect(instance.downloadOfficialReleaseZipSubtitle).toBeDisplayed()
    await expect(instance.downloadOfficialReleaseZipSubtitle).toHaveText('https://github.com/selfcustody/krux/releases/download/v23.09.1/krux-v23.09.1.zip')
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
