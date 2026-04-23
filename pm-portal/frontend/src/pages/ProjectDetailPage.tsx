import React from "react";
import type { ProjectReadiness } from "../types";
import { DimensionCard } from "../components/DimensionCard";
import { RecommendationPanel } from "../components/RecommendationPanel";
import { ScoreBadge } from "../components/ScoreBadge";
import { ClientAgreementPanel } from "../components/ClientAgreementPanel";
import { LaborEstimatePanel } from "../components/LaborEstimatePanel";
import { SecureVaultPanel } from "../components/SecureVaultPanel";
import { CaseProceduralAnalysisPanel } from "../components/CaseProceduralAnalysisPanel";
import { TeamStructurePanel } from "../components/TeamStructurePanel";
import { TicketPanel } from "../components/TicketPanel";

function formatUsd(value: number) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(value ?? 0);
}

export function ProjectDetailPage({ project, onRefresh }: { project: ProjectReadiness; onRefresh: () => Promise<void> }) {
  return (
    <div>
      <h2 className="pm-section-title">{project.project.name}</h2>
      <p className="pm-subtitle">{project.project.role}</p>
      <ScoreBadge score={project.score} band={project.band} />

      <h3 className="pm-section-title pm-section-title-spaced">Operational Snapshot</h3>
      <ul className="pm-inline-list">
        <li>Registry onboarding: {project.registry_status} ({project.project.intake_stage || "unknown stage"})</li>
        <li>Runtime access: {project.runtime_status} - {project.runtime_note}</li>
        <li>Branch: {project.snapshot.branch}</li>
        <li>Head: {project.snapshot.head || "n/a"}</li>
        <li>Summary: {project.snapshot.summary}</li>
        <li>Drift: staged {project.snapshot.staged_count}, unstaged {project.snapshot.unstaged_count}, untracked {project.snapshot.untracked_count}</li>
        <li>Sync: ahead {project.snapshot.ahead ?? "n/a"}, behind {project.snapshot.behind ?? "n/a"}</li>
        <li>KPI profile: {project.project.kpi_profile || "not set"} (owner: {project.project.kpi_owner || "not set"})</li>
        <li>KPI cadence: {project.project.kpi_reporting_cadence || "not set"}</li>
        <li>Financial profile: {project.project.financial_reporting_profile || "not set"}</li>
        <li>Downstream governance: {project.project.downstream_governance_profile || "not set"} (owner: {project.project.downstream_governance_owner || "not set"})</li>
        <li>Budget vs actual: {formatUsd(project.project.budget_planned_usd)} vs {formatUsd(project.project.actual_spend_mtd_usd)}</li>
        <li>Committed vs forecast: {formatUsd(project.project.committed_spend_usd)} vs {formatUsd(project.project.forecast_to_complete_usd)}</li>
        <li>Variance: {formatUsd(project.project.variance_usd)} · Burn/mo: {formatUsd(project.project.burn_rate_monthly_usd)} · Runway: {project.project.runway_months ?? 0} mo</li>
        <li>Open invoices: {formatUsd(project.project.open_invoices_usd)} · Overdue AR: {formatUsd(project.project.overdue_ar_usd)}</li>
      </ul>

      <h3 className="pm-section-title">Readiness Dimensions</h3>
      {project.dimensions.map((dimension) => <DimensionCard key={dimension.dimension} dimension={dimension} />)}

      <h3 className="pm-section-title pm-section-title-spaced">Branch Health</h3>
      <div className="pm-table-wrap">
        <table className="pm-table">
          <thead>
            <tr>
              <th>Branch</th>
              <th>Score</th>
              <th>Band</th>
              <th>Age</th>
              <th>Ahead</th>
              <th>Behind</th>
              <th>Recommendation</th>
            </tr>
          </thead>
          <tbody>
            {project.branch_health.map((row) => (
              <tr key={row.branch}>
                <td>
                  <strong>{row.branch}</strong>
                  <div className="pm-muted-metadata">{row.head} - {row.subject}</div>
                </td>
                <td>{row.score}</td>
                <td>{row.band}</td>
                <td>{row.age_days}d</td>
                <td>{row.ahead ?? "n/a"}</td>
                <td>{row.behind ?? "n/a"}</td>
                <td>{row.recommendation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <RecommendationPanel project={project} onRefresh={onRefresh} />
      <ClientAgreementPanel project={project} onRefresh={onRefresh} />
      <LaborEstimatePanel project={project} onRefresh={onRefresh} />
      <SecureVaultPanel project={project} onRefresh={onRefresh} />
      <CaseProceduralAnalysisPanel project={project} />
      <TeamStructurePanel project={project} onRefresh={onRefresh} />
      <TicketPanel project={project} onRefresh={onRefresh} />
    </div>
  );
}
