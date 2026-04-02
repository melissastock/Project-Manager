#!/usr/bin/env python3

import os
from datetime import datetime

HANDOFF_DIR = os.path.join("docs", "session-handoffs")


def find_latest_handoff():
    if not os.path.exists(HANDOFF_DIR):
        return None

    files = [f for f in os.listdir(HANDOFF_DIR) if f.endswith(".md")]
    if not files:
        return None

    files.sort(reverse=True)
    return os.path.join(HANDOFF_DIR, files[0])


def read_summary(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    summary = []
    capture = False

    for line in lines:
        if "PM-Ready Summary" in line:
            capture = True
            continue
        if capture and line.startswith("---"):
            break
        if capture:
            summary.append(line.rstrip())

    return "\n".join(summary).strip()


def main():
    print("\n=== SESSION OPEN ===\n")

    latest = find_latest_handoff()

    if not latest:
        print("No handoff files found. Starting without prior session context.\n")
    else:
        print(f"Latest handoff: {latest}\n")
        summary = read_summary(latest)

        print("--- PM-READY SUMMARY ---\n")
        print(summary if summary else "(No summary found)")
        print("\n------------------------\n")

    print("Define your session:\n")

    objective = input("Session Objective: ")
    success = input("Success Criteria: ")

    print("\n=== SESSION START CONTEXT ===\n")
    print(f"Objective: {objective}")
    print(f"Success Criteria: {success}")
    print("\nNow proceed with work.\n")


if __name__ == "__main__":
    main()
