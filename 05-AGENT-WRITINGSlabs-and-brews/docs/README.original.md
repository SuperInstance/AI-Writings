# labs/ — index and through-line

## 1. In one breath

`labs/` is a shelf of small, dependency-light tools that record how a manager agent and its crew worked, turn those records into training tables and rewards, and check whether cheaper ways of doing the same job really give the same answer.

## 2. Why it exists

The fleet ships repos, but it also produces a second thing that used to be thrown away: the record of *how* the work was decomposed, routed, judged and paid for. Before these labs, that record was prose in commit messages, and "route B is cheaper" or "this translation is lossless" were claims nobody could replay. Each lab here has one job and a selftest, so a claim about the fleet's own operation can be re-derived instead of trusted. Design background lives in `situations/arch/INTER-RELATIONAL-INTELLIGENCE.md` and `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`; this article is the map of the code.

## 3. The mental model

Three nouns carry everything:

- **Situation / transcript.** One manager+crew mission, stored as an append-only JSONL file. Each line is a relation-record (`TASK`, `ROUTE`, `DRAFT`, `DRAW`, `FOLD`, `KEEP`, `DROP`, `MARK`, `OUTCOME`) whose `refs` point at earlier lines, and each line carries an fnv1a-64 hash chained to the previous one. A `FOLD` is the important one: a compound claim, the score of every part, the located weakest part, and the gap between the whole-claim score and the weakest part.
- **Run / ActiveLog.** One execution of a route (e.g. a calculator computing `18 - 0.01`), stored as `cell.tick` and `route.hop` records with a *budget vector* (`wall_ms`, `usd`, `tokens`, `storage_bytes`) and closed by one `ledger.transaction` that names the product and the declared total. A `route.hop` is double-entry: source units credited, destination units debited, with a `price.rate`.
- **Verdict / receipt.** Every lab ends in a number you can re-derive: a selftest count, an fnv1a-64 digest, or a verdict that is a pure function of recorded rows.

**The important thing about the dependency graph is that it has two strands, joined by convention, not by code.** They share the hash idiom (fnv1a-64 over canonical JSON, which `activeledger` copied from `situation-recorder`) and the receipt habit. Neither strand imports the other. The end-to-end order below is a reading order, not a data pipe.

```
Strand A — what the crew did (transcripts)
  situation-recorder/recorder.py     writes hash-chained transcripts
        │  (ledger_to_transcript.py backfills old dispatch-ledger rows into the same format)
        ▼
  situation-recorder/corpus.py       verifies every chain, writes situations/corpus/{decompositions,routes,judgments}.jsonl
        ▼
  situation-recorder/baseline_decompose.py   the base rate a learned model must beat
  rubric-forge/forge.py              reads the same transcripts' FOLD records → one dense reward in [0,1] per fold
                                     (imports recorder's hash helpers; feeds "B4" route-preference, which is not built here)

Strand B — what a route cost (ActiveLog)
  activeledger/activeledger.py       the shared emitter: envelope, budget vector, double-entry hops, content hash
        ▼
  examples/*-quilt                   five small quilts, each with a cheap route and a full route; each books runs
        │                            (calculator-quilt uses an inline stand-in emitter; see scars)
        ├──▶ unit-translation-audit/audit.py   "B2": replays every route.hop, says EXACT / WITHIN_TOL / LOSSY
        └──▶ system2-backtest/backtest.py      "B7": gates product identity, then prices cheap vs full route
```

In words: `corpus.py`, `baseline_decompose.py` and `rubric-forge` all read the *transcripts*. `unit-translation-audit` and `system2-backtest` both import `activeledger` and both reach into `labs/examples/` for their workloads. `examples/run_all.py` sits over the five quilts and runs their selftests. The Node labs (`jev-fold` → `weakest-claim` → `qd-arena`, plus `quantum-fx`) are a third, separate chain that produces the `FOLD` verdicts and dice that Strand A records.

Where things meet: a route chosen in Strand B is a `ROUTE` record's subject in Strand A, and the reward from `rubric-forge` is meant to rank routes that `system2-backtest` has certified as product-identical. That last join (B4) is described in the design docs and consumed by no code in `labs/` today.

## 4. Walkthrough

The shortest useful look at the collection is to list the shelf and confirm the two headline checks. Full runs with pasted output are in [`using-the-labs.md`](using-the-labs.md); this is the index.

