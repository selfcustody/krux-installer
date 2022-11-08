import { join } from 'path'
import createDebug from 'debug'
import { each } from 'lodash'
import Store from 'electron-store'
import pjson from '../../package.json'
import bufferedSpawn from 'buffered-spawn'

const debug = createDebug('krux:store')

/*
 *
 * The KruxInstaller's persistent storage.
 * If the environment variable DEBUG is attributed to 'krux:store'
 * (DEBUG=krux:store yarn run electron:<serve|build>),
 * any of the messages will be displayed
 * only for this module
 * @param app: The electron application
 */
export default async function (app) {
  try {
    const storeConfig = {
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

    const store = new Store(storeConfig)

    /*
     * Variables to set store
     * For mac, will be necessary to check,
     * with `sw_vers` command,
     * if the `productName` is something like
     * `10.*.*`. This will be necessary when using
     * `ktook-*` command (where * is `mac` or `mac-10`).
     */
    const resourcePath = join(app.getPath('documents'), pjson.name)
    let isMac10 = false
    if (process.platform === 'darwin') {
      const output = await bufferedSpawn('sw_vers', ['-productName'], { cwd: '.' })
      if (output.stderr) {
        throw new Error(output.stderr)
      } else {
        if (output.stdout.match(/10.*/g)) {
          isMac10 = true
        }
      }
    }
    const versions = []
    const version = 'Select version'
    const device = 'Select device'
    const sdcard = ''

    store.set('appVersion', pjson.version)
    store.set('resources', resourcePath)
    store.set('os', process.platform)
    store.set('isMac10', isMac10)
    store.set('versions', versions)
    store.set('version', version)
    store.set('device', device)
    store.set('sdcard', sdcard)

    each(Object.keys(storeConfig), function(key) {
      const value = store.get(key)
      debug(` ${key}: ${value}`)
    })

    return store
  } catch (error) {
    debug(error)
  }
}
