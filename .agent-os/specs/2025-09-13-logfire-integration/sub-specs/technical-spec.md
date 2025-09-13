# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-09-13-logfire-integration/spec.md

## Technical Requirements

- **Main Process Integration Only**: Install and configure `logfire` npm package in main Electron process for Node.js environment
- **Environment-Based Token Management**: Use `dotenv` package to load `LOGFIRE_TOKEN` from `.env` file
- **Service Metadata Configuration**: Configure Logfire with `serviceName: 'penpal-main'` and `serviceVersion` from `app.getVersion()`
- **Lifecycle Event Logging**: Implement startup and shutdown logging with diagnostic attributes (platform, arch)
- **Security Protection**: Explicit protection against token leakage in logs, error messages, or console output
- **Zero Configuration Overhead**: Application runs cleanly when no token is present in environment
- **Future-Ready Architecture**: Design supports eventual Settings UI integration without code changes

## Approach

### Implementation Strategy

1. **Environment-First Configuration**: Use dotenv for token loading, setting up future Settings UI integration
2. **Main Process Only**: Focus on main Electron process for MVP, renderer integration as separate spec
3. **Security-First Design**: Implement explicit token protection and error handling
4. **Minimal Overhead**: Leverage Logfire's built-in conditional sending behavior

### Security Architecture

- **Token Protection**: Never expose `LOGFIRE_TOKEN` in logs, errors, or console output
- **Environment Isolation**: Token loaded from `.env` file, not hardcoded or stored in application code
- **Error Handling**: Graceful handling of missing tokens without exposing token-related information
- **Future Migration Path**: Environment-based approach seamlessly supports Settings UI token injection

### Configuration Pattern

```typescript
import 'dotenv/config';

if (process.env.LOGFIRE_TOKEN) {
  logfire.configure({
    serviceName: 'penpal-main',
    serviceVersion: app.getVersion()
  });
  logfire.info('Penpal app started', {
    platform: process.platform,
    arch: process.arch
  });
}
```

## External Dependencies

- **logfire** - Official Pydantic Logfire SDK for Node.js/main process integration
- **Justification:** Required for main Electron process observability and telemetry

- **dotenv** - Environment variable loading from `.env` files
- **Justification:** Enables simple token configuration and future Settings UI migration path
