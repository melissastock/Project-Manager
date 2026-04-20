#!/usr/bin/env python3

from datetime import datetime
import os
import re
from typing import Optional

try:
    from session_handoff_common import HANDOFF_DIR
except ModuleNotFoundError:
    from scripts.session_handoff_common import HANDOFF_DIR

PROJECT_NAME_RE = re.compile(r"[^a-z0-9-]+")


def normalize_project_name(value: str) -> str:
    normalized = value.strip().lower().replace(" ", "-")
    normalized = PROJECT_NAME_RE.sub("-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized


def build_handoff_filename(project_name: str, now: Optional[datetime] = None) -> str:
    current_time = now or datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")
    return f"{date_str}-{project_name}-handoff.md"


def build_handoff_template(date_str: str) -> str:
    return f"""# Developer Session Handoff

Date: {date_str}
Developer: Codex
Repo(s): 
Branch(es): 

---

# PM-Ready Summary (Read This First)

## What Changed (Facts Only)
- 

## Current State
- Project status:
- Phase:
- Priority shift (if any):

## Blockers / Risks
- 

## Top Next Actions
1. 
2. 
3. 

---

# Evidence Log (Source of Truth)

## Commits Made
| Repo | Branch | Commit SHA | Message |
|------|--------|-----------|--------|

## Files Changed
- Created:
- Updated:
- Deleted / Deprecated:

## Commands / Scripts Run
- 

---

# Fact vs Interpretation

## Facts (Verifiable Only)
- 

## Interpretations (Clearly Marked)
- 

## Opinions (Explicitly Labeled)
- Opinion:
  - 

---

# Context for Next Developer

## What Matters Most
- 

## Where to Look First
- 

## Key Decisions Made
- 

## What Not to Change
- 

---

# Work Status

## Completed
- 

## In Progress
- 

## Not Started (but relevant)
- 

---

# Dependencies

## Confirmed
- 

## Suspected / Unverified
- 

---

# Open Questions
- 

---

# Issues / Challenges
- 

---

# System Impact

## Repo / Structure Impact
- 

## PM Tracking Impact
- Needs update:
  - [ ] repos.json
  - [ ] STATUS.md
  - [ ] dependency docs
  - [ ] none

---

# Validation / Testing

- Tested:
- Passed:
- Failed:
- Not tested:

---

# Raw Notes (Do Not Summarize)
- 
"""


def main() -> int:
    project_name = normalize_project_name(input("Enter short project name: "))
    if not project_name:
        print("Project name is required")
        return 1

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    filename = build_handoff_filename(project_name, now)

    os.makedirs(HANDOFF_DIR, exist_ok=True)
    filepath = os.path.join(HANDOFF_DIR, filename)

    if os.path.exists(filepath):
        print(f"File already exists: {filepath}")
        return 1

    with open(filepath, "w") as f:
        f.write(build_handoff_template(date_str))

    print(f"Created: {filepath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
