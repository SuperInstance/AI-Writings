# Civ Orchestrator — RUN REPORT session 136 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `7ddd3f0` (session 135 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe → HTTP 422
`{"type":"dict_type"}` = token accepted).
**Run status:** all 20 verification checks PASS.

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `git clone` into `/workspace/repos/...` dies on `.git/description`; `cp` exits 1 with `Disk quota exceeded` and leaves 0-byte files that still appear in `ls` |
| Bridge | `ln -sfn /tmp/work/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:12602` on both sides, `-ef` confirms |
| `ls` race | did **not** reproduce — 5/5 sequential retries OK, first attempt OK |
| `gh` | not installed (17th session) |
| Tool timeout | 30 s < run ~50 s → launched detached, polled |
| z.ai credential | **absent** — `ZAI_TOKEN` unset; real endpoint returns 401 `token expired or incorrect` (endpoint healthy ⇒ credential gap, not an outage) |
| JEV | live — 422 on a malformed `questions` = token accepted |

## Mock rebuild

`/tmp` was wiped again ⇒ the mock was rebuilt from the RUNBOOK. **Both** historical bugs had to be
re-applied, and both are load-bearing:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — without it the bridge 500s on `i>=4`
  (`ValueError` on an empty slice) **while the socket stays open**, so a port/200 probe looks healthy.
- session-118 md5-of-whole-message seeding `md5(msg)[:8]` — without it all 8 civs emit
  identical text (`"YouAreA"` is the first 8 alnum chars of *every* cultural prompt) and every
  competition result is void.

**Pre-flight probe (live mock, exact long cultural prompt):** 8 civs → **8/8 distinct seeds**,
**8/8 distinct previews**, HTTP 200, `[mock-zai seed=…]` prefix present, **0 tracebacks** in
`/tmp/mock_zai.log`. The pre-flight probe is what keeps a broken mock from reaching the ledger.

## Verification (20/20 PASS)

- per-civ `simulations.jsonl` Δ = **+10** × 8 (5 sim-phase + 5 competition-phase) = **80 new rows**
- `meta_log.jsonl` Δ = **+5** (413 → 418)
- `Winner:` lines = **5**
- **80/80** rows carry the `[mock-zai` prefix, `provider` = `{zai}`
- **0** rows with a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple
- sim→competition ts gap at index 4 in all 8 civs (1.11 s – 22.75 s)
- `leaderboard.json` rewritten at 22:05:27Z
- registry still 8 civs, all `generation=1`

**Mock non-degeneracy: 5/5 competition prompts at 8/8 distinct previews AND 8/8 distinct seeds —
the ELEVENTH consecutive clean measurement** (118, 120–123, 125, 131–134).

## Results

### Chooser vs `avg_score` argmax: 4/5 (80 %)

`civ-precise` was argmax in 4/5 and won **5/5**. The single disagreement was p3 "ternary values":
argmax `civ-poetic` 0.580, winner `civ-precise` 0.577 — the chooser picked a **marginally lower**
scoring candidate. Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) →
3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) →
2/5 (132) → 2/5 (133) → 0/5 (134) → **4/5 (136)**. Sixteen five-sample points cannot narrow a rate —
the honest claim is *somewhere in 0–80 %*. What survives every session: the chooser is **not** a
pure argmax, and **every** observed disagreement across the fleet goes the same way (it picks a
lower-scoring candidate). **Never treat `win_rate` as a quality metric.**

Winner tally this run: `civ-precise` 5.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 38 consecutive sessions (95–136)

Last on lifetime `avg_score` (**1.1368**), `alignment` (**1.3330**), `quality` (**0.5391**),
`relevance` (**884.22**) and `relevance_per_sim` (**1.093**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.3330 | engineer 1.8073 | **0.4743** |
| `quality` | 0.5391 | therapist 0.6085 | 0.0694 |

The structural gap is **alignment** — ~6.8× wider than quality. Alignment is the dimension the
meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a **voice** failure, not
a prose failure. Its tenets ("concrete images, everyday language, specific examples, no
abstractions") and voice ("warm, factual") are the least differentiating prompt in the field.

Grounded was **also the run-level low** this session on `avg_score` (0.2703) and `alignment`
(0.1510) — the 6th consecutive session where the run-level label went to it (127 whimsical;
128/129/130/133/134/**136** grounded; 135 not in this series). Keep the lifetime finding and the
run-level label as **two separate claims**.

### Other axes

- **`civ-formal`** is the low-**novelty** axis — lifetime novelty **1.4089** (last), alignment
  1.9342 healthy.
- **`civ-poetic`** = 1st on lifetime `avg_score` (1.7210) / `quality` (0.9295) / `alignment`
  (2.2660) but **last on `win_rate` (0.013, 5/393)** — the stable selection-failure inverse.
- **`civ-precise`** = best `win_rate` (0.549), won 5/5, 1st on lifetime `alignment` (2.3233) —
  the mirror inverse.
- **Watch-axis `civ-engineer`** — 7th of 8 on lifetime `relevance_per_sim` (1.280) and 2nd-lowest
  on lifetime `avg_score` (1.2998), but 2nd on run `avg_score` (0.3407) — no trend; **do not
  promote**.
- **Watch-axis `civ-therapist`** — mid-field lifetime (avg 1.3533, 4th of 8), 4th of 8 on this run's
  `avg_score`. The axis stays open.
- **Extinction risk: NONE** — threshold −10; lowest raw relevance +884.22 (88× above the floor).
  Registry 8 civs, `max_civs` 12; birth/extinction only runs under `--loop`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` **1.2200**,
  `novelty` 0.7230, `avg_score` 0.5310, `quality` **0.0380**. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. `quality` again collapsed (0.018–0.056) —
  the 119/121/122/123/125/126/130/131/134 regime vs session-120's 0.106–0.446. **The quality
  collapse is a LEVEL that moves, not a stable property** — compare cross-civ spreads, not absolute
  levels, before ranking on a dimension.
- **Absolute run levels are depressed vs lifetime** (run `avg_score` 0.270–0.801 vs lifetime
  1.14–1.72) — a level shift in the JEV scorer's output for this batch, **not a civ effect**; the
  cross-civ *ordering* carries the information.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42, poetic +37,
  engineer +22, mythic +20, therapist +17, precise +16 (total +260). `save_state()` rewrites
  `culture.json` with no lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an
  auditor.

## Notes on method

- **Assert on rows, never on exit code.** `call_provider()` returns `None` when the token is
  missing, `run_simulation()` returns `None`, and the competition short-circuits on
  `if not results: return None` — all silently, with exit code 0.
- **Isolate this run's rows by count, not by a `ts` cutoff.** Prior sessions left mock rows in the
  ledger, so a `ts >=` filter pulls in historical rows. Use the per-civ tail (`rows[-10:]`).
- **Group the non-degeneracy check by per-civ slot index, not by `prompt`.** `prompt` is truncated
  to 80 chars and the sim phase reuses the same 5 canon prompts ⇒ grouping by prompt yields 16 rows
  per prompt, not 8, and a naive "exactly 8 rows" filter returns **0** competition prompts and a
  false FAIL.
