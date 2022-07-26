const { contextBridge, ipcRenderer } = require('electron')

async function downloadKtoolLinux () {
  await ipcRenderer.invoke('download:ktool:linux')
}

contextBridge.exposeInMainWorld('kruxAPI',{
  download_ktool_linux: downloadKtoolLinux
})
