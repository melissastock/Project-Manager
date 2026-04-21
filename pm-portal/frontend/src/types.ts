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
  monetization_files: string[];
  monetization_required: boolean;
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
  };
  score: number;
  band: "ready" | "monitor" | "at-risk" | "critical";
  dimensions: DimensionScore[];
  snapshot: Snapshot;
  branch_health: BranchHealth[];
  recommendations: Recommendation[];
  decisions: RecommendationDecision[];
}

export interface StandupRun {
  generated_at: string;
  projects: ProjectReadiness[];
}
