import React, { useMemo, useState } from "react";
import { approveProjectTeam, updateTeamAssignment } from "../api";
import type { ProjectReadiness } from "../types";

function statusLabel(status: string): string {
  if (status === "approved") return "approved by owner";
  if (status === "rejected") return "needs replacement";
  return "pending owner approval";
}

export function TeamStructurePanel({ project, onRefresh }: { project: ProjectReadiness; onRefresh: () => Promise<void> }) {
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [approver, setApprover] = useState("Melissa Stock");
  const [note, setNote] = useState("");
  const pendingCount = useMemo(() => project.team_assignments.filter((item) => item.status !== "approved").length, [project.team_assignments]);

  async function approveAll() {
    try {
      setBusy("approve-all");
      setError("");
      await approveProjectTeam(project.project.name, { approved_by: approver.trim() || "Owner", approval_note: note.trim() });
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function markRejected(roleKey: string) {
    try {
      setBusy(roleKey);
      setError("");
      await updateTeamAssignment(project.project.name, roleKey, { status: "rejected", approval_note: "Owner requested a new assignment proposal." });
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  return (
    <div>
      <h3 className="pm-section-title pm-section-title-spaced">Your Delivery Team</h3>
      <p className="pm-subtitle">
        Transparent labor map for this project. Each card shows who is handling the workstream and how responsibility is divided.
      </p>
      {error ? <p className="pm-error">{error}</p> : null}

      <div className="pm-card pm-card-block">
        <div className="pm-flex-between">
          <strong>Human approval checkpoint</strong>
          <span className="pm-muted-metadata">{pendingCount} role(s) pending approval</span>
        </div>
        <div className="pm-action-row">
          <input className="pm-input" value={approver} onChange={(e) => setApprover(e.target.value)} placeholder="Approver name" />
          <input className="pm-input" value={note} onChange={(e) => setNote(e.target.value)} placeholder="Optional approval note" />
          <button className="pm-action-btn" disabled={busy === "approve-all"} onClick={approveAll}>Approve Team</button>
        </div>
      </div>

      {project.team_assignments.map((assignment) => (
        <div key={assignment.id} className="pm-card pm-card-block">
          <div className="pm-flex-between">
            <strong>{assignment.role_label}</strong>
            <span className="pm-muted-metadata">{statusLabel(assignment.status)}</span>
          </div>
          <p><strong>{assignment.assignee_name || "Unassigned"}</strong> ({assignment.assignee_type})</p>
          <p>{assignment.narrative}</p>
          <p className="pm-muted-metadata">
            Workstream: {assignment.workstream} | RACI: {assignment.raci_tags.join("/")}
          </p>
          <p className="pm-muted-metadata">
            Approved by: {assignment.approved_by || "pending"} {assignment.approved_at ? `(${new Date(assignment.approved_at).toLocaleString()})` : ""}
          </p>
          <div className="pm-action-row">
            <button className="pm-action-btn secondary" disabled={busy === assignment.role_key} onClick={() => markRejected(assignment.role_key)}>
              Request Reassignment
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
