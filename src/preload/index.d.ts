import { ElectronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electron: ElectronAPI
    api: {
      getSystemTheme: () => Promise<string>
      onSystemThemeChange: (callback: (theme: string) => void) => () => void
    }
  }
}
