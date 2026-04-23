#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/pm-portal/backend"
FRONTEND_DIR="${ROOT_DIR}/pm-portal/frontend"
BACKEND_STARTED=0
FRONTEND_STARTED=0

port_in_use() {
  local port="$1"
  lsof -iTCP:"${port}" -sTCP:LISTEN >/dev/null 2>&1
}

echo "Starting Case Files MVP services..."

if port_in_use 8080; then
  echo "Backend already running on port 8080; reusing existing service."
else
  (
    cd "${BACKEND_DIR}"
    PYTHONPATH="${BACKEND_DIR}/.vendor:." python3 -m uvicorn app.main:app --port 8080
  ) &
  BACKEND_PID=$!
  BACKEND_STARTED=1
fi

if port_in_use 5173; then
  echo "Frontend already running on port 5173; reusing existing service."
else
  (
    cd "${FRONTEND_DIR}"
    npm run dev -- --port 5173
  ) &
  FRONTEND_PID=$!
  FRONTEND_STARTED=1
fi

cleanup() {
  echo
  echo "Stopping Case Files MVP services..."
  if [[ "${BACKEND_STARTED}" -eq 1 ]]; then
    kill "${BACKEND_PID}" >/dev/null 2>&1 || true
  fi
  if [[ "${FRONTEND_STARTED}" -eq 1 ]]; then
    kill "${FRONTEND_PID}" >/dev/null 2>&1 || true
  fi
}

trap cleanup INT TERM EXIT

echo "Backend:  http://127.0.0.1:8080"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop both services."

wait
