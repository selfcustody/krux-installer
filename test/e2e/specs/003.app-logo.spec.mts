import { expect } from '@wdio/globals'
import { describe, it } from 'mocha'
import { createRequire } from 'module'

const App = createRequire(import.meta.url)('../pageobjects/app.page')

// When wdio gets the generated
// <pre> html tag from vue-ascii-morph,
// its change the first and last string
const KRUX_INSTALLER_LOGO = [
    "██           ",
    "       ██           ",
    "       ██           ",
    "     ██████         ",
    "       ██           ",
    "       ██  ██       ",
    "       ██ ██        ",
    "       ████         ",
    "       ██ ██        ",
    "       ██  ██       ",
    "       ██   ██      ",
    "                    ",
    "   KRUX INSTALLER"
].join('\n')

describe('KruxInstaller initialization', () => {

  let instance: typeof App;

  before(function () {
    instance = new App()
  })

  it('\'#app\' html tag should exist', async () => { 
    await instance.app.waitForExist({ timeout: 5000 })
  })

  it('\'#main\' html tag should exist', async () => { 
    await instance.main.waitForExist({ timeout: 5000 })
  })

  it('krux-installer logo should appears', async () => { 
    await instance.logo.waitForExist({ timeout: 3000 })
    await expect(instance.logo).toBeDisplayed()
    await expect(instance.logo).toHaveText(KRUX_INSTALLER_LOGO)
  })

  it('krux-installer logo should disappear', async () => { 
    await instance.logo.waitForExist({ timeout: 3000, reverse: true })
  })
})
