# Agentic Complexity Analyzer V1 Architecture

## Core path

1. Web submits `repo_url + ref + optional run_spec + optional token`.
2. API writes `analysis_jobs` row and enqueues Celery task.
3. Worker clones repository, resolves run spec, and runs static analyzers.
4. Worker instruments Python code with `libcst` and executes dynamic runs in Docker sandbox.
5. Runtime events are aggregated into dynamic metrics and confidence intervals.
6. Report generator exports Markdown/HTML/JSON/Parquet artifacts.
7. API serves job status, metrics, report metadata, and artifact URIs.

## Failure handling

- Clone/static failure: mark `failed` and emit error artifact.
- Dynamic failure: keep static metrics and available dynamic evidence, mark `partial`.
- Non-zero runtime exit: still collect artifacts and mark `partial`.

## Security baseline

- Docker container isolation with CPU/memory/pid limits.
- Non-root execution user.
- Ephemeral auth token stored in Redis (TTL) and not persisted in DB.
- Artifact-only write path; source mounted read-only inside sandbox.
