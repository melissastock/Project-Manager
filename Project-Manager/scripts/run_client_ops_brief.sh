#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

python3 "$ROOT_DIR/scripts/generate_client_ops_brief.py" \
  --input "$ROOT_DIR/config/client-ops-tracker.json" \
  --output "$ROOT_DIR/docs/client-engagements/client-ops-daily-brief.md"

echo "Client ops brief updated at docs/client-engagements/client-ops-daily-brief.md"
