from __future__ import annotations

import os
from typing import Any

from supabase import create_client, Client


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_ANON_KEY", "").strip()

    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

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
