# Mobile Compliance Governance (Apple + Android)

This policy defines the minimum governance controls required before shipping PM Portal mobile clients to App Store and Google Play.

## Scope

- iOS build and release workflow (Apple App Store)
- Android build and release workflow (Google Play)
- Shared privacy/security controls that must pass before submission

## Governance Owners

- `release_owner`: accountable for submitting builds and metadata
- `privacy_owner`: accountable for privacy disclosures and data mapping
- `security_owner`: accountable for security controls and incident policy
- `compliance_reviewer`: final sign-off gate before store submission

## Shared Compliance Gates

All gates below must be `pass` before submitting to either store:

1. **Data inventory + minimization**
   - Document every data element collected, where it is stored, and retention period.
   - Verify only required operational data is collected.
2. **Consent and policy alignment**
   - Privacy policy published and linked in-app and in store metadata.
   - Terms and support contact published.
3. **Security baseline**
   - TLS in transit for all network calls.
   - No secrets in client bundle or logs.
   - Incident response contact and escalation path documented.
4. **Access and account controls**
   - Authentication behavior documented.
   - Account deletion / data deletion handling documented (if accounts are supported).
5. **Third-party SDK review**
   - SDK list and purposes documented.
   - Tracking/analytics behavior mapped to disclosures.

## Apple App Store Governance

Required artifacts:

- App Privacy answers completed in App Store Connect.
- Privacy policy URL and support URL configured.
- Export compliance/encryption answers reviewed.
- Age rating + content declarations completed.
- If Sign in with Apple is required by policy, implementation status documented.

Apple release gate checklist:

- `apple_privacy_questionnaire_complete`
- `apple_data_types_mapped_to_runtime`
- `apple_encryption_export_compliance_reviewed`
- `apple_age_rating_and_content_review_complete`
- `apple_submission_metadata_reviewed`

## Google Play Governance

Required artifacts:

- Data safety form completed in Play Console.
- Privacy policy URL configured.
- Target API level and SDK policy requirements met.
- Permission declarations justified (especially sensitive permissions).
- If ads/tracking present, disclosure is accurate and complete.

Google release gate checklist:

- `google_data_safety_form_complete`
- `google_permissions_justification_complete`
- `google_target_api_policy_pass`
- `google_privacy_policy_linked`
- `google_submission_metadata_reviewed`

## Evidence Package (per release)

Each release must include an evidence folder under:

`docs/compliance-evidence/mobile/<release-version>/`

Minimum contents:

- Completed gate checklist (Apple + Google)
- Privacy/data inventory snapshot
- SDK inventory and purpose mapping
- Store metadata export/screenshots
- Reviewer sign-off note with timestamp

## Required Disclosure Inputs

Store-facing disclosure sources:

- Privacy/disclosure narrative: `docs/mobile-privacy-and-disclosures.md`
- Machine-readable disclosure config: `backend/config/mobile-store-disclosures.json`

These must be reviewed and updated when runtime data behavior, permissions, or SDK usage changes.

## Stop-Ship Conditions

Do not ship if any of the following is true:

- Privacy disclosures do not match actual runtime behavior.
- Required forms (App Privacy or Data safety) are incomplete.
- Sensitive permission use has no user-facing justification.
- Secrets or tokens are present in mobile bundle/log outputs.

