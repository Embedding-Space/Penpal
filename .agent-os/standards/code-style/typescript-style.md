# TypeScript Style Guide

## Context

Detailed TypeScript conventions for Electron apps with React. These are arbitrary but consistent decisions - we pick one way and stick to it.

## Tooling

### Build and Bundle
- **Vite** for bundling - no webpack, no complex configs
- **TypeScript** with strict mode always enabled
- **ESLint** for linting
- **Prettier** for formatting

### TypeScript Config
```json
{
  "compilerOptions": {
    "strict": true,                      // Non-negotiable
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "target": "ES2022",
    "module": "ESNext",
    "jsx": "react-jsx",                  // No React import needed
    "moduleResolution": "bundler"
  }
}
```

## Formatting Rules (Non-Negotiable)

### The Basics
- **Semicolons:** ALWAYS (prevents ASI gotchas)
- **Quotes:** Single for strings, double for JSX attributes
- **Trailing commas:** ALWAYS (cleaner git diffs)
- **Indentation:** 2 spaces (React ecosystem standard)
- **Line length:** 100 characters max
- **Variable declarations:** `const` > `let` > NEVER `var`

```typescript
// Good
const userName = 'Alice';
const element = <div className="container">;
const items = [
  'first',
  'second',
  'third',  // Trailing comma
];

// Bad
var userName = "Alice"  // No var, wrong quotes, no semicolon
const element = <div className='container'>  // Wrong quotes for JSX
```

## Function Syntax

### Arrow Functions Everywhere
```typescript
// Good - arrow functions for consistency
const calculateTotal = (items: Item[]): number => {
  return items.reduce((sum, item) => sum + item.price, 0);
};

const handleClick = () => {
  console.log('clicked');
};

// Bad - mixed styles
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Exception: React Components
```typescript
// React components use arrow functions too
export const UserProfile: React.FC<UserProfileProps> = ({ user }) => {
  return <div>{user.name}</div>;
};
```

## Type Definitions

### Interfaces vs Types Rule
- **Interfaces:** For objects (they're extendable)
- **Types:** For unions, functions, and aliases

```typescript
// Good - interface for objects
interface User {
  id: string;
  name: string;
  email: string;
}

interface AdminUser extends User {
  permissions: string[];
}

// Good - type for unions and functions
type Status = 'idle' | 'loading' | 'success' | 'error';
type ClickHandler = (event: MouseEvent) => void;

// Bad - using type for objects
type User = {  // Should be interface
  id: string;
  name: string;
};
```

## File Naming

### Clear Rules
- **React Components:** PascalCase (e.g., `UserProfile.tsx`)
- **Utilities/Helpers:** kebab-case (e.g., `format-date.ts`)
- **Types/Interfaces:** PascalCase (e.g., `UserTypes.ts`)
- **Hooks:** camelCase starting with "use" (e.g., `useAuth.ts`)

```
src/
├── components/
│   ├── UserProfile.tsx      # Component - PascalCase
│   └── ChatWindow.tsx
├── hooks/
│   └── useWebSocket.ts       # Hook - camelCase with 'use'
├── utils/
│   ├── format-date.ts        # Utility - kebab-case
│   └── api-client.ts
└── types/
    └── UserTypes.ts          # Types - PascalCase
```

## Exports

### Named Exports Only
```typescript
// Good - named exports
export const UserProfile = () => { ... };
export const useAuth = () => { ... };
export interface User { ... }

// Bad - default exports
export default UserProfile;  // Harder to refactor, worse IDE support
```

### Barrel Exports
```typescript
// components/index.ts
export { UserProfile } from './UserProfile';
export { ChatWindow } from './ChatWindow';
export { MessageList } from './MessageList';
```

## React Patterns

### Component Structure
```typescript
// Always this order and structure
interface UserProfileProps {
  user: User;
  onUpdate?: (user: User) => void;
  className?: string;
}

export const UserProfile: React.FC<UserProfileProps> = ({
  user,
  onUpdate,
  className,
}) => {
  // 1. State
  const [isEditing, setIsEditing] = useState(false);
  
  // 2. Refs
  const inputRef = useRef<HTMLInputElement>(null);
  
  // 3. Context/Redux
  const { theme } = useTheme();
  
  // 4. Effects
  useEffect(() => {
    // Effect logic
  }, [user.id]);
  
  // 5. Handlers (separate, not inline)
  const handleEdit = () => {
    setIsEditing(true);
  };
  
  const handleSave = () => {
    onUpdate?.(user);
    setIsEditing(false);
  };
  
  // 6. Render
  return (
    <div className={className}>
      {/* JSX */}
    </div>
  );
};
```

### Event Handlers

Prefer separate handlers for clarity and stable identities; inline lambdas are acceptable for simple cases where re-renders and identity aren’t a concern.
```typescript
// Good - separate handlers
const handleClick = () => {
  doSomething();
};

