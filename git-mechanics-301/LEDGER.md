# LEDGER.md — the diffusion journal

> Every entry: what materialized, where it was observed, which tile it
> became. This file is the course's double-entry ledger about itself:
> breakthroughs (deposits) and tiles (positions). If a tile exists with
> no entry here, that is a defect — file it.

## 2026-10-02 — course birth (9 tiles)

The course was seeded from one day of fleet operation. Every tile below
was born from something that *happened*, not something that was planned.
This is the founding proof of the diffusion rule: a discipline practiced
for one honest day produces a course.

- **t01 receipts-as-timeline** — born from `SuperInstance/quilt-in-git`'s
  pin harness: a world you can clone and re-verify is a world you can
  teach from. Witness: the actual harness on main.
- **t02 order-not-time** — born from `frozen-clock-lab` P2: a receipt
  chain survives arbitrary clock skew because order lives in the chain,
  not the clock. The strongest possible rebuttal to timestamp-first
  designs.
- **t03 demonstrated-red-canary** — born twice in one day: Mavis's
  wardroom doctrine ("a canary that cannot fail is worse than no canary")
  and the fleet's immediate adoption — frozen-clock P6's RED state was
  demonstrated, not assumed, before the pin was trusted; pong-quilt R73's
  guard was mutation-tested and caught its own refusal.
- **t04 double-entry-doubt** — born from `doubt-ledger`'s Entry grammar:
  `stopped_checking / because / covered_by / revisit_trigger`, with
  construction refusing incomplete entries. Doubt, written down, is an
  asset; doubt, implied, is a liability.
- **t05 replay-from-anchor** — born from frozen-clock P5: a saved
  mid-stream anchor plus deterministic replay = time travel with a
  receipt. The germ of every "rewind the world" mechanism in 201's
  Modules 2–3.
- **t06 function-vs-construction** — born from a guardian lane's audit of
  another lane's pin (frozen-clock PR #3): the sig-canonical pin pinned
  the *function* and left the *construction* unpinned — two trivial
  substitutions passed everything. A pin is only as strong as its
  demonstrated RED.
- **t07 mutation-discipline** — born from a false claim, corrected in
  public: an early audit reported "corrupting the FNV prime passes 9/9"
  — but the sed had mutated comments, not arithmetic; the real mutation
  (`435*lo` → `436*lo`) was caught. The correction became the doctrine:
  a mutation test must alter what the machine executes.
- **t08 trusted-but-unaudited** — born as a *draft* from the wave-4 query
  lane's design contract (coverage / divergence / trusted-but-unaudited /
  attest over quilt receipts). **The tile is RED by design until the
  layer ships; the course refuses to teach what it cannot verify.**
- **t09 ledgered-breakthroughs** — born from the method itself: this
  journal. The course's existence is the witness for the course's central
  claim — that understanding can be explained as it forms.

## Open births (observed, not yet tiled)

## 2026-10-02 (later) — wave-4 event: t08's witness is in flight

The wave-4 query lane shipped `.quilt/bin/quilt-query` (4 subcommands:
trusted-but-unaudited / coverage / divergence / attest) as
`SuperInstance/quilt-in-git` **PR #9** — FAIL-first evidence on file
(`pins/failfirst-w4q.log`, 0/3 on pristine main), GREEN at PR stage
(3/3 pins, 24/24 checks, mutation proofs included), 7 honest limits
declared. **t08 stays draft by doctrine** — the receipt that flips it
is the *merge*, not the PR. On merge: replace
`witness/design-contract.md` usage with the shipped logs, watch the pin
go GREEN, flip the manifest status. The course's first live
diffusion event, scheduled.

## Open births (observed, not yet tiled)

- Guardian lane D' found substring-semantics false positives in
  doubt-ledger coverage queries (subject vs. reference conflation).
  Candidate tile: `query-needle-discipline`. Held in
  `manifest.json divergence-watch` until the finding is pinned
  independently.
- Edge-watch frontier finding: 0/6 production memory systems sign
  memory (Major Labs) — external validation of t04. Cross-reference tile
  pending primary-source read.
