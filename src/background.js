'use strict'

import { app, protocol, BrowserWindow, ipcMain } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'

import request from 'request'
import { join } from 'path'
import { createWriteStream, exists, mkdir } from 'fs'

const isDevelopment = process.env.NODE_ENV !== 'production'

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

let win;

/*
 * Function to check if file or folder exists
 */
function notExistsAsync(p) {
  return new Promise((resolve) => {
    exists(p, function(exist) {
      if (!exist) resolve(true)
      resolve(false)
    })
  })
}

/*
 * Function to create folder 
 */
function mkdirAsync(p) {
  return new Promise((resolve, reject) => {
    console.log(`[ INFO ] krux | mkdir | ${p}`)
    mkdir(p, function(err) {
      if (err) reject(err)
      console.log(`[ INFO ] krux | mkdir | ${p} | DONE`)
      resolve()
    })
  })
}

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
    const __destination__ = join(__dirname, '..', 'dist_electron', options.filename)

    // options.filename can be 
    // - ktool-*
    // - maixpy_*/firmware.bin
    // - maixpy_*/kboot.kfpkg
    const notExist = await notExistsAsync(join(__dirname, '..', 'dist_electron', options.filename))
    
    if (!notExist) {
      console.log(`[ INFO ] krux | download | ${options.filename} | DONE`)
      win.webContents.send(options.sender, '100.00')
    } else {
      console.log(`[ INFO ] krux | download | ${options.filename}`)

      // if `/` is found, then create a new directory
      const __filename__ = options.filename.split('/')
      let disposition

      if (__filename__.length > 1) {  
        const dirNotExist = await notExistsAsync(join(__dirname, '..', 'dist_electron', __filename__[0]))
        if (dirNotExist) {
          await mkdirAsync(join(__dirname, '..', 'dist_electron', __filename__[0]))
        }
        disposition = `attachment; filename=${__filename__[1]}`
      } else {
        disposition = `attachment; filename=${__filename__[0]}`
      }

      // Create a new file
      const file = createWriteStream(__destination__)
      const req = request({
        url: `${baseUrl}/${options.filename}`,
        headers: {
          'Content-Disposition': disposition,
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

      req.pipe(file)
      req.on('response', function ( data ) {
        total = data.headers['content-length']
        percent = ((downloaded/total) * 100).toFixed(2)
        win.webContents.send(options.sender, percent)
      });
      req.on('data', function (chunk) {
        downloaded += chunk.length
        percent = ((downloaded/total) * 100).toFixed(2)
        if (percent === '100.00') {
          console.log(`[ INFO ] krux | download | ${options.filename} | DONE`)
        }
        win.webContents.send(options.sender, percent)
      })
      req.on('finish', () => {
        win.webContents.send(options.sender, 'done')
      })
      req.on('error', function(err) {
        win.webContents.send(options.sender, err)
      })
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
    handleDownload({
      filename: `ktool-${process.platform}`,
      sender: 'download:ktool:status'
    })
  )

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
