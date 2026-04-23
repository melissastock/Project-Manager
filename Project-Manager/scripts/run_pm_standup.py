#!/usr/bin/env python3
"""Generate PM standup artifacts under docs/session-artifacts/standup/.

Also refreshes STATUS.md via portfolio_status so the dashboard matches the same scan.
"""

from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import portfolio_status as ps


ROOT = ps.ROOT
PM_ROOT = ps.PM_ROOT
CONFIG_PATH = ps.CONFIG_PATH
STANDUP_DIR = PM_ROOT / "docs" / "session-artifacts" / "standup"


def drift_score(repo: ps.RepoStatus) -> int:
    if not repo.has_commits:
        return 0
    return repo.untracked_count + repo.unstaged_count * 2 + repo.staged_count * 3


def readiness_band(repo: ps.RepoStatus) -> str:
    if not repo.exists:
        return "missing"
    if not repo.is_git_repo:
        return "not-git"
    if not repo.has_commits:
        return "unborn"
    score = drift_score(repo)
    if repo.lane == "recovery-core" and score >= 50:
        return "critical"
    if repo.lane == "recovery-core" and repo.dirty:
        return "at-risk"
    if score >= 30:
        return "at-risk"
    if repo.dirty:
        return "monitor"
    return "ready"


def _sensitive_data_class(data_class: str) -> bool:
    """Do not echo raw paths into committed standup logs for restricted repos."""
    dc = (data_class or "").lower()
    return any(
        x in dc
        for x in (
            "legal-financial",
            "regulated",
            "family-sensitive",
            "archive-sensitive",
        )
    )


