#!/usr/bin/env python3
"""Run start-of-day execution gate: remote audit + drift classification."""

from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOV_DIR = ROOT / "docs" / "session-artifacts" / "governance"
BASELINE_FILE = ROOT / "config" / "drift-baseline.json"
TARGET_REPOS = {
    "provider-access-hub": ROOT / "provider-access-hub",
    "Momentum-OS": ROOT / "Momentum-OS",
    "bg-legal": ROOT / "bg-legal",
}
ALLOWED_GENERATED = {
    "data/os_registry_snapshot.json",
    "data/files_manifest.json",
    "data/assets/README.md",
}


def _run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def _parse_remote_audit(output: str) -> dict[str, int]:
    counts = {"ok": 0, "needs_update": 0, "missing_binding": 0, "missing_remote_key": 0, "errors": 0}
    for line in output.splitlines():
        if line.startswith("[ok]"):
            counts["ok"] += 1
        elif line.startswith("[needs-update"):
            counts["needs_update"] += 1
        elif line.startswith("[missing-binding]"):
            counts["missing_binding"] += 1
        elif line.startswith("[missing-remote-key]"):
            counts["missing_remote_key"] += 1
        elif line.startswith("[error"):
            counts["errors"] += 1
    return counts


def _classify_drift(repo_path: Path) -> tuple[list[str], list[str]]:
    cp = _run(["git", "status", "--porcelain"], cwd=repo_path)
    if cp.returncode != 0:
        return [], [f"git status failed: {cp.stderr.strip()}"]
    allowed = []
    blocked = []
    for line in cp.stdout.splitlines():
        if not line.strip():
            continue
        rel = line[3:].strip()
        if rel in ALLOWED_GENERATED:
            allowed.append(line)
        else:
            blocked.append(line)
    return allowed, blocked


def _load_baseline() -> dict[str, list[str]]:
    if not BASELINE_FILE.exists():
        return {}
    try:
        payload = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload.get("allowed_drift_by_repo", {})


def main() -> int:
    stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    human = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    GOV_DIR.mkdir(parents=True, exist_ok=True)
    report_path = GOV_DIR / f"START_OF_DAY_GATE-{stamp}.md"

    remote = _run(["python3", "scripts/sync_repo_remotes.py"], cwd=ROOT)
    remote_counts = _parse_remote_audit(remote.stdout)

    standup = _run(["python3", "scripts/run_pm_standup.py"], cwd=ROOT)
    standup_stamp = "unknown"
    for line in standup.stdout.splitlines():
        m = re.match(r"Standup stamp: (\d{8}_\d{6})", line.strip())
        if m:
            standup_stamp = m.group(1)
            break

    baseline = _load_baseline()
    drift_section = []
    blocked_total = 0
    unexpected_total = 0
    for name, repo in TARGET_REPOS.items():
        allowed, blocked = _classify_drift(repo)
        baseline_paths = set(baseline.get(name, []))
        expected = []
        unexpected = []
        for item in blocked:
            rel = item[3:].strip()
            if rel in baseline_paths:
                expected.append(item)
            else:
                unexpected.append(item)
        blocked_total += len(blocked)
        unexpected_total += len(unexpected)
        drift_section.append(f"### {name}")
        drift_section.append("")
        drift_section.append(f"- allowed_generated_changes: {len(allowed)}")
        drift_section.append(f"- blocked_changes: {len(blocked)}")
        drift_section.append(f"- baseline_expected_changes: {len(expected)}")
        drift_section.append(f"- unexpected_changes: {len(unexpected)}")
        if unexpected:
            drift_section.append("- unexpected_entries:")
            drift_section.extend([f"  - `{item}`" for item in unexpected[:20]])
        drift_section.append("")

    gate_pass = (
        remote.returncode == 0
        and remote_counts["needs_update"] == 0
        and remote_counts["missing_binding"] == 0
        and remote_counts["missing_remote_key"] == 0
        and remote_counts["errors"] == 0
        and standup.returncode == 0
        and unexpected_total == 0
    )

    lines = [
        f"# Start-of-Day Gate ({stamp})",
        "",
        f"Generated: {human}",
        "",
        f"Gate result: **{'PASS' if gate_pass else 'FAIL'}**",
        "",
        "## Remote audit",
        "",
        f"- ok: {remote_counts['ok']}",
        f"- needs_update: {remote_counts['needs_update']}",
        f"- missing_binding: {remote_counts['missing_binding']}",
        f"- missing_remote_key: {remote_counts['missing_remote_key']}",
        f"- errors: {remote_counts['errors']}",
        "",
        "## Standup refresh",
        "",
        f"- status: {'PASS' if standup.returncode == 0 else 'FAIL'}",
        f"- standup_stamp: {standup_stamp}",
        "",
        "## Target drift classification",
        "",
        *drift_section,
        "## Enforcement",
        "",
        "- Block product execution if remote audit has any `needs_update`, `missing_binding`, or `missing_remote_key`.",
        "- Block multi-repo commit/push if target repos contain drift outside `config/drift-baseline.json`.",
    ]

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {report_path.relative_to(ROOT)}")
    print(f"Gate result: {'PASS' if gate_pass else 'FAIL'}")
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
