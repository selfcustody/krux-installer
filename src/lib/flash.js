'use strict'

import bufferedSpawn from 'buffered-spawn'
import { join } from 'path'
import createDebug from 'debug'
import Handler from './base'
import Sudoer from '@nathanielks/electron-sudo'

const debug = createDebug('krux:flash')

export default class FlashHandler extends Handler {

  constructor (app, store) {
    super(app)
    this.store = store
  }

  log (msg) {
    debug(msg)
    this.send('window:log:info', msg)
  }

  async chmod () {
    const resources = this.store.get('resources')
    const version = this.store.get('version')
    const os = this.store.get('os')
    const isMac10 = this.store.get('isMac10')

    let __version__ = version
    let __cwd__ = ''
    let __cmd__ = ''
    let __args__ = []

    if (version.match(/selfcustody/g)) {
      __version__ = version.split('tag/')[1]
      __cwd__ = join(resources, __version__, `krux-${__version__}`)
    }

    if (version.match(/odudex/g)) {
      __version__ = join(version, 'raw', 'main')
      __cwd__ = join(resources, __version__)
    }

    try {
      if (os === 'linux') {
        __cmd__ = 'chmod'
        __args__ = ['+x', join(__cwd__, 'ktool-linux')]
      } else if (os === 'darwin' && isMac10) {
        __cmd__ = 'chmod'
        __args__ = ['+x', join(__cwd__, 'ktool-mac-10')]
      } else if (os === 'darwin' && !isMac10) {
        __cmd__ = 'chmod'
        __args__ = ['+x', join(__cwd__, 'ktool-mac')]
      } else if (os === 'win32') {
        // SEE
        // https://ourtechroom.com/tech/windows-equivalent-to-chmod-command/
        __cmd__ = 'icalcs.exe'
        __args__ = [join(__cwd__, 'ktool-win.exe'), '/GRANT', 'USER:RX']

        // It is always better to reset
        // the permission before assigning
        await bufferedSpawn('icalcs.exe', [
          join(__cwd__, 'ktool-win.exe'),
          '/RESET'
        ])
      }
      this.log(`  ${__cmd__} ${__args__.join(' ')}`)
      await bufferedSpawn(__cmd__, __args__)
    } catch (error) {
      this.log(error)
      this.send('flash:writing:error', error)
    }
  }

  async flash () {
    const resources = this.store.get('resources')
    const version = this.store.get('version')
    const device = this.store.get('device')
    const os = this.store.get('os')
    const isMac10 = this.store.get('isMac10')

    let __cwd__ = ''
    const __args__ = ['-B', 'goE', '-b', '1500000']

    if (version.match(/selfcustody/g)) {
      const __version__ = version.split('tag/')[1]
      __cwd__ = join(resources, __version__, `krux-${__version__}`)
    }

    if (version.match(/odudex/g)) {
      const __version__ = join(version, 'raw', 'main')
      __cwd__ = join(resources, __version__)
    }

    __args__.push(join(__cwd__, device, 'kboot.kfpkg'))

    let __ktool__ = ''
    if (os === 'linux') {
      __ktool__ = join(__cwd__, 'ktool-linux')
    } else if (os === 'darwin' && isMac10) {
      __ktool__ = join(__cwd__, 'ktool-mac-10')
    } else if (os === 'darwin' && !isMac10) {
      __ktool__ = join(__cwd__, 'ktool-mac')
    } else if (os === 'win32') {
      __ktool__ = join(__cwd__, 'ktool-win.exe')
    }

    const options = { name: 'KruxInstaller' }
    const sudoer = new Sudoer(options)
    const command = `${__ktool__} ${__args__.join(' ')}`
    this.log(command)

    const flash = await sudoer.spawn(command)

    flash.stdout.on('data', (data) => {
      const out = Buffer.from(data, 'utf-8').toString()
      this.log(out)
      this.send('flash:writing', out)
    })

    flash.stderr.on('data', (data) => {
      const out = Buffer.from(data, 'utf-8').toString()
      this.log(out)
      this.send('flash:writing', out)
    })

    // eslint-disable-next-line no-unused-vars
    flash.on('close', (data) => {
      this.send('flash:writing:done')
    })
  }
}
