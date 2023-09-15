// src/electron-env.d.ts(need create)
export { }
declare global {
  interface Window {
    // Expose some Api through preload script
    api?: any;
    ipcRenderer: import('electron').IpcRenderer
  }
}
