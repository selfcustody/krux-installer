'use strict'

import { spawn } from 'child_process'
import Handler from './base'

class VerifyOpenssl extends Handler {

  constructor (win, store) {
    super('verify-openssl', win, store)
  }

  verify () {
    const platform = this.store.get('platform')
    let shell = ''
    const env = { PATH: process.PATH }
    const args = []
    if (platform === 'linux' ) {
      shell = 'bash'
      args.push('-c')
      args.push('"if type openssl 2>/dev/null; then echo 1 else echo 0 fi"')
    } else if (platform === 'darwin' ) {
      shell = 'zsh'
      args.push('-c')
      args.push('"if type openssl 2>/dev/null; then echo 1 else echo 0 fi"')
    } else if (platform === 'win32') {
      shell = 'cmd'
      args.push('/c')
      // eslint-disable-next-line no-useless-escape
      args.push('IF EXISTS C:\\PROGRA~1\\Git\\usr\\bin\openssl.exe ECHO 1')
    } else {
      throw new Error(`${platform} do not supported`)
    }

    
    const verify = spawn(shell, args, env)
    let stdout = Buffer.alloc(0)
    let isErr = false

    verify.stdout.on('data', function(chunk) {
      stdout = Buffer.concat([stdout, chunk])
    })

    verify.stderr.on('data', function(chunk) {
      isErr = true
      stdout = Buffer.concat([stdout, chunk])
    })

    verify.on('error', (err) => {
      this.log(err)
      this.send(`${this.name}:error`, err)
    })

    verify.on('close', (code) => {
      this.log(`${shell} ${args.join(' ')} exited with code ${code}`)
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
 * wants to verify the existence of openssl on system
 *
 * @param win
 * @apram store
 */
 export default function (win, store) {
  //eslint-disable-next-line no-unused-vars
  return function (_event, options) {
    const handler = new VerifyOpenssl(win, store)
    handler.verify(options)
  }
}