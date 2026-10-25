# Civ Orchestrator — RUN REPORT session 138 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `b969222` (session 137 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe → HTTP 422
`{"type":"too_short"}` = token accepted; `/v1/models` → 200).
**Run status:** all verification checks PASS (23/23).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `git clone` into `/workspace/repos/...` dies on `.git/description`; `cp` exits 1 with `Disk quota exceeded` and leaves 0-byte files that still appear in `ls` |
| Bridge | `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:10423` on both sides, `-ef` confirms |
| Clone target | `/tmp/aiw` (full clone, `--depth 50`); `/tmp` is exempt from the NAS quota |
| `gh` | not installed (19th session) |
| Tool timeout | 30 s < run ~55 s → launched detached, polled |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; real endpoint returns 401 (endpoint healthy ⇒ credential gap, not an outage) |
| JEV | live — 422 on an empty `questions` dict = token accepted; `/v1/models` → 200 |
| Mock teardown | killed **both** pids (wrapper 237 + server 239); `curl` exit 7 = port closed; 0 tracebacks in the log |

## Mock rebuild

`/tmp` was wiped again ⇒ the mock was rebuilt from the RUNBOOK. **Both** historical bugs had to be
re-applied, and both are load-bearing:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — without it the bridge 500s on `i>=4`
  **while the socket stays open**, so a port/200 probe looks healthy.
- session-118 md5-of-whole-message seeding `md5(msg)[:8]` — without it all 8 civs emit
  identical text (`"YouAreA"` is the first 8 alnum chars of *every* cultural prompt) and every
  competition result is void.

**Pre-flight probe (live mock, exact long cultural prompt):** 8 civs → **8/8 distinct seeds**,
**8/8 distinct previews**, HTTP 200, `[mock-zai seed=…]` prefix present on every body,
cultural-prompt lengths 168–200 chars, **0 tracebacks** in `/tmp/mock_zai.log`. The pre-flight
probe is what keeps a broken mock from reaching the ledger.

## Verification (23/23 PASS)

- per-civ `simulations.jsonl` Δ = **+10** × 8 (5 sim-phase + 5 competition-phase) = **80 new rows**
  (engineer 816→826, formal 847→857, grounded 862→872, mythic 819→829, poetic 841→851,
  precise 811→821, therapist 814→824, whimsical 874→884)
- `meta_log.jsonl` Δ = **+5** (423 → 428)
- `Winner:` lines = **5**
- **80/80** rows carry the `[mock-zai` prefix, `provider` = `{zai}` (all 80)
- **0** rows with a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple
- **40 distinct seeds across the 80 new rows** = 8 civs × 5 prompts ⇒ seed is a clean 1:1
  function of `(civ, prompt)`; **0** `(civ, prompt)` combos carry >1 seed
- **5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews** (ts-sorted last-8
  slice) — the **thirteenth consecutive clean measurement** (118, 120–123, 125, 131–134, 136, 137)
- `avg_score` over the 80 new rows: min 0.0500, max 0.6567, mean 0.2777, **66/80 distinct values**
- `leaderboard.json` rewritten at 22:23:43Z
- registry still 8 civs, all `generation=1`, no extinction/birth (single batch, not `--loop`)

## Results

### Chooser vs `avg_score` argmax: 1/5 (20 %)

`civ-precise` won **3/5**; `civ-engineer` 1, `civ-formal` 1. All 4 disagreements go the **same
direction** — the chooser picked a *lower*-scoring candidate:

| prompt | winner | score | argmax | score | delta |
|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 0.497 | `civ-precise` | 0.497 | match |
| bookkeeper's role | `civ-precise` | 0.430 | `civ-whimsical` | 0.497 | **−0.067** |
| witness log | `civ-precise` | 0.620 | `civ-poetic` | 0.637 | **−0.017** |
| ternary values | `civ-engineer` | 0.110 | `civ-poetic` | 0.530 | **−0.420** |
| JEV as a decision oracle | `civ-formal` | 0.230 | `civ-poetic` | 0.597 | **−0.367** |

Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) →
0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) → 2/5 (132) →
2/5 (133) → 0/5 (134) → 4/5 (136) → 1/5 (137) → **1/5 (138)**. Eighteen five-sample points
cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What survives every session:
the chooser is **not** a pure argmax, and **every** observed disagreement across the fleet goes
the same way (it picks a lower-scoring candidate). **Never treat `win_rate` as a quality metric.**

