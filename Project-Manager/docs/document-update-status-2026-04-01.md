# Document Update Status — 2026-04-01

Purpose: record what has been updated in Project Manager, what is current, and what still needs a local sync pass before PR packaging.

## Documents Added This Session

- `docs/current-project-portfolio-audit.md`
- `docs/archiavellian-portfolio-integration.md`
- `docs/archiavellian-dependency-map.md`
- `docs/SESSION_CLOSE.md`
- `docs/codex-close-checklist.md`
- `docs/session-handoffs/README.md`
- `docs/SESSION_OPEN.md`
- `scripts/create_session_handoff.py`
- `scripts/open_session.py`
- `scripts/open_session_v2.py`
- `scripts/open_session_v3.py`

## Portfolio State Reflected In Docs

### Now explicitly documented
- Archiavellian is part of the managed system
- Archiavellian-Archive is part of the managed system as the archive-side companion
- Session open and session close protocols now exist
- Session handoff creation is scripted
- PM sync awareness is scripted at session start

### Still needs local portfolio sync
These items should be updated locally in the working copy, then regenerated and committed as part of the next PR-prep pass:

1. `config/repos.json`
   - add `archiavellian`
   - add `Archiavellian-Archive`

2. `README.md`
   - include Archiavellian repos in managed repository snapshot
   - optionally mention session open/close protocol docs in notes or workflow references

3. `STATUS.md`
   - regenerate with `python3 scripts/portfolio_status.py`
   - do not hand-edit the generated dashboard

## Why these three were not force-updated here

This GitHub-only pass was safe for additive documentation and scripts.

`STATUS.md` is generated and should be refreshed from the local Project Manager workspace so the file reflects the real repo state instead of a guessed or partial remote-only view.

`config/repos.json` and `README.md` should be updated in the same local sync pass so the manifest, human-facing snapshot, and generated status remain aligned.

## PR Packaging Readiness

### Ready now
- supporting docs
- operating protocol docs
- session lifecycle scripts
- Archiavellian integration reference docs

### Must happen before packaging the next PM-related PR
1. update `config/repos.json`
2. update `README.md`
3. regenerate `STATUS.md`
4. run a validation pass on the session scripts
5. confirm Resume Builder PR dependencies separately

## Suggested Commit Sequence For Next Local Pass

1. Add Archiavellian repos to manifest and README
2. Regenerate STATUS
3. Test scripts:
   - `python3 scripts/create_session_handoff.py`
   - `python3 scripts/open_session_v3.py`
4. Package PR with:
   - summary of new docs
   - note that STATUS was regenerated locally
   - note that Archiavellian is now formally part of the portfolio system
