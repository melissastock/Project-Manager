from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .models import Project, SignalSnapshot


def _run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo_path), *args], capture_output=True, text=True)


def _parse_porcelain(output: str) -> tuple[int, int, int]:
    staged = unstaged = untracked = 0
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


def _discover_planning_files(repo_path: Path) -> tuple[list[str], list[str]]:
    candidates = []
    docs = repo_path / "docs"
    if docs.exists():
        candidates.extend(p for p in docs.glob("*.md"))
    candidates.extend(p for p in repo_path.glob("*.md"))
    backlog = sorted(str(p.relative_to(repo_path)) for p in candidates if "backlog" in p.name.lower())
    sprint = sorted(str(p.relative_to(repo_path)) for p in candidates if "sprint" in p.name.lower())
    return backlog, sprint


def collect_snapshot(pm_root: Path, project: Project) -> SignalSnapshot:
    repo_path = pm_root / project.path
    exists = repo_path.exists()
    is_git = exists and (repo_path / ".git").exists()
    backlog_files, sprint_files = ([], [])
    if exists:
        backlog_files, sprint_files = _discover_planning_files(repo_path)

    if not is_git:
        return SignalSnapshot(
            project=project.name,
            branch="missing",
            head="",
            summary="No git repository detected",
            exists=exists,
            is_git_repo=False,
            staged_count=0,
            unstaged_count=0,
            untracked_count=0,
            backlog_files=backlog_files,
            sprint_files=sprint_files,
            captured_at=datetime.now(timezone.utc),
        )

    head_check = _run_git(repo_path, "rev-parse", "--verify", "HEAD")
    if head_check.returncode != 0:
        return SignalSnapshot(
            project=project.name,
            branch="unborn",
            head="",
            summary="Repository has no commits yet",
            exists=True,
            is_git_repo=True,
            staged_count=0,
            unstaged_count=0,
            untracked_count=0,
            backlog_files=backlog_files,
            sprint_files=sprint_files,
            captured_at=datetime.now(timezone.utc),
        )

    branch = _run_git(repo_path, "branch", "--show-current").stdout.strip() or "detached"
    head = _run_git(repo_path, "rev-parse", "--short", "HEAD").stdout.strip()
    summary = _run_git(repo_path, "log", "-1", "--pretty=%s").stdout.strip()
    porcelain = _run_git(repo_path, "status", "--porcelain").stdout
    staged_count, unstaged_count, untracked_count = _parse_porcelain(porcelain)

    ahead = behind = None
    sync = _run_git(repo_path, "rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    if sync.returncode == 0 and sync.stdout.strip():
        left, right = sync.stdout.strip().split()
        behind, ahead = int(left), int(right)

    return SignalSnapshot(
        project=project.name,
        branch=branch,
        head=head,
        summary=summary,
        exists=True,
        is_git_repo=True,
        staged_count=staged_count,
        unstaged_count=unstaged_count,
        untracked_count=untracked_count,
        ahead=ahead,
        behind=behind,
        backlog_files=backlog_files,
        sprint_files=sprint_files,
        captured_at=datetime.now(timezone.utc),
    )
