from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .db import ping_supabase, supabase_configured
from .db import (
    create_secure_vault_signed_download_url,
    create_secure_vault_signed_upload_url,
    download_secure_vault_file_bytes,
    sha256_hex,
    supabase_storage_configured,
)
from .models import ProjectTicket, RecommendationDecision, TeamAssignment
from .config import SECURE_VAULT_DRIVE_CONNECTIONS_PATH
from .service import (
    build_standup_view,
    create_agreement_audit_event,
    get_client_agreement,
    get_team_assignment,
    get_ticket,
    get_secure_vault_file_payload,
    list_agreement_change_orders,
    list_agreement_audit_events,
    list_agreement_messages,
    list_client_agreements,
    list_labor_estimates,
    list_secure_vault_files,
    list_secure_vault_audit_events,
    list_team_assignments,
    set_decision,
    upsert_agreement_message_payload,
    upsert_change_order_payload,
    upsert_client_agreement_payload,
    upsert_labor_estimate_payload,
    upsert_secure_vault_file_payload,
    append_secure_vault_audit_event,
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


class AgreementDeliverableInput(BaseModel):
    id: str | None = None
    title: str
    description: str = ""
    due_date: str = ""
    acceptance_criteria: str = ""


class IntakeResponseInput(BaseModel):
    # Client-owned intake fields
    client_goals: str = ""
    success_criteria: str = ""
    communication_preferences: str = ""
    primary_contact: str = ""
    required_assets: list[str] = []

    # Business-owner-owned intake fields
    constraints: str = ""
    dependencies: str = ""
    budget_range_usd: str = ""
    scope_boundaries: str = ""
    compliance_requirements: str = ""
    approval_authority: str = ""
    risk_assumptions: str = ""

    completed: bool = False
    completed_at: str | None = None


class ClientAgreementCreate(BaseModel):
    project: str
    client_name: str
    package_name: str = ""
    product_brief: str = ""
    scope_definition: str = ""
    deliverables_summary: str = ""
    pricing_model: Literal["fixed", "package", "retainer", "mixed"] = "fixed"
    price_terms_json: dict = {}
    owner_role: str = "business_owner"
    neuro_worker_type: str = "unspecified"
    deliverables: list[AgreementDeliverableInput] = []
    intake: IntakeResponseInput = IntakeResponseInput()


class ClientAgreementUpdate(BaseModel):
    package_name: str | None = None
    product_brief: str | None = None
    scope_definition: str | None = None
    deliverables_summary: str | None = None
    pricing_model: Literal["fixed", "package", "retainer", "mixed"] | None = None
    price_terms_json: dict | None = None
    agreement_status: Literal["draft", "under_review", "ready_for_signature", "active", "locked", "amended"] | None = None
    owner_role: str | None = None
    neuro_worker_type: str | None = None
    deliverables: list[AgreementDeliverableInput] | None = None
    intake: IntakeResponseInput | None = None


class IntakeCompleteRequest(BaseModel):
    completed_by: str
    actor_role: str
    lock_reason: str = "intake-complete"


class AgreementMessageCreate(BaseModel):
    author_name: str
    author_role: str = "client"
    message: str
    visibility: Literal["client_and_team", "internal_only"] = "client_and_team"


class AgreementChangeOrderCreate(BaseModel):
    requested_by: str
    requested_scope_delta: str
    requested_price_delta: str = ""
    requested_timeline_delta: str = ""


class AgreementChangeOrderDecision(BaseModel):
    approver: str
    actor_role: str
    status: Literal["approved", "rejected", "implemented"]
    decision_note: str = ""


class LaborEstimateModuleInput(BaseModel):
    module_key: Literal["strategy", "development", "operationalization", "governance", "marketing", "gtm"]
    estimated_hours: float
    notes: str = ""
    subcomponents: list[str] = []


class LaborEstimateCreate(BaseModel):
    project: str
    hourly_rate_usd: float = 150.0
    confidence: Literal["low", "medium", "high"] = "medium"
    assumptions: list[str] = []
    created_by: str = ""
    modules: list[LaborEstimateModuleInput]
    non_labor_costs: list[dict] = []


class SecureVaultFileCreate(BaseModel):
    project: str
    client_name: str = ""
    file_name: str
    storage_uri: str = ""
    data_class: Literal["ip_invention", "financial", "legal", "medical", "regulated", "other"] = "other"
    sensitivity_level: Literal["restricted", "highly_restricted"] = "restricted"
    encryption_status: Literal["encrypted_at_rest", "encrypted_at_rest_and_transport"] = "encrypted_at_rest_and_transport"
    retention_policy: str = "retain-until-client-request-or-policy-expiry"
    access_roles: list[str] = []
    checksum_sha256: str = ""
    uploaded_by: str = ""
    notes: str = ""


class SecureVaultSignedUrlRequest(BaseModel):
    actor_name: str
    actor_role: str
    expires_in_seconds: int = 900


class SecureVaultChecksumVerifyRequest(BaseModel):
    actor_name: str
    actor_role: str
    expected_checksum_sha256: str


class SecureVaultDriveConnectRequest(BaseModel):
    project: str
    connected_by: str
    actor_role: str = "business_owner"
    drive_account_email: str
    drive_folder_id: str
    notes: str = ""


class SecureVaultDriveDisconnectRequest(BaseModel):
    project: str
    disconnected_by: str
    actor_role: str = "business_owner"
    reason: str = ""


def _project_manager_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_deliverables(payload: list[AgreementDeliverableInput] | None) -> list[dict]:
    if payload is None:
        return []
    result: list[dict] = []
    for item in payload:
        result.append(
            {
                "id": item.id or f"deliv-{uuid4().hex[:8]}",
                "title": item.title,
                "description": item.description,
                "due_date": item.due_date,
                "acceptance_criteria": item.acceptance_criteria,
            }
        )
    return result


def _intake_complete(raw: dict) -> bool:
    intake = raw.get("intake") or {}
    return bool(intake.get("completed"))


def _ensure_intake_ready_for_lock(raw: dict) -> None:
    intake = raw.get("intake") or {}
    required_client = [
        ("client_goals", "client_goals must be provided."),
        ("success_criteria", "success_criteria must be provided."),
        ("primary_contact", "primary_contact must be provided."),
        ("communication_preferences", "communication_preferences must be provided."),
    ]
    required_business_owner = [
        ("scope_boundaries", "scope_boundaries must be provided by business owner."),
        ("budget_range_usd", "budget_range_usd must be provided by business owner."),
        ("compliance_requirements", "compliance_requirements must be provided by business owner."),
        ("approval_authority", "approval_authority must be provided by business owner."),
        ("risk_assumptions", "risk_assumptions must be provided by business owner."),
    ]
    for key, message in required_client + required_business_owner:
        if not str(intake.get(key, "")).strip():
            raise HTTPException(status_code=400, detail=message)
    if not intake.get("completed"):
        raise HTTPException(status_code=400, detail="Intake must be completed before lock.")


def _require_change_order_for_locked_update(raw: dict, updates: dict) -> None:
    protected_fields = {
        "package_name",
        "product_brief",
        "scope_definition",
        "deliverables_summary",
        "pricing_model",
        "price_terms_json",
        "deliverables",
    }
    if not raw.get("is_locked"):
        return
    changing = protected_fields.intersection(set(updates.keys()))
    if changing:
        names = ", ".join(sorted(changing))
        raise HTTPException(
            status_code=409,
            detail=f"Agreement is locked. Use change order flow to modify: {names}",
        )


def _require_owner_role(agreement: dict, caller_role: str, allowed_roles: set[str]) -> None:
    role = (caller_role or "").strip()
    if not role:
        raise HTTPException(status_code=400, detail="actor_role is required for this action")
    if role not in allowed_roles:
        raise HTTPException(status_code=403, detail=f"Role {role} cannot perform this action")
    owner_role = str(agreement.get("owner_role", "")).strip()
    if owner_role and role != owner_role and role != "portfolio_owner":
        raise HTTPException(status_code=403, detail="Action role does not match agreement owner role")


def _with_costs(modules: list[LaborEstimateModuleInput], hourly_rate_usd: float) -> tuple[list[dict], float, float]:
    out: list[dict] = []
    total_hours = 0.0
    total_cost = 0.0
    for module in modules:
        hours = float(module.estimated_hours or 0.0)
        cost = round(hours * float(hourly_rate_usd), 2)
        total_hours += hours
        total_cost += cost
        out.append(
            {
                "module_key": module.module_key,
                "estimated_hours": hours,
                "estimated_cost_usd": cost,
                "notes": module.notes,
                "subcomponents": module.subcomponents,
            }
        )
    return out, round(total_hours, 2), round(total_cost, 2)


def _secure_vault_bucket() -> str:
    import os

    return os.getenv("SUPABASE_SECURE_VAULT_BUCKET", "secure-client-vault").strip() or "secure-client-vault"


def _load_drive_connections() -> dict:
    path = SECURE_VAULT_DRIVE_CONNECTIONS_PATH
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _persist_drive_connections(payload: dict) -> None:
    path = SECURE_VAULT_DRIVE_CONNECTIONS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in (value or "").strip())
    compact = "-".join(part for part in cleaned.split("-") if part)
    return compact or "unknown"


