'use strict'

import { app, protocol, BrowserWindow, ipcMain } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
import usbDetect from 'usb-detection'
import { filter } from 'lodash'
import { join } from 'path'
import {
  notExistsAsync,
  mkdirAsync,
  download,
  hex2dec,
  formatMessage,
  formatBytes,
  detectSDCard,
  sdcardFilesystemType
} from './lib/utils'

const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

/*
 * Define win variable as the app window, as visible in various methods
 */
let win;

/*
 * Function to handle downloads
 * when user select to build or flash
 * prebuiltin binaries
 */
function handleDownload (
  options,
  baseUrl='https://github.com/odudex/krux_binaries/raw/main/'
) {
  return async function () {
    win.webContents.send(options.sender, 'starting')

    // If __dirname/resources isnt exists
    // create it
    const resources = join(__dirname, '..', 'resources')
    const resourcesNotExists = await notExistsAsync(resources)
    if (resourcesNotExists) {
      win.webContents.send('window:log:info', `creating directory ${resources}`)
      await mkdirAsync(resources)
      win.webContents.send('window:log:info', `directory ${resources} created`)
    }

    // Now start the downloading and creation file
    const __destination__ = join(resources, options.filename)

    // options.filename can be
    // - ktool-*
    // - maixpy_*/firmware.bin
    // - maixpy_*/kboot.kfpkg
    const notExist = await notExistsAsync(__destination__)

    if (!notExist) {
      win.webContents.send('window:log:info', `${options.filename} already downloaded`)
      win.webContents.send(options.sender, '100.00')
    } else {
      win.webContents.send('window:log:info', `downloading ${baseUrl}/${options.filename}`)

      // if `/` string is found in filename
      // (could be `maixpy_*/kboot.kfpkg` or `maixpy_*/firmware.bin`
      // then create a new directory
      // in `__dirname/resources`
      // if not have an `/`
      // (could be ktool-*)
      // put it in `__dirname/resources`
      try {
        const __filename__ = options.filename.split('/')
        let disposition

        if (__filename__.length > 1) {
          const d = join(resources, __filename__[0])
          const dirNotExist = await notExistsAsync(d)
          if (dirNotExist) {
            const p = join(d)
            win.webContents.send('window:log:info', `creating directory ${d}`)
            await mkdirAsync(d)
            win.webContents.send('window:log:info', `directory ${d} created`)
          }
          disposition = `attachment; filename=${__filename__[1]}`
        } else {
          disposition = `attachment; filename=${__filename__[0]}`
        }

        let downloaded = 0
        let total = 0
        let percent = 0

        download({
          destination: __destination__,
          url: `${baseUrl}/${options.filename}`,
          headers: {
            'Content-Disposition': disposition,
            'User-Agent': `Chrome/${process.versions.chrome}`,
          },
          onResponse: function (data) {
            total = data.headers['content-length']
            percent = ((downloaded/total) * 100).toFixed(2)
            win.webContents.send('window:log:info', `${baseUrl}/${options.filename} has ${total} bytes`)
            win.webContents.send(options.sender, percent)
          },
          onData: function (chunk) {
            downloaded += chunk.length
            percent = ((downloaded/total) * 100).toFixed(2)
            win.webContents.send(options.sender, percent)
            if (percent === '100.00') {
              win.webContents.send('window:log:info', `${options.filename} downloaded`)
            }
          },
          onError: function(err) {
            win.webContents.send('window:log:info', err.message)
            win.webContents.send(options.sender, err)
          }
        })
      } catch (error) {
        win.webContents.send('window:log:info', error.stack)
      }
    }
  }
}


/*
 * List of devices
 */
const VID_PID_DEVICES = [
  {
    alias: 'maixpy_m5stickv',
    vid: hex2dec('0403'),
    pid: hex2dec('6001')
  },
  {
    alias: 'maixpy_amigo_ips/maixpy_bit/maixy_bit_ov5642',
    vid: hex2dec('0403'),
    pid: hex2dec('6010')
  },
  {
    alias: 'maixpy_dock',
    vid: hex2dec('1a86'),
    pid: hex2dec('7523')
  }
]

/*
 * Says if usb detecation is activated
 */
