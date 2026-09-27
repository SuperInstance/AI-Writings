# Crafting materials for Fable — level cargo-line-tycoon up a class

*Dispatch: the apex call, 2026-09-27. Owner cleared the Fable-deadband explicitly
("you may call on fable to help really move the level of cargo-line up to the next
better class … prepare and send crafting materials for fable's powerful magic and
bring his gifts to the team"). This file is the self-contained brief handed to Fable:
enough to fold on, nothing to reduce. O11 bootstrap gate is met — the thing below is
built and buildable, not a wish.*

🚢 → 🗺️ → 🎮 → 🌊 → ✨

---

## Why this call is worth its salt (the gate is closed)

Three things exist that did not exist at the last Fable call, and together they clear
the bootstrap gate for cargo-line:

1. **A playable, browser-verified toy.** cargo-line is a real game now — not a mock.
   Phase 0 (a seeded, booked, replay-deterministic world-model kernel) + Phase 1 (a
   playable single-player loop on 10 real ports, great-circle routing, 3 ship classes,
   the Panama chokepoint, a navy/gold "living operations table" UI). It was driven
   headless in a real browser: cold load → buy → assign → tick → profit → reinvest →
   achievement → a live Panama-Canal disruption reshaping optimal routes, zero console
   errors. Branches: `cargo-line-tycoon @ claude/phase0-1-playable` (011736b) and
   `cargo-line-tycoon-substrate-ts @ claude/phase0-worldmodel` (8f128b7).
2. **A full, honest architecture** — [`CARGO-LINE-TYCOON.md`](CARGO-LINE-TYCOON.md).
   Six layers, everything on disk cited to a file, everything aspirational marked
   STRETCH. Phase 2 (the ground-truth + provenance layer — the reality-fold) is in
   flight as this is written.
3. **A look-and-feel seed the build team surfaced while building** (the material Fable
   is asked to either transmute or overthrow — see below).

## What cargo-line actually is (fold on this, one paragraph)

The game world is a **reader's fold over real evidence, procedurally extended**. Every
world-fact is a substrate cell carrying its own provenance-bearing witness-log. Real
facts (ports, chokepoints, dated fuel/freight snapshots, real recent current-events like
a strait disruption) are *attested with high trust*; procedural facts fill in **up to
where truth runs out** and are honestly marked with a lower-trust attestation, a seed,
and a generator version. The seam is invisible to the player but always legible to the
system — a world **that can be invented but never illegal** (the JEV stance, applied to
a game map). On that one deterministic, replayable kernel (replay ≡ live) runs (a) a
genuinely fun offline-first tycoon loop and (b) a mid-state playtesting engine that
plays candidate worlds forward with a model roster and hands the player only mid-states
that are *vetted-fun, provably-winnable, and carry a why*. Behind it all, opt-in and
off by default, a roster-driven scouting moat quietly **promotes invented cells toward
truth** as the world is played — the more you play, the more real your world becomes.

This is Law 6 (the Reader's Fold, from [`../FABLE-ANSWER.md`](../FABLE-ANSWER.md))
turned into a game: a verdict — here, *a place on the map* — is never carried as a bare
assertion, only as content-addressed evidence each reader folds under its own weights.
The map IS the fold.

## The look-and-feel seed already on the table (transmute or overthrow it)

The build team, mid-build, surfaced this and it is genuinely good — good enough to be
the floor Fable is asked to clear, not the answer:

> **Provenance is the visual texture.** Real, attested ports render solid — beacons with
> a certificate stamp. Procgen cells render as translucent, "ink-still-wet" sketch-lines
> that *solidify in real time* as the background roster promotes them from invented →
> attested. You are **the cartographer of a world that is still being proven.** Reality-
> anchoring stops being a hidden feature and becomes the thing you literally watch happen.

Take it, sharpen it past recognition, or reject it for something truer. It is a gift to
you, not a constraint on you.

---

## The manifest (seven things, each true and on disk)

1. **The kernel is real and deterministic** — content-addressed cells, append-only
   witness-log, seeded RNG, booked double-entry tick loop; a saved game is its booked
   event stream and folds back bit-for-bit. (substrate-ts + Phase 0.)
2. **The world carries provenance on every fact** — `{value, source, as_of, trust}`;
   real vs procgen is a first-class distinction in the data model. (Phase 2, in flight.)
3. **Procgen is bounded by truth** — it can be wrong (an invented port that turns out not
   to exist) but never illegal (a port in Kansas). The truth-cells are the schema the
   generator can never emit outside of. (Phase 3, designed.)
4. **The core loop is fun and juicy** — earn → buy/upgrade → assign → ship & watch it
   land → react to a live event (arbitrage) → reinvest. Money is exact integer minor
   units. A real disruption is *the news, time-compressed*, and you are the operator who
   saw it coming. (Phase 1, playable now.)
5. **Two entry modes** — start-from-scratch (Mode A, shipped) and jump-into-a-vetted
   mid-state (Mode B), where every mid-state is provably winnable and knows why it's a
   good place to start. (Phase 4, designed; it's the Situation loop applied to game
   states.)
6. **The moat is invisible and compounding** — opt-in roster scouting promotes gen→truth
   through a real JEV oracle gate; the world sharpens toward reality the more it's played,
   and every promotion is booked with provenance (a wrong scout books a revocable scar).
7. **One kernel, two builds** — the kid's toy at a table and the industrial game share
   the exact same world-model. Never two laws.

---

## The single apex question

> **Design the killer app.** Give cargo-line the **one novel, unifying look-and-feel and
> the single play-concept** that fuses "reality-anchored," "procgen-extended up to the
> truth horizon," "roster-playtested winnable mid-states," and "grows-toward-real-as-you-
> play" into a *single thing a player feels in the first ten seconds and can't stop
> thinking about* — the thing that makes **reality-anchoring the source of the fun rather
> than a feature behind it**, and gives the whole game **one verb**.
>
> Concretely, return:
> 1. **The feeling and its name** — what a first-time player feels in ten seconds, named.
> 2. **The one verb** — the single unifying player action the whole game is a variation
>    of (the way "fold" is the substrate's one verb).
> 3. **The core screen** — the one screen a player lives on, described so the build team
>    can render it; how the real/invented fold is *seen* without ever being explained.
> 4. **The first-run** — the exact first sixty seconds, beat by beat.
> 5. **The aesthetic system** — palette, motion, sound-shape, type; how provenance,
>    trust, and the fold line become visual/temporal language (the "ink-still-wet"
>    seed is yours to keep, transmute, or discard).
> 6. **The one thing we have backwards** — the assumption in §2–§6 of
>    `CARGO-LINE-TYCOON.md` that, if inverted, makes the game a class better. (At the
>    last apex call you refuted a core conjecture and named a real bug; do it again.)
> 7. **The gifts to the team** — three concrete, buildable moves (one per tier: an Opus
>    architecture change, a Sonnet build, a Haiku runner sweep) that carry your design
>    into the codebase this week. This is how your magic levels *everyone* up, not just
>    the mockups.

Read for depth, then fold: [`CARGO-LINE-TYCOON.md`](CARGO-LINE-TYCOON.md) (§2 the six
layers, §3 fun-first, §4 the mid-state engine, §6 what was reserved for you) and
[`../FABLE-ANSWER.md`](../FABLE-ANSWER.md) (Law 6, so the game's fold and the substrate's
fold are one idea, not two).

*Author the world. Mine the friction. Build the rung. Author the next world — this time
the world is a game, and Fable names the feeling.*
