#!/usr/bin/env python3

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PM_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PM_ROOT / "config" / "repos.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def save_config(config: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def write_if_missing(path: Path, content: str, overwrite: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite or not path.exists():
        path.write_text(content)
        return True
    return False


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
            f"- Working directory: {ROOT / relative_path}",
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
                else "- Child repo relationship to Project Manager: standalone project folder, not added to portfolio manifest"
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


def upsert_manifest_entry(config: dict, args: argparse.Namespace, relative_path: str) -> str:
    repos = config["managed_repositories"]
    for repo in repos:
        if repo["path"] == relative_path or repo["name"] == args.name:
            repo.update(
                {
                    "name": args.name,
                    "path": relative_path,
                    "category": args.category,
                    "role": args.role,
                    "intake_stage": args.intake_stage,
                }
            )
            repos.sort(key=lambda item: item["name"].lower())
            return "updated"

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
    return "added"


def refresh_status() -> Path:
    try:
        from scripts import portfolio_status
    except ImportError:
        import portfolio_status  # type: ignore

    config = load_config()
    portfolio_status.ROOT = ROOT
    statuses = [portfolio_status.get_repo_status(entry) for entry in config["managed_repositories"]]
    output_path = ROOT / config.get("generated_status_file", "STATUS.md")
    output_path.write_text(portfolio_status.build_markdown(statuses))
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Onboard an existing Project Manager folder into the standard intake/onboarding flow."
    )
    parser.add_argument("--name", required=True, help="Display name for the project.")
    parser.add_argument("--path", required=True, help="Workspace-relative path to an existing project folder.")
    parser.add_argument("--repo-name", help="Repository name. Defaults to the path leaf.")
    parser.add_argument("--description", default="Existing project workspace.")
    parser.add_argument("--category", default="general")
    parser.add_argument("--role", default="managed portfolio project")
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
    parser.add_argument("--onboarding-outcome", default="A ready-to-work project home with clear next steps.")
    parser.add_argument("--github-repo", default="")
    parser.add_argument("--skip-git", action="store_true", help="Skip git initialization if the folder is not meant to be a repo.")
    parser.add_argument("--initial-commit", action="store_true", help="Create an initial commit for the onboarding docs.")
    parser.add_argument(
        "--commit-all-files",
        action="store_true",
        help="When creating the initial commit, stage the full existing project folder instead of only generated onboarding files.",
    )
    parser.add_argument("--overwrite-docs", action="store_true", help="Overwrite README and intake docs if they already exist.")
    parser.add_argument(
        "--skip-portfolio-plan",
        action="store_true",
        help="Keep the folder standalone instead of registering it in the portfolio manifest.",
    )
    parser.add_argument(
        "--skip-refresh-status",
        action="store_true",
        help="Skip regenerating STATUS.md after onboarding.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.init_git = not args.skip_git
    args.add_to_manifest = not args.skip_portfolio_plan

    relative_path = args.path.strip("/")
    project_path = ROOT / relative_path
    if not project_path.exists() or not project_path.is_dir():
        raise SystemExit(f"Existing project folder not found: {project_path}")

    args.repo_name = args.repo_name or project_path.name

    changed_files: list[Path] = []
    if write_if_missing(project_path / "README.md", build_readme(args), overwrite=args.overwrite_docs):
        changed_files.append(project_path / "README.md")
    if write_if_missing(project_path / ".gitignore", build_gitignore(), overwrite=args.overwrite_docs):
        changed_files.append(project_path / ".gitignore")
    if write_if_missing(
        project_path / "docs" / "project-intake.md",
        build_intake(args, relative_path),
        overwrite=args.overwrite_docs,
    ):
        changed_files.append(project_path / "docs" / "project-intake.md")

    git_initialized = False
    if args.init_git and not (project_path / ".git").exists():
        run(["git", "init", "-b", "main"], cwd=project_path)
        git_initialized = True

    manifest_state = "skipped"
    if args.add_to_manifest:
        config = load_config()
        manifest_state = upsert_manifest_entry(config, args, relative_path)
        save_config(config)

    commit_created = False
    if args.initial_commit and args.init_git and (project_path / ".git").exists():
        status = subprocess.run(
            ["git", "-C", str(project_path), "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True,
        )
        if args.commit_all_files:
            run(["git", "add", "."], cwd=project_path)
        else:
            files_to_add = [path.relative_to(project_path).as_posix() for path in changed_files]
            if files_to_add:
                run(["git", "add", *files_to_add], cwd=project_path)
        if args.commit_all_files or changed_files:
            diff = subprocess.run(
                ["git", "-C", str(project_path), "diff", "--cached", "--quiet"],
                capture_output=True,
                text=True,
            )
            if status.returncode != 0 or diff.returncode != 0:
                run(["git", "commit", "-m", "Initialize project onboarding"], cwd=project_path)
                commit_created = True

    refreshed_status = None
    if not args.skip_refresh_status:
        refreshed_status = refresh_status()

    print(f"Project path: {project_path}")
    print(f"Repo initialized this run: {'yes' if git_initialized else 'no'}")
    print(f"Manifest change: {manifest_state}")
    print(f"Created onboarding files: {len(changed_files)}")
    print(f"Initial commit created: {'yes' if commit_created else 'no'}")
    if refreshed_status:
        print(f"Status refreshed: {refreshed_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
