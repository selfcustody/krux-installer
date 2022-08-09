'use strict'

import { app, protocol, BrowserWindow, ipcMain } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
import usbDetect from 'usb-detection'
import { filter } from 'lodash'
import { join } from 'path'
import { handleDownload, handleSDCard } from './lib/handlers'
import { hex2dec } from './lib/utils'

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
 * List of devices
 */
const VID_PID_DEVICES = [
  {
    alias: 'maixpy_m5stickv',
    vid: hex2dec('0403'),
    pid: hex2dec('6001')
  },
  {
    alias: 'maixpy_amigo/maixy_bit',
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

  // This IPCs will be called everytime when the method
  // `window.kruxAPI.download_resource` is executed inside App.vue
  ipcMain.handle('download:resource', async (_event, resource) => {
    await handleDownload(win, resource)
  })

  // This IPC will be called will be called everytime when the method
  // `window.kruxAPI.sdcard_action` is executed inside `App.vue`
  ipcMain.handle('sdcard:action', async (_event, args) => {
    const __args__ = Object.assign(args, { platform: process.platform })
    await handleSDCard(win, __args__)
  })

  // Now create window
  createWindow()
})

process.on('unhandledRejection', (reason, p) => {
  console.log('Unhandled Rejection:', reason, p)
});

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
