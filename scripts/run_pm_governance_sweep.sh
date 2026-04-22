#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== PM governance sweep (from $ROOT) =="
if [[ "${RUN_PORTFOLIO_STATUS:-1}" == "1" ]]; then
  python3 scripts/portfolio_status.py
else
  echo "Skipping portfolio_status.py (set RUN_PORTFOLIO_STATUS=1 to enable)."
fi

if [[ "${RUN_REMOTE_COLLISIONS:-1}" == "1" ]]; then
  python3 scripts/check_remote_collisions.py
else
  echo "Skipping check_remote_collisions.py (set RUN_REMOTE_COLLISIONS=1 to enable)."
fi

if [[ "${RUN_REVIEW_GATE:-0}" == "1" ]]; then
  python3 scripts/review_gate.py
else
  echo "Skipping review_gate.py (set RUN_REVIEW_GATE=1 to enable)."
fi

if [[ "${RUN_SCOPE_CHECK:-1}" == "1" ]]; then
  python3 scripts/validate_cascade_scope.py
else
  echo "Skipping validate_cascade_scope.py (set RUN_SCOPE_CHECK=1 to enable)."
fi

if [[ "${RUN_PORTFOLIO_READINESS_CHECK:-1}" == "1" ]]; then
  python3 scripts/run_portfolio_readiness_checks.py
else
  echo "Skipping run_portfolio_readiness_checks.py (set RUN_PORTFOLIO_READINESS_CHECK=1 to enable)."
fi

if [[ "${RUN_MOBILE_GOVERNANCE_CHECK:-1}" == "1" ]]; then
  python3 scripts/validate_mobile_governance.py
else
  echo "Skipping validate_mobile_governance.py (set RUN_MOBILE_GOVERNANCE_CHECK=1 to enable)."
fi

if [[ "${RUN_RUNTIME_DISCLOSURE_DRIFT_CHECK:-1}" == "1" ]]; then
  python3 scripts/check_runtime_disclosure_drift.py
else
  echo "Skipping check_runtime_disclosure_drift.py (set RUN_RUNTIME_DISCLOSURE_DRIFT_CHECK=1 to enable)."
fi

if [[ "${RUN_ARCH_SCALE_FIT_CHECK:-1}" == "1" ]]; then
  python3 scripts/validate_architecture_scale_fit.py
else
  echo "Skipping validate_architecture_scale_fit.py (set RUN_ARCH_SCALE_FIT_CHECK=1 to enable)."
fi

echo "== Sweep complete =="
