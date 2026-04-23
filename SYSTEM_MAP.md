# System map

This file is the canonical map between **top-level domains** and the **Project Manager** control plane.

## Domains (repository root)

| Path | Role |
| --- | --- |
| `archive/` | Cold storage for inactive, legacy, backup, or ambiguous assets. |
| `execution-finance/` | Active finance and revenue execution lane. |
| `execution-legal/` | Active legal and compliance execution lane. |
| `narrative-output/` | Narrative, publication, and outward-facing artifact lane. |
| `platform-os/` | Shared platform, infrastructure, and cross-cutting systems. |
| `product-lab/` | Product discovery, experiments, and pre-production work. |
| `recovery-core/` | Recovery, continuity, and operational resilience. |
| `Project-Manager/` | Portfolio control plane: `config/`, `scripts/`, `docs/`, `pm-portal/`, and tracked child-repo gitlinks. |

## Control plane

All portfolio automation assumes paths in `Project-Manager/config/repos.json` are **relative to this repository root**.

Promoting or demoting an asset between domains is a deliberate remap: update manifests and docs, then record the decision in `Project-Manager/docs/session-artifacts/` as appropriate.
