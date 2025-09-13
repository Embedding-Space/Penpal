# Technical Stack

## Application Framework
- **Backend**: Python with FastAPI for REST API server and hot reload during development
- **Frontend**: React with Vite for fast development and build tooling
- **Shell**: Electron with electron-vite for development and electron-builder for packaging

## Database System
- **Primary**: SQLite (individual .db files per agent for maximum portability)
- **ORM/Integration**: Direct SQLite integration through Python

## JavaScript Framework
- **Frontend**: React with TypeScript
- **Build Tool**: Vite
- **Package Manager**: npm

## Import Strategy
- **Strategy**: node (Node.js module resolution)

## CSS Framework
- **Framework**: Tailwind CSS v4
- **Configuration**: Latest Tailwind CSS v4 with modern features

## UI Component Library
- **Primary**: shadcn/ui (component library)
- **AI Interface**: assistant-ui (framework for assistant UIs)
- **Component Strategy**: Combination of shadcn/ui for general components and assistant-ui for AI-specific interfaces

## Fonts Provider
- **Provider**: System fonts and web fonts as needed
- **Strategy**: TBD based on design requirements

## Icon Library
- **Library**: Lucide React

## AI Integration
- **Backend AI**: Pydantic AI for handling AI model interactions
- **Model Providers**: 
  - Anthropic (BYOK)
  - OpenAI (BYOK)
  - Google (BYOK)
  - Groq (BYOK)
  - OpenRouter (BYOK)
  - Local: Ollama integration
  - Local: LM Studio integration

## Application Hosting
- **Development**: Local development environment
- **Distribution**: Desktop application (Electron-based, self-hosted)

## Database Hosting
- **Strategy**: Local SQLite files (no remote hosting needed)
- **Backup**: User-managed (portable .db files)

## Asset Hosting
- **Strategy**: Bundled with Electron application
- **Development**: Vite dev server

## Deployment Solution
- **Desktop**: electron-builder for cross-platform packaging
- **Platforms**: Windows, macOS, Linux

## Observability
- **Monitoring**: Pydantic Logfire
- **Frontend**: Pydantic Logfire TypeScript integration
- **Backend**: Pydantic Logfire Python integration
- **Strategy**: Unified observability across frontend and backend

## Code Repository URL
- **Repository**: TBD (likely GitHub, open source)
- **License**: TBD (source available license)