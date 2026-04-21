#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DECISION_RE = re.compile(r"^\s*-\s*Decision:\s*\[(approved|rejected|defer)\]\s*$")
OWNER_RE = re.compile(r"^\s*-\s*Owner:\s*(.+?)\s*$")
DUE_DATE_RE = re.compile(r"^\s*-\s*Due date:\s*(.+?)\s*$")
RATIONALE_RE = re.compile(r"^\s*-\s*Owner rationale:\s*(.+?)\s*$")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail when standup decision logs still contain placeholder decisions."
    )
    parser.add_argument(
        "--decision-log",
        required=True,
        help="Path to decision log markdown file.",
    )
    args = parser.parse_args()

    decision_log = Path(args.decision_log)
    if not decision_log.is_absolute():
        decision_log = ROOT / decision_log

    if not decision_log.exists():
        print("Decision log gate: FAIL")
        print(f"- Missing decision log: {decision_log}")
        return 1

    lines = decision_log.read_text().splitlines()
    failures: list[str] = []
    action_index = 0

    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("- Action "):
            action_index += 1
            block = lines[idx : idx + 8]
            decision_ok = any(DECISION_RE.match(item) for item in block)
            owner_ok = any(OWNER_RE.match(item) and "[approved|rejected|defer]" not in item for item in block)
            due_ok = any(DUE_DATE_RE.match(item) and not item.strip().endswith("Due date:") for item in block)
            rationale_ok = any(
                RATIONALE_RE.match(item) and not item.strip().endswith("Owner rationale:")
                for item in block
            )

            if not decision_ok:
                failures.append(f"Action {action_index}: decision not set to approved/rejected/defer.")
            if not owner_ok:
                failures.append(f"Action {action_index}: owner missing.")
            if not due_ok:
                failures.append(f"Action {action_index}: due date missing.")
            if not rationale_ok:
                failures.append(f"Action {action_index}: owner rationale missing.")

    if action_index == 0:
        failures.append("No action items detected in decision log.")

    if failures:
        print("Decision log gate: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Decision log gate: PASS")
    print("All actions have explicit decision, owner, rationale, and due date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
