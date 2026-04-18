# Project Documentation for Agents

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [Service Details](#service-details)
4. [Communication Contracts](#communication-contracts)
5. [Database Schema](#database-schema)
6. [Development Guide](#development-guide)

---

## Project Overview

**Project Name:** Redirect URL Management System

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
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    Frontend     │────▶│   API Backend    │────▶│   PostgreSQL    │
│   (Next.js)     │     │  (FastAPI)       │     │  (Redirect Links)│
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                │
                                │ Manages
                                ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   End Users     │────▶│  API Redirect    │────▶│     Redis       │
│                 │     │    (Go/Gin)      │     │    (Cache)      │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                                 │ Publishes
                                 ▼
                          ┌──────────────┐
                          │   RabbitMQ   │
                          │  (Events)    │
                          └──────┬───────┘
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

---

## Service Details

### 1. API Redirect Service (`apps/api-redirect/`)

**Purpose:** High-performance redirect handler that processes incoming short URL requests, retrieves target URLs, and publishes analytics events.

**Technology:** Go 1.25, Gin framework

**Key Responsibilities:**
- Handle GET `/:short_code` requests
- Lookup redirect links from PostgreSQL (with Redis caching)
- Publish redirect events to RabbitMQ for analytics
- Track request timing metrics

**Dependencies:**
- PostgreSQL (via GORM)
- Redis (go-redis)
- RabbitMQ (amqp091-go)

**Key Files:**
- `cmd/redirect/main.go` - Application entry point
- `internal/handler/redirect.go` - HTTP handlers
- `internal/service/redirect.go` - Business logic
- `internal/service/analytics.go` - Event publishing
- `internal/repository/postgresql.go` - Data access layer
- `internal/broker/rabbitmq.go` - Message broker client

**Configuration:** See `.env.example` for `REDIS_*`, `POSTGRES_*`, `RABBITMQ_*` variables

---

### 2. API Backend Service (`apps/api-backend/`)

**Purpose:** REST API for managing redirect links (CRUD operations).

**Technology:** Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic

**Key Responsibilities:**
- Create, read, update, delete redirect links
- Generate unique short codes
- Provide OpenAPI specification for frontend

**API Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/redirect_links` | List all redirect links |
| POST | `/api/v1/redirect_links` | Create new redirect link |
| GET | `/api/v1/redirect_links/{id}` | Get specific link |
| PUT | `/api/v1/redirect_links/{id}` | Update redirect link |
| DELETE | `/api/v1/redirect_links/{id}` | Delete redirect link |

**Key Files:**
- `src/main.py` - FastAPI application
- `src/redirect_link/routes.py` - API routes
- `src/redirect_link/service.py` - Business logic
- `src/redirect_link/models.py` - SQLAlchemy models
- `src/redirect_link/short_code.py` - Short code generation

**Database Migrations:**
```bash
# Create new migration
uv run task migrate-revision "description"

# Apply migrations
uv run task migrate-to-head
```

---

### 3. Analytics Service (`apps/analytics/`)

**Purpose:** Background worker that consumes redirect events, enriches them with user agent and IP data, and stores in ClickHouse.

**Technology:** Python 3.13, Celery, ClickHouse

**Key Responsibilities:**
- Consume messages from RabbitMQ
- Parse User-Agent strings (device, browser, OS)
- Geolocate IP addresses
- Batch insert events into ClickHouse

**Key Files:**
- `src/main.py` - Celery application setup
- `src/redirect_events/task.py` - Celery task handlers
- `src/redirect_events/service.py` - Processing logic
- `src/redirect_events/repository.py` - ClickHouse client
- `src/user_agent/` - User-Agent parsing
- `src/ip/` - IP geolocation

**Database Migrations:**
Located in `migrations/` directory, applied via `clickhouse-migrations`

---

### 4. Frontend Service (`apps/frontend/`)

**Purpose:** Web UI for managing redirect links with server-side rendering.

**Technology:** Next.js 16, React 19, TypeScript, Tailwind CSS, shadcn/ui

**Key Responsibilities:**
- Display list of redirect links
- Create new short links
- Edit and delete existing links
- API client auto-generated from OpenAPI spec

**Key Files:**
- `src/app/page.tsx` - Main page
- `src/app/list.tsx` - Links list component
- `src/lib/api/client.ts` - API client
- `src/lib/api/v1.d.ts` - Auto-generated TypeScript types

**API Integration:**
```bash
# Update API types from running backend
npm run openapi:update
```

---

## Communication Contracts

### Event Message Format (RabbitMQ)

**Queue:** `redirect_events`

**Message Structure:**
```json
{
  "short_code": "abc123",
  "target_url": "https://example.com",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
  "ip_address": "192.168.1.1",
  "referer": "https://google.com",
  "language": "en-US",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_duration_ms": 45
}
```

**Publisher:** `api-redirect` service (`internal/service/analytics.go`)

**Consumer:** `analytics` service (`src/redirect_events/task.py`)

---

### API Contracts

#### Redirect Link Model

```json
{
  "id": "uuid",
  "short_code": "abc123",
  "target_url": "https://example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### Create Redirect Link Request

```json
{
  "target_url": "https://example.com"
}
```

#### Create Redirect Link Response

```json
{
  "id": "uuid",
  "short_code": "abc123",
  "target_url": "https://example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

---

## Database Schema

### PostgreSQL (api-backend)

**Table:** `redirect_links`

| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY |
| short_code | VARCHAR | UNIQUE, NOT NULL |
| target_url | VARCHAR | NOT NULL |
| is_active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |

### ClickHouse (analytics)

**Table:** `redirect_events`

| Column | Type | Description |
|--------|------|-------------|
| short_code | String | Short link code |
| target_url | String | Destination URL |
| user_agent | String | Raw User-Agent |
| browser | String | Parsed browser name |
| browser_version | String | Browser version |
| os | String | Operating system |
| os_version | String | OS version |
| device | String | Device type |
| ip_address | String | Client IP |
| country | String | Geolocated country |
| city | String | Geolocated city |
| referer | String | Referrer URL |
| language | String | Accept-Language |
| timestamp | DateTime | Event timestamp |
| request_duration_ms | UInt32 | Request processing time |

---

## Development Guide

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

3. Run migrations:
```bash
# PostgreSQL (api-backend)
cd apps/api-backend
uv run task migrate-to-head

# ClickHouse (analytics)
cd apps/analytics
uv run clickhouse-migrations migrate
```

### Running Services

#### API Redirect (Go)
```bash
cd apps/api-redirect
go run cmd/redirect/main.go
# Server starts on port from env (default: 8080)
```

#### API Backend (Python)
```bash
cd apps/api-backend
uv run task start-app-dev
# Server starts on http://localhost:8000
```

#### Analytics Worker (Python)
```bash
cd apps/analytics
uv run celery -A src.main worker --loglevel=info
```

#### Frontend (Next.js)
```bash
cd apps/frontend
npm run dev
# Server starts on http://localhost:3000
```

### Service Ports

| Service | Port | Description |
|---------|------|-------------|
| api-redirect | 8080 | Redirect handler |
| api-backend | 8000 | Management API |
| frontend | 3000 | Web UI |
| PostgreSQL | 5432 | Main database |
| Redis | 6379 | Cache |
| RabbitMQ | 5672 | Message broker |
| RabbitMQ Mgmt | 15672 | RabbitMQ UI |
| ClickHouse | 8123 | Analytics DB |

### Testing

```bash
# API Backend
cd apps/api-backend
uv run task test

# Frontend
cd apps/frontend
npm run lint
```

---

## Common Tasks for Agents

### Adding a New API Endpoint

1. Define route in `apps/api-backend/src/redirect_link/routes.py`
2. Implement service logic in `apps/api-backend/src/redirect_link/service.py`
3. Add repository methods if needed
4. Regenerate frontend types: `cd apps/frontend && npm run openapi:update`

### Modifying Database Schema

1. Update model in `apps/api-backend/src/redirect_link/models.py`
2. Generate migration: `uv run task migrate-revision "description"`
3. Apply migration: `uv run task migrate-to-head`

### Adding Analytics Event Fields

1. Update event schema in `apps/api-redirect/internal/domain/redirect_event.go`
2. Update publisher in `apps/api-redirect/internal/service/analytics.go`
3. Update consumer in `apps/analytics/src/redirect_events/`
4. Update ClickHouse schema migration

---

## Troubleshooting

### Services won't start
- Check `.env` file exists and is configured
- Verify Docker containers are running: `docker compose ps`
- Check logs: `docker compose logs <service>`

### Database connection errors
- Verify PostgreSQL is healthy: `docker compose ps postgres`
- Check credentials in `.env`
- Ensure migrations are applied

### RabbitMQ connection issues
- Check RabbitMQ is running: `docker compose ps rabbitmq`
- Verify credentials in `.env`
- Management UI: http://localhost:15672 (guest/guest)

---

*Last updated: 2024-01-15*

