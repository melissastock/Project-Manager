#!/usr/bin/env python3
"""Merge PM-portal project tickets into config/client-ops-tracker.json.

Sources (in order):
1. HTTP GET {PM_PORTAL_URL}/api/tickets?project=<name>  (default PM_PORTAL_URL=http://127.0.0.1:8080)
2. Local file pm-portal/data/tickets.json (dict of id -> ticket row)

Only clients with portal_sync.enabled and portal_project set are updated.
Tasks from the portal replace the client's tasks[] for that sync run.
waiting_on: optional portal_sync.merge_blocked_as_waiting adds one line per blocked ticket.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRACKER = ROOT / "config" / "client-ops-tracker.json"
DEFAULT_PORTAL_ROOT = ROOT / "pm-portal"
LOCAL_TICKETS = DEFAULT_PORTAL_ROOT / "data" / "tickets.json"


def ticket_state_to_task_status(state: str) -> str:
    s = (state or "").strip().lower()
    if s == "done":
        return "done"
    if s == "blocked":
        return "blocked"
    if s == "deferred":
        return "deferred"
    if s in ("in_progress", "triaged", "new"):
        return "in_progress" if s == "in_progress" else "todo"
    return "todo"


def priority_to_level(priority: str) -> str:
    p = (priority or "P2").strip().upper()
    if p in ("P0", "P1"):
        return "high"
    if p == "P3":
        return "low"
    return "medium"


def normalize_due_date(raw: str | None) -> str:
    if not raw:
        return ""
    text = str(raw).strip()
    if not text:
        return ""
    # ISO datetime -> date prefix
    if "T" in text:
        return text.split("T", 1)[0]
    return text[:10] if len(text) >= 10 else text


def fetch_tickets_http(base_url: str, project: str, timeout_s: float) -> list[dict[str, Any]]:
    from urllib.parse import quote

    q = quote(project, safe="")
    url = f"{base_url.rstrip('/')}/api/tickets?project={q}"
    req = Request(url, headers={"Accept": "application/json"})
    with urlopen(req, timeout=timeout_s) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return list(data.get("tickets") or [])


def load_tickets_local() -> dict[str, Any]:
    if not LOCAL_TICKETS.exists():
        return {}
    return json.loads(LOCAL_TICKETS.read_text(encoding="utf-8"))


def tickets_for_project_from_local(cache: dict[str, Any], project: str) -> list[dict[str, Any]]:
    pl = project.strip().lower()
    out: list[dict[str, Any]] = []
    for row in cache.values():
        if not isinstance(row, dict):
            continue
        if str(row.get("project", "")).strip().lower() != pl:
            continue
        out.append(row)
    return out


def portal_rows_to_tasks(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for row in rows:
        title = str(row.get("title", "")).strip() or "(untitled ticket)"
        tid = str(row.get("id", "")).strip()
        label = f"{title} [{tid}]" if tid else title
        desc = str(row.get("description", "") or "").strip()
        state = str(row.get("state", "new"))
        tasks.append(
            {
                "task": label,
                "owner": str(row.get("owner", "") or "").strip() or "unassigned",
                "due_date": normalize_due_date(row.get("due_date")),
                "status": ticket_state_to_task_status(state),
                "priority": priority_to_level(str(row.get("priority", "P2"))),
                "blocking_item": desc if state.lower() == "blocked" else "",
            }
        )
    return tasks


def blocked_waiting_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    waiting: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("state", "")).lower() != "blocked":
            continue
        title = str(row.get("title", "")).strip() or "Ticket"
        tid = str(row.get("id", "")).strip()
        desc = str(row.get("description", "") or "").strip()
        owner = str(row.get("owner", "") or "").strip() or "unassigned"
        due = normalize_due_date(row.get("due_date"))
        waiting.append(
            {
                "item": f"Unblock PM-portal ticket: {title}" + (f" ({tid})" if tid else ""),
                "owner": owner,
                "due_date": due,
                "status": "open",
                "impact": desc[:500] if desc else "Ticket is in blocked state in PM-portal.",
            }
        )
    return waiting


def sync_client(
    client: dict[str, Any],
    base_url: str,
    timeout_s: float,
    prefer_http: bool,
) -> tuple[bool, str]:
    sync = client.get("portal_sync") or {}
    if not sync.get("enabled"):
        return False, "portal_sync not enabled"
    project = str(sync.get("portal_project", "") or client.get("portal_project", "")).strip()
    if not project:
        return False, "portal_sync.portal_project missing"

    rows: list[dict[str, Any]] = []
    source = ""

    if prefer_http:
        try:
            rows = fetch_tickets_http(base_url, project, timeout_s)
            source = f"HTTP {base_url}"
        except (URLError, OSError, TimeoutError, ValueError) as exc:
            rows = []
            source = f"HTTP failed ({exc}); trying local file"

    if not rows:
        local = load_tickets_local()
        rows = tickets_for_project_from_local(local, project)
        if rows:
            source = source + " -> " if source else ""
            source += f"local {LOCAL_TICKETS}"

    if not rows:
        return False, f"no tickets for project {project!r} ({source or 'no source'})"

    client["tasks"] = portal_rows_to_tasks(rows)

    if sync.get("merge_blocked_as_waiting"):
        extra = blocked_waiting_rows(rows)
        existing = client.get("waiting_on") or []
        if not isinstance(existing, list):
            existing = []
        # De-dup by item text
        seen = {str(x.get("item", "")).strip() for x in existing if isinstance(x, dict)}
        for w in extra:
            key = str(w.get("item", "")).strip()
            if key and key not in seen:
                existing.append(w)
                seen.add(key)
        client["waiting_on"] = existing

    client["_portal_sync"] = {
        "project": project,
        "ticket_count": len(rows),
        "source": source or "unknown",
    }
    return True, f"synced {len(rows)} tickets from {source or 'portal'}"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sync PM-portal tickets into client-ops-tracker.json")
    p.add_argument("--tracker", default=str(DEFAULT_TRACKER), help="Path to client-ops-tracker.json")
    p.add_argument(
        "--base-url",
        default=os.environ.get("PM_PORTAL_URL", "http://127.0.0.1:8080"),
        help="PM-portal API base URL (or set PM_PORTAL_URL).",
    )
    p.add_argument("--timeout", type=float, default=8.0, help="HTTP timeout seconds")
    p.add_argument(
        "--file-only",
        action="store_true",
        help="Skip HTTP; use pm-portal/data/tickets.json only.",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.tracker)
    if not path.exists():
        print(f"Tracker not found: {path}", file=sys.stderr)
        return 1

    tracker = json.loads(path.read_text(encoding="utf-8"))
    clients = tracker.get("clients")
    if not isinstance(clients, list):
        print("Invalid tracker: clients must be a list", file=sys.stderr)
        return 1

    prefer_http = not args.file_only
    any_ok = False
    messages: list[str] = []

    for client in clients:
        if not isinstance(client, dict):
            continue
        ok, msg = sync_client(client, args.base_url.rstrip("/"), args.timeout, prefer_http)
        name = client.get("name", "?")
        if ok:
            any_ok = True
            messages.append(f"{name}: {msg}")
        elif (client.get("portal_sync") or {}).get("enabled"):
            messages.append(f"{name}: skipped ({msg})")

    if not any_ok and messages:
        # Enabled clients but no data — non-fatal for cron if portal down
        print("PM-portal sync: no ticket data merged. " + "; ".join(messages), file=sys.stderr)
        return 0

    if any_ok or messages:
        for line in messages:
            print(line)

    # Write atomically
    text = json.dumps(tracker, indent=2, ensure_ascii=False) + "\n"
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".client-ops-", suffix=".json")
    try:
        os.write(fd, text.encode("utf-8"))
        os.close(fd)
        Path(tmp).replace(path)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        Path(tmp).unlink(missing_ok=True)
        raise

    print(f"Updated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
