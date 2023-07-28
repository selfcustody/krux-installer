/// <reference path="../typings/index.d.ts"/>
/// <reference path="../node_modules/electron-store/index.d.ts" />

import ElectronStore from 'electron-store';
import Handler from './handler'
import { createRequire } from 'node:module'
import electron, { app, BrowserWindow, dialog, ipcMain } from 'electron';

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
      this.log('Configuring \'wdio-electron\' handler')
      createRequire(import.meta.url)('./node_modules/wdio-electron-service/main')
      this.ipcMain.handle('wdio-electron', (_events, ...args) => {
        return {
          appData: this.app.getPath('appData'),
          documents: this.app.getPath('documents')
        }
      })
    })
  }
} 