# SESSION_OPEN.md

Use this protocol at the **start of every development session**.

Purpose:
- ingest the latest handoff
- restore context quickly
- align with Project Manager (PM) system
- ensure decisions are based on facts, not assumptions

Timebox: 5–7 minutes

## Step 1 — Locate Latest Handoff

Find the most recent file in:

`docs/session-handoffs/`

Confirm:
- correct project
- most recent date

If no handoff exists:
- stop and note: `No prior session context available`

## Step 2 — Read PM-Ready Summary

Read only:
- What Changed
- Current State
- Blockers / Risks
- Top Next Actions

Answer:
- What is the goal of this session?
- What matters most right now?

## Step 3 — Validate Against Evidence

Verify the summary using:
- commits
- files changed
- repo state

Check:
- Does the repo match the stated state?
- Are branches aligned with the summary?
- Are key files present?

If there is a mismatch, flag it as:
- `State mismatch between handoff and repo`

Do not assume the summary is correct.

## Step 4 — Review Evidence Log

Scan:
- commits
- files changed
- commands run

Focus on:
- what actually moved
- what might break
- what is incomplete

## Step 5 — Confirm Facts vs Interpretation

Read:
- Facts
- Interpretations
- Opinions

Ensure:
- Facts are supported
- Interpretations are reasonable
- Opinions are clearly labeled

If unsure, downgrade from fact to interpretation.

## Step 6 — Check Dependencies

From handoff plus PM docs:
- What does this project depend on?
- Has anything changed?

If a dependency is unclear, flag it immediately.

## Step 7 — Align With PM System

Quick check:
- Is the project in `config/repos.json`?
- Does `STATUS.md` reflect reality?
- Any recent changes not reflected?

If yes, note the PM update required.

## Step 8 — Define Session Objective

Write:

### Session Objective
- 

### Success Criteria
- 

Keep it tight:
- 1–2 goals max

## Step 9 — Confirm Starting Point

Document:
- repo
- branch
- key file(s)

This prevents starting in the wrong place.

## Step 10 — Begin Work

Only now start execution.

## Rules

1. Do not trust summaries without verification
2. Do not skip evidence review
3. Do not start work without a clear objective
4. If context is unclear, stop and clarify

## Definition of Done (Session Open)

You should be able to answer:
- What is the current state?
- What am I doing next?
- What could block me?
- What system am I affecting?

If not, you are not ready to start.
