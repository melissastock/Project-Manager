#!/usr/bin/env python3
"""Run product hardening checks ("SKUs") for a single target repo.

SKU A: production readiness (check_production_readiness.py)
SKU B: downstream governance (validate_downstream_governance.py)

These match the per-target pair used in scripts/run_weekly_ops_cycle.py.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PM_ROOT = Path(__file__).resolve().parents[1]

SKU_SCRIPTS: dict[str, tuple[str, Path]] = {
    "a": ("production readiness", PM_ROOT / "scripts" / "check_production_readiness.py"),
    "b": ("downstream governance", PM_ROOT / "scripts" / "validate_downstream_governance.py"),
}


def _resolve_target(target: str) -> Path:
    p = Path(target)
    if p.is_absolute():
        return p
    return ROOT / p


def _parse_skus(raw: str) -> list[str]:
    out: list[str] = []
    for part in raw.split(","):
        token = part.strip().lower()
        if not token:
            continue
        if token not in SKU_SCRIPTS:
            allowed = ", ".join(sorted(SKU_SCRIPTS))
            raise SystemExit(f"Unknown SKU {part.strip()!r}. Use one or more of: {allowed}")
        out.append(token)
    if not out:
        raise SystemExit("No SKUs to run; pass e.g. --skus a,b")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run SKU A (production readiness) and/or SKU B (downstream governance) for one target."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target path relative to Project Manager root, or absolute (e.g. bg-legal).",
    )
    parser.add_argument(
        "--skus",
        default="a,b",
        help="Comma-separated SKUs to run (default: a,b). Values: a, b.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Pass --fix to downstream governance when SKU B runs.",
    )
    args = parser.parse_args()

    target = _resolve_target(args.target)
    if not target.exists():
        print(f"Target does not exist: {target}")
        return 1

    skus = _parse_skus(args.skus)
    target_arg = str(target)
    codes: list[int] = []

    for sku in skus:
        label, script = SKU_SCRIPTS[sku]
        cmd = ["python3", str(script), "--target", target_arg]
        if sku == "b" and args.fix:
            cmd.append("--fix")
        print(f"--- SKU {sku.upper()} ({label}) ---")
        proc = subprocess.run(cmd, cwd=PM_ROOT, text=True)
        codes.append(proc.returncode)

    return 0 if all(c == 0 for c in codes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
