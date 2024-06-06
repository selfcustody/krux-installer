/// <reference path="../typings/index.d.ts"/>
/// <reference path="../node_modules/electron-store/index.d.ts"/>

import { join } from 'path'
import { spawn } from 'child_process'
import Base from './base'
import pkg from '../package.json'
import ElectronStore from 'electron-store'

/*
 * The KruxInstaller's persistent storage.
 * If the environment variable DEBUG is attributed to 'krux:store'
 * (DEBUG=krux:store yarn run electron:<serve|build>),
 * any of the messages will be displayed
 * only for this module
 * @param app: The electron application
 */
export default class Storage extends Base {

  private config;

  constructor(app: Electron.App) {
    super('krux:storage')
    this.app = app
    this.config = {
      appVersion: {
        type: 'string',
      },
      resources: {
        type: 'string',
      },
      os: {
        type: 'string'
      },
      isMac10: {
        type: 'boolean'
      },
      versions: {
        type: 'array',
      },
      version: {
        type: 'string',
        regex: /(?:^odudex\/krux_binaries|selfcustody\/krux\/releases\/tag\/v\d+\.\d+\.\d+)/g
      },
      device: {
        type: 'string',
        regex: /maixpy_(m5stickv5|amigo|dock|bit)/g
      },
      showFlash: {
        type: 'boolean'
      }
    }
  }

  /**
   * Verify, with `sw_vers` utility with `-productName` option
   * the release type of the macOS, necessary to choose which
   * ktool will be used (ktool-mac or ktool-mac-10)
   */ 
  matchIsMac10 (): Promise<boolean> {
    // see
    // https://www.shell-tips.com/mac/find-macos-version/#gsc.tab=0
    return new Promise((resolve, reject) => {
      this.log('Checking macOS build')
      const __cmd__ = 'sw_vers'
      const __args__ = ['-productName']
      const __cwd__ = { cwd: '.' }

      this.log(`${__cmd__} ${__args__.join(" ")}` )
      const __sw_vers__ = spawn(__cmd__, __args__, __cwd__)
      let isMac10 = false

      __sw_vers__.on('data', (data) => {
        this.log(data)
        if (data.match(/10.*/g)) {
          isMac10 = true
        }
      })

      __sw_vers__.on('err', (err) => {
        this.log(err)
        reject(new Error(err))
      })

      __sw_vers__.on('close', (data) => {
        this.log(`return code: ${data}`)
        resolve(isMac10)
      })
    })
  }

  /*
   * Build folders: 
   * See https://www.electronjs.org/docs/latest/api/app#appgetpathname
   *
   * # appData
   *
   *   
   *   - Linux: `$HOME/.config/krux-installer`
   *   - MacOS: `$HOME/Library/Application Support/krux-installer`
   *   - Windows: `$Env:APPDATA/krux-installer`
   *
   * # userData
   * 
   *   - Linux: `$HOME/Documents/krux-installer`
   *   - MacOS: `$HOME/Documents/krux-installer`
   *   - Windows: `$Env:MyDocuments/krux-installer`
   *
   */
  async build (): Promise<ElectronStore> {
    try {
      this.log('Starting storage')
      const { default: Store } = await import('electron-store')
      const store = new Store(this.config)
      /*
       * Variables to set store
       * For mac, will be necessary to check,
       * with `sw_vers` command,
       * if the `productName` is something like
       * `10.*.*`. This will be necessary when using
       * `ktook-*` command (where * is `mac` or `mac-10`).
       */
      const resourcePath = join(this.app.getPath('documents'), pkg.name)
      const versions = []
      const version = 'Select version'
      const device = 'Select device'
      let isMac10 = false
      const showFlash = false

      if (process.platform === 'darwin') {
        isMac10 = await this.matchIsMac10()
      }

      store.set('appVersion', pkg.version)
      store.set('resources', resourcePath)
      store.set('os', process.platform)
      store.set('isMac10', isMac10)
      store.set('versions', versions)
      store.set('version', version)
      store.set('device', device)
      store.set('showFlash', showFlash)

      const keys = Object.keys(this.config)
      for (let k in keys) {
        const key = keys[k]
        const value = store.get(key)
        this.log(` ${key}: ${value}`)
      }
      return store
    } catch (error) {
      this.log(error)
    }
  }
}
