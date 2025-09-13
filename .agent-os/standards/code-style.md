# Code Style Guide

## Context

Global code style rules for Agent OS projects.

<conditional-block context-check="general-formatting">
IF this General Formatting section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using General Formatting rules already in context"
ELSE:
  READ: The following formatting rules

## General Formatting

### Indentation
- TypeScript/JSX/React: 2 spaces (never tabs)
- Python: 4 spaces (PEP 8 standard)
- Maintain consistent indentation throughout files
- Align nested structures for readability

### Naming Conventions

**TypeScript/React:**
- **Variables and Functions**: Use camelCase (e.g., `userProfile`, `calculateTotal`)
- **Classes and Types**: Use PascalCase (e.g., `UserProfile`, `PaymentProcessor`)
- **React Components**: Use PascalCase (e.g., `ChatWindow`, `MessageList`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)

**Python:**
- **Variables and Functions**: Use snake_case (e.g., `user_profile`, `calculate_total`)
- **Classes**: Use PascalCase (e.g., `UserProfile`, `PaymentProcessor`)
- **Constants**: Use UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)

### String Formatting

**TypeScript/React:**
- Use single quotes for strings: `'Hello World'`
- Use template literals for interpolation:
```typescript
`Hello ${name}`
```
- JSX attributes use double quotes: `<div className="container">`

**Python:**
- Use double quotes for strings: `"Hello World"`
- Use f-strings for interpolation: `f"Hello {name}"`
- Triple quotes for multi-line strings: `"""docstring"""`

### Code Comments
- Add brief comments above non-obvious business logic
- Document complex algorithms or calculations
- Explain the "why" behind implementation choices
- Never remove existing comments unless removing the associated code
- Update comments when modifying code to maintain accuracy; however, do not document where things used to be or what we're not doing any more
- Keep comments concise and relevant
</conditional-block>

<conditional-block task-condition="html-css-tailwind" context-check="html-css-style">
IF current task involves writing or updating HTML, CSS, or TailwindCSS:
  IF html-style.md AND css-style.md already in context:
    SKIP: Re-reading these files
    NOTE: "Using HTML/CSS style guides already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get HTML formatting rules from code-style/html-style.md"
        REQUEST: "Get CSS and TailwindCSS rules from code-style/css-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ the following style guides (only if not already in context):
        - @.agent-os/standards/code-style/html-style.md (if not in context)
        - @.agent-os/standards/code-style/css-style.md (if not in context)
    </context_fetcher_strategy>
ELSE:
  SKIP: HTML/CSS style guides not relevant to current task
</conditional-block>

<conditional-block task-condition="typescript" context-check="typescript-style">
IF current task involves writing or updating TypeScript/React:
  IF typescript-style.md already in context:
    SKIP: Re-reading this file
    NOTE: "Using TypeScript style guide already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get TypeScript style rules from code-style/typescript-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ: @.agent-os/standards/code-style/typescript-style.md
    </context_fetcher_strategy>
ELSE:
  SKIP: TypeScript style guide not relevant to current task
</conditional-block>

<conditional-block task-condition="python" context-check="python-style">
IF current task involves writing or updating Python:
  IF python-style.md already in context:
    SKIP: Re-reading this file
    NOTE: "Using Python style guide already in context"
  ELSE:
    <context_fetcher_strategy>
      IF current agent is Claude Code AND context-fetcher agent exists:
        USE: @agent:context-fetcher
        REQUEST: "Get Python style rules from code-style/python-style.md"
        PROCESS: Returned style rules
      ELSE:
        READ: @.agent-os/standards/code-style/python-style.md
    </context_fetcher_strategy>
ELSE:
  SKIP: Python style guide not relevant to current task
</conditional-block>
