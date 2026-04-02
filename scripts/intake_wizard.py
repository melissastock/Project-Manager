#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BOOTSTRAP_SCRIPT = ROOT / "scripts" / "bootstrap_project.py"


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def flag(value: bool) -> str:
    return "yes" if value else "no"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactive wrapper for bootstrapping a new Project Manager child repo."
    )
    parser.add_argument("--name", default="")
    parser.add_argument("--path", default="")
    parser.add_argument("--category", default="general")
    parser.add_argument("--role", default="new portfolio project")
    parser.add_argument("--description", default="New project workspace.")
    parser.add_argument("--owner", default="Melissa Stock")
    parser.add_argument("--milestone", default="TBD")
    parser.add_argument("--intake-stage", default="onboarding")
    parser.add_argument("--project-type", default="software")
    parser.add_argument("--priority", default="medium")
    parser.add_argument("--status-cadence", default="weekly")
    parser.add_argument("--initial-commit", action="store_true")
    parser.add_argument("--skip-portfolio-plan", action="store_true")
    parser.add_argument("--skip-git", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("Project intake wizard")
    print("")

    name = prompt("Project name", args.name)
    if not name:
        print("Project name is required.", file=sys.stderr)
        return 1

    path = prompt("Workspace-relative path", args.path)
    description = prompt("Short description", args.description)
    role = prompt("Portfolio role", args.role)
    category = prompt("Category", args.category)
    owner = prompt("Owner", args.owner)
    milestone = prompt("First milestone", args.milestone)
    intake_stage = prompt("Intake stage", args.intake_stage)
    project_type = prompt("Project type", args.project_type)
    priority = prompt("Priority", args.priority)
    status_cadence = prompt("Status cadence", args.status_cadence)
    add_to_manifest = prompt(
        "Manage this repo from the Project Manager plan", "yes" if not args.skip_portfolio_plan else "no"
    ).lower() in {"y", "yes"}
    init_git = not args.skip_git
    initial_commit = args.initial_commit

    print("")
    print("Planned setup")
    print(f"- Name: {name}")
    print(f"- Path: {path or '(slug from name)'}")
    print(f"- Category: {category}")
    print(f"- Role: {role}")
    print(f"- Intake stage: {intake_stage}")
    print(f"- Git init: {flag(init_git)}")
    print(f"- Managed by Project Manager plan: {flag(add_to_manifest)}")
    print(f"- Initial commit: {flag(initial_commit)}")
    print("")

    confirm = prompt("Proceed", "yes").lower()
    if confirm not in {"y", "yes"}:
        print("Cancelled.")
        return 0

    cmd = [
        sys.executable,
        str(BOOTSTRAP_SCRIPT),
        "--name",
        name,
        "--description",
        description,
        "--role",
        role,
        "--category",
        category,
        "--owner",
        owner,
        "--milestone",
        milestone,
        "--intake-stage",
        intake_stage,
        "--project-type",
        project_type,
        "--priority",
        priority,
        "--status-cadence",
        status_cadence,
    ]

    if path:
        cmd.extend(["--path", path])
    if add_to_manifest:
        cmd.append("--add-to-manifest")
    else:
        cmd.append("--skip-portfolio-plan")
    if initial_commit:
        cmd.append("--initial-commit")
    if not init_git:
        cmd.append("--skip-git")

    subprocess.run(cmd, cwd=ROOT, check=True)
    print("")
    print("Next step: run `python3 scripts/portfolio_status.py` from Project Manager to refresh the dashboard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
