/// <reference path="../typings/index.d.ts"/>

import { join } from 'path'
import { spawn } from 'child_process'
import Handler from './handler'
import ElectronStore from 'electron-store';

export default class VerifyOfficialReleasesSignHandler extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:verify:releases:sign', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // verify the signature of official releases
   * methods: {
   *  async download () {
   *    await window.api.invoke('krux:verify:releases:sig', {
   *      bin: 'v22.08.2/krux-v22.08.2.zip',
   *      pem: 'main/selfcustody.pem',
   *      sig: 'v22.08.2/krux-v22.08.2.zip.sig'
   *    })
   *    
   *    window.api.onSuccess('krux:verify:releases:sig', function(_, result) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:verify:releases:hash', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build (): void {
    super.build((_, options) => {
      const resources = this.storage.get('resources') as string
      const version = this.storage.get('version') as string
      
      const zipResource = version.split('tag/')[1]
      const zipFileRelPath = `${zipResource}/krux-${zipResource}.zip`
      const sigFileRelPath = `${zipResource}/krux-${zipResource}.zip.sig`
      const pemFileRelPath = 'main/selfcustody.pem'
      

      const binPath = join(resources, zipFileRelPath)
      const pemPath = join(resources, pemFileRelPath)
      const sigPath =  join(resources, sigFileRelPath)
      const platform = this.storage.get('os')

      // if platform is linux, use the same command
      // used in krux CLI. Else use sign-check package
      let shell = ''
      let compileArg = ''
      let opensslBin = ''

      if (platform === 'linux') {
        shell = "/bin/bash"
        compileArg = "-c"
        opensslBin = "openssl"
      } else if (platform === 'darwin') {
        shell = "/bin/zsh"
        compileArg = "-c"
        opensslBin = "openssl"
      } else {
        shell = "cmd"
        compileArg = "/c"
        opensslBin = "openssl.exe"
      }

      // you can still omit the quotes
      // and everything will execute correctly
      // through openssl,
      // since child_process will pass it as a single argument:
      // See:
      // https://stackoverflow.com/questions/27670686/ssh-with-nodejs-child-process-command-not-found-on-server
      const signCmd = `${opensslBin} sha256 <${binPath} -binary | ${opensslBin} pkeyutl -verify -pubin -inkey ${pemPath} -sigfile ${sigPath}`
      this.log(`${shell} ${compileArg} ${signCmd}`)

      let stdout = Buffer.alloc(0)
      let isErr = false
      const openssl = spawn(shell, [compileArg, signCmd])

      openssl.stdout.on('data', (chunk) => {
        this.log(`stdout: ${chunk}`)
        stdout = Buffer.concat([stdout, chunk])
      })

      openssl.stderr.on('data', (chunk) => {
        this.log(`stderr: ${chunk}`)
        stdout = Buffer.concat([stdout, chunk])
        isErr = true
      })

      openssl.on('error', (err) => {
        this.send(`${this.name}:error`, { name: err.name, message: err.message, stack: err.stack })
      })

      openssl.on('close', (code) => {
        this.log(`${opensslBin} exited with code ${code}`)
        if (isErr) {
          const err = new Error(stdout.toString())
          this.send(`${this.name}:error`, { name: err.name, message: err.message, stack: err.stack })
        } else {
          this.send(`${this.name}:success`, {
            command: signCmd,
            sign: stdout.toString()
          })
        }
      })
    })
  }
}