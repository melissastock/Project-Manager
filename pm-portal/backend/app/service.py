from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess

from .agreements import (
    append_audit_event,
    get_agreement,
    list_change_orders_for_agreement,
    list_audit_events_for_agreement,
    list_messages_for_agreement,
    list_project_agreements,
    load_audit_events,
    load_agreement_messages,
    load_change_orders,
    load_client_agreements,
    persist_agreement_messages,
    persist_change_orders,
    persist_client_agreements,
)
from .config import (
    AGREEMENT_CHANGE_ORDERS_PATH,
    AGREEMENT_AUDIT_EVENTS_PATH,
    AGREEMENT_MESSAGES_PATH,
    CLIENT_AGREEMENTS_PATH,
    DECISIONS_PATH,
    LABOR_ESTIMATES_PATH,
    POLICY_PATH,
    REPOS_PATH,
    SECURE_VAULT_FILES_PATH,
    SECURE_VAULT_AUDIT_EVENTS_PATH,
    TEAM_ASSIGNMENTS_PATH,
    TICKETS_PATH,
    load_json,
)
from .db import insert_runtime_observations, supabase_configured
from .ingestion import collect_snapshot
from .labor_estimates import (
    list_project_labor_estimates,
    load_labor_estimates,
    persist_labor_estimates,
)
from .models import BranchHealth, Project, ProjectReadiness, RecommendationDecision, RuntimeObservation, RuntimeStatus, StandupRun, TeamAssignment
from .recommendations import build_recommendations, decisions_for_recommendations, load_decisions, persist_decisions
from .scoring import compute_base_score, compute_dimensions, readiness_band
from .team_assignments import list_project_team_assignments, load_team_assignments, persist_team_assignments
from .tickets import list_project_tickets, load_tickets, persist_tickets
from .secure_vault import (
    get_secure_vault_file,
    list_project_secure_vault_files,
    list_vault_audit_events_for_file,
    load_secure_vault_audit_events,
    load_secure_vault_files,
    persist_secure_vault_audit_events,
    persist_secure_vault_files,
)


def _project_manager_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True, text=True)


def _runtime_status(snapshot) -> tuple[RuntimeStatus, str]:
    if not snapshot.exists:
        return "path-missing", "Project path is registered but missing in this runtime."
    if not snapshot.is_git_repo:
        return "git-unavailable", "Project path exists but .git metadata is unavailable in this runtime."
    if snapshot.branch == "unborn":
        return "unborn", "Repository exists but has no commits yet."
    return "ok", "Runtime can read git metadata."


def build_standup_view() -> StandupRun:
    repos_cfg = load_json(REPOS_PATH)
    policy = load_json(POLICY_PATH)
    decisions_cache = load_decisions(DECISIONS_PATH)
    tickets_cache = load_tickets(TICKETS_PATH)
    team_cache = load_team_assignments(TEAM_ASSIGNMENTS_PATH)
    agreements_cache = load_client_agreements(CLIENT_AGREEMENTS_PATH)
    labor_cache = load_labor_estimates(LABOR_ESTIMATES_PATH)
    vault_cache = load_secure_vault_files(SECURE_VAULT_FILES_PATH)
    pm_root = _project_manager_root()

    projects: list[ProjectReadiness] = []
    observations: list[RuntimeObservation] = []
    for entry in repos_cfg["managed_repositories"]:
        project = Project(**{k: entry.get(k, "") for k in Project.model_fields.keys()})
        snapshot = collect_snapshot(pm_root, project)
        runtime_status, runtime_note = _runtime_status(snapshot)
        score = compute_base_score(snapshot, entry, policy)
        band = readiness_band(score, policy["readiness_bands"])
        dimensions = compute_dimensions(score, snapshot, policy)
        recs = build_recommendations(entry, snapshot, band, score, int(policy.get("max_recommendations_per_project", 5)))
        decisions = decisions_for_recommendations([r.id for r in recs], decisions_cache)
        projects.append(ProjectReadiness(
            project=project,
            registry_status="registered",
            runtime_status=runtime_status,
            runtime_note=runtime_note,
            score=score,
            band=band,
            dimensions=dimensions,
            snapshot=snapshot,
            branch_health=[],
            recommendations=recs,
            decisions=decisions,
            tickets=list_project_tickets(project.name, tickets_cache),
            team_assignments=list_project_team_assignments(entry, team_cache),
            client_agreements=list_project_agreements(project.name, agreements_cache),
            labor_estimates=list_project_labor_estimates(project.name, labor_cache),
            secure_vault_files=list_project_secure_vault_files(project.name, vault_cache),
        ))
        observations.append(
            RuntimeObservation(
                project_name=project.name,
                project_path=project.path,
                intake_stage=project.intake_stage,
                registry_status="registered",
                runtime_status=runtime_status,
                runtime_note=runtime_note,
                exists=snapshot.exists,
                is_git_repo=snapshot.is_git_repo,
                branch=snapshot.branch,
                head=snapshot.head,
                summary=snapshot.summary,
                observed_at=datetime.now(timezone.utc),
            )
        )

    if supabase_configured():
        try:
            insert_runtime_observations([row.model_dump(mode="json") for row in observations])
        except Exception:
            # Keep standup usable even when Supabase write fails.
            pass

    projects.sort(key=lambda p: p.score)
    return StandupRun(generated_at=datetime.now(timezone.utc), projects=projects)


def set_decision(recommendation_id: str, decision: RecommendationDecision) -> None:
    cache = load_decisions(DECISIONS_PATH)
    payload = decision.model_dump(mode="json")
    payload["recommendation_id"] = recommendation_id
    cache[recommendation_id] = payload
    persist_decisions(DECISIONS_PATH, cache)


