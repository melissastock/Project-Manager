#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "docs/delivery/backlog.md",
    "docs/delivery/sprint-plan.md",
    "docs/delivery/test-report.md",
    "docs/delivery/pr-readiness.md",
]

GTM_REQUIRED_FILES = [
    "docs/gtm-hypotheses-and-pilot-plan.md",
    "docs/pilot-outreach-brief.md",
]

INVESTOR_REQUIRED_FILES = [
    "docs/investor-book-template.md",
    "docs/investor-book-section-coverage.md",
]

MONETIZATION_REQUIRED_FILES = [
    "docs/monetization-strategy.md",
    "docs/pricing-implementation-plan.md",
]


def load(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def intake_flag_enabled(intake_text: str, label: str) -> bool:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}\s*:\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(intake_text)
    if not match:
        return False
    value = match.group(1).strip().lower()
    return value in {"yes", "y", "true", "required", "1"}


def checklist_complete(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines()]
    checklist = [line for line in lines if line.startswith("- [")]
    if not checklist:
        return False
    return all(line.startswith("- [x]") or line.startswith("- [X]") for line in checklist)


def contains_testing_notes(text: str) -> bool:
    lowered = text.lower()
    return "pass" in lowered and "fail" in lowered and "not tested" in lowered


def contains_sprint_scope(text: str) -> bool:
    lowered = text.lower()
    return "committed scope" in lowered and "sprint goal" in lowered


def contains_grooming(text: str) -> bool:
    lowered = text.lower()
    return "last groomed" in lowered and "prioritized items" in lowered


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check agile production readiness before opening a PR."
    )
    parser.add_argument("--target", required=True, help="Target project path to validate.")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target

    failures: list[str] = []

    for rel in REQUIRED_FILES:
        path = target / rel
        if not path.exists():
            failures.append(f"Missing required file: {rel}")

    backlog = load(target / "docs/delivery/backlog.md")
    sprint = load(target / "docs/delivery/sprint-plan.md")
    tests = load(target / "docs/delivery/test-report.md")
    readiness = load(target / "docs/delivery/pr-readiness.md")
    intake = load(target / "docs/project-intake.md")

    if backlog and not contains_grooming(backlog):
        failures.append("Backlog does not include grooming metadata and prioritized items.")
    if sprint and not contains_sprint_scope(sprint):
        failures.append("Sprint plan is missing sprint goal or committed scope section.")
    if tests and not contains_testing_notes(tests):
        failures.append("Test report must include pass/fail/not tested notes.")
    if readiness and not checklist_complete(readiness):
        failures.append("PR readiness checklist is not fully checked.")

    gtm_required = intake_flag_enabled(intake, "GTM workflow needed")
    if gtm_required:
        for rel in GTM_REQUIRED_FILES:
            if not (target / rel).exists():
                failures.append(f"GTM workflow required by intake, missing file: {rel}")

    investor_required = intake_flag_enabled(intake, "Investor-book workflow needed")
    if investor_required:
        for rel in INVESTOR_REQUIRED_FILES:
            if not (target / rel).exists():
                failures.append(f"Investor-book workflow required by intake, missing file: {rel}")

    monetization_required = intake_flag_enabled(intake, "Monetization workflow needed")
    if monetization_required:
        for rel in MONETIZATION_REQUIRED_FILES:
            if not (target / rel).exists():
                failures.append(f"Monetization workflow required by intake, missing file: {rel}")

    if failures:
        print("Production readiness: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Production readiness: PASS")
    print("All required agile planning and test artifacts are present and complete.")
    if gtm_required:
        print("Conditional gate: GTM workflow required and validated.")
    if investor_required:
        print("Conditional gate: Investor-book workflow required and validated.")
    if monetization_required:
        print("Conditional gate: Monetization workflow required and validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
