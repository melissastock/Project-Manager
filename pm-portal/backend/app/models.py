from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

ReadinessBand = Literal["ready", "monitor", "at-risk", "critical"]
DecisionState = Literal["approved", "rejected", "defer", "pending"]
RegistryStatus = Literal["registered", "unknown"]
RuntimeStatus = Literal["ok", "path-missing", "git-unavailable", "unborn"]
TicketState = Literal["new", "triaged", "in_progress", "blocked", "done", "deferred"]
TicketPriority = Literal["P0", "P1", "P2", "P3"]
AssignmentStatus = Literal["proposed", "approved", "rejected"]
AssigneeType = Literal["human", "agent", "hybrid"]
AgreementStatus = Literal["draft", "under_review", "ready_for_signature", "active", "locked", "amended"]
PricingModel = Literal["fixed", "package", "retainer", "mixed"]
ChangeOrderStatus = Literal["requested", "approved", "rejected", "implemented"]


class Project(BaseModel):
    name: str
    path: str
    lane: str = ""
    priority_class: str = ""
    intake_stage: str = ""
    category: str = ""
    role: str = ""
    governance_steward: str = ""
    lane_operator: str = ""
    release_packaging_owner: str = ""
    compliance_reviewer: str = ""
    automation_maintainer: str = ""
    kpi_profile: str = ""
    kpi_owner: str = ""
    kpi_reporting_cadence: str = ""
    financial_reporting_profile: str = ""
    downstream_governance_profile: str = ""
    downstream_governance_owner: str = ""
    project_type_escalation_triggers: str = ""
    budget_planned_usd: float = 0.0
    actual_spend_mtd_usd: float = 0.0
    committed_spend_usd: float = 0.0
    forecast_to_complete_usd: float = 0.0
    variance_usd: float = 0.0
    burn_rate_monthly_usd: float = 0.0
    runway_months: float = 0.0
    open_invoices_usd: float = 0.0
    overdue_ar_usd: float = 0.0


class SignalSnapshot(BaseModel):
    project: str
    branch: str
    head: str
    summary: str
    exists: bool
    is_git_repo: bool
    staged_count: int
    unstaged_count: int
    untracked_count: int
    ahead: Optional[int] = None
    behind: Optional[int] = None
    backlog_files: list[str] = Field(default_factory=list)
    sprint_files: list[str] = Field(default_factory=list)
    captured_at: datetime


class ReadinessDimensionScore(BaseModel):
    dimension: str
    score: int
    evidence: list[str] = Field(default_factory=list)


class Recommendation(BaseModel):
    id: str
    project: str
    action: str
    why_now: str
    risk_if_delayed: str
    alternatives_considered: str
    confidence: Literal["high", "medium", "low"] = "medium"


class RecommendationDecision(BaseModel):
    recommendation_id: str
    state: DecisionState
    rationale: str = ""
    owner: str = ""
    due_date: str = ""
    updated_at: datetime


class ProjectTicket(BaseModel):
    id: str
    project: str
    title: str
    description: str = ""
    state: TicketState = "new"
    priority: TicketPriority = "P2"
    owner: str = ""
    lane: str = ""
    scope_label: Literal["all-repos", "selected-lanes", "pm-portal-only"] = "pm-portal-only"
    due_date: str = ""
    source: str = "pm-portal"
    created_at: datetime
    updated_at: datetime


class TeamAssignment(BaseModel):
    id: str
    project: str
    role_key: str
    role_label: str
    raci_tags: list[Literal["R", "A", "C", "I"]] = Field(default_factory=list)
    assignee_name: str = ""
    assignee_type: AssigneeType = "human"
    workstream: str = ""
    narrative: str = ""
    status: AssignmentStatus = "proposed"
    approved_by: str = ""
    approved_at: datetime | None = None
    approval_note: str = ""
    source: str = "pm-portal"
    created_at: datetime
    updated_at: datetime


class AgreementDeliverable(BaseModel):
    id: str
    title: str
    description: str = ""
    due_date: str = ""
    acceptance_criteria: str = ""


class IntakeResponse(BaseModel):
    # Client-owned inputs
    client_goals: str = ""
    success_criteria: str = ""
    communication_preferences: str = ""
    primary_contact: str = ""
    required_assets: list[str] = Field(default_factory=list)

    # Business-owner-owned inputs
    constraints: str = ""
    dependencies: str = ""
    budget_range_usd: str = ""
    scope_boundaries: str = ""
    compliance_requirements: str = ""
    approval_authority: str = ""
    risk_assumptions: str = ""

    completed: bool = False
    completed_at: datetime | None = None


