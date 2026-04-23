# bg-legal — single working folder (from `Case Files/`)

The portfolio now uses **`bg-legal/`** as the only managed path for the GitHub repo `melissastock/bg-legal` (Case Files **program** working copy). `config/repos.json` lists this project as **bg-legal**; the Google Drive folder named **Case Files** remains **intake-only**, not a second git working tree.

## Security (Case Files client material)

- **Raw exports and bulk evidence** stay in **`Archiavellian-Archive`** (or other archive intake) per `docs/case-files-track-onboarding-2026-04-22.md`. Do not duplicate full evidence trees into `bg-legal/` for convenience.
- **`bg-legal/`** holds **governed** work: operating docs, routing decisions, timeline CSVs under `docs/timeline-evidence/`, reviewed derivatives, and delivery artifacts. Treat the repo as **private-client** / **legal-financial-restricted**; no public remotes, no casual copies.
- If you had an old **`Case Files/`** folder with git or files: **review** each path before moving; prefer re-cloning `bg-legal` and copying only paths you have classified. Remove or archive `Case Files/` after migration so there is only one working copy.

## One-time operator steps

1. **Clone** (from Project Manager root):  
   `git clone git@github.com:melissastock/bg-legal.git bg-legal`  
   (or HTTPS equivalent)
2. **Migrate** any intentional tracked content from `Case Files/` into `bg-legal/` only after classification (or cherry-pick history if both were git repos — prefer a clean clone if unsure).
3. **Remove** the old `Case Files/` directory when empty or obsolete so scripts and humans do not split edits across two folders.
4. **Remotes**: `python3 scripts/sync_repo_remotes.py --apply` updates `origin` from `config/repo-remotes.json` for repos that exist on disk.

## Scripts that use `bg-legal/`

Timeline and docket automation resolve paths via `scripts/bg_legal_paths.py` (`bg-legal/docs/timeline-evidence/`). Internal portfolio checks: `python3 scripts/run_repo_readiness_gates.py --target bg-legal`.
