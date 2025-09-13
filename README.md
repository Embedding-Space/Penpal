# Penpal

Penpal is an agent-first AI platform for developers and tinkerers who want to create and manage multiple specialized AI agents rather than having ephemeral conversations.

Unlike chat applications that treat AI as temporary interactions, Penpal makes each agent an independent entity with its own database, prompt, history, and capabilities. Each agent gets its own portable SQLite file, making them completely self-contained and transferable.

## Why Penpal?

**Agent-Centric Design**: Create specialized agents for different purposes instead of generic chat sessions. Each agent can be configured with specific tools, system prompts, and behavioral parameters.

**Ridiculous Model Support**: Connect to 400+ models through BYOK (Bring Your Own Key) integrations with Anthropic, OpenAI, and Google, Groq and OpenRouter, GitHub Models plus local inference via Ollama and LM Studio.

**Maximum Hackability**: Built with TypeScript, Python, and Electron using standard web technologies. No proprietary frameworks or complex abstractions—just code you can read, understand, and modify.

## Architecture

- **Frontend**: React + TypeScript with Vite
- **Backend**: Python FastAPI for AI orchestration
- **Desktop**: Electron for native platform integration
- **Database**: SQLite (one file per agent)
- **AI**: PydanticAI for model-agnostic connections

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for your platform
npm run build:mac    # macOS
npm run build:win    # Windows  
npm run build:linux  # Linux
```

## Development

This project uses electron-vite for development and electron-builder for packaging. The codebase follows standard TypeScript and Python conventions with ESLint and Prettier for consistency.

Agent databases are stored as individual `.db` files, making agents completely portable between installations. No cloud dependencies, no vendor lock-in, no telemetry.

## License

MIT - because good tools should be freely available to tinker with.