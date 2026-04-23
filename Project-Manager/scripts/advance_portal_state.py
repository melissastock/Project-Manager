#!/usr/bin/env python3
"""Advance a portal session state with transition and gate enforcement."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ALLOWED_TRANSITIONS: Dict[str, List[str]] = {
    "intake-started": ["intake-complete"],
    "intake-complete": ["route-assigned"],
    "route-assigned": ["timeline-triage"],
    "timeline-triage": ["strategy-ranking"],
    "strategy-ranking": ["motion-drafting"],
    "motion-drafting": ["review-gate"],
    "review-gate": ["counsel-review", "pro-se-filing-ready"],
    "counsel-review": ["execution-tracking"],
    "pro-se-filing-ready": ["execution-tracking"],
    "execution-tracking": ["closed-or-paused"],
    "closed-or-paused": [],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Advance a session state with gate checks."
    )
    parser.add_argument("--session-file", required=True, help="Path to session JSON.")
    parser.add_argument("--to-state", required=True, help="Desired next state.")
    parser.add_argument("--note", default="", help="Optional transition note.")
    parser.add_argument("--output", help="Optional output path (defaults in-place).")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bypass gate checks (still enforces adjacency transitions).",
    )
    return parser.parse_args()


def require(value: bool, message: str, errors: List[str]) -> None:
    if not value:
        errors.append(message)


def check_gates(session_obj: Dict, to_state: str) -> List[str]:
    errors: List[str] = []
    session = session_obj.get("session", {})
    intake = session_obj.get("intake", {})
    strategy = session_obj.get("strategy", {})
    metrics = session_obj.get("metrics", {})
    compliance = session_obj.get("compliance", {})

    representation_status = session.get("representation_status", "")
    route_id = session.get("route_id", "")
    pathway = session.get("pathway", "")
    stage = session.get("stage", "")

    if to_state == "route-assigned":
        require(bool(representation_status), "Missing representation_status.", errors)
        require(bool(route_id), "Missing route_id.", errors)
        require(bool(pathway), "Missing pathway.", errors)

    elif to_state == "timeline-triage":
        require(bool(intake.get("top_events")), "top_events must be initialized.", errors)
        require(bool(intake.get("top_sources")), "top_sources must be initialized.", errors)

    elif to_state == "strategy-ranking":
        require(metrics.get("events_linked", 0) > 0, "events_linked must be > 0.", errors)
        require(metrics.get("evidence_linked", 0) > 0, "evidence_linked must be > 0.", errors)

    elif to_state == "motion-drafting":
        readiness = metrics.get("avenues_ranked", 0)
        require(readiness > 0, "avenues_ranked must be > 0.", errors)

    elif to_state == "review-gate":
        require(
            metrics.get("motions_in_draft", 0) > 0 or metrics.get("motions_ready", 0) > 0,
            "Need at least one motion in draft or ready.",
            errors,
        )

    elif to_state == "counsel-review":
        require(
            representation_status == "represented-by-lawyer",
            "counsel-review requires represented-by-lawyer pathway.",
            errors,
        )
        require(
            bool(compliance.get("legal_privacy_review_complete")),
            "legal_privacy_review_complete must be true.",
            errors,
        )

    elif to_state == "pro-se-filing-ready":
        require(
            representation_status in {"pro-se", "unsure-pending-counsel"},
            "pro-se-filing-ready requires pro-se or unsure-pending-counsel.",
            errors,
        )
        require(
            bool(compliance.get("assertion_test_complete")),
            "assertion_test_complete must be true for pro-se-filing-ready.",
            errors,
        )

    elif to_state == "execution-tracking":
        require(
            stage in {
                "investigation",
                "charging",
                "arraignment",
                "pretrial",
                "trial",
                "post-conviction",
            },
            "Session stage must be a recognized stage.",
            errors,
        )

    elif to_state == "closed-or-paused":
        # Keep lightweight: require at least one prior history transition.
        require(
            len(session.get("state_history", [])) > 0,
            "Need state_history entries before closing/pausing.",
            errors,
        )

    # Example shared check for higher workflow states.
    higher_states = {
        "strategy-ranking",
        "motion-drafting",
        "review-gate",
        "counsel-review",
        "pro-se-filing-ready",
        "execution-tracking",
        "closed-or-paused",
    }
    if to_state in higher_states:
        require(bool(route_id), "route_id must be set.", errors)

    # Optional strategy context check.
    if to_state in {"review-gate", "counsel-review", "pro-se-filing-ready"}:
        require(
            metrics.get("open_gaps", 0) >= 0 and isinstance(metrics.get("open_gaps", 0), int),
            "open_gaps must be an integer.",
            errors,
        )
        require(
            isinstance(strategy.get("rights_flags", []), list),
            "strategy.rights_flags must be a list.",
            errors,
        )

    return errors


def validate_transition(current: str, target: str) -> Tuple[bool, str]:
    if current not in ALLOWED_TRANSITIONS:
        return False, f"Unknown current state: {current}"
    if target not in ALLOWED_TRANSITIONS:
        return False, f"Unknown target state: {target}"
    if target not in ALLOWED_TRANSITIONS[current]:
        allowed = ", ".join(ALLOWED_TRANSITIONS[current]) or "(none)"
        return (
            False,
            f"Invalid transition {current} -> {target}. Allowed next: {allowed}",
        )
    return True, ""


def main() -> None:
    args = parse_args()
    session_path = Path(args.session_file)
    output_path = Path(args.output) if args.output else session_path
    session_obj = json.loads(session_path.read_text(encoding="utf-8"))

    current = session_obj.get("session", {}).get("current_state", "")
    target = args.to_state
    ok, message = validate_transition(current, target)
    if not ok:
        raise SystemExit(message)

    gate_errors = []
    if not args.force:
        gate_errors = check_gates(session_obj, target)
    if gate_errors:
        details = "\n".join(f"- {err}" for err in gate_errors)
        raise SystemExit(f"Gate check failed for transition to {target}:\n{details}")

    session = session_obj["session"]
    session.setdefault("state_history", []).append(
        {"from": current, "to": target, "at": now_iso(), "note": args.note}
    )
    session["current_state"] = target
    session["updated_at"] = now_iso()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(session_obj, indent=2) + "\n", encoding="utf-8")
    print(f"Advanced session: {current} -> {target}")
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
