#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PM_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PM_ROOT / "config" / "repos.json"
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


def _check_repo(repo_rel: str, repo_abs: Path, failures: list[str]) -> bool:
    fit_doc = repo_abs / "docs" / "architecture-scale-fit.md"
    if not fit_doc.exists():
        failures.append(f"{repo_rel}: missing docs/architecture-scale-fit.md.")
        return False

    text = fit_doc.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            failures.append(f"{repo_rel}: missing required section `{section}` in architecture-scale-fit.md")
    return True


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate architecture scale-fit docs for changed repos or a specific target."
    )
    parser.add_argument(
        "--target",
        help="Optional repo path (relative to Project Manager root or absolute) for local/single-repo validation.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    failures: list[str] = []
    checked = 0

    if args.target:
        target = Path(args.target)
        if not target.is_absolute():
            target = ROOT / target
        repo_abs = target.resolve()
        try:
            repo_rel = str(repo_abs.relative_to(ROOT))
        except ValueError:
            repo_rel = str(repo_abs)

        if not repo_abs.exists():
            print("FAIL: architecture/scale fit validation failed.")
            print(f"- {repo_rel}: target path does not exist.")
            return 1
        if not (repo_abs / ".git").exists():
            print("FAIL: architecture/scale fit validation failed.")
            print(f"- {repo_rel}: target is not a git repository.")
            return 1
        if not _repo_has_commits(repo_abs):
            print("FAIL: architecture/scale fit validation failed.")
            print(f"- {repo_rel}: repository has no commits yet.")
            return 1

        _check_repo(repo_rel, repo_abs, failures)
        checked = 1
    else:
        changed = _changed_paths()

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
            _check_repo(repo_rel, repo_abs, failures)

    if failures:
        print("FAIL: architecture/scale fit validation failed.")
        for msg in failures:
            print(f"- {msg}")
        return 1

    if args.target and checked == 1:
        print("PASS: architecture/scale fit validation passed for target repository.")
    elif checked == 0:
        print("PASS: no changed repositories required architecture/scale fit validation.")
    else:
        print(f"PASS: architecture/scale fit validation passed for {checked} changed repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
