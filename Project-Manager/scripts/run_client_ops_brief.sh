#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

if [[ "${SKIP_PORTAL_SYNC:-}" != "1" ]]; then
  python3 "$ROOT_DIR/scripts/sync_client_ops_from_pm_portal.py" \
    --tracker "$ROOT_DIR/config/client-ops-tracker.json" \
    ${PM_PORTAL_URL:+--base-url "$PM_PORTAL_URL"} \
    ${FILE_ONLY_SYNC:+--file-only}
fi

python3 "$ROOT_DIR/scripts/generate_client_ops_brief.py" \
  --input "$ROOT_DIR/config/client-ops-tracker.json" \
  --output "$ROOT_DIR/docs/client-engagements/client-ops-daily-brief.md"

echo "Client ops brief updated at docs/client-engagements/client-ops-daily-brief.md"
