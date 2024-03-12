/// <reference path="../typings/index.d.ts"/>

import Handler from './handler'
import ElectronStore from 'electron-store';

export default class ChangePageHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:change:page', win, storage, ipcMain);
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
   *    await window.api.invoke('krux:change:page')
   *    
   *    window.api.onSuccess('krux:change:page', function(_, list) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:change:page', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build(async (options: { page?: string, data?: any }) => {
      try {
        this.send(`${this.name}:success`, options)
      } catch (error) {
        this.log('Failed')
        this.log(error)
        this.send(`${this.name}:error`, { name: error.name, message: error.message, stack: error.stack.split('\n') })
      }
    })
  }
}
