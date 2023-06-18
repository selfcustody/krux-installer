/// <reference path="../typings/index.d.ts"/>

import ElectronStore from 'electron-store'
import Base from './base'

/**
 * Extended class to serve as 'base' for handlers; they will
 * invoke ipcMain methods to comunicate with the BrowserWindow
 */
export default class Handler extends Base {

  protected storage: ElectronStore;
  protected ipcMain: Electron.IpcMain;

  constructor(name: KruxInstaller.DebugName, win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super(name)
    this.win = win
    this.storage = storage
    this.ipcMain = ipcMain
  }

  build (callback) {
    this.log(`building ipcMain.handle for '${this.name}'`)
    this.ipcMain.handle(`${this.name}`, async (_, options) => {
      await callback(options)
    })
  }

}
