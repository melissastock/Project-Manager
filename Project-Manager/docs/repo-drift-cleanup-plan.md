# Repo Drift Cleanup Plan

## Approach

Treat repo drift as two separate layers:

1. Child repo content drift
   Fix modified, deleted, generated, and untracked files inside the child repo first.
2. Top-level pointer drift
   Update the `Project Manager` gitlink only after the child repo has the exact committed `HEAD` you want recorded.

## Priority Order

1. TuneFab
2. MJS Financial Dash
3. MJS Financial Dash backup 20260310_153810
4. Producer
5. Momentum-OS
6. Aneumind and TC Structure
7. App Builder/Teach/zahmeir-learning-system
8. App Builder/Teach/home-learning-playbook

## Repo-by-Repo Plan

### TuneFab

- Main issue: extremely noisy runtime drift under `provider-access-hub/.tmp/embedded-postgres/`.
- Cleanup move:
  - Add or tighten ignore rules for embedded Postgres runtime state and desktop junk.
  - Separate runtime noise from real source edits in `provider-access-hub/docs/`, `openapi/`, `package.json`, `scripts/`, and migrations.
  - Commit real application changes in one or more focused commits.
- Only after that: run the top-level child repo pointer sync.

### MJS Financial Dash

- Main issue: large structural migration with tracked deletions from `outputs/`, Python source edits, and many new archival folders.
- Cleanup move:
  - Decide whether this is one intentional archival refactor.
  - If yes, commit in slices:
    - outputs routing and removals
    - new AMA tooling
    - archive/data structure additions
  - Add ignore rules for `tmp/` and any generated bundles that should not be tracked.
- Only after that: sync the top-level pointer.

### MJS Financial Dash backup 20260310_153810

- Main issue: backup repo is mixing generated outputs, local tokens, desktop junk, and possible working changes.
- Cleanup move:
  - Decide whether this repo should stay a frozen snapshot or become an actively maintained backup workspace.
  - If frozen, ignore or remove volatile/generated artifacts and keep it minimal.
  - If active, add ignore rules for `.DS_Store`, `.pycache_local/`, and sensitive token/runtime files where appropriate.
- Only after that: sync the top-level pointer if you intend the backup repo to advance.

### Producer

- Main issue: mostly real content drift rather than tooling noise.
- Cleanup move:
  - Group edits into narrative revisions vs archival planning documents.
  - Commit substantive new planning docs separately from revisions to existing story docs.
  - Consider whether `Signal Noise/` should be tracked or ignored.
- This repo is relatively safe to clean because the changes appear intentional.

### Momentum-OS

- Main issue: mixed product/doc edits plus likely local-only files like `.codex/` and `backend/.env.save`.
- Cleanup move:
  - Add ignore rules for `.codex/` and local env backup files if they are not meant for version control.
  - Commit docs/product changes separately from backend changes.
- Then sync the top-level pointer.

### Aneumind and TC Structure

- Main issue: many generated output documents and packet drafts sitting untracked under `output/`.
- Cleanup move:
  - Decide whether `output/spreadsheet/` is a tracked deliverables area or a generated working directory.
  - If it is a deliverables area, commit a curated working set only.
  - If it is generated, add ignore rules and move canonical deliverables elsewhere.
- Then sync the top-level pointer if the repo `HEAD` advances.

### App Builder/Teach/zahmeir-learning-system

- Main issue: broad content and app edits that look intentional, not noisy.
- Cleanup move:
  - Split app code changes from content/template changes if possible.
  - Commit the new session tool and assessment additions as a focused content pass.
- Then sync pointer normally.

### App Builder/Teach/home-learning-playbook

- Main issue: docs/templates growth plus new directories.
- Cleanup move:
  - Group the new assessment/sprint/students/trackers material into one structured curriculum commit.
  - No obvious runtime-noise problem here.
- Then sync pointer normally.

## Portfolio Repo Workflow After Cleanup

1. Clean or intentionally leave dirty each child repo.
2. Commit real child repo changes where appropriate.
3. From `Project Manager`, inspect pointer drift:
   - `python3 scripts/sync_child_repo_pointers.py`
4. When ready, stage the updated gitlinks:
   - `python3 scripts/sync_child_repo_pointers.py --apply`
5. Refresh the dashboard:
   - `python3 scripts/portfolio_status.py`
6. Commit and push the `Project Manager` repo.