def upsert_ticket(ticket_payload: dict) -> None:
    cache = load_tickets(TICKETS_PATH)
    cache[ticket_payload["id"]] = ticket_payload
    persist_tickets(TICKETS_PATH, cache)


def get_ticket(ticket_id: str) -> dict | None:
    cache = load_tickets(TICKETS_PATH)
    return cache.get(ticket_id)


def list_team_assignments(project_name: str) -> list[TeamAssignment]:
    repos_cfg = load_json(REPOS_PATH)
    team_cache = load_team_assignments(TEAM_ASSIGNMENTS_PATH)
    project_entry = next(
        (entry for entry in repos_cfg["managed_repositories"] if str(entry.get("name", "")).lower() == project_name.lower()),
        None,
    )
    if project_entry is None:
        return []
    return list_project_team_assignments(project_entry, team_cache)


def get_team_assignment(project_name: str, role_key: str) -> dict | None:
    for assignment in list_team_assignments(project_name):
        if assignment.role_key == role_key:
            return assignment.model_dump(mode="json")
    return None


def upsert_team_assignment_payload(payload: dict) -> dict:
    cache = load_team_assignments(TEAM_ASSIGNMENTS_PATH)
    cache[payload["id"]] = payload
    persist_team_assignments(TEAM_ASSIGNMENTS_PATH, cache)
    return payload


def list_client_agreements(project_name: str) -> list[dict]:
    cache = load_client_agreements(CLIENT_AGREEMENTS_PATH)
    return [item.model_dump(mode="json") for item in list_project_agreements(project_name, cache)]


def get_client_agreement(agreement_id: str) -> dict | None:
    cache = load_client_agreements(CLIENT_AGREEMENTS_PATH)
    return get_agreement(agreement_id, cache)


def upsert_client_agreement_payload(payload: dict) -> dict:
    cache = load_client_agreements(CLIENT_AGREEMENTS_PATH)
    cache[payload["id"]] = payload
    persist_client_agreements(CLIENT_AGREEMENTS_PATH, cache)
    return payload


def list_agreement_messages(agreement_id: str) -> list[dict]:
    cache = load_agreement_messages(AGREEMENT_MESSAGES_PATH)
    return [item.model_dump(mode="json") for item in list_messages_for_agreement(agreement_id, cache)]


def upsert_agreement_message_payload(payload: dict) -> dict:
    cache = load_agreement_messages(AGREEMENT_MESSAGES_PATH)
    cache[payload["id"]] = payload
    persist_agreement_messages(AGREEMENT_MESSAGES_PATH, cache)
    return payload


def list_agreement_change_orders(agreement_id: str) -> list[dict]:
    cache = load_change_orders(AGREEMENT_CHANGE_ORDERS_PATH)
    return [item.model_dump(mode="json") for item in list_change_orders_for_agreement(agreement_id, cache)]


def upsert_change_order_payload(payload: dict) -> dict:
    cache = load_change_orders(AGREEMENT_CHANGE_ORDERS_PATH)
    cache[payload["id"]] = payload
    persist_change_orders(AGREEMENT_CHANGE_ORDERS_PATH, cache)
    return payload


def create_agreement_audit_event(payload: dict) -> dict:
    return append_audit_event(AGREEMENT_AUDIT_EVENTS_PATH, payload)


def list_agreement_audit_events(agreement_id: str) -> list[dict]:
    cache = load_audit_events(AGREEMENT_AUDIT_EVENTS_PATH)
    return list_audit_events_for_agreement(agreement_id, cache)


def list_labor_estimates(project_name: str) -> list[dict]:
    cache = load_labor_estimates(LABOR_ESTIMATES_PATH)
    return [item.model_dump(mode="json") for item in list_project_labor_estimates(project_name, cache)]


def get_labor_estimate(estimate_id: str) -> dict | None:
    cache = load_labor_estimates(LABOR_ESTIMATES_PATH)
    return cache.get(estimate_id)


def upsert_labor_estimate_payload(payload: dict) -> dict:
    cache = load_labor_estimates(LABOR_ESTIMATES_PATH)
    cache[payload["id"]] = payload
    persist_labor_estimates(LABOR_ESTIMATES_PATH, cache)
    return payload


def list_secure_vault_files(project_name: str) -> list[dict]:
    cache = load_secure_vault_files(SECURE_VAULT_FILES_PATH)
    return [item.model_dump(mode="json") for item in list_project_secure_vault_files(project_name, cache)]


def upsert_secure_vault_file_payload(payload: dict) -> dict:
    cache = load_secure_vault_files(SECURE_VAULT_FILES_PATH)
    cache[payload["id"]] = payload
    persist_secure_vault_files(SECURE_VAULT_FILES_PATH, cache)
    return payload


def get_secure_vault_file_payload(file_id: str) -> dict | None:
    cache = load_secure_vault_files(SECURE_VAULT_FILES_PATH)
    return get_secure_vault_file(file_id, cache)


def append_secure_vault_audit_event(payload: dict) -> dict:
    cache = load_secure_vault_audit_events(SECURE_VAULT_AUDIT_EVENTS_PATH)
    cache[payload["id"]] = payload
    persist_secure_vault_audit_events(SECURE_VAULT_AUDIT_EVENTS_PATH, cache)
    return payload


def list_secure_vault_audit_events(file_id: str) -> list[dict]:
    cache = load_secure_vault_audit_events(SECURE_VAULT_AUDIT_EVENTS_PATH)
    return list_vault_audit_events_for_file(file_id, cache)
