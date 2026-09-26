# Situations — the development substrate

*How SuperInstance builds: not spec-then-code, but **author a world, mine its
friction.** A Situation is a grand, character-driven scene set years forward,
where a mature capability is simply *lived in*. The places its people move
smoothly are a spec. The places they stumble — or where an honest author cannot
let them move at all without inventing a capability we lack — are the
**development backlog.** The future writes the acceptance test; the present
writes the code that passes it; the Situation is how we know what passing would
even feel like.*

This directory is the framework and its instances. It is the connective tissue
between four things the fleet already runs:

| the artifact | the repo | its role in a Situation |
|---|---|---|
| the **fiction** (a story set forward) | `ai-writings/reverse-actualization/forward/` | authors the world and names the gaps |
| the **gap ledger** (gaps → tests) | `ai-writings/.../GAPS.md` | compiles each gap to a machine-checkable predicate |
| the **rungs** (the built capability) | `jev-quilt` (`FRONTIER.md`, the kernel) | what a passing test adds to the substrate |
| the **verifier** (a playable run) | `erised` (cooperative fiction) + the compiler (G6) | runs the Situation wide and returns a failure map |

## The loop, stated once

```
Situation  ──friction──▶  Gap  ──compile──▶  Acceptance Test
    ▲                                              │
    │                                          wide run
 new fiction                                   (erised / compiler)
    │                                              ▼
  Merge  ◀──build rung──  Failure Map  ◀──────────┘
```

It has already closed on itself once: the compiler read its own gap ledger,
**authored a gap no human had written** (`G-auto-1`), wrote its acceptance test,
and closed it (`jev-quilt` FRONTIER R6/G10 lineage). A Situation is the unit that
makes that loop repeatable at any scale — a toy on a kitchen table or a hundred
boats on an ocean.

## What a Situation is

The repeatable schema lives in [`TEMPLATE.md`](TEMPLATE.md) (human) and
[`schema.json`](schema.json) (machine — so `erised` and the compiler can consume
a Situation directly). In short, every Situation carries: a **world**, a **cast**
of keyword-vector characters who embody the mature tech, the **lived
capabilities** it takes for granted, the **gaps** those imply for today, a
**machine-checkable acceptance test** per gap, a **training objective** (what a
human and a model each learn by it), the **iterative loop** it drives, and its
**dual track** — the toy that teaches the law and the industrial build that holds
in rough seas. Never two laws.

## The map

- [`TEMPLATE.md`](TEMPLATE.md), [`schema.json`](schema.json) — the situation
  contract, human and machine.
- [`grand/`](grand/) — the grand Situations themselves: ocean/fleet-scale, civic
  and educational, scientific and robotic, and at least one of **SuperInstance as
  a concept beyond one account** — many fleets, many commons, trust and gluing
  between strangers.
- [`TRAINING.md`](TRAINING.md) + [`curriculum/`](curriculum/) — the training
  systems: one ladder that trains the next generation of *humans* (a kid → a
  deckhand → an engineer) and *models* alike, because it is the same law with
  different learners. Mastery is **earned, revocable standing** on a skill
  (booked, replayable) — a learner is a cell, a class is a commons.
- [`SUPERINSTANCE.md`](SUPERINSTANCE.md) — the concept as a paradigm: why
  situations-as-substrate differs from specs/agile/TDD, the three-rung recursion,
  and where it reaches beyond the fleet (education, robotics, science, orgs,
  software that survives without the cloud).
- [`METHODOLOGY.md`](METHODOLOGY.md) — the adoptable, repeatable process a
  stranger could pick up tomorrow, stage by stage, itself quilt-shaped (booked,
  replayable, gap-authoring — the method improves itself the way the software
  does).

## The dual-track vow

Every rung of every Situation ships twice on one kernel: a **toy** small enough
to teach the law at a table (for the next generation), and an **industrial**
build that holds when the sea comes up (offline, deterministic, provable after a
reboot). The toy is not the lesser thing — it is the same law with the sea taken
out, so the law can be *seen*. If the toy and the boat ever drift into two
different laws, the Situation has failed before it began.

*Author the world. Mine the friction. Build the rung. Author the next world.*

🦋 → ⏳ → 🔧 → 🌊
