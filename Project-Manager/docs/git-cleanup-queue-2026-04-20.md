# Git Cleanup Queue - 2026-04-20

- Generated at: `2026-04-20T12:32:37-06:00`
- Dirty repos: `8`
- Clean repos: `7`
- Queue CSV: `docs/git-cleanup-queue-2026-04-20.csv`

## Priority Queue (Dirty Repos First)

- P1: `MJS Financial Dash Backup` (`MJS Financial Dash backup 20260310_153810`) - 53 changes (staged 0, unstaged 20, untracked 33) - `## main...origin/main`
- P7: `Archiavellian-Archive` (`Archiavellian-Archive`) - 3 changes (staged 0, unstaged 0, untracked 3) - `## main...origin/main [ahead 1]`
- P11: `MJS Financial Dash` (`MJS Financial Dash`) - 68 changes (staged 0, unstaged 23, untracked 45) - `## codex/finance-snapshot-onboarding...origin/codex/finance-snapshot-onboarding`
- P11: `Aneumind and TC Structure` (`Aneumind and TC Structure`) - 48 changes (staged 0, unstaged 3, untracked 45) - `## codex/taylor-shell-claim-scenario`
- P11: `Teach - Zahmeir Learning System` (`App Builder/Teach/zahmeir-learning-system`) - 21 changes (staged 0, unstaged 19, untracked 2) - `## feat/lesson-1-direct-launch...origin/feat/lesson-1-direct-launch [ahead 1]`
- P11: `Producer` (`Producer`) - 17 changes (staged 0, unstaged 7, untracked 10) - `## main...origin/main [ahead 3]`
- P11: `Teach - Home Learning Playbook` (`App Builder/Teach/home-learning-playbook`) - 12 changes (staged 0, unstaged 6, untracked 6) - `## main...origin/main [ahead 1]`
- P11: `Momentum-OS` (`Momentum-OS`) - 11 changes (staged 0, unstaged 5, untracked 6) - `## main...origin/main [ahead 3]`

## Suggested Cleanup Sequence

1. Archive repos first (`Archiavellian-Archive`, archive backups) to preserve evidence-state checkpoints.
2. High-change active repos next (`MJS Financial Dash`, `Aneumind and TC Structure`).
3. Education repos (`Teach - ...`) then platform repos (`Momentum-OS`, `Producer`).
4. Rebuild `STATUS.md` and reconcile top-level gitlinks last.
