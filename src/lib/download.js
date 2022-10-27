import { join } from 'path'
import { createWriteStream } from 'fs'
import axios from 'axios'
import createDebug from 'debug'
import Handler from './base'
import { mkdirAsync, existsAsync } from './utils/fs-async'
import { formatBytes } from './utils/format'

const debug = createDebug('krux:download')

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

  _info (msg) {
    debug(msg)
    this.send('window:log:info', msg)
  }

  /**
   * Checks if full path of resource exists
   */
  async setup() {
    this.isResourceExists = await existsAsync(this.destinationResource)
    this.isDestinationExists = await existsAsync(this.destinationFilename)

    if (this.isResourceExists && this.isDestinationExists) {
      this._info(`${this.destinationFilename} already downloaded`)
      this.send('download:status', '100.00')
      this.send('download:status:done', this.destinationFilename)
    }

    if (!this.isResourceExists) {
      this._info(`creating directory ${this.destinationResource}`)
      await mkdirAsync(this.destinationResource)
      this._info(`directory ${this.destinationResource} created`)
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
        this._info(`downloading ${fullUrl}`)

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
        this._info(`${fullUrl} has ${formatBytes(totalLength)}`)
        this.send('download:status', percent)

        data.on('data', (chunk) => {
          current += chunk.length
          percent = ((current/totalLength) * 100).toFixed(2)
          this.send('download:status', percent)
          if ( percent === '100.00') {
            this._info(`${fullUrl} downloaded`)
            this._info(`resource can be found in ${this.destinationFilename}`)
            this.send('download:status:done', this.destinationFilename)
          }
        })

        data.on('finish', function () {
          file.close()
        })

        data.on('error', (error) => {
          this._info(error)
          this.send('download:status:error', error.stack)
        })

        data.pipe(file)
      } catch (error) {
        this._info(error)
        this.send('download:status:error', error.stack)
      }
    }
  }
}

export default DownloadHandler
