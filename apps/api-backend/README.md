# API Backend Service

## Overview

**Purpose:** REST API for managing redirect links (CRUD operations).

**Technology:** Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic

**Port:** 8000

---

## Responsibilities

- Create, read, update, delete redirect links
- Generate unique short codes
- Provide OpenAPI specification for frontend
- Database migrations via Alembic

---

## Project Structure

**Architecture:** Layered architecture with FastAPI:
- `src/` - Application code
- `src/redirect_link/` - Domain module for redirect links
- `migrations/` - Alembic database migrations

**Key Files:**
- `src/main.py` - FastAPI application setup
- `src/api.py` - Router aggregation
- `src/<domain>/routes.py` - API endpoints
- `src/<domain>/service.py` - Business logic
- `src/<domain>/models.py` - SQLAlchemy models
- `src/<domain>/repository.py` - Data access
- `src/<domain>/schemas.py` - Pydantic schemas
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
# Development (with auto-reload)
uv run task start-app-dev

# Production
uv run task start-app
```

The API will be available at http://localhost:8000

**API Documentation (auto-generated):**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

---

## API Endpoints

**Base URL:** `/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/redirect_links` | List all redirect links |
| POST | `/redirect_links` | Create new redirect link |
| GET | `/redirect_links/{id}` | Get specific link by ID |
| PUT | `/redirect_links/{id}` | Update redirect link |
| DELETE | `/redirect_links/{id}` | Delete redirect link |

**For current schemas and examples, see the live OpenAPI docs at `/docs` when the service is running.**

---

## Database Schema

**Core Table:** `redirect_links`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| short_code | VARCHAR | UNIQUE, NOT NULL | Short URL code |
| target_url | VARCHAR | NOT NULL | Destination URL |
| is_active | BOOLEAN | DEFAULT TRUE | Link status |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update time |

**View current schema:**
```bash
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\d redirect_links"
```

---

## Development

### Available Tasks

```bash
# List all tasks
uv run task list

# Common tasks
uv run task start-app-dev       # Run with auto-reload
uv run task migrate-to-head     # Apply migrations
uv run task migrate-revision "description"  # Create migration
uv run task lint                # Run linter
uv run task lint-fix            # Fix linting issues
uv run task test                # Run tests
uv run task test-coverage       # Run tests with coverage
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
5. Regenerate frontend types: `cd apps/frontend && npm run openapi:update`

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
- Test connection: `uv run python -c "import asyncio; from src.db import async_session; asyncio.run(async_session())"`

### Migration errors
- Check if database exists
- Verify migration files are valid Python
- Check `alembic.ini` configuration

### Import errors
- Ensure you're running from `apps/api-backend` directory
- Check virtual environment: `uv run python --version`

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