class ClientAgreement(BaseModel):
    id: str
    project: str
    client_name: str
    package_name: str = ""
    product_brief: str = ""
    scope_definition: str = ""
    deliverables_summary: str = ""
    pricing_model: PricingModel = "fixed"
    price_terms_json: dict = Field(default_factory=dict)
    agreement_status: AgreementStatus = "draft"
    is_locked: bool = False
    locked_at: datetime | None = None
    locked_by: str = ""
    lock_reason: str = ""
    owner_role: str = "business_owner"
    neuro_worker_type: str = "unspecified"
    intake: IntakeResponse = Field(default_factory=IntakeResponse)
    deliverables: list[AgreementDeliverable] = Field(default_factory=list)
    source: str = "pm-portal"
    created_at: datetime
    updated_at: datetime


class AgreementMessage(BaseModel):
    id: str
    agreement_id: str
    project: str
    author_name: str
    author_role: str = "client"
    message: str
    visibility: Literal["client_and_team", "internal_only"] = "client_and_team"
    created_at: datetime


class AgreementChangeOrder(BaseModel):
    id: str
    agreement_id: str
    project: str
    requested_by: str
    requested_scope_delta: str
    requested_price_delta: str = ""
    requested_timeline_delta: str = ""
    status: ChangeOrderStatus = "requested"
    approver: str = ""
    decision_note: str = ""
    created_at: datetime
    updated_at: datetime


class LaborEstimateModule(BaseModel):
    module_key: Literal["strategy", "development", "operationalization", "governance", "marketing", "gtm"]
    estimated_hours: float = 0.0
    estimated_cost_usd: float = 0.0
    notes: str = ""
    subcomponents: list[str] = Field(default_factory=list)


class NonLaborCostItem(BaseModel):
    category: Literal["hosting", "storage", "third_party_tools", "security_compliance", "operations_support", "contingency", "other"]
    one_time_usd: float = 0.0
    monthly_recurring_usd: float = 0.0
    usage_variable_monthly_usd: float = 0.0
    notes: str = ""


class LaborEstimate(BaseModel):
    id: str
    project: str
    estimate_stage: Literal["post-intake-pre-onboarding"] = "post-intake-pre-onboarding"
    hourly_rate_usd: float = 150.0
    modules: list[LaborEstimateModule] = Field(default_factory=list)
    non_labor_costs: list[NonLaborCostItem] = Field(default_factory=list)
    total_hours: float = 0.0
    total_cost_usd: float = 0.0
    non_labor_one_time_usd: float = 0.0
    non_labor_monthly_usd: float = 0.0
    non_labor_variable_monthly_usd: float = 0.0
    total_build_cost_usd: float = 0.0
    total_monthly_run_cost_usd: float = 0.0
    projected_12m_tco_usd: float = 0.0
    confidence: Literal["low", "medium", "high"] = "medium"
    assumptions: list[str] = Field(default_factory=list)
    created_by: str = ""
    source: str = "pm-portal"
    created_at: datetime
    updated_at: datetime


class SecureVaultFile(BaseModel):
    id: str
    project: str
    client_name: str = ""
    file_name: str
    storage_uri: str = ""
    data_class: Literal["ip_invention", "financial", "legal", "medical", "regulated", "other"]
    sensitivity_level: Literal["restricted", "highly_restricted"] = "restricted"
    encryption_status: Literal["encrypted_at_rest", "encrypted_at_rest_and_transport"] = "encrypted_at_rest_and_transport"
    retention_policy: str = "retain-until-client-request-or-policy-expiry"
    access_roles: list[str] = Field(default_factory=list)
    checksum_sha256: str = ""
    checksum_status: Literal["pending", "verified", "mismatch"] = "pending"
    upload_verified_at: datetime | None = None
    uploaded_by: str = ""
    notes: str = ""
    created_at: datetime
    updated_at: datetime


class BranchHealth(BaseModel):
    branch: str
    head: str
    subject: str
    age_days: int
    upstream: str
    ahead: Optional[int] = None
    behind: Optional[int] = None
    commits_since_main_base: Optional[int] = None
    score: int
    band: ReadinessBand
    recommendation: str


class ProjectReadiness(BaseModel):
    project: Project
    registry_status: RegistryStatus = "registered"
    runtime_status: RuntimeStatus
    runtime_note: str = ""
    score: int
    band: ReadinessBand
    dimensions: list[ReadinessDimensionScore]
    snapshot: SignalSnapshot
    branch_health: list[BranchHealth]
    recommendations: list[Recommendation]
    decisions: list[RecommendationDecision]
    tickets: list[ProjectTicket] = Field(default_factory=list)
    team_assignments: list[TeamAssignment] = Field(default_factory=list)
    client_agreements: list[ClientAgreement] = Field(default_factory=list)
    labor_estimates: list[LaborEstimate] = Field(default_factory=list)
    secure_vault_files: list[SecureVaultFile] = Field(default_factory=list)


class StandupRun(BaseModel):
    generated_at: datetime
    projects: list[ProjectReadiness]


class RuntimeObservation(BaseModel):
    project_name: str
    project_path: str
    intake_stage: str
    registry_status: RegistryStatus
    runtime_status: RuntimeStatus
    runtime_note: str
    exists: bool
    is_git_repo: bool
    branch: str
    head: str
    summary: str
    observed_at: datetime
