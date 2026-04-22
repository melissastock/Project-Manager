#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HANDOFF_DIR = ROOT / "docs" / "session-handoffs"
SCOPE_VALUES = {"all-repos", "selected-lanes", "pm-portal-only"}


def _changed_files() -> set[Path]:
    candidates = set()
    cmds = [
        ["git", "diff", "--name-only", "HEAD~1..HEAD"],
        ["git", "diff", "--name-only"],
    ]
    for cmd in cmds:
        try:
            out = subprocess.run(
                cmd,
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            ).stdout.strip()
        except Exception:
            out = ""
        for rel in out.splitlines():
            rel = rel.strip()
            if not rel:
                continue
            path = (ROOT / rel).resolve()
            candidates.add(path)
    return candidates


def _handoff_files() -> list[Path]:
    if not HANDOFF_DIR.exists():
        return []
    changed = _changed_files()
    files = []
    for path in sorted(HANDOFF_DIR.glob("*.md")):
        name = path.name.lower()
        if name == "readme.md":
            continue
        if "handoff" not in name and "addendum" not in name:
            continue
        if changed and path.resolve() not in changed:
            continue
        files.append(path)
    return files


def _extract_scope(text: str) -> str | None:
    match = re.search(r"Scope label:\s*([a-z-]+)", text, flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip().lower()


def main() -> int:
    files = _handoff_files()
    if not files:
        print("PASS: no changed handoff/addendum files require cascade scope validation.")
        return 0

    failures: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        scope = _extract_scope(text)
        if scope is None:
            failures.append(f"{path.relative_to(ROOT)}: missing `Scope label:`")
            continue
        if scope not in SCOPE_VALUES:
            failures.append(
                f"{path.relative_to(ROOT)}: invalid scope `{scope}` (expected one of {sorted(SCOPE_VALUES)})"
            )

    if failures:
        print("FAIL: cascade scope validation failed.")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print(f"PASS: cascade scope labels validated in {len(files)} handoff/addendum files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
