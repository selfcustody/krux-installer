const { contextBridge, ipcRenderer } = require('electron')


contextBridge.exposeInMainWorld('kruxAPI',{
  async download_resource (resource) {
    await ipcRenderer.invoke(`download:resource`, resource)
  },
  async start_detect_device () {
    await ipcRenderer.invoke('usb:detection:start')
  },
  async stop_detect_device () {
    await ipcRenderer.invoke('usb:detection:stop')
  },
  async sdcard_action (options) {
    await ipcRenderer.invoke('sdcard:action', options)
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
  onDetectedDeviceFoundUsb(callback) {
    ipcRenderer.on('usb:detection:add', callback)
  },
  onDetectedDeviceRemovedUsb(callback) {
    ipcRenderer.on('usb:detection:remove', callback)
  },
  onDetectedDeviceChangedUsb(callback) {
    ipcRenderer.on('usb:detection:change', callback)
  },
  onStopMonitoringDeviceUsb(callback) {
    ipcRenderer.on('usb:detection:stop', callback)
  },
  onDetectedSDCardFound(callback) {
    ipcRenderer.on('sdcard:detection:add', callback)
  },
  onMountAction(callback) {
    ipcRenderer.on('sdcard:mount', callback)
  },
  onFirmwareWritedOnSDCard(callback) {
    ipcRenderer.on('sdcard:write:done', callback)
  }
})
