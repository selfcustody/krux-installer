const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('KruxInstaller', {
  client: {
    async started () {
      await ipcRenderer.invoke('window-started')
    },
    onLog(callback) {
      ipcRenderer.on('window:log:info', callback)
    }
  },
  download: {
    async resource (options) {
      await ipcRenderer.invoke('download-resource', options)
    },
    onData(callback) {
      ipcRenderer.on('download-resource:data', callback)
    },
    onSuccess(callback) {
      ipcRenderer.on('download-resource:success', callback)
    },
    onError(callback) {
      ipcRenderer.on('download-resource:error', callback)
    }
  },
  check: {
    async resource (options) {
      await ipcRenderer.invoke('check-resource', options)
    },
    onSuccess(callback) {
      ipcRenderer.on('check-resource:success', callback)
    },
    onError(callback) {
      ipcRenderer.on('check-resource:error', callback)
    }
  },
  unzip: {
    async resource (options) {
      await ipcRenderer.invoke('unzip-resource', options)
    },
    onData(callback) {
      ipcRenderer.on('unzip-resource:data', callback)
    },
    onSuccess(callback) {
      ipcRenderer.on('unzip-resource:success', callback)
    },
    onError(callback) {
      ipcRenderer.on('unzip-resource:error', callback)
    }
  },
  version: {
    async set(value) {
      await ipcRenderer.invoke('store-set', { key: 'version', value: value })
    },
    async get() {
      await ipcRenderer.invoke('store-get', { key: 'version' })
    },
    onSet(callback) {
      ipcRenderer.on('store-set:version', callback)
    },
    onGet(callback) {
      ipcRenderer.on('store-get:version', callback)
    }
  },
  device: {
    async set(value) {
      await ipcRenderer.invoke('store-set', { key: 'device', value: value })
    },
    async get() {
      await ipcRenderer.invoke('store-get', { key: 'device' })
    },
    onSet(callback) {
      ipcRenderer.on('store-set:device', callback)
    },
    onGet(callback) {
      ipcRenderer.on('store-get:device', callback)
    }
  },
  os: {
    async get() {
      await ipcRenderer.invoke('store-get', { key: 'os' })
    },
    onGet(callback) {
      ipcRenderer.on('store-get:os', callback)
    }
  },
  isMac10: {
    async get() {
      await ipcRenderer.invoke('store-get', { key: 'isMac10' })
    },
    onGet(callback) {
      ipcRenderer.on('store-get:isMac10', callback)
    }
  },
  resources: {
    async check(resource) {
      await ipcRenderer.invoke('check-resource', resource)
    },
    onSuccess(callback) {
      ipcRenderer.on('check-resource:success', callback)
    }
  },
  resourcesPath: {
    async get() {
      await ipcRenderer.invoke('store-get', { key: 'resources' })
    },
    onGet(callback) {
      ipcRenderer.on('store-get:resources', callback)
    }
  },
  hash: {
    async verify() {
      await ipcRenderer.invoke('verify-official-releases-hash')
    },
    onSuccess(callback) {
      ipcRenderer.on('verify-official-releases-hash:success', callback)
    },
    onError(callback) {
      ipcRenderer.on('verify-official-releases-hash:error', callback)
    }
  },
  signature: {
    async verify(options) {
      await ipcRenderer.invoke('verify-official-releases-sign', options)
    },
    onSuccess(callback) {
      ipcRenderer.on('verify-official-releases-sign:success', callback)
    },
    onError(callback) {
      ipcRenderer.on('verify-official-releases-sign:error', callback)
    }
  },
  signature_command: {
    async get() {
      await ipcRenderer.invoke('store-get', { key: 'signature-command' })
    },
    onGet(callback) {
      ipcRenderer.on('store-get:signature-command', callback)
    }
  },
  official_releases: {
    async fetch() {
      await ipcRenderer.invoke('verify-official-releases-fetch')
    },
    onSuccess(callback) {
      ipcRenderer.on('verify-official-releases-fetch:success', callback)
    },
    onError(callback) {
      ipcRenderer.on('verify-official-releases-fetch:error', callback)
    }
  },
  flash: {
    async firmware () {
      await ipcRenderer.invoke('flash')
    },
    onData(callback) {
      ipcRenderer.on('flash:data', callback)
    },
    onError(callback) {
      ipcRenderer.on('flash:error', callback)
    },
    onSuccess(callback) {
      ipcRenderer.on('flash:success', callback)
    }
  },
  openssl: {
    async check () {
      await ipcRenderer.invoke('verify-openssl')
    },
    onError(callback) {
      ipcRenderer.on('verify-openssl:error', callback)
    },
    onSuccess(callback) {
      ipcRenderer.on('verify-openssl:success', callback)
    }
  }
  // async list_serialport () {
  //  await ipcRenderer.invoke('serialport:list')
  // },
  // async sdcard_action (options) {
  //  await ipcRenderer.invoke('sdcard:action', options)
  // },
  // async set_sdcard(value) {
  //   await ipcRenderer.invoke('store:set', { key: 'sdcard', value: value })
  // },
  // async get_sdcard() {
  //   await ipcRenderer.invoke('store:get', { key: 'sdcard' })
  //},
  // onListSerialport(callback) {
  //   ipcRenderer.on('serialport:list', callback)
  // },
  // onSerialportSelected(callback) {
  //   ipcRenderer.on('store:get:device', callback)
  // },
  // onDetectedSDCardSuccess(callback) {
  //   ipcRenderer.on('sdcard:detection:success', callback)
  // },
  // onDetectedSDCardError(callback) {
  //   ipcRenderer.on('sdcard:detection:error', callback)
  // },
  // onMountAction(callback) {
  //   ipcRenderer.on('sdcard:mount', callback)
  // },
  // onMountActionError(callback) {
  //   ipcRenderer.on('sdcard:mount:error', callback)
  // },
  //onFirmwareCopied(callback) {
  //  ipcRenderer.on('sdcard:action:copy_firmware_bin:done', callback)
  //},
  //onVerifiedOS(callback) {
  //  ipcRenderer.on('os:verify:done', callback)
  //},
  // onSetSdcard(callback) {
  //   ipcRenderer.on('store:set:sdcard', callback)
  // },
  // onGetSdcard(callback) {
  //   ipcRenderer.on('store:get:sdcard', callback)
  // },
});
