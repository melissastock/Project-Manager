#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_INTAKE_FIELDS = [
    "Project type",
    "KPI profile",
    "KPI owner",
    "KPI reporting cadence",
    "Financial reporting profile",
    "Downstream governance profile",
    "Downstream governance owner",
    "Project-type escalation triggers",
]

VALID_TYPED_PROJECTS = {"producer", "archiavellian", "archive"}
BLANK_SENTINELS = {"", "tbd", "na", "n/a", "none", "not set", "unknown"}


def _extract_field(text: str, label: str) -> str | None:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip()


def _is_blank(value: str | None) -> bool:
    if value is None:
        return True
    lowered = value.strip().lower()
    return lowered in BLANK_SENTINELS


def _normalize_project_type(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip().lower()


def _select_project_type(target: Path, existing_value: str | None) -> str:
    if existing_value and not _is_blank(existing_value):
        return existing_value.strip()
    name = target.name.lower()
    if name == "producer":
        return "Archiavellian"
    if "archive" in name:
        return "Archive"
    return "Client-Delivery"


def _default_value(field: str, project_type: str) -> str:
    lowered_type = project_type.strip().lower()
    if field == "Project type":
        return project_type
    if field in {"KPI profile", "Downstream governance profile"}:
        if lowered_type in VALID_TYPED_PROJECTS:
            return project_type
        return "Client-Delivery"
    if field in {"KPI owner", "Downstream governance owner"}:
        return "Melissa Stock"
    if field == "KPI reporting cadence":
        if lowered_type == "archive":
            return "monthly"
        if lowered_type in {"producer", "client-delivery"}:
            return "weekly"
        return "biweekly"
    if field == "Financial reporting profile":
        if lowered_type == "archive":
            return "archive-minimal"
        return "operational"
    if field == "Project-type escalation triggers":
        return "Documented in docs/governance/project-type-downstream-governance-rules.md"
    return "TBD"


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
        if current and current.lower() not in BLANK_SENTINELS:
            return text, False
        updated = text[: match.start(2)] + value + text[match.end(2) :]
        return updated, True

    anchor = re.search(r"^\s*-\s*Project type\s*:.*$", text, re.IGNORECASE | re.MULTILINE)
    if anchor:
        insert_at = anchor.end()
        updated = text[:insert_at] + f"\n- {label}: {value}" + text[insert_at:]
        return updated, True

    delivery_shape = re.search(r"^##\s+Delivery Shape\s*$", text, re.IGNORECASE | re.MULTILINE)
    if delivery_shape:
        insert_at = delivery_shape.end()
        updated = text[:insert_at] + f"\n\n- {label}: {value}" + text[insert_at:]
        return updated, True

    updated = text.rstrip() + f"\n\n## Delivery Shape\n\n- {label}: {value}\n"
    return updated, True


def _apply_fixes(intake_path: Path, text: str, values: dict[str, str | None]) -> tuple[str, list[str]]:
    changes: list[str] = []
    project_type = _select_project_type(intake_path.parent.parent, values.get("Project type"))

    updated = text
    for field in REQUIRED_INTAKE_FIELDS:
        desired = _default_value(field, project_type)
        updated, changed = _replace_or_insert_field(updated, field, desired)
        if changed:
            changes.append(field)

    normalized_type = _normalize_project_type(project_type)
    if normalized_type in VALID_TYPED_PROJECTS:
        for field in ("KPI profile", "Downstream governance profile"):
            forced = project_type
            pattern = re.compile(
                rf"(^\s*-\s*{re.escape(field)}\s*:\s*)(.*)$",
                re.IGNORECASE | re.MULTILINE,
            )
            match = pattern.search(updated)
            if match and match.group(2).strip() != forced:
                updated = updated[: match.start(2)] + forced + updated[match.end(2) :]
                if field not in changes:
                    changes.append(field)

    return updated, changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate required downstream governance intake fields for a project."
    )
    parser.add_argument("--target", required=True, help="Target project path to validate.")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fill missing/blank downstream governance intake fields using defaults.",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target

    intake_path = target / "docs" / "project-intake.md"
    failures: list[str] = []

    if not intake_path.exists():
        if args.fix:
            intake_path.parent.mkdir(parents=True, exist_ok=True)
            default_type = _select_project_type(target, None)
            lines = [
                "# New Project Intake",
                "",
                "## Delivery Shape",
                "",
            ]
            for field in REQUIRED_INTAKE_FIELDS:
                lines.append(f"- {field}: {_default_value(field, default_type)}")
            intake_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print("Downstream governance: FIXED")
            print("- Created docs/project-intake.md with required downstream governance fields.")
            return 0
        print("Downstream governance: FAIL")
        print("- Missing required intake file: docs/project-intake.md")
        return 1

    intake_text = intake_path.read_text(encoding="utf-8")
    values: dict[str, str | None] = {}

    for field in REQUIRED_INTAKE_FIELDS:
        value = _extract_field(intake_text, field)
        values[field] = value
        if _is_blank(value):
            failures.append(f"Missing or blank intake field: `{field}`")

    project_type = _normalize_project_type(values.get("Project type"))
    kpi_profile = _normalize_project_type(values.get("KPI profile"))
    downstream_profile = _normalize_project_type(values.get("Downstream governance profile"))

    if project_type in VALID_TYPED_PROJECTS and kpi_profile != project_type:
        failures.append(
            "KPI profile must match project type for `Producer`, `Archiavellian`, and `Archive` projects."
        )
    if project_type in VALID_TYPED_PROJECTS and downstream_profile != project_type:
        failures.append(
            "Downstream governance profile must match project type for `Producer`, `Archiavellian`, and `Archive` projects."
        )

    if failures and args.fix:
        fixed_text, changed_fields = _apply_fixes(intake_path, intake_text, values)
        if fixed_text != intake_text:
            intake_path.write_text(fixed_text, encoding="utf-8")
            print("Downstream governance: FIXED")
            if changed_fields:
                print(f"- Updated fields: {', '.join(changed_fields)}")
            else:
                print("- No field updates were needed.")
            return 0

    if failures:
        print("Downstream governance: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Downstream governance: PASS")
    print("All required downstream governance intake fields are present and valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
