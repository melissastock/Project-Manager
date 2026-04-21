import type { DecisionState, ProjectReadiness, StandupRun } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";

export async function fetchStandup(): Promise<StandupRun> {
  const response = await fetch(`${API_BASE}/api/standup`);
  if (!response.ok) throw new Error("Failed to fetch standup data");
  return response.json();
}

export async function updateDecision(id: string, payload: { state: DecisionState; rationale: string; owner: string; due_date: string; }): Promise<void> {
  const response = await fetch(`${API_BASE}/api/recommendations/${id}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error("Failed to update decision");
}

export function byProject(run: StandupRun, name: string): ProjectReadiness | undefined {
  return run.projects.find((p) => p.project.name === name);
}
