# process-refinery — System-2 pointed at the development process

*Spec: [`situations/arch/DEVELOPMENT-AS-A-QUILT.md`](../../situations/arch/DEVELOPMENT-AS-A-QUILT.md)
§2–§4. Output: [`PROCESS-REFINERY-REPORT.md`](../../situations/arch/PROCESS-REFINERY-REPORT.md) +
[`situations/setups/`](../../situations/setups/).*

The labs are what we build; the **development process** is what we build them *with*. This lab
reads the record of how we worked — the dispatch ledger, the typed process signals, the scars — and
answers three questions deterministically:

1. **Which moves work, per environment?** `worked_rate = WORKED / (WORKED + CLUNKY + SCAR)` per
   (pattern, env).
2. **What still hurts most?** The SCAR-heaviest patterns.
3. **Are we getting cheaper?** `anthropic-tokens-per-shipped-receipt`, trended by booking order.

Then it emits **setup cells** — `situations/setups/<pattern>.<env>.md` — for the top WORKED-dominant
patterns: "to run pattern P in env E, do these steps; here is the receipt; here are the known scars."

## Run it

```
python3 labs/process-refinery/process_refinery.py           # summary
python3 labs/process-refinery/process_refinery.py --write   # report + setup cells
python3 labs/process-refinery/process_refinery.py --json    # everything, machine-readable
python3 labs/process-refinery/selftest.py                   # process-refinery selftest: 65 checks, 0 failures
python3 labs/process-refinery/crew_name_patterns.py         # optional, needs DEEPINFRA_KEY
```

Stdlib only, offline, no clock, no randomness: same files in → same `result_hash` out.

## Inputs

| input | role |
|---|---|
| `situations/corpus/process-signals.jsonl` | typed `process_signal` records (crew-runner writes these). Absent today — loader is ready. |
| `DEVELOPMENT-AS-A-QUILT.md` §2 | the 12 seed scars, parsed from the table. The typed fallback dataset and the known-scar library every setup cell draws from. |
| `situations/dispatch-ledger.csv` | every dispatch. Mined by a rule classifier for pattern / outcome / env. |
| `crew_patterns.json` | advisory cheap-crew labels. Reported, never used in a metric. |

## How a ledger row becomes signals (and the honest limits)

The ledger has no outcome column, so `classify_row` infers one from prose:

- **patterns** — regexes for 11 named moves (`dispatch-5.5-director`, `cheap-crew-brief`,
  `harvest-checkout-fetch-head`, `independent-selftest-receipt`, `verified-gate`, `pr-merge-release`,
  `in-process-subagent`, `scheduled-trigger`, `backoff-push`, `architecture-spec`, `ledger-note`).
- **outcome** — SCAR > CLUNKY > WORKED. SCAR: a `SCAR`/`OWNER-BLOCK` tier, BLOCKED/ABANDONED status, or
  prose naming a break (401/403, blocked, clobber, flaky, stall, injection). CLUNKY: PARTIAL or prose
  naming friction (retry, rate-limit, 503, paused, re-dispatch, salvage, conflict). WORKED: DONE/FOLDED
  otherwise. OPEN/PENDING rows are unresolved and excluded. Doc/arch rows can only fail by status
  (writing *about* a scar is not having one), so `architecture-spec` reads optimistic.
- **env** — `cloud-session` unless the row says the openclaw agent itself shipped/ran something
  (`local-gpu-openclaw`) or a run happened on a fork (`fork+keys`). A cloud row that *schedules* GPU
  work stays cloud.

**Limit:** a row's outcome is charged to every pattern it mentions — one 403 marks the director *and*
the harvest. Typed signals (one per move) remove that; until then read rates as directional.

## The token estimate

The ledger books `cost_class` (8 Opus/Fable · 3 Sonnet · 1 dispatcher/Haiku), not tokens. Tokens are
`cost-units × TOKENS_PER_COST_UNIT` (60,000 — one dispatcher turn-burst with its context reads), and
every token figure is labelled ESTIMATE. **Cost-units-per-receipt is exact.** A *shipped receipt* is a
DONE/FOLDED row citing a verifiable artifact (selftest/check count, PR/merge, commit sha); spend counts
every row, so notes and failures are overhead the receipts carry.

## The cheap crew

`crew_name_patterns.py` sends ledger rows in batches of 20 to DeepInfra flash models
(DeepSeek-V4-Flash, Qwen3.8-Flash, GLM-5.3-Flash) at temperature 0 and caches their proposed pattern
names + outcome guesses in `crew_patterns.json`. The report shows how often the crew agrees with the
rule classifier and lists crew-proposed names with no canonical pattern yet — candidates for a human
to adopt. **Cheap models propose; the deterministic classifier decides.**

## Setup cells

Each cell has front matter (`cell: setup`, `pattern`, `env`, `status`, `evidence`, `generated_by`)
and five ordered sections: Inputs, Steps, Receipt, Known scars, Evidence refs.
`parse_setup_cell` validates that shape; the selftest checks every emitted cell. `status: observed`
means the env has recorded runs; `derived-unverified` means the steps are a translation of the
cloud-session steps and the first real run should book a `process_signal` for that env.

## Composes with

- `labs/system2-backtest` (B7) — same idiom one scale up: a deterministic evaluator with a hash.
- `labs/situation-recorder/corpus.py` — the corpus tables this reads beside.
- `crew-runner` (next) — writes `process-signals.jsonl`, which turns every estimate here into a
  measurement.
