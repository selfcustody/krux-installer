'use strict'

import { join } from 'path'
import { spawn } from 'child_process'
import Handler from './base'

class VerifyOfficialReleasesSignHandler extends Handler {

  constructor (win, store) {
    super('verify-official-releases-sign', win, store)
  }

  sign (options) {
    const resources = this.store.get('resources')

    const binPath = join(resources, options.bin)
    const pemPath = join(resources, options.pem)
    const sigPath =  join(resources, options.sig)

    this.log(`Verifying binary '${binPath}' against pem '${pemPath}' and signature '${sigPath}'`)

    const platform = this.store.get('os')

    // if platform is linux, use the same command
    // used in krux CLI. Else use sign-check package
    let shell = ''
    let opensslBin = ''
    const env = { PATH: '' }
    const __args__ = []

    if (platform === 'linux') {
      shell = "/bin/bash"
      __args__.push("-c")
      opensslBin = "openssl"
      env.PATH = "/bin:/usr/bin:/usr/local/bin"
    } else if (platform === 'darwin') {
      // see
      // https://stackoverflow.com/questions/35129977/how-to-install-latest-version-of-openssl-mac-os-x-el-capitan/46179272#46179272
      shell = "/bin/zsh"
      env.PATH = "/usr/local/opt/openssl/bin:/System/Library/OpenSSL"
      __args__.push("-c")
      opensslBin = "openssl"
    } else {
      shell = "cmd"
      __args__.push("/c")
      // see
      // https://stackoverflow.com/questions/892555/how-do-i-specify-c-program-files-without-a-space-in-it-for-programs-that-cant
      opensslBin = "%ProgramFiles%\\Git\\usr\\bin\\openssl.exe"
    }

    //  you can still omit the quotes
    //  and everything will execute correctly
    //  through openssl,
    //  since child_process will pass it as a single argument:
    // See:
    // https://stackoverflow.com/questions/27670686/ssh-with-nodejs-child-process-command-not-found-on-server
    const sigcmd = [
      `${opensslBin} sha256 <${binPath} -binary `,
      '|',
      `${opensslBin} pkeyutl -verify -pubin -inkey ${pemPath} -sigfile ${sigPath}`
    ]

    this.store.set(`signature-command`, sigcmd)
    __args__.push(sigcmd.join(' '))

    this.log(`${shell} ${__args__.join(' ')}`)
    let stdout = Buffer.alloc(0)
    let isErr = false
    const openssl = spawn(shell, __args__, { cwd: '.', env: env })

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
      this.log(err)
      this.send(`${this.name}:error`, err)
    })

    openssl.on('close', (code) => {
      this.log(`${opensslBin} exited with code ${code}`)
      stdout = stdout.toString()
      if (isErr) {
        const err = new Error(stdout.toString())
        this.log(err)
        this.send(`${this.name}:error`, err)
      } else {
        this.log(stdout)
        this.send(`${this.name}:success`, stdout)
      }
    })
  }
}

/**
 * Function to handle when
 * wants to verify signature of official releases
 *
 * @param win
 * @apram store
 */
export default function (win, store) {
  //eslint-disable-next-line no-unused-vars
  return function (_event, options) {
    const handler = new VerifyOfficialReleasesSignHandler(win, store)
    handler.sign(options)
  }
}
