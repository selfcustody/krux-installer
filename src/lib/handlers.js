import DownloadHandler from './handler-download'
import SDCardHandler from './handler-sdcard'
/**
 * Function to handle mount,
 * umount and copy files to SDCard
 *
 * @param
 */
async function handleSDCard (app, args) {
  const sdcard = new SDCardHandler(app, args.platform)
  if (args.action === 'detect') {
    await sdcard.onDetection()
  } else if (args.action === 'mount' || args.action === 'umount') {
    await sdcard.onAction(args.action)
  } else if (args.action === 'copyto') {
    console.log(args)
    await sdcard.onWrite(args.origin, args.destination)
  } else {
    throw new Error(`SDCardHandler ${action} not implemented`)
  }
}

/*
* Function to handle downloads
* when user select to build or flash
* prebuiltin binaries.
*
* @param fileanme: String
*/
async function handleDownload (app, filename) {
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

export { handleDownload, handleSDCard }
