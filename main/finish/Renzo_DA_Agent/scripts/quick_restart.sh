#!/usr/bin/env bash
# Quick restart: apply .env/compose changes and reload services. No image rebuild.
# Use after: .env change, or app/ code change (app is mounted; backend restart picks it up).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

COMPOSE_CMD="${COMPOSE_CMD:-docker-compose}"
RESTART_BACKEND="${RESTART_BACKEND:-1}"

echo "Applying config and bringing containers up (no build)..."
"$COMPOSE_CMD" up -d

if [[ "$RESTART_BACKEND" == "1" ]]; then
  echo "Restarting backend to pick up mounted app/ and env..."
  "$COMPOSE_CMD" restart backend
fi

echo "Done. Frontend: http://localhost:${FRONTEND_PORT:-13000}  Backend: http://localhost:${BACKEND_PORT:-18000}"
