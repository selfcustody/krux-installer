/// <reference path="../typings/index.d.ts"/>

import { release } from 'node:os'
import { dirname, join } from 'node:path'
import { app, BrowserWindow, shell, ipcMain } from 'electron'
import Base from './base'

/**
 * Extend `Base` class for initializing KruxInstaller application,
 * assigning `krux:app` to `name`property. 
 * 
 * Once `start` method is called, it returns the following objects:
 * 
 * - `app: Electron.App`;
 * - `ipcMain: Electron.IpcMain`
 * - `win: Electron.BrowserWindow`
 * 
 * @example
 * ```
 * import { version } from '../package.json'
 * const myapp = new App(`MyApp | v${version}`)
 * myapp.start(() =>)
 * ``` 
 * @see Electron.App
 * @see Electron.IpcMain
 * @see Electron.BrowserWindow
 */
export default class App extends Base {

  /**
   * The window title
   */
  private title: string;

  constructor (title: string) {
    super('krux:app')
    this.title = title
    this.setupEnvironment()
    this.setupOpenssl()
    this.setupRelease()
    this.setupNotifications()
    this.setupSingleInstanceLock()
  }

  /**
   * Setup environment variables specific to application: 
   *   - `DIST`: where renderer distribuition files are placed
   *   - `DIST_ELECTRON`: where main process distribuition files are placed
   *   - `PUBLIC`: where "public" files are placed
   *   - `WDIO_ELECTRON`: if the context is for test or not
   */
  setupEnvironment (): void {
    /* The built directory structure
     *
     * ├─┬ dist-electron
     * │ ├─┬ main
     * │ │ └── index.js    > Electron-Main
     * │ └─┬ preload
     * │   └── index.js    > Preload-Scripts
     * ├─┬ dist
     * │ └── index.html    > Electron-Renderer
     */
    process.env.DIST_ELECTRON = join(__dirname, '..')
    process.env.DIST = join(process.env.DIST_ELECTRON, '../dist')
    process.env.PUBLIC = process.env.VITE_DEV_SERVER_URL
      ? join(process.env.DIST_ELECTRON, '../public')
      : process.env.DIST

    // Remove electron security warnings
    // This warning only shows in development mode
    // Read more on https://www.electronjs.org/docs/latest/tutorial/security
    // process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true'
    
    this.log('Application environment')
    this.log(`  PORTABLE_EXECUTABLE_FILE:         : ${process.env.PORTABLE_EXECUTABLE_FILE}`)
    this.log(`  DIST                              : ${process.env.DIST}`)
    this.log(`  DIST_ELECTRON                     : ${process.env.DIST_ELECTRON}`)
    this.log(`  PUBLIC                            : ${process.env.PUBLIC}`) 
    this.log(`  TEST                              : ${process.env.TEST}`)
    this.log(`  ELECTRON_DISABLE_SECURITY_WARNINGS: ${process.env.DIST}`)
  }

  /**
   * This will disable GPU Acceleration for Windows 7
   */
  private setupRelease (): void {
    if (release().startsWith('6.1')) {
      this.log('Disabling GPU Acceleration')
      app.disableHardwareAcceleration()
    }
  }

  /**
   * Set application name for Windows 10+ notifications
   */
  private setupNotifications (): void {
    if (process.platform === 'win32') { 
      this.log('Setting application name for Windows notifications')
      app.setAppUserModelId(app.getName())
    }
  }

  /**
   * Setup single instance lock
   */ 
  private setupSingleInstanceLock (): void { 
    if (!app.requestSingleInstanceLock()) { 
      this.log('Requesting single instance lock')
      app.quit()
      process.exit(0)
    }
  }

