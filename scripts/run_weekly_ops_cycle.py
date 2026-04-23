#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOV_DIR = ROOT / "docs" / "session-artifacts" / "governance"
STANDUP_DIR = ROOT / "docs" / "session-artifacts" / "standup"
TARGETS = ["provider-access-hub", "Momentum-OS", "bg-legal"]


@dataclass
class StepResult:
    name: str
    ok: bool
    command: str
    output: str


def _run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


def _short_output(text: str, limit: int = 30) -> str:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    return "\n".join(lines[:limit]) if lines else "(no output)"


def _latest_scorecard_stamp() -> str | None:
    candidates = sorted(STANDUP_DIR.glob("READINESS_SCORECARD-*.md"))
    if not candidates:
        return None
    return candidates[-1].stem.split("READINESS_SCORECARD-")[-1]


def _parse_standup_stamp(output: str) -> str | None:
    for line in output.splitlines():
        match = re.match(r"Standup stamp: (\d{8}_\d{6})", line.strip())
        if match:
            return match.group(1)
    return None


def _run_product_hardening() -> tuple[bool, str]:
    tasks = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        for target in TARGETS:
            tasks.append(
                pool.submit(
                    _run,
                    ["python3", "scripts/check_production_readiness.py", "--target", target],
                )
            )
            tasks.append(
                pool.submit(
                    _run,
                    ["python3", "scripts/validate_downstream_governance.py", "--target", target],
                )
            )

        failures = []
        details = []
        for future in as_completed(tasks):
            cp = future.result()
            cmd = " ".join(cp.args)
            ok = cp.returncode == 0
            details.append(
                f"### {'PASS' if ok else 'FAIL'}: `{cmd}`\n\n```\n{_short_output(cp.stdout + cp.stderr)}\n```"
            )
            if not ok:
                failures.append(cmd)

    return (len(failures) == 0, "\n\n".join(details))


def _write_hardening_artifact(stamp: str, body: str) -> Path:
    path = GOV_DIR / f"PRODUCT_OPS_HARDENING-{stamp}.md"
    content = (
        f"# Product Ops Hardening ({stamp})\n\n"
        f"Targets: `{', '.join(TARGETS)}`\n\n"
        f"{body}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the weekly ops cycle and publish a consolidated proof artifact."
    )
    parser.add_argument(
        "--baseline-stamp",
        help="Optional baseline standup stamp; defaults to latest existing readiness scorecard.",
    )
    parser.add_argument(
        "--auto-scaffold-bg-legal",
        action="store_true",
        help="Scaffold bg-legal delivery docs before hardening checks.",
    )
    args = parser.parse_args()

    GOV_DIR.mkdir(parents=True, exist_ok=True)
    STANDUP_DIR.mkdir(parents=True, exist_ok=True)
    cycle_stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")

    baseline_stamp = args.baseline_stamp or _latest_scorecard_stamp()
    if not baseline_stamp:
        print("No baseline standup scorecard found; pass --baseline-stamp.")
        return 1

    steps: list[StepResult] = []

    preflight = _run(
        [
            "python3",
            "-m",
            "py_compile",
            "scripts/run_start_of_day_gate.py",
            "scripts/validate_registry_artifacts.py",
            "scripts/generate_weekly_ops_memo.py",
            "scripts/scaffold_delivery_docs.py",
            "scripts/run_weekly_ops_cycle.py",
        ]
    )
    steps.append(
        StepResult(
            name="preflight",
            ok=preflight.returncode == 0,
            command="python3 -m py_compile ...",
            output=preflight.stdout + preflight.stderr,
        )
    )

    gate = _run(["python3", "scripts/run_start_of_day_gate.py"])
    steps.append(
        StepResult(
            name="start_of_day_gate",
            ok=gate.returncode == 0,
            command="python3 scripts/run_start_of_day_gate.py",
            output=gate.stdout + gate.stderr,
        )
    )

    registry = _run(["python3", "scripts/validate_registry_artifacts.py"])
    steps.append(
        StepResult(
            name="registry_validation",
            ok=registry.returncode == 0,
            command="python3 scripts/validate_registry_artifacts.py",
            output=registry.stdout + registry.stderr,
        )
    )

    if args.auto_scaffold_bg_legal:
        scaffold = _run(
            [
                "python3",
                "scripts/scaffold_delivery_docs.py",
                "--target",
                "bg-legal",
            ]
        )
        steps.append(
            StepResult(
                name="bg_legal_delivery_scaffold",
                ok=scaffold.returncode == 0,
                command="python3 scripts/scaffold_delivery_docs.py --target bg-legal",
                output=scaffold.stdout + scaffold.stderr,
            )
        )

    hardening_ok, hardening_details = _run_product_hardening()
    hardening_path = _write_hardening_artifact(cycle_stamp, hardening_details)
    steps.append(
        StepResult(
            name="product_ops_hardening",
            ok=hardening_ok,
            command="parallel readiness + downstream checks",
            output=f"Wrote {hardening_path.relative_to(ROOT)}",
        )
    )

    standup = _run(["python3", "scripts/run_pm_standup.py"])
    standup_stamp = _parse_standup_stamp(standup.stdout + standup.stderr)
    steps.append(
        StepResult(
            name="standup",
            ok=standup.returncode == 0 and standup_stamp is not None,
            command="python3 scripts/run_pm_standup.py",
            output=standup.stdout + standup.stderr,
        )
    )

    memo_ok = False
    memo_output = "memo not run"
    if standup_stamp:
        memo = _run(
            [
                "python3",
                "scripts/generate_weekly_ops_memo.py",
                "--baseline-stamp",
                baseline_stamp,
                "--current-stamp",
                standup_stamp,
            ]
        )
        memo_ok = memo.returncode == 0
        memo_output = memo.stdout + memo.stderr
    steps.append(
        StepResult(
            name="weekly_memo",
            ok=memo_ok,
            command="python3 scripts/generate_weekly_ops_memo.py --baseline-stamp ... --current-stamp ...",
            output=memo_output,
        )
    )

    overall_ok = all(step.ok for step in steps)
    report_path = GOV_DIR / f"WEEKLY_OPS_CYCLE-{cycle_stamp}.md"

    lines = [
        f"# Weekly Ops Cycle ({cycle_stamp})",
        "",
        f"Baseline stamp: `{baseline_stamp}`",
        f"Current standup stamp: `{standup_stamp or 'unknown'}`",
        "",
        f"Overall result: **{'PASS' if overall_ok else 'FAIL'}**",
        "",
        "## Step Results",
        "",
    ]

    for step in steps:
        lines.extend(
            [
                f"### {'PASS' if step.ok else 'FAIL'} - {step.name}",
                "",
                f"- command: `{step.command}`",
                "",
                "```",
                _short_output(step.output, limit=40),
                "```",
                "",
            ]
        )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {report_path.relative_to(ROOT)}")
    print(f"Overall result: {'PASS' if overall_ok else 'FAIL'}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
