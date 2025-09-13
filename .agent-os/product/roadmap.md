# Product Roadmap

## Phase 1: Core MVP

**Goal:** Establish basic agent creation and interaction functionality with essential model integrations
**Success Criteria:** Users can create agents, configure basic settings, and have conversations with at least 2 model providers

### Features

- [ ] Pydantic Logfire observability integration `L`
- [ ] Basic agent creation and configuration `M`
- [ ] SQLite database per agent setup `M`
- [ ] OpenAI API integration (BYOK) `L`
- [ ] Anthropic API integration (BYOK) `L`
- [ ] Simple chat interface with agent-centric design `L`
- [ ] Agent list and management UI `M`
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
- [ ] Agent import/export functionality `M`

### Dependencies

- Phase 1 completion
- Model provider API implementations
- Enhanced agent storage schema

## Phase 3: Polish & Advanced Features

**Goal:** Enhance user experience and add advanced functionality for power users
**Success Criteria:** Production-ready application with advanced features, comprehensive observability

### Features

- [ ] Tool integration framework for agents `XL`
- [ ] Advanced conversation search and filtering `M`
- [ ] Model switching for existing agents `M`
- [ ] Agent configuration templates `M`
- [ ] Bulk agent operations `M`
- [ ] Enhanced UI/UX polish `L`

### Dependencies

- Phase 2 completion
- Tool integration architecture design
