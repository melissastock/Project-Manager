from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .config import DECISIONS_PATH, POLICY_PATH, REPOS_PATH, load_json
from .ingestion import collect_snapshot
from .models import Project, ProjectReadiness, RecommendationDecision, StandupRun
from .recommendations import build_recommendations, decisions_for_recommendations, load_decisions, persist_decisions
from .scoring import compute_base_score, compute_dimensions, readiness_band


def _project_manager_root() -> Path:
    # pm-portal lives at Project Manager/pm-portal; parent is Project Manager root.
    return Path(__file__).resolve().parents[3]


def build_standup_view() -> StandupRun:
    repos_cfg = load_json(REPOS_PATH)
    policy = load_json(POLICY_PATH)
    decisions_cache = load_decisions(DECISIONS_PATH)
    pm_root = _project_manager_root()

    projects: list[ProjectReadiness] = []
    for entry in repos_cfg["managed_repositories"]:
        project = Project(**{k: entry.get(k, "") for k in Project.model_fields.keys()})
        snapshot = collect_snapshot(pm_root, project)
        score = compute_base_score(snapshot, entry, policy)
        band = readiness_band(score, policy["readiness_bands"])
        dimensions = compute_dimensions(score, snapshot, policy)
        recs = build_recommendations(entry, snapshot, band, score, int(policy.get("max_recommendations_per_project", 5)))
        decisions = decisions_for_recommendations([r.id for r in recs], decisions_cache)
        projects.append(ProjectReadiness(
            project=project,
            score=score,
            band=band,
            dimensions=dimensions,
            snapshot=snapshot,
            recommendations=recs,
            decisions=decisions,
        ))

    projects.sort(key=lambda p: p.score)
    return StandupRun(generated_at=datetime.now(timezone.utc), projects=projects)


def set_decision(recommendation_id: str, decision: RecommendationDecision) -> None:
    cache = load_decisions(DECISIONS_PATH)
    cache[recommendation_id] = decision.model_dump(mode="json")
    persist_decisions(DECISIONS_PATH, cache)
