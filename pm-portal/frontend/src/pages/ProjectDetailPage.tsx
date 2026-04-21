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
      </ul>

      <h3>Readiness dimensions</h3>
      {project.dimensions.map((dimension) => <DimensionCard key={dimension.dimension} dimension={dimension} />)}

      <RecommendationPanel project={project} onRefresh={onRefresh} />
    </div>
  );
}
