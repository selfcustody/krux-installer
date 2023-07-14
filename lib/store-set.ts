/// <reference path="../typings/index.d.ts"/>

import ElectronStore from 'electron-store';
import Handler from './handler'

export default class StoreSetHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:store:set', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // change some key in store
   * // some keys are forbidden to change
   * // https://api.github.com/repos/selfcustody/krux/git/refs/tags
   * methods: {
   *  async download () {
   *    await window.api.invoke('krux:store:set')
   *    
   *    window.api.onSuccess('krux:store:set', function(_, isChanged) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:store:set', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build((options) => {
      if (
        options.key !== 'appVersion' ||
        options.key !== 'resources' ||
        options.key !== 'os' ||
        options.key !== 'isMac10' ||
        options.key !== 'versions' || 
        options.key !== 'version'
      ) {
        this.storage.set(options.key, options.value)
        const newValue = this.storage.get(options.key)
        const result = {
          ...options,
          value: newValue as string
        }

        // Little hack to set 'showFlash'
        // if 

        this.send(`${this.name}:success`, result)
      } else {
        const error = Error(`Forbidden: cannot set '${options.key}'`)
        this.log(error.stack)
        this.send(`${this.name}:error`, error.stack)
      }
    })
  }
}