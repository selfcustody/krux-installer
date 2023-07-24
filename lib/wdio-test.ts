/// <reference path="../typings/index.d.ts"/>
/// <reference path="../node_modules/electron-store/index.d.ts" />

import ElectronStore from 'electron-store';
import Handler from './handler'

/**
 * Extend `Base` class for initializing KruxInstaller storage,
 * assigning `krux:wdio:e2e` to `name` property. 
 * 
 * Since electron 20
 * the approach descibed in
 * https://webdriver.io/docs/wdio-electron-service/#example-configuration
 * do not works.
 * The 'solution' was copy the contents from node-modules/wdio-electron-service/dist/main
 * and reconfigure some variables
 * 
 * @see Electron.IpcMain
 */
export default class WdioTestHandler extends Handler {
      
  protected app: Electron.App;

  constructor (app: Electron.App, win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:wdio:e2e', win, storage, ipcMain);
    this.app = app
  }

  /*
   * Create `wdio-electron` and `wdio-electron.app` ipcMain handlers`
   */
  build (): void {
    super.build(async (options: any) => {
      try {
        if (process.env.WDIO_ELECTRON === undefined && process.env.WDIO_ELECTRON == 'true') {
          this.log(`building ipcMain.handle for ${this.name}`)
          this.log('Configuring \'wdio-electron\' handler')

          this.ipcMain.handle('wdio-electron', (_events, ...args) => {
            return {
              appData: this.app.getPath('appData'),
              documents: this.app.getPath('documents')
            }
          })

          this.log('Configuring \'wdio-electron.app\' handler')
          this.ipcMain.handle('wdio-electron.app', (_event, propName, ...args) => {
            return new Promise((resolve, reject) => {
              if (!(this.app as any)[propName]) reject(`property or method ${propName} is not valid`)
              try {
                let result: any
                if (typeof (this.app as any)[propName] === 'function') {
                  result = (this.app as any)[propName].apply(this.app, Array.prototype.slice.call(args, 1))
                  this.log(result)
                } else {
                  result = (this.app as any)[propName]
                }
                resolve(result)
              } catch (error) {
                reject(error)
              }
            })
          })
        } else {
          this.log(`not building any ipcMain.handle for ${this.name}`)
        }
      } catch (error) {
        this.log(error as any)
      }
    })
  }
} 
