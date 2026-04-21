#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
REPOS_CONFIG = ROOT / "config" / "repos.json"
POLICY_CONFIG = ROOT / "config" / "pm-standup-policy.json"


@dataclass
class RepoSnapshot:
    name: str
    path: str
    lane: str
    priority_class: str
    intake_stage: str
    exists: bool
    is_git_repo: bool
    branch: str
    head: str
    summary: str
    staged_count: int
    unstaged_count: int
    untracked_count: int
    ahead: int | None
    behind: int | None
    backlog_files: list[str]
    sprint_files: list[str]


def run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_path), *args],
        capture_output=True,
        text=True,
    )


def parse_porcelain(output: str) -> tuple[int, int, int]:
    staged = 0
    unstaged = 0
    untracked = 0
    for line in output.splitlines():
        if not line:
            continue
        if line.startswith("??"):
            untracked += 1
            continue
        if len(line) >= 2:
            if line[0] != " ":
                staged += 1
            if line[1] != " ":
                unstaged += 1
    return staged, unstaged, untracked


def discover_planning_files(repo_path: Path) -> tuple[list[str], list[str]]:
    candidates = []
    docs_dir = repo_path / "docs"
    if docs_dir.exists():
        candidates.extend(p for p in docs_dir.glob("*.md"))
    candidates.extend(p for p in repo_path.glob("*.md"))
    backlog = sorted(str(p.relative_to(repo_path)) for p in candidates if "backlog" in p.name.lower())
    sprint = sorted(str(p.relative_to(repo_path)) for p in candidates if "sprint" in p.name.lower())
    return backlog, sprint


