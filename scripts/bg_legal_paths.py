"""Canonical paths for the bg-legal repo (Case Files program working copy).

Google Drive folder name remains "Case Files" for intake; governed operating
docs and timeline evidence live in the git working tree at bg-legal/.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BG_LEGAL_DIR = ROOT / "bg-legal"
TIMELINE_EVIDENCE_DIR = BG_LEGAL_DIR / "docs" / "timeline-evidence"
