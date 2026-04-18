# Project Documentation for Agents

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [Service Inventory](#service-inventory)
4. [Discovering Current State](#discovering-current-state)
5. [Communication Contracts](#communication-contracts)
6. [Database Schema](#database-schema)
7. [Quick Start Guide](#quick-start-guide)
8. [Troubleshooting](#troubleshooting)
9. [Updating Documentation](#updating-documentation)

---

## Project Overview

**Project Name:** Redirect

**Purpose:** A complete URL shortening and analytics platform that allows users to create short links, track redirects, and analyze user behavior.

**Tech Stack Summary:**
- **Backend Services:** Go (Gin), Python (FastAPI, Celery)
- **Frontend:** Next.js 16, React 19, TypeScript
- **Databases:** PostgreSQL (primary), Redis (cache), ClickHouse (analytics)
- **Message Broker:** RabbitMQ
- **Infrastructure:** Docker Compose

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│    Frontend     ├────▶│   API Backend    ├────▶│   PostgreSQL     │
│   (Next.js)     │     │  (FastAPI)       │     │ (Redirect Links) │
└─────────────────┘     └───────┬──────────┘     └──────────────────┘
                                │                         ▲
                                │ Manages                 │ Cache Misses
                                ▼                         │
┌─────────────────┐     ┌──────────────────┐              │
│   End Users     ├────▶│  API Redirect    ├──────────────┤
│                 │     │    (Go/Gin)      │              │
└─────────────────┘     └────────┬─────────┘              │
                                 │                        │
                                 │ Publishes              │ Cache Hits
                                 ▼                        ▼
                          ┌──────────────┐        ┌──────────────────┐ 
                          │   RabbitMQ   │        │     Redis        │
                          │  (Events)    │        │    (Cache)       │
                          └──────┬───────┘        └──────────────────┘
                                 │
                                 │ Consumes
                                 ▼
                          ┌──────────────┐
                          │  Analytics   │
                          │   (Celery)   │
                          └──────┬───────┘
                                 │
                                 │ Stores
                                 ▼
                          ┌──────────────┐
                          │  ClickHouse  │
                          │ (Analytics)  │
                          └──────────────┘
```

**Data Flow:**
1. **Link Management:** Frontend → API Backend → PostgreSQL
2. **Redirects:** End Users → API Redirect → PostgreSQL (with Redis cache)
3. **Analytics:** API Redirect → RabbitMQ → Analytics Worker → ClickHouse

---

## Service Inventory

| Service | Technology | Port | Purpose | Documentation |
|---------|------------|------|---------|---------------|
| api-redirect | Go 1.25, Gin | 8080 | High-performance redirect handler | [README](./apps/api-redirect/README.md) |
| api-backend | Python 3.13, FastAPI | 8000 | REST API for managing links | [README](./apps/api-backend/README.md) |
| analytics | Python 3.13, Celery | - | Background analytics worker | [README](./apps/analytics/README.md) |
| frontend | Next.js 16, React 19 | 3000 | Web UI for link management | [README](./apps/frontend/README.md) |

---

## Discovering Current State

### API Endpoints

The API Backend provides auto-generated OpenAPI documentation:

```bash
# Start the API Backend service, then visit:
http://localhost:8000/docs        # Swagger UI
http://localhost:8000/redoc       # ReDoc
http://localhost:8000/openapi.json # OpenAPI specification
```

**Or query via CLI:**
```bash
curl http://localhost:8000/openapi.json | jq
```

### Database Schemas

**PostgreSQL (api-backend):**
```bash
# Connect to database
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB

# List tables
\dt

# Describe table
\d redirect_links
```

**ClickHouse (analytics):**
```bash
# Connect to ClickHouse
docker compose exec clickhouse clickhouse-client

# List tables
SHOW TABLES;

# Describe table
DESCRIBE redirect_events;
```

### Message Queue

**RabbitMQ Management UI:**
```
http://localhost:15672
```

**Or via CLI:**
```bash
# List queues
docker compose exec rabbitmq rabbitmqctl list_queues

# List bindings
docker compose exec rabbitmq rabbitmqctl list_bindings
```

### Project Structure

Use standard tools to explore:
```bash
# List Go source files
find apps/api-redirect -name "*.go" | head -20

# List Python modules
find apps/api-backend/src -name "*.py" | head -20

# List React components
find apps/frontend/src -name "*.tsx" | head -20
```

---

## Communication Contracts

### REST API Contracts

**Base URL:** `http://localhost:8000/api/v1`

**Discovery:** API documentation is auto-generated from code. See [Discovering Current State](#discovering-current-state) section.

**Key Concept:** The API provides CRUD operations for redirect links. For current endpoints, request/response schemas, and examples, refer to the live OpenAPI documentation at `/docs` when the service is running.

---

### Message Queue Contracts

**Broker:** RabbitMQ

**Queue:** `redirect_events`

**Core Message Fields:**
- `short_code` - Short link identifier
- `user_agent` - Client User-Agent string
- `ip` - Client IP address
- `event_time` - Event timestamp

**Discovery:** For the complete message schema, see:
- **Publisher:** `apps/api-redirect/internal/domain/redirect_event.go`
- **Consumer:** `apps/analytics/src/redirect_events/schemas.py`

**Publisher:** [api-redirect](./apps/api-redirect/README.md)

**Consumer:** [analytics](./apps/analytics/README.md)

---

## Database Schema

### PostgreSQL (api-backend)

**Core Table:** `redirect_links`

**Key Fields:**
- `id` (UUID, PK) - Unique identifier
- `short_code` (VARCHAR, UNIQUE) - Short URL code
- `target_url` (VARCHAR) - Destination URL
- `is_active` (BOOLEAN) - Link status
- `created_at`, `updated_at` (TIMESTAMP) - Timestamps

**Discovery:** For complete schema, migrations, and indexes:
```bash
# View migration files
ls apps/api-backend/migrations/versions/

# View current table structure (requires running database)
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\d redirect_links"
```

---

### ClickHouse (analytics)

**Core Table:** `redirect_events`

**Key Fields:**
- Event data: `short_code`, `target_url`, `event_date`
- Parsed User-Agent: `browser`, `os`, `device`
- Geolocation: `country`, `city`
- Raw data: `ip`

**Discovery:** For complete schema and migrations:
```bash
# View migration files
ls apps/analytics/migrations/

# View current table structure (requires running database)
docker compose exec clickhouse clickhouse-client -q "DESCRIBE redirect_events"
```

---

## Quick Start Guide

### Prerequisites

- Docker and Docker Compose
- Go 1.25+ (for api-redirect)
- Python 3.13+ with uv (for api-backend, analytics)
- Node.js 20+ (for frontend)

### Environment Setup

1. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

2. Start infrastructure services:
```bash
docker compose up -d
```

3. Run database migrations:
```bash
# PostgreSQL
cd apps/api-backend && uv run task migrate-to-head

# ClickHouse
cd apps/analytics && uv run clickhouse-migrations migrate
```

### Running Services

| Service | Command | URL |
|---------|---------|-----|
| api-redirect | `cd apps/api-redirect && go run cmd/redirect/main.go` | http://localhost:8080 |
| api-backend | `cd apps/api-backend && uv run task start-app` | http://localhost:8000 |
| analytics | `cd apps/analytics && uv run celery -A src.main worker --loglevel=info` | - |
| frontend | `cd apps/frontend && npm run dev` | http://localhost:3000 |

### Service Ports Reference

| Service | Port | Description |
|---------|------|-------------|
| api-redirect | 8080 | Redirect handler |
| api-backend | 8000 | Management API |
| frontend | 3000 | Web UI |
| PostgreSQL | 5432 | Main database |
| Redis | 6379 | Cache |
| RabbitMQ | 5672 | Message broker |
| RabbitMQ Mgmt | 15672 | Management UI |
| ClickHouse | 8123 | Analytics database |

---

## Troubleshooting

### Services Won't Start
- Check `.env` file exists and is configured
- Verify Docker containers are running: `docker compose ps`
- Check logs: `docker compose logs <service>`

### Database Connection Errors
- Verify PostgreSQL is healthy: `docker compose ps postgres`
- Check credentials in `.env`
- Ensure migrations are applied

### RabbitMQ Connection Issues
- Check RabbitMQ is running: `docker compose ps rabbitmq`
- Verify credentials in `.env`
- Management UI: http://localhost:15672

---

## Updating Documentation

When making changes to the system, update the relevant documentation:

### Code Changes

| Change Type | Files to Update |
|-------------|-----------------|
| **New API endpoint** | Add to `apps/api-backend/src/redirect_link/routes.py` - OpenAPI auto-generates docs |
| **API schema changes** | Update Pydantic schemas in `apps/api-backend/src/redirect_link/schemas.py` |
| **Database schema (PostgreSQL)** | Create Alembic migration: `uv run task migrate-revision "description"` |
| **Database schema (ClickHouse)** | Add migration file in `apps/analytics/migrations/` |
| **Message event fields** | Update both `apps/api-redirect/internal/domain/redirect_event.go` and `apps/analytics/src/redirect_events/schemas.py` |
| **New service** | Add to root `AGENTS.md` service inventory and create service `README.md` |

### Documentation Principles

1. **Don't duplicate volatile information** - Link to live docs (OpenAPI, database) instead of copying
2. **Document architecture and concepts** - Explain how things work, not just what exists
3. **Provide discovery instructions** - Tell agents how to find current state
4. **Keep service READMEs focused** - Purpose, key concepts, running instructions, troubleshooting

### Verification Checklist

After making changes, verify:
- [ ] OpenAPI docs show new endpoints/schemas (if applicable)
- [ ] Database migrations are applied successfully
- [ ] Service README mentions the change if it's a key concept
- [ ] Root AGENTS.md still accurate (service inventory, architecture)