def resolve_repo_snapshot(entry: dict[str, Any]) -> RepoSnapshot:
    repo_path = ROOT / entry["path"]
    exists = repo_path.exists()
    is_git_repo = exists and (repo_path / ".git").exists()
    backlog_files, sprint_files = ([], [])
    if exists:
        backlog_files, sprint_files = discover_planning_files(repo_path)
    if not is_git_repo:
        return RepoSnapshot(
            name=entry["name"],
            path=entry["path"],
            lane=entry.get("lane", ""),
            priority_class=entry.get("priority_class", ""),
            intake_stage=entry.get("intake_stage", ""),
            exists=exists,
            is_git_repo=False,
            branch="missing",
            head="",
            summary="No git repo detected",
            staged_count=0,
            unstaged_count=0,
            untracked_count=0,
            ahead=None,
            behind=None,
            backlog_files=backlog_files,
            sprint_files=sprint_files,
        )

    head_cp = run_git(repo_path, "rev-parse", "--verify", "HEAD")
    if head_cp.returncode != 0:
        return RepoSnapshot(
            name=entry["name"],
            path=entry["path"],
            lane=entry.get("lane", ""),
            priority_class=entry.get("priority_class", ""),
            intake_stage=entry.get("intake_stage", ""),
            exists=True,
            is_git_repo=True,
            branch="unborn",
            head="",
            summary="Repository has no commits yet",
            staged_count=0,
            unstaged_count=0,
            untracked_count=0,
            ahead=None,
            behind=None,
            backlog_files=backlog_files,
            sprint_files=sprint_files,
        )

    branch = run_git(repo_path, "branch", "--show-current").stdout.strip() or "detached"
    head = run_git(repo_path, "rev-parse", "--short", "HEAD").stdout.strip()
    summary = run_git(repo_path, "log", "-1", "--pretty=%s").stdout.strip()
    porcelain = run_git(repo_path, "status", "--porcelain").stdout
    staged_count, unstaged_count, untracked_count = parse_porcelain(porcelain)

    ahead = behind = None
    sync = run_git(repo_path, "rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    if sync.returncode == 0:
        left, right = sync.stdout.strip().split()
        behind, ahead = int(left), int(right)

    return RepoSnapshot(
        name=entry["name"],
        path=entry["path"],
        lane=entry.get("lane", ""),
        priority_class=entry.get("priority_class", ""),
        intake_stage=entry.get("intake_stage", ""),
        exists=True,
        is_git_repo=True,
        branch=branch,
        head=head,
        summary=summary,
        staged_count=staged_count,
        unstaged_count=unstaged_count,
        untracked_count=untracked_count,
        ahead=ahead,
        behind=behind,
        backlog_files=backlog_files,
        sprint_files=sprint_files,
    )


def readiness_label(score: int, bands: list[dict[str, Any]]) -> str:
    for band in sorted(bands, key=lambda x: int(x["min_score"]), reverse=True):
        if score >= int(band["min_score"]):
            return str(band["label"])
    return "unknown"


def compute_score(repo: RepoSnapshot, policy: dict[str, Any]) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 50
    score += int(policy["priority_weights"].get(repo.priority_class, 0))
    score += int(policy["lane_weights"].get(repo.lane, 0))
    if not repo.is_git_repo:
        score -= int(policy["risk_penalties"]["missing_git_repo"])
        reasons.append("Repository not initialized as git.")
    score -= repo.staged_count * int(policy["risk_penalties"]["staged"])
    score -= repo.unstaged_count * int(policy["risk_penalties"]["unstaged"])
    reasons.append(f"Working-tree drift staged={repo.staged_count}, unstaged={repo.unstaged_count}, untracked={repo.untracked_count}.")
    score -= min(
        repo.untracked_count * int(policy["risk_penalties"]["untracked_per_item"]),
        int(policy["risk_penalties"]["max_untracked_penalty"]),
    )
    if repo.behind is not None and repo.behind > 0:
        score -= repo.behind * int(policy["risk_penalties"]["behind_per_commit"])
        reasons.append(f"Branch is behind upstream by {repo.behind}.")
    if repo.intake_stage in {"archive", "onboarding"}:
        reasons.append(f"Intake stage is {repo.intake_stage}; execution should remain scoped.")
    if not repo.backlog_files:
        reasons.append("No backlog document detected.")
    if not repo.sprint_files:
        reasons.append("No sprint plan document detected.")
    score = max(0, min(100, score))
    return score, reasons


def recommend_next_steps(repo: RepoSnapshot, score: int, label: str, policy: dict[str, Any]) -> list[dict[str, str]]:
    recs: list[dict[str, str]] = []
    if repo.untracked_count > 0:
        recs.append(
            {
                "action": "Run drift containment and classify untracked items.",
                "why_now": f"{repo.untracked_count} untracked items create reproducibility risk.",
                "risk_if_delayed": "Decision artifacts can diverge from audited history.",
                "alternatives_considered": "Commit everything quickly (rejected due to secret/noise risk); ignore drift (rejected due to traceability risk).",
            }
        )
    if repo.staged_count > 0 or repo.unstaged_count > 0:
        recs.append(
            {
                "action": "Perform controlled commit or explicit holdback disposition.",
                "why_now": "Open tracked modifications indicate unstable handoff state.",
                "risk_if_delayed": "Partial local edits can invalidate readiness claims.",
                "alternatives_considered": "Defer until end of sprint (rejected for high-priority lanes).",
            }
        )
    if not repo.backlog_files or not repo.sprint_files:
        recs.append(
            {
                "action": "Create or refresh backlog/sprint docs for this project.",
                "why_now": "Standup prioritization quality drops without explicit queue context.",
                "risk_if_delayed": "Next-step suggestions become less explainable and auditable.",
                "alternatives_considered": "Use ad-hoc memory only (rejected due to owner approval requirements).",
            }
        )
    if label in {"critical", "at-risk"}:
        recs.append(
            {
                "action": "Run a focused readiness gate before adding feature work.",
                "why_now": f"Current readiness is {label} ({score}/100).",
                "risk_if_delayed": "Feature throughput can mask unresolved operational risk.",
                "alternatives_considered": "Proceed with feature velocity first (rejected for recovery/core safety).",
            }
        )
    if not recs:
        recs.append(
            {
                "action": "Maintain current lane execution and review outcomes at next standup.",
                "why_now": "No urgent operational blockers detected.",
                "risk_if_delayed": "Low; monitor for drift and backlog freshness.",
                "alternatives_considered": "Introduce unscheduled scope (rejected to preserve focus).",
            }
        )
    return recs[: int(policy.get("max_recommendations_per_project", 4))]


def generate_reports(snapshots: list[RepoSnapshot], policy: dict[str, Any], output_dir: Path) -> dict[str, Path]:
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    scores: list[tuple[RepoSnapshot, int, str, list[str]]] = []
    for repo in snapshots:
        score, reasons = compute_score(repo, policy)
        label = readiness_label(score, policy["readiness_bands"])
        scores.append((repo, score, label, reasons))
    scores.sort(key=lambda r: (r[2] != "critical", r[1]))

    summary_path = output_dir / f"STANDUP_SUMMARY-{ts}.md"
    scorecard_path = output_dir / f"READINESS_SCORECARD-{ts}.md"
    proposal_path = output_dir / f"NEXT_STEPS_PROPOSAL-{ts}.md"
    decision_log_path = output_dir / f"DECISION_LOG-{ts}.md"

    summary_lines = [
        "# PM Standup Summary",
        "",
        f"Generated: {now}",
        "",
        f"- Projects evaluated: {len(scores)}",
        f"- Critical: {sum(1 for _, _, l, _ in scores if l == 'critical')}",
        f"- At-risk: {sum(1 for _, _, l, _ in scores if l == 'at-risk')}",
        f"- Monitor: {sum(1 for _, _, l, _ in scores if l == 'monitor')}",
        f"- Ready: {sum(1 for _, _, l, _ in scores if l == 'ready')}",
        "",
        "Human approval is required before any recommended action is executed.",
    ]
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    score_lines = [
        "# Readiness Scorecard",
        "",
        "| Project | Lane | Priority | Score | Band | Drift (staged/unstaged/untracked) | Backlog | Sprint |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for repo, score, label, _ in scores:
        score_lines.append(
            f"| {repo.name} | {repo.lane or '-'} | {repo.priority_class or '-'} | {score} | {label} | {repo.staged_count}/{repo.unstaged_count}/{repo.untracked_count} | {'yes' if repo.backlog_files else 'no'} | {'yes' if repo.sprint_files else 'no'} |"
        )
    scorecard_path.write_text("\n".join(score_lines) + "\n", encoding="utf-8")

    proposal_lines = ["# Prioritized Next Steps Proposal", ""]
    for repo, score, label, reasons in scores:
        recs = recommend_next_steps(repo, score, label, policy)
        proposal_lines.append(f"## {repo.name}")
        proposal_lines.append("")
        proposal_lines.append(f"- Readiness: **{label}** ({score}/100)")
        proposal_lines.append(f"- Evidence: `{repo.summary}` on `{repo.branch}` ({repo.head or 'n/a'})")
        proposal_lines.append("- Critical-thinking trace:")
        for reason in reasons[:4]:
            proposal_lines.append(f"  - {reason}")
        proposal_lines.append("")
        for idx, rec in enumerate(recs, start=1):
            proposal_lines.append(f"{idx}. **Action**: {rec['action']}")
            proposal_lines.append(f"   - Why now: {rec['why_now']}")
            proposal_lines.append(f"   - Risk if delayed: {rec['risk_if_delayed']}")
            proposal_lines.append(f"   - Alternatives considered: {rec['alternatives_considered']}")
        proposal_lines.append("")
    proposal_path.write_text("\n".join(proposal_lines) + "\n", encoding="utf-8")

    decision_lines = [
        "# Standup Decision Log",
        "",
        f"Generated: {now}",
        "",
        "Owner approval is required. Mark each action as `approved`, `rejected`, or `defer`, and include rationale.",
        "",
    ]
    for repo, score, label, _ in scores:
        decision_lines.append(f"## {repo.name} ({label}, {score}/100)")
        decision_lines.append("")
        for idx, rec in enumerate(recommend_next_steps(repo, score, label, policy), start=1):
            decision_lines.append(f"- Action {idx}: {rec['action']}")
            decision_lines.append("  - Decision: [approved|rejected|defer]")
            decision_lines.append("  - Owner rationale:")
            decision_lines.append("  - Owner: Melissa Stock")
            decision_lines.append("  - Due date:")
            decision_lines.append("")
    decision_log_path.write_text("\n".join(decision_lines) + "\n", encoding="utf-8")

    return {
        "summary": summary_path,
        "scorecard": scorecard_path,
        "proposal": proposal_path,
        "decision_log": decision_log_path,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PM standup readiness and recommendation loop.")
    parser.add_argument("--output-dir", help="Override output directory.")
    args = parser.parse_args()

    repos_cfg = json.loads(REPOS_CONFIG.read_text(encoding="utf-8"))
    policy = json.loads(POLICY_CONFIG.read_text(encoding="utf-8"))
    output_rel = args.output_dir or policy.get("generated_dir", "docs/session-artifacts/standup")
    output_dir = ROOT / output_rel
    output_dir.mkdir(parents=True, exist_ok=True)

    snapshots = [resolve_repo_snapshot(entry) for entry in repos_cfg["managed_repositories"]]
    artifacts = generate_reports(snapshots, policy, output_dir)

    print(f"Wrote summary: {artifacts['summary']}")
    print(f"Wrote scorecard: {artifacts['scorecard']}")
    print(f"Wrote proposal: {artifacts['proposal']}")
    print(f"Wrote decision log: {artifacts['decision_log']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
