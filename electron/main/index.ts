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
  app.store = await storageBuilder.build()

  // Reset configurations
  app.store.set('device', 'Select device')
  app.store.set('version', 'Select version')
  app.store.set('versions', [])

  // Create download resource handler
  const changePage = new ChangePageHandler(win, app.store, ipcMain)
  changePage.build()

  // Create download resource handler
  const downloadResource = new DownloadResourcesHandler(win, app.store, ipcMain)
  downloadResource.build()

  // Create check resource handler
  const checkResource = new CheckResourcesHandler(win, app.store, ipcMain)
  checkResource.build()

  // Create unzip resource handler
  const unzipResource = new UnzipResourceHandler(win, app.store, ipcMain)
  unzipResource.build()

  // Create fetcher for newest official release handler
  const verifyOfficialReleasesFetch = new VerifyOfficialReleasesFetchHandler(win, app.store, ipcMain)
  verifyOfficialReleasesFetch.build()

  // Create handler for official release sha256.txt
  const verifyOfficialReleasesHash = new VerifyOfficialReleasesHashHandler(win, app.store, ipcMain)
  verifyOfficialReleasesHash.build()

  // Create handler for official release .sig and .pem handler
  const verifyOfficialReleasesSign = new VerifyOfficialReleasesSignHandler(win, app.store, ipcMain)
  verifyOfficialReleasesSign.build()

  // Create handler for verify existence of openssl
  const verifyOpenssl = new VerifyOpensslHandler(win, app.store, ipcMain)
  verifyOpenssl.build()

  // Create store setter handler
  const storeSet = new StoreSetHandler(win, app.store, ipcMain)
  storeSet.build()

  // Create store getter handler
  const storeGet = new StoreGetHandler(win, app.store, ipcMain)
  storeGet.build()

  // Create 'check if it will flash' handler
  const checkIfItWillFlashHandler = new CheckIfItWillFlashHandler(win, app.store, ipcMain)
  checkIfItWillFlashHandler.build()

  // Create flash' handler
  const flashHandler = new FlashHandler(win, app.store, ipcMain)
  flashHandler.build()

  // Create Wdio test handlers
  // if environment variable WDIO_ELECTRON equals 'true'
  if (process.env.NODE_ENV === 'test') {
    const _electron = await import('electron')
    ipcMain.handle("wdio-electron.execute", (_, script, args) => {
      return new Function(`return (${script}).apply(this, arguments)`)(_electron, ...args);
    })
  }
})
