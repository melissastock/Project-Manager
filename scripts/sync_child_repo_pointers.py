#!/usr/bin/env python3

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Set


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "repos.json"


@dataclass
class PointerChange:
    path: str
    old_sha: str
    new_sha: str
    branch: str
    summary: str


def run(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def tracked_gitlinks() -> dict[str, str]:
    result = run(["git", "ls-files", "--stage"], ROOT)
    gitlinks: dict[str, str] = {}
    for line in result.stdout.splitlines():
        parts = line.split(maxsplit=3)
        if len(parts) != 4:
            continue
        mode, sha, _stage, path = parts
        if mode == "160000":
            gitlinks[path] = sha
    return gitlinks


def repo_has_commits(repo_path: Path) -> bool:
    result = run(["git", "-C", str(repo_path), "rev-parse", "--verify", "HEAD"], ROOT, check=False)
    return result.returncode == 0


def head_sha(repo_path: Path) -> str:
    return run(["git", "-C", str(repo_path), "rev-parse", "HEAD"], ROOT).stdout.strip()


def branch_name(repo_path: Path) -> str:
    name = run(["git", "-C", str(repo_path), "branch", "--show-current"], ROOT).stdout.strip()
    return name or "detached"


def head_summary(repo_path: Path) -> str:
    return run(["git", "-C", str(repo_path), "log", "-1", "--pretty=%s"], ROOT).stdout.strip()


def find_pointer_changes(paths: Optional[Set[str]] = None) -> list[PointerChange]:
    config = load_config()
    current_gitlinks = tracked_gitlinks()
    changes: list[PointerChange] = []

    for entry in config["managed_repositories"]:
        repo_rel = entry["path"]
        if repo_rel not in current_gitlinks:
            continue
        if paths and repo_rel not in paths:
            continue

        repo_path = ROOT / repo_rel
        if not (repo_path / ".git").exists():
            continue
        if not repo_has_commits(repo_path):
            continue

        old_sha = current_gitlinks[repo_rel]
        new_sha = head_sha(repo_path)
        if old_sha == new_sha:
            continue

        changes.append(
            PointerChange(
                path=repo_rel,
                old_sha=old_sha,
                new_sha=new_sha,
                branch=branch_name(repo_path),
                summary=head_summary(repo_path),
            )
        )
    return changes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect or stage updated child repository gitlinks in the Project Manager repo."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Stage the changed child repo pointers in the top-level Project Manager repository.",
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=[],
        help="Optional subset of managed repo paths to inspect or stage.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = set(args.paths) if args.paths else None
    changes = find_pointer_changes(paths)

    if not changes:
        print("No child repo pointer updates found.")
        return 0

    print("Child repo pointer updates:")
    for change in changes:
        print(
            f"- {change.path}: {change.old_sha[:7]} -> {change.new_sha[:7]} "
            f"({change.branch}) {change.summary}"
        )

    if not args.apply:
        print("")
        print("Dry run only. Re-run with --apply to stage these pointer updates.")
        return 0

    for change in changes:
        run(["git", "add", "--", change.path], ROOT)
    print("")
    print(f"Staged {len(changes)} child repo pointer update(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
