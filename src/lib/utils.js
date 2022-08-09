const { userInfo } = require('os');
const bufferedSpawn = require('buffered-spawn');
const { createWriteStream, exists, mkdir, copyFile } = require('fs')
const request = require('request')
const drivelist = require('drivelist')
const sudo = require('sudo-prompt');
const _ = require('lodash')
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
 */
async function detectSDCard () {
  const drives = await drivelist.list()
  const removables = _.reject(drives, { isSystem: true })
  if (removables.length > 0) {
    return removables[0]
  } else {
    throw Error("SDCard Detection: no device detected")
  }
}


function __lsblk__ () {
  return new Promise(function(resolve, reject) {
    bufferedSpawn('lsblk', [
      '--bytes',
      '--paths',
      '--output-all',
      '--json'
    ], function(err, stdout, stderr) {
      if (err) reject(error)
      const obj = JSON.parse(stdout)
      resolve(obj)
    })
  })
}

/*
 * Detect filesystem type of a sdcard
 *
 * @param platform
 * @param sdcard (see detectSDCard)
 */
async function sdcardFilesystemType (platform, sdcard) {
  if (platform === 'linux') {
    const { blockdevices } = await __lsblk__()
    const sdcards = _.filter(blockdevices, { path: sdcard.device })
    if (sdcards.length > 0) {
      const sdcard = sdcards[0]
      return sdcard.pttype
    } else {
      throw new Error(`SDCard Filesystem type detection: no device ${sdcard.device} found`)
    }
  } else if (platform === 'darwin') {
    throw new Error(`SDCard Filesystem type detection: ${platform} not implemented`)
  } else if (platform === 'win32') {
    // https://stackoverflow.com/questions/46853070/get-filesystem-type-with-node-js
    //const fsutil = await bufferedSpawn(`fsutil fsinfo volumeinfo ${sdcard.device}`
    throw new Error(`SDCard Filesystem type detection: ${platform} not implemented`)
  } else {
    throw new Error(`SDCard Filesystem type detection: ${platform} not implemented`)
  }
}

async function sdcardPartitions (platform, sdcard) {
  if (platform === 'linux') {
    const { blockdevices } = await __lsblk__()
    const sdcards = _.filter(blockdevices, { path: sdcard.device })
    if (sdcards.length > 0) {
      return sdcards[0].children
    } else {
      throw new Error(`SDCard Filesystem type detection: no device ${sdcard.device} found`)
    }
  } else if (platform === 'darwin') {
    throw new Error(`SDCard Filesystem type detection: ${platform} not implemented`)
  } else if (platform === 'win32') {
    // https://stackoverflow.com/questions/46853070/get-filesystem-type-with-node-js
    //const fsutil = await bufferedSpawn(`fsutil fsinfo volumeinfo ${sdcard.device}`
    throw new Error(`SDCard Filesystem type detection: ${platform} not implemented`)
  } else {
    throw new Error(`SDCard Filesystem type detection: ${platform} not implemented`)
  }
}

function sudoAsync (script) {
  return new Promise(function (resolve, reject) {
    const options = {
      name: 'Krux Installer'
    };
    sudo.exec(script, options, function (err, stdout, stderr){
      if (err) reject(err);
      if (stderr) reject(stderr);
      resolve();
    })
  });
}

/*
 * Mounts an Sdcard
 *
 * @param sdcard (see detectSDCard)
 */
async function mountSDCard (platform, sdcard, action='mount') {
  if (action !== 'mount' && action !== 'umount') {
    throw new Error(`SDCard mount: ${action} notimplemented`);
  }

  if (platform === 'linux') {
    const partitions = await sdcardPartitions(platform, sdcard);
    const { name, uuid } = partitions[0];
    const username = userInfo().username;
    const usergid = userInfo().gid;
    const useruid = userInfo().uid;
    const umask = '0755'
    const mountpoint = `/run/media/${username}/${uuid}`;

    if (action === 'mount') {
      const script = [
        `mkdir -p ${mountpoint}`,
        `mount -o uid=${useruid},gid=${usergid},umask=0022 -t vfat ${name} ${mountpoint}`
      ].join(" && ")
      await sudoAsync(script);
    }

    if (action === 'umount') {
      const script = [
        `umount ${mountpoint}`,
        `rm -rf ${mountpoint}`
      ].join(' && ');
      await sudoAsync(script);
    }

    return { state: `${action}ed`, mountpoint: mountpoint }

  } else if (platform === 'darwin') {
    throw new Error(`SDCard Filesystem mount: ${platform} not implemented`)
  } else if (platform === 'win32') {
    throw new Error(`SDCard Filesystem mount: ${platform} not implemented`)
  } else {
    throw new Error(`SDCard Filesystem mount: ${platform} not implemented`)
  }
}

function copyFileAsync (origin, destination) {
  return new Promise(function(resolve, reject) {
    copyFile(origin, destination, function (err) {
      if (err) reject(err)
      resolve()
    });
  });
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

module.exports = {
  notExistsAsync,
  mkdirAsync,
  download,
  formatBytes,
  detectSDCard,
  sdcardFilesystemType,
  mountSDCard,
  copyFileAsync
}
