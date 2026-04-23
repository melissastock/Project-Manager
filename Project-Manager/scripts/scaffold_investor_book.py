#!/usr/bin/env python3

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = ROOT / "templates" / "investor-book"


def render(text: str, values: dict[str, str]) -> str:
    output = text
    for key, value in values.items():
        output = output.replace("{{" + key + "}}", value)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold investor-book templates into a target project repo."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Workspace-relative or absolute path to the target repo.",
    )
    parser.add_argument(
        "--project-name",
        default="CONFIDENTIAL COMPANY NAME",
        help="Project/company name placeholder for the generated template.",
    )
    parser.add_argument(
        "--raise-target",
        default="$X Capital Raise | Expansion",
        help="Raise target subtitle placeholder.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files if present.",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target

    docs_dir = target / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    template_file = TEMPLATE_DIR / "investor-book-template.md"
    coverage_file = TEMPLATE_DIR / "investor-book-section-coverage-template.md"

    values = {
        "PROJECT_NAME": args.project_name,
        "RAISE_TARGET": args.raise_target,
    }

    out_template = docs_dir / "investor-book-template.md"
    out_coverage = docs_dir / "investor-book-section-coverage.md"

    if args.force or not out_template.exists():
        out_template.write_text(render(template_file.read_text(), values))
    if args.force or not out_coverage.exists():
        out_coverage.write_text(coverage_file.read_text())

    print(f"Scaffolded investor-book templates into {docs_dir}")
    print(f"- {out_template}")
    print(f"- {out_coverage}")
    print("Next: create docs/investor-book-draft-assumptions.md with [ASSUMPTION] tags.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
