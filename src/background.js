'use strict'

/*
 * Import Standard libraries section
 */
import { join } from 'path'

/*
 * Import third party libraries
 */
import { app, protocol, BrowserWindow, ipcMain } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
import createDebug from 'debug'
import dotenv from 'dotenv'

/*
 * Debugger
 *
 * If the environment variable DEBUG is attributed to 'background'
 * (DEBUG=background yarn run electron:<serve|build>),
 * any of the messages will be displayed
 * only for this module
 */

const debug = createDebug('krux:background')

/*
 * Import local libraries section
 *
 * For first release, do not use sdcard yet,
 * because more research is needed to adapt situations for
 * windows and macos OS.
 */
import createStore from './lib/store'
import windowStarted from './lib/window-started'
import downloadResource from './lib/download-resource'
import checkResource from './lib/check-resource'
import unzipResource from './lib/unzip-resource'
import verifyOfficialReleasesFetch from './lib/verify-official-releases-fetch'
import verifyOfficialReleasesHash from './lib/verify-official-releases-hash'
import verifyOfficialReleasesSign from './lib/verify-official-releases-sign'
import verifyOpenssl from './lib/verify-openssl'
import storeSet from './lib/store-set'
import storeGet from './lib/store-get'
import flash from './lib/flash'
import { existsAsync } from './lib/utils/fs-async'
/*
 * Environment variables setup section
 */
debug('Checking NODE_ENV...')
if (!process.env.NODE_ENV) {
  debug('No NODE_ENV variable assigned')
  const env_path = join(__dirname, '..', '.env')

  debug(`Checking if a '${env_path}' file exists`)
  if (existsAsync(env_path)) {
    debug(`Assign envioronment files with '${env_path}'`)
    dotenv.config({ path: env_path })
  }
} else {
  debug(`NODE_ENV=${process.env.NODE_ENV}`)
}

const isDevelopment = process.env.NODE_ENV !== 'production'

/*
 * Protocol configuration:
 * Scheme must be registered before the app is ready
 */

const schemas = [{ scheme: 'app', privileges: { secure: true, standard: true } }]
debug('Assign privileged protocol schema:')
debug(`  scheme: ${schemas[0].scheme}`)
debug(`  privileges.secure: ${schemas[0].privileges.secure}`)
debug(`  privileges.standard: ${schemas[0].privileges.standard}`)
protocol.registerSchemesAsPrivileged(schemas)

/*
 * Toplevel variables definition:
 * - Define `win` variable to be visible in many situations
 * - Define `store` store variable to be visible in many situations:
 *   - `store` is a persistent memory in a file called `<configpath>/config.json`
 *   - `<configpath>` is defined in `src/lib/store.js` by `electron-store` lib
 */
let win

/*
 * Create the browser window
 */
async function createWindow() {

  const winOptions = {
    width: process.env.ELECTRON_NODE_WIDTH || 840,
    height: process.env.ELECTRON_NODE_HEIGHT || 608,
    webPreferences: {

      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION || false,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION || true,
      enableRemoteModule: process.env.ELECTRON_NODE_INTEGRATION || false,
      // eslint-disable-next-line no-undef
      preload: join(__static, 'preload.js')
    }
  }

  debug('Creating window')
  for (let opt in winOptions) {
    if (opt !== 'webPreferences') {
      debug(`  ${opt}: ${winOptions[opt]}`)
    } else {
      for (let p in winOptions[opt]) {
        debug(`  ${opt}.${p}: ${winOptions[opt][p]}`)
      }
    }
  }

  win = new BrowserWindow(winOptions)

  debug('Creating store')
  const store = await createStore(app)

  debug('Configuring Handlers')
  ipcMain.handle('window-started', windowStarted(win, store))
  ipcMain.handle('download-resource', downloadResource(win, store))
  ipcMain.handle('check-resource', checkResource(win, store))
  ipcMain.handle('unzip-resource', unzipResource(win, store))
  ipcMain.handle('verify-official-releases-fetch', verifyOfficialReleasesFetch(win, store))
  ipcMain.handle('verify-official-releases-hash', verifyOfficialReleasesHash(win, store))
  ipcMain.handle('verify-official-releases-sign', verifyOfficialReleasesSign(win, store))
  ipcMain.handle('verify-openssl', verifyOpenssl(win, store))
  ipcMain.handle('store-set', storeSet(win, store))
  ipcMain.handle('store-get', storeGet(win, store))
  ipcMain.handle('flash', flash(win, store))

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    debug('Loading the url of the dev server in development mode')
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) {
      debug('opening dev tools')
      win.webContents.openDevTools()
    }
  } else {
    debug('Creating \'app\' protocol')
    createProtocol('app')
    debug('Loading the index.html')
    win.loadURL('app://./index.html')
  }
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  debug('All windows closed')
  if (process.platform !== 'darwin') {
    debug('Quiting app')
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    debug('Activating app')
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
      debug('Installing Vue Devtools')
      await installExtension(VUEJS3_DEVTOOLS)
    } catch (e) {
      debug(`Vue Devtools failed to install:, ${e.toString()}`)
    }
  }

  // Check if platform (darwin or win32)
  // needs and additional configuration
  // to add openssl binary
  debug(`Adding openssl in ${process.platform} environment variable PATH`)
  const openssls = []
  let separator = ''

  if (process.platform === 'linux') {
    debug('  no need for add')
  } else if (process.platform === 'darwin' ) {
    separator = ':'
    const _env = process.env.PATH.split(separator)
    if (_env.indexOf('/usr/local/opt/openssl/bin') === -1) {
      openssls.push('/usr/local/opt/openssl/bin')
    }
    if (_env.indexOf('/System/Library/OpenSSL') === -1) {
      openssls.push('/System/Library/OpenSSL')
    }
  } else if (process.platform === 'win32') {
    separator = ';'
    const _env = process.env.PATH.split(separator)

    const vendor = join(__dirname, '..', 'extraResources', 'OpenSSL', 'bin')
    if (_env.indexOf(vendor === -1)) {
      openssls.push(vendor)
    }
  }
  for (let i in openssls) {
    debug(`  adding ${openssls[i]} to PATH`)
    process.env.PATH += `${separator}${openssls[i]}`
  }

  debug('App ready')
  // Now create window
  createWindow()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      debug(data)
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      debug('SIGTERM')
      app.quit()
    })
    process.on('SIGINT', function() {
      debug('SIGINT')
      process.exit(0)
    })
  }
}


process.on('unhandledRejection', (reason, p) => {
  debug(reason)
  p.catch(function(error) {
    debug(error.toString())
  })
})
