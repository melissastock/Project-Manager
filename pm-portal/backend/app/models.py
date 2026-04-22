from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

ReadinessBand = Literal["ready", "monitor", "at-risk", "critical"]
DecisionState = Literal["approved", "rejected", "defer", "pending"]
RegistryStatus = Literal["registered", "unknown"]
RuntimeStatus = Literal["ok", "path-missing", "git-unavailable", "unborn"]


class Project(BaseModel):
    name: str
    path: str
    lane: str = ""
    priority_class: str = ""
    intake_stage: str = ""
    category: str = ""
    role: str = ""


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
