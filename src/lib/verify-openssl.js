'use strict'

import Handler from './base'
import commandExists from 'command-exists'

class VerifyOpenssl extends Handler {

  constructor (win, store) {
    super('verify-openssl', win, store)
    this.platform = this.store.get('os')
  }

  opensslExists () {
    return commandExists('openssl').then((exists) => {
      if (exists) {
        return `"openssl" found in ${process.env.PATH} for ${this.platform}`
      } else {
        throw new Error()
      }
    // eslint-disable-next-line no-unused-vars
    }).catch((error) => {
      return commandExists('openssl.exe').then((existsExe) => {
        if (existsExe) {
          return `"openssl.exe" found in ${process.env.PATH} for ${this.platform}`
        } else {
          throw new Error(`neither "openssl" or "openssl.exe" found in ${process.env.PATH} for ${this.platform}`)
        }
      })
    })
  }

  async verify () {
    try {
      const msg = await this.opensslExists()
      this.log(msg)
      this.send(`${this.name}:success`, msg)
    } catch (error) {
      this.log(error)
      this.send(`${this.name}:error`, error)
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
