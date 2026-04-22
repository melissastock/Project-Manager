#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "repos.json"
REQUIRED_SECTIONS = [
    "## Mandate",
    "## Tech Stack Decision",
    "## Database Structure",
    "## Service Model",
    "## Hooks and Integrations",
    "## Hosting Plan",
    "## Scale Triggers",
]


def _run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def _changed_paths() -> set[str]:
    changed: set[str] = set()
    for args in (("diff", "--name-only", "HEAD~1..HEAD"), ("diff", "--name-only")):
        out = _run_git(*args)
        for line in out.splitlines():
            line = line.strip()
            if line:
                changed.add(line)
    return changed


def _repo_has_commits(repo_path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo_path), "rev-parse", "--verify", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    changed = _changed_paths()

    failures: list[str] = []
    checked = 0

    for entry in cfg["managed_repositories"]:
        repo_rel = entry["path"]
        repo_abs = ROOT / repo_rel
        stage = entry.get("intake_stage", "")

        if stage == "archive":
            continue
        if not repo_abs.exists() or not (repo_abs / ".git").exists():
            continue
        if not _repo_has_commits(repo_abs):
            continue

        impacted = any(path == repo_rel or path.startswith(f"{repo_rel}/") for path in changed)
        if not impacted:
            continue

        checked += 1
        fit_doc = repo_abs / "docs" / "architecture-scale-fit.md"
        if not fit_doc.exists():
            failures.append(
                f"{repo_rel}: missing docs/architecture-scale-fit.md for changed repository."
            )
            continue

        text = fit_doc.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                failures.append(f"{repo_rel}: missing required section `{section}` in architecture-scale-fit.md")

    if failures:
        print("FAIL: architecture/scale fit validation failed.")
        for msg in failures:
            print(f"- {msg}")
        return 1

    if checked == 0:
        print("PASS: no changed repositories required architecture/scale fit validation.")
    else:
        print(f"PASS: architecture/scale fit validation passed for {checked} changed repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
