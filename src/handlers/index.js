import DownloadHandler from './download'
import SDCardHandler from './sdcard'
import UsbDetectionHandler from './usb-detection'

/**
 * Function to handle usbDetection
 * of implmented devices
 *
 * @param app<ElectronApp>
 */
function handleUsbDetection (app) {
  return function (_event, action) {
    const handler = new UsbDetectionHandler(app)
    if (action === 'detect') {
      handler.send('window:log:info', 'Activating usb detection')
      handler.activate()
      handler.send('window:log:info', 'Starting usb detection')
      handler.detect()
    } else if (action === 'stop') {
      handler.send('window:log:info', 'Starting usb deactvation')
      handler.deactivate()
    } else {
      throw new Error(`UsbDetectionHandler action '${action}' not implemented`)
    }
  }
}


/**
 * Function to handle mount,
 * umount and copy files to SDCard
 *
 * @param app<ElectronApp>
 */
function handleSDCard (app) {
  return async function (_event, args) {
    const handler = new SDCardHandler(app, process.platform)
    handler.send('window:log:info', `Starting sdcard '${args.action}' action`)
    if (args.action === 'detect') {
      await handler.onDetection()
    } else if (args.action === 'mount' || args.action === 'umount') {
      await handler.onAction(args.action)
    } else if (args.action === 'copyto') {
      await handler.onWrite(args.origin, args.destination)
    } else {
      throw new Error(`SDCardHandler ${action} not implemented`)
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
function handleDownload (app) {
  return async function (_event, filename) {
    const handler = new DownloadHandler(app)
    handler.send('window:log:info', `download ${filename} started`)
    handler.setDestination(filename)

    // create resources dir if not exists
    await handler.onCreateResourceDir()

    // Before starting downloading, check if exists
    await handler.onDestinationExists()

    //Now start the downloading and creation file
    await handler.onDownloadIfDestinationNotExists()
  }
}

function handleOSVerify (app) {
  return function () {
    app.webContents.send('window:log:info', `OS detected: using ${process.platform}`)
    app.webContents.send('os:verify', process.platform)
  }
}

export { handleDownload, handleSDCard, handleUsbDetection, handleOSVerify }
