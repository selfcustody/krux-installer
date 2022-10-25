'use strict'

import bufferedSpawn from 'buffered-spawn'
import { join } from 'path'
import createDebug from 'debug'
import Handler from './base'
import sudo from 'sudo-prompt'

const debug = createDebug('krux:flash')

export default class FlashHandler extends Handler {

  constructor (app, store) {
    super(app)
    this.store = store
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
        __args__ = ['+x', './ktool-linux']
      } else if (os === 'darwin' && isMac10) {
        __cmd__ = 'chmod'
        __args__ = ['+x', './ktool-mac-10']
      } else if (os === 'darwin' && !isMac10) {
        __cmd__ = 'chmod'
        __args__ = ['+x', './ktool-mac']
      } else if (os === 'win32') {
        // SEE
        // https://ourtechroom.com/tech/windows-equivalent-to-chmod-command/
        __cmd__ = 'icalcs.exe'
        __args__ = ['.\\ktool-win.exe', '/GRANT', 'USER:RX']

        //It is always better to reset the permission before assigning
        await bufferedSpawn('icalcs.exe', ['.\\ktool-win.exe', '/RESET'], { cwd: __cwd__ })
      }
      debug(`[${__cwd__}]: ${__cmd__} ${__args__.join(' ')}`)
      await bufferedSpawn(__cmd__, __args__, { cwd: __cwd__ })
    } catch (error) {
      debug(error)
      this.send('window:log:info', error)
      this.send('flash:writing:error', error)
    }
  }

  /*
   * Shows a dialog requiring the
   * system's administrador password to
   * execute privileged tasks (mounting)
   *
   * @param script<String>: the main script to run with sudo prompt
   */
  static sudoPromptAsync (script) {
    return new Promise(function (resolve, reject) {
      const options = {
        name: 'KruxInstaller'
      };
      sudo.exec(script, options, function (err, stdout, stderr){
        if (err) {
          debug(err)
          reject(err);
        }
        if (stderr) {
          debug(stderr)
          reject(stderr);
        }
        resolve(stdout);
      })
    });
  }

  async flash () {
    const resources = this.store.get('resources')
    const version = this.store.get('version')
    const device = this.store.get('device')
    const os = this.store.get('os')
    const isMac10 = this.store.get('isMac10')

    let __version__ = version
    let __cwd__ = ''
    let __cmd__ = ''

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
        __cmd__ = [
          `${__cwd__}/ktool-linux`,
          '-B',
          'goE',
          '-b',
          '1500000',
          `${__cwd__}/${device}/kboot.kfpkg`
        ].join(' ')
      } else if (os === 'darwin' && isMac10) {
        __cmd__ = [
          `${__cwd__}/ktool-mac-10`,
          '-B',
          'goE',
          '-b',
          '1500000',
          `${__cwd__}/${device}/kboot.kfpkg`
        ].join(' ')
      } else if (os === 'darwin' && !isMac10) {
        __cmd__ = [
          `${__cwd__}/ktool-mac`,
          '-B',
          'goE',
          '-b',
          '1500000',
          `${__cwd__}/${device}/kboot.kfpkg`
        ].join(' ')
      } else if (os === 'win32') {
        __cmd__ = [
          `${__cwd__}\\ktool-win.exe`,
          '-B',
          'goE',
          '-b',
          '1500000',
          `${__cwd__}\\${device}\\kboot.kfpkg`
        ].join(' ')
      }
      debug(__cmd__)
      let output = await FlashHandler.sudoPromptAsync(__cmd__)
      debug(output)
      output = Buffer.from(output, 'utf-8').toString()
      this.send('flash:writing:done', output)
      this.send('window:log:info', output)
    } catch (err) {
      debug(err)
      if (err.code === 'ECMDERR') {
        let msg = Buffer.from(err.stdout, 'utf-8').toString()
        //split('\x1B[0m ')[1]
        //msg = msg.replace('\x1B[32m', ' ')
        //msg = msg.replace('`', '')
        //msg = msg.replace('`', '')
        //const e = new Error(msg)
        this.send('window:log:info', msg)
        this.send('flash:writing:done', msg)
      } else {
        debug(err)
        this.send('window:log:info', err)
        this.send('flash:writing:error', err)
      }
    }
  }
}
