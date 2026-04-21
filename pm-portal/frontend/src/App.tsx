import React, { useEffect, useMemo, useState } from "react";
import { fetchStandup } from "./api";
import { ProjectDetailPage } from "./pages/ProjectDetailPage";
import type { ProjectReadiness, StandupRun } from "./types";

export default function App() {
  const [run, setRun] = useState<StandupRun | null>(null);
  const [selectedName, setSelectedName] = useState<string>("");
  const [error, setError] = useState<string>("");

  async function refresh() {
    try {
      setError("");
      const next = await fetchStandup();
      setRun(next);
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
    <main style={{ maxWidth: 1200, margin: "0 auto", padding: 16, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1>PM Portal</h1>
      <p>Project deep-dive readiness dashboard (Phase 1).</p>
      {error ? <p style={{ color: "crimson" }}>{error}</p> : null}

      <div style={{ display: "grid", gridTemplateColumns: "320px 1fr", gap: 16 }}>
        <aside style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, maxHeight: "80vh", overflow: "auto" }}>
          <h3>Projects</h3>
          <button onClick={refresh}>Refresh</button>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {run?.projects.map((project) => (
              <li key={project.project.name} style={{ marginTop: 10 }}>
                <button style={{ width: "100%", textAlign: "left", padding: 8, borderRadius: 6, border: selectedName === project.project.name ? "2px solid #2255aa" : "1px solid #ccc", background: "#fff" }} onClick={() => setSelectedName(project.project.name)}>
                  <strong>{project.project.name}</strong>
                  <div style={{ fontSize: 12, color: "#555" }}>{project.band} ({project.score})</div>
                </button>
              </li>
            ))}
          </ul>
        </aside>
        <section style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16 }}>
          {selected ? <ProjectDetailPage project={selected} onRefresh={refresh} /> : <p>Select a project.</p>}
        </section>
      </div>
    </main>
  );
}
