#!/usr/bin/env python3

import subprocess

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


def main():
    print("\n=== SESSION OPEN (ENHANCED) ===\n")

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

    print("Define your session:\n")

    objective = input("Session Objective: ")
    success = input("Success Criteria: ")

    print("\n=== SESSION START CONTEXT ===\n")
    print(f"Objective: {objective}")
    print(f"Success Criteria: {success}")

    print("\nReminder:")
    print("- Verify facts against commits/files before acting")
    print("- Do not assume handoff accuracy without validation")

    print("\nNow proceed with work.\n")


if __name__ == "__main__":
    main()
