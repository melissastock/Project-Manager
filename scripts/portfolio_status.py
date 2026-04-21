#!/usr/bin/env python3

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "repos.json"


@dataclass
class RepoStatus:
    name: str
    path: str
    category: str
    lane: str
    priority_class: str
    role: str
    intake_stage: str
    exists: bool
    is_git_repo: bool
    has_commits: bool
    branch: str
    head: str
    summary: str
    extra_note: str
    dirty: bool
    staged_count: int
    unstaged_count: int
    untracked_count: int
    ahead: Optional[int]
    behind: Optional[int]


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


def ahead_behind(repo_path: Path) -> tuple[Optional[int], Optional[int]]:
    result = run_git(repo_path, "rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    if result.returncode != 0:
        return None, None
    left, right = result.stdout.strip().split()
    behind = int(left)
    ahead = int(right)
    return ahead, behind


def get_repo_status(entry: dict) -> RepoStatus:
    repo_path = ROOT / entry["path"]
    exists = repo_path.exists()
    git_dir = repo_path / ".git"
    is_git_repo = exists and git_dir.exists()

    default = RepoStatus(
        name=entry["name"],
        path=entry["path"],
        category=entry.get("category", ""),
        lane=entry.get("lane", ""),
        priority_class=entry.get("priority_class", ""),
        role=entry.get("role", ""),
        intake_stage=entry.get("intake_stage", ""),
        exists=exists,
        is_git_repo=is_git_repo,
        has_commits=False,
        branch="missing",
        head="",
        summary="No repository found",
        extra_note="",
        dirty=False,
        staged_count=0,
        unstaged_count=0,
        untracked_count=0,
        ahead=None,
        behind=None,
    )
    if exists and not is_git_repo:
        default.branch = "not-initialized"
        default.summary = "Folder exists but is not initialized as a git repository"
        return default
    if not is_git_repo:
        return default

    head_check = run_git(repo_path, "rev-parse", "--verify", "HEAD")
    if head_check.returncode != 0:
        default.branch = "unborn"
        default.summary = "Repository exists but has no commits yet"
        return default

    branch = run_git(repo_path, "branch", "--show-current").stdout.strip() or "detached"
    head = run_git(repo_path, "rev-parse", "--short", "HEAD").stdout.strip()
    summary = run_git(repo_path, "log", "-1", "--pretty=%s").stdout.strip()
    extra_bits: list[str] = []
    if entry.get("portfolio_parent"):
        extra_bits.append(f"parent {entry['portfolio_parent']}")
    if entry.get("github_repo_slug"):
        extra_bits.append(f"GitHub {entry['github_repo_slug']} (private)")
    extra_note = "; ".join(extra_bits)
    porcelain = run_git(repo_path, "status", "--porcelain").stdout
    staged_count, unstaged_count, untracked_count = parse_porcelain(porcelain)
    ahead, behind = ahead_behind(repo_path)

    return RepoStatus(
        name=entry["name"],
        path=entry["path"],
        category=entry.get("category", ""),
        lane=entry.get("lane", ""),
        priority_class=entry.get("priority_class", ""),
        role=entry.get("role", ""),
        intake_stage=entry.get("intake_stage", ""),
        exists=True,
        is_git_repo=True,
        has_commits=True,
        branch=branch,
        head=head,
        summary=summary,
        extra_note=extra_note,
        dirty=bool(porcelain.strip()),
        staged_count=staged_count,
        unstaged_count=unstaged_count,
        untracked_count=untracked_count,
        ahead=ahead,
        behind=behind,
    )


def build_markdown(statuses: list[RepoStatus]) -> str:
    generated_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    total = len(statuses)
    dirty = sum(1 for repo in statuses if repo.dirty)
    clean = sum(1 for repo in statuses if repo.has_commits and not repo.dirty)
    onboarding = sum(1 for repo in statuses if repo.intake_stage == "onboarding")

    lines = [
        "# Portfolio Status",
        "",
        f"Generated: {generated_at}",
        "",
        "## Summary",
        "",
        f"- Managed repositories: {total}",
        f"- Clean repositories: {clean}",
        f"- Repositories with local changes: {dirty}",
        f"- Repositories in onboarding: {onboarding}",
        "",
        "## Repository Snapshot",
        "",
        "| Project | Lane | Priority | Stage | Branch | Status | Sync | Head | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for repo in statuses:
        if not repo.exists:
            status_text = "missing"
            sync_text = "-"
            head_text = "-"
        elif not repo.has_commits:
            status_text = "unborn"
            sync_text = "-"
            head_text = "-"
        else:
            counts = []
            if repo.staged_count:
                counts.append(f"staged:{repo.staged_count}")
            if repo.unstaged_count:
                counts.append(f"unstaged:{repo.unstaged_count}")
            if repo.untracked_count:
                counts.append(f"untracked:{repo.untracked_count}")
            status_text = "clean" if not counts else ", ".join(counts)
            if repo.ahead is None and repo.behind is None:
                sync_text = "no-upstream"
            else:
                sync_text = f"ahead:{repo.ahead} behind:{repo.behind}"
            head_text = repo.head

        notes = repo.summary
        if repo.extra_note:
            notes = f"{repo.summary}; {repo.extra_note}"
        lines.append(
            f"| {repo.name} | {repo.lane or '-'} | {repo.priority_class or '-'} | {repo.intake_stage} | {repo.branch} | {status_text} | {sync_text} | {head_text} | {notes} |"
        )

    lines.extend(
        [
            "",
            "## Intake And Onboarding",
            "",
            "Use this repo as the portfolio control plane:",
            "",
            "- Create a new project intake doc from `docs/new-project-intake-template.md`.",
            "- Add the new repo to `config/repos.json` once the location and role are confirmed.",
            "- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.",
            "- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    config = json.loads(CONFIG_PATH.read_text())
    statuses = [get_repo_status(entry) for entry in config["managed_repositories"]]
    output_path = ROOT / config.get("generated_status_file", "STATUS.md")
    output_path.write_text(build_markdown(statuses))
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
