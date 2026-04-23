#!/usr/bin/env python3

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "repos.json"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Roll out latest PM backbone scaffolds to managed projects."
    )
    parser.add_argument(
        "--include-archive",
        action="store_true",
        help="Also apply scaffolds to repositories marked intake_stage=archive.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Pass --force to scaffold scripts to overwrite existing files.",
    )
    args = parser.parse_args()

    config = json.loads(CONFIG_PATH.read_text())
    repos = config.get("managed_repositories", [])

    applied = 0
    skipped = 0
    failures: list[tuple[str, str]] = []

    for repo in repos:
        stage = str(repo.get("intake_stage", "")).lower()
        if stage == "archive" and not args.include_archive:
            skipped += 1
            continue

        target = ROOT / repo["path"]
        if not target.exists():
            failures.append((repo["name"], f"missing path: {target}"))
            continue

        base_cmds = [
            ["python3", "scripts/scaffold_production_delivery.py", "--target", str(target)],
            ["python3", "scripts/scaffold_gtm_pack.py", "--target", str(target)],
            ["python3", "scripts/scaffold_investor_book.py", "--target", str(target), "--project-name", repo["name"]],
        ]
        if args.force:
            for cmd in base_cmds:
                cmd.append("--force")

        repo_failed = False
        for cmd in base_cmds:
            result = run(cmd)
            if result.returncode != 0:
                failures.append((repo["name"], f"command failed: {' '.join(cmd)}\n{result.stderr.strip()}"))
                repo_failed = True
                break

        if not repo_failed:
            applied += 1

    print(f"Backbone rollout complete.")
    print(f"- Repositories updated: {applied}")
    print(f"- Repositories skipped: {skipped}")
    print(f"- Repositories failed: {len(failures)}")
    if failures:
        print("\nFailures:")
        for name, message in failures:
            print(f"- {name}: {message}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
