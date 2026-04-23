#!/usr/bin/env python3
"""Set compliance flags on a portal session JSON."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set portal compliance flags.")
    parser.add_argument("--session-file", required=True, help="Path to session JSON.")
    parser.add_argument("--output", help="Optional output path (defaults in-place).")
    parser.add_argument("--assertion-test-complete", help="true|false")
    parser.add_argument("--legal-privacy-review-complete", help="true|false")
    parser.add_argument("--raw-evidence-copied", help="true|false")
    parser.add_argument("--reviewed-by", default="", help="Reviewer name/identifier.")
    parser.add_argument("--review-note", default="", help="Optional review note.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    session_path = Path(args.session_file)
    output_path = Path(args.output) if args.output else session_path

    obj = json.loads(session_path.read_text(encoding="utf-8"))
    compliance = obj.setdefault("compliance", {})

    changed = False
    if args.assertion_test_complete is not None:
        compliance["assertion_test_complete"] = parse_bool(args.assertion_test_complete)
        changed = True
    if args.legal_privacy_review_complete is not None:
        compliance["legal_privacy_review_complete"] = parse_bool(
            args.legal_privacy_review_complete
        )
        changed = True
    if args.raw_evidence_copied is not None:
        compliance["raw_evidence_copied"] = parse_bool(args.raw_evidence_copied)
        changed = True

    if changed:
        compliance["last_reviewed_at"] = now_iso()
    if args.reviewed_by:
        compliance["last_reviewed_by"] = args.reviewed_by
    if args.review_note:
        obj.setdefault("strategy", {}).setdefault("counsel_questions", []).append(
            f"Compliance note: {args.review_note}"
        )

    obj.setdefault("session", {})["updated_at"] = now_iso()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")

    print(f"Updated compliance: {output_path}")
    print(
        "assertion_test_complete="
        f"{compliance.get('assertion_test_complete')} "
        "legal_privacy_review_complete="
        f"{compliance.get('legal_privacy_review_complete')} "
        "raw_evidence_copied="
        f"{compliance.get('raw_evidence_copied')}"
    )


if __name__ == "__main__":
    main()
