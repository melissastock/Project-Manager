import type {
  AgreementChangeOrder,
  AgreementMessage,
  ClientAgreement,
  DecisionState,
  GovernanceRunSummary,
  ProjectReadiness,
  StandupRun,
  TeamAssignment,
  Ticket,
  LaborEstimate,
  SecureVaultFile,
} from "./types";
import {
  type AddScopesRequest,
  type AddScopesResponse,
  type AuditResponse,
  auditResponseSchema,
  type ConnectGoogleRequest,
  type ConnectGoogleResponse,
  connectGoogleResponseSchema,
  type OauthCallbackRequest,
  type OauthCallbackResponse,
  oauthCallbackResponseSchema,
  type RevokeIntegrationRequest,
  type RevokeIntegrationResponse,
  revokeIntegrationResponseSchema,
  type TriggerSyncRequest,
  type TriggerSyncResponse,
  triggerSyncResponseSchema,
} from "./integrationsContracts";
import {
  changeOrderCreateSchema,
  clientAgreementCreateSchema,
  clientAgreementUpdateSchema,
  agreementMessageCreateSchema,
} from "./clientAgreementContracts";

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

export async function createClientAgreement(payload: {
  project: string;
  client_name: string;
  package_name: string;
  product_brief: string;
  scope_definition: string;
  deliverables_summary: string;
  pricing_model: "fixed" | "package" | "retainer" | "mixed";
  price_terms_json: Record<string, unknown>;
  owner_role: string;
  neuro_worker_type: string;
  intake: {
    client_goals: string;
    success_criteria: string;
    constraints: string;
    dependencies: string;
    primary_contact: string;
    communication_preferences: string;
    required_assets: string[];
    completed: boolean;
    completed_at: string | null;
  };
  deliverables: Array<{
    id?: string;
    title: string;
    description: string;
    due_date: string;
    acceptance_criteria: string;
  }>;
}): Promise<ClientAgreement> {
  const safePayload = clientAgreementCreateSchema.parse(payload);
  const response = await fetch(`${API_BASE}/api/client-agreements`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(safePayload),
  });
  if (!response.ok) throw new Error("Failed to create client agreement");
  const json = await response.json();
  return json.agreement as ClientAgreement;
}

export async function updateClientAgreement(agreementId: string, payload: Record<string, unknown>): Promise<ClientAgreement> {
  const safePayload = clientAgreementUpdateSchema.parse(payload);
  const response = await fetch(`${API_BASE}/api/client-agreements/${agreementId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(safePayload),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Failed to update client agreement");
  }
  const json = await response.json();
  return json.agreement as ClientAgreement;
}

export async function completeIntakeAndLock(agreementId: string, payload: { completed_by: string; actor_role: string; lock_reason: string; }): Promise<ClientAgreement> {
  const response = await fetch(`${API_BASE}/api/client-agreements/${agreementId}/intake-complete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Failed to complete intake and lock");
  }
  const json = await response.json();
  return json.agreement as ClientAgreement;
}

export async function fetchAgreementMessages(agreementId: string): Promise<AgreementMessage[]> {
  const response = await fetch(`${API_BASE}/api/client-agreements/${agreementId}/messages`);
  if (!response.ok) throw new Error("Failed to load agreement messages");
  const json = await response.json();
  return (json.messages ?? []) as AgreementMessage[];
}

export async function createAgreementMessage(
  agreementId: string,
  payload: { author_name: string; author_role: string; message: string; visibility: "client_and_team" | "internal_only"; }
): Promise<AgreementMessage> {
  const safePayload = agreementMessageCreateSchema.parse(payload);
  const response = await fetch(`${API_BASE}/api/client-agreements/${agreementId}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(safePayload),
  });
  if (!response.ok) throw new Error("Failed to send agreement message");
  const json = await response.json();
  return json.message as AgreementMessage;
}

export async function fetchAgreementChangeOrders(agreementId: string): Promise<AgreementChangeOrder[]> {
  const response = await fetch(`${API_BASE}/api/client-agreements/${agreementId}/change-orders`);
  if (!response.ok) throw new Error("Failed to load change orders");
  const json = await response.json();
  return (json.change_orders ?? []) as AgreementChangeOrder[];
}

export async function createAgreementChangeOrder(
  agreementId: string,
  payload: { requested_by: string; requested_scope_delta: string; requested_price_delta: string; requested_timeline_delta: string; }
): Promise<AgreementChangeOrder> {
  const safePayload = changeOrderCreateSchema.parse(payload);
  const response = await fetch(`${API_BASE}/api/client-agreements/${agreementId}/change-orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(safePayload),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Failed to create change order");
  }
  const json = await response.json();
  return json.change_order as AgreementChangeOrder;
}

