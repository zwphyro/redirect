# API Redirect Service

## Overview

**Purpose:** High-performance redirect handler that processes incoming short URL requests, retrieves target URLs, and publishes analytics events.

**Technology:** Go 1.25, Gin framework

**Port:** 8080

---

## Responsibilities

- Handle GET `/:short_code` requests
- Lookup redirect links from PostgreSQL (with Redis caching)
- Publish redirect events to RabbitMQ for analytics
- Track request timing metrics

---

## Project Structure

**Architecture:** Clean architecture with layers:
- `cmd/` - Application entry point
- `internal/handler/` - HTTP handlers
- `internal/service/` - Business logic
- `internal/repository/` - Data access
- `internal/broker/` - Message broker client
- `internal/domain/` - Domain models
- `internal/middleware/` - HTTP middleware
- `internal/config/` - Configuration

**Key Files:**
- `cmd/main.go` - Application initialization
- `internal/handler/redirect.go` - HTTP handlers
- `internal/service/redirect.go` - Business logic
- `internal/service/analytics.go` - Event publishing
- `internal/repository/postgresql.go` - Database access
- `internal/broker/rabbitmq.go` - RabbitMQ client
- `internal/domain/redirect_event.go` - Event schema

**Explore the codebase:**
```bash
# List all Go files
find apps/api-redirect -name "*.go" | head -20

# View main package files
ls apps/api-redirect/cmd/redirect/

# View internal packages
ls apps/api-redirect/internal/
```

---

## Dependencies

- **PostgreSQL** (via GORM) - Stores redirect links
- **Redis** (go-redis) - Caches redirect links
- **RabbitMQ** (amqp091-go) - Publishes analytics events

---

## Configuration

Environment variables (see root `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `HTTP_SERVER_PORT` | Server port | `8080` |
| `HTTP_SERVER_TIMEOUT` | Request timeout | `1s` |
| `POSTGRES_*` | PostgreSQL connection | - |
| `REDIS_*` | Redis connection | - |
| `RABBITMQ_*` | RabbitMQ connection | - |

---

## Running the Service

### Prerequisites

- Go 1.25+
- PostgreSQL running (via Docker Compose)
- Redis running (via Docker Compose)
- RabbitMQ running (via Docker Compose)

### Start the Service

```bash
cd apps/api-redirect
go run cmd/main.go
```

The server will start on port 8080.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/:short_code` | Redirect to target URL |

**Example:**
```bash
curl -v http://localhost:8080/abc123
# Returns 302 redirect to target_url
```

---

## Message Publishing

This service publishes events to RabbitMQ on every successful redirect.

**Queue:** `redirect_events`

**Event Schema:** See `internal/domain/redirect_event.go`

```bash
# View the event structure
cat apps/api-redirect/internal/domain/redirect_event.go
```

**Key fields:**
- `short_code` - Short link identifier
- `target_url` - Destination URL
- `user_agent` - Client User-Agent
- `ip_address` - Client IP
- `timestamp` - Event time
- `request_duration_ms` - Processing time

See [root AGENTS.md](../../AGENTS.md) for message contract details.

---

## Development

### Adding New Middleware

1. Create file in `internal/middleware/`
2. Implement middleware function: `func gin.HandlerFunc`
3. Register in `cmd/main.go`

### Modifying Event Schema

1. Update `internal/domain/redirect_event.go`
2. Update `internal/service/analytics.go` to populate new fields
3. Update consumer in [analytics service](../analytics/)
4. Update root AGENTS.md contract documentation

---

## Troubleshooting

### Service won't start
- Check PostgreSQL is running: `docker compose ps postgres`
- Check Redis is running: `docker compose ps redis`
- Check RabbitMQ is running: `docker compose ps rabbitmq`
- Verify `.env` file exists in project root

### Database connection errors
- Check `POSTGRES_*` environment variables
- Verify database exists and is migrated (run migrations in api-backend)

### Cache not working
- Check `REDIS_*` environment variables
- Verify Redis password is correct

### Events not publishing
- Check `RABBITMQ_*` environment variables
- Verify RabbitMQ queue exists
- Check RabbitMQ logs: `docker compose logs rabbitmq`

---

## Updating This Documentation

When modifying this service, update this README if you change:
- Service responsibilities or architecture
- Key files or project structure
- Configuration variables
- Dependencies

**Don't update:**
- API endpoint details (check OpenAPI at runtime)
- Database schema (check migrations)
- Message schema (check domain models)

Always verify root AGENTS.md remains accurate after changes.
