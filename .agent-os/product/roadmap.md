# Product Roadmap

## Phase 1: Core MVP

**Goal:** Establish basic agent creation and interaction functionality with essential model integrations
**Success Criteria:** Users can create agents, configure basic settings, and have conversations with at least 2 model providers

### Features

- [x] Pydantic Logfire observability integration `L`
- [ ] Settings window with UI for configuring user preferences and secrets `L`
- [ ] Simple chat interface with agent-centric design `L`
- [ ] Agent list and management UI `M`
- [ ] Basic agent creation and configuration `M`
- [ ] SQLite database per agent setup `M`
- [ ] GitHub Models API integration (BYOK) `L`
- [ ] OpenAI API integration (BYOK) `L`
- [ ] Anthropic API integration (BYOK) `L`
- [ ] Basic conversation history storage and retrieval `M`

### Dependencies

- Pydantic Logfire setup
- FastAPI backend setup
- React frontend with Vite
- Electron shell integration
- Basic UI components from shadcn/ui

## Phase 2: Extended Model Support & Core Differentiators

**Goal:** Implement the "ridiculous model support" differentiator and enhance agent management
**Success Criteria:** Support for 100+ models across multiple providers, advanced agent configuration options

### Features

- [ ] Google AI integration (BYOK) `M`
- [ ] Groq integration (BYOK) `M`
- [ ] OpenRouter integration (BYOK) `L`
- [ ] Ollama local model integration `L`
- [ ] LM Studio integration `L`
- [ ] Advanced agent configuration (system prompts, parameters) `M`
- [ ] MCP (Model Context Protocol) support `L`

### Dependencies

- Phase 1 completion

## Phase 3: Polish & Advanced Features

**Goal:** Enhance user experience and add advanced functionality for power users
**Success Criteria:** Production-ready application with advanced features, comprehensive observability

### Features

- [ ] Enhanced UI/UX polish `L`

### Dependencies

- Phase 2 completion
