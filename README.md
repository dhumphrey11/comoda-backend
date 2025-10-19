# Comoda Backend

FastAPI-based backend services and API for the Comoda platform.

## Overview

This repository contains the backend services, API endpoints, and business logic for the Comoda application. It uses FastAPI, SQLAlchemy, and PostgreSQL for transactional data, plus Google BigQuery for analytics.

## Tech Stack

- Framework: FastAPI
- Database: PostgreSQL (SQLAlchemy + psycopg v3)
- Async HTTP: httpx
- Logging: Structured JSON logs
- Analytics: Google BigQuery
- Runtime: Uvicorn
- Containerization: Docker / Cloud Run

## Layout

Key files and folders:

- `main.py` — FastAPI app entrypoint
- `routers/` — API route modules (ingest, signals, trades, admin)
- `services/` — External API, ML, trading, and BigQuery clients
- `utils/` — Logging, DB helpers, rate-limiters
- `models/` — Pydantic schemas
- `requirements.txt` — Python dependencies
- `Dockerfile` — Container image build
- `cloudbuild.yaml` — Build/deploy to Cloud Run
- `docker-compose.yml` — Local Postgres for development

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (optional but recommended for local DB)

### Local Database (optional but recommended)

Start a local Postgres using Docker Compose:

```bash
docker compose up -d postgres
```

This exposes Postgres on `localhost:5432` with user/password `postgres` and database `comoda`.

### Local App Setup

1) Create a virtual environment and install deps

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Configure env vars

```bash
cp .env.example .env
# If using local Postgres via compose, set:
# DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/comoda
```

3) Run the API

```bash
uvicorn main:app --reload --port 8000
```

### API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

See `.env.example`. Notable variables:

- `DATABASE_URL`: Postgres URL (use `postgresql+psycopg://...`)
- `COINAPI_KEY`, `SANTIMENT_API_KEY`: External data provider keys
- `ML_SERVICE_BASE`: Base URL for ML service
- `GCP_PROJECT_ID`, `BQ_DATASET`: BigQuery config

## Docker/Cloud Run

The included `Dockerfile` builds the API image. `cloudbuild.yaml` contains a sample Cloud Build pipeline to build, push, and deploy to Cloud Run using Artifact Registry. Ensure the required secrets and roles are configured (see infra repo).

## Testing

Pytest scaffolding not yet added. Recommended next steps:

- Add unit tests for routers and services
- Add an integration test that boots the app and hits `/health`

## Contributing

1. Create a feature branch: `git checkout -b feature/name`
2. Make your changes and add tests
3. Run the app and tests locally
4. Submit a PR
