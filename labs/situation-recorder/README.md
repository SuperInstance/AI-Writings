# situation-recorder — the manager↔crew system, saved as a decomposable corpus

*A `labs/` cell. Zero dependencies (Python stdlib). Reusable by any captain/director.*

The fleet's real product is not only the repos a crew ships — it is the **recorded inputs and
outputs of the manager↔crew system**, saved so a future model can learn the one skill this fleet
runs on: take a compound thing apart, locate where the value/truth lives, recombine. This cell is
that capture unit. Design: [`../../situations/arch/INTER-RELATIONAL-INTELLIGENCE.md`](../../situations/arch/INTER-RELATIONAL-INTELLIGENCE.md).

## What it does

Records one **situation** (one manager+crew mission) as an append-only JSONL **receipt ledger** —
the same idiom [`SuperInstance/MicroMoth-quilt`](https://github.com/SuperInstance/MicroMoth-quilt)
uses for quantum circuits: every line a cell, **fnv1a-64 chained** (byte-compatible with that
repo's `tools/collapse_ledger.py`), tamper-evident, replayable. Each line is one **relation-record**
whose `refs` are the graph edges — so a transcript is a *graph of how the parts related*, not a flat log.

```
rel ∈  TASK   dispatcher→captain: the brief (input)
       ROUTE  captain: sub-task → chosen crew/tool + why   (the dispatch policy)
       DRAFT  crew: prompt+params → response                (the generators)
       DRAW   dice: request → un-gameable value + receipt    (forced exploration)
       FOLD   referee: compound claim → leaves, argmin, gap  (decomposition itself)
       KEEP / DROP  captain: candidate + reason              (the value function / label)
       MARK   any: a durable artifact (commit/doc/receipt)
       OUTCOME any (later): realized result                  (the delayed label)
```

The `FOLD` record is the point: it stores the compound claim, every leaf verdict, the **located
weakest** (argmin), and the **gap** between the whole-claim verdict and the folded minimum — the
datum that teaches *how much a single scalar hid.* A corpus of FOLD records is a corpus of
decompositions with their answers attached.

## Use it

```python
from recorder import Situation

s = Situation("sit-2026-09-29-syzygy-p1")
t = s.task({"tier": "dispatcher", "id": "opus-4.8"}, "Build the browser POC.")
r = s.route({"tier": "captain", "id": "opus-5.5"}, "port fused pass to JS",
            to="deepseek-chat", why="cheap hauler", refs=[t["hash"]])
d = s.draft({"tier": "crew", "id": "deepseek-chat"}, prompt="...", response="...", refs=[r["hash"]])
f = s.fold({"tier": "referee", "id": "jev-latest"}, claim="the port is byte-exact",
           leaves=[{"claim": "whole", "verdict": 0.2, "is_whole": True},
                   {"claim": "luma matches", "verdict": 0.95},
                   {"claim": "FFT sign convention matches", "verdict": 0.09}],  # ← located here
           refs=[d["hash"]])
s.mark({"tier": "captain", "id": "opus-5.5"}, kind="commit", ref="<sha>", refs=[f["hash"]])
s.write("../../situations/transcripts/sit-2026-09-29-syzygy-p1.jsonl")
```

### Drawing the dice with no network (in-environment)

When the Moth API is rate-limited or blocked, get `DRAW` records **locally** from MicroMoth-quilt —
a Bell/GHZ circuit + `simulate(..., shots=N)` gives quantum-shaped draws, and its collapse ledger
seals the receipt. Same relation, local provenance: put the collapse-ledger id in `receipt`.

## Verify / replay

```bash
python3 recorder.py                              # self-test: build demo, verify, prove tamper-evidence
python3 recorder.py --verify path/to/situation.jsonl
```

`verify()` replays the chain and catches reorder, edit, drop, and forward/unknown `refs` — the same
tamper-evidence MicroMoth-quilt gives a circuit ledger. If it re-derives every hash, the transcript
is a faithful record of how the manager related its parts.

## Why this is a cell, not a script

It has one job, a receipt, and a reproducible self-test, and it leaves a mark for the next agent —
so it composes. Directors emit a transcript per situation into `situations/transcripts/`; the prose
commit stays as the human time-capsule, the transcript is the machine-readable one beside it. As
transcripts accumulate they become the training set for the *learned dispatch router* and the
*decomposer* of [`../../situations/arch/ML-IN-THE-LOOP.md`](../../situations/arch/ML-IN-THE-LOOP.md) —
the fleet modeling itself as a thing.
