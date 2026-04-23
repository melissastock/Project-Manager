#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from backend.app.service import build_standup_view

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "backend" / "data"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    payload = build_standup_view().model_dump(mode="json")
    target = OUT / f"standup-snapshot-{ts}.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
