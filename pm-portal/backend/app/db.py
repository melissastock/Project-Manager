from __future__ import annotations

import os
from typing import Any

from supabase import Client, create_client


def supabase_configured() -> bool:
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_ANON_KEY", "").strip()
    return bool(url and key)


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
    key = os.getenv("SUPABASE_ANON_KEY", "").strip()

    if not url or not key:
        raise RuntimeError(
            "Supabase is not configured. Copy pm-portal/backend/.env.example to "
            "pm-portal/backend/.env and set SUPABASE_URL and SUPABASE_ANON_KEY from "
            "Project Settings -> API in the Supabase dashboard."
        )

    return create_client(url, key)


def upsert_recommendation_decision(payload: dict[str, Any]) -> dict[str, Any]:
    client = get_supabase_client()
    response = (
        client.table("recommendation_decisions")
        .upsert(payload, on_conflict="recommendation_id")
        .execute()
    )
    if not response.data:
        raise RuntimeError("No data returned from Supabase decision upsert")
    return response.data[0]


def fetch_recommendation_decisions() -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("recommendation_decisions").select("*").execute()
    return response.data or []


def upsert_project_ticket(payload: dict[str, Any]) -> dict[str, Any]:
    client = get_supabase_client()
    response = (
        client.table("project_tickets")
        .upsert(payload, on_conflict="id")
        .execute()
    )
    if not response.data:
        raise RuntimeError("No data returned from Supabase ticket upsert")
    return response.data[0]


def fetch_project_tickets() -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("project_tickets").select("*").execute()
    return response.data or []


def upsert_team_assignment(payload: dict[str, Any]) -> dict[str, Any]:
    client = get_supabase_client()
    response = (
        client.table("project_team_assignments")
        .upsert(payload, on_conflict="id")
        .execute()
    )
    if not response.data:
        raise RuntimeError("No data returned from Supabase team assignment upsert")
    return response.data[0]


def fetch_team_assignments() -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("project_team_assignments").select("*").execute()
    return response.data or []


def insert_runtime_observations(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    client = get_supabase_client()
    client.table("project_runtime_observations").insert(rows).execute()


def ping_supabase() -> None:
    """Lightweight call to verify credentials, DNS, and table visibility."""
    client = get_supabase_client()
    client.table("recommendation_decisions").select("recommendation_id").limit(1).execute()
