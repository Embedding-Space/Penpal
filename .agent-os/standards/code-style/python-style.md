# Python Style Guide

## Context

Detailed Python conventions for FastAPI services and PydanticAI agents. These are non-negotiable standards for all Python code.

## Tooling

### Package Management
- **Always use `uv`** - never pip, never python, never python3
- Create virtual environments: `uv venv`
- Install packages: `uv pip install package`
- Run modules (preferred): `uv run python -m app.main`
- Run scripts (if needed): `uv run python script.py`
- Manage dependencies in `pyproject.toml`

### Code Quality
- **Ruff for everything** - linting and formatting
- Run before every commit: `uv run ruff check . && uv run ruff format .`
- Configure in `pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py312"
select = ["E", "F", "I", "N", "UP", "B", "SIM", "RUF"]
```

## Style Decisions (Non-Negotiable)

### String Quotes
- **Always double quotes** for strings
- Exception: Use single quotes to avoid escaping

```python
# Good
message = "Hello, world!"
query = "SELECT * FROM users WHERE name = 'Alice'"

# Bad
message = 'Hello, world!'  # Wrong quotes
```

### Imports
- **Always absolute imports** from project root
- Never relative imports

```python
# Good
from app.services.user_service import UserService
from app.models.user import User

# Bad
from .user_service import UserService  # Relative
from ..models.user import User  # Relative
```

### Line Breaking
- Break **before** operators
- Align with opening delimiter

```python
# Good
result = (
    first_value
    + second_value
    + third_value
)

user = User(
    name="Alice",
    email="alice@example.com",
    age=30,
)

# Bad
result = first_value + \
    second_value + \
    third_value
```

### Trailing Commas
- **Always** for multi-line structures
- **Never** for single-line

```python
# Good
items = [
    "first",
    "second",
    "third",  # Trailing comma
]

point = (1, 2)  # No trailing comma on single line

# Bad
items = ["first", "second", "third",]  # No trailing comma on single line
```

### Docstrings
- **Only for public APIs** (exposed to users)
- Never for internal functions
- Use triple double quotes

```python
# Good - public API
def create_user(name: str, email: str) -> User:
    """Create a new user account.
    
    Args:
        name: User's full name
        email: User's email address
        
    Returns:
        Created user object
    """
    pass

# Good - internal function, no docstring
def _validate_email(email: str) -> bool:
    return "@" in email
```

### Class Method Order
1. `__init__`
2. Properties (`@property`)
3. Public methods
4. Private methods (`_method`)

```python
class UserService:
    def __init__(self):
        self._cache = {}
    
    @property
    def cache_size(self) -> int:
        return len(self._cache)
    
    def get_user(self, id: int) -> User:
        return self._fetch_from_db(id)
    
    def _fetch_from_db(self, id: int) -> User:
        pass
```

### Early Returns
- **Use early returns** for guard clauses
- Reduce nesting

```python
# Good - early returns
def process_user(user: User | None) -> str:
    if not user:
        return "No user"
    
    if not user.is_active:
        return "Inactive user"
    
    # Main logic here
    return f"Processing {user.name}"

# Bad - nested ifs
def process_user(user: User | None) -> str:
    if user:
        if user.is_active:
            return f"Processing {user.name}"
        else:
            return "Inactive user"
    else:
        return "No user"
```

### Exception Handling
- **Always catch specific exceptions**
- Never bare except
- Re-raise or log, don't silence

```python
# Good
try:
    result = await fetch_data()
except httpx.TimeoutException:
    logger.error("Request timed out")
    raise
except httpx.HTTPStatusError as e:
    logger.error(f"HTTP error: {e.response.status_code}")
    raise

# Bad
try:
    result = await fetch_data()
except:  # Never do this
    pass  # Never silence errors
```

### Comprehensions
- **Only when clear and single-line**
- Otherwise use loops

```python
# Good - simple and clear
squares = [x**2 for x in range(10)]
users_by_id = {user.id: user for user in users}

# Bad - too complex
result = [
    process(item)
    for sublist in nested_list
    for item in sublist
    if validate(item) and item.active
]

# Better - use a loop
result = []
for sublist in nested_list:
    for item in sublist:
        if validate(item) and item.active:
            result.append(process(item))
```

### Blank Lines
- **2 lines** between top-level definitions
- **1 line** between class methods
- **0-1 lines** within functions (for logical grouping)

```python
import asyncio  # imports


def first_function():  # 2 lines before
    pass


def second_function():  # 2 lines before
    pass


class MyClass:  # 2 lines before
    
    def method_one(self):
        pass
    
    def method_two(self):  # 1 line before
        # Group 1: initialization
        x = 1
        y = 2
        
        # Group 2: processing (blank line for clarity)
        result = x + y
        
        return result
```

## Type Hints

### Modern Syntax
```python
# Good - modern Python 3.12+
def process_items(items: list[str]) -> dict[str, int]:
    pass

def maybe_get_user(id: int) -> User | None:
    pass

# Bad - old style
from typing import List, Dict, Optional
def process_items(items: List[str]) -> Dict[str, int]:
    pass
```

