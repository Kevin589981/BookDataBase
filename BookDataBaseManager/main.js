import { app, BrowserWindow } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const isDev = process.env.NODE_ENV === 'development';

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      webSecurity: false // 添加这个选项以避免CORS问题
    },
    icon: path.join(__dirname, 'public/booklogo.png')
  });

  if (isDev) {
    win.loadURL('http://localhost:5173');
    win.webContents.openDevTools();
  } else {
    win.loadFile(path.join(__dirname, 'dist/index.html'));
    // 生产环境不自动打开开发者工具，用户可以按F12手动打开
  }

  // 添加错误处理和调试信息
  win.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.log('Failed to load:', errorCode, errorDescription);
  });

  win.webContents.on('dom-ready', () => {
    console.log('DOM is ready');
    // 只在开发环境注入调试脚本
    if (isDev) {
      win.webContents.executeJavaScript(`
        console.log('Electron: DOM ready, checking Vue app...');
        
        // 检测环境
        console.log('Environment detection:');
        console.log('- window.process:', !!window.process);
        console.log('- window.require:', !!window.require);
        console.log('- navigator.userAgent:', navigator.userAgent);
        
        setTimeout(() => {
          const app = document.getElementById('app');
          console.log('App element:', app);
          console.log('App innerHTML length:', app ? app.innerHTML.length : 'App element not found');
          
          // 检查后端连接
          fetch('http://localhost:8000', { 
            method: 'GET',
            mode: 'no-cors'
          })
            .then(() => console.log('✅ 后端服务器连接正常'))
            .catch(err => {
              console.error('❌ 后端服务器连接失败:', err.message);
              console.error('请确保后端服务器运行在 http://localhost:8000');
            });
        }, 2000);
      `);
    }
  });

  win.webContents.on('did-finish-load', () => {
    console.log('Page finished loading');
  });
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