#!/usr/bin/env python3

import json
import os
import subprocess

REPOS_FILE = os.path.join("config", "repos.json")
STATUS_FILE = "STATUS.md"
REVIEW_GATES_FILE = os.path.join("docs", "REVIEW_GATES.md")
PR_CHECKLIST_FILE = os.path.join("docs", "pr-prep-checklist.md")
PUBLICATION_REVIEW_DIR = "docs"

try:
    from session_handoff_common import find_latest_handoff, read_summary
except ModuleNotFoundError:
    from scripts.session_handoff_common import find_latest_handoff, read_summary


def run_cmd(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        return result.decode("utf-8").strip()
    except Exception:
        return None


def get_git_context():
    branch = run_cmd("git rev-parse --abbrev-ref HEAD")
    status = run_cmd("git status --short")
    commits = run_cmd("git log -5 --oneline")
    return branch, status, commits


def read_file(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return f.read()


def check_pm_sync():
    notes = []

    repos_raw = read_file(REPOS_FILE)
    status_raw = read_file(STATUS_FILE)

    if repos_raw is None:
        notes.append("Missing config/repos.json")
        return notes

    if status_raw is None:
        notes.append("Missing STATUS.md")
        return notes

    try:
        repos = json.loads(repos_raw)
        managed = repos.get("managed_repositories", [])
        managed_names = [item.get("name", "") for item in managed]
    except Exception:
        notes.append("Could not parse config/repos.json")
        return notes

    if "Generated:" not in status_raw:
        notes.append("STATUS.md does not look like a generated portfolio file")

    for name in managed_names:
        if name and name not in status_raw:
            notes.append(f"Managed repo missing from STATUS.md: {name}")

    onboarding_count = sum(1 for item in managed if item.get("intake_stage") == "onboarding")
    archive_count = sum(1 for item in managed if item.get("intake_stage") == "archive")

    notes.append(f"Managed repositories in repos.json: {len(managed_names)}")
    notes.append(f"Onboarding repositories in repos.json: {onboarding_count}")
    notes.append(f"Archive repositories in repos.json: {archive_count}")

    return notes


def latest_publication_review():
    if not os.path.exists(PUBLICATION_REVIEW_DIR):
        return None

    files = sorted(
        [
            name
            for name in os.listdir(PUBLICATION_REVIEW_DIR)
            if name.startswith("publication-review-") and name.endswith(".md")
        ],
        reverse=True,
    )
    if not files:
        return None
    return os.path.join(PUBLICATION_REVIEW_DIR, files[0])


def check_review_gates():
    notes = []

    if not os.path.exists(REVIEW_GATES_FILE):
        notes.append("Missing docs/REVIEW_GATES.md")

    if not os.path.exists(PR_CHECKLIST_FILE):
        notes.append("Missing docs/pr-prep-checklist.md")

    publication_review = latest_publication_review()
    if publication_review:
        notes.append(f"Latest publication review: {publication_review}")
    else:
        notes.append("No publication review file found in docs/")

    notes.append("Review gates required: code review, QC / validation, governance / legal / privacy")
    return notes


def main():
    print("\n=== SESSION OPEN (PM SYNC AWARE) ===\n")

    latest = find_latest_handoff()
    if not latest:
        print("No handoff files found. Starting without prior session context.\n")
    else:
        print(f"Latest handoff: {latest}\n")
        summary = read_summary(latest)
        print("--- PM-READY SUMMARY ---\n")
        print(summary if summary else "(No summary found)")
        print("\n------------------------\n")

    branch, status, commits = get_git_context()

    print("--- GIT CONTEXT ---\n")
    print(f"Branch: {branch or 'unknown'}\n")
    print("Recent commits:")
    print(commits or "(no commits found)")
    print("\nWorking tree status:")
    print(status or "clean")
    print("\n-------------------\n")

    if status:
        print("WARNING: Uncommitted changes detected. Verify alignment with handoff.\n")

    print("--- PM SYNC CHECK ---\n")
    sync_notes = check_pm_sync()
    for note in sync_notes:
        print(f"- {note}")
    print("\n---------------------\n")

    print("--- REVIEW GATE CHECK ---\n")
    review_notes = check_review_gates()
    for note in review_notes:
        print(f"- {note}")
    print("\n-------------------------\n")

    print("Define your session:\n")
    objective = input("Session Objective: ")
    success = input("Success Criteria: ")

    print("\n=== SESSION START CONTEXT ===\n")
    print(f"Objective: {objective}")
    print(f"Success Criteria: {success}")

    print("\nReminder:")
    print("- Verify facts against commits/files before acting")
    print("- Do not assume handoff accuracy without validation")
    print("- If PM sync notes show drift, account for that in this session")
    print("- No PR is greenlit until code review, QC, and compliance checks are complete")

    print("\nNow proceed with work.\n")


if __name__ == "__main__":
    main()
