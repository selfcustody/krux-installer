'use strict'

import { spawn } from 'child_process'
import { join } from 'path'
import { userInfo } from 'os'
import Handler from './base'
import Sudoer from '@nathanielks/electron-sudo'

class FlashHandler extends Handler {

  constructor (app, store) {
    super('flash', app, store)

    const resources = this.store.get('resources')
    const version = this.store.get('version')
    const os = this.store.get('os')
    const isMac10 = this.store.get('isMac10')
    const device = this.store.get('device')
  
    if (version.match(/selfcustody/g)) {
      this.version = version.split('tag/')[1]
      this.cwd = join(resources, this.version, `krux-${this.version}`)
    }

    if (version.match(/odudex/g)) {
      this.version = join(version, 'raw', 'main')
      this.cwd = join(resources, this.version)
    }

    if (os === 'linux' ) {
      this.chmod = {
        command: 'chmod',
        args: ['+x', join(this.cwd, 'ktool-linux')]
      }
      this.flash = {
        command: join(this.cwd, 'ktool-linux'),
        args: ['-B', 'goE', '-b', '1500000', join(this.cwd, device, 'kboot.kfpkg')]
      }
    } else if (os === 'darwin' && isMac10) {
      this.chmod = {
        command: 'chmod',
        args: ['+x', join(this.cwd, 'ktool-mac-10')]
      }
      this.flash = {
        command: join(this.cwd, 'ktool-mac-10'),
        args: ['-B', 'goE', '-b', '1500000', join(this.cwd, device, 'kboot.kfpkg')]
      }
    } else if (os === 'darwin' && !isMac10) {
      this.chmod = {
        command: 'chmod',
        args: ['+x', join(this.cwd, 'ktool-mac')]
      }
      this.flash = {
        command: join(this.cwd, 'ktool-mac'),
        args: ['-B', 'goE', '-b', '1500000', join(this.cwd, device, 'kboot.kfpkg')]
      }
    } else if (os === 'win32') {
      // SEE
      // https://stackoverflow.com/questions/2928738/how-to-grant-permission-to-users-for-a-directory-using-command-line-in-windows 
      this.chmod = {
        command: 'icacls.exe',
        args: [join(this.cwd, 'ktool-win.exe'), '/grant', `${userInfo().username}:F`]
      }
      this.flash = {
        command: join(this.cwd, 'ktool-win.exe'),
        args: ['-B', 'goE', '-b', '1500000', join(this.cwd, device, 'kboot.kfpkg')]
      }
    }
  }

  createSpawn(command, args) {
    return new Promise((resolve, reject) => {
      let error = null

      const message = `${command} ${args.join(' ')}`
      this.log(message)
      
      const cmd = spawn(command, args)

      cmd.on('data', (data) => {
        this.log(data)
      })
  
      cmd.on('error', (err) => {
        error = err
      })
  
      cmd.on('close', (code) => {
        this.log(`${message} exit code: ${code}`)
        if (error) reject(error)
        resolve()
      })
    })
  }

  createSudoSpawn(command, args) {
    return new Promise((resolve) => {
      const _cmd_ = `${command} ${args.join(' ')}`
      this.log(_cmd_)
      
      const onData = (data) => {
        const out = Buffer.from(data, 'utf-8').toString()
        this.log(out)
        this.send(`${this.name}:data`, out)
      }

      const onClose = (code) => {
        this.log(`${_cmd_} exit code: ${code}`)
        resolve(code)
      }

      // In Windows, if USERNAME is not provided,
      // it will return code 1332: "No Mapping between account names and Security Id was done".
      // lets resolve this attaching the process.env.USERNAME
      // see:
      // https://answers.microsoft.com/en-us/windows/forum/all/what-is-meant-by-no-mapping-between-account-names/dcccb1bb-1c4d-4bd5-91a7-832cabf9c86b)
      // https://www.techinpost.com/no-mapping-between-account-names-and-security-ids-was-done/
      if (this.store.get('os') === 'win32') {
        const flash = spawn(command, args)
        flash.stdout.on('data', onData)
        flash.stderr.on('data', onData)
        flash.on('close', onClose)
      } else {
        const options = { name: 'KruxInstaller' }
        const sudoer =  new Sudoer(options)
        return sudoer.spawn(command, args).then((flash) => {
          flash.stdout.on('data', onData)
          flash.stderr.on('data', onData)
          flash.on('close', onClose)
        })
      }
    })
  }

  async run () {
    // Windows:
    // according Diwas Poudel
    // (see https://ourtechroom.com/tech/windows-equivalent-to-chmod-command/)
    // "It is always better to reset the permission before assigning."
    const promises = []
    try {
      if (this.chmod.command === 'icacls.exe') {
        const __icalcs_pre_args__ = [
          [join(this.cwd, 'ktool-win.exe'), '/inheritance:r'],
          [join(this.cwd, 'ktool-win.exe'), '/reset']
        ]
      
        for (let i in __icalcs_pre_args__) {
          promises.push(this.createSpawn(this.chmod.command, __icalcs_pre_args__[i]))
        }
      }
      promises.push(this.createSpawn(this.chmod.command, this.chmod.args))
      promises.push(this.createSudoSpawn(this.flash.command, this.flash.args))

      await Promise.all(promises)
      this.send(`${this.name}:success`)
    } catch (error) {
      this.log(error)
      this.send(`${this.name}:error`, error)
    }
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
    await handler.run()
  }
}
