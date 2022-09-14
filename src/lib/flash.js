'use strict'

import bufferedSpawn from 'buffered-spawn'
import { join } from 'path'
import Handler from './base'

export default class FlashHandler extends Handler {

  constructor (app, store, platform) {
    super(app)
    this.store = store

    if (platform !== 'linux') {
      throw new Error(`SDCardHandler not implemented on '${platform}'`)
    } else {
      this.platform = platform
    }
  }

  async flash () {
    const resources = this.store.get('resources')
    const version = this.store.get('version')
    const device = this.store.get('device')

    const __version__ = version.split('tag/')[1]
    const __cwd__ = join(resources, __version__, `krux-${__version__}`)

    if (this.platform === 'linux') {
      let maixpy_device = ''

      // maixpy_m5stickv
      if (device.vendorId === '0403' && device.productId === '6001') {
        maixpy_device = 'maixpy_m5stickv'
      }
      // maixpy_bit
      else if (device.path === '/dev/ttyUSB0' && device.vendorId === '0403' && device.productId === '6010') {
        maixpy_device = 'maixpy_bit'
      }
      // maixpy_amigo
      else if (device.path === '/dev/ttyUSB1' && device.vendorId === '0403' && device.productId === '6010') {
        if (device.type === 'tft') maixpy_device = 'maixpy_amigo_tft'
        if (device.type === 'ips') maixpy_device = 'maixpy_amigo_ips'
      }
      // maixpy_dock
      else if (device.vendorId === '7523' && device.productId === '1a86') {
        maixpy_device = 'maixpy_dock'
      }

      const { stdout, stderr } = await bufferedSpawn('./ktool', [
        '-B',
        'goE',
        '-b',
        '1500000',
        `${maixpy_device}/kboot.kfpkg`
      ],
        {
          cwd: __cwd__,
          stdio: 'pipe'
        }
      )

      const err = []
      stdout.on('data', (chunk) => {
        this.send('flash:writing', chunk.toString())
      })

      stdout.on('end', () => {
        this.send('flash:writing:done', true)
      })

      stderr.on('data', (chunk) => {
        this.send('flash:writing', chunk.toString())
        err.push(chunk.toString())
      })

      stderr.on('end', () => {
        const __err__ = new Error(err.join(''))
        this.send('window:log:info', __err__)
        this.send('flash:writing:error', __err__)
      })
    }
  }
}
