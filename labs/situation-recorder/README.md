# situation-recorder — the manager↔crew system, saved as a decomposable corpus

*A `labs/` cell. Zero dependencies (Python stdlib). Reusable by any captain/director.*

The fleet's real product is not only the repos a crew ships — it is the **recorded inputs and
outputs of the manager↔crew system**, saved so a future model can learn the one skill this fleet
runs on: take a compound thing apart, locate where the value/truth lives, recombine. This cell is
that capture unit. Design: [`../../situations/arch/INTER-RELATIONAL-INTELLIGENCE.md`](../../situations/arch/INTER-RELATIONAL-INTELLIGENCE.md).

## What it does

Records one **situation** (one manager+crew mission) as an append-only JSONL **receipt ledger** —
the same idiom [`SuperInstance/MicroMoth-quilt`](https://github.com/SuperInstance/MicroMoth-quilt)
uses for quantum circuits: every line a cell, **hash-chained**, replayable. Each line is one
**relation-record** whose `refs` are the graph edges — so a transcript is a *graph of how the parts
related*, not a flat log.

## The chain rule: `witness-chain/1`

The chain rule was upgraded. The old one is **`witness-chain/0`** and is still READ and VERIFIED —
a log that cannot verify its own history is a lie about the past. New records are
**`witness-chain/1`**.

```
v0:  hash = fnv1a64(json.dumps({prev, **envelope}, sort_keys=True, separators=(",", ":")))
v1:  leaf(i) = SHA256(0x00 || JCS(record_i))          RFC 6962 2.1 domain separation
     hash(i) = SHA256(0x01 || hash(i-1) || leaf(i))    RFC 6962 2.1
```

**Why the change, in three parts. The third is the one that matters.**

1. **RFC 8785 (JCS)** instead of the house convention. The v0 canonicalisation was
   `json.dumps(sort_keys=True)`, reimplemented by hand in every port. It is not a standard, and it
   diverges from JCS in three measured ways: `1.0` -> `"1.0"` (JCS: `"1"`); keys are sorted by
   **code point** in Python and by **UTF-16 code unit** in JCS, so they disagree for any key above
   U+FFFF against one below; and Python's `ensure_ascii` escapes non-ASCII where JCS does not.
   RFC 8785 is a `MUST` in A2A v1.0 §8.4.1, so this is interoperability, not pedantry.

2. **Domain separation** — a leaf hashes with a `0x00` prefix and a node with `0x01`, so the two
   kinds of thing cannot be confused.

3. **THE OLD RULE HAD NO TAMPER-EVIDENCE AT ALL.** A hash chain is *self-consistent*, and
   self-consistency is not tamper-evidence: rewrite a record, re-chain it, and the chain verifies
   perfectly, because the attacker recomputed it. v0 also used **FNV-1a-64**, which is 64 bits and
   not collision-resistant, so an attacker rewriting a chain does not need to collide anything —
   they just recompute.

   **Tamper-evidence needs an anchor OUTSIDE the log.** `sign_head()` / `verify_head()` implement
   the standard shape (RFC 6962 / Trillian's `LogWitness`): a **signed tree head**, under a key the
   log writer does not hold, published somewhere the writer does not control.

   **Truncation is the same defect, and it is cheaper to exploit.** Delete the last 50 records of a
   121-record `witness-chain/1` transcript and the remaining 71 verify cleanly — `verify()` returns
   ok and the head simply moves. *A truncated chain is a shorter valid chain.* No rewrite, no
   re-hashing, no competence required. So the **publication** half is not a detail of the anchor
   design, it is the whole of it: a signature over a head stored inside the log it anchors is a
   signature the writer can refresh for free.

   **The key must not be the writer's key**, or the writer can re-sign and there is no anchor.
   HMAC-SHA256 is used because it is in both the Python and the JavaScript standard libraries, but
   **it is a stand-in, not a signature** — it is symmetric, so it proves "someone with the key
   wrote it", not "who". Ed25519 is the production answer.

`recorder.py --out` demonstrates all of it, and the self-test asserts both halves:

```
RE-CHAINED rewrite verifies?           True   <- a chain alone CANNOT tell
RE-CHAINED rewrite caught by the signed head? True
```

The forgery in that demo is a **fixpoint**: it re-chains *and* re-points every `refs` entry that
names a changed hash, because re-pointing a ref changes a record's body, which changes its hash,
which cascades. A forgery that only re-chains is caught by the `refs` check — that is a second
layer of detection, and worth knowing about, but it is only as good as the attacker's care. The
signed head does not depend on the attacker's competence.

### Migration

This changes every hash, so it is a **format change**. `verify()` accepts both versions and
**rejects a chain that MIXES them** — the version is a field inside the record, so it is inside
the hashed bytes and cannot be stripped without breaking the chain. To migrate: **start a new
transcript and name the previous head in it.** Do not rewrite history.

### Cross-implementation byte identity

`SuperInstance/witness-spec` holds the conformance vectors and the JavaScript reference. This
implementation reproduces **every canonical form, leaf hash, chain hash, the head, and the
signature** from them, byte for byte. Three implementations, one chain rule.

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

When the Moth API is rate-limited or blocked, get `DRAW` records **locally** with
[`draw_local.py`](draw_local.py) — it builds a MicroMoth-quilt circuit, seals the draw as a
collapse-ledger receipt, self-verifies the chain, and returns `(value, receipt)` you pass straight
to `Situation.draw()`:

```bash
MICROMOTH_QUILT=/path/to/MicroMoth-quilt python3 draw_local.py   # self-demo: reproducible, fair, sealed
```

```python
from draw_local import draw_int
idx, receipt = draw_int(0, 4, seed=42)          # un-steerable-by-the-crew, reproducible
s.draw({"tier": "dice", "id": "micromoth-quilt/local"}, request="...", value=idx, receipt=receipt)
```

**Honest provenance (keeps the corpus clean):** MicroMoth-quilt is a *simulator* — the draw is
quantum-structured and replayable with an attestable receipt (its cell ids re-derive; nothing is
signed and no head is published out of band), but it is **not** a hardware QRNG
and carries no Bell-S. So it's the *throttled-case* dice; reach for the real Moth QRNG when you need
hardware un-gameability, and never launder one as the other. See the first real transcript
[`../../situations/transcripts/sit-2026-09-29-capture-path.jsonl`](../../situations/transcripts/sit-2026-09-29-capture-path.jsonl),
where a `FOLD` located exactly this caveat as the weakest leaf.

## Verify / replay

```bash
python3 recorder.py                              # self-test: build demo, verify, show the limit
python3 recorder.py --verify path/to/situation.jsonl
```

`verify()` replays the chain and catches reorder, edit, drop, and forward/unknown `refs` — the same
**re-derivation** MicroMoth-quilt gives a circuit ledger. If it re-derives every hash, the transcript
is a faithful record of how the manager related its parts, and the transcript is **attestable**: an
edit is expensive and a naive edit is named.

It is **not tamper-evident**, and the difference is not a wording preference. Re-derivation assumes
the tamperer does not recompute: re-chain an edit and the chain verifies perfectly; truncate the
tail and the remainder still verifies. Both need an external anchor, and this repo does not publish
one. The word for what holds here is *attestable*; see the house definition in
[`SuperInstance/witness-spec`](https://github.com/SuperInstance/witness-spec) `SPEC.md`.

## Why this is a cell, not a script

It has one job, a receipt, and a reproducible self-test, and it leaves a mark for the next agent —
so it composes. Directors emit a transcript per situation into `situations/transcripts/`; the prose
commit stays as the human time-capsule, the transcript is the machine-readable one beside it. As
transcripts accumulate they become the training set for the *learned dispatch router* and the
*decomposer* of [`../../situations/arch/ML-IN-THE-LOOP.md`](../../situations/arch/ML-IN-THE-LOOP.md) —
the fleet modeling itself as a thing.
