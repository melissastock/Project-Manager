#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== PM governance sweep (from $ROOT) =="
python3 scripts/portfolio_status.py
python3 scripts/check_remote_collisions.py

if [[ "${RUN_REVIEW_GATE:-0}" == "1" ]]; then
  python3 scripts/review_gate.py
else
  echo "Skipping review_gate.py (set RUN_REVIEW_GATE=1 to enable)."
fi

echo "== Sweep complete =="
