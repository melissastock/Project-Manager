# Brand Template Rules

## Purpose

Use these rules when converting branded source materials into reusable templates.

## Core Rules

- Keep structure and messaging pattern, not brand-specific identity.
- Replace company names, slogans, logos, and trademarked strings with tokens.
- Remove person names, direct contacts, addresses, and private URLs.
- Keep claims only if they are generic and verifiable.
- Do not embed sensitive numbers, client references, legal identifiers, or pricing tied to one private entity.

## Required Tokens

Use these placeholders in all GTM and brand-derived templates:

- `{{BRAND_NAME}}`
- `{{BRAND_TAGLINE}}`
- `{{PRIMARY_AUDIENCE}}`
- `{{CORE_OFFER}}`
- `{{VALUE_PROOF_1}}`
- `{{VALUE_PROOF_2}}`
- `{{PRIMARY_CTA}}`
- `{{CONTACT_CHANNEL}}`

## Logo And Visual Rules

- Do not include source logos in reusable templates.
- Include only a placeholder: `{{LOGO_SLOT}}`.
- Keep color guidance as abstract tokens:
  - `{{PRIMARY_COLOR}}`
  - `{{SECONDARY_COLOR}}`
  - `{{ACCENT_COLOR}}`

## Messaging Rules

- Convert feature language into problem/benefit language.
- Keep copy blocks under standard sections:
  - audience
  - pain
  - promise
  - proof
  - CTA
- Add one compliance line: "Final claims require legal/compliance review before publication."

## Portfolio Mapping Requirement

Every brand-derived template must include:

- `campaign_owner`
- `approval_owner`
- `readiness_gate`
- `next_review_date`
- `distribution_channels`

## Redaction Gate

Before pushing a brand-derived template:

1. Confirm no explicit source brand marks remain.
2. Confirm all names and contact details are tokenized.
3. Confirm no private financial, legal, or client identifiers remain.
4. Confirm file passes `PUSH-CANDIDATE` classification in manifest.
