# Civ Orchestrator — RUN REPORT session 139 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `134777a` (session 138 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe → HTTP 200 with a real
score body, `jev-1.14.0`).
**Run status:** all verification checks PASS (24/24 + 5/5 per-prompt distinctness).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `git clone` into `/workspace/repos/...` dies on `.git/description`; a 1 KB `dd` into `/workspace` also fails; `cp` leaves 0-byte files that still appear in `ls` |
| Bridge | `ln -s /tmp/wk/AI-Writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:12602` on both sides, `-ef` confirms |
| Clone target | `/tmp/wk/AI-Writings` (filtered, `--filter=blob:none --no-checkout --depth 1` + sparse-checkout); `/tmp` is exempt from the NAS quota |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/cellular-first-design` slug 404s (confirmed again, unauthenticated **and** authenticated) |
| `gh` | not installed (20th session) |
| Tool timeout | 30 s < run ~50 s → launched detached, polled |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; all 8 return `401 token expired or incorrect` against z.ai (endpoint healthy ⇒ credential gap, not an outage) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (wrapper 394 + server 396); `curl` exit 7 = port closed; 0 tracebacks in the log |

### Bridge reconstruction gotcha (new this session)

`ln -sfn <target> <link>` **silently replaced the symlink with a real directory** when a
stale `cellular-first-design/` directory already existed at the link path (left behind by the
failed in-NAS clone attempt). The result looked right in `ls -la` but `stat -L` showed
**different inodes** on the two sides and `-ef` failed. `ln -sfn` does **not** clobber a
directory target.

**Check `-ef` / inode identity after creating the bridge, not just `ls -la`.** If the link
path is a real directory, `rm -rf` it first and then use plain `ln -s` (no `-f`).

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
cultural-prompt lengths 167–199 chars, **0 tracebacks** in `/tmp/mock_zai.log`.

## Verification (24/24 PASS + 5/5 per-prompt)

- per-civ `simulations.jsonl` Δ = **+10** × 8 (5 sim-phase + 5 competition-phase) = **80 new rows**
  (engineer 826→836, formal 857→867, grounded 872→882, mythic 829→839, poetic 851→861,
  precise 821→831, therapist 824→834, whimsical 884→894)
- `meta_log.jsonl` Δ = **+5** (428 → 433)
- `Winner:` lines = **5**; "running 5 sims" headers = **8**
- **80/80** rows carry the `[mock-zai` prefix, `provider` = `{zai}` (all 80)
- **0** rows with a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple
- **40 distinct seeds across the 80 new rows** = 8 civs × 5 prompts ⇒ seed is a clean 1:1
  function of `(civ, prompt)`; **0** `(civ, prompt)` combos carry >1 seed
- **5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews** (ts-sorted last-8
  slice) — the **fourteenth consecutive clean measurement** (118, 120–123, 125, 131–134, 136–139)
- `avg_score` over the 80 new rows: min 0.9967, max 2.1967, mean 1.5843, **71/80 distinct values**
- `leaderboard.json` rewritten at 22:43:20Z
- registry still 8 civs, all `generation=1`, no extinction/birth (single batch, not `--loop`)

## Results

### Chooser vs `avg_score` argmax: 2/5 (40 %)

`civ-precise` won **3/5**; `civ-grounded` 1, `civ-formal` 1. All 3 disagreements go the **same
direction** — the chooser picked a *lower*-scoring candidate:

| prompt | winner | score | argmax | score | delta |
|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 2.11 | `civ-precise` | 2.11 | match |
| bookkeeper's role | `civ-precise` | 2.08 | `civ-precise` | 2.08 | match |
| witness log | `civ-grounded` | 1.35 | `civ-precise` | 2.20 | **−0.847** |
| ternary values | `civ-precise` | 1.52 | `civ-poetic` | 1.67 | **−0.153** |
| JEV as a decision oracle | `civ-formal` | 1.47 | `civ-poetic` | 1.81 | **−0.337** |

Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) →
0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) → 2/5 (132) →
2/5 (133) → 0/5 (134) → 4/5 (136) → 1/5 (137) → 1/5 (138) → **2/5 (139)**. Nineteen five-sample
points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What survives every
session: the chooser is **not** a pure argmax, and **every** observed disagreement across the
fleet goes the same way (it picks a lower-scoring candidate). **Never treat `win_rate` as a
quality metric.**

*Mechanism:* the chooser is a JEV **`choice`** question over 150-char `content_preview` snippets,
whereas `avg_score` is the mean of three *score* questions (quality/novelty/alignment) on the
same text. Different questions, different answers — the disagreement is expected, not a bug.
The "witness log" case (chooser took a candidate **0.847 below** the argmax) is the **largest
disagreement in the clean-mock series**, beating the session-137 record (0.683) and the
session-138 record (0.420).

### `civ-grounded` (The Grounded) remains the low-relevance civ — 41 consecutive sessions (95–139)

Last on lifetime `avg_score` (**1.1242**), `alignment` (**1.3061**), `quality` (**0.5239**),
`relevance` (**907.19**) and `relevance_per_sim` (**1.081**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.3061 | poetic 2.2497 | **0.9436** |
| `quality` | 0.5239 | whimsical 0.7377 | 0.2137 |

The structural gap is **alignment** — **4.4× wider** than the quality gap. Alignment is the
dimension the meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a
**voice** failure, not a capability failure. It scores *above* median on lifetime novelty
(1.5426), so it is not boring — it is **unmistakable in a way the chooser does not reward**.

Distinct axes:

| civ | axis | lifetime |
|---|---|---|
| `civ-grounded` | lowest `avg_score`, `alignment`, `quality`, `relevance` | 41 sessions |
| `civ-formal` | lowest `novelty` (1.4177) | steady |
| `civ-engineer` | 2nd-lowest `avg_score` (1.2864) | steady |
| `civ-precise` | highest `alignment` (2.3036) but mid `quality` (0.6216) | steady |
| `civ-poetic` | top on `avg_score` (1.7058) and `quality` (0.9109) | steady |

### This run's own ranking (80 new rows)

| rank | civ | `avg_score` | alignment | quality | novelty |
|---|---|---|---|---|---|
| 1 | `civ-precise` | 1.9520 | 2.7410 | 0.6850 | 2.4300 |
| 2 | `civ-poetic` | 1.8447 | 2.2820 | 0.7920 | 2.4600 |
| 3 | `civ-formal` | 1.6743 | 2.1400 | 0.5070 | 2.3760 |
| 4 | `civ-whimsical` | 1.6683 | 1.9780 | 0.5530 | 2.4740 |
| 5 | `civ-engineer` | 1.6443 | 2.1230 | 0.5090 | 2.3010 |
| 6 | `civ-mythic` | 1.4430 | 1.5120 | 0.5250 | 2.2920 |
| 7 | `civ-grounded` | 1.3163 | 1.3470 | 0.2320 | 2.3700 |
| 8 | `civ-therapist` | **1.1310** | **0.5790** | 0.2860 | 2.5280 |

`civ-grounded` is **7th of 8** on this run's `avg_score` (1.3163) and **7th of 8** on alignment
(1.3470) — consistent with its lifetime position, so no divergence to investigate.
`civ-therapist` took the run-level low on **both** `avg_score` (1.1310) and `alignment`
(0.5790) for the **second consecutive session** (session 138 flagged the same). Per the
session-132 rule this is a *per-run low ⇒ watch axis*, not a finding: Therapist's lifetime
standing is 4th of 8 on `avg_score` (1.3300) and its lifetime alignment is mid-field (1.5912).
**It becomes a finding if it repeats again next session.**

This run's spreads: `alignment` 2.162, `novelty` 0.227, `quality` 0.560 — `alignment` again
carried the widest spread and is again the axis the chooser selects on. Note the `quality`
axis did **not** collapse this session (mean 0.5103, max 0.7920) — confirming that the quality
collapse is a **LEVEL that moves, not a stable property**.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild it from the RUNBOOK with
   **both** fixes, and re-run the pre-flight probe before the batch.
2. `ZAI_TOKEN` is still absent ⇒ the real z.ai endpoint is unusable; Control B remains the only
   provider path. JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. **Do not use `ln -sfn` for the bridge if a real directory sits at the link path** — it
   replaces the symlink with a directory. `rm -rf` the path, then plain `ln -s`, then verify
   `-ef` + inode identity.
4. Use the **run-wide** integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and the
   **ts-sorted last-8-per-prompt** slice for per-prompt distinctness.
5. `civ-grounded` has been the low-relevance civ for 41 straight sessions. If a session ever finds
   it mid-table, that is a *finding* — check the run-wide seed count first to rule out a degenerate
   mock before believing it.
6. **`civ-therapist` is now a second watch axis** — run-level low on `avg_score` and
   `alignment` in **two consecutive sessions** (138, 139). One more repeats it and it becomes a
   finding.
