#!/usr/bin/env python3
"""Update an existing portal session with transitions, metrics, and routing."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
import sys
from pathlib import Path
from typing import Dict, List

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from bg_legal_paths import ROOT, TIMELINE_EVIDENCE_DIR

TIMELINE_DIR = TIMELINE_EVIDENCE_DIR
ROUTING_CSV = TIMELINE_DIR / "intake-routing.csv"

ALLOWED_STATES = {
    "intake-started",
    "intake-complete",
    "route-assigned",
    "timeline-triage",
    "strategy-ranking",
    "motion-drafting",
    "review-gate",
    "counsel-review",
    "pro-se-filing-ready",
    "execution-tracking",
    "closed-or-paused",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update a portal session with route/state/metrics changes."
    )
    parser.add_argument("--session-file", required=True, help="Path to existing session JSON.")
    parser.add_argument("--output", help="Optional output path (defaults to in-place update).")
    parser.add_argument(
        "--representation-status",
        choices=["represented-by-lawyer", "pro-se", "unsure-pending-counsel"],
    )
    parser.add_argument(
        "--stage",
        choices=[
            "investigation",
            "charging",
            "arraignment",
            "pretrial",
            "trial",
            "post-conviction",
        ],
    )
    parser.add_argument("--detained", choices=["true", "false"])
    parser.add_argument("--active-conditions", choices=["true", "false"])
    parser.add_argument("--deadline-within-14-days", choices=["true", "false"])
    parser.add_argument("--next-state", choices=sorted(ALLOWED_STATES))
    parser.add_argument("--state-note", default="")
    parser.add_argument("--events-linked", type=int)
    parser.add_argument("--evidence-linked", type=int)
    parser.add_argument("--avenues-ranked", type=int)
    parser.add_argument("--motions-in-draft", type=int)
    parser.add_argument("--motions-ready", type=int)
    parser.add_argument("--open-gaps", type=int)
    return parser.parse_args()


def parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    return value.lower() == "true"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def split_list(value: str) -> List[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def load_routes() -> List[Dict[str, str]]:
    with ROUTING_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def urgency_matches(condition: str, has_urgency: bool) -> bool:
    if condition.strip() == "none":
        return not has_urgency
    return has_urgency


def stage_matches(route_stage: str, selected_stage: str) -> bool:
    route_stage = route_stage.strip()
    if route_stage == "any":
        return True
    return selected_stage in [item.strip() for item in route_stage.split("|")]


def resolve_route(
    routes: List[Dict[str, str]],
    representation_status: str,
    stage: str,
    has_urgency: bool,
) -> Dict[str, str]:
    for route in routes:
        if route["representation_status"] != representation_status:
            continue
        if not urgency_matches(route["urgency_condition"], has_urgency):
            continue
        if not stage_matches(route["case_stage"], stage):
            continue
        return route
    raise RuntimeError(
        f"No matching route for representation_status={representation_status}, "
        f"stage={stage}, has_urgency={has_urgency}"
    )


def main() -> None:
    args = parse_args()
    session_path = Path(args.session_file)
    output_path = Path(args.output) if args.output else session_path

    session_obj = json.loads(session_path.read_text(encoding="utf-8"))
    session = session_obj["session"]
    workflow = session_obj["workflow"]
    metrics = session_obj["metrics"]

    # Update intake/routing selectors if provided.
    if args.representation_status:
        session["representation_status"] = args.representation_status
    if args.stage:
        session["stage"] = args.stage

    detained = parse_bool(args.detained)
    active_conditions = parse_bool(args.active_conditions)
    deadline_14 = parse_bool(args.deadline_within_14_days)

    if detained is not None:
        session["urgency_flags"]["detained"] = detained
    if active_conditions is not None:
        session["urgency_flags"]["active_conditions"] = active_conditions
    if deadline_14 is not None:
        session["urgency_flags"]["deadline_within_14_days"] = deadline_14

    has_urgency = any(
        [
            bool(session["urgency_flags"].get("detained")),
            bool(session["urgency_flags"].get("active_conditions")),
            bool(session["urgency_flags"].get("deadline_within_14_days")),
        ]
    )

    routes = load_routes()
    route = resolve_route(
        routes=routes,
        representation_status=session["representation_status"],
        stage=session["stage"],
        has_urgency=has_urgency,
    )
    session["route_id"] = route["route_id"]
    session["pathway"] = route["active_pathway"]

    workflow["activated_docs"] = split_list(route["activate_docs"])
    workflow["required_checklists"] = split_list(route["required_checklists"])
    workflow["cadence"] = route["default_cadence"]
    workflow["priority_profile"] = route["priority_profile"]
    workflow["escalation"] = route["escalation"]

    # Optional state transition.
    if args.next_state:
        prior = session.get("current_state", "")
        if prior != args.next_state:
            session.setdefault("state_history", []).append(
                {
                    "from": prior,
                    "to": args.next_state,
                    "at": now_iso(),
                    "note": args.state_note,
                }
            )
            session["current_state"] = args.next_state

    # Metrics updates.
    metric_updates = {
        "events_linked": args.events_linked,
        "evidence_linked": args.evidence_linked,
        "avenues_ranked": args.avenues_ranked,
        "motions_in_draft": args.motions_in_draft,
        "motions_ready": args.motions_ready,
        "open_gaps": args.open_gaps,
    }
    for key, value in metric_updates.items():
        if value is not None:
            metrics[key] = value

    session["updated_at"] = now_iso()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(session_obj, indent=2) + "\n", encoding="utf-8")

    print(f"Updated session: {output_path}")
    print(f"Route selected: {session['route_id']} ({session['pathway']})")
    print(f"Current state: {session['current_state']}")


if __name__ == "__main__":
    main()
