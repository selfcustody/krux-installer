'use strict'

import { userInfo } from 'os'
import { join } from 'path'
import _ from 'lodash'
import bufferedSpawn from 'buffered-spawn'
import * as drivelist from 'drivelist'
import sudo from 'sudo-prompt'

import Handler from './base'
import { copyFileAsync } from './utils/fs-async'
import { formatBytes } from './utils/format'


/**
 * Class to handle SDCard actions
 *
 * Currently, only works with 'linux'
 * TODO: work in 'darwin'
 * TODO: work in 'win32'
 */
export default class SDCardHandler extends Handler {

  constructor (app, store, platform) {
    super(app)
    this.store = store
    if (platform !== 'linux') {
      throw new Error(`SDCardHandler not implemented on '${platform}'`)
    } else {
      this.platform = platform
    }
  }

  /*
   * Detects if a SD card is inserted in any OS
   *
   * @return Object: The object that describe a inserted sdcard
   */
  static async detect () {
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
  static async getBlockDevice (platform, sdcard) {
    if (platform === 'linux') {
      const cmd = 'lsblk'
      const arglist = ['--bytes', '--paths', '--output-all', '--json']
      const { stdout, stderr } = await bufferedSpawn(cmd, arglist)
      if (stderr !== null && stderr !== '') {
        throw new Error(`SDCardHandler: ${stdout}`)
      }
      const { blockdevices } = JSON.parse(stdout)
      const sdcards = _.filter(blockdevices, { path: sdcard.device })
      if (sdcards.length > 0) {
        return sdcards[0].children[0]
      } else {
        throw new Error(`SDCardHandler: Filesystem type detection: no device ${sdcard.device} found`)
      }
    } else if (platform === 'win32') {
      // TODO implement parser like
      // https://stackoverflow.com/questions/46853070/get-filesystem-type-with-node-js
      const cmd = 'fsutil'
      const arglist = ['fsinfo', 'volumeinfo', sdcard.device]
      const { stdout, stderr } = await bufferedSpawn(cmd, arglist)
      if (stderr !== null && stderr !== '') {
        throw new Error(`SDCardHandler: ${stdout}`)
      }
      throw new Error(`SDCardHandler: ${platform} not implemented`)
    } else if (platform === 'darwin') {
      throw new Error(`SDCardHandler: ${platform} not implemented`)
    }
  }


  /*
   * Shows a dialog requiring the
   * system's administrador password to
   * execute privileged tasks (mounting)
   *
   * @param script<String>: the main script to run with sudo prompt
   */
  static sudoPromptAsync (script) {
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
  static async act (platform, sdcard, action='mount') {
    if (action !== 'mount' && action !== 'umount') {
      throw new Error(`SDCard mount: ${action} notimplemented`);
    }

    if (platform === 'linux') {
      const device = await SDCardHandler.getBlockDevice(platform, sdcard)
      console.log(device)
      const name = device.name
      const uuid = device.uuid
      const username = userInfo().username;
      const usergid = userInfo().gid;
      const useruid = userInfo().uid;
      const umask = '0022'
      const mountpoint = `/run/media/${username}/${uuid}`;

      if (action === 'mount') {
        const script = [
          `mkdir -p ${mountpoint}`,
          `mount -o uid=${useruid},gid=${usergid},umask=${umask} -t vfat ${name} ${mountpoint}`
        ].join(" && ")
        await SDCardHandler.sudoPromptAsync(script);
      }

      if (action === 'umount') {
        const script = [
          `umount ${mountpoint}`,
          `rm -rf ${mountpoint}`
        ].join(' && ');
        await SDCardHandler.sudoPromptAsync(script);
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
   * handles sdcard detection
   *
   * @param platform: String
   */
  async onDetection () {
    try {
      const sdcard = await SDCardHandler.detect()
      const blk = await SDCardHandler.getBlockDevice(this.platform, sdcard)
      const data = {
        device: sdcard.device,
        size: formatBytes(sdcard.size),
        description: sdcard.description,
        pttype: blk.pttype === 'dos' ? 'FAT32' : 'not FAT32',
        state: sdcard.mountpoints.length === 0 ? 'umounted' : 'mounted'
      }
      this.store.set('sdcard', data)
      const msg = [
        `found ${data.state === 'umounted' ? 'an' : 'a'} `,
        data.state,
        `${data.fsver ? data.fsver : ''} ${data.size} SDCard at ${data.device}`
      ].join('')
      this.send('window:log:info', msg)
      this.send('sdcard:detection:success', data)
    } catch (error) {
      this.send('window:log:info', error.message)
      this.send('window:log:info', error.stack)
      this.send('sdcard:detection:error', error)
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
      this.send('window:log:info', `sdcard ${action}ing started for ${this.platform}`);
      const sdcard = await SDCardHandler.detect()
      const result = await SDCardHandler.act(this.platform, sdcard, action);
      this.send('window:log:info', `sdcard ${result.state} at ${result.mountpoint}`);
      this.send('sdcard:mount', result)
    } catch (error) {
      this.send('sdcard:mount:error', error)
      this.send('window:log:info', error.stack);
    }
  }

  async onCopyFirmwareBin () {
    try {
      const resources = this.store.get('resources')
      const version = this.store.get('version').split('tag/')[1]
      const sdcard = this.store.get('sdcard')
      const device = this.store.get('device')

      const firmwareBinPathOrig = join(resources, version, `krux-${version}`, device, 'firmware.bin')
      const firmwareBinPathDest = join(sdcard, 'firmware.bin')

      await copyFileAsync(firmwareBinPathOrig, firmwareBinPathDest);
      this.send('window:log:info', `copied ${firmwareBinPathOrig} to ${firmwareBinPathDest}`)
      this.send('sdcard:action:copy_firmware_bin:done', firmwareBinPathDest);
    } catch (error) {
      this.send('window:log:info', error.stack);
    }
  }
}
