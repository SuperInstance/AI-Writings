# Civ Orchestrator — RUN REPORT session 137 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `7ddd3f0` (session 136 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe → HTTP 422
`{"type":"too_short"}` = token accepted).
**Run status:** all verification checks PASS (18/18).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `git clone` into `/workspace/repos/...` dies on `.git/description`; `cp` exits 1 with `Disk quota exceeded` and leaves 0-byte files that still appear in `ls` |
| Bridge | `ln -sfn /tmp/AI-Writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:12601` on both sides, `-ef` confirms |
| Clone target | `/tmp/AI-Writings` (full clone, `--depth 50`); `/tmp` is exempt from the NAS quota |
| `gh` | not installed (18th session) |
| Tool timeout | 30 s < run ~55 s → launched detached, polled |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all sandbox secrets; real endpoint returns 401 (endpoint healthy ⇒ credential gap, not an outage) |
| JEV | live — 422 on an empty `questions` dict = token accepted; `/v1/models` → 200 |
| Mock teardown | killed **both** pids (timeout wrapper 262 + server 264); `curl` exit 7 = port closed; 0 tracebacks in the log |

## Mock rebuild

`/tmp` was wiped again ⇒ the mock was rebuilt from the RUNBOOK. **Both** historical bugs had to be
re-applied, and both are load-bearing:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — without it the bridge 500s on `i>=4`
  **while the socket stays open**, so a port/200 probe looks healthy.
- session-118 md5-of-whole-message seeding `md5(msg)[:8]` — without it all 8 civs emit
  identical text (`"YouAreA"` is the first 8 alnum chars of *every* cultural prompt) and every
  competition result is void.

**Pre-flight probe (live mock, exact long cultural prompt):** 8 civs → **8/8 distinct seeds**,
**8/8 distinct previews**, HTTP 200, `[mock-zai seed=…]` prefix present, **0 tracebacks** in
`/tmp/mock_zai.log`. The pre-flight probe is what keeps a broken mock from reaching the ledger.

## Verification (18/18 PASS)

- per-civ `simulations.jsonl` Δ = **+10** × 8 (5 sim-phase + 5 competition-phase) = **80 new rows**
  (engineer 806→816, formal 837→847, grounded 852→862, mythic 809→819, poetic 831→841,
  precise 801→811, therapist 804→814, whimsical 864→874)
- `meta_log.jsonl` Δ = **+5** (418 → 423)
- `Winner:` lines = **5**
- **80/80** rows carry the `[mock-zai` prefix, `provider` = `{zai}` (all 80)
- **0** rows with a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple
- **40 distinct seeds across the 80 new rows** = 8 civs × 5 prompts ⇒ seed is a clean 1:1
  function of `(civ, prompt)`; **0** `(civ, prompt)` combos carry >1 seed
- **5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews** — the **twelfth
  consecutive clean measurement** (118, 120–123, 125, 131–134, 136)
- `avg_score` over the 80 new rows: min 0.7200, max 1.7267, mean 1.0887, **68/80 distinct values**
- `leaderboard.json` rewritten at 22:12:13Z
- registry still 8 civs, all `generation=1`, no extinction/birth (single batch, not `--loop`)

### NEW (this session) — the *per-prompt* distinctness slice must be the LAST 8 rows, not `rows[-8:]` per prompt

First cut of the mock-integrity check reported **3–6 of 8 distinct previews per prompt** and looked
like a degraded mock. It was the *analysis* that was wrong, not the mock. The 80 new rows are
**two interleaved phases**: 40 sim-phase rows (each civ draws a *random* prompt per sim) and 40
competition-phase rows (each civ answers each of the 5 prompts exactly once). Grouping by prompt
and taking `rows[-8:]` mixes the two phases, so a prompt's last 8 rows can contain the *same* civ
twice and miss others entirely.

The correct slice is **the last 8 rows of each prompt group, taken after sorting the whole 80-row
set by `ts`** — the competition phase is the later block. That yields **8/8 on all 5 prompts**.

Two independent invariants confirm the mock was clean all along:
- **40 distinct seeds / 80 rows** is the *expected* value (8 civs × 5 prompts), and **every**
  `(civ, prompt)` combo maps to exactly one seed (0 combos with >1 seed).
- the sim-phase rows repeat seeds *across civs* on the same prompt (only 5 distinct seeds per
  prompt in the sim phase) because a *cultural* prompt — civ culture + prompt text — is what gets
  hashed, and the sim phase reuses prompts.

