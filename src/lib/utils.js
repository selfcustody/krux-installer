const bufferedSpawn = require('buffered-spawn');
const { createWriteStream, exists, mkdir } = require('fs')
const request = require('request')
const drivelist = require('drivelist')
const { filter } = require('lodash')
/*
 * Function to check if file or folder exists
 */
function notExistsAsync(p) {
  return new Promise((resolve) => {
    exists(p, function(exist) {
      if (!exist) resolve(true)
      resolve(false)
    })
  })
}

/*
 * Function to create folder
 */
function mkdirAsync(p, beforeCreate, afterCreate) {
  return new Promise((resolve, reject) => {
    mkdir(p, function(err) {
      if (err) reject(err)
      resolve()
    })
  })
}


/*
 * Simple function that
 * converts string that represent
 * a hexadecimal number to decimal
 * Utility to convert vendor and product ids
 * os devices in decimal format
 * (required by usb-detection module)
 */
function hex2dec (hexStr) {
  return parseInt(hexStr, 16)
}


/*
 * Helper function to be used on handleStartUSBDetection
 */
function formatMessage(d, action) {
  return `device ${d.deviceName}/${d.manufacturer} on ttyUSB${d.locationId} ${action}`
}

/*
 * @name donwload
 *
 * dowload an attachment file
 *
 * @params options
 */
function download(options) {
  // Create a new file
  const file = createWriteStream(options.destination)
  const headers = Object.assign(options.headers, {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept-Encoding': 'gzip, deflate, br'
  })
  const req = request({
    url: options.url,
    headers: headers,
    gzip: true
  })

  let downloaded = 0
  let total = 0
  let percent = 0

  req.pipe(file)
  req.on('response', options.onResponse)
  req.on('data', options.onData)
  req.on('error', options.onError)
}

/*
 * Detects if a SD card is inserted in any OS
 *
 * TODO: customize regular expression for each platform
 * @param platform
 */
async function detectSDCard (platform) {
  const drives = await drivelist.list()
  if (platform === 'linux') {
    const regex = /mmcblk.*g/
    const sdcards = filter(drives, (d) => /mmcblk/g.test(d.device))
    return sdcards[0]
  } else if (platform === 'darwin') {
    throw new Error(`SDCard detection: ${platform} not implemented yet`)
  } else if (platform === 'windows') {
    throw new Error(`SDCard detection: ${platform} not implemented yet`)
  } else {
    throw new Error(`SDCard Detection: ${platform} not supported by module drivelist`)
  }
}
/*
 * Function to format the size in bytes
 *
 * found at https://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript#18650828
 */
function formatBytes(bytes, decimals = 2) {

if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

module.exports = { notExistsAsync, mkdirAsync, hex2dec, download, formatMessage, formatBytes, detectSDCard }
