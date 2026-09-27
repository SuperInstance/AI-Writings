# TRAINING — the situations that teach the quilt

*Two builds, one kernel — carried into teaching. Every level here ships a **toy**
(small enough to teach the law at a kitchen table in an afternoon) and an
**industrial** version (the same law with the sea put back — offline,
deterministic, provable after a reboot). The toy is not the beginner's version
and the industrial the expert's; they are one lesson, and a learner who cannot
run the toy has not earned the boat. Never let the two drift into two different
laws.*

This is the fleet's training system, built **on top of** `jev-quilt/docs/FRONTIER.md`
(the teaching ladder R1–R6 and its eight rungs) and run **inside** `erised` (the
cooperative-fiction engine — scars, ticks, rewinds). FRONTIER sketched the ladder;
this file is the school that climbs it — the same rungs, deepened into gradeable
Situations, walked by two kinds of learner at once: **the next human** (a kid, a
deckhand, a new engineer) and **the next model** (an agent learning to decide, then
to author its own gap). One law. Different learners. The sea is the only variable.

---

## The premise: the curriculum is built from the substrate

Most schools teach a subject with tools borrowed from somewhere else — a grade
book, a proctor, a certificate on a wall. Ours can't, and shouldn't. The five
laws of jev-quilt are strong enough to teach *themselves* if the school is built
out of them. So it is. The training system is **quilt-shaped**: it obeys the same
five laws it teaches, which means a learner who masters the substrate has already
been living inside a working example of it — themselves, in the class, being
booked and graded and pooled exactly like a cell in a fleet.

Four claims, and each is a law wearing a teacher's coat:

1. **A learner is a cell.** Identity `(k, s)` never floats: `k` is *who* (this
   kid, this deckhand, this model checkpoint), `s` is *what skill*. "Casey learned
   the deadband" is a coordinate, not a vibe. (Law 1 — `q16`, `cell.Cell`.)

2. **A lesson is a hook on a delta, not on a value.** You do not advance because a
   value was *present* in front of you (the answer was on the board); you advance
   because something *changed in you* above your own deadband. "I already knew
   that" registers as **zero delta** and does not promote — the same way a hook
   declines the ordinary chop. Parroting is a value; being changed is a delta. The
   school eats deltas. (Law 2 — `cell.Hook`, `DEADBAND`.)

3. **Mastery is earned, revocable standing on a skill — and the diploma is a
   replay, not a certificate.** A learner earns standing on a skill exactly as a
   cell does: a booked streak of correct decisions on that skill's residue-key
   confers **ANSWER** — the right to stop asking, to act cold. A *single* booked-
   wrong outcome revokes it. Because standing is derived by **replaying the book**
   (`standing.Standing.from_book`), a graduate can *prove* what they know after a
   reboot — and can *lose* it with no examiner in the loop when the world drifts
   under the proof. (Law 4 + Law 5 — `bookkeeper`, `standing`.)

4. **A class is a commons.** A cohort's proven routes pool into one shared,
   content-addressed memory over `fold.mmr_root`; a green learner reads the
   commons and *answers cold* on the handful of things the cohort already proved,
   instead of re-deriving them from zero. Deposits are confluent — the order
   students learn in doesn't change what the class knows. And the inheritance is
   as revocable as everything else: a pooled route whose sea has moved is torn up
   for the whole class at once. (R2 — `commons`, `standing`.)

Learn the substrate and you have been *run on* the substrate. That is the whole
trick. The school is the syllabus.

---

## The levels (one line each)

| Level | Law it teaches | Module you build against | Learner | Toy → Industrial |
|---|---|---|---|---|
| **L0 — The Typed Number** | Identity never floats: `0.73` *as what?* | `q16.Q16`, `cell.Cell.coord` | a **child** (6+) | a jar of coins & a tide chart → a sensor read the boat bets gear on |
| **L1 — The Deadband** | Hooks eat deltas, not values; decline the chop | `cell.Hook`, `DEADBAND` | a deckhand / kid | the "only say it if it changed" game → a bilge alarm that never cries wolf |
| **L2 — The Book & the Reboot** | Every change is booked; replay ≡ live; prove it cold | `bookkeeper.Bookkeeper`, `fold.mmr_root` | a new engineer | index cards you can replay the day from → a cell woken cold after a crash |
| **L3 — The Ripple in the Calm** | Confidence is earned, not assumed; standing is revocable | `calibrate.CalibratedFloor`, `standing`, `predictor.surprise` | deckhand → skipper | spot the rigged card in a flat deck → the rogue set in a long flat sea |
| **L4 — The Authored Gap** | A learner names a thing it cannot yet do, writes the test, and closes it | `inquire`, `imagine`, `engine`, `bookkeeper` | a **model / agent** | "invent the next chore, then pass it" → the self-directing compiler (G6/G10/`G-auto-1`) |

