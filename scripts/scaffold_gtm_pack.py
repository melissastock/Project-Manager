#!/usr/bin/env python3

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates" / "gtm"

FILES = {
    "gtm-hypotheses-and-pilot-plan.md": "docs/gtm-hypotheses-and-pilot-plan.md",
    "pilot-outreach-brief.md": "docs/pilot-outreach-brief.md",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold reusable GTM docs into a target project repo."
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

    print(f"Scaffolded GTM pack into {target}")
    for rel in FILES.values():
        print(f"- {target / rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
