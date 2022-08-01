const bufferedSpawn = require('buffered-spawn');
const { createWriteStream, exists, mkdir } = require('fs')
const request = require('request')
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
 * lblk
 *
 * Same as unix `lsblk` command line interface. See `man lsblk`
 *
 * @param options (Object)
 * @return Object
 */
async function lsblk (options={}) {
  try {
    const __options__ = Object.assign(options, {
      json: true
    })
    const args = []
    if (options.noempty) args.push('--noempty')
    if (options.discard) args.push('--discard')
    if (options.dedup) {
      args.push('--dedup')
      args.push(options.dedup)
    }
    if (options.include) {
      args.push('--include')
      args.push(options.include)
    }
    if (options.json) args.push('--json')
    if (options.merge) args.push('--merge')
    if (options.output_all) args.push('--output-all')
    if (options.pairs) args.push('--pairs')
    if (options.scsi) args.push('--scsi')
    if (options.tree) {
      args.push('--tree')
      args.push(options.tree)
    }
    if (options.all) args.push('--all')
    if (options.bytes) args.push('--bytes')
    if (options.nodeps) args.push('--nodeps')
    if (options.exclude) {
      args.push('--exclude')
      exclude.forEach(function(opt) {
        args.push(opt)
      })
    }
    if (options.fs) args.push('--fs')
    if (options.ascii) args.push('--ascii')
    if (options.list) args.push('--list')
    if (options.perms) args.push('--perms')
    if (options.noheadings) args.push('--noheadings')
    if (options.output) {
      args.push('--output')
      exclude.forEach(function(opt) {
        args.push(opt)
      })
    }
    if (options.paths) args.push('--paths')
    if (options.raw) args.push('--raw')
    if (options.topology) args.push('--topology')
    if (options.width) {
      args.push('--width')
      args.push(options.width)
    }
    if (options.sort) {
      args.push('--sort')
      args.push(options.sort)
    }
    if (options.shell) args.push('--shell')
    if (options.zoned) args.push('--zoned')
    if (options.sysroot) {
      args.push('--sysroot')
      args.push(options.sysroot)
    }

    const res = await bufferedSpawn('lsblk', args)
    const stdout = JSON.parse(res.stdout)
    return stdout
  } catch (error) {
    throw error
  }
}

function filterBlock (blocks, regexp) {
  return filter(blocks, function (b) {

  })
}
module.exports = { notExistsAsync, mkdirAsync, hex2dec, download, formatMessage, lsblk }
