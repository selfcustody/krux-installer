import crypto from 'crypto'
import fs from 'fs'
import { join } from 'path'
import axios from 'axios'
import { readFileAsync } from './utils'
import Handler from './base'

export default class VerifyOfficialReleasesHandler extends Handler {

  constructor (win, store) {
    super(win)
    this.url = 'https://api.github.com/repos/selfcustody/krux/git/refs/tags'
    this.headers = {
      'User-Agent': `Chrome/${process.versions.chrome}`
    }
    this.store = store
  }

  async fetchReleases() {
    try {
      this.send('window:log:info', `fetching ${this.url}`)
      const response = await axios({
        method: 'get',
        url: this.url,
        headers: this.headers
      })
      if (response.status === 200) {
        return response.data
      } else {
        throw new Error(`${this.url} returned ${response.status} code`)
      }
    } catch (error) {
      throw error
    }
  }

  async verifyHash (options) {
    try {
      const result = []
      const version = this.store.get('version')
      const resources = this.store.get('resources')

      const zipFilePath = join(resources, options.zipFile)
      const shaFilePath = join(resources, options.sha256File)

      const sha256buffer = await readFileAsync(shaFilePath, { encoding: 'utf8'})

      result.push({
        name: options.sha256File,
        value: sha256buffer.replace(/[\n\t\r]/g,'')
      })

      const zipBuffer = await readFileAsync(zipFilePath, null)
      const hashSum = crypto.createHash('sha256')
      hashSum.update(zipBuffer)

      result.push({
        name: options.zipFile,
        value: hashSum.digest('hex')
      })

      const isMatch = result[0].value === result[1].value

      if (isMatch) {
        const msg = [
          'sha256sum match:',
          `${result[0].name} has a ${result[1].value} hash`,
          `and ${result[1].name} summed a hash ${result[1].value}.`
        ].join(' ')
        this.send('window:log:info', msg)
        this.send('official:releases:verified:hash', result)
      } else {
        const msg = [
          'sha256sum match error:',
          `${result[0].name} has a hash of ${result[0].value}`,
          `and ${result[1].name} summed a hash of ${result[1].value}`
        ].join(' ')
        const error = new Error(msg)
        this.send('window:log:info', error)
        this.send('official:releases:verified:error', error)
        console.log(error)
      }
    } catch (error) {
      this.send('window:log:info', error)
      this.send('official:releases:verified:error', error)
      console.log(error)
    }
  }
}
