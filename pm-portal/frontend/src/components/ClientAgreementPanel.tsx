import React, { useEffect, useMemo, useState } from "react";
import {
  completeIntakeAndLock,
  createAgreementChangeOrder,
  createAgreementMessage,
  createClientAgreement,
  decideAgreementChangeOrder,
  fetchAgreementAudit,
  fetchAgreementChangeOrders,
  fetchAgreementMessages,
  updateClientAgreement,
} from "../api";
import type { AgreementChangeOrder, AgreementMessage, ClientAgreement, ProjectReadiness } from "../types";

export function ClientAgreementPanel({ project, onRefresh }: { project: ProjectReadiness; onRefresh: () => Promise<void> }) {
  const agreement = useMemo<ClientAgreement | null>(() => project.client_agreements[0] ?? null, [project.client_agreements]);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState<AgreementMessage[]>([]);
  const [changeOrders, setChangeOrders] = useState<AgreementChangeOrder[]>([]);
  const [auditEvents, setAuditEvents] = useState<Array<Record<string, unknown>>>([]);
  const [messageText, setMessageText] = useState("");
  const [changeScope, setChangeScope] = useState("");
  const [changePrice, setChangePrice] = useState("");
  const [changeTimeline, setChangeTimeline] = useState("");
  const [approver, setApprover] = useState("Melissa Stock");
  const [agreementDraft, setAgreementDraft] = useState({
    client_name: "",
    package_name: "",
    product_brief: "",
    scope_definition: "",
    deliverables_summary: "",
    pricing_model: "mixed" as "fixed" | "package" | "retainer" | "mixed",
    price_terms_json: "{\"fixed\":0,\"retainer\":0}",
    client_goals: "",
    success_criteria: "",
    primary_contact: "",
    communication_preferences: "",
    budget_range_usd: "",
    scope_boundaries: "",
    compliance_requirements: "",
    approval_authority: "",
    risk_assumptions: "",
  });

  async function refreshThreadData() {
    if (!agreement) return;
    const [thread, co] = await Promise.all([
      fetchAgreementMessages(agreement.id),
      fetchAgreementChangeOrders(agreement.id),
    ]);
    setMessages(thread);
    setChangeOrders(co);
    setAuditEvents(await fetchAgreementAudit(agreement.id));
  }

  useEffect(() => {
    refreshThreadData().catch(() => undefined);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [agreement?.id]);

  async function createAgreement() {
    try {
      setBusy("create-agreement");
      setError("");
      const parsedTerms = JSON.parse(agreementDraft.price_terms_json || "{}");
      await createClientAgreement({
        project: project.project.name,
        client_name: agreementDraft.client_name,
        package_name: agreementDraft.package_name,
        product_brief: agreementDraft.product_brief,
        scope_definition: agreementDraft.scope_definition,
        deliverables_summary: agreementDraft.deliverables_summary,
        pricing_model: agreementDraft.pricing_model,
        price_terms_json: parsedTerms,
        owner_role: "business_owner",
        neuro_worker_type: "unspecified",
        deliverables: [],
        intake: {
          client_goals: agreementDraft.client_goals,
          success_criteria: agreementDraft.success_criteria,
          primary_contact: agreementDraft.primary_contact,
          communication_preferences: agreementDraft.communication_preferences,
          required_assets: [],
          constraints: "",
          dependencies: "",
          budget_range_usd: agreementDraft.budget_range_usd,
          scope_boundaries: agreementDraft.scope_boundaries,
          compliance_requirements: agreementDraft.compliance_requirements,
          approval_authority: agreementDraft.approval_authority,
          risk_assumptions: agreementDraft.risk_assumptions,
          completed: false,
          completed_at: null,
        },
      });
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function saveAgreementUpdate() {
    if (!agreement) return;
    try {
      setBusy("save-agreement");
      setError("");
      await updateClientAgreement(agreement.id, {
        package_name: agreementDraft.package_name || agreement.package_name,
        product_brief: agreementDraft.product_brief || agreement.product_brief,
        scope_definition: agreementDraft.scope_definition || agreement.scope_definition,
        deliverables_summary: agreementDraft.deliverables_summary || agreement.deliverables_summary,
      });
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function lockAfterIntake() {
    if (!agreement) return;
    try {
      setBusy("lock-agreement");
      setError("");
      await updateClientAgreement(agreement.id, {
        intake: {
          ...agreement.intake,
          completed: true,
          completed_at: new Date().toISOString(),
        },
      });
      await completeIntakeAndLock(agreement.id, {
        completed_by: approver,
        actor_role: "business_owner",
        lock_reason: "intake-complete",
      });
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function sendMessage() {
    if (!agreement || !messageText.trim()) return;
    try {
      setBusy("send-message");
      setError("");
      await createAgreementMessage(agreement.id, {
        author_name: approver || "Team",
        author_role: "team",
        message: messageText.trim(),
        visibility: "client_and_team",
      });
      setMessageText("");
      await refreshThreadData();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function submitChangeOrder() {
    if (!agreement || !changeScope.trim()) return;
    try {
      setBusy("create-change-order");
      setError("");
      await createAgreementChangeOrder(agreement.id, {
        requested_by: approver || "Team",
        requested_scope_delta: changeScope.trim(),
        requested_price_delta: changePrice.trim(),
        requested_timeline_delta: changeTimeline.trim(),
      });
      setChangeScope("");
      setChangePrice("");
      setChangeTimeline("");
      await refreshThreadData();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  async function approveChangeOrder(changeOrderId: string) {
    if (!agreement) return;
    try {
      setBusy(changeOrderId);
      setError("");
      await decideAgreementChangeOrder(agreement.id, changeOrderId, {
        approver: approver || "Business Owner",
        actor_role: "business_owner",
        status: "approved",
        decision_note: "Approved for amendment path.",
      });
      await refreshThreadData();
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(null);
    }
  }

  return (
    <div>
      <h3 className="pm-section-title pm-section-title-spaced">Client Intake and Contract Lock</h3>
      <p className="pm-subtitle">
        Use this section to capture plain-language agreement terms with the client, then lock the agreement so future scope or price changes are tracked through formal change orders.
      </p>
      {error ? <p className="pm-error">{error}</p> : null}
      <div className="pm-card pm-card-block">
        <div className="pm-meta-label">Client and owner</div>
        <div className="pm-action-row">
          <input className="pm-input" placeholder="Client name" value={agreementDraft.client_name} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, client_name: e.target.value }))} />
          <input className="pm-input" placeholder="Business owner name" value={approver} onChange={(e) => setApprover(e.target.value)} />
        </div>
        {!agreement ? (
          <>
            <input className="pm-input" placeholder="Service package or engagement type" value={agreementDraft.package_name} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, package_name: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder="Project overview (what you are hiring us to do)" value={agreementDraft.product_brief} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, product_brief: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder="Scope of work (what is included and excluded)" value={agreementDraft.scope_definition} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, scope_definition: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder="Deliverables (what the client will receive)" value={agreementDraft.deliverables_summary} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, deliverables_summary: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder='Pricing terms (structured JSON), e.g. {"fixed":12000,"retainer":1500}' value={agreementDraft.price_terms_json} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, price_terms_json: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder="Client goals and desired outcomes" value={agreementDraft.client_goals} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, client_goals: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder="Success criteria (how both parties define success)" value={agreementDraft.success_criteria} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, success_criteria: e.target.value }))} />
            <input className="pm-input" placeholder="Primary contact (name and email)" value={agreementDraft.primary_contact} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, primary_contact: e.target.value }))} />
            <input className="pm-input" placeholder="Communication preferences (email, cadence, key participants)" value={agreementDraft.communication_preferences} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, communication_preferences: e.target.value }))} />
            <input className="pm-input" placeholder="Budget range (USD)" value={agreementDraft.budget_range_usd} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, budget_range_usd: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder="Scope boundaries (in scope vs out of scope)" value={agreementDraft.scope_boundaries} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, scope_boundaries: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder="Compliance or legal requirements" value={agreementDraft.compliance_requirements} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, compliance_requirements: e.target.value }))} />
            <input className="pm-input" placeholder="Final approval authority (name/role)" value={agreementDraft.approval_authority} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, approval_authority: e.target.value }))} />
            <textarea className="pm-input pm-textarea" placeholder="Risk assumptions and legal constraints" value={agreementDraft.risk_assumptions} onChange={(e) => setAgreementDraft((prev) => ({ ...prev, risk_assumptions: e.target.value }))} />
            <button className="pm-action-btn" disabled={busy === "create-agreement"} onClick={createAgreement}>Create Agreement</button>
          </>
        ) : (
          <>
            <p className="pm-muted-metadata">
              Status: {agreement.agreement_status} {agreement.is_locked ? `| Locked by ${agreement.locked_by}` : "| Unlocked"}
            </p>
            <p className="pm-muted-metadata">
              Intake ownership split: Client {"->"} goals, success criteria, contact, communication preferences. Business owner {"->"} budget, scope boundaries, compliance, approvals, risk.
            </p>
            {agreement.is_locked ? <p className="pm-meta-label">Agreement is locked after intake completion. Any scope, price, or timeline change must go through a formal change order.</p> : null}
            <textarea className="pm-input pm-textarea" placeholder="Product brief" defaultValue={agreement.product_brief} onBlur={(e) => setAgreementDraft((prev) => ({ ...prev, product_brief: e.target.value }))} disabled={agreement.is_locked} />
            <textarea className="pm-input pm-textarea" placeholder="Scope definition" defaultValue={agreement.scope_definition} onBlur={(e) => setAgreementDraft((prev) => ({ ...prev, scope_definition: e.target.value }))} disabled={agreement.is_locked} />
            <textarea className="pm-input pm-textarea" placeholder="Agreed deliverables" defaultValue={agreement.deliverables_summary} onBlur={(e) => setAgreementDraft((prev) => ({ ...prev, deliverables_summary: e.target.value }))} disabled={agreement.is_locked} />
            {!agreement.is_locked ? (
              <div className="pm-action-row">
                <button className="pm-action-btn secondary" disabled={busy === "save-agreement"} onClick={saveAgreementUpdate}>Save Draft Updates</button>
                <button className="pm-action-btn" disabled={busy === "lock-agreement"} onClick={lockAfterIntake}>Complete Intake and Lock Agreement</button>
              </div>
            ) : null}
          </>
        )}
      </div>

      {agreement ? (
        <>
          <div className="pm-card pm-card-block">
            <div className="pm-meta-label">Client Communication Log</div>
            <div className="pm-action-row">
              <input className="pm-input" placeholder="Message visible to client and legal counsel" value={messageText} onChange={(e) => setMessageText(e.target.value)} />
              <button className="pm-action-btn" disabled={busy === "send-message"} onClick={sendMessage}>Send Message</button>
            </div>
            {messages.length === 0 ? <p className="pm-muted-metadata">No messages yet.</p> : messages.map((msg) => (
              <p key={msg.id} className="pm-muted-metadata">
                [{new Date(msg.created_at).toLocaleString()}] {msg.author_name} ({msg.author_role}): {msg.message}
              </p>
            ))}
          </div>

          <div className="pm-card pm-card-block">
            <div className="pm-meta-label">Formal Change Orders</div>
            {!agreement.is_locked ? (
              <p className="pm-muted-metadata">Change orders become available after the agreement is locked.</p>
            ) : (
              <>
                <textarea className="pm-input pm-textarea" placeholder="Requested scope change (what changes and why)" value={changeScope} onChange={(e) => setChangeScope(e.target.value)} />
                <div className="pm-action-row">
                  <input className="pm-input" placeholder="Pricing impact (USD)" value={changePrice} onChange={(e) => setChangePrice(e.target.value)} />
                  <input className="pm-input" placeholder="Timeline impact (days/weeks)" value={changeTimeline} onChange={(e) => setChangeTimeline(e.target.value)} />
                </div>
                <button className="pm-action-btn" disabled={busy === "create-change-order"} onClick={submitChangeOrder}>Submit Change Order for Approval</button>
              </>
            )}
            {changeOrders.map((co) => (
              <div key={co.id} className="pm-card pm-card-block">
                <p><strong>{co.status.toUpperCase()}</strong> - {co.requested_scope_delta}</p>
                <p className="pm-muted-metadata">Price: {co.requested_price_delta || "n/a"} | Timeline: {co.requested_timeline_delta || "n/a"}</p>
                {co.status === "requested" ? (
                  <button className="pm-action-btn secondary" disabled={busy === co.id} onClick={() => approveChangeOrder(co.id)}>Approve Change Order</button>
                ) : null}
              </div>
            ))}
          </div>

          <div className="pm-card pm-card-block">
            <div className="pm-meta-label">Audit trail (immutable events)</div>
            {auditEvents.length === 0 ? <p className="pm-muted-metadata">No audit events yet.</p> : auditEvents.map((event) => (
              <p key={String(event.id)} className="pm-muted-metadata">
                [{new Date(String(event.created_at)).toLocaleString()}] {String(event.event_type)} by {String(event.actor || "system")} ({String(event.actor_role || "n/a")})
              </p>
            ))}
          </div>
        </>
      ) : null}
    </div>
  );
}
