'use strict'

import { join } from 'path'
import { createHash } from 'crypto'
import { readFileAsync, existsAsync } from './utils/fs-async'
import Handler from './base'

class VerifyOfficialReleasesHashHandler extends Handler {

  constructor (win, store) {
    super('verify-official-releases-hash', win, store)
  }

  /*
   * verifyHash
   */
  async hash () {
    const result = []
    const resources = this.store.get('resources')
    const version = this.store.get('version')
    const resource = version.split('tag/')[1]

    const zipFileRelPath = `${resource}/krux-${resource}.zip`
    const shaFileRelPath = `${resource}/krux-${resource}.zip.sha256.txt`

    const zipFilePath = join(resources, zipFileRelPath)
    const shaFilePath = join(resources, shaFileRelPath)

    // Maybe the sha256txt file could be downloade
    // after checking, so we will check if the file exists
    // and the string represenation is valid
    // every second, and then, return the result to client
    const verify = async (p) => {
      try {
        const exists = await existsAsync(p)
        const sha256buffer = await readFileAsync(shaFilePath, null)
        const sha256txt = sha256buffer.toString()
        if (exists && sha256txt !== '') {
          result.push({
            name: shaFileRelPath,
            value: sha256txt.replace(/[\n\t\r]/g,'')
          })

          const zipBuffer = await readFileAsync(zipFilePath, null)
          const hashSum = createHash('sha256')
          hashSum.update(zipBuffer)

          result.push({
            name: zipFileRelPath,
            value: hashSum.digest('hex')
          })

          const isMatch = result[0].value === result[1].value

          if (isMatch) {
            const msg = [
              'sha256sum match:',
              `${result[0].name} has a ${result[1].value} hash`,
              `and ${result[1].name} summed a hash ${result[1].value}.`
            ].join(' ')
            this.log(msg)
            this.send(`${this.name}:success`, result)
          } else {
            const msg = [
              'sha256sum match error:',
              `${result[0].name} has a hash of ${result[0].value}`,
              `and ${result[1].name} summed a hash of ${result[1].value}`
            ].join(' ')
            const error = new Error(msg)
            this.log(error)
            this.send(`${this.name}:error`, error)
          }
          clearInterval(interval)
        }
      } catch (error) {
        this.log(error)
        this.send(`${this.name}:error`, error)
      }
    }
    this.log(`Verifying ${zipFilePath} against ${shaFilePath}`)
    const interval = setInterval(verify, 1000, shaFilePath)
  }
}

/**
 * Function to handle when
 * wants to verify hashes of official releases
 *
 * @param win
 * @apram store
 */
export default function (win, store) {
  // eslint-disable-next-line no-unused-vars
  return async function (_event, options) {
    const handler = new VerifyOfficialReleasesHashHandler(win, store)
    handler.hash()
  }
}
