#!/usr/bin/env python3
"""Generate case dependencies from normalized docket events."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from bg_legal_paths import BG_LEGAL_DIR

DOCKET_EVENTS = BG_LEGAL_DIR / "docs" / "timeline-evidence" / "docket-events.csv"
DEPENDENCIES = BG_LEGAL_DIR / "docs" / "timeline-evidence" / "case-dependencies.csv"

DEP_HEADERS = [
    "dependency_id",
    "case_number",
    "depends_on_case_number",
    "dependency_type",
    "trigger_event_id",
    "legal_effect",
    "priority",
    "status",
    "review_status",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Link cross-case dependencies.")
    parser.add_argument("--append", action="store_true", help="Append dependencies instead of overwrite.")
    return parser.parse_args()


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def split_related(value: str) -> List[str]:
    normalized = value.replace(",", ";")
    return [part.strip() for part in normalized.split(";") if part.strip()]


def dependency_type(court_name: str, case_a: str, case_b: str) -> str:
    lower = court_name.lower()
    if "municipal" in lower:
        return "municipal-to-county-overlap"
    if "county" in lower:
        return "county-cross-case-impact"
    return "cross-case-impact"


def main() -> None:
    args = parse_args()
    events = read_csv(DOCKET_EVENTS)

    generated: List[Dict[str, str]] = []
    seen: Set[Tuple[str, str, str]] = set()
    dep_index = 1
    for event in events:
        case_number = (event.get("case_number") or "").strip()
        if not case_number:
            continue
        related_cases = split_related(event.get("related_case_numbers", ""))
        for related in related_cases:
            key = (case_number, related, event.get("docket_event_id", ""))
            if key in seen:
                continue
            seen.add(key)
            dtype = dependency_type(event.get("court_name", ""), case_number, related)
            generated.append(
                {
                    "dependency_id": f"DEP-AUTO-{dep_index:05d}",
                    "case_number": case_number,
                    "depends_on_case_number": related,
                    "dependency_type": dtype,
                    "trigger_event_id": event.get("docket_event_id", ""),
                    "legal_effect": "Potential filing, hearing, or discovery impact across related matters",
                    "priority": "medium",
                    "status": "open",
                    "review_status": "reference-level-unreviewed",
                    "notes": "Auto-linked from related_case_numbers field",
                }
            )
            dep_index += 1

    DEPENDENCIES.parent.mkdir(parents=True, exist_ok=True)

    existing: List[Dict[str, str]] = []
    if DEPENDENCIES.exists():
        existing = read_csv(DEPENDENCIES)

    existing_keyed: Dict[Tuple[str, str, str], Dict[str, str]] = {}
    for row in existing:
        key = (
            (row.get("case_number") or "").strip(),
            (row.get("depends_on_case_number") or "").strip(),
            (row.get("trigger_event_id") or "").strip(),
        )
        if key[0] and key[1] and key[2]:
            existing_keyed[key] = row

    merged: List[Dict[str, str]] = []
    preserved = 0
    for row in existing:
        key = (
            (row.get("case_number") or "").strip(),
            (row.get("depends_on_case_number") or "").strip(),
            (row.get("trigger_event_id") or "").strip(),
        )
        if key in existing_keyed:
            merged.append(row)
            preserved += 1
        else:
            merged.append(row)

    added = 0
    for row in generated:
        key = (
            (row.get("case_number") or "").strip(),
            (row.get("depends_on_case_number") or "").strip(),
            (row.get("trigger_event_id") or "").strip(),
        )
        if key in existing_keyed:
            continue
        merged.append(row)
        added += 1

    with DEPENDENCIES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=DEP_HEADERS)
        writer.writeheader()
        for row in merged:
            writer.writerow(row)

    print(f"Dependency sync complete -> {DEPENDENCIES}")
    print(f"generated={len(generated)} added={added} preserved_existing={preserved} total={len(merged)}")


if __name__ == "__main__":
    main()
