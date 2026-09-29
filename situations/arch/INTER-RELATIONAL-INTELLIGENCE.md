# Inter-relational intelligence — saving the system so a model can learn to decompose

*A design-mark (2026-09-29). Owner's brushstroke: "to work through, we will leave artifacts of
systems that worked for something. And the inputs and outputs of that greater system can be data
of the inter-relational-intelligence for modeling the SuperInstance as a thing. That's the broad
brushstroke you're not going for as much as making sure the right information is saved so that when
the time comes, a model can help decompose." This mark makes that concrete: a uniform capture
schema for every manager↔crew situation, so the fleet's own operation becomes a decomposable
corpus. Ties to `fishing-fleet` (the loop), `ML-IN-THE-LOOP.md` (the loop emits its dataset),
`THE-WEAKEST-CLAIM-METHOD.md` (the fold), and `github.com/SuperInstance/MicroMoth-quilt` (in-env
un-gameable dice + the receipt idiom).*

## The reframe: the deliverable is the transcript, not the repo

We keep shipping repos (Syzygy, labs/*, cross-poll manifests). Those are the *silver* — useful,
but not the point. The point the owner is naming: **the manager↔crew system is itself a cell, and
its inputs and outputs are the gold.** When an Opus captain routes work to a cheap-API crew, folds
their output through JEV, draws an un-gameable choice from the dice, keeps one candidate and drops
five, and books a mark — that whole trajectory is a *worked example of decomposition.* If we save
it in a decomposable form, a future model can learn the one skill this fleet runs on: **taking a
compound thing apart, locating where the truth or the value lives, and recombining.**

So "make ideas into repos that work" has a second, quieter product riding underneath it: **every
situation we run should leave a structured transcript of how the greater system related its parts.**
The repos are what worked; the transcripts are *how the working happened* — and the second is the
training set for modeling the SuperInstance as a thing.

## Why "inter-relational"

Per the RSI-as-relationships framing (`SYZYGY-PRODUCTION.md`): a cell is a relationship (in ↔ out ↔
witness), a verdict is a relationship (a reader folds evidence — Law 6), a route is a relationship
(task ↔ crew), a fold is a relationship (whole ↔ parts). **Intelligence here is not in the nodes;
it is in how they relate.** So the corpus must record *relations*, not just events — each record
names what it folded (its `refs`), so the transcript is a **graph**, not a flat log. A model
trained on nodes learns facts; a model trained on this graph learns to *decompose and route* —
which is the manager's actual job, and the thing we want to hand off.

## The capture unit: a situation transcript (hash-chained, replayable)

One **situation** = one manager+crew mission (a dispatch). Its transcript is an append-only JSONL
receipt ledger — the *same idiom MicroMoth-quilt already uses for quantum circuits* (every step a
cell, fnv1a-64 chained, tamper-evident, replayable). Every line is one **relation-record** with a
common envelope and a typed body:

```
envelope:  sid   situation id (stable per mission)
           seq   monotonic index within the situation
           ts    ISO-8601 UTC
           actor {tier: dispatcher|captain|crew|referee|dice, id: model/engine, session}
           rel   the relation type (verbs below)
           refs  [hashes of prior records/artifacts this record folds]   ← the graph edges
           hash  fnv1a-64(prev_hash + canonical(body))                    ← the chain
```

The **relation verbs** (deliberately few, echoing the org's cell algebra `BIND/LINK/EFFECT/VIEW/
TICK`) are the primitives of inter-relational intelligence:

| `rel`     | who emits it | what it records (the body) | what a model learns from it |
|-----------|--------------|----------------------------|-----------------------------|
| `TASK`    | dispatcher→captain | the mission/brief (input) | the space of goals |
| `ROUTE`   | captain      | sub-task → chosen crew/tool + why | the **dispatch policy** |
| `DRAFT`   | crew         | prompt+params → response (or its hash) | the generators' behaviors |
| `DRAW`    | dice         | request → un-gameable value + receipt (Bell S / collapse-ledger id) | where exploration was *forced*, not steered |
| `FOLD`    | referee (JEV)| compound claim → leaf claims, per-leaf verdicts, **argmin (located weakest)**, **gap (whole − folded)** | **decomposition itself** |
| `KEEP`/`DROP` | captain  | candidate + verdict-refs + reason | the **value function** (the label) |
| `MARK`    | any          | a durable artifact written (commit/doc/receipt), content-addressed | provenance / grounding |
| `OUTCOME` | any (later)  | realized downstream result (CI green/red, revert, speedup) | the **delayed label** |

The `FOLD` record is the one the owner singled out ("clever setups for decomposing JEV calls"):
we do **not** save only the scalar verdict. We save the compound claim, every leaf, every leaf
verdict, the **located weakest** (argmin), and the **gap** between the whole-claim verdict and the
folded parts — because the gap is the datum that teaches *how much a single number hid.* A corpus of
FOLD records is a corpus of decompositions with their answers attached: the exact thing a model
needs to learn to decompose.

## MicroMoth-quilt: the in-env dice and the idiom to copy

The owner said to use MicroMoth-quilt "in our environment." It fits twice:

1. **As the un-gameable dice with no network.** `micromoth.py` is stdlib-only pure Python; a Bell/GHZ
   circuit + `shots` gives quantum-shaped draws locally, and `tools/collapse_ledger.py` seals each
   measurement as a receipt. When the Moth API is rate-limited, balance-gated, or CF-blocked, the
   crew still gets `DRAW` records — with a **collapse-ledger receipt id** instead of a Bell-S from
   the network. Same relation, local provenance. Dog-fooding in our own environment, exactly as asked.
2. **As the receipt idiom to copy.** MicroMoth-quilt already answers "what if a circuit *were* a
   hash-chained receipt ledger?" The situation transcript is the same answer for a *dispatch*: what
   if a manager↔crew mission were a hash-chained receipt ledger? So the recorder reuses its
   fnv1a-64 chaining and its `receipts/expNNN.json` shape — one fewer idiom to invent, one more
   relationship made explicit between two cells of the fleet.

## What a model does with the corpus (why we bother)

Once transcripts accumulate across many situations, a model trained on them can:

- **Learn the dispatch policy** from `ROUTE`→`OUTCOME` pairs (which crew/tool for which task, by
  realized cost/quality) — this is `ML-IN-THE-LOOP.md`'s *learned dispatch router*, now with a clean
  input format.
- **Learn to decompose** from `FOLD` records — predict the leaves of a compound claim and where the
  weakest one is, i.e. learn to *make the argmin move itself*, not just consume JEV's.
- **Learn the value function** from `KEEP`/`DROP` labels grounded in `OUTCOME` — what a captain's
  judgment was worth after the fact (booked scars included, which are the clean negatives).
- **Model the SuperInstance as a thing** — the joint distribution over relation-records *is* a model
  of how the fleet relates its parts. That is the "thing" the owner wants modeled: not a heap of
  repos, but the living graph of routes, folds, draws, and judgments that produced them.

The honesty rule from `ML-IN-THE-LOOP.md` carries straight over: a booked scar beats a covered
result *because a hidden failure is a mislabeled example.* Clean transcripts are clean training data.

## The build (small, so it's earned)

- `labs/situation-recorder/` — a zero-dep recorder (stdlib Python) that emits the JSONL transcript,
  chains the hashes, and validates a chain. Reusable by any captain/director. Ships with a self-test
  that builds a demo situation and re-verifies the chain (replayable = the MicroMoth-quilt property).
  **This is the first cell; build it now, here, from this session (git-only, no keys).**
- Directors, once budget returns, **emit a transcript per situation** into `situations/transcripts/`
  (the WAL for the corpus), not only prose commits. The prose commit stays — it's the human-readable
  time-capsule — but the transcript is the machine-readable one beside it.
- The `fishing-fleet` skill gains a "leave a transcript" clause (the schema above), so the capture
  is doctrine, not an afterthought.

## The one-line version

Stop treating the crew's repos as the whole product. **Record how the manager related its parts —
route, draft, draw, fold, keep, drop, outcome — as a hash-chained graph, so the SuperInstance's own
way of decomposing becomes the corpus a future model learns to decompose from.** The system that
worked is the training set; save it on purpose.
