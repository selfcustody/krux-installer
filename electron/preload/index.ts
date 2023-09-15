const { contextBridge, ipcRenderer } = require('electron')

ipcRenderer.on('main-process-message', (_event, args) => {
  console.log(args)
})

if (process.env.TEST === 'true') {
  const validChannels = [
    'wdio-electron',
    'wdio-electron.app'
  ];
  const invoke = async (channel, ...data) => {
    if (!validChannels.includes(channel)) {
        throw new Error(`Channel "${channel}" is invalid`);
    }
    if (!process.env.WDIO_ELECTRON) {
        throw new Error('Electron APIs can not be invoked outside of WDIO');
    }
    return ipcRenderer.invoke(channel, ...data);
  };
  contextBridge.exposeInMainWorld('wdioElectron', {
    app: {
        invoke: (funcName, ...args) => invoke('wdio-electron.app', funcName, ...args),
    },
    custom: {
        invoke: (...args) => invoke('wdio-electron', ...args),
    }
  });
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
