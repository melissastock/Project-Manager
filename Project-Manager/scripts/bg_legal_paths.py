"""Canonical paths for the bg-legal engagement repo.

Google Drive folder name may remain "Case Files" for intake; governed operating
docs and timeline evidence live in the git working tree at `bg-legal/` next to
`Project-Manager/` at the portfolio repository root.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BG_LEGAL_DIR = ROOT / "bg-legal"
TIMELINE_EVIDENCE_DIR = BG_LEGAL_DIR / "docs" / "timeline-evidence"
