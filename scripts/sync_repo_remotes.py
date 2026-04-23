#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config' / 'repo-remotes.json'
PORTFOLIO_CONFIG = ROOT / 'config' / 'repos.json'


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(['git', *args], cwd=cwd, text=True, capture_output=True)


def current_remote(cwd: Path, remote_name: str) -> str | None:
    cp = run_git(['remote', 'get-url', remote_name], cwd)
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()


def ensure_remote(cwd: Path, remote_name: str, target_url: str, apply: bool) -> str:
    existing = current_remote(cwd, remote_name)
    if existing == target_url:
        return 'ok'
    if not apply:
        return f'needs-update ({existing or "missing"} -> {target_url})'
    if existing is None:
        cp = run_git(['remote', 'add', remote_name, target_url], cwd)
    else:
        cp = run_git(['remote', 'set-url', remote_name, target_url], cwd)
    if cp.returncode != 0:
        return f'error: {(cp.stderr or cp.stdout).strip()}'
    return 'updated'


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit/sync child repo remotes from central map')
    parser.add_argument('--apply', action='store_true', help='Apply remote updates (default dry-run)')
    args = parser.parse_args()

    rem = json.loads(CONFIG.read_text())
    repos = json.loads(PORTFOLIO_CONFIG.read_text())['managed_repositories']

    host = rem.get('default_host', 'github.com')
    protocol = rem.get('protocol', 'https')
    remote_name = rem.get('remote_name', 'origin')
    remote_map = rem.get('remote_map', {})
    bindings = rem.get('bindings', {})
    path_overrides = rem.get('path_overrides', {})
    retired_paths = set(rem.get('retired_paths', []))
    retired_names = set(rem.get('retired_names', []))

    print(f"mode={'APPLY' if args.apply else 'DRY-RUN'}")
    updated = 0
    missing_binding = 0
    missing_remote_key = 0

    for entry in repos:
        resolved_path = path_overrides.get(entry.get('name')) or path_overrides.get(entry.get('path')) or entry['path']
        repo_path = ROOT / resolved_path
        if entry.get('path') in retired_paths or entry.get('name') in retired_names:
            print(f"[skip-retired] {entry['name']} -> {entry['path']}")
            continue
        if not (repo_path / '.git').exists():
            print(f"[skip-not-git] {entry['name']} -> {entry['path']}")
            continue

        candidates = [
            entry.get('path',''),
            entry.get('name',''),
            entry.get('github_repo_slug',''),
        ]
        key = None
        for c in candidates:
            if c and c in bindings:
                key = bindings[c]
                break
            if c and c in remote_map:
                key = c
                break

        if not key:
            print(f"[missing-binding] {entry['name']} ({entry['path']})")
            missing_binding += 1
            continue
        if key not in remote_map:
            print(f"[missing-remote-key] {entry['name']} uses key '{key}'")
            missing_remote_key += 1
            continue

        repo_slug = remote_map[key]
        target_url = f"{protocol}://{host}/{repo_slug}.git"
        status = ensure_remote(repo_path, remote_name, target_url, args.apply)
        print(f"[{status}] {entry['name']} -> {target_url}")
        if status in {'updated'}:
            updated += 1

    print(f"summary: updated={updated}, missing_binding={missing_binding}, missing_remote_key={missing_remote_key}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
