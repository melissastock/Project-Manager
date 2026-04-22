import React, { useEffect, useState } from "react";
import {
  connectSecureVaultDrive,
  createSecureVaultFile,
  disconnectSecureVaultDrive,
  fetchSecureVaultDriveConnection,
  fetchSecureVaultAudit,
  getSecureVaultSignedDownloadUrl,
  getSecureVaultSignedUploadUrl,
  verifySecureVaultChecksum,
} from "../api";
import type { ProjectReadiness } from "../types";

export function SecureVaultPanel({ project, onRefresh }: { project: ProjectReadiness; onRefresh: () => Promise<void> }) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [signedUrlOutput, setSignedUrlOutput] = useState("");
  const [auditOutput, setAuditOutput] = useState("");
  const [expectedChecksumByFile, setExpectedChecksumByFile] = useState<Record<string, string>>({});
  const [driveStatus, setDriveStatus] = useState<null | {
    status: "connected" | "disconnected";
    drive_account_email: string;
    drive_folder_id: string;
    connected_at: string;
    updated_at: string;
  }>(null);
  const [driveForm, setDriveForm] = useState({
    drive_account_email: "",
    drive_folder_id: "",
    notes: "",
  });
  const [form, setForm] = useState({
    client_name: "",
    file_name: "",
    storage_uri: "",
    input_source: "local_upload" as "google_drive" | "vault" | "local_upload",
    file_category: "other" as "incident_record" | "investigation_record" | "charging_record" | "court_filing" | "correspondence" | "media" | "financial" | "medical" | "other",
    procedural_stage: "other" as "incident" | "investigation" | "charging" | "pretrial" | "plea" | "trial" | "post_disposition" | "other",
    usage_goal: "",
    source_reference: "",
    data_class: "other" as "ip_invention" | "financial" | "legal" | "medical" | "regulated" | "other",
    sensitivity_level: "restricted" as "restricted" | "highly_restricted",
    retention_policy: "retain-until-client-request-or-policy-expiry",
    access_roles: "business_owner,portfolio_owner,technical_owner",
    checksum_sha256: "",
    uploaded_by: "Melissa Stock",
    notes: "",
  });

  useEffect(() => {
    let active = true;
    async function loadDrive() {
      try {
        const connection = await fetchSecureVaultDriveConnection(project.project.name);
        if (!active) return;
        if (!connection) {
          setDriveStatus(null);
          return;
        }
        setDriveStatus({
          status: connection.status,
          drive_account_email: connection.drive_account_email,
          drive_folder_id: connection.drive_folder_id,
          connected_at: connection.connected_at,
          updated_at: connection.updated_at,
        });
      } catch {
        if (active) setDriveStatus(null);
      }
    }
    loadDrive();
    return () => {
      active = false;
    };
  }, [project.project.name]);

  async function registerFile() {
    if (!form.file_name.trim()) return;
    try {
      setBusy(true);
      setError("");
      await createSecureVaultFile({
        project: project.project.name,
        client_name: form.client_name,
        file_name: form.file_name,
        storage_uri: form.storage_uri,
        input_source: form.input_source,
        file_category: form.file_category,
        procedural_stage: form.procedural_stage,
        usage_goal: form.usage_goal,
        source_reference: form.source_reference,
        data_class: form.data_class,
        sensitivity_level: form.sensitivity_level,
        encryption_status: "encrypted_at_rest_and_transport",
        retention_policy: form.retention_policy,
        access_roles: form.access_roles.split(",").map((x) => x.trim()).filter(Boolean),
        checksum_sha256: form.checksum_sha256,
        uploaded_by: form.uploaded_by,
        notes: form.notes,
      });
      setForm((prev) => ({
        ...prev,
        file_name: "",
        storage_uri: "",
        source_reference: "",
        checksum_sha256: "",
        notes: "",
      }));
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function issueSignedUrl(vaultFileId: string, direction: "upload" | "download") {
    try {
      setBusy(true);
      setError("");
      const payload = { actor_name: form.uploaded_by || "portal-user", actor_role: "business_owner", expires_in_seconds: 900 };
      const result =
        direction === "upload"
          ? await getSecureVaultSignedUploadUrl(vaultFileId, payload)
          : await getSecureVaultSignedDownloadUrl(vaultFileId, payload);
      setSignedUrlOutput(JSON.stringify(result, null, 2));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function uploadFileDirect(vaultFileId: string, file: File) {
    try {
      setBusy(true);
      setError("");
      const payload = { actor_name: form.uploaded_by || "portal-user", actor_role: "business_owner", expires_in_seconds: 900 };
      const result = await getSecureVaultSignedUploadUrl(vaultFileId, payload);
      const signedUpload = (result.signed_upload ?? {}) as Record<string, unknown>;
      const uploadPath = String(result.storage_path ?? "");
      const signedUrl =
        String(signedUpload.signedURL ?? signedUpload.signedUrl ?? signedUpload.url ?? "");
      const token = String(signedUpload.token ?? "");
      if (!signedUrl) {
        throw new Error("Signed upload URL not returned by backend.");
      }
      const headers: Record<string, string> = {};
      if (token) headers.authorization = `Bearer ${token}`;
      const response = await fetch(signedUrl, {
        method: "PUT",
        body: file,
        headers,
      });
      if (!response.ok) throw new Error("Direct upload failed.");
      setSignedUrlOutput(JSON.stringify({ uploadPath, signedUpload }, null, 2));
      await onRefresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function downloadFileDirect(vaultFileId: string) {
    try {
      setBusy(true);
      setError("");
      const payload = { actor_name: form.uploaded_by || "portal-user", actor_role: "business_owner", expires_in_seconds: 900 };
      const result = await getSecureVaultSignedDownloadUrl(vaultFileId, payload);
      const signedDownload = (result.signed_download ?? {}) as Record<string, unknown>;
      const signedUrl = String(signedDownload.signedURL ?? signedDownload.signedUrl ?? signedDownload.url ?? "");
      if (!signedUrl) throw new Error("Signed download URL not returned by backend.");
      window.open(signedUrl, "_blank", "noopener,noreferrer");
      setSignedUrlOutput(JSON.stringify(result, null, 2));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function verifyChecksum(vaultFileId: string) {
    try {
      setBusy(true);
      setError("");
      const expected = expectedChecksumByFile[vaultFileId] || "";
      if (!expected.trim()) throw new Error("Enter expected checksum before verifying.");
      await verifySecureVaultChecksum(vaultFileId, {
        actor_name: form.uploaded_by || "portal-user",
        actor_role: "business_owner",
        expected_checksum_sha256: expected.trim(),
      });
      await onRefresh();
      await loadAudit(vaultFileId);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function loadAudit(vaultFileId: string) {
    try {
      setBusy(true);
      setError("");
      const events = await fetchSecureVaultAudit(vaultFileId);
      setAuditOutput(JSON.stringify(events, null, 2));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function connectDrive() {
    try {
      setBusy(true);
      setError("");
      const connection = await connectSecureVaultDrive({
        project: project.project.name,
        connected_by: form.uploaded_by || "portal-user",
        actor_role: "business_owner",
        drive_account_email: driveForm.drive_account_email.trim(),
        drive_folder_id: driveForm.drive_folder_id.trim(),
        notes: driveForm.notes.trim(),
      });
      setDriveStatus({
        status: connection.status,
        drive_account_email: connection.drive_account_email,
        drive_folder_id: connection.drive_folder_id,
        connected_at: connection.connected_at,
        updated_at: connection.updated_at,
      });
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function disconnectDrive() {
    try {
      setBusy(true);
      setError("");
      const connection = await disconnectSecureVaultDrive({
        project: project.project.name,
        disconnected_by: form.uploaded_by || "portal-user",
        actor_role: "business_owner",
        reason: "manual disconnect from portal",
      });
      setDriveStatus({
        status: connection.status,
        drive_account_email: connection.drive_account_email,
        drive_folder_id: connection.drive_folder_id,
        connected_at: connection.connected_at,
        updated_at: connection.updated_at,
      });
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <h3 className="pm-section-title pm-section-title-spaced">Secure Client Vault</h3>
      <p className="pm-subtitle">
        Secure file handling for privileged or sensitive client records (IP, legal, financial, medical, and regulated materials).
      </p>
      {error ? <p className="pm-error">{error}</p> : null}
      <div className="pm-card pm-card-block">
        <div className="pm-meta-label">Google Drive Connection</div>
        <p className="pm-muted-metadata">
          Status: {driveStatus?.status ?? "not connected"}
          {driveStatus?.drive_account_email ? ` | Account: ${driveStatus.drive_account_email}` : ""}
          {driveStatus?.drive_folder_id ? ` | Folder: ${driveStatus.drive_folder_id}` : ""}
        </p>
        <p className="pm-muted-metadata">
          Connect the approved client Drive destination once per project so files are routed to the correct legal archive location.
        </p>
        <div className="pm-action-row">
          <input
            className="pm-input"
            placeholder="Drive account email"
            value={driveForm.drive_account_email}
            onChange={(e) => setDriveForm((p) => ({ ...p, drive_account_email: e.target.value }))}
          />
          <input
            className="pm-input"
            placeholder="Drive folder ID (approved legal folder)"
            value={driveForm.drive_folder_id}
            onChange={(e) => setDriveForm((p) => ({ ...p, drive_folder_id: e.target.value }))}
          />
        </div>
        <div className="pm-action-row">
          <input
            className="pm-input"
            placeholder="Connection notes (optional, visible in audit context)"
            value={driveForm.notes}
            onChange={(e) => setDriveForm((p) => ({ ...p, notes: e.target.value }))}
          />
          <button className="pm-action-btn secondary" disabled={busy} onClick={connectDrive}>
            Connect Drive Folder
          </button>
          <button className="pm-action-btn secondary" disabled={busy} onClick={disconnectDrive}>
            Disconnect Drive Folder
          </button>
        </div>
      </div>
      <div className="pm-card pm-card-block">
        <p className="pm-muted-metadata">
          Step 1: register the file metadata. Step 2: upload. Step 3: verify checksum and review audit log.
        </p>
        <div className="pm-action-row">
          <input className="pm-input" placeholder="Client name" value={form.client_name} onChange={(e) => setForm((p) => ({ ...p, client_name: e.target.value }))} />
          <input className="pm-input" placeholder="File name with extension (e.g., Engagement-Letter.pdf)" value={form.file_name} onChange={(e) => setForm((p) => ({ ...p, file_name: e.target.value }))} />
        </div>
        <div className="pm-action-row">
          <select className="pm-input" value={form.input_source} onChange={(e) => setForm((p) => ({ ...p, input_source: e.target.value as typeof form.input_source }))}>
            <option value="local_upload">Source: local upload</option>
            <option value="google_drive">Source: Google Drive</option>
            <option value="vault">Source: existing vault transfer</option>
          </select>
          <select className="pm-input" value={form.procedural_stage} onChange={(e) => setForm((p) => ({ ...p, procedural_stage: e.target.value as typeof form.procedural_stage }))}>
            <option value="incident">Stage: incident</option>
            <option value="investigation">Stage: investigation</option>
            <option value="charging">Stage: charging</option>
            <option value="pretrial">Stage: pretrial</option>
            <option value="plea">Stage: plea</option>
            <option value="trial">Stage: trial</option>
            <option value="post_disposition">Stage: post disposition</option>
            <option value="other">Stage: other</option>
          </select>
          <select className="pm-input" value={form.file_category} onChange={(e) => setForm((p) => ({ ...p, file_category: e.target.value as typeof form.file_category }))}>
            <option value="incident_record">Category: incident record</option>
            <option value="investigation_record">Category: investigation record</option>
            <option value="charging_record">Category: charging record</option>
            <option value="court_filing">Category: court filing</option>
            <option value="correspondence">Category: correspondence</option>
            <option value="media">Category: media</option>
            <option value="financial">Category: financial</option>
            <option value="medical">Category: medical</option>
            <option value="other">Category: other</option>
          </select>
        </div>
        <div className="pm-action-row">
          <input className="pm-input" placeholder="Usage goal (e.g., procedural timeline review, charging challenge)" value={form.usage_goal} onChange={(e) => setForm((p) => ({ ...p, usage_goal: e.target.value }))} />
          <input className="pm-input" placeholder="Source reference (Drive link ID, vault ref, local note)" value={form.source_reference} onChange={(e) => setForm((p) => ({ ...p, source_reference: e.target.value }))} />
        </div>
        <div className="pm-action-row">
          <input className="pm-input" placeholder="Secure storage path (optional; auto-generated if blank)" value={form.storage_uri} onChange={(e) => setForm((p) => ({ ...p, storage_uri: e.target.value }))} />
          <select className="pm-input" value={form.data_class} onChange={(e) => setForm((p) => ({ ...p, data_class: e.target.value as typeof form.data_class }))}>
            <option value="ip_invention">IP / invention</option>
            <option value="financial">financial</option>
            <option value="legal">legal</option>
            <option value="medical">medical</option>
            <option value="regulated">regulated</option>
            <option value="other">other</option>
          </select>
          <select className="pm-input" value={form.sensitivity_level} onChange={(e) => setForm((p) => ({ ...p, sensitivity_level: e.target.value as typeof form.sensitivity_level }))}>
            <option value="restricted">restricted</option>
            <option value="highly_restricted">highly restricted</option>
          </select>
        </div>
        <div className="pm-action-row">
          <input className="pm-input" placeholder="Allowed roles (comma-separated, e.g., business_owner,portfolio_owner)" value={form.access_roles} onChange={(e) => setForm((p) => ({ ...p, access_roles: e.target.value }))} />
          <input className="pm-input" placeholder="SHA256 checksum (optional at registration)" value={form.checksum_sha256} onChange={(e) => setForm((p) => ({ ...p, checksum_sha256: e.target.value }))} />
        </div>
        <textarea className="pm-input pm-textarea" placeholder="Retention policy and legal notes" value={form.notes} onChange={(e) => setForm((p) => ({ ...p, notes: e.target.value }))} />
        <button className="pm-action-btn" disabled={busy} onClick={registerFile}>Register Secure File</button>
      </div>

      {project.secure_vault_files.length === 0 ? (
        <p className="pm-muted-metadata">No secure files registered yet.</p>
      ) : (
        project.secure_vault_files.map((file) => (
          <div key={file.id} className="pm-card pm-card-block">
            <strong>{file.file_name}</strong>
            <p className="pm-muted-metadata">
              Class: {file.data_class} | Sensitivity: {file.sensitivity_level} | Encryption: {file.encryption_status}
            </p>
            <p className="pm-muted-metadata">
              URI: {file.storage_uri || "not set"} | Access: {file.access_roles.join(", ") || "none"}
            </p>
            <p className="pm-muted-metadata">
              Source: {file.input_source} | Stage: {file.procedural_stage} | Category: {file.file_category}
            </p>
            <p className="pm-muted-metadata">
              Retention: {file.retention_policy} | Checksum status: {file.checksum_status} | Goal: {file.usage_goal || "not set"}
            </p>
            <p className="pm-muted-metadata">
              Sorting tags: {(file.sorting_tags ?? []).join(", ") || "none"} | Next action: {file.next_action_hint || "none"}
            </p>
            <div className="pm-action-row">
              <input
                className="pm-input"
                type="file"
                onChange={(e) => {
                  const picked = e.target.files?.[0];
                  if (picked) uploadFileDirect(file.id, picked);
                }}
              />
              <button className="pm-action-btn secondary" disabled={busy} onClick={() => issueSignedUrl(file.id, "upload")}>
                Show Signed Upload Link
              </button>
              <button className="pm-action-btn secondary" disabled={busy} onClick={() => downloadFileDirect(file.id)}>
                Open Secure Download
              </button>
              <button className="pm-action-btn secondary" disabled={busy} onClick={() => loadAudit(file.id)}>
                View Access Audit
              </button>
            </div>
            <div className="pm-action-row">
              <input
                className="pm-input"
                placeholder="Expected SHA256 checksum (from original source file)"
                value={expectedChecksumByFile[file.id] || ""}
                onChange={(e) => setExpectedChecksumByFile((prev) => ({ ...prev, [file.id]: e.target.value }))}
              />
              <button className="pm-action-btn secondary" disabled={busy} onClick={() => verifyChecksum(file.id)}>
                Verify Checksum
              </button>
            </div>
          </div>
        ))
      )}
      {signedUrlOutput ? (
        <div className="pm-card pm-card-block">
          <div className="pm-meta-label">Signed URL payload</div>
          <pre className="pm-muted-metadata">{signedUrlOutput}</pre>
        </div>
      ) : null}
      {auditOutput ? (
        <div className="pm-card pm-card-block">
          <div className="pm-meta-label">Vault audit events</div>
          <pre className="pm-muted-metadata">{auditOutput}</pre>
        </div>
      ) : null}
    </div>
  );
}
