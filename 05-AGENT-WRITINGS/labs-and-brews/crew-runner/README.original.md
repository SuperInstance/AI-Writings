# crew-runner — a cheap-model crew you can import, and a sensor that records how development went

## In one breath

A small Python module: a director calls `crew.ask(...)` to fan a prompt out to several cheap models,
keeps only the answers a verified gate accepts, and every call leaves behind a typed, hash-chained record
of its cost and outcome.

## Why it exists

Without this module, every director hand-rolled its own cheap-model calls: re-probing the roster, keeping
crew output it never checked, and recording cost as prose ("MCP flapped again") that nothing can count.
Blueprint 02 (`situations/blueprints/02-cheap-crew-dispatch.md`) sets the doctrine: cheap models propose,
the gate decides, cache the prefix, record the run. `situations/arch/DEVELOPMENT-AS-A-QUILT.md` defines the
record format. This module implements both once, so any director or a stranger's script gets them from a
single `import`.

## The mental model

```
director ──ask(role, prompt)──▶ [stable prefix | branch context | task] ──▶ model A, B, C   (parallel)
                                        │ cache hit? return stored answer, 0 calls
outputs ──gate(outputs, gate_fn)──▶ kept (becomes branch context)  /  rejected (never does)
every ask + gate ──▶ process_signal ──▶ situations/corpus/process-signals.jsonl   (fnv1a-64 chain)
```

- **Crew**: `provider:model` strings. Defaults to the first three pinned DeepInfra flash models when
  `DEEPINFRA_KEY` is set. Without a key it falls back to `stub:a/b/c`, a deterministic offline model, plus
  `stub:broken` (malformed output) and `stub:down` (always fails) for tests.
- **Gate**: a function `text -> bool | (bool, reason)`, for example `json_gate("idea", "metric")`. Only
  accepted text is added to the branch's context.
- **Cache**: keyed on `fnv1a64(canon([model, messages, max_tokens]))` and persisted with `cache_path=`. The
  messages always put the stable prefix first, so a DeepInfra re-run also hits the provider's prefix cache.
- **Branch / checkpoint / rewind**: the convo-quilt idiom. A branch's kept history is the context for its
  next ask. `rewind` truncates history, `branch` forks it, and entry ids are never reused. The signal chain
  is append-only: it never rewinds.
- **Process signal**: `{phase, pattern, outcome, cost, env, fix, ref}` from DEVELOPMENT-AS-A-QUILT.md §2,
  plus `seq`, `ts` and `hash = fnv1a64(canon({prev, **record}))`. This is the same chain rule as
  situation-recorder, starting from GENESIS `0x0000000000000000`.

## Walkthrough

```python
import sys; sys.path.insert(0, "labs/crew-runner")
from crew_runner import CrewRunner, json_gate

crew = CrewRunner(ref="d163", env="cloud-session")        # DeepInfra if keyed, else stubs
crew.checkpoint("start")
outs = crew.ask("brainstorm", 'One idea. Reply ONLY {"idea": ..., "metric": ...}')
kept, rejected = crew.gate(outs, json_gate("idea", "metric"))
crew.rewind("start")                                      # try again from the same point
crew.signal("HARVEST", "checkout FETCH_HEAD -- <dir>", "WORKED", {"wall_s": 4})
print(crew.split())       # measured cheap tokens vs estimated Anthropic tokens, cache-hit rate, USD
```

```
$ python3 labs/crew-runner/selftest.py
crew-runner selftest: 33 checks, 0 failures
$ python3 labs/crew-runner/crew_runner.py --live          # 2026-10-03, 3 DeepInfra models
gate: 3 kept, 0 rejected []
repeat ask: 3/3 served from cache
  provider cache deepinfra:deepseek-ai/DeepSeek-V4-Flash  cached 1536/1552 prompt tokens, usd 0.000145 -> 0.0000348
  provider cache deepinfra:zai-org/GLM-5.3-Flash          cached 0/1509 prompt tokens, usd 0.000124 -> 0.000125
  provider cache deepinfra:Qwen/Qwen3.8-Flash             cached 1024/1597 prompt tokens, usd 0.000239 -> 0.000216
split: {"cheap_tokens": 9979, "cheap_cached": 2560, "anthropic_tokens_est": 542, "cheap_share": 0.9485,
        "cache_hit_rate": 0.3333, "calls": 6, "retries": 0, "failures": 0, "api_usd": 0.000884}
ok: 22 signals, chain intact
```

