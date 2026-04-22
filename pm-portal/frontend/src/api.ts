import type { DecisionState, GovernanceRunSummary, ProjectReadiness, StandupRun, TeamAssignment, Ticket } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";

export async function fetchStandup(): Promise<StandupRun> {
  const response = await fetch(`${API_BASE}/api/standup`);
  if (!response.ok) throw new Error("Failed to fetch standup data");
  return response.json();
}

export async function fetchLatestGovernanceSummary(): Promise<GovernanceRunSummary | null> {
  const response = await fetch(`${API_BASE}/api/governance/latest`);
  if (!response.ok) throw new Error("Failed to fetch governance summary");
  const payload = await response.json();
  if (!payload.available) return null;
  return payload.summary as GovernanceRunSummary;
}

export async function updateDecision(id: string, payload: { state: DecisionState; rationale: string; owner: string; due_date: string; }): Promise<void> {
  const response = await fetch(`${API_BASE}/api/recommendations/${id}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error("Failed to update decision");
}

export async function createTicket(payload: {
  project: string;
  title: string;
  description: string;
  priority: "P0" | "P1" | "P2" | "P3";
  owner: string;
  lane: string;
  scope_label: "all-repos" | "selected-lanes" | "pm-portal-only";
  due_date: string;
}): Promise<Ticket> {
  const response = await fetch(`${API_BASE}/api/tickets`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to create ticket");
  const json = await response.json();
  return json.ticket as Ticket;
}

export async function updateTicket(id: string, payload: Partial<Pick<Ticket, "state" | "priority" | "owner" | "due_date" | "title" | "description">>): Promise<Ticket> {
  const response = await fetch(`${API_BASE}/api/tickets/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to update ticket");
  const json = await response.json();
  return json.ticket as Ticket;
}

export async function updateTeamAssignment(projectName: string, roleKey: string, payload: Partial<Pick<TeamAssignment, "assignee_name" | "assignee_type" | "workstream" | "narrative" | "status" | "approval_note">>): Promise<TeamAssignment> {
  const response = await fetch(`${API_BASE}/api/team-assignments/${encodeURIComponent(projectName)}/${roleKey}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to update team assignment");
  const json = await response.json();
  return json.team_assignment as TeamAssignment;
}

export async function approveProjectTeam(projectName: string, payload: { approved_by: string; approval_note: string; }): Promise<TeamAssignment[]> {
  const response = await fetch(`${API_BASE}/api/team-assignments/${encodeURIComponent(projectName)}/approve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to approve team assignments");
  const json = await response.json();
  return (json.team_assignments ?? []) as TeamAssignment[];
}

export function byProject(run: StandupRun, name: string): ProjectReadiness | undefined {
  return run.projects.find((p) => p.project.name === name);
}
