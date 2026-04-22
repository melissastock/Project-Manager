from __future__ import annotations

import json
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
PROJECT_MANAGER_ROOT = ROOT.parent
REPOS_PATH = PROJECT_MANAGER_ROOT / "config" / "repos.json"
POLICY_PATH = ROOT / "backend" / "config" / "pm-standup-policy.json"
DECISIONS_PATH = ROOT / "data" / "decisions.json"
TICKETS_PATH = ROOT / "data" / "tickets.json"
TEAM_ASSIGNMENTS_PATH = ROOT / "data" / "team_assignments.json"
CLIENT_AGREEMENTS_PATH = ROOT / "data" / "client_agreements.json"
AGREEMENT_MESSAGES_PATH = ROOT / "data" / "agreement_messages.json"
AGREEMENT_CHANGE_ORDERS_PATH = ROOT / "data" / "agreement_change_orders.json"
AGREEMENT_AUDIT_EVENTS_PATH = ROOT / "data" / "agreement_audit_events.json"
LABOR_ESTIMATES_PATH = ROOT / "data" / "labor_estimates.json"
SECURE_VAULT_FILES_PATH = ROOT / "data" / "secure_vault_files.json"
SECURE_VAULT_AUDIT_EVENTS_PATH = ROOT / "data" / "secure_vault_audit_events.json"
SECURE_VAULT_DRIVE_CONNECTIONS_PATH = ROOT / "data" / "secure_vault_drive_connections.json"

# Portal root first, then backend (backend wins on duplicate keys).
load_dotenv(ROOT / ".env")
load_dotenv(ROOT / "backend" / ".env", override=True)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
