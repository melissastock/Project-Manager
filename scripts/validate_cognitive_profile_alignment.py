#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INTAKE_REL = "docs/project-intake.md"
PROFILE_CONFIG = ROOT / "config/cognitive-profiles.json"
BLANK = {"", "tbd", "na", "n/a", "none", "not set", "unknown"}

PROFILE_LABEL = "Creator cognitive profile (`adhd` / `audhd` / `autistic` / `neurotypical`)"
PREFERENCES_LABEL = "Creator workflow preferences"
FOCUS_PLAN_LABEL = "Focus plan artifact path"
CLOSEOUT_RHYTHM_LABEL = "Closeout rhythm artifact path"

VALID_PROFILES = {"adhd", "audhd", "autistic", "neurotypical"}


def _extract(text: str, label: str) -> str:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}\s*:\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _is_blank(value: str) -> bool:
    return value.strip().lower() in BLANK


def _replace_or_insert(text: str, label: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(rf"(^\s*-\s*{re.escape(label)}\s*:\s*)(.*)$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    if match:
        current = match.group(2).strip()
        if current == value:
            return text, False
        if current and current.lower() not in BLANK:
            return text, False
        updated = text[: match.start(2)] + value + text[match.end(2) :]
        return updated, True
    anchor = re.search(r"^##\s+Delivery Shape\s*$", text, re.IGNORECASE | re.MULTILINE)
    if anchor:
        pos = anchor.end()
        return text[:pos] + f"\n\n- {label}: {value}" + text[pos:], True
    return text.rstrip() + f"\n\n## Delivery Shape\n\n- {label}: {value}\n", True


def _ensure_artifact(path: Path, template_path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if template_path.exists():
        path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        path.write_text("# Placeholder\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate cognitive profile metadata and self-imposed workflow artifacts."
    )
    parser.add_argument("--target", required=True, help="Target project path.")
    parser.add_argument("--fix", action="store_true", help="Auto-fill missing profile fields and scaffold artifacts.")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target

    intake = target / INTAKE_REL
    if not intake.exists():
        print("Cognitive profile alignment: FAIL")
        print(f"- Missing required intake file: {INTAKE_REL}")
        return 1

    config_raw = PROFILE_CONFIG.read_text(encoding="utf-8")
    profiles = set(json.loads(config_raw).get("profiles", {}).keys())
    valid_profiles = VALID_PROFILES & profiles if profiles else VALID_PROFILES

    text = intake.read_text(encoding="utf-8")
    profile = _extract(text, PROFILE_LABEL).lower()
    preferences = _extract(text, PREFERENCES_LABEL)
    focus_path = _extract(text, FOCUS_PLAN_LABEL)
    closeout_path = _extract(text, CLOSEOUT_RHYTHM_LABEL)

    failures: list[str] = []
    if profile not in valid_profiles:
        failures.append(f"`{PROFILE_LABEL}` must be one of: {', '.join(sorted(valid_profiles))}.")
    if _is_blank(preferences):
        failures.append(f"Missing or blank intake field: `{PREFERENCES_LABEL}`")
    if _is_blank(focus_path):
        failures.append(f"Missing or blank intake field: `{FOCUS_PLAN_LABEL}`")
    if _is_blank(closeout_path):
        failures.append(f"Missing or blank intake field: `{CLOSEOUT_RHYTHM_LABEL}`")

    if focus_path and not _is_blank(focus_path) and not (target / focus_path).exists():
        failures.append(f"Focus plan artifact path does not exist: {focus_path}")
    if closeout_path and not _is_blank(closeout_path) and not (target / closeout_path).exists():
        failures.append(f"Closeout rhythm artifact path does not exist: {closeout_path}")

    if failures and args.fix:
        updated = text
        changed: list[str] = []
        defaults = {
            PROFILE_LABEL: "neurotypical",
            PREFERENCES_LABEL: "Prefer clear milestones, explicit priorities, and predictable check-ins.",
            FOCUS_PLAN_LABEL: "docs/process/creator-focus-plan.md",
            CLOSEOUT_RHYTHM_LABEL: "docs/process/creator-closeout-rhythm.md",
        }
        for label, value in defaults.items():
            updated, did = _replace_or_insert(updated, label, value)
            if did:
                changed.append(label)
        if updated != text:
            intake.write_text(updated, encoding="utf-8")

        _ensure_artifact(
            target / "docs/process/creator-focus-plan.md",
            ROOT / "templates/process/creator-focus-plan-template.md",
        )
        _ensure_artifact(
            target / "docs/process/creator-closeout-rhythm.md",
            ROOT / "templates/process/creator-closeout-rhythm-template.md",
        )

        print("Cognitive profile alignment: FIXED")
        if changed:
            print(f"- Updated fields: {', '.join(changed)}")
        print("- Ensured creator focus and closeout rhythm artifacts exist.")
        return 0

    if failures:
        print("Cognitive profile alignment: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Cognitive profile alignment: PASS")
    print("Cognitive profile metadata and self-imposed workflow artifacts are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
