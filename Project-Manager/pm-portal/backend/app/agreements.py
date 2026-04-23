from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .db import (
    fetch_agreement_audit_events,
    fetch_agreement_change_orders,
    fetch_agreement_messages,
    fetch_client_agreements,
    insert_agreement_audit_event,
    supabase_configured,
    upsert_agreement_change_order,
    upsert_agreement_message,
    upsert_client_agreement,
)
from .models import AgreementChangeOrder, AgreementMessage, ClientAgreement


def load_audit_events(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if supabase_configured():
        try:
            rows = fetch_agreement_audit_events()
            return {row["id"]: row for row in rows if row.get("id")}
        except Exception:
            pass
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_audit_events(path: Path | None, events: dict[str, dict[str, Any]]) -> None:
    if supabase_configured():
        try:
            for value in events.values():
                insert_agreement_audit_event(value)
            return
        except Exception:
            pass
    if path is None:
        raise RuntimeError("Agreement audit path is required when Supabase is not configured")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(events, indent=2, default=str), encoding="utf-8")


def list_audit_events_for_agreement(
    agreement_id: str, cache: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    items = [
        row
        for row in cache.values()
        if str(row.get("agreement_id", "")) == agreement_id
    ]
    items.sort(key=lambda item: str(item.get("created_at", "")))
    return items


def append_audit_event(path: Path | None, event_payload: dict[str, Any]) -> dict[str, Any]:
    if supabase_configured():
        try:
            insert_agreement_audit_event(event_payload)
            return event_payload
        except Exception:
            pass
    events = load_audit_events(path)
    events[event_payload["id"]] = event_payload
    if path is None:
        raise RuntimeError("Agreement audit path is required when Supabase is not configured")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(events, indent=2, default=str), encoding="utf-8")
    return event_payload


def load_client_agreements(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if supabase_configured():
        try:
            rows = fetch_client_agreements()
            return {row["id"]: row for row in rows if row.get("id")}
        except Exception:
            pass
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_client_agreements(path: Path | None, agreements: dict[str, dict[str, Any]]) -> None:
    if supabase_configured():
        try:
            for value in agreements.values():
                upsert_client_agreement(value)
            return
        except Exception:
            pass
    if path is None:
        raise RuntimeError("Client agreement path is required when Supabase is not configured")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(agreements, indent=2, default=str), encoding="utf-8")


def list_project_agreements(project_name: str, cache: dict[str, dict[str, Any]]) -> list[ClientAgreement]:
    items: list[ClientAgreement] = []
    for raw in cache.values():
        if str(raw.get("project", "")).lower() != project_name.lower():
            continue
        items.append(ClientAgreement(**raw))
    items.sort(key=lambda item: item.updated_at, reverse=True)
    return items


def get_agreement(agreement_id: str, cache: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    return cache.get(agreement_id)


def load_agreement_messages(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if supabase_configured():
        try:
            rows = fetch_agreement_messages()
            return {row["id"]: row for row in rows if row.get("id")}
        except Exception:
            pass
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_agreement_messages(path: Path | None, messages: dict[str, dict[str, Any]]) -> None:
    if supabase_configured():
        try:
            for value in messages.values():
                upsert_agreement_message(value)
            return
        except Exception:
            pass
    if path is None:
        raise RuntimeError("Agreement message path is required when Supabase is not configured")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(messages, indent=2, default=str), encoding="utf-8")


def list_messages_for_agreement(
    agreement_id: str, cache: dict[str, dict[str, Any]]
) -> list[AgreementMessage]:
    items: list[AgreementMessage] = []
    for raw in cache.values():
        if str(raw.get("agreement_id", "")) != agreement_id:
            continue
        items.append(AgreementMessage(**raw))
    items.sort(key=lambda item: item.created_at)
    return items


def load_change_orders(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if supabase_configured():
        try:
            rows = fetch_agreement_change_orders()
            return {row["id"]: row for row in rows if row.get("id")}
        except Exception:
            pass
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_change_orders(path: Path | None, change_orders: dict[str, dict[str, Any]]) -> None:
    if supabase_configured():
        try:
            for value in change_orders.values():
                upsert_agreement_change_order(value)
            return
        except Exception:
            pass
    if path is None:
        raise RuntimeError("Agreement change-order path is required when Supabase is not configured")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(change_orders, indent=2, default=str), encoding="utf-8")


def list_change_orders_for_agreement(
    agreement_id: str, cache: dict[str, dict[str, Any]]
) -> list[AgreementChangeOrder]:
    items: list[AgreementChangeOrder] = []
    for raw in cache.values():
        if str(raw.get("agreement_id", "")) != agreement_id:
            continue
        items.append(AgreementChangeOrder(**raw))
    items.sort(key=lambda item: item.created_at, reverse=True)
    return items
