from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .db import ping_supabase, supabase_configured
from .models import ProjectTicket, RecommendationDecision, TeamAssignment
from .service import (
    build_standup_view,
    get_team_assignment,
    get_ticket,
    list_team_assignments,
    set_decision,
    upsert_team_assignment_payload,
    upsert_ticket,
)

app = FastAPI(title="PM Portal API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DecisionUpdate(BaseModel):
    state: str
    rationale: str = ""
    owner: str = ""
    due_date: str = ""


class TicketCreate(BaseModel):
    project: str
    title: str
    description: str = ""
    state: str = "new"
    priority: str = "P2"
    owner: str = ""
    lane: str = ""
    scope_label: str = "pm-portal-only"
    due_date: str = ""
    source: str = "pm-portal"


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: str | None = None
    priority: str | None = None
    owner: str | None = None
    lane: str | None = None
    scope_label: str | None = None
    due_date: str | None = None


class TeamAssignmentUpdate(BaseModel):
    assignee_name: str | None = None
    assignee_type: str | None = None
    workstream: str | None = None
    narrative: str | None = None
    status: str | None = None
    approval_note: str | None = None


class TeamApprovalRequest(BaseModel):
    approved_by: str
    approval_note: str = ""


def _project_manager_root() -> Path:
    return Path(__file__).resolve().parents[3]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/supabase")
def health_supabase() -> dict[str, str]:
    if not supabase_configured():
        return {
            "status": "skipped",
            "detail": "SUPABASE_URL / SUPABASE_ANON_KEY not set; decisions use local JSON.",
        }
    try:
        ping_supabase()
        return {"status": "ok"}
    except Exception as exc:  # noqa: BLE001 — surface connectivity errors to operators
        return {"status": "error", "detail": str(exc)}


@app.get("/api/standup")
def get_standup() -> dict:
    return build_standup_view().model_dump(mode="json")


@app.get("/api/governance/latest")
def get_latest_governance_summary() -> dict:
    summary_path = _project_manager_root() / "docs" / "session-artifacts" / "governance" / "last-governance-run.json"
    if not summary_path.exists():
        return {
            "available": False,
            "detail": "No governance summary found yet. Run scripts/run_governance_profile.sh first.",
        }
    return {
        "available": True,
        "summary": json.loads(summary_path.read_text(encoding="utf-8")),
    }


@app.get("/api/projects/{project_name}")
def get_project(project_name: str) -> dict:
    run = build_standup_view()
    for project in run.projects:
        if project.project.name.lower() == project_name.lower():
            return project.model_dump(mode="json")
    raise HTTPException(status_code=404, detail="Project not found")


@app.post("/api/recommendations/{recommendation_id}/decision")
def update_decision(recommendation_id: str, payload: DecisionUpdate) -> dict:
    if payload.state not in {"approved", "rejected", "defer", "pending"}:
        raise HTTPException(status_code=400, detail="Invalid decision state")
    decision = RecommendationDecision(
        recommendation_id=recommendation_id,
        state=payload.state,
        rationale=payload.rationale,
        owner=payload.owner,
        due_date=payload.due_date,
        updated_at=datetime.now(timezone.utc),
    )
    set_decision(recommendation_id, decision)
    return {"ok": True, "decision": decision.model_dump(mode="json")}


@app.get("/api/tickets")
def list_tickets(project: str | None = None, state: str | None = None) -> dict:
    run = build_standup_view()
    tickets: list[dict] = []
    for item in run.projects:
        tickets.extend(t.model_dump(mode="json") for t in item.tickets)

    if project:
        tickets = [t for t in tickets if str(t.get("project", "")).lower() == project.lower()]
    if state:
        tickets = [t for t in tickets if str(t.get("state", "")).lower() == state.lower()]

    return {"tickets": tickets, "count": len(tickets)}


@app.post("/api/tickets")
def create_ticket(payload: TicketCreate) -> dict:
    now = datetime.now(timezone.utc)
    ticket = ProjectTicket(
        id=f"tkt-{uuid4().hex[:12]}",
        project=payload.project,
        title=payload.title,
        description=payload.description,
        state=payload.state,  # validated by model type
        priority=payload.priority,
        owner=payload.owner,
        lane=payload.lane,
        scope_label=payload.scope_label,
        due_date=payload.due_date,
        source=payload.source,
        created_at=now,
        updated_at=now,
    )
    upsert_ticket(ticket.model_dump(mode="json"))
    return {"ok": True, "ticket": ticket.model_dump(mode="json")}


@app.patch("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: str, payload: TicketUpdate) -> dict:
    current = get_ticket(ticket_id)
    if not current:
        raise HTTPException(status_code=404, detail="Ticket not found")

    merged = dict(current)
    for key, value in payload.model_dump(exclude_none=True).items():
        merged[key] = value
    merged["updated_at"] = datetime.now(timezone.utc).isoformat()

    ticket = ProjectTicket(**merged)
    upsert_ticket(ticket.model_dump(mode="json"))
    return {"ok": True, "ticket": ticket.model_dump(mode="json")}


@app.get("/api/team-assignments")
def get_team_assignments(project: str) -> dict:
    assignments = list_team_assignments(project)
    return {"project": project, "team_assignments": [a.model_dump(mode="json") for a in assignments]}


@app.patch("/api/team-assignments/{project_name}/{role_key}")
def update_team_assignment(project_name: str, role_key: str, payload: TeamAssignmentUpdate) -> dict:
    current = get_team_assignment(project_name, role_key)
    if not current:
        raise HTTPException(status_code=404, detail="Team assignment not found")
    merged = dict(current)
    for key, value in payload.model_dump(exclude_none=True).items():
        merged[key] = value
    merged["updated_at"] = datetime.now(timezone.utc).isoformat()
    assignment = TeamAssignment(**merged)
    saved = upsert_team_assignment_payload(assignment.model_dump(mode="json"))
    return {"ok": True, "team_assignment": saved}


@app.post("/api/team-assignments/{project_name}/approve")
def approve_team_assignments(project_name: str, payload: TeamApprovalRequest) -> dict:
    assignments = list_team_assignments(project_name)
    if not assignments:
        raise HTTPException(status_code=404, detail="Project team assignments not found")
    now = datetime.now(timezone.utc)
    updated: list[dict] = []
    for item in assignments:
        merged = item.model_dump(mode="json")
        merged["status"] = "approved"
        merged["approved_by"] = payload.approved_by
        merged["approved_at"] = now.isoformat()
        if payload.approval_note:
            merged["approval_note"] = payload.approval_note
        merged["updated_at"] = now.isoformat()
        assignment = TeamAssignment(**merged)
        saved = upsert_team_assignment_payload(assignment.model_dump(mode="json"))
        updated.append(saved)
    return {"ok": True, "project": project_name, "count": len(updated), "team_assignments": updated}