def _build_secure_vault_path(project: str, client_name: str, data_class: str, file_name: str, file_id: str) -> str:
    project_slug = _slug(project)
    client_slug = _slug(client_name)
    class_slug = _slug(data_class)
    safe_name = _slug(file_name.rsplit(".", 1)[0])
    extension = ""
    if "." in file_name:
        extension = "." + file_name.rsplit(".", 1)[1].lower()
    return f"{project_slug}/{client_slug}/{class_slug}/{file_id}/{safe_name}{extension}"


def _require_vault_role(file_row: dict, actor_role: str) -> None:
    role = (actor_role or "").strip()
    if not role:
        raise HTTPException(status_code=400, detail="actor_role is required")
    allowed = [str(x).strip() for x in (file_row.get("access_roles") or []) if str(x).strip()]
    if allowed and role not in allowed:
        raise HTTPException(status_code=403, detail=f"Role {role} is not allowed for this vault file")


def _require_drive_connection_role(actor_role: str) -> None:
    allowed_roles = {"business_owner", "portfolio_owner", "technical_owner"}
    role = (actor_role or "").strip()
    if role not in allowed_roles:
        raise HTTPException(status_code=403, detail=f"Role {role} cannot manage Drive connections")


def _summarize_non_labor(non_labor_costs: list[dict]) -> tuple[list[dict], float, float, float]:
    normalized: list[dict] = []
    one_time = 0.0
    monthly = 0.0
    variable = 0.0
    for item in non_labor_costs:
        one = float(item.get("one_time_usd", 0.0) or 0.0)
        mon = float(item.get("monthly_recurring_usd", 0.0) or 0.0)
        var = float(item.get("usage_variable_monthly_usd", 0.0) or 0.0)
        one_time += one
        monthly += mon
        variable += var
        normalized.append(
            {
                "category": item.get("category", "other"),
                "one_time_usd": round(one, 2),
                "monthly_recurring_usd": round(mon, 2),
                "usage_variable_monthly_usd": round(var, 2),
                "notes": item.get("notes", ""),
            }
        )
    return normalized, round(one_time, 2), round(monthly, 2), round(variable, 2)


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