return <button onClick={handleClick}>Click</button>;

// Also acceptable for trivial cases
return <button onClick={() => doSomething()}>Click</button>;
```

### Hooks Rules
```typescript
// Custom hooks always start with 'use'
export const useWebSocket = (url: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  
  useEffect(() => {
    // WebSocket logic
  }, [url]);
  
  return { isConnected, message };
};
```

## Async Handling

### Always async/await
```typescript
// Good - async/await
const fetchUser = async (id: string): Promise<User> => {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching user:', error);
    throw error;
  }
};

// Bad - promise chains
const fetchUser = (id: string): Promise<User> => {
  return fetch(`/api/users/${id}`)
    .then(response => {
      if (!response.ok) throw new Error();
      return response.json();
    })
    .catch(error => {
      console.error(error);
      throw error;
    });
};
```

## Error Handling

### Try/Catch with Proper Types
```typescript
// Define error types
class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Type guard
const isApiError = (error: unknown): error is ApiError => {
  return error instanceof ApiError;
};

// Use in try/catch
try {
  const user = await fetchUser(id);
} catch (error) {
  if (isApiError(error)) {
    console.error(`API error ${error.statusCode}: ${error.message}`);
  } else {
    console.error('Unknown error:', error);
  }
}
```

## Electron-Specific

### IPC Type Safety
```typescript
// shared/ipc-types.ts - shared between main and renderer
export interface IpcChannels {
  'file:open': {
    request: { filters: string[] };
    response: string | null;
  };
  'app:quit': {
    request: void;
    response: void;
  };
}

// Type-safe invoke
export const ipcInvoke = <K extends keyof IpcChannels>(
  channel: K,
  data: IpcChannels[K]['request']
): Promise<IpcChannels[K]['response']> => {
  return window.electron.invoke(channel, data);
};
```

### Preload Scripts
```typescript
// preload.ts
import { contextBridge, ipcRenderer } from 'electron';

// Expose only an explicit, typed, whitelisted API
// Define specific surface methods instead of generic channel pass-through
type FileOpenRequest = { filters: string[] };

const api = {
  file: {
    open: (filters: string[]) =>
      ipcRenderer.invoke('file:open', { filters } as FileOpenRequest) as Promise<string | null>,
  },
  app: {
    quit: () => ipcRenderer.invoke('app:quit') as Promise<void>,
  },
} as const;

contextBridge.exposeInMainWorld('electron', api);
```

## State Management

### Zustand Patterns
```typescript
// stores/user-store.ts
interface UserStore {
  user: User | null;
  isLoading: boolean;
  setUser: (user: User) => void;
  logout: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  isLoading: false,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

## What NOT to Do

### Never Use
- `var` - use `const` or `let`
- `any` without a comment explaining why
- `// @ts-ignore` - fix the type issue
- Default exports - use named exports
- Inline event handlers - define them separately
- `.then()` chains - use async/await
- Function declarations - use arrow functions
- Classes (except for errors) - use functions and hooks

### Anti-Patterns
```typescript
// Bad - everything wrong
var data: any = {};  // var and any
export default function() {  // default export, no name
  return (
    <div onClick={() => {  // inline handler
      fetch('/api').then(r => r.json())  // promise chain
    }}>
    </div>
  );
}

// Good - the right way
const data: UserData = {};
export const DataComponent = () => {
  const handleClick = async () => {
    const response = await fetch('/api');
    const json = await response.json();
  };
  
  return <div onClick={handleClick}></div>;
};
```

## Import Organization

### Order and Grouping
```typescript
// 1. React/Node built-ins
import { useState, useEffect } from 'react';
import { readFile } from 'fs/promises';

// 2. External packages
import { z } from 'zod';
import { format } from 'date-fns';

// 3. Internal absolute imports
import { UserProfile } from '@/components/UserProfile';
import { useAuth } from '@/hooks/useAuth';

// 4. Relative imports
import { formatDate } from './utils';

// 5. Types (if separate)
import type { User } from '@/types';
```

### Path Aliases
```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  }
}
```
If using ESLint import rules, configure the import resolver for aliases accordingly.

## ESLint + Prettier
Avoid rule conflicts by extending Prettier in ESLint:
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ]
}
```

## The TypeScript Meta Rule

TypeScript is about confidence through types. Every decision here is designed to maximize type safety, consistency, and readability. When in doubt, choose the more explicit option. The compiler is your friend - if it's complaining, listen.
