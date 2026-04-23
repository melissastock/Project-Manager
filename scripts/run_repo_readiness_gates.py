#!/usr/bin/env python3
"""Run portfolio readiness checks for one target repo (internal QA gates).

These are **not** consulting offer SKUs (see docs/master-consulting-operator-workflow.md).

- **readiness**: agile delivery artifacts (check_production_readiness.py)
- **governance**: downstream governance intake (validate_downstream_governance.py)
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATES: dict[str, tuple[str, Path]] = {
    "readiness": ("production readiness", ROOT / "scripts" / "check_production_readiness.py"),
    "governance": ("downstream governance", ROOT / "scripts" / "validate_downstream_governance.py"),
}


def _resolve_target(target: str) -> Path:
    p = Path(target)
    if p.is_absolute():
        return p
    return ROOT / p


def _parse_gates(raw: str) -> list[str]:
    out: list[str] = []
    for part in raw.split(","):
        token = part.strip().lower()
        if not token:
            continue
        if token not in GATES:
            allowed = ", ".join(sorted(GATES))
            raise SystemExit(f"Unknown gate {part.strip()!r}. Use one or more of: {allowed}")
        out.append(token)
    if not out:
        raise SystemExit("No gates to run; pass e.g. --gates readiness,governance")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run internal readiness and/or governance validators for one repo path."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Path relative to Project Manager root or absolute (e.g. bg-legal).",
    )
    parser.add_argument(
        "--gates",
        default="readiness,governance",
        help="Comma-separated gates (default: readiness,governance). Values: readiness, governance.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Pass --fix to downstream governance when the governance gate runs.",
    )
    args = parser.parse_args()

    target = _resolve_target(args.target)
    if not target.exists():
        print(f"Target does not exist: {target}")
        return 1

    target_arg = str(target)
    codes: list[int] = []

    for gate in _parse_gates(args.gates):
        label, script = GATES[gate]
        cmd = ["python3", str(script), "--target", target_arg]
        if gate == "governance" and args.fix:
            cmd.append("--fix")
        print(f"--- {gate} ({label}) ---")
        proc = subprocess.run(cmd, cwd=ROOT, text=True)
        codes.append(proc.returncode)

    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
