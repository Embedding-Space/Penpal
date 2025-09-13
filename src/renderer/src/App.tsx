import { ThemeProvider } from "./components/ThemeProvider"

function App(): React.JSX.Element {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <div className="min-h-screen bg-background text-foreground">
      </div>
    </ThemeProvider>
  )
}

export default App
