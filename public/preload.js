const { contextBridge, ipcRenderer } = require('electron')


contextBridge.exposeInMainWorld('kruxAPI',{
  async download_resource (resource) {
    await ipcRenderer.invoke(`download:resource`, resource)
  },
  async usb_detection (action) {
    await ipcRenderer.invoke('usb:detection', action)
  },
  async sdcard_action (options) {
    await ipcRenderer.invoke('sdcard:action', options)
  },
  async verify_os () {
    await ipcRenderer.invoke('os:verify')
  },
  onLogLevelInfo(callback) {
    ipcRenderer.on('window:log:info', callback)
  },
  onDownloadStatus(callback) {
    ipcRenderer.on('download:status', callback)
  },
  onDownloadDone(callback) {
    ipcRenderer.on('download:status:done', callback)
  },
  onDetectedDevice(callback) {
    ipcRenderer.on('usb:detection', callback)
  },
  onDetectedSDCardFound(callback) {
    ipcRenderer.on('sdcard:detection:add', callback)
  },
  onMountAction(callback) {
    ipcRenderer.on('sdcard:mount', callback)
  },
  onFirmwareWritedOnSDCard(callback) {
    ipcRenderer.on('sdcard:write:done', callback)
  },
  onVerifiedOS(callback) {
    ipcRenderer.on('os:verify:done', callback)
  }
})
