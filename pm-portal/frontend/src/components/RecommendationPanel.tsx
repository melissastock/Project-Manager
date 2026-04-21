import React, { useMemo, useState } from "react";
import { updateDecision } from "../api";
import type { DecisionState, ProjectReadiness } from "../types";

function decisionFor(project: ProjectReadiness, id: string) {
  return project.decisions.find((d) => d.recommendation_id === id);
}

export function RecommendationPanel({ project, onRefresh }: { project: ProjectReadiness; onRefresh: () => Promise<void> }) {
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string>("");

  const ownerDefault = useMemo(() => "Melissa Stock", []);

  async function decide(id: string, state: DecisionState) {
    try {
      setBusy(id);
      setError("");
      await updateDecision(id, {
        state,
        rationale: `Decision set to ${state} from PM portal UI`,
        owner: ownerDefault,
        due_date: ""
      });
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  return (
    <div>
      <h3>Recommended next steps</h3>
      {error ? <p style={{ color: "crimson" }}>{error}</p> : null}
      {project.recommendations.map((rec) => {
        const decision = decisionFor(project, rec.id);
        return (
          <div key={rec.id} style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, marginBottom: 10 }}>
            <strong>{rec.action}</strong>
            <p><strong>Why now:</strong> {rec.why_now}</p>
            <p><strong>Risk if delayed:</strong> {rec.risk_if_delayed}</p>
            <p><strong>Alternatives considered:</strong> {rec.alternatives_considered}</p>
            <p><strong>Decision:</strong> {decision?.state ?? "pending"}</p>
            <div style={{ display: "flex", gap: 8 }}>
              <button disabled={busy === rec.id} onClick={() => decide(rec.id, "approved")}>Approve</button>
              <button disabled={busy === rec.id} onClick={() => decide(rec.id, "defer")}>Defer</button>
              <button disabled={busy === rec.id} onClick={() => decide(rec.id, "rejected")}>Reject</button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