Other commands: `--verify [path]` re-verifies a chain, and `--seed-scars` books §2's 12 scars (it is
idempotent).

## The contract

- **Input:** models, a prompt, and a gate. **Output:** per-model `{model, text, tokens{in,out,cached},
  usd, cached, attempts, error?}`, then the `(kept, rejected)` lists from `gate`.
- **Invariants:**
  - Rejected or failed output never enters branch context.
  - A cache hit makes zero calls.
  - Failures and retries are returned and recorded, never hidden.
  - The signal file is an unbroken chain: an edited, reordered or dropped record fails `verify_signals`.
  - `phase` must be one of PLAN, DISPATCH, BUILD, HARVEST, BOOK or PUSH.
  - `outcome` must be one of WORKED, CLUNKY or SCAR.
- **Auto-signals:**
  - `ask` writes `crew.ask:<role>` with `wall_s`, cheap tokens in/out/cached, cache hits per lookup,
    retries, `anthropic_tokens_est`, and `api_usd` when the provider reports it. Outcome is SCAR if
    every model failed, CLUNKY if some failed or retried, else WORKED.
  - `gate` writes `crew.gate` with the accepted and rejected counts. Outcome is SCAR if nothing was
    accepted, CLUNKY if some output was rejected, else WORKED. The rejection reasons go in `fix`.
- **Receipt:** `selftest.py` runs offline with stubs, using temp files only. It proves fan-out, gate
  rejection, a cache repeat without a second call, retry and failure accounting, rewind and branch,
  signal write plus chain verification and tamper detection, and the 12-scar seed. It also verifies the
  repo's `process-signals.jsonl` chain.

## Failure modes / scars

- **The Anthropic figure is an estimate.** It is chars/4 of the prompt the director wrote plus the
  answers it reads. The director's real usage is not visible from inside the module. Cheap-model tokens
  and USD are measured from provider `usage`.
- **Provider prefix caching only starts above about 1,024 prompt tokens** (measured). GLM-5.3-Flash
  didn't cache at all. The first live smoke used a short prefix and recorded 0 cached tokens; the long
  prefix fixed that.
- **Gated output changes the context.** Kept text joins the branch history, so asking the same prompt
  again is a different request and a cache miss. To repeat a request exactly, `rewind` first. The first
  live smoke missed this (0/3 cache hits). Its signals are still in the chain: seq 12–16.
- **Reasoning models can return empty text at low token caps.** The module retries once with three times
  the cap. If that still fails, the record says so.
- **`process-signals.jsonl` is a source file, not a derived table.** `situations/corpus/.gitignore` has an
  exception for it, so it stays tracked.
- **The 12 seeded scars have `cost: {}`.** Their costs were never measured, and `provenance` marks them
  as seeded from prose.

## How it composes

- **Reuses:**
  - `labs/convo-quilt/providers.py` for endpoints and keys.
  - `labs/quilt-kernel` for `fnv1a64` and `canon`.
  - situation-recorder's chain rule.
  - convo-quilt's snapshot/rewind idiom.
- **Gates:** any verified cell fits as the `gate_fn`, such as the B7 product-identity check, a
  quilt-kernel `diff`, a probes file, or a TypeSafe JEV call.
- **Feeds:** `process-refinery` (next wave) reads `process-signals.jsonl` to compute the worked-rate per
  pattern per env and the Anthropic tokens per shipped receipt.

## Where to look next

- `situations/arch/DEVELOPMENT-AS-A-QUILT.md`: the signal schema, setup cells and seed scars.
- `situations/blueprints/02-cheap-crew-dispatch.md`: the doctrine and the pinned roster.
- `labs/convo-quilt/`: the conductor over a quilt of cheap models, where rewind and branch come from.
