'use strict'

import bufferedSpawn from 'buffered-spawn'
import { join } from 'path'
import Handler from './base'
import sudo from 'sudo-prompt'

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

    let __version__ = version
    let __cwd__ = ''

    if (version.match(/selfcustody/g)) {
      __version__ = version.split('tag/')[1]
      __cwd__ = join(resources, __version__, `krux-${__version__}`)
    }

    if (version.match(/odudex/g)) {
      __version__ = join(version, 'raw', 'main')
      __cwd__ = join(resources, __version__)
    }

    if (this.platform === 'linux') {
      try {
        await bufferedSpawn('chmod', ['+x', './ktool-linux'], { cwd: __cwd__ })
      } catch (error) {
        this.send('window:log:info', error)
        this.send('flash:writing:error', error)
      }
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
        name: 'Krux Installer'
      };
      sudo.exec(script, options, function (err, stdout, stderr){
        if (err) reject(err);
        if (stderr) reject(stderr);
        resolve(stdout);
      })
    });
  }

  async flash () {
    const resources = this.store.get('resources')
    const version = this.store.get('version')
    const device = this.store.get('device')

    let __version__ = version
    let __cwd__ = ''

    if (version.match(/selfcustody/g)) {
      __version__ = version.split('tag/')[1]
      __cwd__ = join(resources, __version__, `krux-${__version__}`)
    }

    if (version.match(/odudex/g)) {
      __version__ = join(version, 'raw', 'main')
      __cwd__ = join(resources, __version__)
    }

    try {
      if (this.platform === 'linux') {
        const script = [
          `${__cwd__}/ktool-linux`,
          '-B',
          'goE',
          '-b',
          '1500000',
          `${__cwd__}/${device}/kboot.kfpkg`
        ].join(' ')
        const output = await FlashHandler.sudoPromptAsync(script)
        console.log(output)
        this.send('flash:writing:done', output)
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
        console.log(err)
        this.send('window:log:info', err)
        this.send('flash:writing:error', err)
      }
    }
  }
}
