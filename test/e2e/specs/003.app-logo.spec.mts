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

  it('should #app html exist', async () => { 
    await instance.app.waitForExist({ timeout: 5000 })
  })

  it('should main tag exist', async () => { 
    await instance.main.waitForExist({ timeout: 5000 })
  })

  it('should krux-installer logo appears', async () => { 
    await instance.logo.waitForExist({ timeout: 3000 })
    await expect(instance.logo).toBeDisplayed()
    await expect(instance.logo).toHaveText(KRUX_INSTALLER_LOGO)
  })

  it('should krux-installer logo disappears', async () => { 
    await instance.logo.waitForExist({ timeout: 3000, reverse: true })
  })
})
