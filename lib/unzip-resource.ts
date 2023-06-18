/// <reference path="../typings/index.d.ts"/>

import { join } from 'path'
import { createWriteStream } from 'fs'
import { open } from 'yauzl'
import { mkdirAsync } from './utils'
import Handler from './handler'
import ElectronStore from 'electron-store'

/**
 * unzipAsync
 *
 * unzip the required .zip file selected in options.file
 * to a selected destination in options.destination
 *
 * @param handler
 * @param options
 */
function unzipAsync (handler, options) {
  return new Promise(function (resolve, reject) {
    const zipFilePath = join(options.destination, options.resource, options.file)

    handler.log(`Opening ${zipFilePath}`)
    open(zipFilePath, { lazyEntries: true }, function (err, zipfile) {
      if (err) reject(err)
      zipfile.readEntry()

      const entries = []

      // Each fileName should be added to entries array
      // that will be returned to client application
      // This event should extract each file to
      // a destination folder defined in store
      zipfile.on('entry', async function (entry) {
        if (/\/$/.test(entry.fileName)) {
          // Directory file names end with '/'.
          // Note that entries for directories themselves are optional.
          // An entry's fileName implicitly requires its parent directories to exist.
          const folder = join(options.destination, options.resource, entry.fileName)
          handler.log(`Creating ${folder}`)
          await mkdirAsync(folder)
          zipfile.readEntry();
        } else {
          handler.log(`Extracting ${entry.fileName}`)

          // create the destination file
          const writeStreamPath = join(options.destination, options.resource, entry.fileName)
          const writeStream = createWriteStream(writeStreamPath)

          // define some variables to calculate the
          // percentege o extraction
          const uncompressedSize = entry.uncompressedSize
          let currentSize = 0

          // reset progress on client
          handler.send(`${handler.name}:data`, {
            file: entry.fileName,
            progress: 0
          })

          // put the names in array
          entries.push(entry.fileName)

          // extract it
          zipfile.openReadStream(entry, function (entryError, readStream) {
            if (entryError) reject(entryError)

            readStream.on('data',function (chunk) {
              currentSize += chunk.length
              const percent = ((currentSize/uncompressedSize) * 100).toFixed(2)
              handler.send(`${handler.name}:data`, {
                file: entry.fileName,
                progress: percent
              })
            })

            readStream.on('end', function () {
              handler.log(`Extracted to ${writeStreamPath}`)
              zipfile.readEntry()
            })

            readStream.on('error', function (streamErr) {
              reject(streamErr)
            })

            readStream.pipe(writeStream)
          })
        }
      })

      zipfile.on('end', function () {
        zipfile.close()
        handler.send(`${handler.name}:success`, entries)
        resolve(entries)
      })

      zipfile.on('error', function(zipErr) {
        reject(zipErr)
      })
    })
  })
}

export default class UnzipResourceHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:unzip:resource', win, storage, ipcMain)
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // unzip in client
   * // the $HOME/documents/krux-installer/v22.08.2/krux-v22.08.2.zip resource
   * methods: {
   *  async check () {
   *    await window.api.invoke('krux:unzip:resource', {
   *      resource: 'v22.08.2',
   *      file: 'krux-v22.08.2.zip'
   *    })
   * 
   *    // When the invoked method was successfully invoked,
   *    // it doesn't matter if it's true or false
   *    window.api.onSuccess('krux:unzip:resource', function(_, list) {
   *      // ... do something
   *    }) 
   *  
   *    // When an error occurs
   *    window.api.onError('krux:unzip:resource', function(_, error) {
   *      // ... do something
   *    }) 
   *  }
   * }
   * 
   * ```
   */
  build () {
    super.build(async (_, options) =>{
      try {
        const destination = this.storage.get('resources') as string
        this.log(`Extracting ${join(options.resource, options.file)}`)
        await unzipAsync(this, {
          resource: options.resource,
          file: options.file,
          destination: destination
        })
      } catch (error) {
        this.log(error)
        this.send(`${this.name}:error`, error)
      }
    })
  }
}