@app.get("/api/client-agreements")
def get_client_agreements(project: str) -> dict:
    agreements = list_client_agreements(project)
    return {"project": project, "client_agreements": agreements}


@app.post("/api/client-agreements")
def create_client_agreement(payload: ClientAgreementCreate) -> dict:
    now = datetime.now(timezone.utc)
    agreement = {
        "id": f"agr-{uuid4().hex[:12]}",
        "project": payload.project,
        "client_name": payload.client_name,
        "package_name": payload.package_name,
        "product_brief": payload.product_brief,
        "scope_definition": payload.scope_definition,
        "deliverables_summary": payload.deliverables_summary,
        "pricing_model": payload.pricing_model,
        "price_terms_json": payload.price_terms_json,
        "agreement_status": "draft",
        "is_locked": False,
        "locked_at": None,
        "locked_by": "",
        "lock_reason": "",
        "owner_role": payload.owner_role,
        "neuro_worker_type": payload.neuro_worker_type,
        "intake": payload.intake.model_dump(mode="json"),
        "deliverables": _build_deliverables(payload.deliverables),
        "source": "pm-portal",
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }
    saved = upsert_client_agreement_payload(agreement)
    return {"ok": True, "agreement": saved}


@app.patch("/api/client-agreements/{agreement_id}")
def update_client_agreement(agreement_id: str, payload: ClientAgreementUpdate) -> dict:
    current = get_client_agreement(agreement_id)
    if not current:
        raise HTTPException(status_code=404, detail="Client agreement not found")
    updates = payload.model_dump(exclude_none=True)
    _require_change_order_for_locked_update(current, updates)
    merged = dict(current)
    if "deliverables" in updates:
        merged["deliverables"] = _build_deliverables(payload.deliverables)
        del updates["deliverables"]
    if "intake" in updates:
        merged["intake"] = payload.intake.model_dump(mode="json")
        del updates["intake"]
    for key, value in updates.items():
        merged[key] = value
    merged["updated_at"] = _now_iso()
    saved = upsert_client_agreement_payload(merged)
    create_agreement_audit_event(
        {
            "id": f"audit-{uuid4().hex[:12]}",
            "agreement_id": agreement_id,
            "project": saved["project"],
            "event_type": "agreement_updated",
            "actor": "team",
            "actor_role": "team",
            "details": {"updated_fields": sorted(list(updates.keys()))},
            "created_at": _now_iso(),
            "data_class": "CONFIDENTIAL",
        }
    )
    return {"ok": True, "agreement": saved}


