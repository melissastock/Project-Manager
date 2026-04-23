from __future__ import annotations

import os
import hashlib
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


def supabase_storage_configured() -> bool:
    url = os.getenv("SUPABASE_URL", "").strip()
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    return bool(url and service_key)


def get_supabase_service_client() -> Client:
    url = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not url or not key:
        raise RuntimeError(
            "Supabase storage is not configured. Set SUPABASE_URL and "
            "SUPABASE_SERVICE_ROLE_KEY in pm-portal/backend/.env."
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


def create_secure_vault_signed_upload_url(
    bucket: str, path: str, expires_in_seconds: int = 900
) -> dict[str, Any]:
    client = get_supabase_service_client()
    storage = client.storage.from_(bucket)
    if hasattr(storage, "create_signed_upload_url"):
        return storage.create_signed_upload_url(path)
    raise RuntimeError("Supabase client does not support signed upload URLs in this version.")


def create_secure_vault_signed_download_url(
    bucket: str, path: str, expires_in_seconds: int = 900
) -> dict[str, Any]:
    client = get_supabase_service_client()
    storage = client.storage.from_(bucket)
    if hasattr(storage, "create_signed_url"):
        return storage.create_signed_url(path, expires_in_seconds)
    raise RuntimeError("Supabase client does not support signed download URLs in this version.")


def download_secure_vault_file_bytes(bucket: str, path: str) -> bytes:
    client = get_supabase_service_client()
    storage = client.storage.from_(bucket)
    data = storage.download(path)
    if isinstance(data, bytes):
        return data
    if hasattr(data, "read"):
        return data.read()
    raise RuntimeError("Unexpected storage download response type.")


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def upsert_client_agreement(payload: dict[str, Any]) -> dict[str, Any]:
    client = get_supabase_client()
    response = client.table("client_agreements").upsert(payload, on_conflict="id").execute()
    if not response.data:
        raise RuntimeError("No data returned from Supabase client agreement upsert")
    return response.data[0]


def fetch_client_agreements() -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("client_agreements").select("*").execute()
    return response.data or []


def upsert_agreement_message(payload: dict[str, Any]) -> dict[str, Any]:
    client = get_supabase_client()
    response = client.table("agreement_messages").upsert(payload, on_conflict="id").execute()
    if not response.data:
        raise RuntimeError("No data returned from Supabase agreement message upsert")
    return response.data[0]


def fetch_agreement_messages() -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("agreement_messages").select("*").execute()
    return response.data or []


def upsert_agreement_change_order(payload: dict[str, Any]) -> dict[str, Any]:
    client = get_supabase_client()
    response = (
        client.table("agreement_change_orders")
        .upsert(payload, on_conflict="id")
        .execute()
    )
    if not response.data:
        raise RuntimeError("No data returned from Supabase change order upsert")
    return response.data[0]


def fetch_agreement_change_orders() -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("agreement_change_orders").select("*").execute()
    return response.data or []


def insert_agreement_audit_event(payload: dict[str, Any]) -> dict[str, Any]:
    client = get_supabase_client()
    response = client.table("agreement_audit_events").insert(payload).execute()
    if not response.data:
        raise RuntimeError("No data returned from Supabase audit event insert")
    return response.data[0]


def fetch_agreement_audit_events() -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("agreement_audit_events").select("*").execute()
    return response.data or []
