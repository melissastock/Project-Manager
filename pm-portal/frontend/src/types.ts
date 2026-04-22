export type DecisionState = "approved" | "rejected" | "defer" | "pending";

export interface RecommendationDecision {
  recommendation_id: string;
  state: DecisionState;
  rationale: string;
  owner: string;
  due_date: string;
  updated_at: string;
}

export interface Recommendation {
  id: string;
  project: string;
  action: string;
  why_now: string;
  risk_if_delayed: string;
  alternatives_considered: string;
  confidence: "high" | "medium" | "low";
}

export interface Ticket {
  id: string;
  project: string;
  title: string;
  description: string;
  state: "new" | "triaged" | "in_progress" | "blocked" | "done" | "deferred";
  priority: "P0" | "P1" | "P2" | "P3";
  owner: string;
  lane: string;
  scope_label: "all-repos" | "selected-lanes" | "pm-portal-only";
  due_date: string;
  source: string;
  created_at: string;
  updated_at: string;
}

export interface TeamAssignment {
  id: string;
  project: string;
  role_key: string;
  role_label: string;
  raci_tags: Array<"R" | "A" | "C" | "I">;
  assignee_name: string;
  assignee_type: "human" | "agent" | "hybrid";
  workstream: string;
  narrative: string;
  status: "proposed" | "approved" | "rejected";
  approved_by: string;
  approved_at: string | null;
  approval_note: string;
  source: string;
  created_at: string;
  updated_at: string;
}

export interface GovernanceCheckStatus {
  check: string;
  flag: string;
  status: "enabled" | "skipped";
}

export interface GovernanceRunSummary {
  generated_at: string;
  profile: string;
  target_repo: string;
  target_lane: string;
  trigger_reason: string;
  checks: GovernanceCheckStatus[];
}

export interface DimensionScore {
  dimension: string;
  score: number;
  evidence: string[];
}

export interface Snapshot {
  branch: string;
  head: string;
  summary: string;
  staged_count: number;
  unstaged_count: number;
  untracked_count: number;
  ahead: number | null;
  behind: number | null;
  backlog_files: string[];
  sprint_files: string[];
}

export interface BranchHealth {
  branch: string;
  head: string;
  subject: string;
  age_days: number;
  upstream: string;
  ahead: number | null;
  behind: number | null;
  commits_since_main_base: number | null;
  score: number;
  band: "ready" | "monitor" | "at-risk" | "critical";
  recommendation: string;
}

export interface ProjectReadiness {
  project: {
    name: string;
    path: string;
    lane: string;
    priority_class: string;
    intake_stage: string;
    category: string;
    role: string;
    governance_steward: string;
    lane_operator: string;
    release_packaging_owner: string;
    compliance_reviewer: string;
    automation_maintainer: string;
    kpi_profile: string;
    kpi_owner: string;
    kpi_reporting_cadence: string;
    financial_reporting_profile: string;
    downstream_governance_profile: string;
    downstream_governance_owner: string;
    project_type_escalation_triggers: string;
    budget_planned_usd: number;
    actual_spend_mtd_usd: number;
    committed_spend_usd: number;
    forecast_to_complete_usd: number;
    variance_usd: number;
    burn_rate_monthly_usd: number;
    runway_months: number;
    open_invoices_usd: number;
    overdue_ar_usd: number;
  };
  registry_status: "registered" | "unknown";
  runtime_status: "ok" | "path-missing" | "git-unavailable" | "unborn";
  runtime_note: string;
  score: number;
  band: "ready" | "monitor" | "at-risk" | "critical";
  dimensions: DimensionScore[];
  snapshot: Snapshot;
  branch_health: BranchHealth[];
  recommendations: Recommendation[];
  decisions: RecommendationDecision[];
  tickets: Ticket[];
  team_assignments: TeamAssignment[];
}

export interface StandupRun {
  generated_at: string;
  projects: ProjectReadiness[];
}
