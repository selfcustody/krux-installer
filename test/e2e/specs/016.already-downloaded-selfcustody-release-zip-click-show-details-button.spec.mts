import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { join } from 'path'
import { homedir } from 'os'
import { osLangSync } from 'os-lang'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

describe('KruxInstaller SelectVersion page (already downloaded release - click show details button)', () => {

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

  it ('should overlay not be shown', async () => {
    await expect(instance.warningAlreadyDownloadedOverlay).not.toBeDisplayed()
  })

  it ('should click \'Show details\' button and overlay must be visible', async () => {
    await instance.warningDownloadShowDetailsButton.click()
    await instance.warningAlreadyDownloadedOverlay.waitForExist()
    await expect(instance.warningAlreadyDownloadedOverlay).toBeDisplayed()
  })

  it ('should overlay title be \'Resource details\'', async () => {
    await instance.warningAlreadyDownloadedOverlayTitle.waitForExist()
    await expect(instance.warningAlreadyDownloadedOverlayTitle).toBeDisplayed()
    await expect(instance.warningAlreadyDownloadedOverlayTitle).toHaveText('Resource details')
  })

  it ('should overlay subtitle be \'v24.03.0/krux-v24.03.0.zip\'', async () => {
    await instance.warningAlreadyDownloadedOverlayTitle.waitForExist()
    await expect(instance.warningAlreadyDownloadedOverlaySubtitle).toBeDisplayed()
    await expect(instance.warningAlreadyDownloadedOverlaySubtitle).toHaveText('v24.03.0/krux-v24.03.0.zip')
  })

  it ('should a overlay text have \'Remote: https://github.com/selfcustody/krux/releases/download/v24.03.0/krux-v24.03.0.zip\'', async () => {
    await instance.warningAlreadyDownloadedOverlayTextRemote.waitForExist()
    await expect(instance.warningAlreadyDownloadedOverlayTextRemote).toBeDisplayed()
    await expect(instance.warningAlreadyDownloadedOverlayTextRemote).toHaveText('Remote:\nhttps://github.com/selfcustody/krux/releases/download/v24.03.0/krux-v24.03.0.zip')
  })

  it ('should a overlay text have properly local resource', async () => {
    await instance.warningAlreadyDownloadedOverlayTextLocal.waitForExist()
    await expect(instance.warningAlreadyDownloadedOverlayTextLocal).toBeDisplayed()
    
    let resources = ''
    if (process.env.CI && process.env.GITHUB_ACTION) {
      if (process.platform  === 'linux') {
        resources = '/home/runner/krux-installer'
      } else if (process.platform  === 'win32') {
        resources = 'C:\\Users\\runneradmin\\Documents\\krux-installer'
      } else if (process.platform  === 'darwin') {
        resources = '/Users/runner/Documents/krux-installer'
      }
    } else {
      const lang = osLangSync()
      const home = homedir()
      if ( lang.match(/en-*/g)) {
        resources = join(home, 'Documents', 'krux-installer')
      } else if ( lang.match(/pt-*/g)) {
        resources = join(home, 'Documentos', 'krux-installer')
      } else {
        throw new Error(`${lang} not implemented. Please implement it with correct \'Documents\' folder name`)
      }
    }

    const resource = join(resources, 'v24.03.0', 'krux-v24.03.0.zip')
    await expect(instance.warningAlreadyDownloadedOverlayTextLocal).toHaveText(`Local:\n${resource}`)
  })

  it('should a overlay text have the properly description', async () => {
    await instance.warningAlreadyDownloadedOverlayTextWhatdo.waitForExist()
    await expect(instance.warningAlreadyDownloadedOverlayTextWhatdo).toBeDisplayed()
    await expect(instance.warningAlreadyDownloadedOverlayTextWhatdo).toHaveText('Description:\nThis file is the official release with all necessary contents to flash or update krux firmware on your Kendryte K210 device, including the firmware signature that prove the firmware\'s authenticity')
  })

  it('should \'close\' have \'Close\' text',async () => {
    await instance.warningAlreadyDownloadedOverlayButtonClose.waitForExist()
    await expect(instance.warningAlreadyDownloadedOverlayButtonClose).toBeDisplayed()
    await expect(instance.warningAlreadyDownloadedOverlayButtonClose).toHaveText('Close')
  })

  it('should \'close\' button make overlay not visible', async () => {
    await instance.warningAlreadyDownloadedOverlayButtonClose.click()
    await instance.warningAlreadyDownloadedOverlay.waitForExist({ reverse: true })
    await expect(instance.warningAlreadyDownloadedOverlay).not.toBeDisplayed()
  })
  
})
