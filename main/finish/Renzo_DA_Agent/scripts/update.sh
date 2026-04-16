#!/usr/bin/env bash
# Update and start: incremental build only for changed images, then up.
# Use after: backend/ or frontend/ code change (api_gateway.py, Dockerfile, frontend src).
# Not needed for: .env only, or app/*.py only (use quick_restart.sh for those).
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

echo "Building only changed images and starting..."
tmp_err="$(mktemp)"
set +e
"$COMPOSE_CMD" up -d --build 2> >(tee "$tmp_err" >&2)
rc=$?
set -e

if [[ $rc -ne 0 ]]; then
  if grep -q "ContainerConfig" "$tmp_err"; then
    echo "Detected docker-compose ContainerConfig compatibility issue."
    echo "Running '$COMPOSE_CMD down' then retrying '$COMPOSE_CMD up -d --build'..."
    "$COMPOSE_CMD" down
    "$COMPOSE_CMD" up -d --build
  else
    echo "Update failed. See error output above."
    rm -f "$tmp_err"
    exit $rc
  fi
fi

rm -f "$tmp_err"

echo "Done. Frontend: http://localhost:${FRONTEND_PORT:-13000}  Backend: http://localhost:${BACKEND_PORT:-18000}"
