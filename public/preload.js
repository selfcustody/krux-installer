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
  async start_detect_device () {
    await ipcRenderer.invoke('usb:detection:start')
  },
  async stop_detect_device () {
    await ipcRenderer.invoke('usb:detection:stop')
  },
  onDownloadedKtoolStatus(callback) {
    ipcRenderer.on('download:ktool:status', callback)
  },
  onDownloadedFirmwareStatus(callback) {
    ipcRenderer.on('download:firmware:status', callback)
  },
  onDownloadedKbootStatus(callback) {
    ipcRenderer.on('download:kboot:status', callback)
  },
  onDetectedDeviceFoundUsb(callback) {
    ipcRenderer.on('usb:detection:found', callback)
  },
  onDetectedDeviceRemovedUsb(callback) {
    ipcRenderer.on('usb:detection:removed', callback)
  },
  onDetectedDeviceChangedUsb(callback) {
    ipcRenderer.on('usb:detection:change', callback)
  },
  onStopMonitoringDeviceUsb(callback) {
    ipcRenderer.on('usb:detection:stop', callback)
  }
})
