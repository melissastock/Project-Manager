# Cascade Applicability Matrix

Use this matrix to classify every spine-level change before rollout.

## Scope Labels

| Scope label | Meaning | Typical examples |
| --- | --- | --- |
| `all-repos` | Must be applied across the full managed portfolio. | Secret-handling policy, review-gate requirements, baseline security checks. |
| `selected-lanes` | Applies only to specific portfolio lanes or project classes. | Investor-pack gates for product lanes; archive retention controls for archive lanes. |
| `pm-portal-only` | Applies only to PM Portal backend/frontend/runtime. | Portal API fields, Supabase portal tables, portal UI branding/theme updates. |

## Decision Rules (in order)

1. **Runtime boundary check**  
   If the change touches only `pm-portal/` runtime behavior or schema, classify `pm-portal-only`.
2. **Policy intent check**  
   If the change is governance/security baseline intended for all managed repos, classify `all-repos`.
3. **Lane relevance check**  
   If the change depends on lane purpose (for example `archive-incubator` vs `platform-product`), classify `selected-lanes`.
4. **Evidence requirement**  
   Record the chosen scope in handoff/addendum notes and list affected repos or lanes explicitly.

## Lane Mapping Template (`selected-lanes`)

When using `selected-lanes`, include this block in the handoff/addendum:

```md
Scope: selected-lanes
Lanes: recovery-core, platform-product
Excluded lanes: archive-incubator, family-outcomes
Reason: <why this policy/change is lane-specific>
```

## Rollout Checklist By Scope

### `all-repos`

- Update spine docs/scripts first.
- Run portfolio sweep (`portfolio_status`, remote collision, review gate).
- Verify every managed repo reflects required artifact/policy state.

### `selected-lanes`

- Name included lanes and exclusions.
- Verify only in-scope repos receive changes.
- Confirm excluded lanes are intentionally unchanged.

### `pm-portal-only`

- Apply changes under `pm-portal/` only.
- Confirm no unintended child-repo cascade.
- Validate backend/frontend build and Supabase behavior where applicable.

## Anti-Drift Guardrails

- Do not infer “all repos” from urgency alone.
- Do not infer “pm-portal-only” if docs/policies in root must also change.
- Every release addendum must include one of: `all-repos`, `selected-lanes`, `pm-portal-only`.

