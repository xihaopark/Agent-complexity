# Agentic Complexity Analyzer V1

Agentic Complexity Analyzer is a conference-oriented open-source platform that evaluates AI agent systems from a single GitHub link. It runs static and dynamic complexity analysis inside Docker sandboxes and produces a structured report with per-metric evidence.

## Architecture

- `apps/web`: Next.js UI for submitting analysis jobs and viewing reports.
- `apps/api`: FastAPI service with public APIs (`/api/v1/analyses/*`).
- `services/orchestrator`: Job orchestration, DB access, status management.
- `workers/sandbox_runner`: Celery worker that executes the analysis pipeline.
- `analyzers`: Static, dynamic, and reporting analyzers.
- `collectors/otel-gateway`: OpenTelemetry collector config.

## Quick Start

1. Copy environment file:

```bash
cp .env.example .env
```

2. Start stack:

```bash
docker compose up --build
```

3. Open:
- Web: http://localhost:3000
- API docs: http://localhost:8000/docs

## API

- `POST /api/v1/analyses`
- `GET /api/v1/analyses/{id}`
- `GET /api/v1/analyses/{id}/report`
- `GET /api/v1/analyses/{id}/metrics`
- `GET /api/v1/analyses/{id}/artifacts`

## Notes

- Default output is metrics only (no composite score).
- Composite score can be enabled via `AGENTIC_COMPOSITE_SCORE_ENABLED=true`.
- Private repo tokens are stored in Redis with short TTL and never persisted in PostgreSQL.
