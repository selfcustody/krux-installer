/// <reference path="../typings/index.d.ts"/>
/// <reference path="../node_modules/electron-store/index.d.ts" />
/// <reference path="../node_modules/wdio-electron-service/dist/main.d.ts" />

import Base from './base'
import electron, { BrowserWindow, dialog } from 'electron';
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
export default class WdioTestHandler extends Base {
      
  protected app: Electron.App;
  protected ipcMain: Electron.IpcMain;

  constructor (app: Electron.App, ipcMain: Electron.IpcMain) {
    super('krux:wdio:e2e');
    this.app = app
    this.ipcMain = ipcMain
  }

  /*
   * Create `wdio-electron` and `wdio-electron.app` ipcMain handlers`
   */
  build (): void {
    
  }
}