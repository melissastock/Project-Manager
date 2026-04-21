from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import Recommendation, RecommendationDecision, SignalSnapshot


def build_recommendations(project: dict, snapshot: SignalSnapshot, band: str, score: int, max_items: int) -> list[Recommendation]:
    recs: list[Recommendation] = []
    prefix = project["name"].lower().replace(" ", "-")

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


def load_decisions(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def persist_decisions(path: Path, decisions: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(decisions, indent=2), encoding="utf-8")


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
