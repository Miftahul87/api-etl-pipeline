# API Data Integration & ETL Pipeline

A portfolio-grade backend ETL service built with **Python, FastAPI, SQLAlchemy, and PostgreSQL**. It extracts paginated JSON from a REST API, validates and normalizes records, and loads them into a relational database using idempotent upserts.

> This repository includes a deterministic mock source so the entire pipeline can be demonstrated locally without API keys or external services.

## Highlights
- REST API to trigger an ETL run and inspect execution status/history.
- Paginated source extraction with timeouts, retry/backoff, and configurable source URL.
- Transformation layer: field normalization, type coercion, validation, and rejection accounting.
- PostgreSQL persistence through SQLAlchemy 2.x; SQLite is supported for local tests.
- Idempotent loading using a unique external ID and database upsert semantics.
- Run-level metrics: extracted, loaded, rejected, duration, status, and error summary.
- Docker Compose setup, OpenAPI/Swagger docs, and automated tests.

## Architecture

```text
REST Source API
     |
     v
Extractor (pagination + retries)
     |
     v
Transformer (normalize + validate)
     |
     v
Loader (SQLAlchemy + idempotent upsert)
     |
     v
PostgreSQL  <--- FastAPI: trigger / status / records
```

## Run with Docker

Requirements: Docker Desktop.

```bash
cp .env.example .env
docker compose up --build
```

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Trigger a pipeline: `POST http://localhost:8000/trigger`
- Latest status: `GET http://localhost:8000/status`
- Stored records: `GET http://localhost:8000/records`
- Run history: `GET http://localhost:8000/runs`

The mock source is exposed at `GET /mock-source?page=1&page_size=10`. The default ETL source URL points to this endpoint.

### Example trigger

```bash
curl -X POST http://localhost:8000/trigger
```

### Inspect status and data

```bash
curl http://localhost:8000/status
curl "http://localhost:8000/records?limit=20"
curl http://localhost:8000/runs
```

## Run locally (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=sqlite:///./etl.db
export SOURCE_API_URL=http://127.0.0.1:8000/mock-source
uvicorn app.main:app --reload
```

In another terminal, call `POST /trigger`.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Database/API health |
| POST | `/trigger` | Starts an ETL run in the background |
| GET | `/status` | Latest run status |
| GET | `/runs` | Recent execution history |
| GET | `/records` | Query loaded records |
| GET | `/mock-source` | Paginated deterministic source for demo |

## Data contract

Source records are mapped to:
- `external_id` — stable unique source identifier
- `name` — trimmed title/name
- `email` — normalized lowercase email (optional)
- `amount` — numeric value (optional)
- `source_updated_at` — source timestamp (optional)
- `payload` — original source JSON for traceability

Records without a valid `external_id` or name are rejected and counted. Existing records are updated by `external_id`, making reruns idempotent.

## Configuration

See `.env.example`. Important settings:
- `DATABASE_URL`
- `SOURCE_API_URL`
- `SOURCE_PAGE_SIZE`
- `SOURCE_MAX_PAGES`
- `HTTP_TIMEOUT_SECONDS`
- `MAX_RETRIES`

## Tests

```bash
pytest -q
```

Tests use an isolated SQLite database and mocked HTTP responses; they do not require PostgreSQL or a live source API.

## Resume wording (only after you run and verify it)

- Built a FastAPI-based ETL service that extracts paginated REST API data, validates and normalizes JSON records, and loads them into PostgreSQL using idempotent upserts.
- Implemented retry/backoff, execution tracking, run metrics, Docker Compose, and automated tests for extraction, transformation, and persistence.
