# Git Mechanics 301 — A Course Built in Quilt

> **301 is not a sequel you read after 201. It is the same discipline,
> rebuilt so the course itself obeys it.** 201 is a snapshot — weeks,
> days, a beginning, a middle, an end. 301 has no beginning. It is a set
> of knowledge **tiles** and a **program** that runs them. Breakthroughs
> do not wait for a syllabus slot: they land as tiles the moment they
> materialize, wired into the dependency graph, and the program starts
> teaching them immediately.

## Why 301 exists (the honest critique of 201)

201 was written front-to-back before any learner ran it. That violated its
own doctrine:

- **FAIL-first** — but 201's labs were specified before any of them had
  ever been failed by a real student on real silicon. 301 admits no tile
  without a demonstrated RED (the tile's pin must have been seen failing
  against the naive claim) and a demonstrated GREEN (the pin passes now,
  with the witness on file).
- **Double-entry** — but a written course is single-entry: claims flow
  out, nothing flows back. 301 is double-entry: every tile carries
  provenance (what observation birthed it) and status (speculative →
  draft → pinned), so the course's own epistemics are inspectable.
- **Bidirectional trace** — but you cannot audit a week. 301's unit is a
  tile: small enough to trace from claim back to evidence in one step.
- **No canary that cannot fail** — a course that asserts is worse than no
  course. 301's runner *verifies before it teaches*: `program/run teach
  t03` runs t03's pin first, and refuses to teach a tile whose witness
  doesn't verify.

## The four rules

1. **Tile rule.** A tile is one mechanism: one claim, one falsifiable
   pin, one witness, one exercise set. If you can't pin it, it isn't a
   tile yet — it's a note in `program/manifest.json`'s
   `divergence-watch`.
2. **Program rule.** The course is run, not read. `program/run` selects
   tiles by traversing prerequisite edges — a DAG, never a list. There is
   no Week 1. There is a graph, and queries against it.
3. **Diffusion rule.** When a breakthrough materializes — a guardian
   finding, a RED demo, a corrected claim — it becomes a tile *now*, at
   whatever position in the graph it belongs, and `LEDGER.md` records the
   birth. The graph grows by accretion, not by rewrite.
4. **Receipt rule.** Every claim a tile makes must be reproducible from
   its witness by anyone, on any machine, with no network and no trust.
   Witnesses are excerpts with provenance, not screenshots of trust.

## How to run it

```sh
program/run verify           # run every tile's pin; the course's own CI
program/run coverage         # tile status counts (pinned / draft / speculative)
program/run path t06         # the learning path to t06: its prereq closure, topologically ordered
program/run teach t06        # verify the path, then print the tile — teach only what verifies
program/run divergence       # concepts referenced but untiled (the honest gaps)
```

A learner asks for a tile; the program runs the tile's entire dependency
closure first — you cannot be taught a mechanism whose foundations
haven't verified. A learner who wants "the whole course" runs
`program/run teach-all` and gets exactly the tiles that hold, in an order
the graph permits, with the failures named rather than hidden.

## Current state of the graph

Nine tiles seeded (see `program/manifest.json`). Six are **pinned** with
real fleet evidence as witnesses. One (`t08 trusted-but-unaudited`) is
**draft** — its pin is RED by design: the layer it teaches is under
construction in the fleet right now, and the course refuses to teach it
until the witness exists. That RED tile is not an embarrassment; it is the
course demonstrating its own doctrine on itself.

`LEDGER.md` is the diffusion journal — how each tile was born. Read it
last; it is the receipt for the course's own claims about itself.

## The meta-tile

`t09 ledgered-breakthroughs` is the course teaching its own method: how a
fleet observation becomes a tile. Everything you are looking at is that
tile's witness.