export async function decideAgreementChangeOrder(
  agreementId: string,
  changeOrderId: string,
  payload: { approver: string; actor_role: string; status: "approved" | "rejected" | "implemented"; decision_note: string; }
): Promise<AgreementChangeOrder> {
  const response = await fetch(`${API_BASE}/api/client-agreements/${agreementId}/change-orders/${changeOrderId}/decision`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to update change order decision");
  const json = await response.json();
  return json.change_order as AgreementChangeOrder;
}

export async function fetchAgreementAudit(agreementId: string): Promise<Array<Record<string, unknown>>> {
  const response = await fetch(`${API_BASE}/api/client-agreements/${agreementId}/audit`);
  if (!response.ok) throw new Error("Failed to load agreement audit");
  const json = await response.json();
  return (json.events ?? []) as Array<Record<string, unknown>>;
}

export async function createLaborEstimate(payload: {
  project: string;
  hourly_rate_usd: number;
  confidence: "low" | "medium" | "high";
  assumptions: string[];
  created_by: string;
  modules: Array<{
    module_key: "strategy" | "development" | "operationalization" | "governance" | "marketing" | "gtm";
    estimated_hours: number;
    notes: string;
    subcomponents: string[];
  }>;
  non_labor_costs: Array<{
    category: "hosting" | "storage" | "third_party_tools" | "security_compliance" | "operations_support" | "contingency" | "other";
    one_time_usd: number;
    monthly_recurring_usd: number;
    usage_variable_monthly_usd: number;
    notes: string;
  }>;
}): Promise<LaborEstimate> {
  const response = await fetch(`${API_BASE}/api/labor-estimates`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to create labor estimate");
  const json = await response.json();
  return json.labor_estimate as LaborEstimate;
}

export async function createSecureVaultFile(payload: {
  project: string;
  client_name: string;
  file_name: string;
  storage_uri: string;
  data_class: "ip_invention" | "financial" | "legal" | "medical" | "regulated" | "other";
  sensitivity_level: "restricted" | "highly_restricted";
  encryption_status: "encrypted_at_rest" | "encrypted_at_rest_and_transport";
  retention_policy: string;
  access_roles: string[];
  checksum_sha256: string;
  uploaded_by: string;
  notes: string;
}): Promise<SecureVaultFile> {
  const response = await fetch(`${API_BASE}/api/secure-vault/files`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to register secure vault file");
  const json = await response.json();
  return json.secure_vault_file as SecureVaultFile;
}

export async function getSecureVaultSignedUploadUrl(
  vaultFileId: string,
  payload: { actor_name: string; actor_role: string; expires_in_seconds?: number }
): Promise<Record<string, unknown>> {
  const response = await fetch(`${API_BASE}/api/secure-vault/files/${vaultFileId}/signed-upload-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to create signed upload URL");
  return (await response.json()) as Record<string, unknown>;
}

export async function getSecureVaultSignedDownloadUrl(
  vaultFileId: string,
  payload: { actor_name: string; actor_role: string; expires_in_seconds?: number }
): Promise<Record<string, unknown>> {
  const response = await fetch(`${API_BASE}/api/secure-vault/files/${vaultFileId}/signed-download-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to create signed download URL");
  return (await response.json()) as Record<string, unknown>;
}

export async function fetchSecureVaultAudit(vaultFileId: string): Promise<Array<Record<string, unknown>>> {
  const response = await fetch(`${API_BASE}/api/secure-vault/files/${vaultFileId}/audit`);
  if (!response.ok) throw new Error("Failed to load secure vault audit");
  const json = await response.json();
  return (json.events ?? []) as Array<Record<string, unknown>>;
}

export async function verifySecureVaultChecksum(
  vaultFileId: string,
  payload: { actor_name: string; actor_role: string; expected_checksum_sha256: string }
): Promise<SecureVaultFile> {
  const response = await fetch(`${API_BASE}/api/secure-vault/files/${vaultFileId}/verify-checksum`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to verify checksum");
  const json = await response.json();
  return json.secure_vault_file as SecureVaultFile;
}

export async function startGoogleConnect(payload: ConnectGoogleRequest): Promise<ConnectGoogleResponse> {
  const response = await fetch(`${API_BASE}/integrations/google/connect`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to start Google OAuth flow");
  return connectGoogleResponseSchema.parse(await response.json());
}

export async function completeGoogleCallback(payload: OauthCallbackRequest): Promise<OauthCallbackResponse> {
  const response = await fetch(`${API_BASE}/integrations/google/callback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to exchange OAuth callback");
  return oauthCallbackResponseSchema.parse(await response.json());
}

export async function requestAdditionalScopes(integrationId: string, payload: AddScopesRequest): Promise<AddScopesResponse> {
  const response = await fetch(`${API_BASE}/integrations/${integrationId}/scopes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to request additional scopes");
  return connectGoogleResponseSchema.parse(await response.json());
}

export async function revokeIntegration(integrationId: string, payload: RevokeIntegrationRequest): Promise<RevokeIntegrationResponse> {
  const response = await fetch(`${API_BASE}/integrations/${integrationId}/revoke`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to revoke integration");
  return revokeIntegrationResponseSchema.parse(await response.json());
}

export async function triggerIntegrationSync(integrationId: string, payload: TriggerSyncRequest): Promise<TriggerSyncResponse> {
  const response = await fetch(`${API_BASE}/integrations/${integrationId}/sync`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to queue integration sync");
  return triggerSyncResponseSchema.parse(await response.json());
}

export async function fetchIntegrationAudit(integrationId: string, limit = 50, cursor?: string | null): Promise<AuditResponse> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (cursor) params.set("cursor", cursor);
  const response = await fetch(`${API_BASE}/integrations/${integrationId}/audit?${params.toString()}`);
  if (!response.ok) throw new Error("Failed to load integration audit");
  return auditResponseSchema.parse(await response.json());
}
