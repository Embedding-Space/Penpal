import * as logfire from 'logfire'
import { writeJsonLog } from './json-logger'

interface Logger {
  trace(message: string, data?: Record<string, unknown>): void
  debug(message: string, data?: Record<string, unknown>): void
  info(message: string, data?: Record<string, unknown>): void
  warn(message: string, data?: Record<string, unknown>): void
  error(message: string, data?: Record<string, unknown>): void
}

class DualLogger implements Logger {
  trace(message: string, data?: Record<string, unknown>): void {
    logfire.trace(message, data)
    writeJsonLog('trace', message, data)
  }

  debug(message: string, data?: Record<string, unknown>): void {
    logfire.debug(message, data)
    writeJsonLog('debug', message, data)
  }

  info(message: string, data?: Record<string, unknown>): void {
    logfire.info(message, data)
    writeJsonLog('info', message, data)
  }

  warn(message: string, data?: Record<string, unknown>): void {
    logfire.warn(message, data)
    writeJsonLog('warn', message, data)
  }

  error(message: string, data?: Record<string, unknown>): void {
    logfire.error(message, data)
    writeJsonLog('error', message, data)
  }
}

export const logger = new DualLogger()
