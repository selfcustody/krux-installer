/// <reference path="../typings/index.d.ts"/>

import { join, dirname } from 'path'
import { createWriteStream } from 'fs'
import axios, { AxiosRequestConfig } from 'axios'
import Handler from './handler'
import { existsAsync, mkdirAsync, rmAsync, formatBytes } from './utils' 
import ElectronStore from 'electron-store'

export default class DownloadResourcesHandler extends Handler {

  private resources: string;
  private baseUrl: string;
  private originResource: string;
  private originFilename: string;
  private destinationResource: string;
  private destinationFilename: string;

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:download:resources', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // Download in client
   * // https://github.com/selfcustody/krux/releases/download/v22.08.2/krux-v22.08.2.zip
   * // to $HOME/documents/krux-installer/v22.08.2/krux-v22.08.2.zip
   * methods: {
   *  async download () {
   *    await window.api.invoke('krux:download:resources', {
   *      baseUrl: 'https://github.com/selfcustody/krux/releases/download',
   *      resource: 'v22.08.2',
   *      filename: 'krux-v22.08.2.zip'
   *    })
   *    
   *    window.api.onData('krux:download:resources', function(_, percent) {
   *      // ... do something
   *    })
   * 
   *    window.api.onSuccess('krux:download:resources', function(_, destinationFileName) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:download:resources', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build(async (options) => {
      const { baseUrl, resourceFrom, resourceTo } = options
      this.log(options)
      
      const destinationResource = dirname(resourceTo)

      try {
        // First check if destination resource exists
        // if not exists, then create a new directory
        if (!await existsAsync(destinationResource)) {
          this.log(`Creating directory ${destinationResource}`)
          await mkdirAsync(destinationResource)
          this.log(`Directory ${destinationResource} created`)
        }

        // Check if destination filename exists
        // if exists, remove it
        if (await existsAsync(resourceTo)) {
          this.log(`Removing existing ${resourceTo}`)
          await rmAsync(resourceTo)
        }

        // Setup download stream
        const fullUrl = `${baseUrl}/${resourceFrom}`
        this.log(`Downloading ${fullUrl}`)

        const file = createWriteStream(resourceTo)
        const filename = resourceTo.split(`${destinationResource}/`)[1]
        const axiosOpts = {
          method: 'get',
          url: fullUrl,
          responseType: 'stream',
          headers: {
            'Content-Disposition': `attachment filename=${filename}`,
            'User-Agent': `Chrome/${process.versions.chrome}`,
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Accept-Encoding': 'gzip, deflate, br'
          }
        } 
        this.log(axiosOpts)
        const { data, headers } = await axios(axiosOpts as AxiosRequestConfig)

        // While download occurs
        // use the chucks of data to show
        // the current progress of download
        let current = 0
        let percent: number | string  = 0
        const totalLength = headers['content-length']
        percent = ((current/totalLength) * 100).toFixed(2)
        this.log(`${resourceFrom} has ${formatBytes(totalLength)}`)
        this.send(`${this.name}:data`, percent)

        data.on('data', (chunk) => {
          current += chunk.length
          percent = ((current/totalLength) * 100)
          if (percent > 100.00) {
            percent = 100.00
          }
          percent = percent.toFixed(2)
          this.send(`${this.name}:data`, percent)
        })

        data.on('finish', () => {
          //file.close()
          this.log(`${resourceFrom} downloaded`)
        })

        data.on('close', () => {
          this.log(`Resource can be found in ${resourceTo}`)

          this.send(`${this.name}:success`, {
            from: options.from,
            resourceFrom: options.resourceFrom,
            resourceTo: options.resourceTo
          })
        })

        data.on('error', (error) => {
          this.log(error)
          this.send(`${this.name}:error`, { name: error.name, message: error.message, stack: error.stack })
        })

        data.pipe(file)
      } catch (error) {
        this.log(error)
        this.send(`${this.name}:error`, { name: error.name, message: error.message, stack: error.stack })
      }
    })
  }
}