import React from "react";
import type { ProjectReadiness } from "../types";
import { DimensionCard } from "../components/DimensionCard";
import { RecommendationPanel } from "../components/RecommendationPanel";
import { ScoreBadge } from "../components/ScoreBadge";

export function ProjectDetailPage({ project, onRefresh }: { project: ProjectReadiness; onRefresh: () => Promise<void> }) {
  return (
    <div>
      <h2>{project.project.name}</h2>
      <p>{project.project.role}</p>
      <ScoreBadge score={project.score} band={project.band} />

      <h3 style={{ marginTop: 20 }}>Delivery snapshot</h3>
      <ul>
        <li>Branch: {project.snapshot.branch}</li>
        <li>Head: {project.snapshot.head || "n/a"}</li>
        <li>Summary: {project.snapshot.summary}</li>
        <li>Drift: staged {project.snapshot.staged_count}, unstaged {project.snapshot.unstaged_count}, untracked {project.snapshot.untracked_count}</li>
        <li>Sync: ahead {project.snapshot.ahead ?? "n/a"}, behind {project.snapshot.behind ?? "n/a"}</li>
        <li>Monetization docs: {project.snapshot.monetization_files.length} (required: {project.snapshot.monetization_required ? "yes" : "no"})</li>
      </ul>

      <h3>Readiness dimensions</h3>
      {project.dimensions.map((dimension) => <DimensionCard key={dimension.dimension} dimension={dimension} />)}

      <h3 style={{ marginTop: 20 }}>Branch health</h3>
      <div style={{ overflowX: "auto", marginBottom: 20 }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Branch</th>
              <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Score</th>
              <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Band</th>
              <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Age</th>
              <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Ahead</th>
              <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Behind</th>
              <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Recommendation</th>
            </tr>
          </thead>
          <tbody>
            {project.branch_health.map((row) => (
              <tr key={row.branch}>
                <td style={{ borderBottom: "1px solid #f0f0f0", padding: "6px 0" }}>
                  <strong>{row.branch}</strong>
                  <div style={{ fontSize: 12, color: "#555" }}>{row.head} - {row.subject}</div>
                </td>
                <td style={{ borderBottom: "1px solid #f0f0f0" }}>{row.score}</td>
                <td style={{ borderBottom: "1px solid #f0f0f0" }}>{row.band}</td>
                <td style={{ borderBottom: "1px solid #f0f0f0" }}>{row.age_days}d</td>
                <td style={{ borderBottom: "1px solid #f0f0f0" }}>{row.ahead ?? "n/a"}</td>
                <td style={{ borderBottom: "1px solid #f0f0f0" }}>{row.behind ?? "n/a"}</td>
                <td style={{ borderBottom: "1px solid #f0f0f0" }}>{row.recommendation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <RecommendationPanel project={project} onRefresh={onRefresh} />
    </div>
  );
}
