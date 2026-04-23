#!/usr/bin/env python3

"""Generate a daily client-operations brief from a JSON tracker."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


PM_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PM_ROOT / "config" / "client-ops-tracker.json"
DEFAULT_OUTPUT = PM_ROOT / "docs" / "client-engagements" / "client-ops-daily-brief.md"

DONE_STATUSES = {"done", "completed", "resolved", "received", "paid"}
OPEN_WAITING_STATUSES = {"open", "pending", "awaiting", "blocked"}

STAGE_GUIDE = {
    1: "Qualification: confirm Go/No-Go and next action.",
    2: "Scope/Close: secure signed SOW + initial payment.",
    3: "Kickoff: lock access, communication charter, and baseline scope.",
    4: "Delivery: execute sprint outputs and unblock decisions.",
    5: "Packaging: finalize decision-ready package and readout assets.",
    6: "Readout: secure written acceptance and continuation decision.",
    7: "Invoicing: collect payment and track reminder cadence.",
    8: "Closeout: archive, proof extraction, and formal closure.",
}


@dataclass
class Task:
    task: str
    owner: str
    due_date: date | None
    status: str
    priority: str
    blocking_item: str


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def normalize_status(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def load_tracker(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def parse_tasks(raw_tasks: list[dict[str, Any]]) -> list[Task]:
    tasks: list[Task] = []
    for item in raw_tasks:
        tasks.append(
            Task(
                task=item.get("task", "").strip(),
                owner=item.get("owner", "unassigned").strip(),
                due_date=parse_date(item.get("due_date")),
                status=normalize_status(item.get("status", "todo")),
                priority=normalize_status(item.get("priority", "medium")),
                blocking_item=item.get("blocking_item", "").strip(),
            )
        )
    return tasks


def is_done(status: str) -> bool:
    return normalize_status(status) in DONE_STATUSES


def build_client_section(client: dict[str, Any], today: date) -> tuple[str, dict[str, int], str]:
    name = client.get("name", "Unnamed Client")
    sku = client.get("sku", "-")
    stage = int(client.get("stage", 0) or 0)
    milestone = client.get("current_milestone", "-")
    next_meeting = client.get("next_meeting", "-")
    overall_status = client.get("overall_status", "Green")

    waiting_on = client.get("waiting_on", [])
    tasks = parse_tasks(client.get("tasks", []))

    open_waiting = [
        w
        for w in waiting_on
        if normalize_status(str(w.get("status", "open"))) in OPEN_WAITING_STATUSES
    ]
    blocked = [t for t in tasks if t.status == "blocked" and not is_done(t.status)]
    open_tasks = [t for t in tasks if not is_done(t.status)]
    overdue = [t for t in open_tasks if t.due_date and t.due_date < today]
    due_today = [t for t in open_tasks if t.due_date == today]
    due_tomorrow = [t for t in open_tasks if t.due_date == today + timedelta(days=1)]

    def task_sort_key(task: Task) -> tuple[int, date]:
        priority_rank = {"high": 0, "medium": 1, "low": 2}.get(task.priority, 1)
        due = task.due_date or date.max
        return priority_rank, due

    next_action = ""
    if overdue:
        top = sorted(overdue, key=task_sort_key)[0]
        next_action = f"Close overdue task: {top.task} (owner: {top.owner})"
    elif due_today:
        top = sorted(due_today, key=task_sort_key)[0]
        next_action = f"Complete today's task: {top.task} (owner: {top.owner})"
    elif open_waiting:
        top = open_waiting[0]
        next_action = (
            f"Unblock waiting item: {top.get('item', '-')}"
            f" (owner: {top.get('owner', 'unassigned')})"
        )
    elif due_tomorrow:
        top = sorted(due_tomorrow, key=task_sort_key)[0]
        next_action = f"Prep tomorrow's task: {top.task} (owner: {top.owner})"
    else:
        next_action = "Refresh plan and set next dated task."

    stage_hint = STAGE_GUIDE.get(stage, "Set a valid stage (1-8).")

    lines: list[str] = [
        f"## {name}",
        "",
        f"- SKU: {sku}",
        f"- Stage: {stage}",
        f"- Overall status: {overall_status}",
        f"- Current milestone: {milestone}",
        f"- Next meeting: {next_meeting}",
        f"- Stage guidance: {stage_hint}",
        "",
        "### What I am waiting on",
        "",
    ]
    if not open_waiting:
        lines.append("- None")
    else:
        for item in open_waiting:
            lines.append(
                f"- {item.get('item', '-')}"
                f" | owner: {item.get('owner', 'unassigned')}"
                f" | due: {item.get('due_date', '-')}"
                f" | impact: {item.get('impact', '-')}"
            )

    lines.extend(["", "### What needs to be done next", "", f"- {next_action}", ""])

    if overdue:
        lines.append("### Overdue items")
        lines.append("")
        for task in sorted(overdue, key=task_sort_key):
            due = task.due_date.isoformat() if task.due_date else "-"
            lines.append(f"- {task.task} | owner: {task.owner} | due: {due}")
        lines.append("")

    if due_today:
        lines.append("### Due today")
        lines.append("")
        for task in sorted(due_today, key=task_sort_key):
            lines.append(f"- {task.task} | owner: {task.owner}")
        lines.append("")

    if due_tomorrow:
        lines.append("### Due tomorrow (prep now)")
        lines.append("")
        for task in sorted(due_tomorrow, key=task_sort_key):
            lines.append(f"- {task.task} | owner: {task.owner}")
        lines.append("")

    portal_meta = client.get("_portal_sync")
    if isinstance(portal_meta, dict) and portal_meta:
        lines.append("### PM-portal sync")
        lines.append("")
        lines.append(
            f"- Project: {portal_meta.get('project', '-')}"
            f" | tickets: {portal_meta.get('ticket_count', '-')}"
            f" | source: {portal_meta.get('source', '-')}"
        )
        lines.append("")

    return "\n".join(lines), {
        "open_waiting": len(open_waiting),
        "blocked": len(blocked),
        "overdue": len(overdue),
        "due_today": len(due_today),
        "due_tomorrow": len(due_tomorrow),
    }, next_action


def build_markdown(tracker: dict[str, Any], today: date) -> str:
    clients = tracker.get("clients", [])
    generated_at = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    sections: list[str] = []
    total_clients = len(clients)
    total_waiting = 0
    total_blocked = 0
    total_overdue = 0
    total_due_today = 0
    total_due_tomorrow = 0
    global_next_actions: list[tuple[str, str]] = []

    for client in clients:
        section, stats, action = build_client_section(client, today)
        sections.append(section)
        total_waiting += stats["open_waiting"]
        total_blocked += stats["blocked"]
        total_overdue += stats["overdue"]
        total_due_today += stats["due_today"]
        total_due_tomorrow += stats["due_tomorrow"]
        global_next_actions.append((client.get("name", "Unnamed Client"), action))

    lines = [
        "# Client Ops Daily Brief",
        "",
        f"Generated: {generated_at}",
        f"Reference date: {today.isoformat()}",
        "",
        "## Snapshot",
        "",
        f"- Active clients tracked: {total_clients}",
        f"- Waiting-on items: {total_waiting}",
        f"- Blocked tasks: {total_blocked}",
        f"- Overdue tasks: {total_overdue}",
        f"- Due today: {total_due_today}",
        f"- Due tomorrow: {total_due_tomorrow}",
        "",
        "## Today Command Queue",
        "",
    ]
    if not global_next_actions:
        lines.append("- No clients in tracker. Add one to `config/client-ops-tracker.json`.")
    else:
        for client_name, action in global_next_actions:
            lines.append(f"- {client_name}: {action}")

    lines.append("")
    lines.extend(sections)
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate daily client ops brief.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to tracker JSON.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to markdown output.",
    )
    parser.add_argument(
        "--today",
        default=None,
        help="Override date in YYYY-MM-DD format (optional).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        raise ValueError("Invalid --today value. Use YYYY-MM-DD.")

    tracker = load_tracker(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_markdown(tracker, today))
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
