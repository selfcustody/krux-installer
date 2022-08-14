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

    // Initialize configuration
    // if needed for each key in store
    const appVersion = store.get('appVersion')
    const resources = store.get('resources')
    const state = store.get('state')
    const versions = store.get('versions')

    if (appVersion === undefined || appVersion === null) {
      store.set('appVersion', pjson.version)
    }

    if (resources === undefined || resources === null) {
      store.set('resources', join(app.getPath('appData'), pjson.name, 'blob_storage'))
    }

    store.set('state', 'loading')

    return store
  } catch (error) {
    console.log(error)
  }
}
