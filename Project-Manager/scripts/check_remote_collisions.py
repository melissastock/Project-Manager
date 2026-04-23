#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PM_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PM_ROOT / "config" / "repos.json"


def get_origin_url(repo_path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_path), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def main() -> int:
    config = json.loads(CONFIG_PATH.read_text())
    collisions: dict[str, list[dict]] = {}

    for entry in config["managed_repositories"]:
        repo_path = ROOT / entry["path"]
        if not (repo_path / ".git").exists():
            continue
        origin = get_origin_url(repo_path)
        if not origin:
            continue
        collisions.setdefault(origin, []).append(
            {
                "name": entry["name"],
                "intake_stage": entry.get("intake_stage", ""),
                "category": entry.get("category", ""),
            }
        )

    bad: dict[str, list[dict]] = {}
    for url, repos in collisions.items():
        if len(repos) <= 1:
            continue
        has_archive_or_backup = any(
            r["intake_stage"] == "archive"
            or "archive" in r["category"]
            or "backup" in r["name"].lower()
            for r in repos
        )
        if has_archive_or_backup:
            bad[url] = repos

    if not bad:
        print("PASS: no risky origin collisions detected across managed repositories.")
        return 0

    print("FAIL: duplicate origin remotes detected:")
    for url, repos in sorted(bad.items()):
        print(f"- {url}")
        for repo in sorted(repos, key=lambda x: x["name"]):
            print(
                f"  - {repo['name']} (stage={repo['intake_stage']}, category={repo['category']})"
            )
    print("")
    print("Remediation: backup/archive repositories must use dedicated remotes.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
