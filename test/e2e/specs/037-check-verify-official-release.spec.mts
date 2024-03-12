import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

const LEN_SASSAMAN = [
    ":.:'' ,,xiW,\"4x, ''           ",
    "         :  ,dWWWXXXXi,4WX,            ",
    "         ' dWWWXXX7\"     `X,           ",
    "         lWWWXX7   __   _ X            ",
    "         :WWWXX7 ,xXX7' \"^^X           ",
    "         lWWWX7, _.+,, _.+.,           ",
    "         :WWW7,. `^\"-\" ,^-'            ",
    "         WW\",X:        X,              ",
    "         \"7^^Xl.    _(_x7'             ",
    "         l ( :X:       __ _            ",
    "         `. \" XX  ,xxWWWWX7            ",
    "           )X- \"\" 4X\" .___.            ",
    "         ,W X     :Xi  _,,_            ",
    "         WW X      4XiyXWWXd           ",
    "         \"\" ,,      4XWWWWXX           ",
    "         , R7X,       \"^447^           ",
    "         R, \"4RXk,      _, ,           ",
    "         TWk  \"4RXXi,   X',x           ",
    "         lTWk,  \"4RRR7' 4 XH           ",
    "         :lWWWk,  ^\"     `4            ",
    "         ::TTXWWi,_  Xll :..           ",
    "                                       ",
    "   Len Sassaman is using openssl to    ",
    "   verify sha256sum and signature..." 
].join('\n')

describe('KruxInstaller CheckVerifyOfficialRelease page (show Lensassaman \'using\' openssl)', () => {

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
  })

  it('should go to CheckVerifyOfficialRelease page', async () => { 
    await instance.checkVerifyOfficialReleasePage.waitForExist({ timeout: 3000 })
    await expect(instance.checkVerifyOfficialReleasePage).toBeDisplayed()
  })

  it('should show correctly Len Sassaman \'verifying\' with openssl', async () => {
    await instance.checkVerifyOfficialReleaseLenSassamanIsUsingOpenssl.waitForExist()
    await expect(instance.checkVerifyOfficialReleaseLenSassamanIsUsingOpenssl).toHaveText(LEN_SASSAMAN)
  })

  it('should go out of CheckVerifyOfficialRelease page', async () => {
    await instance.checkVerifyOfficialReleaseLenSassamanIsUsingOpenssl.waitForExist({ reverse: true })
    await instance.checkVerifyOfficialReleasePage.waitForExist({ reverse: true })
  })
  
})