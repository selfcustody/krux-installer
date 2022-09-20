import { map } from 'lodash'
import DownloadHandler from './download'
import SDCardHandler from './sdcard'
import SerialportHandler from './serialport'
import VerifyOfficialReleasesHandler from './verify-official-releases'
import UnzipHandler from './unzip'
import FlashHandler from './flash'

/**
 * Function to handle when
 * window is started
 *
 * @param win
 * @apram store
 */
export function handleWindowStarted (win, store) {
  // eslint-disable-next-line no-unused-vars
  return function (_event, action) {
    store.set('state', 'running')
    const version = store.get('appVersion')
    const state = store.get('state')
    win.webContents.send('window:log:info', `Krux installer ${version} ${state}`)
    win.webContents.send('window:log:info', 'page: MainPage')
  }
}


/**
 * Function to handle when
 * wants to verify official releases
 *
 * @param win
 * @apram store
 */
export function handleVerifyOfficialReleases (win, store) {
  // eslint-disable-next-line no-unused-vars
  return async function (_event, action) {
    const handler = new VerifyOfficialReleasesHandler(win, store)
    const releases = await handler.fetchReleases()
    let list = store.get('versions')

    // verify for new releases if length of fetch is greater than the local list
    if (list.length === 0 || list.length < (Object.keys(releases)).length) {
      const __list__ = map(releases, (r) => {
        const version = r.ref.split('tags/')[1]
        return `selfcustody/krux/releases/tag/${version}`
      })
      __list__.push('odudex/krux_binaries')
      store.set('versions', __list__)
      list = store.get('versions')
    }
    handler.send('official:releases:get', { releases: list })
  }
}

/**
 * Function to handle the setting of many config values
 *
 * @param win
 * @param store
 */
export function handleStoreSet (win, store) {
  return function (_event, action) {
    if (
      action.key !== 'appVersion' ||
      action.key !== 'resources' ||
      action.key === 'state' ||
      action.key !== 'versions'
    ) {
      store.set(action.key, action.value)
      win.webContents.send('window:log:info', `store set: ${action.key} = '${store.get(action.key)}'`)
      win.webContents.send(`store:set:${action.key}`, store.get(action.key) ? true : false)
    } else {
      throw new Error(`Forbidden: cannot set '${action.key}'`)
    }
  }
}

/**
 * Function to handle the capture of many config values
 *
 * @param win
 * @param store
 */
export function handleStoreGet (win, store) {
  return function (_event, action) {
    const val = store.get(action.key)
    win.webContents.send('window:log:info', `store get: ${action.key} = '${val}'`)
    win.webContents.send(`store:get:${action.key}`, val)
  }
}
/**
 * Function to handle usbDetection
 * of implmented devices
 *
 * @param app<ElectronApp>
 */
export function handleSerialport (win, store) {
  // eslint-disable-next-line no-unused-vars
  return function (_event, options) {
    const handler = new SerialportHandler(win, store)
    handler.list()
  }
}


/**
 * Function to handle mount,
 * umount and copy files to SDCard
 *
 * @param app<ElectronApp>
 */
export function handleSDCard (app, store) {
  return async function (_event, args) {

    const handler = new SDCardHandler(app, store, process.platform)
    handler.send('window:log:info', `Starting sdcard '${args.action}' action`)
    if (args.action === 'detect') {
      await handler.onDetection()
    } else if (args.action === 'mount' || args.action === 'umount') {
      await handler.onAction(args.action)
    } else if (args.action === 'copy_firmware_bin') {
      await handler.onCopyFirmwareBin()
    } else {
      throw new Error(`SDCardHandler ${args.action} not implemented`)
    }
  }
}

/*
* Function to handle downloads
* when user select to build or flash
* prebuiltin binaries.
*
* @param fileanme: String
*/
export function handleDownload (app, store) {
  return async function (_event, options) {
    const handler = new DownloadHandler(app, store, options)

    // Before starting downloading, check if exists
    await handler.setup()

    // check if resource folder not exists
    await handler.download()
  }
}

export function handleOSVerify (app) {
  return function () {
    app.webContents.send('window:log:info', `OS detected: using ${process.platform}`)
    app.webContents.send('os:verify', process.platform)
  }
}

export function handleVerifyOfficialReleasesHash (win, store) {
  // eslint-disable-next-line no-unused-vars
  return async function (_event, options) {
    const handler = new VerifyOfficialReleasesHandler(win, store)
    handler.verifyHash()
  }
}

export function handleVerifyOfficialReleasesSign (win, store) {
  return async function (_event, options) {
    const handler = new VerifyOfficialReleasesHandler(win, store)
    options.platform = process.platform
    handler.verifySign(options)
  }
}

export function handleUnzip (win, store) {
  return async function (_event, options) {
    const handler = new UnzipHandler(win, store)
    handler.unzip(options)
  }
}

export function handleFlash (win, store) {
  // eslint-disable-next-line no-unused-vars
  return async function (_event, options) {
    const handler = new FlashHandler(win, store, process.platform)
    handler.chmod()
    handler.flash()
  }
}