@app.post("/api/client-agreements/{agreement_id}/intake-complete")
def complete_intake_and_lock(agreement_id: str, payload: IntakeCompleteRequest) -> dict:
    current = get_client_agreement(agreement_id)
    if not current:
        raise HTTPException(status_code=404, detail="Client agreement not found")
    _require_owner_role(current, payload.actor_role, {"business_owner", "portfolio_owner"})
    merged = dict(current)
    intake = dict(merged.get("intake") or {})
    intake["completed"] = True
    intake["completed_at"] = _now_iso()
    merged["intake"] = intake
    _ensure_intake_ready_for_lock(merged)
    merged["is_locked"] = True
    merged["agreement_status"] = "locked"
    merged["locked_at"] = _now_iso()
    merged["locked_by"] = payload.completed_by
    merged["lock_reason"] = payload.lock_reason
    merged["updated_at"] = _now_iso()
    saved = upsert_client_agreement_payload(merged)
    create_agreement_audit_event(
        {
            "id": f"audit-{uuid4().hex[:12]}",
            "agreement_id": agreement_id,
            "project": saved["project"],
            "event_type": "agreement_locked",
            "actor": payload.completed_by,
            "actor_role": payload.actor_role,
            "details": {"lock_reason": payload.lock_reason},
            "created_at": _now_iso(),
            "data_class": "CONFIDENTIAL",
        }
    )
    return {"ok": True, "agreement": saved}


@app.get("/api/client-agreements/{agreement_id}/messages")
def get_agreement_messages(agreement_id: str) -> dict:
    current = get_client_agreement(agreement_id)
    if not current:
        raise HTTPException(status_code=404, detail="Client agreement not found")
    return {"agreement_id": agreement_id, "messages": list_agreement_messages(agreement_id)}