Every level is a triple, and the triple is the level:

- a runnable **erised Situation** (the drama that makes the law *cost* something —
  scars, ticks, rewinds; the cast from `presets/FIRST_SEASON.md` is the faculty);
- a buildable **jev-quilt exercise** (a named module, a real test to make pass);
- a gradeable **acceptance test** (booked, so passing it is a receipt, not an
  opinion).

Detailed level files live in `curriculum/`.

---

## The two-builds discipline, in teaching

The FRONTIER doctrine — *build the toy so the law can be seen, build the
industrial so the law can be trusted, and never let them drift into two different
laws* — is the pedagogy, verbatim. In this school it has three teeth:

- **Same kernel, checkable.** The toy and the industrial build cite the **same
  jev-quilt module**. `examples/rough_seas.py` (ten lines a kid can read) and the
  `CalibratedFloor` a boat runs are literally the same `calibrate.py`. A level that
  can't point both builds at one module has smuggled in a second law and is
  rejected.
- **The sea is the only variable.** To turn a toy into its industrial build you
  *add the sea* — noise, offline operation, a cold reboot, an adversary, a clock —
  and change nothing else. To turn an industrial build back into a toy you *take
  the sea out*. If you had to change the law to cross that gap, the toy was a lie.
- **Graduation requires both.** You have not earned a level by passing the toy.
  You earn it by passing the toy **and then** surviving the same law with the sea
  put back. A kid who names `0.73 as feet-of-tide` at the table has seen the law;
  the deckhand who trusts that number when the plotter dies at 3 a.m. has earned
  it. The school does not confuse the two — but it insists they are the same
  number.

---

## The assessment model

Grading is not bolted on; it *is* the substrate, pointed at the learner.

### Scars are the failure taxonomy — the honest one

