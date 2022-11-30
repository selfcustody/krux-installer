'use strict'

//import { spawn } from 'child_process'
import Handler from './base'
import hasbin from 'hasbin'
class VerifyOpenssl extends Handler {

  constructor (win, store) {
    super('verify-openssl', win, store)

    const platform = this.store.get('os')

    if (platform === 'linux') {
      this.executable = 'openssl'
    }
    if (platform === 'darwin') {
      this.executable = 'openssl'
      process.env.PATH = `${process.env.PATH}:/usr/local/opt/openssl/bin:/System/Library/OpenSSL`
    }
    if (platform === 'win32') {
      this.executable = 'openssl.exe'
      process.env.PATH = `${process.env.PATH};C:\\PROGRA~1\\Git\\usr\\bin`
    }
  }

  verify () {
    return new Promise((resolve, reject) => {
      hasbin(this.executable, (result) => {
        this.log(`Openssl exists in PATH: ${result}`)
        if (result) {
          this.send(`${this.name}:success`, result)
          resolve()
        } else {
          const error = new Error(`No opessl found in PATH (${process.env.PATH})`)
          this.send(`${this.name}:error`, error)
          reject(error)
        }
      })
    })
  }
}

/**
 * Function to handle when
 * wants to verify the existence of openssl on system
 *
 * @param win
 * @apram store
 */
 export default function (win, store) {
  //eslint-disable-next-line no-unused-vars
  return async function (_event, options) {
    const handler = new VerifyOpenssl(win, store)
    await handler.verify()
  }
}
