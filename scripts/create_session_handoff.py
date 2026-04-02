#!/usr/bin/env python3

from datetime import datetime
import os

# Simple script to create a new session handoff file

project_name = input("Enter short project name: ").strip().replace(" ", "-")

if not project_name:
    print("Project name is required")
    exit(1)

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
filename = f"{date_str}-{project_name}-handoff.md"

folder = os.path.join("docs", "session-handoffs")
os.makedirs(folder, exist_ok=True)

filepath = os.path.join(folder, filename)

if os.path.exists(filepath):
    print(f"File already exists: {filepath}")
    exit(1)

content = f"""# Developer Session Handoff

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

with open(filepath, "w") as f:
    f.write(content)

print(f"Created: {filepath}")
