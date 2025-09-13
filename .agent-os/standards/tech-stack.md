# Tech Stack

## Context

Global tech stack defaults for Agent OS projects, overridable in project-specific `.agent-os/product/tech-stack.md`.

## Desktop Application

- Framework: Electron (latest stable)
- Language: TypeScript 5.x
- UI Framework: React 18+ (upgrade to 19 when ecosystem is stable for the project)
- Build Tool: Vite (latest)
- Module System: ES Modules
- Package Manager: npm
- Node Version: 22 LTS

## User Interface

- CSS Framework: Tailwind CSS (latest)
- Component Libraries: Project-specific
- State Management: Project-specific
- Icons: Lucide React

## Python Backend

- Language: Python 3.12+
- API Framework: FastAPI (latest)
- Web Server: Uvicorn
- Package Manager: uv
- Virtual Environment: venv via uv

## AI/LLM

- Agent Framework: PydanticAI (latest)
- Model Configuration: Runtime JSON configs
- Tool System: Dynamic toolsets (no decorators)

## Data Storage

- Database: SQLite (local files)
- Settings: electron-store
- User Data: app.getPath('userData')
- Secrets: OS keychain via `keytar` or Electron `safeStorage` (never in `electron-store`/localStorage)
  - SQLite notes: enable WAL mode; prefer a single writer; use async drivers or a threadpool when using sync drivers

## Communication

- IPC: Electron IPC with TypeScript types
- Backend API: HTTP (localhost only)
- Streaming: Server-Sent Events (SSE)

## Development Tools

- Version Control: Git
- Code Editor: Claude Code
- Python Linting/Formatting: Ruff
- TypeScript Linting: ESLint
- TypeScript Formatting: Prettier
- Python Testing: pytest + pytest-asyncio
- TypeScript Testing: Vitest

## Distribution

- Packaging: Electron Forge
- Auto-Updates: Electron autoUpdater
- Code Signing: Platform-specific certificates
