#!/usr/bin/env python3

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates" / "production-delivery"

FILES = {
    "backlog.md": "docs/delivery/backlog.md",
    "sprint-plan.md": "docs/delivery/sprint-plan.md",
    "test-report.md": "docs/delivery/test-report.md",
    "pr-readiness.md": "docs/delivery/pr-readiness.md",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold agile production delivery docs into a project repo."
    )
    parser.add_argument("--target", required=True, help="Target project path.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target
    target.mkdir(parents=True, exist_ok=True)

    for src_name, dest_rel in FILES.items():
        src = TEMPLATE_DIR / src_name
        dest = target / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and not args.force:
            continue
        dest.write_text(src.read_text())

    print(f"Scaffolded production delivery docs into {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
