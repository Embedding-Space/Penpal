# Development Best Practices

## Context

Global development guidelines for Agent OS projects.

<conditional-block context-check="core-principles">
IF this Core Principles section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using Core Principles already in context"
ELSE:
  READ: The following principles

## Core Principles

### Keep It Simple
- Be concise but not cryptic
- Avoid over-engineering solutions
- Choose straightforward approaches over clever ones
- Prefer explicit over implicit

### Optimize for Readability
- Prioritize code clarity over micro-optimizations
- Write self-documenting code with clear variable names
- Add comments for "why" not "what"

### DRY (Don't Repeat Yourself)
- Extract repeated logic to separate functions
- Extract repeated UI markup to reusable components
- Create utility functions for common operations
- But don't abstract prematurely - wait for patterns to emerge

### File Structure
- Keep files focused on a single responsibility
- Group related functionality together
- Use consistent naming conventions
</conditional-block>

<conditional-block context-check="dependencies" task-condition="choosing-external-library">
IF current task involves choosing an external library:
  IF Dependencies section already read in current context:
    SKIP: Re-reading this section
    NOTE: "Using Dependencies guidelines already in context"
  ELSE:
    READ: The following guidelines
ELSE:
  SKIP: Dependencies section not relevant to current task

## Dependencies

### Choose Libraries Wisely
When adding third-party dependencies:
- Select the most popular and actively maintained option
- Consider bundle size for frontend dependencies
- Consider package compatibility with your deployment target
- Avoid unnecessary cloud service dependencies
- Check the library's GitHub repository for:
  - Recent commits (within last 6 months)
  - Active issue resolution
  - Number of stars/downloads
  - Clear documentation
</conditional-block>

<conditional-block context-check="electron-principles" task-condition="electron-development">
IF current task involves Electron development:
  IF Electron Principles section already read in current context:
    SKIP: Re-reading this section
    NOTE: "Using Electron Principles already in context"
  ELSE:
    READ: The following principles
ELSE:
  SKIP: Electron principles not relevant to current task

## Electron Architecture

### Process Separation
- Maintain strict process separation - main process handles system access, renderer handles UI
- Never expose Node.js APIs directly to renderer process
- All privileged operations must go through validated IPC channels
- Type all IPC communication boundaries between processes

### Resource Management
- Clean up event listeners when components unmount
- Cancel async operations when no longer needed
- Profile memory usage regularly during development
- Lazy load expensive resources

### Security Principles
- Validate all IPC messages in the main process
- Use context isolation and sandbox mode
- Never trust data from renderer process
- Store sensitive data using platform-secure methods (not localStorage or electron-store)
- BrowserWindow defaults: `contextIsolation: true`, `sandbox: true`, `nodeIntegration: false`, `enableRemoteModule: false`
- Set a strict Content Security Policy (CSP) and only load trusted content
- Validate IPC payload schemas per channel (e.g., zod/io-ts) before acting
 - In production, load only `file://` or a fixed trusted HTTPS origin; set `allowRunningInsecureContent: false`

### Local-First Design
- Design for offline operation when building desktop apps
- Use appropriate platform paths for user data
- Handle missing network gracefully
- Minimize required cloud dependencies for core functionality
</conditional-block>

<conditional-block context-check="python-async" task-condition="python-development">
IF current task involves Python development:
  IF Python Async Patterns section already read in current context:
    SKIP: Re-reading this section
    NOTE: "Using Python Async Patterns already in context"
  ELSE:
    READ: The following patterns
ELSE:
  SKIP: Python patterns not relevant to current task

## Python/Async Patterns

### Async by Default (with pragmatic exceptions)
- Prefer async/await end-to-end for I/O-bound work
- FastAPI routes should be async for I/O; sync routes are acceptable when wrapping CPU-bound or sync-only code (they run in a threadpool)
- Database operations should be async; if your driver is sync-only, use a threadpool wrapper or switch to an async driver
- For CPU-bound tasks, offload to threads or processes instead of blocking the event loop

