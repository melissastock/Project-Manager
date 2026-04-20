#!/usr/bin/env python3

try:
    from session_handoff_common import find_latest_handoff, read_summary
except ModuleNotFoundError:
    from scripts.session_handoff_common import find_latest_handoff, read_summary


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