@app.post("/api/client-agreements/{agreement_id}/messages")
def create_agreement_message(agreement_id: str, payload: AgreementMessageCreate) -> dict:
    current = get_client_agreement(agreement_id)
    if not current:
        raise HTTPException(status_code=404, detail="Client agreement not found")
    message = {
        "id": f"msg-{uuid4().hex[:12]}",
        "agreement_id": agreement_id,
        "project": current["project"],
        "author_name": payload.author_name,
        "author_role": payload.author_role,
        "message": payload.message,
        "visibility": payload.visibility,
        "created_at": _now_iso(),
    }
    saved = upsert_agreement_message_payload(message)
    create_agreement_audit_event(
        {
            "id": f"audit-{uuid4().hex[:12]}",
            "agreement_id": agreement_id,
            "project": current["project"],
            "event_type": "agreement_message_created",
            "actor": payload.author_name,
            "actor_role": payload.author_role,
            "details": {"visibility": payload.visibility},
            "created_at": _now_iso(),
            "data_class": "CONFIDENTIAL",
        }
    )
    return {"ok": True, "message": saved}


@app.get("/api/client-agreements/{agreement_id}/change-orders")
def get_change_orders(agreement_id: str) -> dict:
    current = get_client_agreement(agreement_id)
    if not current:
        raise HTTPException(status_code=404, detail="Client agreement not found")
    return {"agreement_id": agreement_id, "change_orders": list_agreement_change_orders(agreement_id)}


@app.post("/api/client-agreements/{agreement_id}/change-orders")
def create_change_order(agreement_id: str, payload: AgreementChangeOrderCreate) -> dict:
    current = get_client_agreement(agreement_id)
    if not current:
        raise HTTPException(status_code=404, detail="Client agreement not found")
    if not current.get("is_locked"):
        raise HTTPException(status_code=400, detail="Change orders are only required after agreement lock.")
    now = _now_iso()
    change_order = {
        "id": f"co-{uuid4().hex[:12]}",
        "agreement_id": agreement_id,
        "project": current["project"],
        "requested_by": payload.requested_by,
        "requested_scope_delta": payload.requested_scope_delta,
        "requested_price_delta": payload.requested_price_delta,
        "requested_timeline_delta": payload.requested_timeline_delta,
        "status": "requested",
        "approver": "",
        "decision_note": "",
        "created_at": now,
        "updated_at": now,
    }
    saved = upsert_change_order_payload(change_order)
    create_agreement_audit_event(
        {
            "id": f"audit-{uuid4().hex[:12]}",
            "agreement_id": agreement_id,
            "project": current["project"],
            "event_type": "change_order_requested",
            "actor": payload.requested_by,
            "actor_role": "requestor",
            "details": {"scope_delta": payload.requested_scope_delta},
            "created_at": _now_iso(),
            "data_class": "CONFIDENTIAL",
        }
    )
    return {"ok": True, "change_order": saved}


