#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DISCLOSURE_PATH = ROOT / "pm-portal" / "backend" / "config" / "mobile-store-disclosures.json"

# Source-of-truth classes currently produced/persisted by PM Portal runtime behavior:
# - project metadata + readiness snapshots (service/ingestion/scoring models)
# - recommendation decisions (local json or Supabase table)
# - runtime observations (Supabase project_runtime_observations)
# - operational timestamps (generated_at/updated_at/observed_at)
RUNTIME_DATA_CLASSES = {
    "project_metadata",
    "readiness_signals",
    "recommendation_decisions",
    "runtime_observations",
    "operational_timestamps",
}

# Sensitive classes that must remain excluded from portal runtime and disclosures.
RESTRICTED_CLASSES = {
    "phi",
    "client_sensitive_source_files",
    "draft_legal_agreements",
    "financial_internals",
    "credentials_or_tokens",
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if not DISCLOSURE_PATH.exists():
        print(f"FAIL: missing disclosure config {DISCLOSURE_PATH.relative_to(ROOT)}")
        return 1

    payload = _load_json(DISCLOSURE_PATH)
    declared_allowed = set(payload.get("allowed_data_classes", []))
    declared_prohibited = set(payload.get("prohibited_data_classes", []))

    failures: list[str] = []

    missing_from_disclosure = sorted(RUNTIME_DATA_CLASSES - declared_allowed)
    if missing_from_disclosure:
        failures.append(
            "allowed_data_classes missing runtime classes: "
            + ", ".join(missing_from_disclosure)
        )

    undeclared_runtime = sorted(declared_allowed - RUNTIME_DATA_CLASSES)
    if undeclared_runtime:
        failures.append(
            "allowed_data_classes contains classes not mapped in runtime policy: "
            + ", ".join(undeclared_runtime)
        )

    missing_restricted = sorted(RESTRICTED_CLASSES - declared_prohibited)
    if missing_restricted:
        failures.append(
            "prohibited_data_classes missing restricted classes: "
            + ", ".join(missing_restricted)
        )

    overlap = sorted(declared_allowed & declared_prohibited)
    if overlap:
        failures.append(
            "data classes cannot be both allowed and prohibited: "
            + ", ".join(overlap)
        )

    user_disclosures = payload.get("user_disclosures", [])
    if not isinstance(user_disclosures, list) or len(user_disclosures) < 3:
        failures.append("expected at least 3 user_disclosures entries")
    else:
        text = " ".join(str(v).lower() for v in user_disclosures)
        for token in ("project", "privacy", "disclos", "sensitive"):
            if token not in text:
                failures.append(f"user_disclosures appears to miss expected keyword: {token}")

    if failures:
        print("FAIL: runtime-vs-disclosure drift detected.")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("PASS: runtime behavior and mobile disclosure config are aligned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
