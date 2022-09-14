import { join } from 'path'
import Store from 'electron-store'
import pjson from '../../package.json'

export default function (app) {
  try {
    const store = new Store({
      appVersion: {
        type: 'string',
      },
      resources: {
        type: 'string',
      },
      state: {
        type: 'string',
        regex: /(not_running|loading|running|shutdowning)/g,
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
    })

    store.set('appVersion', pjson.version)
    store.set('resources', join(app.getPath('documents'), pjson.name))
    store.set('state', 'loading')
    store.set('versions', [])
    store.set('version', 'Select version')
    store.set('action', 'Select action')
    store.set('device', 'Select device firmware')
    store.set('sdcard', '')

    return store
  } catch (error) {
    console.log(error)
  }
}