### Service Structure
- Handle errors at service boundaries
- Return structured responses with Pydantic models
- Keep business logic separate from API routes
- Clean shutdown handling for graceful stops
</conditional-block>

<conditional-block context-check="type-safety" task-condition="typed-languages">
IF current task involves TypeScript or Python:
  IF Type Safety section already read in current context:
    SKIP: Re-reading this section
    NOTE: "Using Type Safety Philosophy already in context"
  ELSE:
    READ: The following philosophy
ELSE:
  SKIP: Type safety not relevant to current task

## Type Safety Philosophy

### Types as Documentation
- Types are the best form of documentation
- A well-typed function signature explains itself
- Update types when changing behavior
- Never use `any` or `Any` without a comment explaining why

### Type Boundaries
- Type all boundaries between systems
- Validate at runtime (e.g., Pydantic for Python, validation libraries for TypeScript)
- Share type definitions between frontend and backend
- Fail fast on type mismatches
</conditional-block>

<conditional-block context-check="ai-llm" task-condition="ai-development">
IF current task involves AI/LLM functionality:
  IF AI/LLM Development section already read in current context:
    SKIP: Re-reading this section
    NOTE: "Using AI/LLM Development practices already in context"
  ELSE:
    READ: The following practices
ELSE:
  SKIP: AI/LLM practices not relevant to current task

## AI/LLM Development

### Model-Agnostic Design
- Never hardcode model names or providers
- Configuration over code for model settings
- Support multiple providers simultaneously
- Abstract model-specific behavior

### Resilience and Cost
- Graceful degradation when models fail
- Cost-aware model selection (cheaper models for simple tasks)
- Implement retry logic with exponential backoff
- Cache responses when appropriate
</conditional-block>

<conditional-block context-check="dev-workflow" task-condition="general-development">
IF this Development Workflow section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using Development Workflow already in context"
ELSE:
  READ: The following workflow practices

## Development Workflow

### Git Practices
- Commit messages explain why, not what
- Branch names describe the feature/experiment
- Push broken code to branches, never to main
- Squash merges to keep history clean

### Testing Philosophy
- Test business logic thoroughly
- Don't test simple getters/setters
- Integration tests for critical paths only
- Manual testing for UI/UX validation
</conditional-block>

<conditional-block context-check="error-handling" task-condition="general-development">
IF this Error Handling section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using Error Handling Philosophy already in context"
ELSE:
  READ: The following error handling practices

## Error Handling Philosophy

### Fail Fast and Loud
- Surface errors immediately with clear messages
- Log everything during development
- Use log levels: verbose DEBUG in development; INFO/WARN/ERROR in production (DEBUG off by default)
- Make problems visible, not hidden

### User Experience
- User-friendly error messages (no stack traces)
- Suggest solutions when possible
- Differentiate between user errors and system errors
- Always provide a way forward
</conditional-block>

<conditional-block context-check="philosophy" task-condition="general-development">
IF this Philosophy section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using Development Philosophy already in context"
ELSE:
  READ: The following philosophical principles

## Development Philosophy

### The Tinkerer's Manifesto
- Build to learn, not just to ship
- The journey is the product
- If you're not having fun, you're doing it wrong
- Features exist because they're interesting, not because they're needed
- Our code is our real deliverable - ideas embodied in implementation
- Everything we publish is open source (MIT) or source-available
- Make the code nice - it's going public on GitHub

### Documentation Philosophy
- Code should be self-documenting
- Don't write docs that the code could tell you
- README should get someone running, not explain architecture
- Comments for "why," never "what"
- Dead code doesn't belong in public repos

### Collaboration Principles
- Code is a conversation, not a monologue
- Working alone is harder than working together
- Push early, push often, push broken (to branches)
- Questions are better than assumptions

### Privacy and Ownership
- Users own their data
- Users bring their own API keys
- Everything works offline
- No telemetry without explicit consent
- Local-first, always
</conditional-block>
