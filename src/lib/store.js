import { join } from 'path'
import createDebug from 'debug'
import Store from 'electron-store'
import pjson from '../../package.json'
import bufferedSpawn from 'buffered-spawn'

const debug = createDebug('krux:store')

/*
 *
 * The KruxInstaller's persistent storage.
 * If the environment variable DEBUG is attributed to 'krux:store'
 * (DEBUG=store yarn run electron:<serve|build>),
 * any of the messages will be displayed
 * only for this module
 * @param app: The electron application
 */
export default async function (app) {
  try {
    debug('Creating store')
    const store = new Store({
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
      action: {
        type: 'string'
      },
      device: {
        type: 'string',
        regex: /maixpy_(m5stickv5|amigo|dock|bit)/g
      },
      sdcard: {
        type: 'string'
      }
    })

    debug(`  appversion: ${pjson.version}`)
    store.set('appVersion', pjson.version)

    const resourcePath = join(app.getPath('documents'), pjson.name)
    debug(`  resource: ${resourcePath}`)
    store.set('resources', resourcePath)

    debug(`  platform: ${process.platform}`)
    store.set('os', process.platform)

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
    debug(`  isMac10: ${isMac10}`)
    store.set('isMac10', isMac10)

    const versions = []
    debug(`  versions: ${versions}`)
    store.set('versions', versions)

    const version = 'Select version'
    debug(`  version: ${version}`)
    store.set('version', 'Select version')

    const action = 'Select action'
    debug(`  action: ${action}`)
    store.set('action', action)

    const device = 'Select device firmware'
    debug(`  device: ${device}`)
    store.set('device', device)

    const sdcard = ''
    debug(`  sdcard: ${sdcard}`)
    store.set('sdcard', sdcard)

    return store
  } catch (error) {
    debug(error)
  }
}
