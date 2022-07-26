'use strict'

import { app, protocol, BrowserWindow, ipcMain } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'

import request from 'request'
import { join } from 'path'
import { createWriteStream } from 'fs'

const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

let win;

function handleDownload (url, filename, webContent) {
  return async function () {
    try {
      const destination_path = join(__dirname, '..', 'dist_electron', filename)
      const file = createWriteStream(destination_path)
      const req = request({
        url: url,
        headers: {
          'Content-Disposition': `attachment; filename=${filename}`,
          'User-Agent': `Chrome/${process.versions.chrome}`,
          'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Accept-Encoding': 'gzip, deflate, br'
        },
         gzip: true
      })

      let downloaded = 0
      let total = 0
      let percent = 0

      win.webContents.send(webContent, 'starting')

      req.pipe(file)
      req.on('response', function ( data ) {
        total = data.headers['content-length']
        console.log(`${url}: ${total}`)
        percent = ((downloaded/total) * 100).toFixed(2)
        win.webContents.send(webContent, percent)
      });
      req.on('data', function (chunk) {
        downloaded += chunk.length
        percent = ((downloaded/total) * 100).toFixed(2)
        win.webContents.send(webContent, percent)
      })
      req.on('finish', () => {
        win.webContents.send(webContent, 'done')
      })
      req.on('error', function(err) {
        win.webContents.send(webContent, err)
      })
    } catch (error) {
      console.log(error)
    }
  }
}

async function createWindow() {
  // Create the browser window.
  win = new BrowserWindow({
    width: 768,
    height: 512,
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
  // `window.kruxAPI.download_ktool(os)` is executed inside App.vue
  ipcMain.handle(
    `download:ktool:${process.platform}`, 
    handleDownload(
      `https://github.com/odudex/krux_binaries/raw/main/ktool-${process.platform}`,
      `ktool-${process.platform}`,
      'download:ktool:status'
    )
  )

  // This IPC will be called everytime when the method
  // `window.kruxAPI.download_firmware(device)` is executed inside App.vue
  ipcMain.handle(
    'download:firmware:maixpy_m5stickv', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_m5stickv/firmware.bin',
      'firmware.bin',
      'download:firmware:status'
    )
  )

  ipcMain.handle(
    'download:firmware:maixpy_amigo_ips', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_amigo_ips/firmware.bin',
      'firmware.bin',
      'download:firmware:status'
    )
  )

  ipcMain.handle(
    'download:firmware:maixpy_bit', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_bit/firmware.bin',
      'firmware.bin',
      'download:firmware:status'
    )
  )

  ipcMain.handle(
    'download:firmware:maixpy_bit_ov5642', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_bit_ov5642/firmware.bin',
      'firmware.bin',
      'download:firmware:status'
    )
  )

  ipcMain.handle(
    'download:firmware:maixpy_dock', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_dock/firmware.bin',
      'firmware.bin',
      'download:firmware:status'
    )
  )


  // This IPC will be called everytime when the method
  // `window.kruxAPI.download_kboot(device)` is executed inside App.vue
  ipcMain.handle(
    'download:kboot:maixpy_m5stickv', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_m5stickv/kboot.kfpkg',
      'kboot.kfpkg',
      'download:kboot:status'
    )
  )

  ipcMain.handle(
    'download:kboot:maixpy_amigo_ips', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_amigo_ips/kboot.kfpkg',
      'kboot.kfpkg',
      'download:kboot:status'
    )
  )

  ipcMain.handle(
    'download:kboot:maixpy_bit', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_bit/kboot.kfpkg',
      'kboot.kfpkg',
      'download:kboot:status'
    )
  )

  ipcMain.handle(
    'download:kboot:maixpy_bit_ov5642', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_bit_ov5642/kboot.kfpkg',
      'kboot.kfpkg',
      'download:kboot:status'
    )
  )

  ipcMain.handle(
    'download:kboot:maixpy_dock', 
    handleDownload(
      'https://github.com/odudex/krux_binaries/raw/main/maixpy_dock/kboot.kfpkg',
      'kboot.kfpkg',
      'download:kboot:status'
    )
  )
  // Now create window
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
