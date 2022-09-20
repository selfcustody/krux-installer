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

  async chmod () {
    const resources = this.store.get('resources')
    const version = this.store.get('version')

    const __version__ = version.split('tag/')[1]
    const __cwd__ = join(resources, __version__, `krux-${__version__}`)

    if (this.platform === 'linux') {
      try {
        await bufferedSpawn('chmod', ['+x', './ktool-linux'], { cwd: __cwd__ })
      } catch (error) {
        this.send('window:log:info', error)
        this.send('flash:writing:error', error)
      }
    }
  }

  async flash () {
    const resources = this.store.get('resources')
    const version = this.store.get('version')
    const device = this.store.get('device')

    const __version__ = version.split('tag/')[1]
    const __cwd__ = join(resources, __version__, `krux-${__version__}`)
    console.log(__cwd__)
    try {
      if (this.platform === 'linux') {
        const { stdout, stderr } = await bufferedSpawn(
          './ktool-linux',
          ['-B', 'goE', '-b', '1500000', `${device}/kboot.kfpkg`],
          { cwd: __cwd__ }
        )

        console.log(stdout)
        console.log(stderr)
        if (stdout) {
          this.send('flash:writing', stdout)
        }

        if (stderr) {
          this.send('flash:writing', stderr)
          const __err__ = new Error('Flash failed')
          this.send('window:log:info', __err__)
          this.send('flash:writing:error', __err__)
        }
      }
    } catch (err) {
      if (err.code === 'ECMDERR') {
        let msg = err.stdout.split('\x1B[0m ')[1]
        msg = msg.replace('\x1B[32m', ' ')
        msg = msg.replace('`', '')
        msg = msg.replace('`', '')
        const e = new Error(msg)
        this.send('window:log:info', e)
        this.send('flash:writing:error', e)
      } else {
        this.send('window:log:info', err)
        this.send('flash:writing:error', err)
      }
    }
  }
}
