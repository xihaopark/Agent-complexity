#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$BASE_DIR/.run"
PID_FILE="$RUN_DIR/backend-dev.pid"
LOG_FILE="$RUN_DIR/backend-dev.log"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

mkdir -p "$RUN_DIR"

is_running() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [[ -n "${pid}" ]] && kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

ensure_dependencies() {
  if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "python3 is required but not found"
    exit 1
  fi
  if ! "$PYTHON_BIN" -c "import fastapi" >/dev/null 2>&1; then
    echo "installing backend dependencies with $PYTHON_BIN -m pip ..."
    "$PYTHON_BIN" -m pip install -r "$BASE_DIR/requirements.txt"
  fi
}

start() {
  if is_running; then
    echo "backend daemon already running (pid $(cat "$PID_FILE"))"
    exit 0
  fi

  ensure_dependencies
  echo "starting backend daemon on ${HOST}:${PORT} ..."
  nohup bash -lc "cd \"$BASE_DIR\" && \"$PYTHON_BIN\" -m uvicorn api_gateway:app --host \"$HOST\" --port \"$PORT\"" >>"$LOG_FILE" 2>&1 &
  echo "$!" > "$PID_FILE"
  sleep 1

  if is_running; then
    echo "backend daemon started (pid $(cat "$PID_FILE"))"
    echo "log file: $LOG_FILE"
  else
    echo "failed to start backend daemon"
    exit 1
  fi
}

stop() {
  if ! is_running; then
    echo "backend daemon is not running"
    rm -f "$PID_FILE"
    exit 0
  fi

  local pid
  pid="$(cat "$PID_FILE")"
  echo "stopping backend daemon (pid $pid) ..."
  kill "$pid" 2>/dev/null || true
  for _ in $(seq 1 20); do
    if ! kill -0 "$pid" 2>/dev/null; then
      break
    fi
    sleep 0.2
  done
  if kill -0 "$pid" 2>/dev/null; then
    kill -9 "$pid" 2>/dev/null || true
  fi
  rm -f "$PID_FILE"
  echo "backend daemon stopped"
}

status() {
  if is_running; then
    echo "backend daemon is running (pid $(cat "$PID_FILE"))"
    echo "url: http://localhost:${PORT}/"
  else
    echo "backend daemon is not running"
    exit 1
  fi
}

logs() {
  touch "$LOG_FILE"
  tail -n 120 "$LOG_FILE"
}

case "${1:-}" in
  start) start ;;
  stop) stop ;;
  restart) stop || true; start ;;
  status) status ;;
  logs) logs ;;
  *)
    echo "usage: $0 {start|stop|restart|status|logs}"
    exit 2
    ;;
esac
