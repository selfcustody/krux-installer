const { contextBridge, ipcRenderer } = require('electron')

ipcRenderer.on('main-process-message', (_event, args) => {
  console.log(args)
})

if (process.env.WDIO_ELECTRON) {
  require('wdio-electron-service/preload')
}

contextBridge.exposeInMainWorld('api', {
  async invoke (channel: string, data: string): Promise<any> {
    await ipcRenderer.invoke(channel, data)
  }, 
  onData (channel: string, callback: any): void {
    ipcRenderer.on(`${channel}:data`, callback)
  },
  onSuccess (channel: string, callback: any): void {
    ipcRenderer.on(`${channel}:success`, callback)
  },
  onceSuccess (channel: string, callback: any): void {
    ipcRenderer.once(`${channel}:success`, callback)
  },
  onError (channel: string, callback: any): void {
    ipcRenderer.on(`${channel}:error`, callback)
  }
})
