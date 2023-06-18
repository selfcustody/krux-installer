/// <reference path="../typings/index.d.ts"/>

import axios from 'axios'
import Handler from './handler'
import ElectronStore from 'electron-store';

export default class VerifyOfficialReleasesFetchHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:verify:releases:fetch', win, storage, ipcMain);
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
   *    await window.api.invoke('krux:verify:releases:fetch')
   *    
   *    window.api.onSuccess('krux:verify:releases:fetch', function(_, list) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:verify:releases:fetch', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build(async (options) => {
      const url = 'https://api.github.com/repos/selfcustody/krux/git/refs/tags'
      let releases: string[] = []
      try {
        this.log(`Fetching ${url}`)
        const response = await axios({
          method: 'get',
          url: url,
          headers: {
            'User-Agent': `Chrome/${process.versions.chrome}`
          }
        })
        if (response.status === 200) {
          this.log(response.data)
        } else {
          throw new Error(`${url} returned ${response.status} status code`)
        }

        this.log('Saving fetched versions in storage')
        const list = []

        // verify for newest release
        const version = response.data[response.data.length - 1]["ref"].split('tags/')[1] as string
        list.push(`selfcustody/krux/releases/tag/${version}`)
        list.push('odudex/krux_binaries')
        this.storage.set('versions', list)
        const result = {
          from: options.from,
          value: this.storage.get('versions')
        }
        this.send(`${this.name}:success`, result as KruxInstaller.JsonDict)
      } catch (error) {
        this.send(`${this.name}:error`, error)
      }
    })
  }
}