We do not grade on a curve or a rubric of opinions. We grade on **scars**
(`erised`'s `addScar`, bound to a tick + kind + note). A scar is a booked failure:
a call that came up empty, a set that lost gear, a moment a learner acted on
standing the water then proved wrong. Scars **persist through rewinds** — you can
re-run the round, but you cannot patch over having failed it. The scar list is the
transcript that matters, and it is honest by construction: it records what
*happened*, not what a grader felt. The kinds of scar *are* the taxonomy of ways
to fail this substrate:

- **`float-scar`** — you let identity float ("0.73" with no unit, a coord that
  drifted). The L0 failure.
- **`chop-scar`** — you woke on noise, or slept through the real change: a
  deadband set wrong in either direction. The L1 failure.
- **`amnesia-scar`** — a change you never booked, so replay ≠ live; you could not
  prove the day cold. The L2 failure.
- **`bored-middle-scar`** — legal the whole time, over-confident the whole time;
  the ripple you slept through in the flat calm. The L3 failure.
- **`hoard-scar`** — standing (or ticks) held and never spent, which is worth
  nothing; the deckhand who never dared act on what he'd earned.
- **`overreach-scar`** — you acted on standing you had not earned, or that the sea
  had already revoked; the skipper's gut, wrong, spending the crew's trust.
- **`ungapped-scar`** (L4) — you claimed a capability you could not name a test
  for; a boast with no predicate.

A learner's scar list is their true record. It rewinds; it does not erase.

### Standing is earned, revocable, and provable cold

Passing a level does not hand you a certificate. It confers **standing on a
skill**, derived the way `standing.verdict()` derives it for a cell: a booked
streak of correct decisions on that skill's residue-key returns
`('ANSWER', proven)` — you have earned the right to *stop asking* and act on this
skill cold. The rules that make it honest are the same rules that make a cell
honest:

- **Earned, never self-granted.** ANSWER only ever names an answer the *book*
  proved. A learner cannot declare themselves competent; the receipts do.
- **Revocable by one miss.** A single booked-wrong outcome on the skill tears the
  standing up. You earn it back the way you earned it — by asking, and being right,
  again.
- **The reboot exam.** Assessment is not a proctored final; it is a **cold wake**.
  Come back a season later (a human on the beach for the winter; a model reloaded
  from a checkpoint) and *replay your own book against today's sea*. Standing
  survives only if replay still equals live (Law 4). This is the boat's oldest
  rule made into a grade: you do not trust gear — or a deckhand, or a model — that
  cannot prove itself after a power cycle.
- **Revocable by drift, with no examiner in the loop.** This is the mechanic the
  school is built around (below). A skill whose *world moved* revokes its own
  standing the first time the learner acts on it and the water disagrees. A
  certificate cannot expire itself; a booked standing can, and must.

### The commons: a class inherits what the cohort proved

A cohort is not a set of individuals graded in parallel; it is a **commons**
(`commons.Commons` over `fold.mmr_root`). Every learner's proven routes are
deposited, content-addressed, and confluent — the order students learn in cannot
change what the class knows (`A.merge(B).root() == B.merge(A).root()`). Two
consequences the school runs on:

- **Pooled standing is real standing.** Ten deckhands each with a streak of one on
  "reading the flat-calm ripple" sum to a fleet weight of ten. A fresh learner
  reads the commons and **answers cold** on that route — inherits the cohort's
  proof instead of re-deriving it from a blank sea. The class is faster than any
  student because the class remembers.
- **Inheritance is as revocable as everything else.** When a pooled route's sea
  moves, the booked-wrong that proves it tears the route up **for the whole class
  at once**. A cohort cannot pass down a lesson the world has retired. This is the
  difference between a living commons and a dead syllabus.

---

## The clever core: standing the sea can revoke

The single mechanic the whole school turns on: **a diploma that can expire itself,
with no examiner deciding to expire it.**

A paper certificate is a *value* — a frozen claim, true forever regardless of the
world. Standing on the quilt is a *replay* — a claim that is only as true as the
last time the book agreed with the water. So we grade the way a boat trusts gear:

> Your standing on a skill is not a thing you *have*. It is a thing your book keeps
> *proving*, one decision at a time, against a sea that keeps moving. The day the
> sea moves under a proof you earned, the next honest decision books wrong, and the
> standing tears up — not because a teacher failed you, but because the world did,
> and the book is honest about the world.

This is why the toy and the industrial build must be one law. A certificate earned
on the calm pool would stay valid forever; standing earned on the calm pool is
**re-tested by the sea every time it's used**, and quietly retired when it stops
being true. It makes three otherwise-hard things fall out for free:

- **Honest expiry.** No arbitrary "recertify every N years." A skill expires
  exactly when — and only when — the world it named has changed enough to break it.
- **Symmetry between human and model.** A model checkpoint reloaded onto a shifted
  task distribution and a deckhand back from a winter onto a moved fishery fail the
  *same way*: replay ≠ live, standing revoked. One mechanism, two learners.
- **A failure that isn't shameful.** A revoked standing is a scar, and a scar is
  data, not a verdict on the person. "The fishery moved" is a `bored-middle-scar`
  or an `overreach-scar` on the log — a true note about the water, earned live,
  that tells you exactly which token to change on the rewind.

---

## One ladder, two learners

The human and the model climb the **same rungs against the same tests**. The
divergence is never in the law; it is only ever in *how much sea* the learner can
already stand.

| | The human learner | The model / agent learner |
|---|---|---|
| **Identity `(k,s)`** | who you are, which skill | which checkpoint, which skill-head |
| **The lesson-as-hook** | you advance when *you* changed | weights advance only on above-deadband loss deltas — no update on noise |
| **The book** | index cards, a scar log, a season's diary | the receipt chain the training run already writes |
| **The reboot exam** | back from the winter, onto a moved fishery | reloaded from a checkpoint, onto a shifted distribution |
| **Standing** | the right to act without asking the deck | the right to `ANSWER` from the commons instead of re-inferring |
| **The commons** | the crew's pooled proven routes | the fleet's pooled proven routes (sheaf-gossip, one 32-byte compare) |
| **The top rung (L4)** | "here is a chore I can't do yet, and its test" | the self-directing compiler that authors and closes a gap |

The models are not being trained *instead of* the humans, and not *to replace*
them. They are the other learner at the same table, held to the same booked proof,
so that when a human says "the model knows this cold" they mean the *identical*
thing they mean about a deckhand who's earned standing: the book proved it, and the
sea can still revoke it. That symmetry is the safety property. A model whose
competence is a certificate is a boast; a model whose competence is a revocable,
replayable standing is crew.

---

## The graduation graph — what each level unlocks

Standing compounds up the ladder the way it does in a fleet: you cannot earn the
higher rung until the lower one holds under the sea.

- **L0 (Typed Number) →** unlocks the right to be *given a reading to act on*. Until
  a learner never lets identity float, no one hands them a number that costs gear.
- **L1 (Deadband) →** unlocks the right to *stand a watch alone*. A learner who
  wakes on noise or sleeps through change cannot be trusted with an alarm.
- **L2 (Book & Reboot) →** unlocks the right to be *left in charge across a
  reboot* — a night watch, a solo haul, a checkpoint reload. If you can't prove the
  shift cold, you can't own it.
- **L3 (Ripple in the Calm) →** unlocks **earned standing itself** — the right to
  act on your own read without asking the deck, and to answer from the commons. This
  is the rung where a deckhand becomes crew and a model earns `ANSWER`.
- **L4 (Authored Gap) →** unlocks the right to *change the curriculum* — to author
  the next level's gap and its test, gated by a human yes. A learner who reaches
  L4 stops being taught the ladder and starts extending it. This is `G-auto-1`: the
  system authoring its own gap, now the school authoring its own next rung.

The graph is a partial order, not a line — a learner can hold L1 standing on
"bilge watch" and still be earning L0 on "engine temp." Standing is per-skill,
per-coordinate, always.

---

## The self-authoring level (why the school never finishes)

`G-auto-1` — the gap where the system authors its own gap — becomes, in the school,
the level that writes the next level. When a cohort's commons shows that every
learner holds firm standing on L0–L4 for the current fishery, L4's compiler cell is
turned loose (gated by a human yes) to **probe the frontier to its breaking point,
author a new Situation with a machine-checkable acceptance test, confirm the cohort
currently fails it, and file it as `L5-*.md`.** The curriculum is then, itself, a
cell that has earned the standing to extend the ladder — booked, revocable, and
pooled. A school built from the substrate does not graduate its last class; it
hands them the pen.

---

## Running the school

1. **The table (toy).** No network, no tokens, no models required. Open a level
   file in `curriculum/`, run its toy at the kitchen table (L0–L2 need nothing but
   coins, cards, and a tide chart), or run the ten-line jev-quilt example it cites
   (`python examples/rough_seas.py` for L3). This is where the law is *seen*.
2. **The mirror (drama).** Open `erised`'s `index.html`, load
   `presets/FIRST_SEASON.md` as the faculty (Mara the skipper is L3's earned
   standing; Jonah the deckhand is the learner climbing L0→L3; Dell the watch is
   L1/L3's calibrated floor; Sig the memory is L2's book; Pol the refusal is the
   human-yes gate on L4). Tick through the level's Situation. Let it break where it
   breaks. When a scar lands, rewind, change **one** token — the smallest one that
   answers the break — and tick again. This is where the law is made to *cost*.
3. **The boat (industrial).** Build the level's exercise against the named
   jev-quilt module, make its test pass, and then **put the sea back** — run it
   offline, kill it mid-run and replay, feed it noise, shift its world — until the
   same law holds. Book the run. The receipt is the grade. This is where the law is
   *trusted*.

You have earned a level when its scar is on your log (you have failed it honestly
at least once), its jev-quilt test passes, and your standing on it **survives a
cold reboot against today's sea.** Then it goes into the commons, and the next
learner inherits it — until the sea moves, and the class earns it again.

---

*Filed on top of `jev-quilt/docs/FRONTIER.md` (the ladder R1–R6), run inside
`erised` (`presets/FIRST_SEASON.md`, `presets/VALLEY.md`), and graded against the
Forward-Arc gaps (G2–G10, `G-auto-1`). Levels in `curriculum/`. Two builds, one
kernel — and the school is the kernel, teaching itself to the ones who come next.*
