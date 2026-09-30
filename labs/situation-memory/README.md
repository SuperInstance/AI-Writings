# situation-memory — recall over the mission corpus

*A `labs/` cell. Python stdlib only, offline, deterministic. Realizes proposal #2 of
[`../../situations/arch/TURBOVEC-FAMILY-STUDY.md`](../../situations/arch/TURBOVEC-FAMILY-STUDY.md).*

## 1. In one breath

Give it a new mission (a transcript or a sentence of task text) and it returns the nearest past
missions from the fleet's recorded corpus, each with a distance and how that mission ended
(DONE / OPEN / SCAR).

## 2. Why it exists

[`situation-recorder`](../situation-recorder/) makes every manager↔crew mission a hash-chained
transcript, so the corpus is **replayable**. Nothing made it **searchable**: to answer "have we done
something like this before, and did it work?" you had to grep `dispatch-ledger.csv` or read
transcripts by hand. System-2 ([ACTIVELEDGER-CELL-GRAPH.md §11](../../situations/arch/ACTIVELEDGER-CELL-GRAPH.md))
studies history to propose alternative networks and needs exactly that lookup. The turbovec family
already had the pattern (vector cells on an fnv1a-64 chain with `find_similar`), but over prompts,
critiques and edges, not missions. This cell joins the two chains.

**What it does not do.** The embedder is a **lexical/structural stand-in**, not a semantic model.
It finds missions that *share words and shape* with the query. It does not find missions that
*mean the same thing in different words* (§6 shows a real miss). The interface is built so a
semantic embedder can replace it without changing callers.

## 3. The mental model

```
transcript (situation-recorder chain, verified)        ── one per mission, GENESIS-rooted by sid
      │  embed (stand-in)
      ▼
{rel: 9-d, budget: 14-d, text: 64-d}                   ── three unit-norm blocks
      │  per-block seeded rotation, 4-bit Lloyd-Max codes   (turbovec-substrate shape)
      ▼
mission cell {sid, transcript_head, outcome, vec, codes, embedder, prev_hash, hash}
      │  appended to the MEMORY chain (fnv1a-64, GENESIS 0x0)
      ▼
MissionIndex.find_similar_missions(query, k) → [{rank, sid, distance, outcome, outcome_raw, …}]
```

Five nouns:

- **Transcript**: the source of truth. It is verified with `recorder.verify` before indexing, and a
  transcript that fails is refused.
- **Embedder**: `MissionEmbedder`, id `situation-memory/structural-lexical-v1`, `semantic = False`.
  - `rel`: histogram of the nine relation verbs (TASK ROUTE DRAFT DRAW FOLD KEEP DROP MARK OUTCOME).
    It encodes the mission's shape, e.g. a harvest-and-fold versus a straight build.
  - `budget`: 14 features listed in `BUDGET_FEATURES`. Situation transcripts do not yet carry the
    ActiveLog budget vector (§8), so most of these are **proxies**: record count, actor count, tier
    mix, and `cost_class` parsed from backfilled ROUTEs. Real `body.budget.{wall_ms,tokens,usd}`
    values are summed when a record has them. In the current corpus none do.
  - `text`: a signed 64-bucket fnv1a-64 hash bag-of-words over the TASK briefs. This is the same
    technique as turbovec's `simple_embed`, so it has the same lexical limit.
