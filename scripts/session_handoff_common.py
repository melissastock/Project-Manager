#!/usr/bin/env python3

import os
import re
from typing import Optional


HANDOFF_DIR = os.path.join("docs", "session-handoffs")
HANDOFF_FILE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+-handoff\.md$")


def list_handoff_files(handoff_dir: str = HANDOFF_DIR) -> list[str]:
    if not os.path.exists(handoff_dir):
        return []

    return sorted(
        [name for name in os.listdir(handoff_dir) if HANDOFF_FILE_RE.match(name)],
        reverse=True,
    )


def find_latest_handoff(handoff_dir: str = HANDOFF_DIR) -> Optional[str]:
    files = list_handoff_files(handoff_dir)
    if not files:
        return None
    return os.path.join(handoff_dir, files[0])


def read_summary(filepath: str) -> str:
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
