'use strict'

import { copyFile, readFile } from 'fs'
import { userInfo } from 'os'
import _ from 'lodash'
import bufferedSpawn from 'buffered-spawn'
import * as drivelist from 'drivelist'
import sudo from 'sudo-prompt'

/**
 * Copy file in asynchronous manner
 *
 * @param origin<String>: the full path of origin file
 * @param destination<String>: the full path of destination file
 */
export function copyFileAsync (origin, destination) {
  return new Promise(function(resolve, reject) {
    copyFile(origin, destination, function (err) {
      if (err) reject(err)
      resolve()
    });
  });
}

/**
 * Copy file in asynchronous manner
 *
 * @param origin<String>: the full path of origin file
 * @param destination<String>: the full path of destination file
 */
export function readFileAsync (origin, options) {
  return new Promise(function(resolve, reject) {
    readFile(origin, options, function (err, data) {
      if (err) reject(err)
      resolve(data)
    });
  });
}

/*
 * Detects if a SD card is inserted in any OS
 *
 */
export async function detectSDCard () {
  const drives = await drivelist.list()
  const removables = _.reject(drives, { isSystem: true })
  if (removables.length > 0) {
    return removables[0]
  } else {
    throw Error("SDCardHandler: no device detected")
  }
}


/*
 * Unix utility for more information
 * about inserted disks
 *
 * @param sdcard<Object>: the detected sdcard
 */
function getUnixBlockDevice (sdcard) {
  return new Promise(function(resolve, reject) {
    bufferedSpawn('lsblk', [
      '--bytes',
      '--paths',
      '--output-all',
      '--json'
    ], function(err, stdout, stderr) {
      if (err) reject(error)
      const { blockdevices } = JSON.parse(stdout)
      const sdcards = _.filter(blockdevices, { path: sdcard.device })
      if (sdcards.length > 0) {
        resolve(sdcards[0])
      } else {
        const error = new Error(`SDCardHandler: Filesystem type detection: no device ${sdcard.device} found`)
        reject(error)
      }
    }
    )
  })
}


/*
 * Windows utility for more information
 * about inserted disks
 */
function getWin32BlockDevices (sdcard) {
  return new Promise(function(resolve, reject) {
    // https://stackoverflow.com/questions/46853070/get-filesystem-type-with-node-js
    bufferedSpawn(`fsutil fsinfo volumeinfo ${sdcard.device}`,
      function (err, stdout, stderr) {
        if (err) reject(err)
        resolve(stdout)
      }
    )
  })
}

/*
 * Detect filesystem type of a sdcard
 *
 * TODO: implement 'darwin' and 'win32'
 * @param platform
 * @param sdcard (see detectSDCard)
 */
export async function getBlockDeviceFilesystemType (platform, sdcard) {
  if (platform === 'linux') {
    const blockdevice = await getUnixBlockDevice(sdcard)
    return blockdevice.fsver
  } else if (platform === 'darwin') {
    throw new Error(`Filesystem type detection: ${platform} not implemented`)
  } else if (platform === 'win32') {
    const sdcard = await getWin32BlockDevices(sdcard)
    return sdcard.pttype
  } else {
    throw new Error(`SDCard Filesystem type detection: ${platform} not implemented`)
  }
}


/*
 * Gets them mounted partitions of a block device
 *
 * @param platform<String>: the name of operational system
 * @param sdcard<Object>: the sdcard
 */
async function getBlockPartitions (platform, sdcard) {
  if (platform === 'linux') {
    const partition = await getUnixBlockDevice(sdcard)
    return partition.children[0]
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

/**
 * Shows a dialog requiring the
 * system's administrador password to
 * execute privileged tasks (mounting)
 *
 * @param script<String>: the main script to run with sudo prompt
 */
export function sudoPromptAsync (script) {
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
 * @param platform<String>: the string representing the OS
 * @param sdcard<Object> (see detectSDCard)
 * @param action<String>: the action ('mount' || 'umount')
 */
export async function mountSDCard (platform, sdcard, action='mount') {
  if (action !== 'mount' && action !== 'umount') {
    throw new Error(`SDCard mount: ${action} notimplemented`);
  }

  if (platform === 'linux') {
    const partition = await getBlockPartitions(platform, sdcard);
    const { name, uuid } = partition;
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
      await sudoPromptAsync(script);
    }

    if (action === 'umount') {
      const script = [
        `umount ${mountpoint}`,
        `rm -rf ${mountpoint}`
      ].join(' && ');
      await sudoPromptAsync(script);
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


/*
 * Function to format the size in bytes
 *
 * found at https://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript#18650828
 */
export function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}
