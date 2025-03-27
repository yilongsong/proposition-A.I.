const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    backgroundColor: '#1e1e1e',  // Match dark theme
    vibrancy: 'dark',           // Add dark vibrancy effect
    titleBarStyle: 'default',   // Use default title bar
    trafficLightPosition: { x: 20, y: 20 }, // Adjust traffic light position
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      sandbox: false // Allow preload script to access node modules
    }
  });

  win.loadFile(path.join(__dirname, 'renderer/index.html'));
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});