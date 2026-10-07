const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

let mainWindow;
let splashWindow;
let pythonProcess;
let nextjsProcess;

function createSplashScreen() {
  splashWindow = new BrowserWindow({
    width: 600,
    height: 400,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: true
    }
  });
  splashWindow.loadFile('splash.html');
}

function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    show: false,
    webPreferences: {
      nodeIntegration: true
    }
  });
  // Load the local Next.js server
  mainWindow.loadURL('http://localhost:3000');

  mainWindow.once('ready-to-show', () => {
    if (splashWindow) {
      splashWindow.close();
    }
    mainWindow.show();
  });
}

function startBackgroundServices() {
  console.log('Starting Local Python FastAPI Server (AI & Telemetry)...');
  
  // 1. Spawn Local Python Backend
  const backendDir = path.join(__dirname, '../ApisLM_Local_Backend');
  // In production, we would use bundled python or a frozen .exe of the backend
  pythonProcess = spawn('python', ['main_api.py'], { cwd: backendDir });
  
  pythonProcess.stdout.on('data', (data) => console.log(`[Python]: ${data}`));
  pythonProcess.stderr.on('data', (data) => console.error(`[Python ERR]: ${data}`));

  console.log('Starting Next.js Production Server (Cloud Tenant Dashboard)...');
  
  // 2. Spawn Next.js Dashboard
  const frontendDir = path.join(__dirname, '../ApisLM_Workspace/cloud-tenant-dashboard');
  // Usually this would be built into static files, but for the orchestrator we run 'npm start'
  nextjsProcess = spawn(/^win/.test(process.platform) ? 'npm.cmd' : 'npm', ['run', 'start'], { cwd: frontendDir });
  
  nextjsProcess.stdout.on('data', (data) => console.log(`[Next.js]: ${data}`));
  nextjsProcess.stderr.on('data', (data) => console.error(`[Next.js ERR]: ${data}`));

  // 3. Health Check Poller
  // Wait for Next.js to boot up before showing the main window
  const checkServer = setInterval(() => {
    http.get('http://localhost:3000', (res) => {
      if (res.statusCode === 200) {
        clearInterval(checkServer);
        createMainWindow();
      }
    }).on('error', (e) => {
      // Server not ready yet...
    });
  }, 1000);
}

app.whenReady().then(() => {
  createSplashScreen();
  startBackgroundServices();
});

// --- Graceful Shutdown Logic ---
app.on('window-all-closed', () => {
  console.log("Shutting down background services...");
  
  if (pythonProcess) {
    pythonProcess.kill();
  }
  
  if (nextjsProcess) {
    nextjsProcess.kill();
  }
  
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
