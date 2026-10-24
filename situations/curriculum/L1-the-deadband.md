# L1 — The Deadband

> *Nobody polls. You speak only when something changed — and only if it changed
> enough to matter.*

**The law:** Hooks eat deltas, not values (Law 2). A cell does not wake because a
value is *present*; it wakes because a value *changed* past a floor. The ordinary
chop never wakes it. The real change is never buried in false alarms.

**Who this is for:** a kid ready for a second rung, a deckhand learning to stand a
watch, a model learning that "no update" is a valid and often correct output.

**Build against:** `jev_quilt/cell.py` (`Hook`, `DEADBAND`, `Hook.when`).

---

## The toy — the table version (the sea taken out)

You need: the thermometer or tide chart from L0, and quiet.

**The game — "only if it changed."**

Set a **deadband** out loud first: *"We only call the tide when it moves more than
a hand's width."* Now everyone watches the chart. The rule is brutal and simple:

- If the reading **changed more than the deadband** since the last call — you call
  it. *"Tide up two hands."*
- If it **didn't** — you **stay silent.** Silence is the correct answer. Silence
  is *work being done well.*

Two ways to lose, and a kid learns to feel both:

- **The Crier** calls every tiny wiggle — *"up a fingernail! down a fingernail!"* —
  and drowns the table so nobody hears the real move when it comes. That's a
  **`chop-scar`**: woke on noise.
- **The Sleeper** sets the deadband so wide they miss the tide turning. Also a
  **`chop-scar`**: slept through the change.

The win is the *quiet, correct* watcher who says nothing for ten minutes and then
exactly one true thing. This is the hardest lesson for a child (and for a chatty
model): **doing nothing, on purpose, is the job.**

**The `when` twist (touch shallow):** add a second rule — *"only call the tide if
we're actually fishing this hour; ignore it otherwise."* Now the watcher declines
deltas that are real but *not theirs to care about.* That's `Hook.when` — a hook
eats deltas, but it also **declines deltas whose shape isn't its business.**

---

## The industrial version — the same law, the sea put back

A bilge alarm on a boat in a gale. The water is *always* sloshing — that's the
chop, and an alarm that fires on chop is an alarm the crew learns to ignore, which
is the same as no alarm. The `Hook` with a `DEADBAND` floor eats the slosh and
wakes the crew only on a real rise. Rough water *is* noise; the deadband is what
lets the one real leak be heard over a sea that never stops moving.

Same law, sea added: now the deadband has to survive genuine violence without
either crying wolf (crew stops trusting it) or going deaf (crew drowns). The
`Hook.when` predicate is the difference between "the bilge rose" (wake me) and "the
bilge rose because we're taking spray over the bow on purpose in this turn" (don't).

---

## The exercise (buildable today)

Wire two `Cell`s: a source that emits a noisy reading, and a watcher whose input
`Hook` has a `DEADBAND` floor. Feed it a long run of small wiggles and one real
step. Prove the watcher fires **once** (on the step) and **never** on the chop.

```python
from jev_quilt.cell import Cell, Hook, DEADBAND
watch = Cell(
    name="bilge_watch", coord=(4, 1),
    input_hooks=[Hook(source="bilge_level", floor=DEADBAND,
                      when=lambda s: s.get("fishing"))],  # decline deltas that aren't ours
)
```

Then swap `DEADBAND` for an explicit `Q16` magnitude and tune it two ways wrong
(too tight → cries wolf; too wide → goes deaf) so the learner *feels* both scars
before finding the floor that's right for this sea.

---

## The acceptance test (booked, gradeable)

A learner **passes L1** when, given a stream of 100 readings — 99 chop, 1 real
step — their watcher:

1. **fires exactly once**, on the real step, and
2. **stays silent** on all 99 chop readings, and
3. **declines** a real delta that its `when` predicate says isn't its business.

Fire on chop → **`chop-scar` (cried wolf)**. Miss the step → **`chop-scar` (went
deaf)**. Both book. A perfect run books a receipt on the skill `deadband-watch`.
The subtle grade: a learner who never fires at all "passes" the no-false-alarm test
and *fails* the real-step test — the school does not reward silence that is really
absence.

## Graduation — what L1 standing unlocks

Earn the streak and you hold **ANSWER** on `deadband-watch`: the right to **stand a
watch alone.** A learner who wakes on noise or sleeps through change cannot be left
with an alarm, human or model. This is also where a model learns the discipline
that keeps it from being a Crier: *most inputs deserve no output*, and emitting
nothing is frequently the correct, gradeable action.

Lose it — set the deadband wrong for a sea that changed — and it's revoked on the
booked-wrong; the sea moved, the chop got bigger, your old floor is now deaf. Earn
it back by re-tuning against the new water.

**In the mirror (`erised`):** Dell the watch (`presets/FIRST_SEASON.md`,
`ripple+0.5, calm+0.3, bored-0.3`) *is* this level — the calibrated deadband made
into a crewmate whose guard tightens in the flat calm. Run the L1 Situation and
watch whether Dell's net shift tops the field. If it doesn't, the fiction isn't
honest about who keeps the boat off the rocks — and neither is the lesson.
