import { join } from 'path'
import { createWriteStream } from 'fs'
import { open } from 'yauzl'
import { mkdirAsync } from './utils/fs-async'
import Handler from './base'

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
    console.log(options)
    const zipFilePath = join(options.destination, options.resource, options.file)
    console.log(zipFilePath)
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
          await mkdirAsync(folder)
          zipfile.readEntry();
        } else {
          handler.send('window:log:info', `extracting ${entry.fileName}`)

          // create the destination file
          const writeStreamPath = join(options.destination, options.resource, entry.fileName)
          console.log(writeStreamPath)
          const writeStream = createWriteStream(writeStreamPath)

          // define some variables to calculate the
          // percentege o extraction
          const uncompressedSize = entry.uncompressedSize
          let currentSize = 0

          // reset progress on client
          handler.send('zip:extract:progress', {
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
              handler.send('zip:extract:progress', {
                file: entry.fileName,
                progress: percent
              })
            })

            readStream.on('end', function () {
              handler.send('window:log:info', `extracted to ${writeStreamPath}`)
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
        handler.send('zip:extract:done', entries)
        resolve()
      })

      zipfile.on('error', function(zipErr) {
        reject(zipErr)
      })
    })
  })
}

export default class UnzipHandler extends Handler {

  constructor (win, store) {
    super(win)
    this.store = store
  }

  async unzip (options) {
    const destination = this.store.get('resources')
    try {
      this.send('window:log:info', `extracting ${join(options.resource, options.file)}`)
      await unzipAsync(this, {
        resource: options.resource,
        file: options.file,
        destination: destination
      })
    } catch (error) {
      this.send('window:log:info', error)
      this.send('zip:extract:error', error)
      console.log(error)
    }
  }
}
