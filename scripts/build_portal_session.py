#!/usr/bin/env python3
"""Build a portal session JSON from intake answers and routing rules."""

from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
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
TEMPLATE_JSON = TIMELINE_DIR / "portal-session-template.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build portal session JSON from intake routing rules."
    )
    parser.add_argument(
        "--representation-status",
        required=True,
        choices=["represented-by-lawyer", "pro-se", "unsure-pending-counsel"],
    )
    parser.add_argument(
        "--stage",
        default="pretrial",
        choices=[
            "investigation",
            "charging",
            "arraignment",
            "pretrial",
            "trial",
            "post-conviction",
        ],
    )
    parser.add_argument("--detained", action="store_true")
    parser.add_argument("--active-conditions", action="store_true")
    parser.add_argument("--deadline-within-14-days", action="store_true")
    parser.add_argument("--session-id", default="SESSION-0001")
    parser.add_argument("--case-label", default="")
    parser.add_argument("--jurisdiction", default="")
    parser.add_argument("--case-number", default="")
    parser.add_argument("--defendant-display-name", default="")
    parser.add_argument("--primary-goal", default="")
    parser.add_argument("--output", required=True, help="Path to output JSON file.")
    return parser.parse_args()


def load_routing_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def split_list(value: str) -> List[str]:
    return [piece.strip() for piece in value.split(";") if piece.strip()]


def any_urgency(detained: bool, active_conditions: bool, deadline_within_14_days: bool) -> bool:
    return detained or active_conditions or deadline_within_14_days


def urgency_matches(condition: str, has_urgency: bool) -> bool:
    condition = condition.strip()
    if condition == "none":
        return not has_urgency
    return has_urgency


def stage_matches(route_stage: str, selected_stage: str) -> bool:
    route_stage = route_stage.strip()
    if route_stage == "any":
        return True
    valid = [item.strip() for item in route_stage.split("|")]
    return selected_stage in valid


def resolve_route(
    rows: List[Dict[str, str]],
    representation_status: str,
    stage: str,
    has_urgency: bool,
) -> Dict[str, str]:
    for row in rows:
        if row["representation_status"] != representation_status:
            continue
        if not urgency_matches(row["urgency_condition"], has_urgency):
            continue
        if not stage_matches(row["case_stage"], stage):
            continue
        return row
    raise RuntimeError(
        f"No route found for representation_status={representation_status}, "
        f"stage={stage}, has_urgency={has_urgency}"
    )


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> None:
    args = parse_args()
    routing_rows = load_routing_rows(ROUTING_CSV)
    template = json.loads(TEMPLATE_JSON.read_text(encoding="utf-8"))
    session = deepcopy(template)

    has_urgency = any_urgency(
        detained=args.detained,
        active_conditions=args.active_conditions,
        deadline_within_14_days=args.deadline_within_14_days,
    )
    route = resolve_route(
        rows=routing_rows,
        representation_status=args.representation_status,
        stage=args.stage,
        has_urgency=has_urgency,
    )
    timestamp = now_iso()

    session["session"]["session_id"] = args.session_id
    session["session"]["created_at"] = timestamp
    session["session"]["updated_at"] = timestamp
    session["session"]["case_label"] = args.case_label
    session["session"]["jurisdiction"] = args.jurisdiction
    session["session"]["case_number"] = args.case_number
    session["session"]["defendant_display_name"] = args.defendant_display_name
    session["session"]["representation_status"] = args.representation_status
    session["session"]["pathway"] = route["active_pathway"]
    session["session"]["route_id"] = route["route_id"]
    session["session"]["stage"] = args.stage
    session["session"]["urgency_flags"] = {
        "detained": bool(args.detained),
        "active_conditions": bool(args.active_conditions),
        "deadline_within_14_days": bool(args.deadline_within_14_days),
    }

    session["workflow"]["activated_docs"] = split_list(route["activate_docs"])
    session["workflow"]["required_checklists"] = split_list(route["required_checklists"])
    session["workflow"]["cadence"] = route["default_cadence"]
    session["workflow"]["priority_profile"] = route["priority_profile"]
    session["workflow"]["escalation"] = route["escalation"]
    session["intake"]["primary_goal"] = args.primary_goal

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(session, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote session: {output_path}")
    print(f"Route selected: {route['route_id']} ({route['active_pathway']})")


if __name__ == "__main__":
    main()
