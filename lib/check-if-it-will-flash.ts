/// <reference path="../typings/index.d.ts"/>

import ElectronStore from 'electron-store';
import Handler from './handler'
import { join } from 'path';
import { existsAsync } from './utils';

export default class CheckIfItWillFlashHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:check:will:flash', win, storage, ipcMain);
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
      const version = this.storage.get('version') as string
      const resources = this.storage.get('resources') as string
      const os = this.storage.get('os') as string
      const isMac10 = this.storage.get('isMac10') as boolean

      if (device.match(/maixpy_(m5stickv|amigo|amigo_ips|amigo_tft|bit|dock|yahboom|cube)/g)) {
        if (version.match(/selfcustody\/.*/g)) {
          const __version__ = version.split('tag/')[1]
          const destinationResourceZip = join(resources, __version__, `krux-${__version__}.zip`)
          const destinationResourceSha = join(resources, __version__, `krux-${__version__}.zip.sha256.txt`)
          const destinationResourceSig = join(resources, __version__, `krux-${__version__}.zip.sig`)

          if (
            await existsAsync(destinationResourceZip) &&
            await existsAsync(destinationResourceSha) &&
            await existsAsync(destinationResourceSig)
          ) {
            this.send(`${this.name}:success`, { showFlash: true })
          } else {
            
            this.send(`${this.name}:success`, { showFlash: false })
          }
        } else if (version.match(/odudex\/krux_binaries/g)) {
          const destinationResourceFirmware = join(resources, version, 'main', device, 'firmware.bin')
          const destinationResourceKboot = join(resources, version, 'main', device, 'kboot.kfpkg')
          let destinationResourceKtool = ''
          if (os === 'linux') {
            destinationResourceKtool= join(resources, version, 'main', 'ktool-linux')
          } else if (os === 'win32') {
            destinationResourceKtool= join(resources, version, 'main', 'ktool-win.exe')
          } else if (os === 'darwin' && !isMac10) {
            destinationResourceKtool= join(resources, version, 'main', 'ktool-mac')
          } else if (os === 'darwin' && isMac10) {
            destinationResourceKtool= join(resources, version, 'main', 'ktool-mac-10')
          }

          if (
            await existsAsync(destinationResourceFirmware) &&
            await existsAsync(destinationResourceKboot) &&
            await existsAsync(destinationResourceKtool)
          ) {
            this.send(`${this.name}:success`, { showFlash: true })
          } else {
            this.send(`${this.name}:success`, { showFlash: false })
          }
        } else {
          this.send(`${this.name}:success`, { showFlash: false })
        }
      }
    })
  }
}
