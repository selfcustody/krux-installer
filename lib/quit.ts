/// <reference path="../typings/index.d.ts"/>

import { app } from 'electron'
import ElectronStore from 'electron-store'
import Handler from './handler'

export default class QuitHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:quit', win, storage, ipcMain);
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
   *    await window.api.invoke('krux:quit')
   *    
   *    window.api.onSuccess('krux:quit', function(_, isChanged) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:quit', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build(async (options) => {
      try {
        this.send(`${this.name}:success`, '👋 Quiting krux-installer...')
        app.quit()
        process.exit(0)
      } catch (error) {
        this.send(`${this.name}:error`, { name: error.name, stack: error.stack, message: error.message })
      }
    })
  }
}
