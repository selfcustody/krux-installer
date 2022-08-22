import { SerialPort } from 'serialport'
import { filter, includes } from 'lodash'
import Handler from './base'

/*
 * List of devices as hexadecimal
 * vendor ids and product ids
 */

const MAIXPY_M5STICKV_AMIGO_BIT_PID = '0403'
const MAIXPY_DOCK_PID = '1a86'

const MAIXPY_M5STICKV_VID = '6001'
const MAIXPY_AMIGO_BIT_VID= '6010'
const MAIXPY_DOCK_VID = '7523'

const MAIXPY_M5STICKV_ALIAS = 'maixpy_m5stickv'
const MAIXPY_AMIGO_BIT_ALIAS = 'maixpy_amigo/maixy_bit'
const MAIXPY_DOCK_ALIAS = 'maixpy_dock'

class SerialportHandler extends Handler {

  constructor (win, store) {
    super(win)
    this.store = store
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
   async list () {
    try {
      const ports = await SerialPort.list()
      const kruxs = filter(ports, function(o) {
        // maixpy_m5sticv
        if (o.vendorId === '0403' && o.productId === '6001') {
          o.devices = ['maixpy_m5stickv']
          o.message = 'use this if you are using maixpy_m5stickv'
          return o
        }
        // maixpy_bit
        if (o.vendorId === '0403' && o.productId === '6010' && o.path === '/dev/ttyUSB0') {
          o.devices = ['maixpy_bit']
          o.message = 'use this if you are using maixpy_bit'
          return o
        }
        // maixpy_amigo
        if (o.vendorId === '0403' && o.productId === '6010' && o.path === '/dev/ttyUSB1') {
          o.devices = ['maixpy_amigo_tft', 'maixpy_amigo_ips']
          o.message = 'use this if you are using maixpy_amigo_tft or maixpy_amigo_ips'
          return o
        }
        // maixpy_amigo
        if (o.vendorId === '7523' && o.productId === '1a86') {
          o.devices = ['maixpy_dock']
          o.message = 'use this if you are using maixpy_dock'
          return o
        }
      })
      kruxs.forEach((k) => {
        const msg = `found ${k.pnpId} from ${k.manufacturer} at ${k.path} (${k.vendorId}:${k.productId})`
        this.send('window:log:info', msg)
      })
      this.send('serialport:list', kruxs)
    } catch (error) {
      this.send('window:log:info', error.stack)
      console.log(error)
    }
  }

  select(device) {
    this.store.set('device', device)
    this.send('serialport:selected', device)
  }

}

export default SerialportHandler
