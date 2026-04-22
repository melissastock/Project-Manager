#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from governance_modules import (
    MODULE_CORE_READINESS,
    MODULE_DOWNSTREAM,
    MODULE_LAUNCH,
    MODULE_LIFECYCLE,
    MODULE_PERSONA,
    infer_modules,
    read_intake,
)


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "repos.json"
READINESS_CHECK = ROOT / "scripts" / "check_production_readiness.py"
DOWNSTREAM_GOVERNANCE_CHECK = ROOT / "scripts" / "validate_downstream_governance.py"
LAUNCH_READINESS_CHECK = ROOT / "scripts" / "validate_launch_readiness.py"
LIFECYCLE_STATE_CHECK = ROOT / "scripts" / "validate_lifecycle_state.py"
PERSONA_RESEARCH_CHECK = ROOT / "scripts" / "validate_persona_research_layer.py"


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


def _run_check(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True)


def _check_one(entry: dict, fix_downstream: bool) -> tuple[str, int, str, list[str]]:
    repo_path = ROOT / entry["path"]
    intake_text = read_intake(repo_path)
    active_modules = sorted(infer_modules(entry, intake_text))
    fix_suffix = ["--fix"] if fix_downstream else []

    sections: list[str] = [f"## Active Modules\n{', '.join(active_modules)}"]
    codes: list[int] = []

    if MODULE_CORE_READINESS in active_modules:
        readiness_proc = _run_check(["python3", str(READINESS_CHECK), "--target", str(repo_path)])
        sections.append("## Production Readiness\n" + (readiness_proc.stdout + "\n" + readiness_proc.stderr).strip())
        codes.append(readiness_proc.returncode)

    if MODULE_DOWNSTREAM in active_modules:
        downstream_proc = _run_check(
            ["python3", str(DOWNSTREAM_GOVERNANCE_CHECK), "--target", str(repo_path), *fix_suffix]
        )
        sections.append("## Downstream Governance\n" + (downstream_proc.stdout + "\n" + downstream_proc.stderr).strip())
        codes.append(downstream_proc.returncode)

    if MODULE_LAUNCH in active_modules:
        launch_proc = _run_check(["python3", str(LAUNCH_READINESS_CHECK), "--target", str(repo_path), *fix_suffix])
        sections.append("## Launch Readiness\n" + (launch_proc.stdout + "\n" + launch_proc.stderr).strip())
        codes.append(launch_proc.returncode)

    if MODULE_PERSONA in active_modules:
        persona_proc = _run_check(
            ["python3", str(PERSONA_RESEARCH_CHECK), "--target", str(repo_path), *fix_suffix]
        )
        sections.append("## Persona Research Layer\n" + (persona_proc.stdout + "\n" + persona_proc.stderr).strip())
        codes.append(persona_proc.returncode)

    if MODULE_LIFECYCLE in active_modules:
        lifecycle_proc = _run_check(["python3", str(LIFECYCLE_STATE_CHECK), "--target", str(repo_path), *fix_suffix])
        sections.append("## Lifecycle State\n" + (lifecycle_proc.stdout + "\n" + lifecycle_proc.stderr).strip())
        codes.append(lifecycle_proc.returncode)

    combined_output = "\n\n".join(section.strip() for section in sections if section.strip()).strip()
    combined_code = 0 if all(code == 0 for code in codes) else 1
    return entry["name"], combined_code, combined_output, active_modules


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run portfolio readiness checks across all eligible managed repositories."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Pass --fix to module validators that support auto-remediation.",
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
    module_rollup: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(_check_one, entry, args.fix): entry for entry in eligible}
        for future in as_completed(futures):
            name, code, output, active_modules = future.result()
            for module in active_modules:
                module_rollup[module] = module_rollup.get(module, 0) + 1
            if code != 0:
                failures.append((name, output))

    print(f"Readiness targets: {len(eligible)} checked, {len(skipped)} skipped.")
    if skipped:
        for name, reason in skipped:
            print(f"- skipped: {name} ({reason})")
    if module_rollup:
        print("Active module counts:")
        for module in sorted(module_rollup):
            print(f"- {module}: {module_rollup[module]}")

    if failures:
        print("FAIL: portfolio readiness checks failed.")
        for name, output in failures:
            print(f"\n## {name}\n{output}")
        return 1

    print("PASS: portfolio readiness checks passed for all eligible repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
