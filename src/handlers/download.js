import { join } from 'path'
import { createWriteStream, exists, mkdir } from 'fs'
import request from 'request'
import Handler from './base'

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

/*
 * Dowload an attachment file
 *
 * @params options<Object>: key/value based arguments
 * @params options.destination<String>: where the file should live
 * @params options.url<String>: where we get the file
 * @params options.headers<Object>: some headers to add to request. Generally 'Content-Disposition' and 'User-Agent'. 'Connection', 'Cache-Control' and 'Accept-Encoding' are added by default.
 * @params options.onResponse<Function>: callback on request's first response
 * @params options.onData<Function>: callback when a chunk of data comes in
 * @params options.onError<Function>: callback when an error occurs
 */
function download(options) {
  // Create a new file
  const file = createWriteStream(options.destination)
  const headers = Object.assign(options.headers, {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept-Encoding': 'gzip, deflate, br'
  })
  const req = request({
    url: options.url,
    headers: headers,
    gzip: true
  })

  req.pipe(file)
  req.on('response', options.onResponse)
  req.on('data', options.onData)
  req.on('error', options.onError)
}
/**
 * Class to handle downloads
 */
class DownloadHandler extends Handler {

  constructor (
    app,
    options={
      resources: resources=join(__dirname, '..', 'resources'),
      baseUrl: 'https://github.com/odudex/krux_binaries/raw/main'
    }
  ) {
    super(app, options)
    this.resources = options.resources
    this.baseUrl = options.baseUrl
  }

  /**
   * Create a resource directory in the
   * root directory, if not exists.
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
