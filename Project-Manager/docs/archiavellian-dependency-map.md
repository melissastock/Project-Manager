# Archiavellian Dependency Map

Date: 2026-04-01
Status: active portfolio dependency map
Owner: Melissa Stock

## Purpose

This document defines how `archiavellian` fits into the broader project system so it can be supervised, sequenced, and reported consistently inside Project Manager.

## Project Role

`archiavellian` is the narrative, strategy, and productization workspace for turning archived evidence, story structure, and system insight into organized outputs.

`Archiavellian-Archive` is the preservation-side companion repository for source materials, evidence inputs, and archive-bound project support files.

## Dependency Classification

### Upstream inputs into Archiavellian

#### 1. Archiavellian-Archive
Type: hard dependency
Why it matters:
- preserves source materials
- holds evidence and archive-bound inputs
- supports traceability between narrative output and source material

Dependency impact if missing:
- narrative work loses source grounding
- archive retrieval becomes inconsistent
- evidence-to-story mapping weakens

#### 2. Producer / Producer Archive
Type: soft dependency
Why it matters:
- overlaps with story development, production thinking, and source organization
- may contain adjacent creative or narrative structure relevant to Archiavellian execution

Dependency impact if missing:
- less coordination across narrative and production workspaces
- possible duplication of story architecture or archive handling

#### 3. MJS Financial Dash
Type: selective dependency
Why it matters:
- supports any Archiavellian outputs that rely on financial reconstruction, timeline support, or evidentiary structure
- provides normalized fact base where money trail or operational structure intersects the story

Dependency impact if missing:
- fact-linked narrative outputs become harder to validate
- financial or operational assertions may drift from source-of-truth systems

## Downstream outputs from Archiavellian

#### 1. Productized story assets
Examples:
- sizzle materials
- landing page structure
- deck concepts
- product framing
- strategic narrative outputs

#### 2. Portfolio-level planning visibility
Project Manager should be able to treat Archiavellian as:
- an active project
- a priority candidate
- a milestone-driven workstream
- a system with dependencies rather than a standalone creative repo

## Cross-Project Relationship Summary

| Project | Relationship to Archiavellian | Dependency strength | Notes |
| --- | --- | --- | --- |
| Archiavellian-Archive | source archive and evidence preservation | hard | Primary archive-side companion repo |
| Project Manager | supervision, prioritization, sequencing, reporting | hard | Control plane for portfolio visibility |
| MJS Financial Dash | fact base for financial and evidentiary overlap | selective | Use when claims depend on money trail, reconstruction, or operational proof |
| Producer | adjacent narrative and production workspace | soft | Coordinate to avoid duplication |
| Producer Archive | adjacent archive structure | soft | Coordinate preserved source materials where relevant |
| Resume Builder | no direct dependency | none for now | Separate monetization track |
| provider-access-hub | no direct dependency | none | Separate product workstream |
| Momentum-OS | planning adjacency only | soft | Can host execution planning but is not a source dependency |

## Reporting Recommendation

Archiavellian should report into Project Manager in these ways:

1. Portfolio manifest entry in `config/repos.json`
2. Generated status visibility in `STATUS.md`
3. Inclusion in any future lane, milestone, or dependency dashboards
4. Explicit archive linkage to `Archiavellian-Archive`

## Suggested Lane Placement

### Lane: strategic asset development
Use when Archiavellian is being developed as:
- an intellectual property asset
- a story-driven product or media concept
- a pitch, deck, or narrative system

### Lane: archive-backed evidence synthesis
Use when the work is focused on:
- source review
- pattern extraction
- evidence organization
- timeline-supported narrative development

## Operational Rule

When Archiavellian work depends on raw evidence, preserved source files, or traceability, the source should live in `Archiavellian-Archive` and the working narrative output should live in `archiavellian`.

When Archiavellian work depends on validated financial reconstruction or operational fact patterns, those inputs should reference `MJS Financial Dash` rather than duplicating core financial truth inside the Archiavellian repo.

## Next Actions

1. Add `archiavellian` and `Archiavellian-Archive` to `config/repos.json`.
2. Regenerate `STATUS.md` locally.
3. Add milestone and dependency tracking for Archiavellian once the relevant Project Manager views are formalized.
4. Use this document as the default dependency reference until a centralized dependency database or dashboard exists.
