import usbDetect from 'usb-detection'
import Handler from './base'

/*
 * List of devices as hexadecimal
 * vendor ids and product ids
 */
const DEVICES = [
  {
    alias: 'maixpy_m5stickv',
    vid: parseInt('0403', 16),
    pid: parseInt('6001', 16)
  },
  {
    alias: 'maixpy_amigo/maixy_bit',
    vid: parseInt('0403', 16),
    pid: parseInt('6010', 16)
  },
  {
    alias: 'maixpy_dock',
    vid: parseInt('1a86', 16),
    pid: parseInt('7523', 16)
  }
];

class UsbDetectionHandler extends Handler {

  constructor (app) {
    super(app)
    this.isActive = false
    this.device = null
  }

  /*10yy*
   * activate
   *
   * activate usb detection and
   * set isActive to true
   */
  activate () {
    usbDetect.startMonitoring()
    this.isActive = true
  }

  /**
   * detect
   *
   * detect if usb device was plugged in to computer
   * and check if its vendor and product ids (vid and pid)
   * are from implemented maixpy devices.
   *
   * If usbdetection started and the implemented device is
   * connected, send 'add' or 'remove' listeners to
   * window application
   */
   detect () {
    if (this.isActive) {
      DEVICES.forEach( (device) => {
        ['add', 'remove'].forEach( (action) => {
          const detection = `${action}:${device.vid}:${device.pid}`
          usbDetect.on(detection, (d) => {
            const message = `device: ${d.deviceName}/${d.manufacturer} on ttyUSB${d.locationId} ${action}ed`
            const data = Object.assign(d, {
              alias: device.alias,
              status: action
            })
            this.send('window:log:info', message)
            this.send('usb:detection', data)
          })
        })
      })
    } else {
      throw new Error('UsbDetectionHandler is not active')
    }
  }

  /*
   * deactivate
   *
   * Stop usb detection and send
   * information to window, if necessary
   */
  deactivate () {
    if (this.isActive) {
      usbDetect.stopMonitoring()
      this.Active = false
      win.webContents.send('window:log:info', 'Stopped usb detection')
    }
  }

}

export default UsbDetectionHandler
