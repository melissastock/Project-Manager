#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDUP_DIR = ROOT / "docs" / "session-artifacts" / "standup"
GOV_DIR = ROOT / "docs" / "session-artifacts" / "governance"


def _latest(prefix: str, folder: Path) -> Path:
    files = sorted(folder.glob(f"{prefix}-*.md"))
    if not files:
        raise FileNotFoundError(f"No files found for {prefix}")
    return files[-1]


def _extract_drift_row(scorecard: str, project: str) -> str:
    for line in scorecard.splitlines():
        if f"| {project} |" in line:
            return line
    return ""


def _extract_result(doc: str, label: str) -> str:
    for line in doc.splitlines():
        if line.strip().startswith(label):
            return line.split("**")[-2] if "**" in line else line
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate weekly operations memo from standup/governance artifacts.")
    parser.add_argument("--baseline-stamp", required=True)
    parser.add_argument("--current-stamp", required=True)
    args = parser.parse_args()

    baseline_scorecard = (STANDUP_DIR / f"READINESS_SCORECARD-{args.baseline_stamp}.md").read_text(encoding="utf-8")
    current_scorecard = (STANDUP_DIR / f"READINESS_SCORECARD-{args.current_stamp}.md").read_text(encoding="utf-8")
    decision_log = (STANDUP_DIR / f"DECISION_LOG-{args.current_stamp}.md").read_text(encoding="utf-8")

    latest_gate = _latest("START_OF_DAY_GATE", GOV_DIR)
    latest_registry = _latest("REGISTRY_TARGET_VALIDATION", GOV_DIR)
    gate_text = latest_gate.read_text(encoding="utf-8")
    reg_text = latest_registry.read_text(encoding="utf-8")

    projects = ["provider-access-hub", "Momentum-OS", "bg-legal"]
    movement_lines = []
    for project in projects:
        before = _extract_drift_row(baseline_scorecard, project)
        after = _extract_drift_row(current_scorecard, project)
        movement_lines.append(f"- `{project}` baseline: `{before}`")
        movement_lines.append(f"- `{project}` current: `{after}`")

    unresolved = []
    in_owner_section = False
    for line in decision_log.splitlines():
        if line.strip() == "## Owner decisions required":
            in_owner_section = True
            continue
        if in_owner_section and line.startswith("## "):
            break
        if in_owner_section and line.startswith("| ") and "---" not in line and "Topic" not in line:
            unresolved.append(line)

    gate_result = _extract_result(gate_text, "Gate result:")
    registry_result = _extract_result(reg_text, "Result:")

    out = STANDUP_DIR / f"WEEKLY_OPS_MEMO-{args.current_stamp}.md"
    lines = [
        f"# Weekly Operations Proof Memo ({args.current_stamp})",
        "",
        "## Scope",
        "",
        "- Focus products: `provider-access-hub`, `Momentum-OS`, `bg-legal`.",
        f"- Baseline standup stamp: `{args.baseline_stamp}`.",
        f"- End-state standup stamp: `{args.current_stamp}`.",
        "",
        "## Reliability Controls",
        "",
        f"- Start-of-day gate: **{gate_result}** (`{latest_gate.name}`).",
        f"- Registry target validation: **{registry_result}** (`{latest_registry.name}`).",
        "",
        "## Readiness Movement (baseline -> current)",
        "",
        *movement_lines,
        "",
        "## Unresolved Owner Decisions",
        "",
        *([f"- `{line}`" for line in unresolved] if unresolved else ["- None captured in current decision log."]),
        "",
        "## Carryover Priorities",
        "",
        "- Complete OAuth/API credential rotation for keys tied to `MJS-Financial-Dash` history.",
        "- Decide and configure private remote posture for `Divorce`.",
        "- Keep daily remote/drift gate and weekly standup generation as non-skippable ops cadence.",
    ]

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
