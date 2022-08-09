import { join } from 'path'
import Handler from './handler-base'
import {
  notExistsAsync,
  mkdirAsync,
  download,
} from './utils'


/**
 * Class to handle downloads
 */
class DownloadHandler extends Handler {

  constructor (app) {
    super(app)
    this.resources = join(__dirname, '..', 'resources')
    this.baseUrl = 'https://github.com/odudex/krux_binaries/raw/main'
  }

  /**
   * Create a resource directory in the
   * root directory, if not exists.
   *
   * @param dirname: String
   */
  async onCreateResourceDir() {
    const resourcesNotExists = await notExistsAsync(this.resources)
    if (resourcesNotExists) {
      this.send('window:log:info', `creating directory ${this.resources}`)
      await mkdirAsync(this.resources)
      this.send('window:log:info', `directory ${this.resources} created`)
    } else {
      this.send('window:log:info', `directory ${this.resources} already exists`)
    }
  }

  /**
   * Set the full path of resource
   *
   * @param filename: String
   */
  async setDestination(filename) {
    this.filename = filename
    this.destination = join(this.resources, this.filename)

    const __filenameArray__ = this.destination.split('/')
    const resource = __filenameArray__[__filenameArray__.length - 1]
    this.isDestinationExists = !(await notExistsAsync(this.destination))
  }

  /**
   * Checks if full path of resource exists
   */
  async onDestinationExists() {
    // options.filename can be
    // - ktool-*
    // - maixpy_*/firmware.bin
    // - maixpy_*/kboot.kfpkg
    try {
      if (this.isDestinationExists) {
        this.send('window:log:info', `${this.destination} already downloaded`)
        this.send('download:status', '100.00')
        this.send('download:status:done', this.destination)
      }
    } catch (error) {
      this.send('window:log:info', error)
    }
  }

  /**
   * Check if destination not exists,
   * and download it if needed.
   *
   */
  async onDownloadIfDestinationNotExists() {
    this.send('window:log:info', `downloading ${this.baseUrl}/${this.filename}`)

    // if `/` string is found in filename
    // (could be `maixpy_*/kboot.kfpkg` or `maixpy_*/firmware.bin`
    // then create a new directory
    // in `__dirname/resources`
    // if not have an `/`
    // (could be ktool-*)
    // put it in `__dirname/resources`
    if (!this.isDestinationExists) {
      try {
        const __filename__ = this.filename.split('/')
        let disposition = ''
        if (__filename__.length > 1) {
          const d = join(this.resources, __filename__[0])
          const dirNotExist = await notExistsAsync(d)
          if (dirNotExist) {
            this.send('window:log:info', `creating directory ${d}`)
            await mkdirAsync(d)
            this.send('window:log:info', `directory ${d} created`)
          }
          disposition = `attachment filename=${__filename__[1]}`
        } else {
          disposition = `attachment filename=${__filename__[0]}`
        }

        let downloaded = 0
        let total = 0
        let percent = 0

        download({
          destination: this.destination,
          url: `${this.baseUrl}/${this.filename}`,
          headers: {
            'Content-Disposition': disposition,
            'User-Agent': `Chrome/${process.versions.chrome}`
          },
          onResponse: (data) => {
            total = data.headers['content-length']
            percent = ((downloaded/total) * 100).toFixed(2)
            this.send('window:log:info', `${this.baseUrl}/${this.filename} has ${total} bytes`)
            this.send('download:status', percent)
          },
          onData: (chunk) => {
            downloaded += chunk.length
            percent = ((downloaded/total) * 100).toFixed(2)
            this.send('download:status', percent)
            if (percent === '100.00') {
              this.send('window:log:info', `${this.baseUrl}/${this.filename} downloaded`)
              this.send('window:log:info', `resource can be found in ${this.destination}`)
              this.send('download:status:done', this.destination)
            }
          },
          onError: (err) => {
            this.send('window:log:info', err.stack)
            this.send(options.sender, err)
          }
        })
      } catch (error) {
        this.send('window:log:info', error.stack)
      }
    }
  }
}

export default DownloadHandler
