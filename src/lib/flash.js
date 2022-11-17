'use strict'

import { spawn } from 'child_process'
import { join } from 'path'
import Handler from './base'
import Sudoer from '@nathanielks/electron-sudo'

class FlashHandler extends Handler {

  constructor (app, store) {
    super('flash', app, store)
  }

  chmod () {
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
    }

    // If running in windows, according the previous
    // mentioned comment (issued in link above),
    // It is always better to reset
    // the permission before assigning
    if (__cmd__ === 'icalcs.exe') {
      const __icalcs_reset_args__ = [ join(__cwd__, 'ktool-win.exe'), '/RESET']
      this.log(`${__cmd__} ${__icalcs_reset_args__.join(" ")}`)
      const icalcs_reset = spawn(__cmd__, __icalcs_reset_args__)

      icalcs_reset.on('data', (data) => {
        this.log(data)
      })

      icalcs_reset.on('error', (err) => {
        this.log(err)
        this.send(`${this.name}:error`, err)
      })

      icalcs_reset.on('close', (data) => {
        this.log(data)
      })
    }

    const chmod = spawn(__cmd__, __args__)

    chmod.on('data', (data) => {
      this.log(data)
    })

    chmod.on('error', (err) => {
      this.log(err)
      this.send(`${this.name}:error`, err)
    })

    chmod.on('close', (data) => {
      this.log(data)
    })

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
      this.send(`${this.name}:data`, out)
    })

    flash.stderr.on('data', (data) => {
      const out = Buffer.from(data, 'utf-8').toString()
      this.log(out)
      this.send(`${this.name}:data`, out)
    })

    // eslint-disable-next-line no-unused-vars
    flash.on('close', (data) => {
      this.send(`${this.name}:success`)
    })
  }
}

/**
 * Function to handle the
 * Flashing (write krux firmware direct onto device) process
 *
 * @param win
 * @param store
 */
export default function (win, store) {
  // eslint-disable-next-line no-unused-vars
  return async function (_event, options) {
    const handler = new FlashHandler(win, store)
    handler.chmod()
    await handler.flash()
  }
}
