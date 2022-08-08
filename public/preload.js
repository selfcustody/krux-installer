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
  async start_detect_sdcard () {
    await ipcRenderer.invoke('sdcard:detection:start')
  },
  async start_mount_sdcard () {
    await ipcRenderer.invoke('sdcard:mount:start')
  },
  async stop_mount_sdcard () {
    await ipcRenderer.invoke('sdcard:mount:stop')
  },
  async start_write_firmware_to_sdcard (resource, sdcard) {
    await ipcRenderer.invoke(`sdcard:write:start`, { resource: resource, sdcard: sdcard })
  },
  onLogLevelInfo(callback) {
    ipcRenderer.on('window:log:info', callback)
  },
  onDownloadedKtoolStatus(callback) {
    ipcRenderer.on('download:ktool:status', callback)
  },
  onDownloadedFirmwareStatus(callback) {
    ipcRenderer.on('download:firmware:status', callback)
  },
  onDownloadFirmwareDone(callback) {
    ipcRenderer.on('download:firmware:status:done', callback)
  },
  onDownloadedKbootStatus(callback) {
    ipcRenderer.on('download:kboot:status', callback)
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
  onMountedSDCard(callback) {
    ipcRenderer.on('sdcard:mount:add', callback)
  },
  onUmountedSDCard(callback) {
    ipcRenderer.on('sdcard:mount:remove', callback)
  },
  onFirmwareWritedOnSDCard(callback) {
    ipcRenderer.on('sdcard:write:done', callback)
  }
})
