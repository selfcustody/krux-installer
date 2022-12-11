'use strict'

import Handler from './base'
import commandExists from 'command-exists'

class VerifyOpenssl extends Handler {

  constructor (win, store) {
    super('verify-openssl', win, store)

    const platform = this.store.get('os')

    if (platform === 'linux' || platform === 'darwin') {
      this.executable = 'openssl'
    }
    if (platform === 'win32') {
      this.executable = 'openssl.exe'
    }
  }

  async verify () {
    const exists = await commandExists(this.executable)
    this.log(`Openssl exists in ${process.env.PATH}`)
    if (exists) {
      this.send(`${this.name}:success`, exists)
    } else {
      this.send(`${this.name}:error`, new Error(`${this.executable} not found in ${process.env.PATH}`))
    }
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
