'use strict'
import { join } from 'path'
import { app, protocol, BrowserWindow, ipcMain } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
import {
  handleDownload,
  handleSDCard,
  handleUsbDetection,
  handleOSVerify
} from './lib/handlers'

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

  // This IPC will be called everytime when the method
  // `window.kruxAPI.detect_usb()` is exected inside App.vue
  ipcMain.handle('usb:detection', handleUsbDetection(win))

  // This IPCs will be called everytime when the method
  // `window.kruxAPI.download_resource` is executed inside App.vue
  ipcMain.handle('download:resource', handleDownload(win))

  // This IPC will be called will be called everytime when the method
  // `window.kruxAPI.sdcard_action` is executed inside `App.vue`
  ipcMain.handle('sdcard:action', handleSDCard(win))

  // This IPC will be called will be called everytime when the method
  // `window.kruxAPI.verify_os` is executed inside `App.vue`
  ipcMain.handle('os:verify', handleOSVerify(win))

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }

  win.webContents.send('window:log:info', 'Krux installer v.0.01 started')
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {

  handleUsbDetection(win, 'stop')

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

  // Now create window
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        handleUsbDetection(win, 'stop')
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      handleUsbDetection(win, 'stop')
      app.quit()
    })
    process.on('SIGINT', function() {
      handleUsbDetection(win, 'stop')
      process.exit(0)
    })
  }
}


process.on('unhandledRejection', (reason, p) => {
  p.catch((error) => console.error(error.stack))
});
