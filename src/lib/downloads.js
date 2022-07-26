import { join } from 'path'
import request from 'request'
import { createWriteStream } from 'fs'

const KTOOL_URLS = {
  'linux': 'https://github.com/odudex/krux_binaries/raw/main/ktool-linux'
}

const KTOOL_DESTS = join(__dirname, '..', 'dist_electron')

class Download {

  constructor(options) {
    this.url = options.url
    this.filename = options.filename
    this.dest = join(__dirname, '..', 'dist_electron', this.filename)
  }

  async get () {
    return new Promise((resolve, reject) => {
      const file = createWriteStream(this.dest)
      const stream = request({
        url: this.url,
        headers: {
          'Content-Disposition': `attachment; filename=${this.filename}`,
          'User-Agent': `Chrome/${process.versions.chrome}`,
          'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Accept-Encoding': 'gzip, deflate, br'
        },
         gzip: true
      })
      .pipe(file)
      .on('finish', () => {
        console.log(`${this.filename} downloaded at ${this.dest}`)
        resolve()
      })
      .on('error', function(err) {
        reject(err)
      })
    }).catch(error => {
      console.log(`Something happened: ${error}`)
    })
  }
}


function handleDownloadKtool(os) {
  if (os === 'win32') os = 'windows'
  return async function () {
    try {
      const downloader = new Download({
        url: KTOOL_URLS[os],
        filename: `ktool-${os}`,
        dest: KTOOL_DESTS
      })
      await downloader.get()
      return
    } catch (error) {
      console.error(error)
      return error
    }
  }
}
export { handleDownloadKtool }
