import { createRequire } from 'module'
import App from '../../lib/app'
import Storage from '../../lib/storage'
import ChangePageHandler from '../../lib/change-page'
import DownloadResourcesHandler from '../../lib/download-resources'
import CheckResourcesHandler from '../../lib/check-resource'
import UnzipResourceHandler from '../../lib/unzip-resource'
import VerifyOfficialReleasesFetchHandler from '../../lib/verify-official-releases-fetch'
import VerifyOfficialReleasesHashHandler from '../../lib/verify-official-releases-hash'
import VerifyOfficialReleasesSignHandler from '../../lib/verify-official-releases-sign'
import StoreSetHandler from '../../lib/store-set'
import StoreGetHandler from '../../lib/store-get'
import VerifyOpensslHandler from '../../lib/verify-openssl'
import CheckIfItWillFlashHandler from '../../lib/check-if-it-will-flash'
import FlashHandler from '../../lib/flash'

const { version } = createRequire(import.meta.url)('../../package.json')
const kruxInstaller = new App(`KruxInstaller | v${version}`)

kruxInstaller.start(async ({ app, win, ipcMain}) => {
  // Create storage
  const storageBuilder = new Storage(app)
  const store = await storageBuilder.build()

  // Reset configurations
  store.set('device', 'Select device')
  store.set('version', 'Select version')
  store.set('versions', [])

  // Create download resource handler
  const changePage = new ChangePageHandler(win, store, ipcMain)
  changePage.build()

  // Create download resource handler
  const downloadResource = new DownloadResourcesHandler(win, store, ipcMain)
  downloadResource.build()

  // Create check resource handler
  const checkResource = new CheckResourcesHandler(win, store, ipcMain)
  checkResource.build()

  // Create unzip resource handler
  const unzipResource = new UnzipResourceHandler(win, store, ipcMain)
  unzipResource.build()

  // Create fetcher for newest official release handler
  const verifyOfficialReleasesFetch = new VerifyOfficialReleasesFetchHandler(win, store, ipcMain)
  verifyOfficialReleasesFetch.build()

  // Create handler for official release sha256.txt
  const verifyOfficialReleasesHash = new VerifyOfficialReleasesHashHandler(win, store, ipcMain)
  verifyOfficialReleasesHash.build()

  // Create handler for official release .sig and .pem handler
  const verifyOfficialReleasesSign = new VerifyOfficialReleasesSignHandler(win, store, ipcMain)
  verifyOfficialReleasesSign.build()

  // Create handler for verify existence of openssl
  const verifyOpenssl = new VerifyOpensslHandler(win, store, ipcMain)
  verifyOpenssl.build()

  // Create store setter handler
  const storeSet = new StoreSetHandler(win, store, ipcMain)
  storeSet.build()

  // Create store getter handler
  const storeGet = new StoreGetHandler(win, store, ipcMain)
  storeGet.build()

  // Create 'check if it will flash' handler
  const checkIfItWillFlashHandler = new CheckIfItWillFlashHandler(win, store, ipcMain)
  checkIfItWillFlashHandler.build()

  // Create flash' handler
  const flashHandler = new FlashHandler(win, store, ipcMain)
  flashHandler.build()

  // Create Wdio test handlers
  // if environment variable WDIO_ELECTRON equals 'true'
  if (process.env.TEST === 'true') {
    win.webContents.send('building ipcMain.handle for \'wdio-electron.app\'') 
    ipcMain.handle('wdio-electron.app', (_event, funcName, ...args) => {
      const appProp = app[funcName];
      if (typeof appProp === 'function') {
        return appProp.apply(app, args);
      }
      return appProp;
    });

    win.webContents.send('building ipcMain.handle for \'wdio-electron\'') 
    ipcMain.handle('wdio-electron', (_events, ...args) => {
      return {
        appData: app.getPath('appData'),
        documents: app.getPath('documents')
      }
    })
  } else { 
    win.webContents.send("skip build ipcMain.handle for 'wdio-electron.app'")  
    win.webContents.send("skip build ipcMain.handle for 'wdio-electron'") 
  }
})
