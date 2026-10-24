# Situation template

*Copy this. Fill every field. A Situation with no machine-checkable acceptance
test is a daydream; a Situation with no gap is a postcard from a place that costs
us nothing to visit. Both are rejected at the door.*

```
# <title> — Situation <id>, horizon <N years out>

WORLD
  The setting, lived-in, concrete, sensory. Not a pitch — a place. The mature
  capability is plumbing here; nobody in the scene is impressed by it. That
  ordinariness is the whole method: it lets the seams show as friction, not
  spectacle.

CAST  (4–6)
  For each character:
    - name, role
    - the mature capability they embody (a rung, lived)
    - 2–3 keyword-vectors in the erised style (e.g. trust+0.5, ask-0.2) — the
      character sheet; opposite valences on the same noun are where scenes ignite

LIVED CAPABILITIES
  What this world takes for granted that today's stack cannot yet do. Bullet it.

GAPS
  Each: { id (G##), what the future has that today lacks, the failure it prevents }
  Prefer NEW gaps (G11+). A gap must cost us something or it teaches nothing.

ACCEPTANCE TESTS
  For each gap: a MACHINE-CHECKABLE predicate — a scenario an engineer could code
  against jev-quilt / erised today, plus the exact pass condition. Not prose.
  (e.g. "warm-start on regime B from A's commons reaches target in < K generations,
  transfer degrades monotonically with regime distance, 0 illegal.")

TRAINING OBJECTIVE
  for_humans:  what a kid → deckhand → engineer learns by playing/building it
  for_models:  what an agent learns (often: to author or close a gap)
  ladder_level: where it sits in situations/TRAINING.md

ITERATIVE LOOP
  How playing/building it advances the frontier:
  fiction → gap → situation → wide run → merged rung → new fiction.

DUAL TRACK
  toy:        the table version that teaches the law (for the next generation)
  industrial: the rough-seas version (offline, deterministic, provable on reboot)

LINEAGE
  erised:    which preset/scenario it could run as
  jev-quilt: which rung/module it compiles toward
  forward:   which reverse-actualization story it extends
```

## Rules of the form

1. **The future has to cost us something.** No gap, no Situation.
2. **The test is machine-checkable or it is not a test.** Compile it into
   `GAPS.md` as a predicate against a named module.
3. **Two builds, one kernel.** If the toy and the industrial build need
   different laws, the Situation is wrong, not the kernel.
4. **Honesty about limits.** Mark anything you cannot yet ground as STRETCH or
   FICTION — the same discipline as the physics companions in the Forward Arc.
5. **Ordinariness is load-bearing.** If the characters are amazed by the tech,
   you have written a demo, not a Situation. Let it be plumbing.
