# API Backend Service

## Overview

**Purpose:** REST API for managing redirect links (CRUD operations).

**Technology:** Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic, PyJWT, pwdlib

**Port:** 8000

---

## Responsibilities

- Create, read, update, delete redirect links
- Generate unique short codes
- JWT-based user authentication (register, login, refresh tokens)
- Provide OpenAPI specification for frontend
- Database migrations via Alembic

---

## Project Structure

**Architecture:** Layered architecture with FastAPI:
- `src/` - Application code
- `src/redirect_link/` - Domain module for redirect links
- `src/auth/` - Domain module for authentication and JWT
- `src/exception_registry.py` - Automatic exception handler registration
- `migrations/` - Alembic database migrations
- `cmd/` - Application entry point

**Key Files:**
- `src/main.py` - FastAPI application setup and exception registry wiring
- `cmd/run.py` - Uvicorn runner with CLI argument parsing
- `src/api.py` - Router aggregation
- `src/exception_registry.py` - Declarative exception-to-status-code registry
- `src/<domain>/routes.py` - API endpoints
- `src/<domain>/service.py` - Business logic
- `src/<domain>/models.py` - SQLAlchemy models
- `src/<domain>/repository.py` - Data access
- `src/<domain>/schemas.py` - Pydantic schemas
- `src/unit_of_work.py` - Transaction boundary management
- `src/db.py` - Database engine and session

**Explore the codebase:**
```bash
# List all Python files
find apps/api-backend/src -name "*.py" | head -20

# View migrations
ls apps/api-backend/migrations/versions/
```

---

## Dependencies

- **FastAPI** - Web framework
- **SQLAlchemy 2.0** - ORM
- **asyncpg** - Async PostgreSQL driver
- **Alembic** - Database migrations
- **Pydantic Settings** - Configuration management
- **PyJWT** - JWT token encoding/decoding
- **pwdlib** - Password hashing (Argon2)

---

## Configuration

Environment variables (see root `.env.example`):

| Variable | Description |
|----------|-------------|
| `POSTGRES_HOST` | PostgreSQL host |
| `POSTGRES_PORT` | PostgreSQL port |
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |
| `BACKEND_HOST` | API server host (default: `0.0.0.0`) |
| `BACKEND_PORT` | API server port (default: `8000`) |
| `BACKEND_JWT_ALGORITHM` | JWT algorithm (e.g., `HS256`) |
| `BACKEND_JWT_SECRET_KEY` | JWT signing secret |
| `BACKEND_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL in minutes |
| `BACKEND_REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL in days |

---

## Running the Service

### Prerequisites

- Python 3.13+
- uv package manager
- PostgreSQL running (via Docker Compose)

### Setup

```bash
cd apps/api-backend
uv sync
```

### Run Migrations

```bash
# Apply all migrations
uv run task migrate-to-head

# Check current migration
uv run task migrate-check-current

# See migration history
uv run task migrate-check-history
```

### Start the Service

```bash
# Production mode
uv run task start

# Development mode (with auto-reload)
uv run task start --dev
```

The API will be available at http://localhost:8000

**API Documentation (auto-generated):**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

**Launch details:**
- Entry point: `cmd/run.py` parses CLI arguments and starts Uvicorn
- `--dev` flag enables hot reload via Uvicorn
- Configuration is loaded from root `.env` via Pydantic Settings

---

## Exception Registry

The service uses a declarative `ExceptionRegistry` that maps custom exceptions to HTTP status codes. Exception classes decorated with `@ExceptionRegistry.register(<status_code>)` automatically receive a JSON response handler applied to the FastAPI app via `ExceptionRegistry.apply(app)`.

**Example:**
```python
# src/exceptions.py
from fastapi import status
from src.exception_registry import ExceptionRegistry

@ExceptionRegistry.register(status.HTTP_404_NOT_FOUND)
class NotFoundError(Exception): ...
```

---

## API Endpoints

**Base URL:** `/api/v1`

