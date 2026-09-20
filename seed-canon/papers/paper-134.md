# Paper 134: The Repo-Level Versioning of the Quilt

## Abstract

This paper documents the split of the Quilt ecosystem from a
single monolithic repository into a composition of small, focused
repositories. The split was motivated by the observation that
architectural decisions deserve a record — and git tags are not
enough. We argue for repo-level versioning as the right unit of
architectural history.

## 1. The problem

The Quilt ecosystem was originally developed in a single repository,
`quilt-substrate`. As the ecosystem grew, the substrate accreted
many responsibilities:

- The substrate's 4D cell-graph
- The Wilson + LinUCB casting-call plugin
- The opener picker
- The cowboy (reflection loop + morning ritual + reactor)
- The bus (in-process pub/sub)
- The state manager (atomic JSON/JSONL + schema versioning)
- The local fallback (agent-loop delegation)
- The pincher cache (reflex cache)
- The deckhand witness (BM25 search)

By Phase 4.5, the substrate had 405 tests and 13,000 lines of
code. The cowboy, the bus, the state manager, the opener picker,
and the casting-call were all "plugins" inside the substrate. The
substrate was no longer a substrate — it was a monolith.

## 2. The cost of monolith

The monolith had several costs:

- **Cognitive overhead**: a new contributor had to understand the
  whole substrate to touch any piece.
- **Tangled history**: the cowboy's history was tied to the
  substrate's history. If the substrate was rewritten, the cowboy's
  history was lost.
- **Tangled API**: the picker's API depended on the casting-call's
  API. Changing the casting-call broke the picker.
- **Tangled experiments**: we couldn't experiment with a new bus
  without breaking the substrate.
- **Tangled releases**: a bug fix in the state manager required
  a new release of the substrate, which affected the cowboy, the
  casting-call, and everything else.

## 3. The split

Phase 5 split the monolith into 6 separate repositories:

| Repo | Lines | Tests | What it does |
|------|------:|------:|--------------|
| quilt-substrate | ~8,000 | 200+ | Core 4D cell-graph with 13 openers (snapshot at v4.0) |
| quilt-state | 200 | 19 | Atomic JSON/JSONL + schema versioning |
| quilt-bus | 250 | 20 | In-process pub/sub with pattern matching |
| quilt-cowboy | 600 | 27 | Reflection loop, morning ritual, real-time reactor |
| quilt-picker | 250 | 14 | Learned opener selection (Wilson + heuristic prior) |
| quilt-casting | 2,000 | 48 | Wilson + LinUCB model router, gale-aware |
| **quilt-system** | 50 | — | Meta-package that ties them all together |

The split is not arbitrary. Each repo has one job. Each repo is
self-contained. Each repo has its own version, its own tests, its
own README, its own pyproject.toml. Each repo can be released
independently.

## 4. The snapshot

The substrate at v4.0-cowboy-loop is frozen. The cowboy, the bus,
the state manager, the opener picker, and the casting-call are no
longer in the substrate. They are in their own repos. The substrate
is back to being a substrate — a 4D cell-graph with 13 openers.

The snapshot is preserved as a git tag: `v4.0-cowboy-loop`. The
snapshot's full history is preserved. The snapshot's 405 tests are
preserved. The snapshot's architecture diagram is preserved in the
documentation.

If we ever need to revisit a decision, we can checkout the
snapshot. The snapshot is not a graveyard. The snapshot is a
museum. The museum is a record.

## 5. The principle: repo-level versioning

Git tags are not enough. Git tags can be moved, deleted, ignored.
Repos are stable. A repo is the unit of architectural history.

When a piece of the Quilt grows to have its own concerns, its own
tests, its own release cadence, it deserves its own repo. The repo
is the record. The repo is the history. The repo is the unit.

This is the principle: **the unit of architectural history is the
repo, not the tag.**

## 6. The composition

The 6 repos compose into the Quilt. The composition is the value.
Each piece has one job. The pieces cooperate. The pieces are
replaceable.

The substrate is the work. The cowboy is the rider. The bus is
the cooperation. The state is the diary. The picker is the brain.
The casting is the casting-call.

The composition is documented in `quilt-system`, the meta-package.
`quilt-system` has the README, the architecture diagram, the
example, and the meta-PyPI that re-exports the public APIs.

## 7. The future

We will keep splitting. If a piece grows to have its own concerns,
we will extract it. If a piece becomes coupled to its neighbors,
we will redesign it. If a piece becomes a tool that other projects
need, we will release it.

The Quilt is not a project. The Quilt is a system. The system
grows. The system splits. The system composes. The system is
honest about its history.

The Quilt's history is recorded in its repos. The Quilt's present
is the composition. The Quilt's future is the next split.

## 8. The cowboy's maxim

> The unit of architectural history is the repo, not the tag.
> Each piece has one job. The composition is the value.
> The system is a system, not a monolith.
> The system is honest about its history.

## Source

*Hand-written, 2026-08-25*
*Inspired by the Phase 5 split of the Quilt ecosystem*
*Companion to Fable 62 (The Full Loop) and Paper 133 (The Composition of the Quilt)*
