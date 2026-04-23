#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DELIVERY_DIR = Path("docs/delivery")


def _resolve_target(target: str) -> Path:
    target_path = Path(target)
    if target_path.is_absolute():
        return target_path
    return ROOT / target_path


def _write_if_allowed(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold delivery readiness docs from templates."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target repository path (relative to Project Manager root or absolute).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files.",
    )
    args = parser.parse_args()

    target = _resolve_target(args.target)
    if not target.exists():
        print(f"Target does not exist: {target}")
        return 1

    now = datetime.now().astimezone().strftime("%Y-%m-%d")
    out_dir = target / DELIVERY_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    templates = {
        "backlog.md": f"""# Delivery Backlog

- Last groomed: {now}
- Prioritized items:
  - [ ] Confirm sprint-critical reliability tasks.
  - [ ] Confirm dependencies and ownership.
  - [ ] Confirm carryover candidates for next sprint.
""",
        "sprint-plan.md": """# Sprint Plan

## Sprint Goal
State the single operational outcome this sprint must prove.

## Committed Scope
- Item 1
- Item 2
- Item 3

## Acceptance Checks
- [ ] Readiness checks pass.
- [ ] Governance checks pass.
- [ ] Evidence artifacts generated.
""",
        "test-report.md": """# Test Report

- Pass: List checks that passed.
- Fail: List checks that failed (or write `None`).
- Not tested: List deferred checks and owner.
""",
        "pr-readiness.md": """# PR Readiness

- [x] Scope matches sprint objective.
- [x] Delivery docs are present and updated.
- [x] Test report includes pass/fail/not tested notes.
- [x] Governance/risk checks are complete.
""",
    }

    wrote = []
    skipped = []
    for name, content in templates.items():
        file_path = out_dir / name
        if _write_if_allowed(file_path, content, args.force):
            wrote.append(str(file_path.relative_to(target)))
        else:
            skipped.append(str(file_path.relative_to(target)))

    print(f"Target: {target}")
    print(f"Wrote: {len(wrote)}")
    for path in wrote:
        print(f"- {path}")
    print(f"Skipped existing: {len(skipped)}")
    for path in skipped:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