@app.post("/api/client-agreements/{agreement_id}/change-orders/{change_order_id}/decision")
def decide_change_order(
    agreement_id: str, change_order_id: str, payload: AgreementChangeOrderDecision
) -> dict:
    current = get_client_agreement(agreement_id)
    if not current:
        raise HTTPException(status_code=404, detail="Client agreement not found")
    _require_owner_role(current, payload.actor_role, {"business_owner", "portfolio_owner"})
    existing = next(
        (co for co in list_agreement_change_orders(agreement_id) if co["id"] == change_order_id),
        None,
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Change order not found")
    updated = dict(existing)
    updated["status"] = payload.status
    updated["approver"] = payload.approver
    updated["decision_note"] = payload.decision_note
    updated["updated_at"] = _now_iso()
    saved_change_order = upsert_change_order_payload(updated)

    agreement = dict(current)
    if payload.status in {"approved", "implemented"}:
        agreement["agreement_status"] = "amended"
        agreement["updated_at"] = _now_iso()
        upsert_client_agreement_payload(agreement)
    create_agreement_audit_event(
        {
            "id": f"audit-{uuid4().hex[:12]}",
            "agreement_id": agreement_id,
            "project": current["project"],
            "event_type": "change_order_decision",
            "actor": payload.approver,
            "actor_role": payload.actor_role,
            "details": {"status": payload.status, "note": payload.decision_note},
            "created_at": _now_iso(),
            "data_class": "CONFIDENTIAL",
        }
    )
    return {"ok": True, "change_order": saved_change_order}


@app.get("/api/client-agreements/{agreement_id}/audit")
def get_agreement_audit(agreement_id: str) -> dict:
    current = get_client_agreement(agreement_id)
    if not current:
        raise HTTPException(status_code=404, detail="Client agreement not found")
    return {"agreement_id": agreement_id, "events": list_agreement_audit_events(agreement_id)}


@app.get("/api/labor-estimates")
def get_labor_estimates(project: str) -> dict:
    estimates = list_labor_estimates(project)
    return {"project": project, "labor_estimates": estimates}


@app.post("/api/labor-estimates")
def create_labor_estimate(payload: LaborEstimateCreate) -> dict:
    if not payload.modules:
        raise HTTPException(status_code=400, detail="At least one module is required")
    module_costs, total_hours, total_cost = _with_costs(payload.modules, payload.hourly_rate_usd)
    non_labor_costs, non_labor_one_time, non_labor_monthly, non_labor_variable = _summarize_non_labor(payload.non_labor_costs)
    total_build_cost = round(total_cost + non_labor_one_time, 2)
    total_monthly_run_cost = round(non_labor_monthly + non_labor_variable, 2)
    projected_12m_tco = round(total_build_cost + (total_monthly_run_cost * 12), 2)
    now = _now_iso()
    estimate = {
        "id": f"labor-{uuid4().hex[:12]}",
        "project": payload.project,
        "estimate_stage": "post-intake-pre-onboarding",
        "hourly_rate_usd": payload.hourly_rate_usd,
        "modules": module_costs,
        "non_labor_costs": non_labor_costs,
        "total_hours": total_hours,
        "total_cost_usd": total_cost,
        "non_labor_one_time_usd": non_labor_one_time,
        "non_labor_monthly_usd": non_labor_monthly,
        "non_labor_variable_monthly_usd": non_labor_variable,
        "total_build_cost_usd": total_build_cost,
        "total_monthly_run_cost_usd": total_monthly_run_cost,
        "projected_12m_tco_usd": projected_12m_tco,
        "confidence": payload.confidence,
        "assumptions": payload.assumptions,
        "created_by": payload.created_by,
        "source": "pm-portal",
        "created_at": now,
        "updated_at": now,
    }
    saved = upsert_labor_estimate_payload(estimate)
    return {"ok": True, "labor_estimate": saved}


@app.get("/api/secure-vault/files")
def get_secure_vault_files(project: str) -> dict:
    files = list_secure_vault_files(project)
    return {"project": project, "secure_vault_files": files}


@app.get("/api/secure-vault/drive-connection")
def get_secure_vault_drive_connection(project: str) -> dict:
    cache = _load_drive_connections()
    project_key = project.strip().lower()
    return {"project": project, "drive_connection": cache.get(project_key)}


@app.post("/api/secure-vault/drive-connection")
def connect_secure_vault_drive(payload: SecureVaultDriveConnectRequest) -> dict:
    _require_drive_connection_role(payload.actor_role)
    now = _now_iso()
    cache = _load_drive_connections()
    project_key = payload.project.strip().lower()
    record = {
        "id": cache.get(project_key, {}).get("id", f"vault-drive-{uuid4().hex[:12]}"),
        "project": payload.project,
        "provider": "google_drive",
        "status": "connected",
        "drive_account_email": payload.drive_account_email.strip(),
        "drive_folder_id": payload.drive_folder_id.strip(),
        "connected_by": payload.connected_by,
        "connected_at": now,
        "last_verified_at": now,
        "notes": payload.notes,
        "updated_at": now,
    }
    cache[project_key] = record
    _persist_drive_connections(cache)
    return {"ok": True, "drive_connection": record}


@app.post("/api/secure-vault/drive-connection/disconnect")
def disconnect_secure_vault_drive(payload: SecureVaultDriveDisconnectRequest) -> dict:
    _require_drive_connection_role(payload.actor_role)
    cache = _load_drive_connections()
    project_key = payload.project.strip().lower()
    existing = cache.get(project_key)
    if not existing:
        raise HTTPException(status_code=404, detail="Drive connection not found for project")
    now = _now_iso()
    updated = dict(existing)
    updated["status"] = "disconnected"
    updated["disconnected_by"] = payload.disconnected_by
    updated["disconnect_reason"] = payload.reason
    updated["updated_at"] = now
    cache[project_key] = updated
    _persist_drive_connections(cache)
    return {"ok": True, "drive_connection": updated}


@app.post("/api/secure-vault/files")
def register_secure_vault_file(payload: SecureVaultFileCreate) -> dict:
    now = _now_iso()
    file_id = f"vault-{uuid4().hex[:12]}"
    storage_path = payload.storage_uri or _build_secure_vault_path(
        payload.project, payload.client_name, payload.data_class, payload.file_name, file_id
    )
    file_row = {
        "id": file_id,
        "project": payload.project,
        "client_name": payload.client_name,
        "file_name": payload.file_name,
        "storage_uri": storage_path,
        "data_class": payload.data_class,
        "sensitivity_level": payload.sensitivity_level,
        "encryption_status": payload.encryption_status,
        "retention_policy": payload.retention_policy,
        "access_roles": payload.access_roles,
        "checksum_sha256": payload.checksum_sha256,
        "checksum_status": "pending",
        "upload_verified_at": None,
        "uploaded_by": payload.uploaded_by,
        "notes": payload.notes,
        "created_at": now,
        "updated_at": now,
    }
    saved = upsert_secure_vault_file_payload(file_row)
    append_secure_vault_audit_event(
        {
            "id": f"vault-audit-{uuid4().hex[:12]}",
            "vault_file_id": saved["id"],
            "project": saved["project"],
            "event_type": "file_registered",
            "actor_name": payload.uploaded_by or "system",
            "actor_role": "uploader",
            "details": {"data_class": payload.data_class, "sensitivity": payload.sensitivity_level, "storage_path": storage_path},
            "created_at": _now_iso(),
        }
    )
    return {"ok": True, "secure_vault_file": saved}


@app.post("/api/secure-vault/files/{vault_file_id}/signed-upload-url")
def get_secure_vault_signed_upload_url(vault_file_id: str, payload: SecureVaultSignedUrlRequest) -> dict:
    row = get_secure_vault_file_payload(vault_file_id)
    if not row:
        raise HTTPException(status_code=404, detail="Secure vault file not found")
    _require_vault_role(row, payload.actor_role)
    if not supabase_storage_configured():
        raise HTTPException(status_code=503, detail="Secure storage is not configured")
    storage_path = row.get("storage_uri") or _build_secure_vault_path(
        row.get("project", "unknown"),
        row.get("client_name", "unknown"),
        row.get("data_class", "other"),
        row.get("file_name", "file.bin"),
        vault_file_id,
    )
    signed = create_secure_vault_signed_upload_url(
        _secure_vault_bucket(), storage_path, payload.expires_in_seconds
    )
    append_secure_vault_audit_event(
        {
            "id": f"vault-audit-{uuid4().hex[:12]}",
            "vault_file_id": vault_file_id,
            "project": row.get("project", ""),
            "event_type": "signed_upload_url_issued",
            "actor_name": payload.actor_name,
            "actor_role": payload.actor_role,
            "details": {"expires_in_seconds": payload.expires_in_seconds},
            "created_at": _now_iso(),
        }
    )
    return {"ok": True, "signed_upload": signed, "storage_path": storage_path}


@app.post("/api/secure-vault/files/{vault_file_id}/signed-download-url")
def get_secure_vault_signed_download_url(vault_file_id: str, payload: SecureVaultSignedUrlRequest) -> dict:
    row = get_secure_vault_file_payload(vault_file_id)
    if not row:
        raise HTTPException(status_code=404, detail="Secure vault file not found")
    _require_vault_role(row, payload.actor_role)
    if not supabase_storage_configured():
        raise HTTPException(status_code=503, detail="Secure storage is not configured")
    storage_path = row.get("storage_uri") or _build_secure_vault_path(
        row.get("project", "unknown"),
        row.get("client_name", "unknown"),
        row.get("data_class", "other"),
        row.get("file_name", "file.bin"),
        vault_file_id,
    )
    signed = create_secure_vault_signed_download_url(
        _secure_vault_bucket(), storage_path, payload.expires_in_seconds
    )
    append_secure_vault_audit_event(
        {
            "id": f"vault-audit-{uuid4().hex[:12]}",
            "vault_file_id": vault_file_id,
            "project": row.get("project", ""),
            "event_type": "signed_download_url_issued",
            "actor_name": payload.actor_name,
            "actor_role": payload.actor_role,
            "details": {"expires_in_seconds": payload.expires_in_seconds},
            "created_at": _now_iso(),
        }
    )
    return {"ok": True, "signed_download": signed, "storage_path": storage_path}


@app.get("/api/secure-vault/files/{vault_file_id}/audit")
def get_secure_vault_file_audit(vault_file_id: str) -> dict:
    row = get_secure_vault_file_payload(vault_file_id)
    if not row:
        raise HTTPException(status_code=404, detail="Secure vault file not found")
    events = list_secure_vault_audit_events(vault_file_id)
    return {"vault_file_id": vault_file_id, "events": events}


@app.post("/api/secure-vault/files/{vault_file_id}/verify-checksum")
def verify_secure_vault_checksum(vault_file_id: str, payload: SecureVaultChecksumVerifyRequest) -> dict:
    row = get_secure_vault_file_payload(vault_file_id)
    if not row:
        raise HTTPException(status_code=404, detail="Secure vault file not found")
    _require_vault_role(row, payload.actor_role)
    if not supabase_storage_configured():
        raise HTTPException(status_code=503, detail="Secure storage is not configured")
    storage_path = row.get("storage_uri") or _build_secure_vault_path(
        row.get("project", "unknown"),
        row.get("client_name", "unknown"),
        row.get("data_class", "other"),
        row.get("file_name", "file.bin"),
        vault_file_id,
    )
    content = download_secure_vault_file_bytes(_secure_vault_bucket(), storage_path)
    actual_checksum = sha256_hex(content)
    expected = payload.expected_checksum_sha256.strip().lower()
    status = "verified" if actual_checksum == expected else "mismatch"
    updated = dict(row)
    updated["checksum_sha256"] = actual_checksum
    updated["checksum_status"] = status
    updated["upload_verified_at"] = _now_iso()
    updated["updated_at"] = _now_iso()
    saved = upsert_secure_vault_file_payload(updated)
    append_secure_vault_audit_event(
        {
            "id": f"vault-audit-{uuid4().hex[:12]}",
            "vault_file_id": vault_file_id,
            "project": row.get("project", ""),
            "event_type": "checksum_verified",
            "actor_name": payload.actor_name,
            "actor_role": payload.actor_role,
            "details": {"expected": expected, "actual": actual_checksum, "status": status},
            "created_at": _now_iso(),
        }
    )
    return {"ok": True, "secure_vault_file": saved, "status": status}
