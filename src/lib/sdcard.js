'use strict'

import Handler from './base'
import {
  copyFileAsync,
  sudoPromptAsync,
  detectSDCard,
  getBlockDeviceFilesystemType,
  mountSDCard,
  formatBytes
} from './utils'


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
   * handles sdcard detection
   *
   * @param platform: String
   */
  async onDetection () {
    try {
      const sdcard = await detectSDCard()
      const fstype = await getBlockDeviceFilesystemType(this.platform, sdcard)
      const data = {
        device: sdcard.device,
        size: formatBytes(sdcard.size),
        description: sdcard.description,
        isFAT32: fstype === 'dos',
        state: sdcard.mountpoints.length === 0 ? 'umounted' : 'mounted'
      }
      this.store('sdcard', data)
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
      this.send('window:log:info', `sdcard ${action}ing started for ${this.platform}`);
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