| lab | one job | language | selftest / check |
|---|---|---|---|
| `situation-recorder` | capture manager↔crew missions as hash-chained transcripts; build corpus tables and a base rate | Python | `python3 recorder.py`; `bash run_all.sh` |
| `activeledger` | ActiveLog v1 emitter, budget vector, double-entry hops, OTel projection (B1) | Python | 28 checks |
| `examples/` (5 quilts) | small use-cases with a cheap and a full route that reach the same product | Python | 12 + 21 + 14 + 18 + 17 checks; `examples/run_all.py` |
| `rubric-forge` | turn a `FOLD` into a weighted rubric and a dense scalar reward | Python | 1091 checks |
| `unit-translation-audit` | round-trip audit of every `route.hop` (B2) | Python | 34 checks |
| `system2-backtest` | price two recorded routes only if their product is identical (B7) | Python | 38 checks |
| `tool-pin-receipts` | hash-pin tool/MCP manifests, flag drift and description injection | Python | `python3 pin.py --self-test` |
| `dominated-novelty-search` | threshold-free quality-diversity selection, drop-in for `qd-arena`'s grid | Python | see its README |
| `jev-fold` | split a claim, score each part with JEV, return the weakest | Node | `node --test fold.test.mjs` |
| `weakest-claim` | fold + a dice-drawn adversary, to audit a guarantee | Node | `node --test audit.test.mjs` |
| `qd-arena` | MAP-Elites over live generator models | Node | `node --test qd.test.mjs` |
| `quantum-fx` | one client for five Moth quantum engines | Node | `node --test qfx.test.mjs` |

The counts for the Python labs in the middle of the table were re-run for this article (see `using-the-labs.md` §4). I did not run the Node labs or `tool-pin-receipts`/`dominated-novelty-search` selftests when writing it, so their rows only name the command their README gives. The Node labs that score with JEV or draw with Moth need network keys (`TYPESAFEAI_KEY`, `MOTHQUANTUM_*`); `jev-fold` and `weakest-claim` fall back to recorded fixtures when those are missing.

Functional use, per capability: the recorder gives you replayable evidence of who routed what to whom; the corpus tables give you rows to train or evaluate a decomposer or router on; `rubric-forge` gives a graded label where a single yes/no would hide which part failed; the audit tells you which unit conversions lose information; the backtest tells you, per workload, which route to prefer and when.

## 5. The contract

- **Inputs.** Strand A reads `situations/transcripts/**/*.jsonl`. Strand B reads ActiveLog runs emitted by the quilts (in memory, not from files on disk).
- **Outputs.** `situations/corpus/{decompositions,routes,judgments}.jsonl`; a reward table from `forge.py`; an audit record per hop plus an `audit_digest`; a `verdict` and `verdict_hash` per backtested pair.
- **Invariants.** Every record is content-hashed with fnv1a-64 over canonical JSON. Transcript chains must verify or `corpus.py` stops. Backtests refuse to show budgets when products differ. Audits and verdicts are pure functions of their inputs, so re-running yields the same digest.
- **Receipt.** All of it is checked by running: `bash labs/situation-recorder/run_all.sh` (expects "all 154 chains verified"), `python3 labs/examples/run_all.py` (5/5 green), and each Python lab's `selftest.py`.

## 6. Failure modes / scars

- **The two strands are not wired together.** Nothing feeds `activeledger` runs into `corpus.py`, and nothing feeds `rubric-forge` rewards into `system2-backtest`. If you read the pipeline order as a data flow you will look for glue that does not exist.
- **"5/5 on the shared ledger" is a weaker statement than it sounds.** `examples/run_all.py` decides that an example is on the shared ledger by searching its `.py` files for the string `activeledger`. `calculator-quilt` matches only because a comment mentions it; its emitter is an inline stand-in (`examples/calculator-quilt/calc_quilt.py`, "ActiveLog v1 emitter (stand-in…)"). `unit-translation-audit` traces the calculator's 5 lossy hops to that stand-in never running the shared emit gate.
- **The base rate is a scaffold.** The lexical baseline scores 0.14 top-1 on 7 folds against a 0.25 random rate. N=7 is far too few to gate CI on, and the script says so itself.
- **Self-consistency is not correctness.** The audit checks a hop against its own recorded price; the backtest's product gate is only as fine as the `ledger.transaction` fields. Both READMEs book this.
- **Simulated numbers.** Budgets in the quilts are a deterministic cost model, not measurements. The storage-bytes gaps in the backtest (16× to 78× between cheap and full routes) are outputs of that model, not hardware measurements.
- **Backfilled transcripts are reconstructed.** 147 of the 154 situations come from `ledger_to_transcript.py` and are stamped `backfill-from-ledger (reconstructed)`; only 7 carry real `FOLD` records.

## 7. How it composes

Two composition rules keep the shelf coherent. (1) Share the hash idiom, not the code: `activeledger`, `rubric-forge`, `tool-pin-receipts` and `situation-recorder` all use the same fnv1a-64 canonical-JSON hash, so a digest from one can be booked as a `MARK` in another. (2) Build on, don't reimplement: `weakest-claim` imports `jev-fold`, `qd-arena` imports `weakest-claim`, `unit-translation-audit` and `system2-backtest` import `activeledger`. To add a lab, give it one job, a `selftest.py`, and an entry in `labs/README.md`; to add a quilt, emit through `labs/activeledger` (not a stand-in) so the audit's emit gate applies.

## 8. Where to look next

- [`using-the-labs.md`](using-the-labs.md): the same loop run end to end, with real output.
- [`../README.md`](../README.md): the per-lab table, including the labs this article only names.
- `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`: the design behind Strand B (§8 envelope, §11 System-2, §13 example collection). It is a design doc; several items it proposes (B3, B4, B8) are not implemented in `labs/`.
