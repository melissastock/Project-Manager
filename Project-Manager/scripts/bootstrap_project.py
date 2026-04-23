#!/usr/bin/env python3

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "repos.json"


def slugify(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "-" for char in value.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "new-project"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def save_config(config: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content)


def build_readme(args: argparse.Namespace) -> str:
    portfolio_mode = "managed by Project Manager" if args.add_to_manifest else "standalone project"
    return (
        f"# {args.name}\n\n"
        f"{args.description}\n\n"
        "## Project Setup\n\n"
        f"- Category: {args.category}\n"
        f"- Intake stage: {args.intake_stage}\n"
        f"- Owner: {args.owner}\n"
        f"- Primary milestone: {args.milestone}\n"
        f"- Portfolio role: {args.role}\n"
        f"- Portfolio mode: {portfolio_mode}\n"
    )


def build_gitignore() -> str:
    return "\n".join(
        [
            ".DS_Store",
            "__pycache__/",
            ".pytest_cache/",
            ".venv/",
            "node_modules/",
            "dist/",
            "build/",
            "",
        ]
    )


def build_intake(args: argparse.Namespace, relative_path: str) -> str:
    stakeholders = args.stakeholders or "TBD"
    dependencies = args.external_dependencies or "TBD"
    return "\n".join(
        [
            "# New Project Intake",
            "",
            "## Basic Identity",
            "",
            f"- Project name: {args.name}",
            f"- Working directory: {relative_path}",
            f"- Repository name: {args.repo_name}",
            f"- Owner: {args.owner}",
            f"- Primary stakeholders: {stakeholders}",
            "",
            "## Purpose",
            "",
            f"- Core outcome: {args.description}",
            f"- Problem being solved: {args.problem_statement}",
            f"- Success definition: {args.success_definition}",
            f"- Deadline or milestone date: {args.milestone}",
            "",
            "## Delivery Shape",
            "",
            f"- Project type: {args.project_type}",
            f"- Main deliverables: {args.deliverables}",
            f"- Required tools or platforms: {args.tools}",
            f"- Sensitive data involved: {args.sensitive_data}",
            f"- External dependencies: {dependencies}",
            "",
            "## Git And Workspace Setup",
            "",
            f"- Repo initialized: {'yes' if args.init_git else 'no'}",
            f"- Remote created: {args.github_repo or 'not yet'}",
            "- Default branch: main",
            "- Ignore rules needed: starter .gitignore created",
            (
                "- Child repo relationship to Project Manager: tracked as independent child repository"
                if args.add_to_manifest
                else "- Child repo relationship to Project Manager: standalone repo, not added to portfolio manifest"
            ),
            "",
            "## Intake Decisions",
            "",
            f"- Category: {args.category}",
            f"- Intake stage: {args.intake_stage}",
            f"- Priority: {args.priority}",
            f"- Status cadence: {args.status_cadence}",
            f"- Notes for dashboard: {args.role}",
            "",
            "## First Moves",
            "",
            f"- First milestone: {args.milestone}",
            f"- First three setup tasks: {args.first_tasks}",
            f"- Risks or blockers: {args.risks}",
            f"- What onboarding should produce: {args.onboarding_outcome}",
            "",
        ]
    )


def add_manifest_entry(config: dict, args: argparse.Namespace, relative_path: str) -> bool:
    repos = config["managed_repositories"]
    for repo in repos:
        if repo["path"] == relative_path or repo["name"] == args.name:
            return False
    repos.append(
        {
            "name": args.name,
            "path": relative_path,
            "category": args.category,
            "role": args.role,
            "intake_stage": args.intake_stage,
        }
    )
    repos.sort(key=lambda item: item["name"].lower())
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap a new child project for the Project Manager portfolio."
    )
    parser.add_argument("--name", required=True, help="Display name for the project.")
    parser.add_argument("--path", help="Workspace-relative path. Defaults to a slug based on the name.")
    parser.add_argument("--repo-name", help="Repository name. Defaults to the path leaf.")
    parser.add_argument("--description", default="New project workspace.")
    parser.add_argument("--category", default="general")
    parser.add_argument("--role", default="new portfolio project")
    parser.add_argument("--intake-stage", default="onboarding")
    parser.add_argument("--owner", default="Melissa Stock")
    parser.add_argument("--stakeholders", default="")
    parser.add_argument("--problem-statement", default="TBD")
    parser.add_argument("--success-definition", default="TBD")
    parser.add_argument("--milestone", default="TBD")
    parser.add_argument("--project-type", default="software")
    parser.add_argument("--deliverables", default="TBD")
    parser.add_argument("--tools", default="TBD")
    parser.add_argument("--sensitive-data", default="none identified")
    parser.add_argument("--external-dependencies", default="")
    parser.add_argument("--priority", default="medium")
    parser.add_argument("--status-cadence", default="weekly")
    parser.add_argument("--first-tasks", default="1. Confirm scope 2. Create plan 3. Start setup")
    parser.add_argument("--risks", default="TBD")
    parser.add_argument("--onboarding-outcome", default="A ready-to-work repository with clear first milestone.")
    parser.add_argument("--github-repo", default="")
    parser.add_argument("--skip-git", action="store_true", help="Create files only and skip git init.")
    parser.add_argument(
        "--skip-portfolio-plan",
        action="store_true",
        help="Opt out of adding this project to the Project Manager portfolio manifest.",
    )
    parser.add_argument(
        "--add-to-manifest",
        action="store_true",
        help="Register the new repo in config/repos.json. This is the default unless --skip-portfolio-plan is used.",
    )
    parser.add_argument(
        "--initial-commit",
        action="store_true",
        help="Create an initial commit after bootstrapping the project.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.init_git = not args.skip_git
    args.add_to_manifest = not args.skip_portfolio_plan

    relative_path = args.path.strip("/") if args.path else slugify(args.name)
    repo_name = args.repo_name or Path(relative_path).name
    args.repo_name = repo_name

    project_path = ROOT / relative_path
    project_path.mkdir(parents=True, exist_ok=True)

    ensure_file(project_path / "README.md", build_readme(args))
    ensure_file(project_path / ".gitignore", build_gitignore())
    ensure_file(project_path / "docs" / "project-intake.md", build_intake(args, relative_path))

    if args.init_git and not (project_path / ".git").exists():
        run(["git", "init", "-b", "main"], cwd=project_path)

    if args.initial_commit and args.init_git:
        status = subprocess.run(
            ["git", "-C", str(project_path), "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True,
        )
        run(["git", "add", "README.md", ".gitignore", "docs/project-intake.md"], cwd=project_path)
        message = "Initialize project workspace"
        if status.returncode != 0:
            run(["git", "commit", "-m", message], cwd=project_path)
        else:
            diff = subprocess.run(
                ["git", "-C", str(project_path), "diff", "--cached", "--quiet"],
                capture_output=True,
                text=True,
            )
            if diff.returncode != 0:
                run(["git", "commit", "-m", message], cwd=project_path)

    if args.add_to_manifest:
        config = load_config()
        added = add_manifest_entry(config, args, relative_path)
        if added:
            save_config(config)

    print(f"Project path: {project_path}")
    print(f"Repo initialized: {'yes' if args.init_git else 'no'}")
    print(f"Managed by Project Manager plan: {'yes' if args.add_to_manifest else 'no'}")
    print(f"Manifest updated: {'yes' if args.add_to_manifest else 'no'}")
    print("Next: run `python3 scripts/portfolio_status.py` from the Project Manager repo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
