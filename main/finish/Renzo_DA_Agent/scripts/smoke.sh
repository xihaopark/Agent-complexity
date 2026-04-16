#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_CMD="${COMPOSE_CMD:-docker-compose}"
BACKEND_PORT="${BACKEND_PORT:-18000}"
FRONTEND_PORT="${FRONTEND_PORT:-13000}"
SMOKE_BUILD="${SMOKE_BUILD:-1}"
SMOKE_TIMEOUT="${SMOKE_TIMEOUT:-90}"

cd "$ROOT_DIR"

wait_http_ok() {
  local url="$1"
  local timeout="$2"
  local started
  started="$(date +%s)"
  while true; do
    local code
    code="$(curl -sS -o /dev/null -w '%{http_code}' "$url" || true)"
    if [[ "$code" == "200" ]]; then
      return 0
    fi
    if (( "$(date +%s)" - started > timeout )); then
      echo "timed out waiting for $url (last code: $code)"
      return 1
    fi
    sleep 2
  done
}

echo "[smoke] starting compose services..."
if [[ "$SMOKE_BUILD" == "1" ]]; then
  if ! "$COMPOSE_CMD" up --build -d; then
    echo "[smoke] compose up failed, retrying after cleanup..."
    "$COMPOSE_CMD" down --remove-orphans || true
    "$COMPOSE_CMD" up --build -d
  fi
else
  if ! "$COMPOSE_CMD" up -d; then
    echo "[smoke] compose up failed, retrying after cleanup..."
    "$COMPOSE_CMD" down --remove-orphans || true
    "$COMPOSE_CMD" up -d
  fi
fi

echo "[smoke] waiting for backend readiness..."
wait_http_ok "http://127.0.0.1:${BACKEND_PORT}/api/health" "$SMOKE_TIMEOUT"
wait_http_ok "http://127.0.0.1:${BACKEND_PORT}/api/ready" "$SMOKE_TIMEOUT"

echo "[smoke] waiting for frontend..."
wait_http_ok "http://127.0.0.1:${FRONTEND_PORT}/" "$SMOKE_TIMEOUT"

echo "[smoke] checking frontend->backend proxy path..."
wait_http_ok "http://127.0.0.1:${FRONTEND_PORT}/api/health" "$SMOKE_TIMEOUT"
wait_http_ok "http://127.0.0.1:${FRONTEND_PORT}/api/sessions" "$SMOKE_TIMEOUT"
wait_http_ok "http://127.0.0.1:${FRONTEND_PORT}/api/workflows" "$SMOKE_TIMEOUT"

echo "[smoke] all checks passed"
echo "[smoke] frontend: http://localhost:${FRONTEND_PORT}"
echo "[smoke] backend:  http://localhost:${BACKEND_PORT}"
