from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .db import fetch_team_assignments, supabase_configured, upsert_team_assignment
from .models import TeamAssignment

ROLE_DEFS: dict[str, dict[str, Any]] = {
    "governance_steward": {
        "label": "Governance Steward",
        "raci": ["A", "R"],
        "workstream": "Policy and risk governance",
        "narrative": "Owns guardrails, policy changes, and risk acceptance decisions.",
    },
    "lane_operator": {
        "label": "Lane Operator",
        "raci": ["R"],
        "workstream": "Execution flow and lane prioritization",
        "narrative": "Keeps lane backlog healthy and sequences work for steady delivery.",
    },
    "release_packaging_owner": {
        "label": "Release and Packaging Owner",
        "raci": ["R"],
        "workstream": "Release readiness and package quality",
        "narrative": "Prepares release bundles and validates that artifacts are complete and send-ready.",
    },
    "compliance_reviewer": {
        "label": "Compliance Reviewer",
        "raci": ["A", "R"],
        "workstream": "Privacy, legal, and publication controls",
        "narrative": "Checks sensitive boundaries before any external release or disclosure event.",
    },
    "automation_maintainer": {
        "label": "Automation Maintainer",
        "raci": ["R", "C"],
        "workstream": "Tooling and CI reliability",
        "narrative": "Maintains scripts and automation so checks are consistent and observable.",
    },
}


def load_team_assignments(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if supabase_configured():
        try:
            rows = fetch_team_assignments()
            return {row["id"]: row for row in rows if row.get("id")}
        except Exception:
            pass
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_team_assignments(path: Path | None, assignments: dict[str, dict[str, Any]]) -> None:
    if supabase_configured():
        try:
            for value in assignments.values():
                upsert_team_assignment(value)
            return
        except Exception:
            pass
    if path is None:
        raise RuntimeError("Team assignment path is required when Supabase is not configured")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(assignments, indent=2, default=str), encoding="utf-8")


def list_project_team_assignments(project_entry: dict[str, Any], cache: dict[str, dict[str, Any]]) -> list[TeamAssignment]:
    project_name = str(project_entry.get("name", ""))
    now = datetime.now(timezone.utc)
    out: list[TeamAssignment] = []
    for role_key, role_cfg in ROLE_DEFS.items():
        assignment_id = f"{project_name.lower().replace(' ', '-')}-{role_key}"
        raw = cache.get(assignment_id, {})
        fallback_assignee = str(project_entry.get(role_key, "")).strip()
        out.append(
            TeamAssignment(
                id=assignment_id,
                project=project_name,
                role_key=role_key,
                role_label=role_cfg["label"],
                raci_tags=list(role_cfg["raci"]),
                assignee_name=str(raw.get("assignee_name") or fallback_assignee),
                assignee_type=str(raw.get("assignee_type") or "human"),
                workstream=str(raw.get("workstream") or role_cfg["workstream"]),
                narrative=str(raw.get("narrative") or role_cfg["narrative"]),
                status=str(raw.get("status") or "proposed"),
                approved_by=str(raw.get("approved_by") or ""),
                approved_at=raw.get("approved_at"),
                approval_note=str(raw.get("approval_note") or ""),
                source=str(raw.get("source") or "pm-portal"),
                created_at=raw.get("created_at") or now,
                updated_at=raw.get("updated_at") or now,
            )
        )
    out.sort(key=lambda item: item.role_label)
    return out