*Mechanism:* the chooser is a JEV **`choice`** question over 150-char `content_preview` snippets,
whereas `avg_score` is the mean of three *score* questions (quality/novelty/alignment) on the
same text. Different questions, different answers — the disagreement is expected, not a bug.
The "ternary values" case (chooser took a candidate **0.420 below** the argmax) ties the
session-137 record (0.683) for the largest disagreement in the clean-mock series.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 40 consecutive sessions (95–138)

Last on lifetime `avg_score` (**1.1220**), `alignment` (**1.3056**), `quality` (**0.5273**),
`relevance` (**978.37**) and `relevance_per_sim` (**1.078**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.3056 | engineer 1.7750 | **0.4694** |
| `quality` | 0.5273 | engineer 0.5722 | 0.0450 |

The structural gap is **alignment** — **10.4× wider** than the quality gap. Alignment is the
dimension the meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a
**voice** failure, not a capability failure. It scores *above* median on lifetime novelty
(1.5331), so it is not boring — it is **unmistakable in a way the chooser does not reward**.

Distinct axes:

| civ | axis | lifetime |
|---|---|---|
| `civ-grounded` | lowest `avg_score`, `alignment`, `quality`, `relevance` | 40 sessions |
| `civ-formal` | lowest `novelty` (1.4065) | steady |
| `civ-engineer` | 2nd-lowest `avg_score` (1.2821) | steady |
| `civ-precise` | highest `alignment` (2.2983) but mid `quality` (0.6208) | steady |
| `civ-poetic` | top on `avg_score` (1.7042) and `quality` (0.9123) | steady |

### This run's own ranking (80 new rows)

`civ-grounded` is **6th of 8** on this run's `avg_score` (0.1550), not last — `civ-therapist` took
the run-level low (0.1257) and `civ-engineer` was 7th (0.1313). Grounded is also **6th of 8** on
this run's `alignment` (0.0400) behind Therapist (0.0180) and Mythic (0.2190)… in fact only
Therapist sits lower on alignment. Per the session-132 rule this is a **per-run low ⇒ watch axis**,
not a finding: Grounded's **lifetime** position is unchanged and the lifetime table is the
structural signal. `civ-therapist` taking the run-level low for the first time (it was flagged as
a watch axis in session 123 on alignment) is worth noting but does not displace Grounded.

The this-run `quality` axis collapsed again (mean 0.0139, max 0.030) — the 119/121/122/138 regime
vs session-120's 0.106–0.446. **The quality collapse is a LEVEL that moves, not a stable
property** — compare cross-civ spreads before ranking on a dimension. This run's spreads:
`alignment` 1.140, `novelty` 0.427, `quality` 0.026 — `alignment` again carried the widest
spread and is again the axis the chooser selects on.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild it from the RUNBOOK with
   **both** fixes, and re-run the pre-flight probe before the batch.
2. `ZAI_TOKEN` is still absent ⇒ the real z.ai endpoint is unusable; Control B remains the only
   provider path. JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the **run-wide** integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and the
   **ts-sorted last-8-per-prompt** slice for per-prompt distinctness.
4. `civ-grounded` has been the low-relevance civ for 40 straight sessions. If a session ever finds
   it mid-table, that is a *finding* — check the run-wide seed count first to rule out a degenerate
   mock before believing it.
5. **`civ-therapist` is now a second watch axis** — it took the run-level low on both `avg_score`
   (0.1257) and `alignment` (0.0180). Its lifetime standing is mid-field (5th of 8 on
   `avg_score`), so it is not yet a finding; it becomes one if it repeats.
