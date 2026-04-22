import React, { useMemo, useState } from "react";
import { createTicket, updateTicket } from "../api";
import type { ProjectReadiness, Ticket } from "../types";

const STATES: Ticket["state"][] = ["new", "triaged", "in_progress", "blocked", "done", "deferred"];
const PRIORITIES: Ticket["priority"][] = ["P0", "P1", "P2", "P3"];

export function TicketPanel({ project, onRefresh }: { project: ProjectReadiness; onRefresh: () => Promise<void> }) {
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<Ticket["priority"]>("P2");
  const ownerDefault = useMemo(() => "Melissa Stock", []);

  async function createNewTicket() {
    if (!title.trim()) return;
    try {
      setBusy("create");
      setError("");
      await createTicket({
        project: project.project.name,
        title: title.trim(),
        description: description.trim(),
        priority,
        owner: ownerDefault,
        lane: project.project.lane,
        scope_label: "pm-portal-only",
        due_date: "",
      });
      setTitle("");
      setDescription("");
      setPriority("P2");
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function setState(id: string, state: Ticket["state"]) {
    try {
      setBusy(id);
      setError("");
      await updateTicket(id, { state });
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  return (
    <div>
      <h3 className="pm-section-title pm-section-title-spaced">Tickets</h3>
      {error ? <p className="pm-error">{error}</p> : null}

      <div className="pm-card pm-card-block">
        <div className="pm-meta-label">Create ticket</div>
        <input
          className="pm-input"
          placeholder="Ticket title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          className="pm-input pm-textarea"
          placeholder="Short description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <div className="pm-action-row">
          <select className="pm-input" value={priority} onChange={(e) => setPriority(e.target.value as Ticket["priority"])}>
            {PRIORITIES.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
          <button className="pm-action-btn" disabled={busy === "create"} onClick={createNewTicket}>
            Create
          </button>
        </div>
      </div>

      {project.tickets.length === 0 ? (
        <p className="pm-muted-metadata">No tickets yet for this project.</p>
      ) : (
        project.tickets.map((ticket) => (
          <div key={ticket.id} className="pm-card pm-card-block">
            <div className="pm-flex-between">
              <strong>{ticket.title}</strong>
              <span className="pm-muted-metadata">{ticket.priority}</span>
            </div>
            <p>{ticket.description || "No description"}</p>
            <p className="pm-muted-metadata">
              State: {ticket.state} | Owner: {ticket.owner || "unassigned"} | Scope: {ticket.scope_label}
            </p>
            <div className="pm-action-row">
              {STATES.map((state) => (
                <button
                  key={state}
                  className="pm-action-btn secondary"
                  disabled={busy === ticket.id || ticket.state === state}
                  onClick={() => setState(ticket.id, state)}
                >
                  {state}
                </button>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

