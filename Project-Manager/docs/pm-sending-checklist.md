# PM Outbound Sending and Release Checklist

Use this before any external send (counsel, court, investor, partner, or public publish).

## 1) Classify the payload

- [ ] Recipient class recorded (internal / counsel / court / investor / partner / public)
- [ ] Data class matches manifest policy (`data_class` from [config/repos.json](config/repos.json))
- [ ] IP class respected (`ip_class`; Personal OS and client invention material stay private)
- [ ] `public_sync_allowed` is `true` only for intentional public releases

## 2) Technical readiness

- [ ] Source repo is correct canonical home (not an archive-only clone)
- [ ] `python3 scripts/check_production_readiness.py --target "<path>"` where delivery gates apply
- [ ] No secrets, tokens, or raw identifiers in outbound bundle

## 3) Governance gates

- [ ] [docs/REVIEW_GATES.md](REVIEW_GATES.md) satisfied for the change set
- [ ] Compliance reviewer signoff for restricted legal/financial/regulated material
- [ ] Publication review file exists when visibility or sensitivity is in scope

## 4) Send record

- [ ] What was sent (artifact list + version / commit SHA)
- [ ] Who approved send
- [ ] Date and channel
- [ ] Retention note (where originals live; derived copies labeled)

## 5) Exception path

If any box cannot be checked:

- [ ] Exception reason documented
- [ ] Risk owner and expiry date assigned
- [ ] Recorded in session handoff under `Issues / Challenges`
