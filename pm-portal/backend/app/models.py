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
