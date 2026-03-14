# Deribit Price Tracker

A backend service that periodically fetches cryptocurrency index prices from the [Deribit API](https://docs.deribit.com/) and exposes them via a REST API built with FastAPI.

## Features

- Fetches `btc_usd` and `eth_usd` index prices from Deribit every minute via Celery Beat
- Stores ticker, price, and UNIX timestamp in PostgreSQL
- REST API with three endpoints, all requiring a `ticker` query parameter
- Fully containerized with Docker Compose

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI |
| Task queue | Celery + Redis |
| HTTP client | aiohttp |
| Database | PostgreSQL |
| ORM | SQLAlchemy (async) |
| DB driver | asyncpg |
| Validation | Pydantic v2 |
| Testing | pytest + pytest-asyncio |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
deribit-price-tracker/
├── app/
│   ├── api/
│   │   └── routers/
│   │       └── prices.py        # FastAPI route handlers
│   ├── clients/
│   │   └── deribit_client.py    # Async HTTP client for Deribit API
│   ├── database/
│   │   ├── connection.py        # Async engine and session factory
│   │   └── models.py            # SQLAlchemy ORM model
│   ├── repositories/
│   │   └── price_repository.py  # All database query logic
│   ├── schemas/
│   │   └── price_schemas.py     # Pydantic response schemas
│   ├── tasks/
│   │   ├── celery_app.py        # Celery configuration and beat schedule
│   │   └── price_tasks.py       # Periodic price fetching task
│   ├── config.py                # Settings loaded from .env
│   └── main.py                  # FastAPI app entry point
├── tests/
│   ├── conftest.py              # Shared test fixtures
│   ├── test_api_routes.py       # API endpoint tests
│   └── test_price_repository.py # Repository unit tests
├── .env.example                 # Environment variable template
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## API Endpoints

All endpoints require the `ticker` query parameter (`btc_usd` or `eth_usd`).

| Method | Endpoint | Description |
|---|---|---|
| GET | `/prices/?ticker=` | All stored records for a ticker |
| GET | `/prices/latest?ticker=` | Most recent price for a ticker |
| GET | `/prices/filter?ticker=&date_from=&date_to=` | Records within a UNIX timestamp range |

Interactive documentation is available at **`http://localhost:8000/docs`** after startup.

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed

### 1. Clone the repository

```bash
git clone https://gitlab.com/your-username/deribit-price-tracker.git
cd deribit-price-tracker
```

### 2. Create the environment file

```bash
cp .env.example .env
```

The default `.env` values work out of the box with Docker Compose — no changes needed.

### 3. Start all services

```bash
docker compose up --build
```

This starts five services:

| Service | Role |
|---|---|
| `db` | PostgreSQL database |
| `redis` | Message broker for Celery |
| `app` | FastAPI application on port 8000 |
| `celery_worker` | Executes price-fetching tasks |
| `celery_beat` | Schedules tasks every 60 seconds |

### 4. Verify it works

Open the API docs in your browser:
```
http://localhost:8000/docs
```

Or test with curl:
```bash
# Wait ~60 seconds for the first price fetch, then:
curl "http://localhost:8000/prices/latest?ticker=btc_usd"
curl "http://localhost:8000/prices/?ticker=eth_usd"
```

### 5. Stop all services

```bash
docker compose down
```

To also remove the stored database data:
```bash
docker compose down -v
```

---

## Running Tests

Tests use mocked database sessions and do not require a running database or Docker.

```bash
# Install dependencies locally
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run all tests
pytest

# Run with output detail
pytest -v
```

---

## Environment Variables

| Variable | Description | Default in .env.example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:password@localhost:5432/deribit_db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `DERIBIT_BASE_URL` | Deribit API base URL | `https://www.deribit.com/api/v2` |

> **Note:** When running via Docker Compose, the hosts in `.env` must match the service names defined in `docker-compose.yml`: `db` for PostgreSQL and `redis` for Redis.

---

## Design Decisions

### Why Celery + Redis instead of APScheduler?

Celery provides production-grade tooling: retry logic on failure, task monitoring via Flower, and the ability to scale workers horizontally without touching the scheduler. APScheduler is simpler but lives inside the application process — if the app crashes, scheduled tasks stop too. Celery Beat and workers are independent processes, which makes the system more resilient.

### Why aiohttp instead of httpx?

The task specification explicitly requires aiohttp. Both libraries are solid async HTTP clients; aiohttp has a slight performance edge under high concurrency due to its connection pooling model.

### Why the Repository pattern?

All database query logic lives in `PriceRepository`, completely isolated from the API layer. The FastAPI route handlers never write SQL — they only call repository methods. This makes unit testing straightforward (mock the repository, not the database), and if the storage layer ever changes, only the repository needs to be updated.

### Why UNIX timestamps instead of datetime?

`BigInteger` UNIX timestamps are timezone-independent, trivial to compare and index in PostgreSQL, and avoid the Y2K38 overflow problem that affects standard 32-bit integers. Clients can convert to any datetime format they need.

### Why separate containers for Celery Beat and Celery Worker?

Beat is the scheduler — it only puts tasks into the Redis queue. Worker is the executor — it picks up and runs those tasks. Keeping them separate means you can run multiple worker instances for higher throughput without duplicating the scheduler, which would cause tasks to be queued multiple times.

### Why `expire_on_commit=False` on the session factory?

With the default `expire_on_commit=True`, SQLAlchemy marks all ORM objects as expired after a commit, requiring a new SELECT query to access any attribute. Since we sometimes need to read the created object after saving it, disabling this avoids unnecessary round-trips to the database.