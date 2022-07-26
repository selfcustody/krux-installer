const { contextBridge, ipcRenderer } = require('electron')

async function downloadKtool (os) {
  const response = await ipcRenderer.invoke(`download:ktook:${os}`)
  console.log(response)
}
contextBridge.exposeInMainWorld('electronAPI',{
  download_ktool: downloadKtool
})
