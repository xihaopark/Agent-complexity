# Renzo Quick Start Guide

## Prerequisites

- Docker + Docker Compose
- For local optional mode: Node.js 18+, Python 3.10+

## Mode Matrix

- Docker-first (recommended): frontend `13000`, backend `18000`
- Local optional mode: frontend `5173`, backend `8000`

## Option 1: Docker Compose (Recommended)

### Start the full stack

```bash
cd /mnt/workspace-storage/lab_workspace/projects/Biomni-main/renzo
cp .env.example .env   # optional, only if .env doesn't exist
docker-compose up --build -d
```

This starts:
- Backend API: `http://localhost:18000`
- Frontend UI: `http://localhost:13000`
- API Docs: `http://localhost:18000/docs`
- Health: `http://localhost:18000/api/health`
- Ready: `http://localhost:18000/api/ready`

### Smoke validation

```bash
./scripts/smoke.sh
```

### External / WAN access

In `.env` set `BIND_IP=0.0.0.0` (default) so the host listens on all interfaces. Then use the server’s IP or hostname in the browser:

- Frontend: `http://<server-ip>:13000`
- API Docs: `http://<server-ip>:18000/docs`

To bind only to a specific NIC, set `BIND_IP=<that-ip>` (e.g. `BIND_IP=192.168.1.10`). Then run `./scripts/quick_restart.sh` (or `docker-compose up -d`).

### Stop the services

```bash
docker-compose down
```

### Quick restart vs Update (no full rebuild)

You don’t need to rebuild images every time. Use:

| Situation | Command | What it does |
|-----------|--------|----------------|
| **Quick restart** | `./scripts/quick_restart.sh` | Applies `.env` / compose, restarts containers. Reloads **app/** (mounted) by restarting backend. **No image build.** |
| **Update (delta)** | `./scripts/update.sh` | Runs `docker-compose up -d --build`. Rebuilds **only** images whose context changed (backend/ or frontend/). Use after changing `api_gateway.py`, Dockerfile, or frontend code. |

- **Only .env or app/\*.py changed** → `./scripts/quick_restart.sh`
- **backend/api_gateway.py or frontend/ or Dockerfile changed** → `./scripts/update.sh`
- **First run or want a clean build** → `docker-compose up --build -d`

To only apply config without restarting backend: `docker-compose up -d` (no script).

## Option 2: Local Development (Optional)

One-click daemon mode:

```bash
cd /mnt/workspace-storage/lab_workspace/projects/Biomni-main/renzo
./start_local.sh start
```

Local URLs:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

Control commands:

```bash
./start_local.sh status
./start_local.sh logs
./start_local.sh stop
```

## Usage

1. Open frontend URL (`13000` for Docker, `5173` for local dev)
2. Upload CSV/Excel/JSON
3. Send analysis request
4. Inspect progress, logs, outputs, and artifacts

## Troubleshooting

### Port conflict
- Override Docker ports in `.env`:
  - `BACKEND_PORT=18080`
  - `FRONTEND_PORT=13080`

### External access (connection refused / -102)
- Ensure `BIND_IP=0.0.0.0` in `.env` so the host listens on all interfaces.
- Open the app using the **server’s IP or hostname**, not `localhost`, e.g. `http://<server-ip>:13000`.
- If using Cursor/remote dev, use the port-forwarding URL Cursor provides for port 13000.

### 5173 unavailable
- Ensure local daemons started:
  - `./start_local.sh status`
- Check local logs:
  - `./start_local.sh logs`

### Workflow runner fails (Nextflow/Snakemake)
- Check readiness details:
  - `curl http://localhost:18000/api/ready`
- Confirm docker mounts exist in compose:
  - `/var/run/docker.sock:/var/run/docker.sock`

### Docker build fails
- Ensure Docker daemon is running
- Check disk space
- Clean old resources if needed:
  - `docker system prune -a`

## Architecture

```
Browser
  -> Nginx (frontend)
  -> FastAPI (backend)
  -> Renzo Agent + Workflow Runtime
```
