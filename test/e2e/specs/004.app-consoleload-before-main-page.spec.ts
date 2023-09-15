const expectChai = require('chai').expect
const expectWDIO = require('@wdio/globals').expect
const { describe, it } = require('mocha')

const App = require('../pageobjects/app.page')

// When wdio gets the generated
// <pre> html tag from vue-ascii-morph,
// its change the first and last string
const LOADING_DATA_MESSAGE: string = 'Loading data from storage'
const VERIFYING_OPENSSL_MESSAGE: string = 'Verifying openssl'
const OPENSSL_FOUND_LINUX_MESSAGE: string = 'openssl for linux found'
const OPENSSL_FOUND_DARWIN_MESSAGE: string = 'openssl for darwin found'
const OPENSSL_FOUND_WIN32_MESSAGE: string = 'openssl for win32 found'

describe('KruxInstaller loading messages', () => {

  let instance: any;

  before(function () {
    instance = new App()
  })

  it('should \'Loading data from storage\' message appears', async () => {
    await instance.loadingDataMsg.waitForExist({ timeout: 3000 })
    await expectWDIO(instance.loadingDataMsg).toBeDisplayed()
    await expectWDIO(instance.loadingDataMsg).toHaveText(LOADING_DATA_MESSAGE)
  })

  it('should \'Verifying openssl\' message appears', async () => {
    await instance.verifyingOpensslMsg.waitForExist({ timeout: 6000 })
    await expectWDIO(instance.verifyingOpensslMsg).toBeDisplayed()
    await expectWDIO(instance.verifyingOpensslMsg).toHaveText(VERIFYING_OPENSSL_MESSAGE)
  })

  it('should \'openssl for <platform> found\' message appears', async () => {
    if (process.platform === 'linux') {
      await instance.opensslForLinuxFound.waitForExist({ timeout: 9000 })
      await expectWDIO(instance.opensslForLinuxFound).toBeDisplayed()
      await expectWDIO(instance.opensslForLinuxFound).toHaveText(OPENSSL_FOUND_LINUX_MESSAGE)
    } else if (process.platform === 'darwin') {
      await instance.opensslForDarwinFound.waitForExist({ timeout: 9000 })
      await expectWDIO(instance.verifyingOpensslMsg).toBeDisplayed()
      await expectWDIO(instance.opensslForDarwinFound).toHaveText(OPENSSL_FOUND_DARWIN_MESSAGE)
    } else if (process.platform === 'win32') {
      await instance.opensslForWin32Found.waitForExist({ timeout: 9000 })
      await expectWDIO(instance.verifyingOpensslMsg).toBeDisplayed()
      await expectWDIO(instance.opensslForWin32Found).toHaveText(OPENSSL_FOUND_WIN32_MESSAGE)
    }
    
  })

  it('should messages disappears', async () => {
    await instance.loadingDataMsg.waitForExist({ timeout: 12000, reverse: true })
    await instance.verifyingOpensslMsg.waitForExist({ timeout: 12000, reverse: true })
    if (process.platform === 'linux') {
      await instance.opensslForLinuxFound.waitForExist({ timeout: 12000, reverse: true  })
    } else if (process.platform === 'darwin') {
      await instance.opensslForDarwinFound.waitForExist({ timeout: 12000, reverse: true  })
    } else if (process.platform === 'win32') {
      await instance.opensslForWin32Found.waitForExist({ timeout: 12000, reverse: true })
    }
  })
})
