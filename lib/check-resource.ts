/// <reference path="../typings/index.d.ts"/>

import { join } from 'path'
import Handler from './handler'
import { existsAsync } from './utils' 
import ElectronStore from 'electron-store';

export default class CheckResourcesHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:check:resource', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // check in client
   * // if $HOME/documents/krux-installer/v22.08.2/krux-v22.08.2.zip
   * // exists
   * methods: {
   *  async check () {
   *    await window.api.invoke('krux:check:resource', 'v22.08.2/krux-v22.08.2.zip')
   * 
   *    // When the invoked method was successfully invoked,
   *    // it doesn't matter if it's true or false
   *    window.api.onSuccess('krux:check:resource', function(_, result) {
   *      // ... do something
   *    }) 
   *  
   *    // When an error occurs
   *    window.api.onError('krux:check:resource', function(_, error) {
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
        console.log(options)
        const resources = this.storage.get('resources') as string
        const destinationResource = join(resources, options.resource)
      
        this.log(`Checking if ${destinationResource} exists`)
      
        const __exists__ = await existsAsync(destinationResource)

        
        this.send(`${this.name}:success`, {
          from: options.from,
          exists: __exists__,
          baseUrl: options.baseUrl,
          resourceFrom: options.resource,
          resourceTo: destinationResource
        })
      } catch (error) {
        this.send(`${this.name}:error`, { name: error.name, message: error.message, stack: error.stack })
      }
    })
  }
}