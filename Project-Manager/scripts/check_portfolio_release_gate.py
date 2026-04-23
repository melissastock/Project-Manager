#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PM_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> tuple[int, str]:
    result = subprocess.run(command, cwd=PM_ROOT, capture_output=True, text=True)
    output = (result.stdout or "").strip()
    error = (result.stderr or "").strip()
    if error:
        output = f"{output}\n{error}".strip()
    return result.returncode, output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run consolidated portfolio release gate checks."
    )
    parser.add_argument("--target", required=True, help="Target project path to validate.")
    parser.add_argument(
        "--decision-log",
        help="Optional decision log path to enforce owner decision completeness.",
    )
    args = parser.parse_args()

    checks: list[tuple[str, list[str]]] = [
        (
            "Production readiness",
            ["python3", "scripts/check_production_readiness.py", "--target", args.target],
        ),
        (
            "Packaged output",
            ["python3", "scripts/check_packaged_output.py", "--target", args.target],
        ),
        ("Review gate", ["python3", "scripts/review_gate.py"]),
        ("Remote collision safety", ["python3", "scripts/check_remote_collisions.py"]),
    ]

    if args.decision_log:
        checks.append(
            (
                "Decision log completeness",
                [
                    "python3",
                    "scripts/check_decision_log_completeness.py",
                    "--decision-log",
                    args.decision_log,
                ],
            )
        )

    failures: list[str] = []

    for title, command in checks:
        code, output = run(command)
        status = "PASS" if code == 0 else "FAIL"
        print(f"[{status}] {title}")
        if output:
            print(output)
        print("")
        if code != 0:
            failures.append(title)

    if failures:
        print("Portfolio release gate: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Portfolio release gate: PASS")
    print("All configured release checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
