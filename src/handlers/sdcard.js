import { copyFile } from 'fs'
import _ from 'lodash'
import bufferedSpawn from 'buffered-spawn'
import drivelist from 'drivelist'
import sudo from 'sudo-prompt'
import Handler from './base'

/**
 * Copy file in asynchronous manner
 *
 * @param origin<String>: the full path of origin file
 * @param destination<String>: the full path of destination file
 */
function copyFileAsync (origin, destination) {
  return new Promise(function(resolve, reject) {
    copyFile(origin, destination, function (err) {
      if (err) reject(err)
      resolve()
    });
  });
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
async function getBlockdeviceFilesystemType (platform, sdcard) {
  if (platform === 'linux') {
    const blockdevice = await getUnixBlockDevice(sdcard)
    return blockdevice.fsver
  } else if (platform === 'darwin') {
    throw new Error(`SDCardHandler: Filesystem type detection: ${platform} not implemented`)
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
    const { blockdevices } = await getUnixBlockDevices()
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

/**
 * Shows a dialog requiring the
 * system's administrador password to
 * execute privileged tasks (mounting)
 *
 * @param script<String>: the main script to run with sudo prompt
 */
function sudoPromptAsync (script) {
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


/*
 * Function to format the size in bytes
 *
 * found at https://stackoverflow.com/questions/15900485/correct-way-to-convert-size-in-bytes-to-kb-mb-gb-in-javascript#18650828
 */
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i]
}


/**
 * Class to handle SDCard actions
 *
 * Currently, only works with 'linux'
 * TODO: work in 'darwin'
 * TODO: work in 'win32'
 */
class SDCardHandler extends Handler {

  constructor (app, platform) {
    super(app)
    if (platform !== 'linux') {
      throw new Error(`SDCardHandler not implemented on '${platform}'`)
    } else {
      this.platform = platform
    }
  }

  /*
   * handles sdcard detection
   *
   * @param platform: String
   */
  async onDetection () {
    try {
      const sdcard = await detectSDCard()
      const fstype = await sdcardFilesystemType(this.platform, sdcard)
      const data = {
        device: sdcard.device,
        size: formatBytes(sdcard.size),
        description: sdcard.description,
        isFAT32: fstype === 'dos',
        state: sdcard.mountpoints.length === 0 ? 'umounted' : 'mounted'
      }
      const msg = [
        `found a ${data.state === 'umounted' ? 'n' : ''} `,
        `${data.fstype} ${data.size} SDCard at ${data.device}`
      ].join('')
      this.send('window:log:info', msg)
      this.send('sdcard:detection:add', data)
    } catch (error) {
      this.send('window:log:info', error.stack)
      this.send('sdcard:detection:add', { error: error.message })
    }
  }

  /*
   * handles sdcard mounting
   */
  async onAction (action) {
    if (action !== 'mount' && action !== 'umount') {
      throw new Error(`SDCardHandler ${action} isn't implemented`)
    }
    try {
      this.send('window:log:info', `sdcard ${action}ing started`);
      const sdcard = await detectSDCard()
      const result = await mountSDCard(this.platform, sdcard, action);
      this.send('window:log:info', `sdcard ${result.state} at ${result.mountpoint}`);
      this.send('sdcard:mount', result)
    } catch (error) {
      this.send('window:log:info', error.stack);
    }
  }

  async onWrite (origin, destination) {
    try {
      this.send('window:log:info', `starting write ${origin} -> ${destination}`)
      const result = await copyFileAsync(origin, destination);
      this.send('window:log:info', `${origin} copied to ${destination}`);
      this.send('sdcard:write:done', destination);
    } catch (error) {
      this.send('window:log:info', error.stack);
    }
  }
}

export default SDCardHandler
