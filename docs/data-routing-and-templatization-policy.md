# Data Routing And Templatization Policy

Version: `v1.0`  
Last updated: `2026-04-21`

## Purpose

This policy defines where sensitive and non-sensitive artifacts belong, what can be pushed to git, and how to convert source documents into reusable templates for the portfolio system.

## System Routing Rules

- `Project Manager` stores portfolio metadata, governance, and sanitized templates only.
- `MJS Financial Dash` stores tax, payroll, banking, accounting, and reconciliation source documents.
- `Divorce` stores personal legal dispute, attorney packet, separation, and authority-conflict source documents.
- `Archiavellian` stores private compliance and sensitive evidence archives, including client/consent records and provider attestation packets.
- `PAH` receives sanitized process templates for credentialing, payer enrollment, and billing workflows.
- `Momentum-OS` receives sanitized operational and GTM templates.

## Push Decision Framework

Use this order when triaging files:

1. If file contains direct identifiers, account numbers, tax IDs, credentials, legal signatures, or client/clinical details -> `LOCAL-ONLY`.
2. If file is a branded collateral or process narrative without sensitive fields -> `PUSH-CANDIDATE`.
3. If file is useful as a repeatable process but includes sensitive examples -> `TEMPLATE-CANDIDATE` after redaction.

## Never Push (Raw)

- `*password*`
- `*W-9*`, `*EIN*`, `*1095*`, tax returns
- bank reconciliation, ledger, journal exports
- payroll exports and compensation detail files
- client intake exports with names, DOB, addresses, diagnosis, insurance IDs
- consent/disclosure forms with signatures
- attorney briefing packets and executed legal agreements

## Template-First Extraction Standard

When converting a source file into a template:

- Remove all names, dates of birth, IDs, account numbers, signatures, and locations.
- Replace examples with placeholders using uppercase tokens, such as `{{CLIENT_ROLE}}`.
- Keep structure, controls, and decision logic.
- Add required evidence fields to support PM readiness and governance tracking.
- Include an explicit "Do not store sensitive identifiers" note in each template.
- Apply `docs/templates/brand-template-rules.md` to all brand-derived GTM or collateral templates.

## Portfolio Metadata Hand-Off Format

Only pass the following to `Project Manager` from sensitive systems:

- `artifact_category`
- `owner`
- `status`
- `risk_level`
- `next_review_date`
- `readiness_score`
- `redaction_complete` (`yes/no`)
- `source_system` (`MJS Financial Dash`, `Divorce`, `Archiavellian`)

## Pre-Push Checklist

1. Classify file as `PUSH-CANDIDATE`, `LOCAL-ONLY`, or `TEMPLATE-CANDIDATE`.
2. Run redaction validation for template candidates.
3. Confirm no blocked patterns are included.
4. Commit only sanitized outputs to shared repos.
5. Store source raw files in routed private repository only.
