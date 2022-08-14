import { homedir } from 'os'
import { join } from 'path'
import { createWriteStream, exists, mkdir } from 'fs'
import axios from 'axios'
import Handler from './base'
import { formatBytes } from './utils'

/*
 * Function to check if file or folder exists
 * in async/await approach. Always resoulves to
 * a boolean value.
 *
 * @param p<String>: path of the file
 * @return Boolean
 */
function existsAsync(p) {
  return new Promise((resolve) => {
    exists(p, function(exist) {
      if (exist) {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

/*
 * Function to create folder
 * in async/await approach. Throws
 * an error if any occurs.
 *
 * @param p<String>: path of the file
 * @throw Error: if some error occurs
 */
function mkdirAsync(p) {
  return new Promise((resolve, reject) => {
    mkdir(p, function(err) {
      if (err) reject(err)
      resolve()
    })
  })
}

/**
 * Class to handle downloads
 */
class DownloadHandler extends Handler {

  constructor (app, store, options) {
    super(app)
    this.store = store
    this.resources = store.get('resources')
    this.baseUrl = options.baseUrl
    this.originResource = options.resource
    this.originFilename = options.filename
    this.destinationResource = join(this.resources, this.originResource)
    this.destinationFilename = join(this.destinationResource, this.originFilename)
  }

  /**
   * Checks if full path of resource exists
   */
  async setup() {
    this.isResourceExists = await existsAsync(this.destinationResource)
    this.isDestinationExists = await existsAsync(this.destinationFilename)

    if (this.isResourceExists && this.isDestinationExists) {
      this.send('window:log:info', `${this.destination} already downloaded`)
      this.send('download:status', '100.00')
      this.send('download:status:done', this.destinationFilename)
    }

    if (!this.isResourceExists) {
      this.send('window:log:info', `creating directory ${this.destinationResource}`)
      await mkdirAsync(this.destinationResource)
      this.send('window:log:info', `directory ${this.destinationResource} created`)
    }
  }


  /**
   * Check if destination not exists,
   * and download it if needed.
   *
   */
  async download() {
    if (!this.isDestinationExists) {

      try {
        const fullUrl = `${this.baseUrl}/${this.originResource}/${this.originFilename}`
        this.send('window:log:info', `downloading ${fullUrl}`)

        const file = createWriteStream(this.destinationFilename)
        const { data, headers } = await axios({
          method: 'get',
          url: fullUrl,
          responseType: 'stream',
          headers: {
            'Content-Disposition': `attachment filename=${this.originFilename}`,
            'User-Agent': `Chrome/${process.versions.chrome}`,
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept-Encoding': 'gzip, deflate, br'
          }
        })

        let current = 0
        let percent = 0
        const totalLength = headers['content-length']
        percent = ((current/totalLength) * 100).toFixed(2)
        this.send('window:log:info', `${fullUrl} has ${formatBytes(totalLength)}`)
        this.send('download:status', percent)

        data.on('data', (chunk) => {
          current += chunk.length
          percent = ((current/totalLength) * 100).toFixed(2)
          this.send('download:status', percent)
          if ( percent === '100.00') {
            this.send('window:log:info', `${fullUrl} downloaded`)
            this.send('window:log:info', `resource can be found in ${this.destinationFilename}`)
            this.send('download:status:done', this.destinationFilename)
          }
        })

        data.on('error', (error) => {
          this.send('window:log:info', error.stack)
          this.send('download:status:error', error.stack)
        })

        data.pipe(file)
      } catch (error) {
        this.send('window:log:info', error.stack)
        this.send('download:status:error', error.stack)
      }
    }
  }
}

export default DownloadHandler
