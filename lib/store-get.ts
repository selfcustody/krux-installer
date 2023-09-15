/// <reference path="../typings/index.d.ts"/>

import ElectronStore from 'electron-store';
import Handler from './handler'

export default class StoreGetHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:store:get', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // get some value from key in store
   * //  - "appVersion"
   * //  - "resources"
   * //  - "os"
   * //  - "isMac10"
   * //  - "versions"
   * //  - "version"
   * //  - "device"
   * //  - "sdcard"

   * methods: {
   *  async download () {
   *    // keys:
   *    await window.api.invoke('krux:store:get', { key: 'version' })
   *    
   *    window.api.onSuccess('krux:store:get', function(_, value) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:store:get', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build() {
    super.build((options: { from: string, keys: string[] }) => {
      try {
        const result = {
          from: options.from,
          values: {}
        }
        for (let i in options.keys) {
          const key = options.keys[i]
          result.values[key] = this.storage.get(key) as KruxInstaller.JsonValue
        }
        this.send(`${this.name}:success`, result)
      } catch (error) {
        this.send(`${this.name}:error`, error)
      }
    })
  }
}