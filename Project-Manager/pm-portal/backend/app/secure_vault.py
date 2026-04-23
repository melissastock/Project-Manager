from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import SecureVaultFile


def load_secure_vault_files(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_secure_vault_files(path: Path | None, files: dict[str, dict[str, Any]]) -> None:
    if path is None:
        raise RuntimeError("Secure vault file path is required")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(files, indent=2, default=str), encoding="utf-8")


def list_project_secure_vault_files(
    project_name: str, cache: dict[str, dict[str, Any]]
) -> list[SecureVaultFile]:
    items: list[SecureVaultFile] = []
    for raw in cache.values():
        if str(raw.get("project", "")).lower() != project_name.lower():
            continue
        items.append(SecureVaultFile(**raw))
    items.sort(key=lambda item: item.updated_at, reverse=True)
    return items


def get_secure_vault_file(file_id: str, cache: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    return cache.get(file_id)


def load_secure_vault_audit_events(path: Path | None = None) -> dict[str, dict[str, Any]]:
    if path is not None and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def persist_secure_vault_audit_events(path: Path | None, events: dict[str, dict[str, Any]]) -> None:
    if path is None:
        raise RuntimeError("Secure vault audit path is required")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(events, indent=2, default=str), encoding="utf-8")


def list_vault_audit_events_for_file(
    file_id: str, cache: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    items = [row for row in cache.values() if str(row.get("vault_file_id", "")) == file_id]
    items.sort(key=lambda item: str(item.get("created_at", "")))
    return items
