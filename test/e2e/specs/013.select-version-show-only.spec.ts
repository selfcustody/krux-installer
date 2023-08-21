const expectChai = require('chai').expect
const expectWDIO = require('@wdio/globals').expect
const { describe, it } = require('mocha')

const App = require('../pageobjects/app.page')

const GITHUB_OCTOCAT = [ 
    "MMM.           .MMM        ",
    "       MMMMMMMMMMMMMMMMMMM        ",
    "       MMMMMMMMMMMMMMMMMMM        ",  
    "      MMMMMMMMMMMMMMMMMMMMM       ",
    "     MMMMMMMMMMMMMMMMMMMMMMM      ",
    "    MMMMMMMMMMMMMMMMMMMMMMMMM     ",
    "    MMMM::- -:::::::- -::MMMM     ",
    "     MM~:~ 00~:::::~ 00~:~MM      ",
    ".. MMMMM::.00:::+:::.00::MMMMM .. ",
    "      .MM::::: ._. :::::MM.       ",
    "         MMMM;:::::;MMMM          ",
    "  -MM        MMMMMMM              ",
    "  ^  M+     MMMMMMMMM             ",
    "      MMMMMMM MM MM MM            ",
    "           MM MM MM MM            ",
    "           MM MM MM MM            ",
    "        .~~MM~MM~MM~MM~~.         ",
    "     ~~~~MM:~MM~~~MM~:MM~~~~      ",
    "    ~~~~~~==~==~~~==~==~~~~~~     ",
    "     ~~~~~~==~==~==~==~~~~~~      ",
    "         :~==~==~==~==~~          ",
    " Checking latest release on github"
  ].join('\n')

describe('KruxInstaller SelectVersion page (show only)', () => {

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
  })

  it('should click on \'Select version\' button and page change', async () => {
    await instance.mainSelectVersionButton.click()
    await instance.mainPage.waitForExist({ reverse: true })
  })

  it('should github\'s ocotcat checker appears', async () => { 
    await instance.githubOctocatCheckerLogo.waitForExist({ timeout: 3000 })
    await expectWDIO(instance.githubOctocatCheckerLogo).toBeDisplayed()
    await expectWDIO(instance.githubOctocatCheckerLogo).toHaveText(GITHUB_OCTOCAT)
  })

  it('should \'Select version\' page appear', async () => {
    await instance.selectVersionPage.waitForExist()
    await expectWDIO(instance.selectVersionPage).toBeDisplayed()
  })
  
  it('should \'selfcustody/krux/releases/tag/v22.08.2\' button appear', async () => {
    await instance.selectVersionSelfcustodyButton.waitForExist()
    await expectWDIO(instance.selectVersionSelfcustodyButton).toBeDisplayed()
  })

  it('should \'selfcustody/krux/releases/tag/v22.08.2\' button have \'selfcustody/krux/releases/tag/v22.08.2\' text', async () => {
    await instance.selectVersionSelfcustodyText.waitForExist()
    await expectWDIO(instance.selectVersionSelfcustodyText).toHaveText('selfcustody/krux/releases/tag/v22.08.2')
  })

  it('should \'odudex/krux_binaries\' button appear', async () => {
    await instance.selectVersionOdudexButton.waitForExist()
    await expectWDIO(instance.selectVersionOdudexButton).toBeDisplayed()
  })

  it('should \'selfcustody/krux/releases/tag/v22.08.2\' button have \'selfcustody/krux/releases/tag/v22.08.2\' text', async () => {
    await instance.selectVersionOdudexText.waitForExist()
    await expectWDIO(instance.selectVersionOdudexText).toHaveText('odudex/krux_binaries')
  })
})
