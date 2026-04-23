import React, { useEffect, useMemo, useState } from "react";
import { fetchLatestGovernanceSummary, fetchStandup } from "./api";
import { ProjectDetailPage } from "./pages/ProjectDetailPage";
import type { GovernanceRunSummary, ProjectReadiness, StandupRun } from "./types";

export default function App() {
  const [run, setRun] = useState<StandupRun | null>(null);
  const [selectedName, setSelectedName] = useState<string>("");
  const [error, setError] = useState<string>("");
  const [govSummary, setGovSummary] = useState<GovernanceRunSummary | null>(null);

  async function refresh() {
    try {
      setError("");
      const next = await fetchStandup();
      const nextSummary = await fetchLatestGovernanceSummary();
      setRun(next);
      setGovSummary(nextSummary);
      if (!selectedName && next.projects.length > 0) {
        setSelectedName(next.projects[0].project.name);
      }
    } catch (err) {
      setError((err as Error).message);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  const selected: ProjectReadiness | undefined = useMemo(
    () => run?.projects.find((p) => p.project.name === selectedName),
    [run, selectedName]
  );

  return (
    <main className="pm-app">
      <h1 className="pm-brand-title">Portfolio Command Center</h1>
      <p className="pm-subtitle">Decision-oriented readiness dashboard aligned to the MJSDS brand system.</p>
      {error ? <p className="pm-error">{error}</p> : null}

      <div className="pm-shell">
        <aside className="pm-card pm-pane pm-scroll-pane">
          <div className="pm-card-block">
            <div className="pm-meta-label">Latest Governance Run</div>
            {govSummary ? (
              <div>
                <div className="pm-status-line">Profile: {govSummary.profile}</div>
                <div className="pm-status-line">Trigger: {govSummary.trigger_reason}</div>
                <div className="pm-status-line">
                  Enabled checks: {govSummary.checks.filter((c) => c.status === "enabled").length}/{govSummary.checks.length}
                </div>
                <div className="pm-status-line">Updated: {new Date(govSummary.generated_at).toLocaleString()}</div>
              </div>
            ) : (
              <div className="pm-status-line">No governance run summary available yet.</div>
            )}
          </div>
          <div className="pm-sidebar-header">
            <div>
              <div className="pm-meta-label">Portfolio Projects</div>
              <strong>Needs Decision Queue</strong>
            </div>
            <button className="pm-action-btn" onClick={refresh}>Refresh</button>
          </div>
          <ul className="pm-project-list">
            {run?.projects.map((project) => (
              <li key={project.project.name}>
                <button className={`pm-project-btn ${selectedName === project.project.name ? "active" : ""}`} onClick={() => setSelectedName(project.project.name)}>
                  <strong>{project.project.name}</strong>
                  <div className="pm-status-line">{project.band} ({project.score})</div>
                  <div className="pm-status-line">onboarding: {project.registry_status}, runtime: {project.runtime_status}</div>
                </button>
              </li>
            ))}
          </ul>
        </aside>
        <section className="pm-card pm-pane">
          {selected ? <ProjectDetailPage project={selected} onRefresh={refresh} /> : <p>Select a project.</p>}
        </section>
      </div>
    </main>
  );
}
