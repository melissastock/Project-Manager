from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .db import fetch_recommendation_decisions, supabase_configured, upsert_recommendation_decision
from .models import Recommendation, RecommendationDecision, SignalSnapshot


def build_recommendations(project: dict, snapshot: SignalSnapshot, band: str, score: int, max_items: int) -> list[Recommendation]:
    recs: list[Recommendation] = []
    prefix = project["name"].lower().replace(" ", "-")
    intake_stage = str(project.get("intake_stage", "")).strip().lower()

    if intake_stage and not snapshot.is_git_repo:
        recs.append(Recommendation(
            id=f"{prefix}-runtime-access-validation",
            project=project["name"],
            action="Validate runtime repository access for this environment.",
            why_now="Project is onboarded in portfolio metadata, but this runtime cannot read .git state.",
            risk_if_delayed="Dashboards can incorrectly imply the project is not initialized.",
            alternatives_considered="Treat as not onboarded (rejected: metadata already records onboarding).",
            confidence="high",
        ))

    if snapshot.untracked_count > 0:
        recs.append(Recommendation(
            id=f"{prefix}-drift-containment",
            project=project["name"],
            action="Run drift containment and classify untracked artifacts.",
            why_now=f"{snapshot.untracked_count} untracked items reduce reproducibility confidence.",
            risk_if_delayed="Decision-critical data can diverge from auditable source-of-truth.",
            alternatives_considered="Commit all quickly (rejected: secret/noise risk); ignore drift (rejected: reproducibility risk).",
            confidence="high",
        ))
    if snapshot.staged_count > 0 or snapshot.unstaged_count > 0:
        recs.append(Recommendation(
            id=f"{prefix}-tracked-disposition",
            project=project["name"],
            action="Complete controlled tracked-change disposition before new scope.",
            why_now="Open tracked changes indicate unstable handoff state.",
            risk_if_delayed="Partially applied changes increase legal/operational ambiguity.",
            alternatives_considered="Continue feature work first (rejected for recovery governance).",
            confidence="high",
        ))
    if band in {"critical", "at-risk"}:
        recs.append(Recommendation(
            id=f"{prefix}-readiness-gate",
            project=project["name"],
            action="Run focused readiness gate and freeze non-critical feature work.",
            why_now=f"Current readiness is {band} ({score}/100).",
            risk_if_delayed="Execution velocity can hide unresolved delivery risks.",
            alternatives_considered="Proceed as-is (rejected: elevated risk posture).",
            confidence="medium",
        ))
    if not snapshot.backlog_files or not snapshot.sprint_files:
        recs.append(Recommendation(
            id=f"{prefix}-planning-artifacts",
            project=project["name"],
            action="Create/update backlog and sprint artifacts for explicit prioritization.",
            why_now="Standup intelligence quality depends on visible planning artifacts.",
            risk_if_delayed="Approval decisions become less evidence-based.",
            alternatives_considered="Ad hoc planning only (rejected: weak auditability).",
            confidence="medium",
        ))

    if not recs:
        recs.append(Recommendation(
            id=f"{prefix}-maintain-course",
            project=project["name"],
            action="Maintain execution course and review readiness in next standup.",
            why_now="No urgent risk indicators currently detected.",
            risk_if_delayed="Low immediate risk; continue monitoring.",
            alternatives_considered="Inject unscheduled scope (rejected to preserve sprint focus).",
            confidence="medium",
        ))
    return recs[:max_items]


def load_decisions(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if supabase_configured():
        try:
            rows = fetch_recommendation_decisions()
            return {
                row["recommendation_id"]: row
                for row in rows
                if row.get("recommendation_id")
            }
        except Exception:
            # Keep portal usable when Supabase is temporarily unavailable.
            pass
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_decisions(path: Path | None, decisions: dict[str, dict[str, Any]]) -> None:
    if supabase_configured():
        try:
            for value in decisions.values():
                upsert_recommendation_decision(value)
            return
        except Exception:
            # Fall through to local persistence as a resilience path.
            pass
    if path is None:
        raise RuntimeError("Decision path is required when Supabase is not configured")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(decisions, indent=2, default=str), encoding="utf-8")


def decisions_for_recommendations(rec_ids: list[str], cache: dict[str, dict]) -> list[RecommendationDecision]:
    out = []
    for rid in rec_ids:
        raw = cache.get(rid)
        if raw:
            out.append(RecommendationDecision(**raw))
        else:
            out.append(RecommendationDecision(
                recommendation_id=rid,
                state="pending",
                rationale="",
                owner="",
                due_date="",
                updated_at=datetime.now(timezone.utc),
            ))
    return out
