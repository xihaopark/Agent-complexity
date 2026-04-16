#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DAEMON="$ROOT_DIR/backend/scripts/backend-daemon.sh"
FRONTEND_DAEMON="$ROOT_DIR/frontend/scripts/frontend-daemon.sh"

load_env_file() {
  if [[ -f "$ROOT_DIR/.env" ]]; then
    set -a
    # shellcheck disable=SC1091
    source "$ROOT_DIR/.env"
    set +a
  fi
}

ensure_prereqs() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required but not found"
    exit 1
  fi
  if ! command -v npm >/dev/null 2>&1; then
    echo "npm is required but not found"
    exit 1
  fi
  if [[ ! -x "$BACKEND_DAEMON" ]]; then
    chmod +x "$BACKEND_DAEMON"
  fi
  if [[ ! -x "$FRONTEND_DAEMON" ]]; then
    chmod +x "$FRONTEND_DAEMON"
  fi
}

ensure_frontend_deps() {
  if [[ ! -d "$ROOT_DIR/frontend/node_modules" ]]; then
    echo "installing frontend dependencies..."
    (cd "$ROOT_DIR/frontend" && npm install)
  fi
}

start_local() {
  load_env_file
  ensure_prereqs
  ensure_frontend_deps

  local backend_port="${LOCAL_BACKEND_PORT:-8000}"
  local frontend_port="${LOCAL_FRONTEND_PORT:-5173}"
  local proxy_target="${VITE_PROXY_TARGET:-http://127.0.0.1:${backend_port}}"

  echo "starting Renzo local development mode..."
  HOST=0.0.0.0 PORT="$backend_port" "$BACKEND_DAEMON" start
  HOST=0.0.0.0 PORT="$frontend_port" VITE_PROXY_TARGET="$proxy_target" "$FRONTEND_DAEMON" start

  echo ""
  echo "=========================================="
  echo "Renzo local services started"
  echo "Frontend: http://localhost:${frontend_port}"
  echo "Backend API: http://localhost:${backend_port}"
  echo "API Docs: http://localhost:${backend_port}/docs"
  echo "=========================================="
}

stop_local() {
  ensure_prereqs
  "$FRONTEND_DAEMON" stop || true
  "$BACKEND_DAEMON" stop || true
}

status_local() {
  load_env_file
  ensure_prereqs
  local backend_port="${LOCAL_BACKEND_PORT:-8000}"
  local frontend_port="${LOCAL_FRONTEND_PORT:-5173}"
  HOST=0.0.0.0 PORT="$backend_port" "$BACKEND_DAEMON" status || true
  HOST=0.0.0.0 PORT="$frontend_port" "$FRONTEND_DAEMON" status || true
}

logs_local() {
  ensure_prereqs
  echo "--- backend logs ---"
  "$BACKEND_DAEMON" logs || true
  echo "--- frontend logs ---"
  "$FRONTEND_DAEMON" logs || true
}

case "${1:-start}" in
  start) start_local ;;
  stop) stop_local ;;
  restart) stop_local; start_local ;;
  status) status_local ;;
  logs) logs_local ;;
  *)
    echo "usage: $0 {start|stop|restart|status|logs}"
    exit 2
    ;;
esac
