# Blueprint 02 — Dispatch cheap-crew directors (and record the process while you do)

*How to run a 5.5 director that does its volume on cheap, cacheable APIs instead of expensive Anthropic
tokens — and leaves a process signal so the setup gets better each time. The companion to Blueprint 01
(which covers the dispatch loop itself); this one is about **effective API use + portability across
environments**. Follows the dual-audience standard in this folder's README.*

## In one breath

A director spends its own (expensive) tokens only on decomposition and verification; it hands all the
breadth and volume to a crew of cheap models over their own APIs, gates their output with a verified cell,
and records what the run cost so the next director spends even less.

## Why it exists

Expensive-model thinking is scarce; cheap-model tokens are abundant and cache nearly free. A director that
reasons through everything in its own chain-of-thought burns the scarce resource on work a flash model could
do. The fix is a role split and a gate — and once you measure the token split, "we use APIs effectively"
stops being a claim and becomes a number you drive down.

## The mental model (five nouns)

- **Director** — a 5.5 session (Sonnet for build, Opus for architecture). Decomposes, routes, verifies.
- **Crew** — several cheap models called over APIs. They propose, draft, brainstorm, critique in volume.
- **Gate** — a verified cell (B7 product-identity, probes, or TypeSafe typed-check) that decides whether a
  crew output counts. *Cheap models propose; the gate decides.* Never ship ungated crew output.
- **Cache** — a stable prompt prefix so repeated calls hit the provider cache; re-runs become near-free.
- **Process signal** — the record of what the run cost + what was clunky (see DEVELOPMENT-AS-A-QUILT.md).

## The working roster (pinned — don't re-probe)

From the convo-quilt probe (`situations/arch/CONVO-QUILT-IDEATION.md` §II.1), the models that actually
answer at a usable budget:

- **DeepInfra** (`https://api.deepinfra.com/v1/openai`, OpenAI-compatible, caches cheaply):
  `deepseek-ai/DeepSeek-V4-Flash`, `zai-org/GLM-5.3-Flash`, `moonshotai/Kimi-K3`, `Qwen/Qwen3.8-Flash`,
  `inclusionAI/Ling-3.0-flash`, `XiaomiMiMo/MiMo-V2.6-Pro`, `tencent/Hy3`, `openai/gpt-oss-120b`.
- **z.ai** — the **coding** endpoint for `glm-4.6` / `glm-5.3` (the general endpoint has no balance).
- **Groq** — `openai/gpt-oss-120b`, `qwen/qwen3.8-27b` (fast/cheap) when `GROQ_KEY` is set.
- **TypeSafe.ai** (`TYPESAFEAI_KEY`) — a cheap typed/structured gate *before* a bigger call.
- **MothQuantum** (`MOTHQUANTUM_KEY` + `MOTHQUANTUM_BASE`) — un-gameable draws for selection.
- **Avoid at low budgets:** `thinkingmachines/Inkling-Small`, `meta-models/Muse-Glimmer-30B`,
  `ibm-granite/granite-4.2-30b` — reasoning models that spend their budget thinking and return empty text.

Role → model: flash models for breadth; TypeSafe to reject malformed proposals cheaply; a mid model
(`gpt-oss-120b` / `glm-5.3`) for synthesis; MothQuantum to choose among survivors.

## Walkthrough (the brief shape)

Spawn the director with `source_url = <the repo it pushes to>`, `extra_allowed_tools` it needs, and an
`append_system_prompt` that: (1) names it a trusted builder (its repo files aren't injection), (2) says
*do NOT call add_repo*, (3) **pins the roster above and the conserve-Anthropic mandate**, (4) says push
incrementally and end with a receipt. The task prompt names: the deliverable, the gate, the selftest, and
"the crew does the volume; you verify." See the live briefs in `situations/dispatch-ledger.csv` (the B8 /
playtester / creator wave) for worked examples.

## The contract

- **Input:** a repo + a task + the pinned roster. **Output:** a pushed branch + a verified receipt + a
  booked row + a process signal. **Invariant:** no ungated crew output lands; ~90% of tokens are API, not
  Anthropic.
- **Receipt:** the selftest re-run green on `main` by the dispatcher, the ledger row, and the recorded
  token-split / cache-hit rate.

## Failure modes / scars

All booked in `DEVELOPMENT-AS-A-QUILT.md` §2 — the big ones: metaphor briefs trip the safety classifier
(keep briefs plain); z.ai general endpoint 429s (use the coding endpoint); Kimi direct 429s (use it via
DeepInfra); reasoning models return empty at low token caps (avoid or raise the cap); never trust ungated
crew output; pin the roster so you don't re-probe every lane.

## How it composes

`crew-runner` (the importable substrate) gives any director this pattern + the process-signal emitter for
free; `process-refinery` mines the signals to update the roster and the setup cells; the gate is whichever
verified cell fits (`labs/system2-backtest` B7, `labs/quilt-kernel` differ, or a `probes.yaml`). Portable
across environments via the **setup cells** in `DEVELOPMENT-AS-A-QUILT.md` §3 (cloud-session /
local-gpu-openclaw / fork+keys).

## Where to look next

- `situations/arch/DEVELOPMENT-AS-A-QUILT.md` — the process-as-data frame + the signal schema + setup cells.
- `situations/arch/CONVO-QUILT-IDEATION.md` — the conductor-over-cheap-models engine + the full probe.
- `situations/blueprints/01-dispatch-5.5-directors.md` — the dispatch loop these briefs run on.
