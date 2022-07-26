const { contextBridge, ipcRenderer } = require('electron')


contextBridge.exposeInMainWorld('kruxAPI',{
  async download_ktool (os) {
    await ipcRenderer.invoke(`download:ktool:${os}`)
  },
  async download_firmware (device) {
    await ipcRenderer.invoke(`download:firmware:${device}`)
  },
  async download_kboot (device) {
    await ipcRenderer.invoke(`download:kboot:${device}`)
  },
  onDownloadedKtoolStatus(callback) {
    ipcRenderer.on('download:ktool:status', callback)
  },
  onDownloadedFirmwareStatus(callback) {
    ipcRenderer.on('download:firmware:status', callback)
  },
  onDownloadedKbootStatus(callback) {
    ipcRenderer.on('download:kboot:status', callback)
  }
})
