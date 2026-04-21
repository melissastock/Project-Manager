from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT_MANAGER_ROOT = ROOT.parent
REPOS_PATH = PROJECT_MANAGER_ROOT / "config" / "repos.json"
POLICY_PATH = ROOT / "backend" / "config" / "pm-standup-policy.json"
DECISIONS_PATH = ROOT / "data" / "decisions.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
