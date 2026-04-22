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

export interface AgreementDeliverable {
  id: string;
  title: string;
  description: string;
  due_date: string;
  acceptance_criteria: string;
}

export interface IntakeResponse {
  // Client-owned
  client_goals: string;
  success_criteria: string;
  communication_preferences: string;
  primary_contact: string;
  required_assets: string[];

  // Business-owner-owned
  constraints: string;
  dependencies: string;
  budget_range_usd: string;
  scope_boundaries: string;
  compliance_requirements: string;
  approval_authority: string;
  risk_assumptions: string;

  completed: boolean;
  completed_at: string | null;
}

export interface ClientAgreement {
  id: string;
  project: string;
  client_name: string;
  package_name: string;
  product_brief: string;
  scope_definition: string;
  deliverables_summary: string;
  pricing_model: "fixed" | "package" | "retainer" | "mixed";
  price_terms_json: Record<string, unknown>;
  agreement_status: "draft" | "under_review" | "ready_for_signature" | "active" | "locked" | "amended";
  is_locked: boolean;
  locked_at: string | null;
  locked_by: string;
  lock_reason: string;
  owner_role: string;
  neuro_worker_type: string;
  intake: IntakeResponse;
  deliverables: AgreementDeliverable[];
  source: string;
  created_at: string;
  updated_at: string;
}

export interface AgreementMessage {
  id: string;
  agreement_id: string;
  project: string;
  author_name: string;
  author_role: string;
  message: string;
  visibility: "client_and_team" | "internal_only";
  created_at: string;
}

export interface AgreementChangeOrder {
  id: string;
  agreement_id: string;
  project: string;
  requested_by: string;
  requested_scope_delta: string;
  requested_price_delta: string;
  requested_timeline_delta: string;
  status: "requested" | "approved" | "rejected" | "implemented";
  approver: string;
  decision_note: string;
  created_at: string;
  updated_at: string;
}

export interface LaborEstimateModule {
  module_key: "strategy" | "development" | "operationalization" | "governance" | "marketing" | "gtm";
  estimated_hours: number;
  estimated_cost_usd: number;
  notes: string;
  subcomponents: string[];
}

export interface NonLaborCostItem {
  category: "hosting" | "storage" | "third_party_tools" | "security_compliance" | "operations_support" | "contingency" | "other";
  one_time_usd: number;
  monthly_recurring_usd: number;
  usage_variable_monthly_usd: number;
  notes: string;
}

export interface LaborEstimate {
  id: string;
  project: string;
  estimate_stage: "post-intake-pre-onboarding";
  hourly_rate_usd: number;
  modules: LaborEstimateModule[];
  non_labor_costs: NonLaborCostItem[];
  total_hours: number;
  total_cost_usd: number;
  non_labor_one_time_usd: number;
  non_labor_monthly_usd: number;
  non_labor_variable_monthly_usd: number;
  total_build_cost_usd: number;
  total_monthly_run_cost_usd: number;
  projected_12m_tco_usd: number;
  confidence: "low" | "medium" | "high";
  assumptions: string[];
  created_by: string;
  source: string;
  created_at: string;
  updated_at: string;
}

export interface SecureVaultFile {
  id: string;
  project: string;
  client_name: string;
  file_name: string;
  storage_uri: string;
  data_class: "ip_invention" | "financial" | "legal" | "medical" | "regulated" | "other";
  sensitivity_level: "restricted" | "highly_restricted";
  encryption_status: "encrypted_at_rest" | "encrypted_at_rest_and_transport";
  retention_policy: string;
  access_roles: string[];
  checksum_sha256: string;
  checksum_status: "pending" | "verified" | "mismatch";
  upload_verified_at: string | null;
  uploaded_by: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface SecureVaultDriveConnection {
  id: string;
  project: string;
  provider: "google_drive";
  status: "connected" | "disconnected";
  drive_account_email: string;
  drive_folder_id: string;
  connected_by: string;
  connected_at: string;
  last_verified_at: string;
  notes: string;
  updated_at: string;
  disconnected_by?: string;
  disconnect_reason?: string;
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
  client_agreements: ClientAgreement[];
  labor_estimates: LaborEstimate[];
  secure_vault_files: SecureVaultFile[];
}

export interface StandupRun {
  generated_at: string;
  projects: ProjectReadiness[];
}
