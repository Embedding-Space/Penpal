import { mkdirSync, writeFileSync, appendFileSync } from 'fs'
import { join } from 'path'
import { app } from 'electron'

// Get the proper OS-specific logs directory
const logsDir = join(app.getPath('logs'))
const logFile = join(logsDir, 'Penpal.json')

// Ensure directory exists and truncate file on startup
function initializeLogFile(): void {
  try {
    mkdirSync(logsDir, { recursive: true })
    writeFileSync(logFile, '', 'utf8')
  } catch (error) {
    console.error('Failed to initialize log file:', error)
  }
}

// Initialize on module load
initializeLogFile()

export function writeJsonLog(level: string, message: string, data?: Record<string, any>): void {
  try {
    const entry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...data
    }

    appendFileSync(logFile, JSON.stringify(entry) + '\n', 'utf8')
  } catch (error) {
    console.error('Failed to write to log file:', error)
  }
}