- **Mission cell**: one per transcript, chained with `prev_hash`. It anchors `transcript_head`
  (the transcript's last record hash), which links the memory chain to the mission chain. It keeps
  both the rounded float vector and the 4-bit codes, one hex nibble per coordinate.
- **Outcome**: the last OUTCOME record's `result`, kept raw (`outcome_raw`) and classified:
  - `SCAR`: matches scar/blocked/abandon/fail/red/revert/refus/dropped/rejected (checked first).
  - `OPEN`: matches open/pending/partial/awaiting/wip.
  - `DONE`: matches done/verified/validated/shipped/folded/kept/green/landed/merged.
  - `OTHER`: none of the above.
  - `UNLABELED`: the mission has no OUTCOME record.
- **Hit**: a ranked neighbour with its distance and outcome. System-2 needs "near, and it ended as
  a scar", not only "near".

Distance is the weighted root-mean-square of per-block L2 distances. Default weights are text 0.60,
rel 0.25, budget 0.15, applied only over blocks the query has. A plain-string query has only the
`text` block. Rotation preserves L2, so the float mode is exact. `mode="codes"` compares the query
against the cells' **dequantized 4-bit codes** (asymmetric distance). This is the retrieval-on-codes
path the turbovec study (gap #1) found missing. The float vectors are still stored, so no
compression is claimed.

## 4. Walkthrough (real corpus, actual output)

```bash
cd labs/situation-memory
python3 selftest.py
python3 situation_memory.py --like sit-2026-09-29-syzygy-p1-harvest -k 5
```

The corpus is the 7 live transcripts under `situations/transcripts/` plus 151 missions backfilled
from `situations/dispatch-ledger.csv`. If `run_all.sh` has already written the backfill, it is read
from `transcripts/backfill/ledger.jsonl`. Otherwise it is transcoded in memory with no write.
The index head is the same both ways (verified: `0x5e263232f28969ee`).

**Query with a real transcript** (the Syzygy P1 harvest, excluding itself):

```
embedder: situation-memory/structural-lexical-v1  (semantic=False — lexical/structural STAND-IN)
indexed 158 missions (7 live, 151 backfill)  ok: 158 mission cells, chain intact
index head: 0x5e263232f28969ee
find_similar_missions(like=sit-2026-09-29-syzygy-p1-harvest, k=5, mode=float):
  1. d=0.8891  DONE      sit-2026-09-29-syzygy-verifier-harvest       both-cells-independently-verified-shippe
       brief: Harvest + INDEPENDENTLY verify the two Syzygy verifier cells (5.5 wave, builder #3).
  2. d=0.9084  DONE      sit-2026-09-29-tool-pin-harvest              cell-shipped-verified
       brief: Harvest + independently verify the tool-pin-receipts cell built by the Sonnet 5.5 builder.
  3. d=0.9789  OPEN      sit-2026-09-29-hermit-harvest                fix-structurally-verified-awaiting-CI
       brief: Harvest + verify the hermit RED-main fix (5.5 re-dispatch).
  4. d=1.0066  OPEN      ledger-d126                                  OPEN
       brief: Budget returned early (rate_limit status=allowed at 04:34) so the wave started ahead of the 05:18 re
  5. d=1.0093  DONE      ledger-d088                                  DONE
       brief: LANDED all 9 cross-pollination branches (claude/cross-poll-edu) onto their DEFAULT branches, clean (
results_hash: 0x7e6228d5cfafe470
```

The three other harvest-and-verify missions come first. Two ended DONE; one is still OPEN
awaiting CI. Hits 4 and 5 are weak: they share a few words and a tier mix, not the task.

**Query with task text only:**

```bash
python3 situation_memory.py --query "harvest and independently verify a builder cell before booking it" -k 5
```

```
find_similar_missions('harvest and independently verify a builder cell before booking it', k=5, mode=float):
  1. d=0.8603  DONE      sit-2026-09-29-syzygy-p1-harvest             P1-byte-exact-verified
       brief: Harvest + independently verify the Syzygy P1 browser POC before booking it.
  2. d=0.8971  DONE      sit-2026-09-29-tool-pin-harvest              cell-shipped-verified
       brief: Harvest + independently verify the tool-pin-receipts cell built by the Sonnet 5.5 builder.
  3. d=1.0690  DONE      sit-2026-09-29-syzygy-verifier-harvest       both-cells-independently-verified-shippe
       brief: Harvest + INDEPENDENTLY verify the two Syzygy verifier cells (5.5 wave, builder #3).
  4. d=1.1154  DONE      ledger-d023                                  DONE
       brief: Build G18 org-on-quilt (replay-verifiable half): OrgBook books dispatches as receipts, routing = sta
  5. d=1.1154  DONE      ledger-d077                                  DONE
       brief: Docket item: aha-budget UNMARKED-MARK BUG — FIXED + LIVE + verified. The page's renderScore() drew a
results_hash: 0x875705dac710529b
```

With `--mode codes` the top 3 are the same, in the same order (d = 0.8456 / 0.9175 / 1.0791). Hits 4
and 5 swap because they are tied in float mode. Results hash `0x7fecc0f9960e5a96`.

From Python:

```python
import situation_memory as sm
sits, _ = sm.load_corpus()
idx = sm.build_index()
hits = idx.find_similar_missions(sits["sit-2026-09-29-hermit-harvest"], k=3,
                                 exclude=["sit-2026-09-29-hermit-harvest"])
scars = [h for h in idx.find_similar_missions("fix RED main", k=10) if h["outcome"] == "SCAR"]
```

## 5. The contract

- **Inputs:** a query is either a transcript (`list[dict]` of recorder records) or a task-text
  `str`. `k` is an int. `mode` is `"float"` (default) or `"codes"`. `exclude` is a list of sids
  to skip. `weights` is an optional `{block: w}` dict.
- **Output:** a list of up to `k` hits, sorted by `(distance, sid)`. Each hit is
  `{rank, sid, distance, outcome, outcome_raw, provenance, brief, cell}`. `provenance` separates
  live captures from `backfill-from-ledger (reconstructed)` rows, so a consumer can down-weight
  silver data.
- **Invariants:**
  - Only verified transcripts are indexed.
  - The memory chain uses the fleet's fnv1a-64 constants (offset `0xcbf29ce484222325`, prime
    `0x100000001b3`) and is rooted at GENESIS `0x0000000000000000`.
  - Every cell carries `embedder` and `semantic: false`, so a later semantic index cannot be mistaken
    for this one.
  - Vectors are rounded to 6 decimals before hashing.
  - The same corpus and the same query give the same hits and the same `results_hash`.
- **Swap point:** any object with `.id`, `.semantic`, `.blocks` (`{name: dim}`), `.embed(records)`
  and, for text queries, `.embed_text(str)` can be passed as `MissionIndex(embedder=…)` or
  `build_index(embedder=…)`. The selftest plugs in a second embedder to show this works.
- **Receipt:** `python3 selftest.py` → `situation-memory selftest: 28 checks, 0 failures` (as run for
  this commit). It checks:
  - All 158 source chains replay, and the index chain verifies.
  - Editing or dropping a cell is caught.
  - A planted-near mission ranks #1 and ahead of a planted-far one in float and codes modes, for both
    transcript and text queries (far lands at #117–#118 of 159 for transcript queries and #62 for text queries).
  - Same input gives the same head (`0x5e263232f28969ee`) and the same results hash
    (`0x7e6228d5cfafe470`).
  - A tampered transcript is refused.

## 6. Failure modes / scars

- **Paraphrase misses (the main limit).** A query for the same Syzygy P1 mission reworded as
  `"check and confirm the web demo prototype is exact before recording"` returns ledger-d036, d031
  and d061 (cargo-line work) at d ≈ 1.14–1.18. The actual P1 harvest is not in the top 3. It shares
  no hashed tokens with that wording. Fix: a semantic embedder behind the same interface.
- **Weak tail.** Distances around 1.0 or more mean "barely related". The hash bag-of-words has 64
  buckets, so collisions add noise. Treat the tail as a hint, not evidence.
- **Budget block is mostly proxy.** Until transcripts carry ActiveLog budget vectors, "budget
  similarity" means a similar tier mix and size, not a similar cost. The features that are real are
  labelled in `BUDGET_FEATURES`.
- **Keyword outcome classes.** The classifier is a keyword rule. `ledger-d147`'s status is a long
  mixed sentence ("docs complete … failed on the session limit"), and it is classed `SCAR` because
  scar keywords are checked first. `outcome_raw` is always returned so a reader can overrule it.
  The two `jev-usage-folds` situations have no OUTCOME and read `UNLABELED`.
- **Corpus skew.** 151 of 158 missions are reconstructed ledger rows. Each has TASK/ROUTE/MARK/OUTCOME
  shape and no FOLD, so the `rel` block separates live from backfill more than it separates task types.
- **No persistence yet.** The index is rebuilt from transcripts on every run (about 0.2 s at this
  size). The transcripts are the durable store. A persisted `memory.jsonl` would be another derived
  artifact to keep in sync.

## 7. How it composes

- **System-2 (§11 of [ACTIVELEDGER-CELL-GRAPH.md](../../situations/arch/ACTIVELEDGER-CELL-GRAPH.md)).**
  Before the redesigner (B8) proposes an alternative network for a mission, it can ask
  `find_similar_missions(mission, k)` for precedents. SCAR hits name routes that already failed, and
  DONE hits give the sids whose recorded runs [`system2-backtest`](../system2-backtest/) (B7) can
  replay. The results can also narrow the history that [`route-preference`](../route-preference/)
  (B4) reinforces. The §11.2 regime-shift caveat applies: each hit carries its provenance, and live
  sids carry dates.
- **turbovec-substrate.** It uses the same chain algebra (fnv1a-64 constants, GENESIS, `prev_hash`
  linking), a seeded data-oblivious rotation, and 4-bit Lloyd-Max codes. It differs in three ways:
  - Rotation is per block, so a text-only query can be compared on its own block.
  - Centroids are the symmetric N(0,1) Lloyd-Max table.
  - `mode="codes"` actually ranks on the codes.

  The cells are not byte-identical to substrate cells. A shared cell schema would be the next step if
  both are to live on one canon.
- **situation-recorder.** It reads that cell's transcripts and `ledger_to_transcript.transcode`
  unchanged and verifies with its `verify`. Each mission cell's `transcript_head` points back into
  the recorder chain.
- **`near-adapter` (turbovec study proposal #3).** `find_similar_missions` is one more "find near X"
  door. A `/near` client could call it next to i2i-ledger and superinstance-api.

## 8. Where to look next

- [`situations/arch/TURBOVEC-FAMILY-STUDY.md`](../../situations/arch/TURBOVEC-FAMILY-STUDY.md): the
  substrate pattern and its gaps. This cell addresses #1 partially (retrieval can ride codes) and
  still has #2 (lexical, not semantic).
- [`situations/arch/ACTIVELEDGER-CELL-GRAPH.md`](../../situations/arch/ACTIVELEDGER-CELL-GRAPH.md)
  §11: the System-2 loop this recall feeds.
- [`../situation-recorder/`](../situation-recorder/): the transcript format and the corpus this
  indexes (`bash ../situation-recorder/run_all.sh` rebuilds it).
