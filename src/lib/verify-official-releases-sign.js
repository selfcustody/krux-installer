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
    const platform = this.store.get('os')

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

    //  you can still omit the quotes
    //  and everything will execute correctly
    //  through openssl,
    //  since child_process will pass it as a single argument:
    // See:
    // https://stackoverflow.com/questions/27670686/ssh-with-nodejs-child-process-command-not-found-on-server
    const signCmd = `${opensslBin} sha256 <${binPath} -binary | ${opensslBin} pkeyutl -verify -pubin -inkey ${pemPath} -sigfile ${sigPath}`
    this.store.set(`signature-command`, signCmd)
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