### Type Everything
- Every function parameter
- Every function return
- Every class attribute
- Use `Any` only with a comment explaining why

### Pydantic for Validation
```python
from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(..., ge=0, le=150)
```

## Async Patterns

### Async Everywhere
```python
# Good - async all the way
async def get_user(user_id: int) -> User:
    async with get_db() as db:
        result = await db.fetch_one("SELECT * FROM users WHERE id = ?", user_id)
        return User(**result)

# Bad - synchronous I/O
def get_user(user_id: int) -> User:
    with sqlite3.connect("db.sqlite") as conn:
        result = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return User(**result.fetchone())
```

### Concurrency
```python
# Good - concurrent operations
results = await asyncio.gather(
    fetch_user(user_id),
    fetch_preferences(user_id),
    fetch_history(user_id),
)

# Bad - sequential awaits
user = await fetch_user(user_id)
prefs = await fetch_preferences(user_id)
history = await fetch_history(user_id)
```

### Cleanup
```python
# Always use async context managers
async with aiofiles.open("file.txt") as f:
    content = await f.read()

# Clean shutdown
async def shutdown():
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
```

## FastAPI Patterns

### Route Organization
```python
# routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Create a new user."""
    return await service.create(user)
```

### Dependency Injection
```python
# dependencies.py
async def get_db() -> AsyncGenerator[Database, None]:
    db = Database("sqlite:///app.db")
    try:
        yield db
    finally:
        await db.close()

# Use in routes
@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: Database = Depends(get_db),
) -> UserResponse:
    return await db.fetch_user(user_id)
```

### Error Handling
```python
# Specific error responses
@router.get("/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return user
```

## PydanticAI Patterns

### No Decorators
```python
# Bad - decorator magic
@agent.tool
async def get_weather(city: str) -> str:
    pass

# Good - dynamic toolsets
from pydantic_ai import Tool

weather_tool = Tool(
    name="get_weather",
    description="Get weather for a city",
    func=get_weather_func,
)

agent.tools = [weather_tool]  # Hot-swappable
```

## Code Organization

### File Size
- Maximum 200 lines per file
- If approaching limit, split into logical modules
- One major class or function group per file

### Module Structure
```python
project/
├── api/
│   ├── __init__.py
│   ├── routes.py        # Route definitions only
│   └── dependencies.py  # Shared dependencies
├── services/
│   ├── __init__.py
│   └── user_service.py  # Business logic
├── models/
│   ├── __init__.py
│   └── user.py          # Pydantic models
└── core/
    ├── __init__.py
    └── config.py        # Settings management
```

### Imports
```python
# Standard library
import json
import asyncio
from pathlib import Path

# Third-party
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

# Local - absolute imports
from app.models.user import User
from app.services.user_service import UserService
```

## What NOT to Do

### No ORMs
```python
# Bad - ORM complexity
from sqlalchemy.orm import Session
users = session.query(User).filter(User.age > 18).all()

# Good - simple and clear
users = await db.fetch_all(
    "SELECT * FROM users WHERE age > ?", 
    18
)
```

### No Synchronous I/O
```python
# Bad - blocks event loop
import requests
response = requests.get("https://api.example.com")

# Good - async
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")
```

### No Magic
```python
# Bad - too much magic
@auto_retry
@cache_result
@validate_input
@log_execution
def do_something():
    pass

# Good - explicit
async def do_something():
    try:
        validate_input(data)
        result = await execute()
        cache.set(key, result)
        return result
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise
```

## Error Messages

### User-Friendly
```python
# Bad
raise Exception("Error: 0x80004005")

# Good
raise ValueError("Email address must contain @ symbol")
```

### Actionable
```python
# Bad
raise ConfigError("Invalid configuration")

# Good
raise ConfigError(
    f"Missing required config key 'api_key'. "
    f"Add it to config.json or set API_KEY environment variable"
)
```

## Testing

### Async Tests
```python
import pytest

@pytest.mark.asyncio
async def test_create_user():
    user = await create_user({"name": "Test", "email": "test@test.com"})
    assert user.id is not None
```

### Fixtures
```python
@pytest.fixture
async def client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_endpoint(client):
    response = await client.get("/users/1")
    assert response.status_code == 200
```

## The Python Meta Rule

Python gives us clarity through simplicity. Use type hints religiously, make everything async, and keep it explicit. If you're fighting the language, you're doing it wrong. And always, always use `uv`.
### Exceptions and Wrappers
```python
# If a library is sync-only, wrap calls in a threadpool to avoid blocking the event loop
import anyio

def compute_sync(value: int) -> int:
    # CPU-bound or sync-only library call
    return value * value

async def compute(value: int) -> int:
    return await anyio.to_thread.run_sync(compute_sync, value)

# Note: FastAPI sync route handlers run in a threadpool automatically.
```