### Redirect Links

| Method | Endpoint | Response Model |
|--------|----------|-------------|
| GET | `/redirect_links` | `list[RedirectLinkSchema]` |
| POST | `/redirect_links` | `RedirectLinkSchema` |
| GET | `/redirect_links/{short_code}` | `RedirectLinkSchema` |
| PUT | `/redirect_links/active/{short_code}` | `RedirectLinkSchema` |
| DELETE | `/redirect_links/{short_code}` | `RedirectLinkSchema` |

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user (silent if email already exists) |
| POST | `/auth/login` | Login and receive JWT access + refresh tokens |
| POST | `/auth/refresh` | Refresh token pair |
| GET | `/auth/me` | Get current authenticated user (requires Bearer token) |

**For current schemas and examples, see the live OpenAPI docs at `/docs` when the service is running.**

---

## Database Schema

**View current tables:**
```bash
# Redirect links table
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\d"
```

**View current schema:**
```bash
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\d <table_name>"

# For example:
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\d users"
```

---

## Development

### Available Tasks

```bash
# List all tasks
uv run task list

# Common tasks
uv run task start                           # Run production server
uv run task migrate-to-head                 # Apply migrations
uv run task migrate-revision "description"  # Create migration
uv run task lint                            # Run linter
uv run task lint-fix                        # Fix linting issues
uv run task test                            # Run tests
uv run task test-coverage                   # Run tests with coverage
```

### Creating Migrations

After modifying models in `src/<domain>/models.py`:

```bash
# Generate migration
uv run task migrate-revision "add new field"

# Review generated migration in migrations/versions/

# Apply migration
uv run task migrate-to-head
```

### Adding New Endpoints

1. Add route in `src/<domain>/routes.py`
2. Implement logic in `src/<domain>/service.py`
3. Add repository methods if needed in `src/<domain>/repository.py`
4. Update schemas if needed in `src/<domain>/schemas.py`
5. Register new domain exceptions using decorator `@ExceptionRegistry.register(status.HTTP_XXX)`
6. Create new models in `src/<domain>/models.py` and import them in `src/models.py`
7. Include new router in `src/api.py`
8. Regenerate frontend types: `cd apps/frontend && npm run openapi:update`

---

## Testing

```bash
# Run all tests
uv run task test

# Run with coverage
uv run task test-coverage
```

---

## Troubleshooting

### Database connection errors
- Check `POSTGRES_*` environment variables in `.env`
- Verify PostgreSQL is running: `docker compose ps postgres`
- Test connection: `uv run python -c "import asyncio; from src.db import AsyncSessionLocal; asyncio.run(AsyncSessionLocal())"`

### Migration errors
- Check if database exists
- Verify migration files are valid Python
- Check `alembic.ini` configuration

### Import errors
- Ensure you're running from `apps/api-backend` directory
- Check virtual environment: `uv run python --version`

### Service won't start (ValidationError)
- Check that all required environment variables are set in root `.env`:
  - `BACKEND_HOST`, `BACKEND_PORT`
  - `BACKEND_JWT_SECRET_KEY`, `BACKEND_JWT_ALGORITHM`
  - `BACKEND_ACCESS_TOKEN_EXPIRE_MINUTES`, `BACKEND_REFRESH_TOKEN_EXPIRE_DAYS`

### Token errors
- Verify `BACKEND_JWT_SECRET_KEY` is set and secure
- Check that `BACKEND_JWT_ALGORITHM` matches (default: `HS256`)
- Ensure system clock is correct (tokens are time-sensitive)

---

## Updating This Documentation

When modifying this service, update this README if you change:
- Service responsibilities or architecture
- Key files or project structure
- Configuration variables
- Dependencies

**Don't manually document:**
- API endpoints (use OpenAPI at `/docs`)
- Request/response schemas (use OpenAPI)
- Database columns (use migrations or `\d` command)

Always verify root AGENTS.md remains accurate after changes.
