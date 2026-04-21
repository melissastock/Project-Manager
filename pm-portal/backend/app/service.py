from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess

from .config import DECISIONS_PATH, POLICY_PATH, REPOS_PATH, load_json
from .ingestion import collect_snapshot
from .models import BranchHealth, Project, ProjectReadiness, RecommendationDecision, StandupRun
from .recommendations import build_recommendations, decisions_for_recommendations, load_decisions, persist_decisions
from .scoring import compute_base_score, compute_dimensions, readiness_band


def _project_manager_root() -> Path:
    # pm-portal lives at Project Manager/pm-portal; parent is Project Manager root.
    return Path(__file__).resolve().parents[3]


def _run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True, text=True)


def _compute_branch_health(repo_path: Path, policy: dict) -> list[BranchHealth]:
    if not (repo_path / ".git").exists():
        return []

    refs = _run_git(repo_path, "for-each-ref", "--format=%(refname:short)", "refs/heads")
    if refs.returncode != 0:
        return []

    now = datetime.now(timezone.utc)
    items: list[BranchHealth] = []
    for branch in [b for b in refs.stdout.splitlines() if b]:
        head = _run_git(repo_path, "rev-parse", "--short", branch).stdout.strip()
        subject = _run_git(repo_path, "log", "-1", "--pretty=%s", branch).stdout.strip()
        commit_iso = _run_git(repo_path, "log", "-1", "--date=iso-strict", "--pretty=%cd", branch).stdout.strip()
        try:
            age_days = (now - datetime.fromisoformat(commit_iso).astimezone(timezone.utc)).days
        except Exception:
            age_days = 999

        up = _run_git(repo_path, "rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}")
        upstream = up.stdout.strip() if up.returncode == 0 else "none"

        ahead = behind = None
        if upstream != "none":
            lr = _run_git(repo_path, "rev-list", "--left-right", "--count", f"{upstream}...{branch}")
            if lr.returncode == 0 and lr.stdout.strip():
                left, right = lr.stdout.strip().split()
                behind, ahead = int(left), int(right)

        mb = _run_git(repo_path, "merge-base", branch, "origin/main")
        commits_since_main_base = None
        if mb.returncode == 0 and mb.stdout.strip():
            count = _run_git(repo_path, "rev-list", "--count", f"{mb.stdout.strip()}..{branch}")
            if count.returncode == 0 and count.stdout.strip():
                commits_since_main_base = int(count.stdout.strip())

        score = 100
        if ahead is not None and ahead > 0:
            score -= 5
        if behind is not None and behind > 0:
            score -= min(30, behind * 3)
        score -= min(20, age_days // 14)
        if commits_since_main_base is None:
            score -= 20
        score = max(0, score)
        band = readiness_band(score, policy["readiness_bands"])

        recommendations = []
        if upstream == "none":
            recommendations.append("Set upstream or archive branch")
        if behind is not None and behind > 0:
            recommendations.append("Reconcile behind commits before active use")
        if commits_since_main_base is None:
            recommendations.append("History split vs origin/main; avoid direct merge")
        if age_days > 30:
            recommendations.append("Refresh branch intent or archive")
        if not recommendations:
            recommendations.append("Continue as active canonical branch")

        items.append(
            BranchHealth(
                branch=branch,
                head=head,
                subject=subject,
                age_days=age_days,
                upstream=upstream,
                ahead=ahead,
                behind=behind,
                commits_since_main_base=commits_since_main_base,
                score=score,
                band=band,
                recommendation="; ".join(recommendations),
            )
        )
    items.sort(key=lambda b: b.score)
    return items


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
        branch_health = _compute_branch_health(pm_root / project.path, policy)
        recs = build_recommendations(entry, snapshot, band, score, int(policy.get("max_recommendations_per_project", 5)))
        decisions = decisions_for_recommendations([r.id for r in recs], decisions_cache)
        projects.append(ProjectReadiness(
            project=project,
            score=score,
            band=band,
            dimensions=dimensions,
            snapshot=snapshot,
            branch_health=branch_health,
            recommendations=recs,
            decisions=decisions,
        ))

    projects.sort(key=lambda p: p.score)
    return StandupRun(generated_at=datetime.now(timezone.utc), projects=projects)


def set_decision(recommendation_id: str, decision: RecommendationDecision) -> None:
    cache = load_decisions(DECISIONS_PATH)
    cache[recommendation_id] = decision.model_dump(mode="json")
    persist_decisions(DECISIONS_PATH, cache)
