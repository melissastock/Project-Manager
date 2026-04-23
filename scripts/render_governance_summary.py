#!/usr/bin/env python3

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "session-artifacts" / "governance"
JSON_PATH = OUT_DIR / "last-governance-run.json"
MD_PATH = OUT_DIR / "last-governance-run.md"


def _env_flag(name: str, default: str = "0") -> str:
    return os.getenv(name, default)


def _status(flag: str) -> str:
    return "enabled" if flag == "1" else "skipped"


def main() -> int:
    profile = os.getenv("PROFILE", "fast")
    target_repo = os.getenv("TARGET_REPO", "")
    target_lane = os.getenv("TARGET_LANE", "")
    trigger_reason = os.getenv("GOVERNANCE_TRIGGER_REASON", "manual")

    checks = [
        ("portfolio_status", _env_flag("RUN_PORTFOLIO_STATUS", "0")),
        ("remote_collisions", _env_flag("RUN_REMOTE_COLLISIONS", "0")),
        ("review_gate", _env_flag("RUN_REVIEW_GATE", "0")),
        ("cascade_scope", _env_flag("RUN_SCOPE_CHECK", "0")),
        ("portfolio_readiness", _env_flag("RUN_PORTFOLIO_READINESS_CHECK", "0")),
        ("mobile_governance", _env_flag("RUN_MOBILE_GOVERNANCE_CHECK", "0")),
        ("runtime_disclosure_drift", _env_flag("RUN_RUNTIME_DISCLOSURE_DRIFT_CHECK", "0")),
        ("architecture_scale_fit", _env_flag("RUN_ARCH_SCALE_FIT_CHECK", "0")),
    ]

    now = datetime.now(timezone.utc).isoformat()
    payload = {
        "generated_at": now,
        "profile": profile,
        "target_repo": target_repo,
        "target_lane": target_lane,
        "trigger_reason": trigger_reason,
        "checks": [
            {"check": check, "flag": flag, "status": _status(flag)}
            for check, flag in checks
        ],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Governance Run Summary",
        "",
        f"- Generated at (UTC): {now}",
        f"- Profile: `{profile}`",
        f"- Trigger reason: `{trigger_reason}`",
        f"- Target repo: `{target_repo or '-'} `",
        f"- Target lane: `{target_lane or '-'} `",
        "",
        "| Check | Flag | Status |",
        "| --- | --- | --- |",
    ]
    for check, flag in checks:
        lines.append(f"| `{check}` | `{flag}` | `{_status(flag)}` |")
    lines.append("")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {JSON_PATH}")
    print(f"Wrote {MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
