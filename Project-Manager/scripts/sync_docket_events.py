#!/usr/bin/env python3
"""Normalize court docket export CSVs into docket-events.csv."""

from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
PM_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PM_ROOT / "outputs" / "docket-inputs"

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from bg_legal_paths import BG_LEGAL_DIR

TARGET = BG_LEGAL_DIR / "docs" / "timeline-evidence" / "docket-events.csv"

TARGET_HEADERS = [
    "docket_event_id",
    "source_connector",
    "jurisdiction",
    "court_name",
    "case_number",
    "related_case_numbers",
    "party_role",
    "event_date",
    "event_time",
    "event_type",
    "docket_text",
    "document_ref",
    "filing_party",
    "judge",
    "status",
    "retrieved_at",
    "source_hash",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize docket CSV exports.")
    parser.add_argument(
        "--input-glob",
        default="*.csv",
        help="Glob pattern relative to outputs/docket-inputs/.",
    )
    parser.add_argument(
        "--source-connector",
        required=True,
        choices=["denton-county-tx", "denver-county-co", "denver-municipal-co"],
    )
    parser.add_argument("--jurisdiction", required=True)
    parser.add_argument("--court-name", required=True)
    parser.add_argument("--party-role", default="defendant")
    parser.add_argument("--append", action="store_true", help="Append instead of overwrite.")
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_hash(parts: List[str]) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return digest


def read_rows(input_paths: List[Path]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for path in input_paths:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows.append({k.strip(): (v or "").strip() for k, v in row.items()})
    return rows


def load_existing_target() -> Tuple[List[Dict[str, str]], Dict[str, Dict[str, str]], int]:
    if not TARGET.exists():
        return [], {}, 0
    with TARGET.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    by_hash = {row.get("source_hash", ""): row for row in rows if row.get("source_hash")}
    max_id = 0
    for row in rows:
        raw_id = row.get("docket_event_id", "")
        # Pattern: DKT-<CONNECTOR>-00001
        suffix = raw_id.rsplit("-", 1)[-1] if "-" in raw_id else ""
        if suffix.isdigit():
            max_id = max(max_id, int(suffix))
    return rows, by_hash, max_id


def main() -> None:
    args = parse_args()
    input_paths = sorted(OUT_DIR.glob(args.input_glob))
    if not input_paths:
        raise SystemExit(f"No input files found in {OUT_DIR} for glob: {args.input_glob}")

    raw_rows = read_rows(input_paths)
    if not raw_rows:
        raise SystemExit("Input CSV files contained no data rows.")

    normalized: List[Dict[str, str]] = []
    retrieved_at = now_iso()

    existing_rows, existing_by_hash, max_existing_id = load_existing_target()
    next_id = max_existing_id + 1
    added = 0
    updated = 0
    skipped = 0

    for idx, raw in enumerate(raw_rows, start=1):
        case_number = raw.get("case_number") or raw.get("case") or raw.get("case_no") or ""
        event_date = raw.get("event_date") or raw.get("date") or raw.get("filed_date") or ""
        event_time = raw.get("event_time") or raw.get("time") or ""
        event_type = raw.get("event_type") or raw.get("type") or raw.get("entry_type") or "docket-entry"
        docket_text = raw.get("docket_text") or raw.get("description") or raw.get("text") or ""
        document_ref = raw.get("document_ref") or raw.get("document") or raw.get("doc_link") or ""
        filing_party = raw.get("filing_party") or raw.get("party") or ""
        judge = raw.get("judge") or ""
        status = raw.get("status") or "unknown"
        related = raw.get("related_case_numbers") or raw.get("related_cases") or ""

        source_hash = stable_hash(
            [
                args.source_connector,
                case_number,
                event_date,
                event_time,
                event_type,
                docket_text,
                document_ref,
            ]
        )
        maybe_existing = existing_by_hash.get(source_hash)
        if maybe_existing:
            refreshed = dict(maybe_existing)
            refreshed.update(
                {
                    "source_connector": args.source_connector,
                    "jurisdiction": args.jurisdiction,
                    "court_name": args.court_name,
                    "case_number": case_number,
                    "related_case_numbers": related,
                    "party_role": args.party_role,
                    "event_date": event_date,
                    "event_time": event_time,
                    "event_type": event_type,
                    "docket_text": docket_text,
                    "document_ref": document_ref,
                    "filing_party": filing_party,
                    "judge": judge,
                    "status": status,
                    "retrieved_at": retrieved_at,
                    "source_hash": source_hash,
                }
            )
            normalized.append(refreshed)
            updated += 1
            continue

        normalized.append(
            {
                "docket_event_id": f"DKT-{args.source_connector.upper()}-{next_id:05d}",
                "source_connector": args.source_connector,
                "jurisdiction": args.jurisdiction,
                "court_name": args.court_name,
                "case_number": case_number,
                "related_case_numbers": related,
                "party_role": args.party_role,
                "event_date": event_date,
                "event_time": event_time,
                "event_type": event_type,
                "docket_text": docket_text,
                "document_ref": document_ref,
                "filing_party": filing_party,
                "judge": judge,
                "status": status,
                "retrieved_at": retrieved_at,
                "source_hash": source_hash,
                "notes": "",
            }
        )
        next_id += 1
        added += 1

    # Preserve existing rows that were not touched in this run unless overwrite requested.
    new_hashes = {row["source_hash"] for row in normalized if row.get("source_hash")}
    untouched_existing = [row for row in existing_rows if row.get("source_hash") not in new_hashes]
    skipped = len(untouched_existing)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    mode = "w"
    with TARGET.open(mode, newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=TARGET_HEADERS)
        writer.writeheader()
        # Keep historical untouched rows, then refreshed/new rows.
        for row in untouched_existing:
            writer.writerow(row)
        for row in normalized:
            writer.writerow(row)

    print(f"Synced docket events -> {TARGET}")
    print(f"added={added} updated={updated} untouched_preserved={skipped} total={len(untouched_existing)+len(normalized)}")


if __name__ == "__main__":
    main()
