#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PM_ROOT = Path(__file__).resolve().parents[1]
INTAKE_REL = "docs/project-intake.md"
BLANK = {"", "tbd", "na", "n/a", "none", "not set", "unknown"}

PRIMARY_PERSONA = "Primary user persona"
MODULAR_INSTANCE = "Modular instance type(s)"
PORTFOLIO_ORIENTATION = "Portfolio orientation (`horizontal` / `vertical`)"
PERSONA_STATUS = "Persona validation status (`pending` / `validated`)"
PERSONA_EVIDENCE = "Persona research evidence path"
PERSONA_CONFIDENCE = "Persona research confidence (`low` / `medium` / `high`)"
PERSONA_LAST_DATE = "Last persona validation date"
LIFECYCLE_LABEL = "Lifecycle state (`not-onboarded` / `governed` / `execution-ready` / `launch-ready` / `scaled`)"

VALID_ORIENTATION = {"horizontal", "vertical"}
VALID_STATUS = {"pending", "validated"}
VALID_CONFIDENCE = {"low", "medium", "high"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _extract(text: str, label: str) -> str:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}\s*:\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE)
    m = pattern.search(text)
    return m.group(1).strip() if m else ""


def _is_blank(value: str) -> bool:
    return value.strip().lower() in BLANK


def _replace_or_insert(text: str, label: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(rf"(^\s*-\s*{re.escape(label)}\s*:\s*)(.*)$", re.IGNORECASE | re.MULTILINE)
    m = pattern.search(text)
    if m:
        cur = m.group(2).strip()
        if cur == value:
            return text, False
        if cur and cur.lower() not in BLANK:
            return text, False
        updated = text[: m.start(2)] + value + text[m.end(2) :]
        return updated, True
    anchor = re.search(r"^##\s+Delivery Shape\s*$", text, re.IGNORECASE | re.MULTILINE)
    if anchor:
        pos = anchor.end()
        return text[:pos] + f"\n\n- {label}: {value}" + text[pos:], True
    return text.rstrip() + f"\n\n## Delivery Shape\n\n- {label}: {value}\n", True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate persona, modular-instance, orientation, and research evidence layer."
    )
    parser.add_argument("--target", required=True, help="Target project path.")
    parser.add_argument("--fix", action="store_true", help="Auto-fill missing persona/research metadata.")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target

    intake = target / INTAKE_REL
    if not intake.exists():
        print("Persona research layer: FAIL")
        print(f"- Missing required intake file: {INTAKE_REL}")
        return 1

    text = _read(intake)

    primary = _extract(text, PRIMARY_PERSONA)
    modular = _extract(text, MODULAR_INSTANCE)
    orientation = _extract(text, PORTFOLIO_ORIENTATION).lower()
    persona_status = _extract(text, PERSONA_STATUS).lower()
    evidence_path = _extract(text, PERSONA_EVIDENCE)
    confidence = _extract(text, PERSONA_CONFIDENCE).lower()
    last_date = _extract(text, PERSONA_LAST_DATE)
    lifecycle = _extract(text, LIFECYCLE_LABEL).lower()

    failures: list[str] = []
    if _is_blank(primary):
        failures.append(f"Missing or blank intake field: `{PRIMARY_PERSONA}`")
    if _is_blank(modular):
        failures.append(f"Missing or blank intake field: `{MODULAR_INSTANCE}`")
    if orientation not in VALID_ORIENTATION:
        failures.append(f"`{PORTFOLIO_ORIENTATION}` must be one of: horizontal, vertical.")
    if persona_status not in VALID_STATUS:
        failures.append(f"`{PERSONA_STATUS}` must be one of: pending, validated.")
    if confidence not in VALID_CONFIDENCE:
        failures.append(f"`{PERSONA_CONFIDENCE}` must be one of: low, medium, high.")
    if _is_blank(evidence_path):
        failures.append(f"Missing or blank intake field: `{PERSONA_EVIDENCE}`")
    if _is_blank(last_date):
        failures.append(f"Missing or blank intake field: `{PERSONA_LAST_DATE}`")

    # Lifecycle-sensitive enforcement.
    if lifecycle in {"execution-ready", "launch-ready", "scaled"}:
        if persona_status != "validated":
            failures.append("Lifecycle requires persona validation status `validated`.")
        if confidence not in {"medium", "high"}:
            failures.append("Lifecycle requires persona research confidence of at least `medium`.")
    if lifecycle in {"launch-ready", "scaled"} and confidence != "high":
        failures.append("Launch/scaled lifecycle requires persona research confidence `high`.")

    if evidence_path and not _is_blank(evidence_path):
        p = target / evidence_path
        if not p.exists():
            failures.append(f"Persona research evidence path does not exist: {evidence_path}")

    if failures and args.fix:
        fixed = text
        changed = []
        defaults = {
            PRIMARY_PERSONA: "delivery lead",
            MODULAR_INSTANCE: "delivery-core",
            PORTFOLIO_ORIENTATION: "vertical",
            PERSONA_STATUS: "pending",
            PERSONA_EVIDENCE: "docs/research/persona-validation-notes.md",
            PERSONA_CONFIDENCE: "low",
            PERSONA_LAST_DATE: "2026-04-21",
        }
        for label, value in defaults.items():
            fixed, did = _replace_or_insert(fixed, label, value)
            if did:
                changed.append(label)

        evidence_file = target / "docs/research/persona-validation-notes.md"
        if not evidence_file.exists():
            evidence_file.parent.mkdir(parents=True, exist_ok=True)
            template = PM_ROOT / "templates/research/persona-validation-notes-template.md"
            if template.exists():
                evidence_file.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                evidence_file.write_text("# Persona Validation Notes\n", encoding="utf-8")

        if fixed != text:
            intake.write_text(fixed, encoding="utf-8")

        print("Persona research layer: FIXED")
        if changed:
            print(f"- Updated fields: {', '.join(changed)}")
        print("- Ensured persona research evidence artifact exists.")
        return 0

    if failures:
        print("Persona research layer: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Persona research layer: PASS")
    print("Persona, modular-instance, orientation, and research evidence layer are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
