# Development as a quilt — refining the process itself, not just the output

*2026-10-01. Casey's standing lens, made load-bearing: "part of what we are doing is learning from the
situational development engineering that works and that is clunky, and refining the process as a system on
a quilt for reusable setups in different development environments." The labs are the visible output; the
real product is **the development process itself, captured as data and distilled into portable setups.**
This doc defines the capture format (so clunk becomes queryable) and the setup-cell idea (so a working
pattern runs in someone else's environment unchanged). Voice: inform, honest; keep every addition minimal.*

---

## 1. The thesis in one breath

Every dispatch — spawn a director, hand it a cheap-crew brief, harvest its branch, book a row — is itself a
**cell with a receipt**. The dispatch-ledger is already that chain (161 rows and counting). So the same
machinery we point at *code* (capture → gate → price → refine) we can point at *development*: record which
patterns worked and which were clunky, mine the record, and promote the winners into reusable setups. The
quilt gets better at **being developed on**, not just bigger.

## 2. The process signal — making clunk into data

Prose in a ledger note ("MCP flapped again") is not minable. A typed record is. Alongside its mission
chain, a run emits one or more **process signals**:

```
process_signal {
  phase:    PLAN | DISPATCH | BUILD | HARVEST | BOOK | PUSH   # where in the loop
  pattern:  str      # the named move, e.g. "cheap-crew-brief", "checkout FETCH_HEAD -- <dir>",
                     #   "backoff-push", "probe-model-roster", "metaphor-brief"
  outcome:  WORKED | CLUNKY | SCAR     # SCAR = it broke and cost real time
  cost:     { wall_s?, anthropic_tokens?, api_usd?, retries? }   # what it cost (budget vector, process-scale)
  env:      str      # "cloud-session" | "local-gpu-openclaw" | "fork+keys" | ...
  fix:      str      # what resolved it (empty if WORKED)
  ref:      str      # dispatch-ledger d-row or session id
}
```

This is the ActiveLog budget vector applied one scale up — the "budget" of a *development move*. The
recorder (`labs/situation-recorder`) gains an optional emitter for it; `crew-runner` (next wave) writes
them automatically as it runs, so new runs deposit process-data without anyone remembering to.

### The scars already observed this session (the seed corpus)

Booked here so the first `process-refinery` run has real data, not a blank table:

| pattern | outcome | fix |
|---|---|---|
| metaphor-heavy director brief | SCAR | plain technical briefs; keep the poetry in docs, not runtime prompts (`[reasoning_extraction]` false-positive) |
| `default` perm mode + no `extra_allowed_tools` | SCAR | pass the tool list; a cloud director can't answer a permission prompt |
| director calls `add_repo` | CLUNKY | tell it in the brief: don't; everything is in your source repo |
| cross-repo push (403) | SCAR | spawn the director with `source_url = the target repo` |
| harvest via full merge | CLUNKY | `git checkout FETCH_HEAD -- <dir>` — bring only the files you want |
| branch's older README clobbers a fresh rewrite on harvest | SCAR | restore from HEAD, re-add rows; never blind-checkout a shared index file |
| MCP/GitHub 503 + container restarts | CLUNKY | commit locally, then backoff-push; work is safe once committed |
| GitHub push-auth expiry mid-session | SCAR | reconnect at claude.ai/connect-github; a *fresh* session picks up new keys |
| 5h / 7d usage caps stalling child lanes | CLUNKY | lanes push incrementally; harvest the branch even when the session's last turn errored |
| re-probing the cheap-model roster each lane | CLUNKY | pin the working set once (CONVO-QUILT-IDEATION.md §II.1); hand it to every brief |
| flaky selftest (unseeded draw) | SCAR | pin the seed; prove N consecutive green before trusting |
| trusting a cheap model's output ungated | SCAR | cheap models propose, verified cells (B7/probes/TypeSafe) decide |

Each row is a `process_signal` in prose; the schema above is how the next ones get recorded so they can be
counted, not just remembered.

## 3. Setup cells — a working pattern that travels

A **setup cell** encodes *"to run pattern P in environment E, do these exact steps"* — parameterized by
environment, so the same effective pattern runs in different hands:

- `env: cloud-session` — our CCR directors (`create_session` + cheap-crew brief + git harvest).
- `env: local-gpu-openclaw` — Casey's workstation agent (same crew doctrine, local git, its own keys).
- `env: fork+keys` — a stranger who forked a repo and has only API keys (no CCR): run the cheap-crew
  directly from a script; `crew-runner` is importable standalone for exactly this.

The contract a setup cell carries: **inputs** (repo, task, model roster, env), **the steps**, **the
receipt** (a selftest/row that proves it ran), and **the known scars for that env** (from §2). A setup cell
is itself a patch-in-an-expert — an expert on *running this kind of lane here* (see the patchwork-experts
`patch-as-cell` frame: a setup cell is a cell with a gate + budget + env tag).

## 4. The two cells that make this live (next wave)

- **`crew-runner`** — the cheap-crew substrate every director imports, **and the sensor**: it writes
  `process_signal`s (token split cheap-vs-Anthropic, cache-hit rate, retries, outcome) for every lane. Build
  once; every future lane self-records.
- **`process-refinery`** — System-2 aimed at development: reads the dispatch-ledger + the process-signal
  corpus + §2's scars, reports which patterns are WORKED-dominant vs CLUNKY/SCAR-dominant per env, and emits
  updated **setup cells**. The honest metric is not "how many dispatches" but **worked-rate per pattern per
  env** and **Anthropic-tokens-per-shipped-receipt** (the thing we're driving down).

## 5. What this is not

Not a process-management framework, not a dashboard for its own sake, not ceremony. One typed record, a
handful of setup cells, and a refinery that reads them. The discipline is the same as everywhere in the
quilt: a cell has one job, a receipt, and a mark; a process-signal is just the mark a *development move*
leaves. We keep only the pins a refinery provably uses, and we learn which from where the process breaks —
not from predicting it.

## Where to look next

- `situations/blueprints/02-cheap-crew-dispatch.md` — the human-readable, env-portable how-to.
- `situations/blueprints/01-dispatch-5.5-directors.md` — the original dispatch loop + scars (prose form).
- `situations/arch/CONVO-QUILT-IDEATION.md` §II.1 — the pinned working model roster.
- `labs/situation-recorder/` — where the process-signal emitter attaches; `labs/quilt-kernel` — the cell
  contract a setup cell instantiates.
