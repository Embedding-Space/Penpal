# Penpal Backend

Backend API for the Penpal AI agent management platform.

## Development

```bash
# Install dependencies
uv sync

# Run the backend server
uv run python -m penpal_backend

# Run tests
uv run pytest

# Lint and format
uv run ruff check .
uv run ruff format .
```

## Architecture

- **FastAPI**: Web framework for the API
- **PydanticAI**: AI agent orchestration
- **SQLite**: Database storage (one file per agent)
- **Logfire**: Observability and logging
- **uv**: Python package management

## API Endpoints

- `GET /api/v1/health` - Health check
