const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  scanFolder: (folder) => ipcRenderer.invoke('scan-folder', folder),
  setFaceLabel: (db, cid, name) =>
    ipcRenderer.invoke('set-face-label', db, cid, name),
  getFaceLabel: (db, cid) =>
    ipcRenderer.invoke('get-face-label', db, cid),
});
