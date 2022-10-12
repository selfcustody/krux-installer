'use strict'
import { join } from 'path'
import { app, protocol, BrowserWindow, ipcMain } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
import createStore from './lib/store'
import {
  handleWindowStarted,
  handleVerifyOfficialReleases,
  handleVerifyOfficialReleasesHash,
  handleVerifyOfficialReleasesSign,
  handleUnzip,
  handleStoreSet,
  handleStoreGet,
  handleDownload,
  handleSDCard,
  handleSerialport,
  handleFlash
} from './lib/handlers'

const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

/*
 * Define win variable as the app window, as visible in various methods
 */
let win
let store

/*
 * Create the browser window
 */
async function createWindow() {
  win = new BrowserWindow({
    width: 840,
    height: 608,
    webPreferences: {

      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION || false,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION || true,
      enableRemoteModule: process.env.ELECTRON_NODE_INTEGRATION || false,
      // eslint-disable-next-line no-undef
      preload: join(__static, 'preload.js')
    }
  })

  // This IPC will be called everytime when the method
  // `window.kruxAPI.isStarted()` is executed inside App.vue
  ipcMain.handle('window:started', handleWindowStarted(win, store))

  // This IPC will be called everytime when the method
  // `window.kruxAPI.list_serialport` is exected inside App.vue
  ipcMain.handle('serialport:list', handleSerialport(win, store))

  // This IPCs will be called everytime when the method
  // `window.kruxAPI.download_resource` is executed inside App.vue
  ipcMain.handle('download:resource', handleDownload(win, store))

  // This IPCs will be called everytime when the method
  // `window.kruxAPI.unzip` is executed inside App.vue
  ipcMain.handle('zip:extract', handleUnzip(win, store))

  // This IPC will be called everytime when the method
  // `window.kruxAPI.sdcard_action` is executed inside `App.vue`
  ipcMain.handle('sdcard:action', handleSDCard(win, store))

  // This IPC will be called everytime when the method
  // `window.kruxAPI.verify_official_releases` is executed inside `App.vue`
  ipcMain.handle('official:releases:set', handleVerifyOfficialReleases(win, store))

  // This IPC will be called everytime when the method
  // `window.kruxAPI.verify_official_releases` is executed inside `App.vue`
  ipcMain.handle('official:releases:verify:hash', handleVerifyOfficialReleasesHash(win, store))

  // This IPC will be called everytime when the method
  // `window.kruxAPI.verify_official_releases` is executed inside `App.vue`
  ipcMain.handle('official:releases:verify:sign', handleVerifyOfficialReleasesSign(win, store))

  // These IPC will be act like Vuex store,
  // called everytime when the methods
  // `window.kruxAPI.set_version`
  // are executed inside `App.vue`
  ipcMain.handle('store:set', handleStoreSet(win, store))
  ipcMain.handle('store:get', handleStoreGet(win, store))

  // This IPC will be called everytime when the method
  // `window.kruxAPI.flash_firmware_to_device` is executed inside `App.vue`
  ipcMain.handle('flash:firmware', handleFlash(win, store))

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

  store.delete('device')
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    store = createStore(app)
    createWindow()
  }
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

  // Now create store
  store = createStore(app)

  // Now create window
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        store.delete('device')
        store.set('state', 'stopped')
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      store.delete('device')
      store.set('state', 'stopped')
      app.quit()
    })
    process.on('SIGINT', function() {
      store.delete('device')
      store.set('state', 'stopped')
      process.exit(0)
    })
  }
}


process.on('unhandledRejection', (reason, p) => {
  p.catch((error) => console.error(error.stack))
})
