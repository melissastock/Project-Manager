#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

COMMERCIALIZATION_LABEL = "Launch-proximal commercialization plan required"
MARKETING_LABEL = "Launch-proximal marketing plan required"
OPS_LABEL = "Launch-proximal operationalization SOP set required"
PATH2_LABEL = "Path 2 white-label brand identity applicable"
PATH2_MODE_LABEL = "If yes, selected brand identity mode"

REQUIRED_LAUNCH_FILES = [
    "docs/commercialization-plan.md",
    "docs/marketing-plan.md",
    "docs/operationalization-sops.md",
]
TEMPLATE_MAP = {
    "docs/commercialization-plan.md": ROOT / "templates" / "monetization" / "commercialization-plan-template.md",
    "docs/marketing-plan.md": ROOT / "templates" / "gtm" / "marketing-plan-template.md",
    "docs/operationalization-sops.md": ROOT / "templates" / "operations" / "operationalization-sop-template.md",
}


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def intake_flag_enabled(intake_text: str, label: str) -> bool:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}\s*:\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(intake_text)
    if not match:
        return False
    value = match.group(1).strip().lower()
    return value in {"yes", "y", "true", "required", "1"}


def intake_value(intake_text: str, label: str) -> str:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}\s*:\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(intake_text)
    if not match:
        return ""
    return match.group(1).strip()


def is_blank(value: str) -> bool:
    return value.strip().lower() in {"", "tbd", "na", "n/a", "none", "not set", "unknown"}


def _replace_or_insert_field(text: str, label: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf"(^\s*-\s*{re.escape(label)}\s*:\s*)(.*)$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text)
    if match:
        current = match.group(2).strip()
        if current == value:
            return text, False
        if current and not is_blank(current):
            return text, False
        updated = text[: match.start(2)] + value + text[match.end(2) :]
        return updated, True

    intake_decisions = re.search(r"^##\s+Intake Decisions\s*$", text, re.IGNORECASE | re.MULTILINE)
    if intake_decisions:
        insert_at = intake_decisions.end()
        updated = text[:insert_at] + f"\n\n- {label}: {value}" + text[insert_at:]
        return updated, True

    updated = text.rstrip() + f"\n\n## Intake Decisions\n\n- {label}: {value}\n"
    return updated, True


def _scaffold_launch_artifacts(target: Path) -> list[str]:
    created: list[str] = []
    for rel_path in REQUIRED_LAUNCH_FILES:
        dest = target / rel_path
        if dest.exists():
            continue
        template = TEMPLATE_MAP[rel_path]
        dest.parent.mkdir(parents=True, exist_ok=True)
        if template.exists():
            dest.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            dest.write_text(f"# {Path(rel_path).stem.replace('-', ' ').title()}\n", encoding="utf-8")
        created.append(rel_path)
    return created


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate launch-proximal commercialization, marketing, and SOP readiness gates."
    )
    parser.add_argument("--target", required=True, help="Target project path to validate.")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-create missing launch artifacts and fill missing Path 2 brand mode when required.",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target

    intake = load(target / "docs/project-intake.md")
    if not intake:
        print("Launch readiness: FAIL")
        print("- Missing required intake file: docs/project-intake.md")
        return 1

    launch_required = any(
        intake_flag_enabled(intake, label)
        for label in (COMMERCIALIZATION_LABEL, MARKETING_LABEL, OPS_LABEL)
    )

    if not launch_required:
        print("Launch readiness: PASS")
        print("Launch-proximal gates are not required for this project yet.")
        return 0

    failures: list[str] = []
    for rel in REQUIRED_LAUNCH_FILES:
        if not (target / rel).exists():
            failures.append(f"Missing required launch artifact: {rel}")

    path2_required = intake_flag_enabled(intake, PATH2_LABEL)
    if path2_required:
        mode = intake_value(intake, PATH2_MODE_LABEL)
        if is_blank(mode):
            failures.append(
                "Path 2 white-label identity is required, but selected brand identity mode is missing."
            )

    if failures and args.fix:
        created = _scaffold_launch_artifacts(target)
        patched_intake = intake
        updated_fields: list[str] = []
        if path2_required and is_blank(intake_value(intake, PATH2_MODE_LABEL)):
            patched_intake, changed = _replace_or_insert_field(
                patched_intake, PATH2_MODE_LABEL, "path2-whitelabel"
            )
            if changed:
                updated_fields.append(PATH2_MODE_LABEL)
        if patched_intake != intake:
            (target / "docs/project-intake.md").write_text(patched_intake, encoding="utf-8")

        # re-check after remediation
        intake = load(target / "docs/project-intake.md")
        remaining_failures: list[str] = []
        for rel in REQUIRED_LAUNCH_FILES:
            if not (target / rel).exists():
                remaining_failures.append(f"Missing required launch artifact: {rel}")
        if path2_required and is_blank(intake_value(intake, PATH2_MODE_LABEL)):
            remaining_failures.append(
                "Path 2 white-label identity is required, but selected brand identity mode is missing."
            )
        if remaining_failures:
            print("Launch readiness: FAIL")
            for item in remaining_failures:
                print(f"- {item}")
            return 1

        print("Launch readiness: FIXED")
        if created:
            print(f"- Created launch artifacts: {', '.join(created)}")
        if updated_fields:
            print(f"- Updated intake fields: {', '.join(updated_fields)}")
        print("Launch-proximal commercialization, marketing, and SOP gates are satisfied.")
        if path2_required:
            print("Conditional gate: Path 2 white-label identity configured.")
        return 0

    if failures:
        print("Launch readiness: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Launch readiness: PASS")
    print("Launch-proximal commercialization, marketing, and SOP gates are satisfied.")
    if path2_required:
        print("Conditional gate: Path 2 white-label identity configured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
