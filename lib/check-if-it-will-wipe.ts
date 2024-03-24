/// <reference path="../typings/index.d.ts"/>

import ElectronStore from 'electron-store';
import Handler from './handler'
import { join } from 'path';
import { existsAsync } from './utils';
import { glob } from 'glob'

export default class CheckIfItWillWipeHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:check:will:wipe', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // check if all requirements to flash 
   * // a firmware are meet (i.e. files for device)
   * methods: {
   *  async download () {
   *    await window.api.invoke('krux:check:will:flash')
   *    
   *    window.api.onSuccess('krux:store:set', function(_, isChanged) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:check:will:flash', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build(async (options) => {
      const device = this.storage.get('device') as string
      const resources = this.storage.get('resources') as string

      if (device.match(/maixpy_(m5stickv|amigo|bit|dock|yahboom|cube)/g)) {
        const globfiles = await glob(
          [
            join(resources, 'odudex', 'krux_binaries', 'main', device, 'kboot.kfpkg'),
            join(resources, 'v\d+\.\d+\.\d', 'krux-v\d+\.\d+\.\d\.zip')
          ]
        )

        if (globfiles.length > 0) {
          this.send(`${this.name}:success`, { showWipe: true })
        } else {
          this.send(`${this.name}:success`, { showWipe: false })
        }
      } else {
        this.send(`${this.name}:success`, { showWipe: false })
      }
    })
  }
}
