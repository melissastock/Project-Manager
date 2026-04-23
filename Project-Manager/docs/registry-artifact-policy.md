# Registry Artifact Policy

This policy normalizes `os-registry` artifact handling for the sprint focus products.

## Policy source

- `config/registry-artifact-policy.json`
- Validator: `scripts/validate_registry_artifacts.py`

## Target handling

- `provider-access-hub`: **commit** `data/os_registry_snapshot.json`, `data/files_manifest.json`, `data/assets/README.md`
- `Momentum-OS`: **commit** `data/os_registry_snapshot.json`, `data/files_manifest.json`, `data/assets/README.md`
- `bg-legal`: **ignore** `data/os_registry_snapshot.json`, `data/files_manifest.json` (repo-level `data/*.json` rule)

## Validation command

```bash
python3 scripts/validate_registry_artifacts.py
```

Validation output is written to `docs/session-artifacts/governance/REGISTRY_TARGET_VALIDATION-<stamp>.md`.
