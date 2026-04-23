# Mobile Privacy And Disclosures (MJSDS-Adapted)

This document adapts privacy/disclosure principles used on `mjsdigitalstrategy.com` for mobile app release governance.

Source alignment:

- `mjsds-website/docs/visibility-policy.md`
- `mjsds-website/docs/content-playbook.md`
- `mjsds-website/docs/workspace-model.md`

## App Store Disclosure Summary (Plain Language)

The PM Portal mobile app is a portfolio operations tool. It is designed to show project readiness, project metadata, and recommendation decisions. It is **not** a public website, and it is **not** intended to expose private or regulated source materials.

The app may process:

- project metadata (project name, lane, stage, path, status signals)
- workflow decisions (approved/rejected/defer)
- operational timestamps and reviewer/owner fields

The app must not expose:

- PHI
- client-sensitive source files
- draft legal agreements
- financial internals
- credentials, tokens, access instructions

## Data Use Disclosure (Mobile)

- **Primary purpose:** operational readiness review and decision tracking.
- **No sale of personal data:** data is used for product operations only.
- **No hidden tracking claims:** if analytics/SDKs are used, they must be declared in Apple App Privacy and Google Play Data Safety forms.
- **Data minimization:** only collect data necessary for portfolio operations.

## Mobile-Specific User Disclosure Text

Use this copy (or stricter) in app settings/privacy screens and store metadata:

1. **Operational data only**
   - “This app collects only the project and decision data needed to run portfolio operations.”
2. **Protected information boundary**
   - “Protected legal, financial, client, and health-related materials are not intended for mobile exposure in this app.”
3. **Third-party services**
   - “If analytics or infrastructure providers are used, their data handling is disclosed in store privacy forms.”
4. **Control and contact**
   - “For privacy and data requests, contact the support channel listed in the app store listing.”

## Apple App Store (Adapted Disclosure Requirements)

Before submission:

- Complete App Privacy answers using actual runtime behavior.
- Ensure disclosure answers match app permissions and SDK behavior.
- Keep privacy policy URL and support URL active.
- Do not claim data categories the app does not collect.
- Do not omit categories the app does collect.

## Google Play (Adapted Disclosure Requirements)

Before submission:

- Complete Data Safety form using actual runtime behavior.
- Map permissions to explicit in-app purpose.
- Keep privacy policy URL active and consistent with app behavior.
- Ensure “data collected/shared” answers match production app behavior.

## Analytics / Script Injection Rule (Mobile Adaptation)

Web guidance for shared scripts/analytics (`workspace-model.md`) maps to mobile as:

- No new SDK may be added without privacy review.
- Every SDK must have documented purpose and data classes.
- Every SDK must be reflected in Apple/Google disclosure forms.
- If SDK behavior changes, update disclosures before release.

## Release Blocking Conditions

Do not ship mobile releases if:

- Store disclosures do not match runtime behavior.
- Sensitive data boundary above is violated.
- Privacy policy/support links are missing.
- New SDKs are added without disclosure updates.

