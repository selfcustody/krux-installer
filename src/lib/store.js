import { join } from 'path'
import { spawn } from 'child_process'
import createDebug from 'debug'
import Store from 'electron-store'
import pjson from '../../package.json'

/*
 * The KruxInstaller's persistent storage.
 * If the environment variable DEBUG is attributed to 'krux:store'
 * (DEBUG=krux:store yarn run electron:<serve|build>),
 * any of the messages will be displayed
 * only for this module
 * @param app: The electron application
 */
class KruxInstallerStore {

  constructor(app, name) {
    this.app = app
    this.name = `krux:${name}`
    this.debug = createDebug(this.name)
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
      sdcard: {
        type: 'string'
      }
    }
  }

  log (msg) {
    this.debug(msg)
  }

  matchIsMac10 () {
    // see
    // https://www.shell-tips.com/mac/find-macos-version/#gsc.tab=0
    return new Promise(function(resolve, reject) {
      const __cmd__ = 'sw_vers'
      const __args__ = ['-productName']
      const __cwd__ = { cwd: '.' }

      this.log(`${__cmd__} ${__args__.join(" ")}` )
      const __sw_vers__ = spawn(__cwd__, __args__, __cwd__)
      let isMac10 = false

      __sw_vers__.on('data', (data) => {
        this.log(data)
        if (data.match(/10.*/g)) {
          isMac10 = true
        }
      })

      __sw_vers__.on('err', (err) => {
        reject(new Error(err))
      })

      __sw_vers__.on('close', (data) => {
        this.log(data)
        resolve(isMac10)
      })
    })
  }

  async build () {
    try {
      const store = new Store(this.config)
      /*
       * Variables to set store
       * For mac, will be necessary to check,
       * with `sw_vers` command,
       * if the `productName` is something like
       * `10.*.*`. This will be necessary when using
       * `ktook-*` command (where * is `mac` or `mac-10`).
       */
      const resourcePath = join(this.app.getPath('documents'), pjson.name)
      const versions = []
      const version = 'Select version'
      const device = 'Select device'
      const sdcard = ''
      let isMac10 = false

      if (process.platform === 'darwin') {
        isMac10 = await this.matchIsMac10()
      }

      store.set('appVersion', pjson.version)
      store.set('resources', resourcePath)
      store.set('os', process.platform)
      store.set('isMac10', isMac10)
      store.set('versions', versions)
      store.set('version', version)
      store.set('device', device)
      store.set('sdcard', sdcard)

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

export default async function (app) {
  const installerStore = new KruxInstallerStore(app, 'store')
  return installerStore.build()
}
