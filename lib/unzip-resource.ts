/// <reference path="../typings/index.d.ts"/>

import { join } from 'path'
import { createWriteStream } from 'fs'
import { ZipFile, open } from 'yauzl'
import { mkdirAsync } from './utils'
import Handler from './handler'
import ElectronStore from 'electron-store'

function openZipFile (filepath: string): Promise<ZipFile> {
  return new Promise(function (resolve, reject) {
    open(filepath, { lazyEntries: true }, function (err, zipfile) {
      if (err) {
        reject(err)
      } else {
        resolve(zipfile)
      }
    })
  })
}

export default class UnzipResourceHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:unzip', win, storage, ipcMain)
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // unzip in client
   * // the $HOME/{{ Documents folder }}/krux-installer/{{ latest-version }}/krux-{{ latest-version }}.zip resource
   * methods: {
   *  async check () {
   *    await window.api.invoke('krux:unzip')
   * 
        // When the invoked method was successfully invoked,
   *    // it doesn't matter if it's true or false
   *    window.api.onData('krux:unzip', function(_, message) {
   *      // ... do something
   *    }) 

   *    // When the invoked method was successfully invoked,
   *    // it doesn't matter if it's true or false
   *    window.api.onSuccess('krux:unzip', function() {
   *      // ... do something
   *    }) 
   *  
   *    // When an error occurs
   *    window.api.onError('krux:unzip', function(_, error) {
   *      // ... do something
   *    }) 
   *  }
   * }
   * 
   * ```
   */
  build () {
    super.build(async (_: Event) =>{
      try {
        // Only unzip if is a selfcustody version
        let version = this.storage.get('version') as string;
        if (version.match(/selfcustody.*/g)) {
          const device = this.storage.get('device') as string;
          const resources  = this.storage.get('resources') as string;
          const os  = this.storage.get('os') as string;
          const isMac10  = this.storage.get('isMac10') as boolean;
          version = version.split('tag/')[1];
          const zipFilePath = join(resources, version, `krux-${version}.zip`)
          

          this.send(`${this.name}:data`, `Extracting ${zipFilePath}<br/><br/>`)

          const zipfile = await openZipFile(zipFilePath)
          zipfile.readEntry()

          // Each fileName should be added to entries array
          // that will be returned to client application
          // This event should extract each file to
          // a destination folder defined in store
          zipfile.on('entry', async (entry) => {

            // Directory file names end with '/'.
            // Note that entries for directories themselves are optional.
            // An entry's fileName implicitly requires its parent directories to exist.
            const destination = join(resources, entry.fileName)

            if (/\/$/.test(entry.fileName)) {
              const onlyRootKruxFolder = /^(.*\/)?krux-v[0-9\.]+\/$/
              const deviceKruxFolder = new RegExp(`^(.*\/)?krux-v[0-9\.]+\/${device}\/$`)
              if (onlyRootKruxFolder.test(entry.fileName) ||  deviceKruxFolder.test(entry.fileName)) {
                this.send(`${this.name}:data`, `Creating ${destination}<br/><br/>`)
                await mkdirAsync(destination)
              }
              zipfile.readEntry();
            } else {

              let ktoolKrux: RegExp;
              let deviceKruxFirmwareBin: RegExp;
              let deviceKruxFirmwareBinSig: RegExp;
              let deviceKruxKboot: RegExp;

              if (os === 'linux') {
                ktoolKrux = /^(.*\/)?krux-v[0-9\.]+\/ktool-linux$/
              } else if (os === 'darwin' && !isMac10) {
                ktoolKrux = /^(.*\/)?krux-v[0-9\.]+\/ktool-mac$/
              } else if (os === 'darwin' && isMac10) {
                ktoolKrux = /^(.*\/)?krux-v[0-9\.]+\/ktool-mac-10$/
              } else if (os === 'win32') {
                ktoolKrux = /^(.*\\)?krux-v[0-9\.]+\\ktool-win\.exe$/
              }

              if (os === 'linux' || os === 'darwin') {
                deviceKruxFirmwareBin = new RegExp(`^(.*\/)?krux-v[0-9\.]+\/${device}\/firmware.bin$`)
                deviceKruxFirmwareBinSig = new RegExp(`^(.*\/)?krux-v[0-9\.]+\/${device}\/firmware.bin.sig$`)
                deviceKruxKboot = new RegExp(`^(.*\/)?krux-v[0-9\.]+\/${device}\/kboot.kfpkg$`)
              } else if (os === 'win32') {
                deviceKruxFirmwareBin = new RegExp(`^(.*\\\\)?krux-v[0-9\.]+\\\\${device}\\\\firmware.bin$`)
                deviceKruxFirmwareBinSig = new RegExp(`^(.*\\\\)?krux-v[0-9\.]+\\\\${device}\\\\firmware.bin.sig$`)
                deviceKruxKboot = new RegExp(`^(.*\\\\)?krux-v[0-9\.]+\\\\${device}\\\\kboot.kfpkg$`)
              }

              // (only extract device related files)
              if (
                deviceKruxFirmwareBin.test(destination) ||
                deviceKruxFirmwareBinSig.test(destination) || 
                deviceKruxKboot.test(destination) ||
                ktoolKrux.test(destination)
              ) {
                
                // create the destination file
                const writeStream = createWriteStream(destination)

                this.send(`${this.name}:data`, `Extracting ${entry.fileName}...<br/><br/>`)

                // extract it
                zipfile.openReadStream(entry, (entryError, readStream) => {
                  if (entryError) {
                    this.send(`${this.name}:error`, { name: entryError.name, message: entryError.message, stack: entryError.stack })
                  } else {
                    readStream.on('end', () => {
                      this.send(`${this.name}:data`, `Extracted to ${destination}<br/><br/>`)
                      zipfile.readEntry()
                    })

                    readStream.on('error', (streamErr) => {
                      this.send(`${this.name}:error`, { name: streamErr.name, message: streamErr.message, stack: streamErr.stack })
                    })

                    readStream.pipe(writeStream)
                  }
                })
              } else {
                zipfile.readEntry()
              }
            }
          })

          zipfile.on('end', () => {
            zipfile.close()
            this.send(`${this.name}:success`, null)
          })

          zipfile.on('error', (zipErr) => {
            this.send(`${this.name}:error`, { name: zipErr.name, message: zipErr.message, stack: zipErr.stack })
          })
        } else {
          this.send(`${this.name}:success`, null)
        }
      } catch (error) {
        this.send(`${this.name}:error`, { name: error.name, message: error.message, stack: error.stack })
      }
    })
  }
}