#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PM_PORTAL = ROOT / "pm-portal"
MOBILE_POLICY_DOC = PM_PORTAL / "docs" / "mobile-compliance-governance.md"
MOBILE_DISCLOSURE_DOC = PM_PORTAL / "docs" / "mobile-privacy-and-disclosures.md"
MOBILE_GOVERNANCE_JSON = PM_PORTAL / "backend" / "config" / "mobile-compliance-governance.json"
MOBILE_DISCLOSURE_JSON = PM_PORTAL / "backend" / "config" / "mobile-store-disclosures.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _require_keys(payload: dict, keys: list[str], label: str) -> list[str]:
    missing = [k for k in keys if k not in payload]
    return [f"{label}: missing key `{k}`" for k in missing]


def main() -> int:
    failures: list[str] = []

    for path in [MOBILE_POLICY_DOC, MOBILE_DISCLOSURE_DOC, MOBILE_GOVERNANCE_JSON, MOBILE_DISCLOSURE_JSON]:
        if not path.exists():
            failures.append(f"missing file: {path.relative_to(ROOT)}")

    if failures:
        print("FAIL: mobile governance validation failed.")
        for msg in failures:
            print(f"- {msg}")
        return 1

    governance = _load_json(MOBILE_GOVERNANCE_JSON)
    disclosures = _load_json(MOBILE_DISCLOSURE_JSON)

    failures.extend(
        _require_keys(
            governance,
            ["policy_version", "owners", "shared_gates", "apple", "android", "stop_ship_conditions", "disclosure_policy"],
            "mobile-compliance-governance.json",
        )
    )
    failures.extend(
        _require_keys(
            disclosures,
            [
                "version",
                "source_alignment",
                "app_purpose",
                "allowed_data_classes",
                "prohibited_data_classes",
                "user_disclosures",
                "apple_required_checks",
                "google_required_checks",
                "sdk_governance_rules",
                "release_blockers",
            ],
            "mobile-store-disclosures.json",
        )
    )

    disclosure_policy = governance.get("disclosure_policy", {})
    expected_doc = "docs/mobile-privacy-and-disclosures.md"
    expected_json = "backend/config/mobile-store-disclosures.json"
    if disclosure_policy.get("privacy_doc") != expected_doc:
        failures.append("mobile-compliance-governance.json: disclosure_policy.privacy_doc mismatch")
    if disclosure_policy.get("store_disclosure_config") != expected_json:
        failures.append("mobile-compliance-governance.json: disclosure_policy.store_disclosure_config mismatch")

    if len(disclosures.get("user_disclosures", [])) < 3:
        failures.append("mobile-store-disclosures.json: expected at least 3 user disclosures")
    if len(disclosures.get("release_blockers", [])) < 3:
        failures.append("mobile-store-disclosures.json: expected at least 3 release blockers")

    if failures:
        print("FAIL: mobile governance validation failed.")
        for msg in failures:
            print(f"- {msg}")
        return 1

    print("PASS: mobile governance/disclosure docs and configs are present and structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