**Durable rule: use the run-wide count (40 seeds / 80 rows) and the per-`(civ,prompt)` 1:1 check
as the integrity signal. A per-prompt preview-distinctness number below 8/8 is a *slicing* artifact
until you have confirmed the phase split.** A degenerate mock (session-117, first-8-alnum seeding)
would instead show 1 seed for all 8 civs on the *same* prompt — check the *seed*, never the preview.

## Results

### Chooser vs `avg_score` argmax: 1/5 (20 %)

`civ-precise` was argmax in 1/5 but won **4/5**. All 4 disagreements go the **same direction** —
the chooser picked a *marginally lower*-scoring candidate:

| prompt | winner | argmax | delta |
|---|---|---|---|
| what a cell is | `civ-precise` 1.473 | `civ-precise` 1.473 | match |
| bookkeeper's role | `civ-precise` 1.253 | `civ-poetic` 1.420 | **−0.167** |
| witness log | `civ-mythic` 0.880 | `civ-precise` 1.563 | **−0.683** |
| ternary values | `civ-precise` 1.153 | `civ-poetic` 1.257 | **−0.103** |
| JEV as a decision oracle | `civ-precise` 1.413 | `civ-poetic` 1.727 | **−0.313** |

Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) →
0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) → 2/5 (132) →
2/5 (133) → 0/5 (134) → 4/5 (136) → **1/5 (137)**. Seventeen five-sample points cannot narrow a
rate — the honest claim is *somewhere in 0–80 %*. What survives every session: the chooser is
**not** a pure argmax, and **every** observed disagreement across the fleet goes the same way
(it picks a lower-scoring candidate). **Never treat `win_rate` as a quality metric.**

*Mechanism (confirmed in the source this session):* the chooser is a JEV **`choice`** question over
150-char `content_preview` snippets, whereas `avg_score` is the mean of three *score* questions
(quality/novelty/alignment) on the same text. Different questions, different answers — the
disagreement is expected, not a bug. The "witness log" case (chooser took a candidate 0.683 below
the argmax) is the largest disagreement yet recorded in the clean-mock series.

Winner tally this run: `civ-precise` 4, `civ-mythic` 1.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 39 consecutive sessions (95–137)

Last on lifetime `avg_score` (**1.1332**), `alignment` (**1.3203**), `quality` (**0.5333**),
`relevance` (**892.47**) and `relevance_per_sim` (**1.090**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.3203 | therapist 1.6230 | **0.3027** |
| `quality` | 0.5333 | formal 0.5661 | 0.0328 |

The structural gap is **alignment** — ~9.2× wider than quality. Alignment is the dimension the
meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a **voice** failure,
not a capability failure. It scores *above* median on novelty (1.5460 lifetime), so it is not
boring — it is **unmistakable in a way the chooser does not reward**.

This run's `alignment` gap is the widest in the tracked series (0.3027 lifetime, vs 0.4743
reported for the previous session on a different comparison pair — the pair changes as the ranking
shifts, so the absolute gap is not directly comparable across sessions).

Distinct axes:

| civ | axis | lifetime |
|---|---|---|
| `civ-grounded` | lowest `avg_score`, `alignment`, `quality`, `relevance` | 39 sessions |
| `civ-formal` | lowest `novelty` (1.4189) | steady |
| `civ-engineer` | 2nd-lowest `avg_score` (1.2962) | steady |
| `civ-precise` | highest `alignment` (2.3154) but mid `quality` (0.6282) | steady |
| `civ-poetic` | top on `avg_score` (1.7180) and `quality` (0.9228) | steady |

### This run's own ranking (80 new rows)

`civ-grounded` is again last (0.8250), but the this-run ordering is much flatter than lifetime:
only 0.0340 separates Grounded from `civ-therapist` (0.8590). The this-run `alignment` ordering is
also compressed: Grounded 0.2420 vs Therapist 0.2350 — a gap of 0.0070, i.e. **the two are
indistinguishable on alignment this run**, and Grounded is nominally *above* Therapist there.
Do not read the this-run Grounded-last result as a reproduction of the lifetime gap; the lifetime
table is the structural signal.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild it from the RUNBOOK with
   **both** fixes, and re-run the pre-flight probe before the batch.
2. `ZAI_TOKEN` is still absent ⇒ the real z.ai endpoint is unusable; Control B remains the only
   provider path. JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the **run-wide** integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and the
   **ts-sorted last-8-per-prompt** slice for per-prompt distinctness.
4. `civ-grounded` has been the low-relevance civ for 39 straight sessions. If a session ever finds
   it mid-table, that is a *finding* — check the run-wide seed count first to rule out a degenerate
   mock before believing it.
