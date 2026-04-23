# Client Engagement Scaffold Rollout Plan

## Purpose

This document sets the rollout order for the reusable client engagement scaffold across active Project Manager repositories.

The goal is not to force every repo into the same shape. The goal is to apply the scaffold where it improves orientation, delivery clarity, and handoff quality.

## What We Have Proven

Two working examples now exist:

- `Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System`: discovery-oriented client engagement pattern
- `provider-access-hub`: active delivery-oriented platform pattern

These examples show that the scaffold works in both an early discovery project and a more mature execution repo.

## Rollout Criteria

A repo should get the scaffold when at least two of these are true:

- outside collaborators or clients may read the repo
- the repo needs a cleaner front door than the current README provides
- the repo has meaningful product or delivery docs but weak orientation
- the repo would benefit from clearer phase, scope, and ownership language

A repo should not be prioritized when:

- it is archive-only
- it is primarily an internal portfolio-control repository
- the repo is too unstable to benefit from orientation docs yet
- the work is dominated by private or legal material that should stay tightly contained

## Recommended Rollout Order

### Wave 1: highest-value next targets

1. `Aneumind and TC Structure`
   - Why: active-client classification, likely to benefit immediately from clearer engagement framing
   - Recommended pattern: discovery-plus-delivery hybrid

2. `Momentum-OS`
   - Why: active platform and operations planning repo with broad scope that benefits from stronger front-door orientation
   - Recommended pattern: execution-oriented scaffold adapted for operations and planning

3. `MJSDS Dashboard`
   - Why: published-facing project where contributor orientation and scope clarity matter
   - Recommended pattern: delivery-oriented scaffold with website and release emphasis

### Wave 2: likely good fits after Wave 1

4. `Wayne Strain`
   - Why: research repo that would benefit from clearer purpose, phase, and deliverables
   - Recommended pattern: research-engagement variant

5. `Producer`
   - Why: active story/archive workspace with broad purpose that may need stronger operating boundaries
   - Recommended pattern: delivery-oriented scaffold adapted for media and archive workflows

6. `Teach - Home Learning Playbook`
   - Why: active education project that may benefit from a client-readable orientation layer
   - Recommended pattern: education-project delivery scaffold

7. `Teach - Zahmeir Learning System`
   - Why: similar to the Home Learning Playbook, but lower priority if active development churn remains high
   - Recommended pattern: education-project delivery scaffold

### Wave 3: conditional or low-priority targets

8. `MJS Financial Dash`
   - Why not earlier: very high local churn and sensitive finance context; orientation cleanup is useful but not urgent until working-tree noise is reduced
   - Recommended pattern: finance-delivery variant only after cleanup

9. `App Builder`
   - Why not earlier: this repo already acts partly as a portfolio scaffolding/tooling home; a client-facing scaffold may not be the right default
   - Recommended pattern: only if a specific subproject needs it

## Rollout Method

For each target repo:

1. read the existing README and docs folder first
2. decide whether the repo needs a discovery-oriented or delivery-oriented scaffold
3. use `python3 scripts/scaffold_client_engagement_pack.py --target "path/to/repo" --project-name "Project Name"` only as a starting point
4. replace generic text with repo-specific phase, scope, and ownership language before committing
5. keep canonical deep-dive docs linked rather than duplicated

## Done Criteria Per Repo

A rollout is complete when:

- the README has a clear front door
- `docs/engagement-overview.md` exists and reflects the repo's real current phase
- the scaffold docs are adapted to the repo instead of left generic
- the changes are committed in the child repo and reflected in the parent gitlink when appropriate
