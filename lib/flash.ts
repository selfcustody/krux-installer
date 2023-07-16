/// <reference path="../typings/index.d.ts"/>

import { spawn } from 'child_process'
import { join } from 'path'
import { SudoerLinux, SudoerDarwin } from '@o/electron-sudo/src/sudoer'
import ElectronStore from 'electron-store'
import Handler from './handler'

export default class FlashHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:flash', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // change some key in store
   * // some keys are forbidden to change
   * // https://api.github.com/repos/selfcustody/krux/git/refs/tags
   * methods: {
   *  async download () {
   *    await window.api.invoke('krux:store:set')
   *    
   *    window.api.onSuccess('krux:store:set', function(_, isChanged) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:store:set', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build(async (options) => {
      // Store
      const os = this.storage.get('os') as string
      const isMac10 = this.storage.get('isMac10') as boolean
      const resources = this.storage.get('resources') as string
      const device = this.storage.get('device') as string
      
      // OS commands
      const flash = { command: '', args: [] }
      const chmod = { commands: [] }

      // dynamic variables
      let  version = this.storage.get('version') as string
      let cwd = ''

      if (version.match(/selfcustody/g)) {
        version = version.split('tag/')[1]
        cwd = join(resources, version, `krux-${version}`)
      } else if (version.match(/odudex/g)) {
        version = join(version, 'main')
        cwd = join(resources, version)
      }

      // Choose the correct ktool flasher
      if (os === 'linux') {
        flash.command = join(cwd, 'ktool-linux')
        chmod.commands.push({ command: 'chmod', args: ['+x', flash.command] })
      } else if (os === 'win32') {
        flash.command = join(cwd, 'ktool-win.exe')
      } else if (os === 'darwin' && !isMac10) {
        flash.command = join(cwd, 'ktool-mac')
        chmod.commands.push({ command: 'chmod', args: ['+x', flash.command] })
      } else if (os === 'linux' && isMac10) {
        flash.command = join(cwd, 'ktool-mac-10')
        chmod.commands.push({ command: 'chmod', args: ['+x', flash.command] })
      }

      // set correct kboot.kfpkg
      const kboot = join(cwd, device, 'kboot.kfpkg')

      // set correct flash instructions
      // if the device 'maixpy_dock' the board argument (-B) is 'dan', 
      // otherwise, is 'goE'
      // SEE https://github.com/odudex/krux_binaries#flash-instructions
      if (device.match(/maixpy_dock/g)) {
        flash.args = `-B dan -b 1500000 ${kboot}`.split(' ')
      } else {
        flash.args = `-B goE -b 1500000 ${kboot}`.split(' ')
      }

      // stack commands to be executed
      const promises = chmod.commands.map((cmd) => {
        return new Promise<void>((resolve, reject) => {
          const message = `${cmd.command} ${cmd.args.join(' ')}`

          let error = null
          let buffer = Buffer.alloc(0)
          this.log(message)

          const script = spawn(cmd.command, cmd.args)

          script.stdout.on('data', (data) => {
            buffer = Buffer.concat([buffer, data])
          })

          script.stderr.on('data', (data) => {
            buffer = Buffer.concat([buffer, data])
            error = true
          })

          script.on('close', (code) => {
            this.log(`${message} exit code: ${code}`)
            if (error) {
              error = new Error(buffer.toString())
              reject(error)
            }
            resolve()
          })
        })
      })

      // setup flash command
      const result: Record<string, string | Function> = {}
      result.message =  `${flash.command} ${flash.args.join(' ')}`

      if (os === 'linux') {
        result.spawn = async () => {
          this.log(result.message as string)
          const sudoer = new SudoerLinux({ name: 'KruxInstaller' })
          return await sudoer.spawn(flash.command, flash.args, { env: process.env })
        }
      } if (os === 'darwin') {
        result.spawn = async () => {
          2,10
          this.log(result.message as string)
          const sudoer = new SudoerDarwin({ name: 'KruxInstaller' })
          return await sudoer.spawn(flash.command, flash.args, { env: process.env })
        }
      } else if (os === 'win32') {
        result.spawn = () => {
          return new Promise((resolve) => {
            this.log(result.message as string)
            resolve(spawn(flash.command, flash.args))
          })
        }
      }

      // add flash command to stack
      promises.push(new Promise<void>(async (resolve, reject) => {
        const runner = await (result.spawn as Function)()
        let firstRun = true
        let err = false
        let out = ''

        runner.stdout.on('data', (data: any) => {
          if (firstRun) {
            this.send(`${this.name}:data`, `\x1b[32m$> ${data}\x1b[0m\n\n`)
            firstRun = false
          }
          out = Buffer.from(data, 'utf-8').toString()
          this.send(`${this.name}:data`, out)
        })

        runner.stderr.on('data', (data: any) => {
          out = Buffer.from(data, 'utf-8').toString()
          err = true
          this.send(`${this.name}:data`, out)
        })

        runner.on('close', (code: any) => {
          if (!err) {
            resolve()
          } else {
            reject(new Error(out))
          }
        })
      }))

      try {
        await Promise.all(promises)
        this.send(`${this.name}:success`, { done: true })
      } catch(err) {
        this.send(`${this.name}:error`, { name: err.name, message: err.message, stack: err.stack })
      }
    })
  }
}
