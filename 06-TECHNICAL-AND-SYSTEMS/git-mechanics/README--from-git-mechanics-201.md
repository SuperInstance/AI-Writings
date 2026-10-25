# Git Mechanics 201 — The Foundational Course

> Source: an ideation conversation between Kimi and another AI agent
> (~3,800 lines). 201 organizes it into something learnable; **301**
> (`../git-mechanics-301/`) rebuilds the same discipline as a runnable
> quilt of tiles. Read 201 to understand the shape. Run 301 to practice it.

## Honest header — read this first

1. **Every number below is a design target, not a receipt.** No part of
   this course has been built, benchmarked, or run on the hardware it
   names. Where the source conversation asserted "X fits in Y," this
   document preserves the assertion and labels it. The course's own
   doctrine (Module 2: no receipts exist for unrehearsed contingencies)
   applies to itself, here, on page one.
2. **Weeks 1, 11, 14, 15 have no deep-dive material in the source.** The
   curriculum's table of contents names them; the conversation never
   wrote their labs. They are marked [scaffolded] rather than invented.
3. **The hardware baseline is one laptop** — RTX 4050, 6 GB VRAM, 32 GB
   RAM. Every performance claim is relative to that envelope.
4. **Labs 1, 2, 4, 8 ship strict constraints.** They are the spine.

## The course in one paragraph

One machine, one mind: an agent sits on a laptop recording voice and
keystrokes while it codes (dual-signal input). Everything it does —
human or model — lands in one append-only, double-entry ledger with
bidirectional trace (Module 2). The ledger lets the agent rewind itself:
splice out a work session as if it never happened, roll back cleanly,
checkpoint safely (Module 3). And the whole discipline replicates
planetary-scale through git itself — content-addressed, hash-chained,
CRDT-merged — so a mesh of cheap boxes can audit and recover from
anything short of losing every copy (Module 4). Five open problems
(§5) mark where the design is still vapor. Side quests (§6) mark what
deliberately stays out of scope.

## Contents

| File | What it is |
|---|---|
| `00-foundations.md` | The tripartite model; why intent is physical; the universal vocabulary (tile, dial, upstream trigger, intent mask, course) |
| `01-module1-dual-signal-input.md` | Weeks 2–4 + Labs 1–3: the physical stream and the translation matrix |
| `02-module2-temporal-ledger.md` | Weeks 5–7 + Labs 4–5: double-entry state history, bidirectional trace |
| `03-module3-grafting-and-rollback.md` | Weeks 8–10 + Labs 6–8: freeze, splice, lock-free compaction, settlement |
| `04-module4-planetary-replication.md` | Weeks 12–13 + Lab 9: the `.bpp` blueprint patch and the sovereign audit |
| `05-open-problems.md` | The five gaps the conversation itself named |
| `06-side-quests.md` | Related threads deliberately deferred |

## The universal vocabulary (use these words, or be misunderstood)

- **tile** — smallest unit of durable comprehension
- **dial** — smallest unit of runtime modification
- **upstream trigger** — a signal that pre-dates and determines later behavior
- **intent mask** — the live structure of what the system is currently for
- **course** — an emergent path through state space, not a syllabus
