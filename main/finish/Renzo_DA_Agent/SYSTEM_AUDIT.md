# SYSTEM_AUDIT (2026-02-11)

## Scope

- Renzo core (`frontend`, `backend`, `app`, `docker-compose`)
- Standalone paths: `./workflow_pool` (in-repo)
- Delivery target: Docker-first stability baseline with optional local dev mode

## P0 Fixes Applied

1. Startup and port system
- `docker-compose.yml` switched to configurable host ports:
  - `BACKEND_PORT` default `18000`
  - `FRONTEND_PORT` default `13000`
- Added backend `healthcheck` on `/api/health`
- Added service restart policy (`unless-stopped`)
- Frontend now depends on backend `service_healthy`
- Mounted docker socket by default for workflow execution
- Backend image now includes Docker CLI binary (no host docker binary bind)

2. Runtime configuration baseline
- Added `renzo/.env.example` with:
  - docker and local ports
  - runtime install switches
  - nextflow/snakemake target versions
  - integration mount paths

3. Local dev optional mode (5173/8000)
- Reworked `start_local.sh` into command-style controller:
  - `start|stop|restart|status|logs`
- Added `backend/scripts/backend-daemon.sh`
- Kept `frontend/scripts/frontend-daemon.sh` as frontend daemon backend
- Local mode now consistently uses `python3`

4. API health and observability
- Added `/health` compatibility alias
- Added `/api/ready` readiness endpoint with:
  - app path checks (`data_root`, `workflow_pool`)
  - workflow runtime checks (nextflow/snakemake/docker-cli/docker.sock)
- Introduced structured error payload for key workflow failure paths

5. Workflow runtime robustness
- Backend image now includes runtime prerequisites:
  - `bash`, `curl`, `git`, `ca-certificates`, `default-jre-headless`
- Improved on-demand installation diagnostics in:
  - `app/runners/nextflow_runner.py`
  - `app/runners/snakemake_runner.py`
- Added workflow executor preflight + structured runtime failures in:
  - `app/workflows/executor.py`

6. Documentation and validation tooling
- Updated `README.md`, `QUICKSTART.md`, `WORKFLOW_QUICKSTART.md`
- Added smoke test script: `scripts/smoke.sh`
- Added backend API readiness tests: `tests/test_api_health_ready.py`

## Quality Gate Baseline

P0 gate (required):
- Docker services start and health checks pass
- `/api/health`, `/api/ready` reachable
- Frontend home and proxy paths reachable
- Frontend `npm run build` passes

P1 gate (in progress):
- Frontend lint/type debt reduction

Current frontend lint baseline snapshot:
- `npm run lint` -> `99 problems` (`96 errors`, `3 warnings`)
- Main debt type: `@typescript-eslint/no-explicit-any`
- Additional debt: selected React hooks dependency warnings

## Residual Risks

1. Runtime install latency
- First workflow run may still be slow due to on-demand engine installation.

2. docker.sock security model
- Default mounted for functionality; this is a known host-level trust tradeoff.

3. Frontend lint debt
- Does not block runtime, but should be reduced gradually on high-traffic paths first.

## Recommended P1 Next Steps

1. Add structured error handling to remaining non-workflow endpoints.
2. Add retry/backoff policy around runtime install downloads.
3. Triage frontend lint issues by impact:
- `src/api/client.ts`
- `src/stores/agentStore.ts`
- `src/components/VisualizationPanel.tsx`
4. Add CI step for `scripts/smoke.sh` + backend tests.
