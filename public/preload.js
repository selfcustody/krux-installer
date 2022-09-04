const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('kruxAPI',{
  async window_started () {
    await ipcRenderer.invoke('window:started', { state: 'running' })
  },
  async download_resource (options) {
    await ipcRenderer.invoke('download:resource', options)
  },
  async serialport (options) {
    await ipcRenderer.invoke('serialport:action', options)
  },
  async sdcard_action (options) {
    await ipcRenderer.invoke('sdcard:action', options)
  },
  async verify_os () {
    await ipcRenderer.invoke('os:verify')
  },
  async set_version(value) {
    await ipcRenderer.invoke('store:set', { key: 'version', value: value })
  },
  async get_version() {
    await ipcRenderer.invoke('store:get', { key: 'version' })
  },
  async set_action(value) {
    await ipcRenderer.invoke('store:set', { key: 'action', value: value })
  },
  async get_action() {
    await ipcRenderer.invoke('store:get', { key: 'action' })
  },
  async set_device(value) {
    await ipcRenderer.invoke('store:set', { key: 'device', value: value })
  },
  async get_device() {
    await ipcRenderer.invoke('store:get', { key: 'device' })
  },
  async set_sdcard(value) {
    await ipcRenderer.invoke('store:set', { key: 'sdcard', value: value })
  },
  async get_sdcard() {
    await ipcRenderer.invoke('store:get', { key: 'sdcard' })
  },
  async verify_hash() {
    await ipcRenderer.invoke('official:releases:verify:hash')
  },
  async verify_signature(options) {
    await ipcRenderer.invoke('official:releases:verify:sign', options)
  },
  async verify_official_releases() {
    await ipcRenderer.invoke('official:releases:set')
  },
  async unzip (options) {
    await ipcRenderer.invoke('zip:extract', options)
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
  onDownloadError(callback) {
    ipcRenderer.on('download:status:error', callback)
  },
  onSerialportList(callback) {
    ipcRenderer.on('serialport:list', callback)
  },
  onSerialportSelected(callback) {
    ipcRenderer.on('serialport:selected', callback)
  },
  onDetectedSDCardSuccess(callback) {
    ipcRenderer.on('sdcard:detection:success', callback)
  },
  onDetectedSDCardError(callback) {
    ipcRenderer.on('sdcard:detection:error', callback)
  },
  onMountAction(callback) {
    ipcRenderer.on('sdcard:mount', callback)
  },
  onMountActionError(callback) {
    ipcRenderer.on('sdcard:mount:error', callback)
  },
  onFirmwareCopied(callback) {
    ipcRenderer.on('sdcard:action:copy_firmware_bin:done', callback)
  },
  onVerifiedOS(callback) {
    ipcRenderer.on('os:verify:done', callback)
  },
  onSetVersion(callback) {
    ipcRenderer.on('store:set:version', callback)
  },
  onGetVersion(callback) {
    ipcRenderer.on('store:get:version', callback)
  },
  onSetAction(callback) {
    ipcRenderer.on('store:set:action', callback)
  },
  onGetAction(callback) {
    ipcRenderer.on('store:get:action', callback)
  },
  onSetDevice(callback) {
    ipcRenderer.on('store:set:device', callback)
  },
  onGetDevice(callback) {
    ipcRenderer.on('store:get:device', callback)
  },
  onSetSdcard(callback) {
    ipcRenderer.on('store:set:sdcard', callback)
  },
  onGetSdcard(callback) {
    ipcRenderer.on('store:get:sdcard', callback)
  },
  onVerifyOfficialReleases(callback) {
    ipcRenderer.on('official:releases:get', callback)
  },
  onVerifiedHash(callback) {
    ipcRenderer.on('official:releases:verified:hash', callback)
  },
  onVerifiedHashError(callback) {
    ipcRenderer.on('official:releases:verified:hash:error', callback)
  },
  onVerifiedSign(callback) {
    ipcRenderer.on('official:releases:verified:sign', callback)
  },
  onVerifiedSignError(callback) {
    ipcRenderer.on('official:releases:verified:sign:error', callback)
  },
  onUnzipped(callback) {
    ipcRenderer.on('zip:extract:done', callback)
  },
  onUnzipProgress(callback) {
    ipcRenderer.on('zip:extract:progress', callback)
  },
  onUnzipError(callback) {
    ipcRenderer.on('zip:extract:error', callback)
  }
})
