/// <reference path="../typings/index.d.ts"/>

import { join } from 'path'
import { createHash } from 'crypto'
import { readFileAsync, existsAsync } from './utils'
import Handler from './handler'
import ElectronStore from 'electron-store';

export default class VerifyOfficialReleasesHashHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:verify:releases:hash', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // verify latest release from
   * // https://api.github.com/repos/selfcustody/krux/git/refs/tags
   * methods: {
   *  async download () {
   *    await window.api.invoke('krux:verify:releases:hash',
   *      'v22.08.2/krux-v22.08.2.zip',
   *      'v22.08.2/krux-v22.08.2.zip.sha256.txt'
   *    )
   *    
   *    window.api.onSuccess('krux:verify:releases:hash', function(_, list) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:verify:releases:hash', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build((_: Event, options: Record<string, any> )=> {
      const result = []
      const resources = this.storage.get('resources')as string
      const version = this.storage.get('version') as string
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
          const sha256txt = sha256buffer.toString().split(" ")[0]
          
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
              this.send(`${this.name}:error`, { name: error.name, message: error.message, stack: error.stack })
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
    })
  }
}