let isUsbDetectActivate = false


/*
 * handles usb detection according devices
 */
async function handleStartUSBdetection () {
  usbDetect.startMonitoring();
  isUsbDetectActivate = true
  VID_PID_DEVICES.forEach(function (device, i) {
    ['add', 'remove', 'change'].forEach(function(action) {
      usbDetect.on(`${action}:${device.vid}:${device.pid}`, function (d) {
        win.webContents.send('window:log:info', formatMessage(d, action))
        win.webContents.send(`usb:detection:${action}`, device.alias)
      })
    })
  })
}

/*
 * handles stop usb detection
 */
function handleStopUSBdetection () {
  if (isUsbDetectActivate) {
    usbDetect.stopMonitoring()
    isUsbDetectActivate = false
    win.webContents.send('window:log:info', 'Stopped usb detection')
    win.webContents.send('usb:detection:stop', true)
  }
}

/*
 * handles sdcard detection
 */
async function handleSDCardDetection () {
  try {
    win.webContents.send('window:log:info', 'sdcard detection started')
    const sdcard = await detectSDCard()
    let fstype = await sdcardFilesystemType(process.platform, sdcard)
    if (fstype === 'dos') {
      fstype = 'FAT32'
    } else {
      fstype = '(not) FAT32'
    }
    const data = {
      device: sdcard.device,
      size: formatBytes(sdcard.size),
      description: sdcard.description,
      fstype: fstype,
      state: sdcard.mountpoints.length === 0 ? 'unmounted' : 'mounted'
    }
    const msg = `found a ${data.state === 'unmounted' ? 'n' : ''} ${data.fstype} ${data.size} SDCard at ${data.device}`
    win.webContents.send('window:log:info', msg)
    win.webContents.send('sdcard:detection:add', data)
  } catch (error) {
    win.webContents.send('window:log:info', error)
    win.webContents.send('sdcard:detection:add', { error: error.message })
  }
}

/*
 * Create the browser window
 */
async function createWindow() {
  win = new BrowserWindow({
    width: 768,
    height: 608,
    webPreferences: {

      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION || false,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION || true,
      enableRemoteModule: process.env.ELECTRON_NODE_INTEGRATION || false,
      preload: join(__static, 'preload.js')
    }
  })

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
  win.webContents.send('window:log:info', 'Krux installer v.0.01 started')
  win.webContents.send('window:log:info', 'page: main')
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  // This IPC will be called everytime when the method
  // `window.kruxAPI.detect_usb()` is exected inside App.vue
  ipcMain.handle('usb:detection:start', handleStartUSBdetection)
  ipcMain.handle('usb:detection:stop', handleStopUSBdetection)

  // This IPC will be called everytime when the method
  // `window.kruxAPI.download_ktool(os)` is executed inside App.vue
  ipcMain.handle(`download:ktool:${process.platform}`, handleDownload({
    filename: `ktool-${process.platform}`,
    sender: 'download:ktool:status'
  }))

  // This IPC will be called everytime when the method
  // `window.kruxAPI.download_<firmware | kboot>(device)` is executed inside App.vue
  const downloads = ['firmware.bin', 'kboot.kfpkg'];
  const devices = ['maixpy_m5stickv', 'maixpy_amigo_ips', 'maixpy_bit', 'maixpy_bit_ov5642', 'maixpy_dock'];
  downloads.forEach(function (bin){
    devices.forEach(function (device){
      const sender = bin.split('.')[0]
      const handler = handleDownload({
        filename: `${device}/${bin}`,
        sender: `download:${sender}:status`
      })
      ipcMain.handle(`download:${sender}:${device}`, handler)
    })
  })

  // This IPC will be called will be called everytime when the method
  // `window.kruxAPI.sdcard_detect` is executed inside `App.vue`
  ipcMain.handle('sdcard:detection:start', handleSDCardDetection)

  // Now create window
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        if (isUsbDetectActivate) usbDetect.stopMonitoring()
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      if (isUsbDetectActivate) usbDetect.stopMonitoring()
      app.quit()
    })
    process.on('SIGINT', function() {
      if (isUsbDetectActivate) usbDetect.stopMonitoring()
      process.exit(0)
    })
  }
}
