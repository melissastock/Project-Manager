#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "repos.json"
READINESS_CHECK = ROOT / "scripts" / "check_production_readiness.py"
DOWNSTREAM_GOVERNANCE_CHECK = ROOT / "scripts" / "validate_downstream_governance.py"
LAUNCH_READINESS_CHECK = ROOT / "scripts" / "validate_launch_readiness.py"


def _run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True, text=True)


def _eligible(entry: dict) -> tuple[bool, str]:
    stage = entry.get("intake_stage", "")
    if stage in {"archive"}:
        return False, "archive stage"

    repo_path = ROOT / entry["path"]
    if not repo_path.exists():
        return False, "missing path"
    if not (repo_path / ".git").exists():
        return False, "no .git"
    head = _run_git(repo_path, "rev-parse", "--verify", "HEAD")
    if head.returncode != 0:
        return False, "unborn"
    return True, "ok"


def _check_one(entry: dict, fix_downstream: bool) -> tuple[str, int, str]:
    repo_path = ROOT / entry["path"]
    readiness_proc = subprocess.run(
        ["python3", str(READINESS_CHECK), "--target", str(repo_path)],
        capture_output=True,
        text=True,
    )
    downstream_cmd = ["python3", str(DOWNSTREAM_GOVERNANCE_CHECK), "--target", str(repo_path)]
    if fix_downstream:
        downstream_cmd.append("--fix")
    downstream_proc = subprocess.run(
        downstream_cmd,
        capture_output=True,
        text=True,
    )
    launch_cmd = ["python3", str(LAUNCH_READINESS_CHECK), "--target", str(repo_path)]
    if fix_downstream:
        launch_cmd.append("--fix")
    launch_proc = subprocess.run(
        launch_cmd,
        capture_output=True,
        text=True,
    )

    combined_output = (
        "## Production Readiness\n"
        + (readiness_proc.stdout + "\n" + readiness_proc.stderr).strip()
        + "\n\n## Downstream Governance\n"
        + (downstream_proc.stdout + "\n" + downstream_proc.stderr).strip()
        + "\n\n## Launch Readiness\n"
        + (launch_proc.stdout + "\n" + launch_proc.stderr).strip()
    ).strip()

    combined_code = 0 if (
        readiness_proc.returncode == 0
        and downstream_proc.returncode == 0
        and launch_proc.returncode == 0
    ) else 1
    return entry["name"], combined_code, combined_output


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run portfolio readiness checks across all eligible managed repositories."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Pass --fix to downstream and launch readiness validators to auto-remediate missing fields/artifacts.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    eligible: list[dict] = []
    skipped: list[tuple[str, str]] = []

    for entry in cfg["managed_repositories"]:
        ok, reason = _eligible(entry)
        if ok:
            eligible.append(entry)
        else:
            skipped.append((entry["name"], reason))

    failures: list[tuple[str, str]] = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(_check_one, entry, args.fix): entry for entry in eligible}
        for future in as_completed(futures):
            name, code, output = future.result()
            if code != 0:
                failures.append((name, output))

    print(f"Readiness targets: {len(eligible)} checked, {len(skipped)} skipped.")
    if skipped:
        for name, reason in skipped:
            print(f"- skipped: {name} ({reason})")

    if failures:
        print("FAIL: portfolio readiness checks failed.")
        for name, output in failures:
            print(f"\n## {name}\n{output}")
        return 1

    print("PASS: portfolio readiness checks passed for all eligible repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
