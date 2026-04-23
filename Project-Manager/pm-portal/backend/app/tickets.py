from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .db import fetch_project_tickets, supabase_configured, upsert_project_ticket
from .models import ProjectTicket


def load_tickets(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if supabase_configured():
        try:
            rows = fetch_project_tickets()
            return {row["id"]: row for row in rows if row.get("id")}
        except Exception:
            pass
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_tickets(path: Path | None, tickets: dict[str, dict[str, Any]]) -> None:
    if supabase_configured():
        try:
            for value in tickets.values():
                upsert_project_ticket(value)
            return
        except Exception:
            pass
    if path is None:
        raise RuntimeError("Ticket path is required when Supabase is not configured")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tickets, indent=2, default=str), encoding="utf-8")


def list_project_tickets(project_name: str, cache: dict[str, dict[str, Any]]) -> list[ProjectTicket]:
    out: list[ProjectTicket] = []
    for raw in cache.values():
        if str(raw.get("project", "")).lower() != project_name.lower():
            continue
        out.append(ProjectTicket(**raw))
    out.sort(key=lambda t: (t.state, t.priority, t.updated_at), reverse=True)
    return out

