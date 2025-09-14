import { app, shell, BrowserWindow, ipcMain, nativeTheme } from 'electron'
import { join } from 'path'
import { spawn } from 'child_process'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import 'dotenv/config'
import 'fix-path'
import * as logfire from 'logfire'
import { logger } from '../shared/logger'

// Configure Logfire
logfire.configure({
  serviceName: 'penpal-main',
  serviceVersion: app.getVersion(),
  console: true
})

// Backend process management
let backendProcess: ReturnType<typeof spawn> | null = null
let backendUrl: string | null = null

function startBackend(): void {
  // In development, __dirname is src/main, in production it's out/main
  // We need to go up to the project root and then into src/backend
  const projectRoot = is.dev
    ? join(__dirname, '../..') // src/main -> project root
    : join(__dirname, '../..') // out/main -> project root
  const backendPath = join(projectRoot, 'src', 'backend')

  logger.info('Starting backend process', { backendPath })

  backendProcess = spawn('uv', ['run', 'python', '-m', 'penpal_backend'], {
    cwd: backendPath,
    stdio: ['pipe', 'pipe', 'pipe']
  })

  backendProcess.stdout?.on('data', (data: Buffer) => {
    const output = data.toString()
    console.log('Backend stdout:', output.trim())
  })

  backendProcess.stderr?.on('data', (data: Buffer) => {
    const output = data.toString().trim()
    console.log('Backend stderr:', output)

    // Parse port from uvicorn startup message
    const portMatch = output.match(/Uvicorn running on http:\/\/localhost:(\d+)/)
    if (portMatch) {
      const port = portMatch[1]
      backendUrl = `http://localhost:${port}`
      logger.info('Backend started', { port, url: backendUrl })

      // Notify renderer process of backend URL
      BrowserWindow.getAllWindows().forEach((window) => {
        window.webContents.send('backend-ready', backendUrl)
      })
    }
  })

  backendProcess.on('close', (code: number) => {
    logger.info('Backend process closed', { code })
    backendProcess = null
    backendUrl = null
  })

  backendProcess.on('error', (error: Error) => {
    logger.error('Failed to start backend', { error: error.message })
  })
}

function stopBackend(): void {
  if (backendProcess) {
    logger.info('Stopping backend process')
    backendProcess.kill()
    backendProcess = null
    backendUrl = null
  }
}

function createWindow(): void {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    show: false,
    autoHideMenuBar: true,
    ...(process.platform === 'linux' ? { icon } : {}),
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    console.log('Loading URL:', process.env['ELECTRON_RENDERER_URL'])
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

// Start backend as early as possible
app.on('will-finish-launching', () => {
  startBackend()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Log application startup
  logger.info('Penpal app started', {
    platform: process.platform,
    arch: process.arch,
    version: app.getVersion()
  })

  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  // IPC test
  ipcMain.on('ping', () => console.log('pong'))

  // Theme detection IPC handlers
  ipcMain.handle('get-system-theme', () => {
    return nativeTheme.shouldUseDarkColors ? 'dark' : 'light'
  })

  // Backend IPC handlers
  ipcMain.handle('get-backend-url', () => {
    return backendUrl
  })

  // Listen for system theme changes and notify renderer
  nativeTheme.on('updated', () => {
    const theme = nativeTheme.shouldUseDarkColors ? 'dark' : 'light'
    BrowserWindow.getAllWindows().forEach((window) => {
      window.webContents.send('system-theme-changed', theme)
    })
  })

  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    logger.info('Penpal app shutdown')
    app.quit()
  }
})

app.on('before-quit', () => {
  logger.info('Penpal app shutdown')
  stopBackend()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
