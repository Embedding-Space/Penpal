import { createContext, useContext, useEffect, useState } from "react"

type Theme = "dark" | "light" | "system"

type ThemeProviderProps = {
  children: React.ReactNode
  defaultTheme?: Theme
  storageKey?: string
}

type ThemeProviderState = {
  theme: Theme
  setTheme: (theme: Theme) => void
}

const initialState: ThemeProviderState = {
  theme: "system",
  setTheme: () => null,
}

const ThemeProviderContext = createContext<ThemeProviderState>(initialState)

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "vite-ui-theme",
  ...props
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem(storageKey) as Theme) || defaultTheme
  )

  useEffect(() => {
    const root = window.document.documentElement

    const applyTheme = async (currentTheme: Theme) => {
      root.classList.remove("light", "dark")

      if (currentTheme === "system") {
        // Use Electron's system theme detection if available, fallback to matchMedia
        if (window.api?.getSystemTheme) {
          try {
            const systemTheme = await window.api.getSystemTheme()
            root.classList.add(systemTheme)
          } catch (error) {
            console.warn("Failed to get system theme from Electron, falling back to matchMedia:", error)
            const fallbackTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
            root.classList.add(fallbackTheme)
          }
        } else {
          // Fallback for non-Electron environments
          const fallbackTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
          root.classList.add(fallbackTheme)
        }
      } else {
        root.classList.add(currentTheme)
      }
    }

    applyTheme(theme)
  }, [theme])

  // Listen for system theme changes from Electron
  useEffect(() => {
    if (theme === "system" && window.api?.onSystemThemeChange) {
      const unsubscribe = window.api.onSystemThemeChange((newTheme: string) => {
        const root = window.document.documentElement
        root.classList.remove("light", "dark")
        root.classList.add(newTheme)
      })

      return unsubscribe
    }
  }, [theme])

  const value = {
    theme,
    setTheme: (theme: Theme) => {
      localStorage.setItem(storageKey, theme)
      setTheme(theme)
    },
  }

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeProviderContext)

  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider")

  return context
}