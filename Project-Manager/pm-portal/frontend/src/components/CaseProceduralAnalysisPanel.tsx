import React, { useEffect, useMemo, useState } from "react";
import {
  bootstrapIncidentCaseTemplate,
  createCaseProceduralAction,
  createCaseProceduralTimelineEvent,
  fetchCaseProceduralActions,
  fetchCaseProceduralTimeline,
} from "../api";
import type { CaseActionItem, CaseTimelineEvent, ProjectReadiness } from "../types";

export function CaseProceduralAnalysisPanel({
  project,
}: {
  project: ProjectReadiness;
}) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [events, setEvents] = useState<CaseTimelineEvent[]>([]);
  const [actions, setActions] = useState<CaseActionItem[]>([]);
  const [eventForm, setEventForm] = useState({
    event_date: "",
    stage: "incident" as CaseTimelineEvent["stage"],
    title: "",
    summary: "",
    actor: "",
    source_reference: "",
    evidence_status: "missing" as CaseTimelineEvent["evidence_status"],
    procedural_status: "unknown" as CaseTimelineEvent["procedural_status"],
    legal_significance: "",
  });
  const [actionForm, setActionForm] = useState({
    title: "",
    objective: "",
    priority: "high" as CaseActionItem["priority"],
    due_date: "",
    owner: "Melissa Stock",
    evidence_required: "",
    related_timeline_event_id: "",
    notes: "",
  });

  async function loadData() {
    const [timelineRows, actionRows] = await Promise.all([
      fetchCaseProceduralTimeline(project.project.name),
      fetchCaseProceduralActions(project.project.name),
    ]);
    setEvents(timelineRows);
    setActions(actionRows);
  }

  useEffect(() => {
    loadData().catch((err) => setError((err as Error).message));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [project.project.name]);

  const evidenceGapCount = useMemo(
    () => events.filter((e) => e.evidence_status === "missing" || e.procedural_status === "potential_issue").length,
    [events]
  );

  async function addEvent() {
    try {
      setBusy(true);
      setError("");
      await createCaseProceduralTimelineEvent({
        project: project.project.name,
        event_date: eventForm.event_date,
        stage: eventForm.stage,
        title: eventForm.title,
        summary: eventForm.summary,
        actor: eventForm.actor,
        source_reference: eventForm.source_reference,
        evidence_status: eventForm.evidence_status,
        procedural_status: eventForm.procedural_status,
        legal_significance: eventForm.legal_significance,
      });
      setEventForm((prev) => ({ ...prev, title: "", summary: "", source_reference: "", legal_significance: "" }));
      await loadData();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function addAction() {
    try {
      setBusy(true);
      setError("");
      await createCaseProceduralAction({
        project: project.project.name,
        title: actionForm.title,
        objective: actionForm.objective,
        priority: actionForm.priority,
        due_date: actionForm.due_date,
        owner: actionForm.owner,
        evidence_required: actionForm.evidence_required
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        related_timeline_event_id: actionForm.related_timeline_event_id,
        notes: actionForm.notes,
      });
      setActionForm((prev) => ({ ...prev, title: "", objective: "", evidence_required: "", notes: "" }));
      await loadData();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <h3 className="pm-section-title pm-section-title-spaced">Procedural Timeline and Action Plan</h3>
      <p className="pm-subtitle">
        Evidence-first case analysis: document what happened from incident through charging, flag procedural gaps, and create action-oriented next steps before plea-stage decisions.
      </p>
      {error ? <p className="pm-error">{error}</p> : null}
      <div className="pm-card pm-card-block">
        <div className="pm-meta-label">Case posture snapshot</div>
        <p className="pm-muted-metadata">
          Timeline events: {events.length} | Open action items: {actions.filter((a) => a.status !== "done").length} | Evidence/procedural gaps: {evidenceGapCount}
        </p>
        <div className="pm-action-row">
          <button
            className="pm-action-btn secondary"
            disabled={busy}
            onClick={async () => {
              try {
                setBusy(true);
                setError("");
                const result = await bootstrapIncidentCaseTemplate({
                  project: project.project.name,
                  loaded_by: "Melissa Stock",
                  overwrite_existing: false,
                });
                if (!result.ok && result.detail) {
                  setError(result.detail);
                }
                await loadData();
              } catch (err) {
                setError((err as Error).message);
              } finally {
                setBusy(false);
              }
            }}
          >
            Load Incident-to-Charges Starter Template
          </button>
        </div>
      </div>

      <div className="pm-card pm-card-block">
        <div className="pm-meta-label">Add procedural timeline event</div>
        <div className="pm-action-row">
          <input className="pm-input" type="date" value={eventForm.event_date} onChange={(e) => setEventForm((p) => ({ ...p, event_date: e.target.value }))} />
          <select className="pm-input" value={eventForm.stage} onChange={(e) => setEventForm((p) => ({ ...p, stage: e.target.value as CaseTimelineEvent["stage"] }))}>
            <option value="incident">incident</option>
            <option value="investigation">investigation</option>
            <option value="charging">charging</option>
            <option value="pretrial">pretrial</option>
            <option value="plea">plea</option>
            <option value="trial">trial</option>
            <option value="post_disposition">post disposition</option>
            <option value="other">other</option>
          </select>
          <input className="pm-input" placeholder="Event title" value={eventForm.title} onChange={(e) => setEventForm((p) => ({ ...p, title: e.target.value }))} />
        </div>
        <textarea className="pm-input pm-textarea" placeholder="What happened? Include key facts only." value={eventForm.summary} onChange={(e) => setEventForm((p) => ({ ...p, summary: e.target.value }))} />
        <div className="pm-action-row">
          <input className="pm-input" placeholder="Actor (officer, investigator, prosecutor, witness)" value={eventForm.actor} onChange={(e) => setEventForm((p) => ({ ...p, actor: e.target.value }))} />
          <input className="pm-input" placeholder="Source reference (doc ID, filing, bodycam file)" value={eventForm.source_reference} onChange={(e) => setEventForm((p) => ({ ...p, source_reference: e.target.value }))} />
        </div>
        <div className="pm-action-row">
          <select className="pm-input" value={eventForm.evidence_status} onChange={(e) => setEventForm((p) => ({ ...p, evidence_status: e.target.value as CaseTimelineEvent["evidence_status"] }))}>
            <option value="supported">evidence supported</option>
            <option value="conflicted">evidence conflicted</option>
            <option value="missing">evidence missing</option>
          </select>
          <select className="pm-input" value={eventForm.procedural_status} onChange={(e) => setEventForm((p) => ({ ...p, procedural_status: e.target.value as CaseTimelineEvent["procedural_status"] }))}>
            <option value="compliant">procedurally compliant</option>
            <option value="potential_issue">potential procedural issue</option>
            <option value="unknown">procedural status unknown</option>
          </select>
        </div>
        <textarea className="pm-input pm-textarea" placeholder="Legal significance and why this event matters" value={eventForm.legal_significance} onChange={(e) => setEventForm((p) => ({ ...p, legal_significance: e.target.value }))} />
        <button className="pm-action-btn" disabled={busy} onClick={addEvent}>Add Timeline Event</button>
      </div>

      <div className="pm-card pm-card-block">
        <div className="pm-meta-label">Action-oriented next step</div>
        <div className="pm-action-row">
          <input className="pm-input" placeholder="Action title" value={actionForm.title} onChange={(e) => setActionForm((p) => ({ ...p, title: e.target.value }))} />
          <select className="pm-input" value={actionForm.priority} onChange={(e) => setActionForm((p) => ({ ...p, priority: e.target.value as CaseActionItem["priority"] }))}>
            <option value="urgent">urgent</option>
            <option value="high">high</option>
            <option value="normal">normal</option>
          </select>
          <input className="pm-input" type="date" value={actionForm.due_date} onChange={(e) => setActionForm((p) => ({ ...p, due_date: e.target.value }))} />
        </div>
        <textarea className="pm-input pm-textarea" placeholder="Objective (what legal/procedural outcome this supports)" value={actionForm.objective} onChange={(e) => setActionForm((p) => ({ ...p, objective: e.target.value }))} />
        <div className="pm-action-row">
          <input className="pm-input" placeholder="Owner" value={actionForm.owner} onChange={(e) => setActionForm((p) => ({ ...p, owner: e.target.value }))} />
          <select className="pm-input" value={actionForm.related_timeline_event_id} onChange={(e) => setActionForm((p) => ({ ...p, related_timeline_event_id: e.target.value }))}>
            <option value="">Related timeline event (optional)</option>
            {events.map((event) => (
              <option key={event.id} value={event.id}>
                {event.event_date || "date?"} - {event.title}
              </option>
            ))}
          </select>
        </div>
        <input className="pm-input" placeholder="Evidence required (comma-separated)" value={actionForm.evidence_required} onChange={(e) => setActionForm((p) => ({ ...p, evidence_required: e.target.value }))} />
        <textarea className="pm-input pm-textarea" placeholder="Notes and constraints" value={actionForm.notes} onChange={(e) => setActionForm((p) => ({ ...p, notes: e.target.value }))} />
        <button className="pm-action-btn" disabled={busy} onClick={addAction}>Add Action Item</button>
      </div>

      <div className="pm-card pm-card-block">
        <div className="pm-meta-label">Timeline events</div>
        {events.length === 0 ? (
          <p className="pm-muted-metadata">No procedural events recorded yet.</p>
        ) : (
          events.map((event) => (
            <div key={event.id} className="pm-card pm-card-block">
              <p>
                <strong>{event.event_date || "date n/a"} - {event.title}</strong> ({event.stage})
              </p>
              <p className="pm-muted-metadata">
                Evidence: {event.evidence_status} | Procedure: {event.procedural_status} | Actor: {event.actor || "n/a"}
              </p>
              <p className="pm-muted-metadata">
                Source: {event.source_reference || "n/a"}
              </p>
              <p className="pm-muted-metadata">{event.legal_significance || event.summary || "No details provided."}</p>
            </div>
          ))
        )}
      </div>

      <div className="pm-card pm-card-block">
        <div className="pm-meta-label">Action queue</div>
        {actions.length === 0 ? (
          <p className="pm-muted-metadata">No action items yet.</p>
        ) : (
          actions.map((action) => (
            <div key={action.id} className="pm-card pm-card-block">
              <p>
                <strong>{action.title}</strong> ({action.priority}) - {action.status}
              </p>
              <p className="pm-muted-metadata">
                Owner: {action.owner || "n/a"} | Due: {action.due_date || "n/a"}
              </p>
              <p className="pm-muted-metadata">{action.objective}</p>
              <p className="pm-muted-metadata">Evidence needed: {(action.evidence_required || []).join(", ") || "none listed"}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
