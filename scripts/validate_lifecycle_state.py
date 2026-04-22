#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from governance_modules import (
    MODULE_COGNITIVE,
    MODULE_DOWNSTREAM,
    MODULE_LAUNCH,
    MODULE_PERSONA,
    extract_field,
    infer_modules,
    launch_required,
)


ROOT = Path(__file__).resolve().parent.parent
INTAKE_PATH = "docs/project-intake.md"
LIFECYCLE_LABEL = "Lifecycle state (`not-onboarded` / `governed` / `execution-ready` / `launch-ready` / `scaled`)"

VALID_STATES = [
    "not-onboarded",
    "governed",
    "execution-ready",
    "launch-ready",
    "scaled",
]
STATE_RANK = {state: idx for idx, state in enumerate(VALID_STATES)}

DOWNSTREAM_SCRIPT = ROOT / "scripts" / "validate_downstream_governance.py"
PRODUCTION_SCRIPT = ROOT / "scripts" / "check_production_readiness.py"
ARCH_SCRIPT = ROOT / "scripts" / "validate_architecture_scale_fit.py"
LAUNCH_SCRIPT = ROOT / "scripts" / "validate_launch_readiness.py"
PERSONA_SCRIPT = ROOT / "scripts" / "validate_persona_research_layer.py"
COGNITIVE_SCRIPT = ROOT / "scripts" / "validate_cognitive_profile_alignment.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _replace_or_insert_field(text: str, label: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(rf"(^\s*-\s*{re.escape(label)}\s*:\s*)(.*)$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    if match:
        if match.group(2).strip() == value:
            return text, False
        updated = text[: match.start(2)] + value + text[match.end(2) :]
        return updated, True

    anchor = re.search(r"^##\s+Intake Decisions\s*$", text, re.IGNORECASE | re.MULTILINE)
    if anchor:
        pos = anchor.end()
        updated = text[:pos] + f"\n\n- {label}: {value}" + text[pos:]
        return updated, True

    updated = text.rstrip() + f"\n\n## Intake Decisions\n\n- {label}: {value}\n"
    return updated, True


def _run(script: Path, target: Path) -> int:
    proc = subprocess.run(
        ["python3", str(script), "--target", str(target)],
        capture_output=True,
        text=True,
    )
    return proc.returncode


def _recommended_state(target: Path, intake_text: str) -> tuple[str, dict[str, bool]]:
    active_modules = infer_modules({}, intake_text)

    downstream_required = MODULE_DOWNSTREAM in active_modules
    persona_required = MODULE_PERSONA in active_modules
    cognitive_required = MODULE_COGNITIVE in active_modules
    launch_module_enabled = MODULE_LAUNCH in active_modules

    downstream_ok = (_run(DOWNSTREAM_SCRIPT, target) == 0) if downstream_required else True
    production_ok = _run(PRODUCTION_SCRIPT, target) == 0
    arch_ok = _run(ARCH_SCRIPT, target) == 0
    persona_ok = (_run(PERSONA_SCRIPT, target) == 0) if persona_required else True
    cognitive_ok = (_run(COGNITIVE_SCRIPT, target) == 0) if cognitive_required else True
    launch_required_gate = launch_module_enabled and launch_required(intake_text)
    launch_ok = (_run(LAUNCH_SCRIPT, target) == 0) if launch_required_gate else True

    execution_ok = production_ok and arch_ok and downstream_ok and persona_ok and cognitive_ok

    if not downstream_ok:
        state = "not-onboarded"
    elif not execution_ok:
        state = "governed"
    elif launch_required_gate and launch_ok:
        state = "launch-ready"
    elif execution_ok:
        state = "execution-ready"
    else:
        state = "governed"

    return state, {
        "active_modules": ",".join(sorted(active_modules)),
        "downstream_required": downstream_required,
        "downstream_ok": downstream_ok,
        "production_ok": production_ok,
        "arch_ok": arch_ok,
        "persona_required": persona_required,
        "persona_ok": persona_ok,
        "cognitive_required": cognitive_required,
        "cognitive_ok": cognitive_ok,
        "launch_required": launch_required_gate,
        "launch_ok": launch_ok,
        "execution_ok": execution_ok,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate lifecycle state against governance/execution/launch gates."
    )
    parser.add_argument("--target", required=True, help="Target project path to validate.")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-set lifecycle state to the highest valid state based on current gates.",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target

    intake_file = target / INTAKE_PATH
    intake_text = _read(intake_file)
    if not intake_text:
        print("Lifecycle state: FAIL")
        print(f"- Missing required intake file: {INTAKE_PATH}")
        return 1

    declared = extract_field(intake_text, LIFECYCLE_LABEL).strip().lower()
    recommended, gate_info = _recommended_state(target, intake_text)

    if declared == "scaled":
        if not gate_info["execution_ok"]:
            if args.fix:
                updated, changed = _replace_or_insert_field(intake_text, LIFECYCLE_LABEL, recommended)
                if changed:
                    intake_file.write_text(updated, encoding="utf-8")
                print("Lifecycle state: FIXED")
                print(f"- Updated lifecycle state to `{recommended}` based on gate results.")
                return 0
            print("Lifecycle state: FAIL")
            print("- `scaled` requires all execution gates to pass.")
            return 1
        print("Lifecycle state: PASS")
        print("Lifecycle state is valid (`scaled`) and required gates pass.")
        return 0

    if declared not in VALID_STATES:
        if args.fix:
            updated, changed = _replace_or_insert_field(intake_text, LIFECYCLE_LABEL, recommended)
            if changed:
                intake_file.write_text(updated, encoding="utf-8")
            print("Lifecycle state: FIXED")
            print(f"- Set lifecycle state to `{recommended}`.")
            return 0
        print("Lifecycle state: FAIL")
        print("- Missing or invalid lifecycle state in intake.")
        print(f"- Expected one of: {', '.join(VALID_STATES)}")
        return 1

    if STATE_RANK[declared] > STATE_RANK[recommended]:
        if args.fix:
            updated, changed = _replace_or_insert_field(intake_text, LIFECYCLE_LABEL, recommended)
            if changed:
                intake_file.write_text(updated, encoding="utf-8")
            print("Lifecycle state: FIXED")
            print(f"- Downgraded lifecycle state from `{declared}` to `{recommended}` based on gate results.")
            return 0
        print("Lifecycle state: FAIL")
        print(f"- Declared lifecycle state `{declared}` exceeds current gate-valid state `{recommended}`.")
        return 1

    print("Lifecycle state: PASS")
    print(f"Declared lifecycle state `{declared}` is valid for current gate results (max: `{recommended}`).")
    print(f"Active modules: {gate_info['active_modules']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
