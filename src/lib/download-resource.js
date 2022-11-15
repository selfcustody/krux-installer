import { join } from 'path'
import { createWriteStream } from 'fs'
import axios from 'axios'
import Handler from './base'
import { mkdirAsync, existsAsync, rmAsync } from './utils/fs-async'
import { formatBytes } from './utils/format'


/**
 * Class to handle downloads
 */
class DownloadResourcesHandler extends Handler {

  constructor (win, store, options) {
    super('download-resource', win, store)
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
    this.isResourcesExists = await existsAsync(this.destinationResource)
    this.isDestinationExists = await existsAsync(this.destinationFilename)
    if (!this.isResourceExists) {
      this.log(`Creating directory ${this.destinationResource}`)
      await mkdirAsync(this.destinationResource)
      this.log(`Directory ${this.destinationResource} created`)
    }
  }

  /**
   * Remove resource if exists
   */
  async removeIfExists() {
    try {
      const exists = await existsAsync(this.destinationFilename)
      if (exists) {
        this.log(`Removing existing ${this.destinationFilename}`)
        await rmAsync(this.destinationFilename)
      }
    } catch (error) {
      this.log(error)
    }
  }

  /*
   * Download resource
   * to stream file.
   */
  async download () {
    try {
      const fullUrl = `${this.baseUrl}/${this.originResource}/${this.originFilename}`
      this.log(`Downloading ${fullUrl}`)

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
      this.log(`${fullUrl} has ${formatBytes(totalLength)}`)
      this.send(`${this.name}:data`, percent)

      data.on('data', (chunk) => {
        current += chunk.length
        percent = ((current/totalLength) * 100).toFixed(2)
        this.send(`${this.name}:data`, percent)
      })

      data.on('finish', () => {
        //file.close()
        this.log(`${fullUrl} downloaded`)
      })

      data.on('close', () => {
        this.log(`Resource can be found in ${this.destinationFilename}`)
        this.send(`${this.name}:success`, this.destinationFilename)
      })

      data.on('error', (error) => {
        this.log(error)
        this.send(`${this.name}:error`, error.stack)
      })

      data.pipe(file)
    } catch (error) {
      this.log(error)
      this.send(`${this.name}:error`, error.stack)
    }
  }
}

export default function (win, store) {
  return async function (_event, options) {
    const handler = new DownloadResourcesHandler(win, store, options)
    await handler.setup()
    await handler.removeIfExists()
    await handler.download()
  }
}