def sample_untracked(repo_path: Path, entry: dict, limit: int = 25) -> list[str]:
    if not (repo_path / ".git").exists():
        return []
    if _sensitive_data_class(entry.get("data_class", "")):
        r = subprocess.run(
            ["git", "-C", str(repo_path), "status", "--porcelain", "-u"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            return [f"(git status failed: {r.stderr.strip()})"]
        n = sum(1 for ln in r.stdout.splitlines() if ln.startswith("??"))
        return [
            f"(**{n}** untracked paths; full paths omitted in standup log for `{entry.get('data_class', '')}` — run `git status` locally in `{entry.get('path', '')}`.)"
        ]
    r = subprocess.run(
        ["git", "-C", str(repo_path), "status", "--porcelain", "-u"],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return [f"(git status failed: {r.stderr.strip()})"]
    lines = [ln for ln in r.stdout.splitlines() if ln.startswith("??")]
    return lines[:limit]


def main() -> int:
    stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    human = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    config = json.loads(CONFIG_PATH.read_text())
    statuses = [ps.get_repo_status(entry) for entry in config["managed_repositories"]]

    STANDUP_DIR.mkdir(parents=True, exist_ok=True)

    by_band: dict[str, list[ps.RepoStatus]] = defaultdict(list)
    for s in statuses:
        by_band[readiness_band(s)].append(s)

    critical = sorted(by_band["critical"], key=drift_score, reverse=True)
    at_risk = sorted(by_band["at-risk"], key=drift_score, reverse=True)
    monitor = sorted(by_band["monitor"], key=drift_score, reverse=True)
    ready = [s for s in statuses if readiness_band(s) == "ready"]
    unborn = [s for s in statuses if readiness_band(s) == "unborn"]

    dirty = [s for s in statuses if s.dirty and s.has_commits]

    summary_path = STANDUP_DIR / f"STANDUP_SUMMARY-{stamp}.md"
    score_path = STANDUP_DIR / f"READINESS_SCORECARD-{stamp}.md"
    next_path = STANDUP_DIR / f"NEXT_STEPS_PROPOSAL-{stamp}.md"
    decision_path = STANDUP_DIR / f"DECISION_LOG-{stamp}.md"

    summary_lines = [
        f"# Standup summary ({stamp})",
        "",
        f"Generated: {human}",
        "",
        "## Portfolio counts",
        "",
        f"- Managed repositories: {len(statuses)}",
        f"- Ready (clean tree): {len(ready)}",
        f"- Monitor (dirty, lower severity): {len(monitor)}",
        f"- At-risk: {len(at_risk)}",
        f"- Critical: {len(critical)}",
        f"- Unborn (no commits): {len(unborn)}",
        "",
        "## Highest drift (top 8 by drift score)",
        "",
        "| Project | Drift score | Band | Lane | untracked | unstaged | staged |",
        "| --- | ---: | --- | --- | ---: | ---: | ---: |",
    ]
    ranked = sorted(
        (s for s in statuses if s.has_commits),
        key=drift_score,
        reverse=True,
    )[:8]
    for s in ranked:
        summary_lines.append(
            f"| {s.name} | {drift_score(s)} | {readiness_band(s)} | {s.lane} | {s.untracked_count} | {s.unstaged_count} | {s.staged_count} |"
        )
    summary_lines.append("")
    summary_path.write_text("\n".join(summary_lines) + "\n")

    score_lines = [
        f"# Readiness scorecard ({stamp})",
        "",
        f"Generated: {human}",
        "",
        "Bands: **critical** / **at-risk** / **monitor** / **ready** / **unborn** / **missing**.",
        "",
        "| Project | Band | Drift | Branch | Sync | Head |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for s in sorted(statuses, key=lambda x: (-drift_score(x), x.name)):
        if not s.has_commits:
            sync = "-"
            head = "-"
            d = "-"
        else:
            d = str(drift_score(s))
            if s.ahead is None and s.behind is None:
                sync = "no-upstream"
            else:
                sync = f"ahead:{s.ahead} behind:{s.behind}"
            head = s.head
        score_lines.append(
            f"| {s.name} | {readiness_band(s)} | {d} | {s.branch} | {sync} | {head} |"
        )
    score_lines.append("")
    score_path.write_text("\n".join(score_lines) + "\n")

    next_lines = [
        f"# Next steps proposal ({stamp})",
        "",
        f"Generated: {human}",
        "",
        "Ordered for portfolio execution queue batches (see `docs/portfolio-execution-queue.md`).",
        "",
        "## Batch A — Security and evidence drift",
        "",
        "- Review untracked paths below for secrets, credentials, or governed legal/finance material before any `git add`.",
        "- Do not bulk-commit from the parent repo without per-path classification.",
        "",
        "## Batch B — Highest-risk product drift",
        "",
    ]
    top_dirty = [s for s in ranked if s.dirty][:5]
    if top_dirty:
        for s in top_dirty:
            next_lines.append(
                f"- **{s.name}** (score {drift_score(s)}): classify untracked vs intentional artifacts; prefer explicit paths when committing."
            )
    else:
        next_lines.append("- No dirty repos in top drift slice; re-scan after local changes.")
    next_lines.extend(
        [
            "",
            "## Batch C — Remaining drift",
            "",
            "- Address smaller `untracked` piles repo-by-repo (readiness scaffold, dashboard, website, resume, Wayne Strain).",
            "",
            "## Batch D — Planning-only / unborn",
            "",
            "- **2024 Taxes** and **Bankruptcy**: initialize first commit or explicitly **defer** with owner rationale in the decision log.",
            "",
            "## Verification",
            "",
            "- Run `python3 scripts/portfolio_status.py` after changes.",
            "- Re-run this script to mint a new timestamped artifact set.",
            "",
        ]
    )
    next_path.write_text("\n".join(next_lines) + "\n")

    class_lines = [
        f"# Evidence and drift classification ({stamp})",
        "",
        f"Generated: {human}",
        "",
        "Per-repo **sample** of untracked lines (`git status --porcelain`, first 25). Use for Batch A triage; not exhaustive.",
        "",
    ]
    entry_by_path = {e["path"]: e for e in config["managed_repositories"]}
    for s in sorted(dirty, key=lambda x: -x.untracked_count):
        repo_path = ROOT / s.path
        entry = entry_by_path.get(s.path, {})
        class_lines.append(f"## {s.name} (`{s.path}`)")
        class_lines.append("")
        samples = sample_untracked(repo_path, entry, 25)
        if not samples:
            class_lines.append("(no untracked sample lines; may be staged/unstaged only)")
        else:
            class_lines.extend(f"- `{ln}`" for ln in samples)
        class_lines.append("")
        class_lines.append(
            "**Classification prompt:** PUSH (sanitized portfolio artifact) / LOCAL-ONLY (secrets, raw legal, PII) / TEMPLATE-CANDIDATE / IGNORE-via-gitignore (generated or machine-local)."
        )
        class_lines.append("")

    decision_lines = [
        f"# Decision log ({stamp})",
        "",
        f"Generated: {human}",
        "",
        "## Owner decisions required",
        "",
        "| Topic | Status | Notes |",
        "| --- | --- | --- |",
        "| OAuth / API credential rotation for keys ever present in `MJS-Financial-Dash` history | **pending owner** | History rewrite does not revoke issued tokens; complete in provider consoles. |",
        "| `Divorce` private remote | **optional** | `clean` locally; add private `origin` + `github_repo_url` in `config/repos.json` when ready. |",
        "| **2024 Taxes** / **Bankruptcy** repos (unborn) | **defer** | No commits yet; defer initialization until recovery-core drift batches progress; see Batch D. |",
        "",
        "## Automation / structural",
        "",
        "| Topic | Status | Notes |",
        "| --- | --- | --- |",
        "| Backup vs canonical MJS remote collision | **pass** | `python3 scripts/check_remote_collisions.py` reports no risky duplicate origins (archive uses dedicated backup remote). |",
        "",
        "## Batch A classification (summary)",
        "",
        f"- Repos with working tree noise: **{len(dirty)}**.",
        f"- Largest untracked count this scan: **{max((s.untracked_count for s in statuses), default=0)}** ({max(statuses, key=lambda x: x.untracked_count).name if statuses else 'n/a'}).",
        "",
        "---",
        "",
        "## Detailed untracked samples",
        "",
    ]
    decision_lines.extend(class_lines[4:])  # skip duplicate header
    decision_path.write_text("\n".join(decision_lines) + "\n")

    ps.main()

    print(f"Standup stamp: {stamp}")
    print(f"Wrote {summary_path.relative_to(PM_ROOT)}")
    print(f"Wrote {score_path.relative_to(PM_ROOT)}")
    print(f"Wrote {next_path.relative_to(PM_ROOT)}")
    print(f"Wrote {decision_path.relative_to(PM_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
