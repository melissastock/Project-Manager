import React from "react";
import type { ProjectReadiness } from "../types";
import { DimensionCard } from "../components/DimensionCard";
import { RecommendationPanel } from "../components/RecommendationPanel";
import { ScoreBadge } from "../components/ScoreBadge";
import { TeamStructurePanel } from "../components/TeamStructurePanel";
import { TicketPanel } from "../components/TicketPanel";

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
      <TeamStructurePanel project={project} onRefresh={onRefresh} />
      <TicketPanel project={project} onRefresh={onRefresh} />
    </div>
  );
}
