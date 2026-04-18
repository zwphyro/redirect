# Analytics Service

## Overview

**Purpose:** Background worker that consumes redirect events from RabbitMQ, enriches them with user agent and IP geolocation data, and stores in ClickHouse.

**Technology:** Python 3.13, Celery, ClickHouse

**Type:** Background Worker (no HTTP port)

---

## Responsibilities

- Consume messages from RabbitMQ queue `redirect_events`
- Parse User-Agent strings (device, browser, OS)
- Geolocate IP addresses via external API
- Batch insert enriched events into ClickHouse

---

## Project Structure

**Architecture:** Celery worker with modular processors:
- `src/` - Application code
- `src/redirect_events/` - Event processing module
- `src/user_agent/` - User-Agent parsing
- `src/ip/` - IP geolocation
- `migrations/` - ClickHouse migrations

**Key Files:**
- `src/main.py` - Celery app initialization
- `src/redirect_events/task.py` - Celery task handlers
- `src/redirect_events/service.py` - Event enrichment logic
- `src/redirect_events/repository.py` - ClickHouse client
- `src/user_agent/service.py` - User-Agent parsing
- `src/ip/service.py` - IP geolocation service
- `src/clickhouse.py` - ClickHouse connection

**Explore the codebase:**
```bash
# List all Python files
find apps/analytics/src -name "*.py" | head -20

# View migrations
ls apps/analytics/migrations/
```

---

## Dependencies

- **Celery** - Distributed task queue
- **clickhouse-connect** - ClickHouse Python driver
- **clickhouse-migrations** - Database migrations
- **user-agents** - User-Agent string parsing
- **requests** - HTTP client for IP geolocation
- **pandas** - Data manipulation for batch inserts

---

## Configuration

Environment variables (see root `.env.example`):

| Variable | Description |
|----------|-------------|
| `CLICKHOUSE_DB` | ClickHouse database name |
| `CLICKHOUSE_HOST` | ClickHouse host |
| `CLICKHOUSE_PORT` | ClickHouse port (HTTP) |
| `CLICKHOUSE_USER` | ClickHouse user |
| `CLICKHOUSE_PASSWORD` | ClickHouse password |
| `RABBITMQ_HOST` | RabbitMQ host |
| `RABBITMQ_PORT` | RabbitMQ port |
| `RABBITMQ_DEFAULT_USER` | RabbitMQ user |
| `RABBITMQ_DEFAULT_PASS` | RabbitMQ password |
| `IP_API_HOST` | IP geolocation API host (default: http://ip-api.com) |
| `IP_API_TIMEOUT_SECONDS` | API timeout (default: 2.0) |
| `IP_API_MAX_RETRIES` | API retry count (default: 3) |

---

## Running the Service

### Prerequisites

- Python 3.13+
- uv package manager
- RabbitMQ running (via Docker Compose)
- ClickHouse running (via Docker Compose)

### Setup

```bash
cd apps/analytics
uv sync
```

### Run Migrations

```bash
# Apply all ClickHouse migrations
uv run clickhouse-migrations migrate
```

### Start the Worker

```bash
# Start Celery worker
uv run celery -A src.main worker --loglevel=info

# With concurrency (optional)
uv run celery -A src.main worker --loglevel=info --concurrency=4
```

---

## Message Consumption

This service consumes events from RabbitMQ queue `redirect_events`.

**Event Structure (from api-redirect):**
```json
{
  "event_time": "2024-01-15T10:30:00Z",
  "short_code": "abc123",
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0 ...",
  "language": "en-US",
  "origin": "https://google.com",
}
```

**Enrichment Process:**
1. Parse User-Agent → browser, browser_version, os, os_version, device
2. Geolocate IP → country, city
3. Insert enriched data into ClickHouse

**View message schema:**
```bash
cat apps/analytics/src/redirect_events/schemas.py
```

See [root AGENTS.md](../../AGENTS.md) for message contract details.

---

## Database Schema

**Core Table:** `redirect_events`

| Column | Type | Description |
|--------|------|-------------|
| short_code | String | Short link code |
| browser | String | Parsed browser name |
| browser_version | String | Browser version |
| os | String | Operating system |
| os_version | String | OS version |
| device | String | Device type |
| ip | String | Client IP |
| country_code | String | Geolocated country |
| city | String | Geolocated city |
| origin | String | Referrer URL |
| language | String | Accept-Language |
| event_time | DateTime | Event timestamp |

**View current schema:**
```bash
docker compose exec clickhouse clickhouse-client -q "DESCRIBE redirect_events"
```

The ClickHouse schema for `redirect_events` must match the `RedirectEventSchema` schema from `src/redirect_events/schemas.py`.

---

## Development

### Creating Migrations

Create SQL files in `migrations/` with sequential numbering:

```sql
-- migrations/0006_add_new_column.sql
ALTER TABLE redirect_events
ADD COLUMN new_field String DEFAULT '';
```

Apply migrations:
```bash
uv run clickhouse-migrations migrate
```

### Monitoring Tasks

```bash
# Flower (Celery monitoring) - optional
uv run celery -A src.main flower
```

### Processing Logic

The main task in `src/redirect_events/task.py` uses Celery batches for efficient bulk inserts into ClickHouse.

---

## Troubleshooting

### Worker won't start
- Check RabbitMQ is running: `docker compose ps rabbitmq`
- Check ClickHouse is running: `docker compose ps clickhouse`
- Verify environment variables in `.env`

### Messages not being consumed
- Check RabbitMQ queue exists: `docker compose exec rabbitmq rabbitmqctl list_queues`
- Verify queue has messages: Management UI at http://localhost:15672
- Check worker logs for errors

### ClickHouse connection errors
- Check `CLICKHOUSE_*` environment variables
- Verify ClickHouse is healthy: `docker compose ps clickhouse`
- Test connection: `curl http://localhost:8123/ping`

### IP geolocation failures
- Check `IP_API_HOST` configuration
- Verify network connectivity to ip-api.com
- Check rate limits (free tier: 45 requests/minute)

### Data not appearing in ClickHouse
- Check worker logs for insert errors
- Verify table schema matches migration
- Check ClickHouse logs: `docker compose logs clickhouse`

---

## Updating This Documentation

When modifying this service, update this README if you change:
- Service responsibilities or architecture
- Key files or project structure
- Configuration variables
- Dependencies

**Don't manually document:**
- Database columns (use ClickHouse `DESCRIBE` command)
- Message schema fields (check `src/redirect_events/schemas.py`)

Always verify root AGENTS.md remains accurate after changes.
