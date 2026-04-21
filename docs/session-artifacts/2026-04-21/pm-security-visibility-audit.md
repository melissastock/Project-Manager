# PM Security And Visibility Audit

Date: `2026-04-21`
Scope: `Project Manager` control plane and managed GitHub remotes
Method: local git topology audit + `gh api` repository settings checks

---

## 1) Summary Findings

- `P0` **Branch protection gap:** audited GitHub repos show no active branch protection on `main`.
- `P0` **Remote topology risk:** `MJS Financial Dash` backup clone still points to canonical production remote.
- `P1` **Visibility posture mostly private:** audited repos are mostly private, with `mjsds_dashboard` intentionally public.
- `P1` **Secret-scanning visibility inconsistent:** explicit secret scanning status is visible only for public repo; private repo API responses report unknown in this audit context.
- `P1` **Local-only repos remain unmanaged remotely:** multiple managed repos still have no configured remote in local clones.

---

## 2) Evidence Snapshot

### Remote topology (local audit)

- `MJS Financial Dash` -> `https://github.com/melissastock/MJS-Financial-Dash.git`
- `MJS Financial Dash backup 20260310_153810` -> `https://github.com/melissastock/MJS-Financial-Dash.git` (**collision**)
- `Divorce` -> `none` (local repo has no `origin` configured in this workspace)

### GitHub visibility/security (sampled managed remotes)

- Private: `Archiavellian-Archive`, `CIMPT`, `MJS-Financial-Dash`, `app-builder`, `archiavellian`, `home-learning-playbook`, `momentum-os`, `provider-access-hub`, `wayne-strain`
- Public: `mjsds_dashboard`
- Branch protection on `main`: `none` for all audited remotes
- Rulesets endpoint: unavailable/unknown for most private remotes in this audit context
- Secret scanning + push protection: explicitly `enabled` for `mjsds_dashboard`; `unknown` for audited private remotes

---

## 3) Priority Remediation Checklist

## `P0` (today)

1. Enable branch protection (or rulesets) on canonical default branches.
2. Re-point backup/archive remotes away from canonical production remotes.
3. Lock down public exposure to allowlisted PM export artifacts only.

## `P1` (next)

1. Confirm secret scanning + push protection settings for private repos via repo settings UI/organization policy.
2. Add periodic automated topology checks to detect duplicate origin collisions.
3. Add policy checks that fail status generation if critical classification fields are missing.

---

## 4) Risk Register

- **Risk:** accidental force-push or overwrite from backup clones.
  - **Mitigation:** enforce remote separation and deny direct push from backup remotes.
- **Risk:** private client/IP data drift into public PM artifacts.
  - **Mitigation:** allowlist exporter + classification gating + manual approval.
- **Risk:** policy blind spots due to missing metadata.
  - **Mitigation:** require `visibility_tier`, `data_class`, `ip_class`, and `public_sync_allowed` in manifest and intake.

