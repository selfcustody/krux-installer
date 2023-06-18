import Base from './base'

/**
 * Extend `Base` class for initializing KruxInstaller storage,
 * assigning `krux:wdio-test` to `name` property. 
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
export default class WdioTest extends Base {
      
  private ipcMain: Electron.IpcMain;

  constructor (app: Electron.App, ipcMain: Electron.IpcMain) {
    super('krux:wdio-test')
    this.app = app
    this.ipcMain = ipcMain
  }

  /*
   * Create `wdio-electron` and `wdio-electron.app` ipcMain handlers`
   */
  build (): void {
    if (process.env.WDIO_ELECTRON === 'true') {
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
          if (!this.app[propName]) reject(`property or method ${propName} is not valid`)
          try {
            let result
            if (typeof this.app[propName] === 'function') {
              result = this.app[propName].apply(this.app, Array.prototype.slice.call(args, 1))
              this.log(result)
            } else {
              result = this.app[propName]
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
  }
} 
