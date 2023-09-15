/// <reference path="../typings/index.d.ts"/>

import ElectronStore from 'electron-store';
import Handler from './handler'
import commandExists from 'command-exists'

export default class VerifyOpensslHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:verify:openssl', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * methods: {
   *  async verify () {
   *    // keys:
   *    await window.api.invoke('krux:verify:openssl', 'version')
   *    
   *    window.api.onSuccess('krux:verify:openssl', function(_, value) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:verify:openssl', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build (): void {
    super.build(async (options: { from: string }) => {
      try {
        const platform = this.storage.get('os')
        let msg = ''
        let exists: string =  ''
        if (platform === 'linux' || platform === 'darwin' ) {
          exists = await commandExists('openssl')
        }
        else if (platform === 'win32') {
          exists = await commandExists('openssl.exe')
        } else {
          throw new Error(`neither "openssl" or "openssl.exe" found for ${platform}`)
        }
        
        msg = "openssl for "+platform+`${exists ? " found" : "not found"}`

        const result = {
          ...options,
          message: msg
        }
        this.send(`${this.name}:success`, result)
      } catch (error) {
        this.send(`${this.name}:error`, error)
      }
    })
  }
}