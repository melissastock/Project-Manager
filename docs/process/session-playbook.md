# Session Playbook

## Purpose

Create a repeatable way to run governance updates with low friction and low cleanup risk.

This playbook defines:
- a mode to choose at session start
- a standard commit sequence
- a push sequence
- a closeout checklist

---

## Session Modes

### Draft Mode (read-only validation)

Use when you want diagnostics and risk visibility before changing files.

Run:
- `python3 scripts/run_portfolio_readiness_checks.py`

Behavior:
- no auto-remediation
- no generated intake/research scaffolds
- best for planning and review

### Apply Mode (automated remediation)

Use when you want to implement and propagate fixes now.

Run:
- `python3 scripts/run_portfolio_readiness_checks.py --fix`

Behavior:
- validators may update `docs/project-intake.md`
- validators may scaffold `docs/research/persona-validation-notes.md`
- requires commit batching to keep history clean

---

## Standard Commit Sequence

Commit in this order:

1) **Engine changes (parent)**
- scripts
- governance docs
- shared schemas/templates

2) **Child repo implementation/scaffold changes**
- per-repo `docs/project-intake.md`
- per-repo `docs/research/persona-validation-notes.md`
- repo-specific implementation files (if any)

3) **Parent pointer sync**
- update child repo pointers in `Project-Manager`

---

## Push Sequence

Run pushes in this order:

1) push child repos first
2) push parent pointer sync commit second

This prevents parent references from pointing at commits that are not yet available remotely.

---

## Closeout Checklist

- Draft or Apply mode chosen at start
- portfolio checks run and reviewed
- child repos clean after child commits
- parent repo clean after pointer sync commit
- sensitive/evidence files reviewed before push
- pushed refs confirmed

---

## Notes on Evidence Handling

- `docs/research/persona-validation-notes.md` starts as scaffold-only and may be committed as structure.
- Once populated with interview or stakeholder findings, treat as sensitive governance evidence and review before push.

