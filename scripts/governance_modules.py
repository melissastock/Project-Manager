from __future__ import annotations

import re
from pathlib import Path


MODULE_CORE_READINESS = "core-readiness"
MODULE_LIFECYCLE = "lifecycle-state"
MODULE_DOWNSTREAM = "downstream-governance"
MODULE_PERSONA = "persona-research"
MODULE_LAUNCH = "launch-readiness"

ALWAYS_ENABLED_MODULES = {MODULE_CORE_READINESS, MODULE_LIFECYCLE}
KNOWN_MODULES = ALWAYS_ENABLED_MODULES | {MODULE_DOWNSTREAM, MODULE_PERSONA, MODULE_LAUNCH}

LAUNCH_FLAGS = [
    "Launch-proximal commercialization plan required",
    "Launch-proximal marketing plan required",
    "Launch-proximal operationalization SOP set required",
]


def read_intake(repo_path: Path, intake_rel: str = "docs/project-intake.md") -> str:
    intake_path = repo_path / intake_rel
    if not intake_path.exists():
        return ""
    return intake_path.read_text(encoding="utf-8")


def extract_field(text: str, label: str) -> str:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}\s*:\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def launch_required(intake_text: str) -> bool:
    for label in LAUNCH_FLAGS:
        value = extract_field(intake_text, label).lower()
        if value in {"yes", "y", "true", "required", "1"}:
            return True
    return False


def parse_enabled_modules(value: str) -> set[str]:
    if not value:
        return set()
    modules: set[str] = set()
    for part in value.split(","):
        token = part.strip().lower()
        if token in KNOWN_MODULES:
            modules.add(token)
    return modules


def infer_modules(entry: dict, intake_text: str) -> set[str]:
    modules = set(ALWAYS_ENABLED_MODULES)

    explicit = parse_enabled_modules(extract_field(intake_text, "Enabled modules"))
    if explicit:
        return modules | explicit

    cfg_modules = entry.get("enabled_modules", [])
    if isinstance(cfg_modules, list):
        for item in cfg_modules:
            token = str(item).strip().lower()
            if token in KNOWN_MODULES:
                modules.add(token)

    if extract_field(intake_text, "Project type") or extract_field(intake_text, "Downstream governance profile"):
        modules.add(MODULE_DOWNSTREAM)

    if extract_field(intake_text, "Primary user persona") or extract_field(
        intake_text, "Portfolio orientation (`horizontal` / `vertical`)"
    ):
        modules.add(MODULE_PERSONA)

    if launch_required(intake_text):
        modules.add(MODULE_LAUNCH)

    return modules