  /**
   * Check if platform (darwin or win32)
   * needs and additional configuration
   * to add openssl binary
   */
  private setupOpenssl (): void {
    this.log(`Adding openssl in ${process.platform} environment variable PATH`)
    const openssls = []
    let separator = ''

    if (process.platform === 'linux') {
      this.log('  no need for add')
    } else if (process.platform === 'darwin' ) {
      separator = ':'
      const _env = (process.env.PATH as string).split(separator)
      if (_env.indexOf('/usr/local/opt/openssl/bin') === -1) {
        openssls.push('/usr/local/opt/openssl/bin')
      }
      if (_env.indexOf('/System/Library/OpenSSL') === -1) {
        openssls.push('/System/Library/OpenSSL')
      }
    } else if (process.platform === 'win32') {
      separator = ';'
      const _env = (process.env.PATH as string).split(separator)
      
      // This path only will exist
      // when build occurs
      // inside github-actions
      const __opensslBinDir =  join(process.env.DIST, '..', '..', 'extraResources', 'OpenSSL', 'bin')

      if (_env.indexOf(__opensslBinDir) === -1) {
        openssls.push(__opensslBinDir)
      }
      
    }
    for (let i in openssls) {
      this.log(`  adding ${openssls[i]} to PATH`)
      process.env.PATH += `${separator}${openssls[i]}`
    }
  }

  /**
   * Configure app listeners:
   * - `app.on('window-all-closed')`;
   * - `app.on('activate')`;
   * - `app.on('second-instance')`;
   * 
   * And invoke `this.create` when app is ready.
   * @returns KruxInstaller.StartedApp  
   */ 
  public start (callback: any): void {
    app.on('window-all-closed', () => {
      console.log('All windows closed: quiting')
      if (process.platform !== 'darwin') app.quit()
    })

    app.on('activate', () => {
      this.log('Checking existence of other windows')
      const allWindows =  Electron.BrowserWindow.getAllWindows()
      if (allWindows.length) {
        allWindows[0].focus()
      } else {
        this.create()
      }
    })

    app.on('second-instance', () => {
      this.log('Trying to opening a second instance')
      if (this.win) {
        // Focus on the main window if the user tried to open another
        if (this.win.isMinimized()) {
          this.win.restore()
        }
        this.win.focus()
      }
    })

    app.whenReady().then(() => {
      this.log('App ready')
      this.create()
      callback({ app: app, win: this.win, ipcMain: ipcMain })
    })
  }

  /**
   * Create application when ready. Do not all it directly.
   * @see start
   */
  private create (): void {   
    this.log('Creating app')
    const preload = join(__dirname, '../preload/index.js')
    const url = process.env.VITE_DEV_SERVER_URL
    const indexHtml = join(process.env.DIST, 'index.html')
    const icon = join(process.env.PUBLIC, 'favicon.ico')
    
    this.log('Application variables')
    this.log(`  preload   : ${preload}`)
    this.log(`  url       : ${url}`)
    this.log(`  index.html: ${indexHtml}`)
    this.log(`  title     : ${this.title}`)
    this.log(`  icon      : ${icon}`)
    
    this.log('Creating Browser Window')
    this.win = new BrowserWindow({
      width: 840,
      height: 640,
      title: this.title,
      icon: icon,
      show: false,
      webPreferences: {
        preload,
        // Warning: Enable nodeIntegration and  disable contextIsolation is not secure in production
        // Consider using contextBridge.exposeInMainWorld
        // Read more on https://www.electronjs.org/docs/latest/tutorial/context-isolation
        nodeIntegration: false,
        contextIsolation: true,
      },
    })

    if (process.env.VITE_DEV_SERVER_URL) { // electron-vite-vue#298 
      this.log(`loading ${url}`)
      this.win.loadURL(url)
      // Open devTool if the app is not packaged
      this.win.webContents.openDevTools()
    } else {
      this.log(`loading ${indexHtml}`)
      this.win.loadFile(indexHtml)
    }

    // Test actively push message to the Electron-Renderer
    this.win.webContents.on('did-finish-load', () => {
      this.log('Finished loading')
      const msg = `${this.title} running`
      this.log(msg)
    })

    // Make all links open with the browser, not with the application
    this.win.webContents.setWindowOpenHandler(({ url }) => {
      if (url.startsWith('https:')) {
        this.log(`Opening external ${url} on browser`)
        shell.openExternal(url)
      }
      return { action: 'deny' }
    })

    this.log('showing window')
    this.win.show()
    // win.webContents.on('will-navigate', (event, url) => { }) #344
  }
}
