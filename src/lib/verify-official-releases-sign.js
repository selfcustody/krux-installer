'use strict'

import { join } from 'path'
import bufferedSpawn from 'buffered-spawn'
import Handler from './base'

class VerifyOfficialReleasesSignHandler extends Handler {

  constructor (win, store) {
    super('verify-official-releases-sign', win, store)
  }

  async sign (options) {
    try {
      const resources = this.store.get('resources')

      const binPath = join(resources, options.bin)
      const pemPath = join(resources, options.pem)
      const sigPath =  join(resources, options.sig)

      this.log(`Verifying binary '${binPath}' against pem '${pemPath}' and signature '${sigPath}'`)

      const platform = this.store.get('os')
      // if platform is linux, use the same command
      // used in krux CLI. Else use sign-check package
      if (platform === 'linux' || platform === 'darwin') {
        const { stdout, stderr } = await bufferedSpawn('sh', [
          '-c',
          `openssl sha256 <${binPath} -binary | openssl pkeyutl -verify -pubin -inkey ${pemPath} -sigfile ${sigPath}`
        ])
        if (stderr !== null && stderr !== '') {
          this.log(stderr)
          this.send(`${this.name}:error`, stderr)
        } else {
          this.log(stdout)
          this.send(`${this.name}:success`, stdout)
        }
      } else {
        const err = new Error(`${options.platform} not implemented`)
        this.log(err)
        this.send(`${this.name}:error`, err)
      }
    } catch (error) {
      this.log(error)
      this.send(`${this.name}:error`, error)
    }
  }
}

/**
 * Function to handle when
 * wants to verify signature of official releases
 *
 * @param win
 * @apram store
 */
export default function (win, store) {
  //eslint-disable-next-line no-unused-vars
  return async function (_event, options) {
    const handler = new VerifyOfficialReleasesSignHandler(win, store)
    handler.sign(options)
  }
}
