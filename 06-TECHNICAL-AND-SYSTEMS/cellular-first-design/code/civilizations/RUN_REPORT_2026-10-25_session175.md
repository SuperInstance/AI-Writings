# Civ Orchestrator — Run Report, session 175 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `53039bb` (session 174 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override alone is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; probe -> HTTP 200, real score body,
model `jev-1.14.0`).
**Run status:** all verification checks PASS — 80 new rows, 5/5 competitions, 0 JEV errors,
mock non-degenerate 5/5, **16th consecutive clean measurement**.

---

## Headline for the next session

- **`civ-grounded` remains the low-relevance civ — 50th consecutive session.** Last of 8 on
  lifetime `avg_score` 1.0024, `alignment` 1.0586, `quality` 0.4036, `relevance` 1160.61,
  `relevance_per_sim` 0.968. Alignment gap **0.1726** vs quality gap **0.0420** => **4.11x**
  wider => a **voice** failure, not a prose failure. Extinction risk **NONE** (threshold −10;
  lowest +1160.61 = **116x** the floor).
- **The run-level low ROTATED to `civ-engineer`** (0.6283 run bottom on `avg_score`,
  `alignment` 0.5180, `quality` 0.0720) while its *lifetime* standing is 6th of 8.
  **Watch axis, not the finding** (session-132 rule).
- **Chooser vs `avg_score` argmax: 2/5 (40 %)** — `civ-precise` swept **5/5**. All **three**
  disagreements went the same way: the chooser took the **lower**-scoring candidate
  (−0.2033, −0.2000, −0.1200). Consistent with every observed disagreement in the series.
- **Counter gap +68.3667** — the sum of `avg_score` over the 80 new rows; `d_relevance` is
  **8/8 EXACT** against it (max abs diff **1.94e-13**).
- Run spreads: `avg_score` 0.9807, `alignment` **0.7360**, quality **0.2080**, novelty 0.6760.
  `avg_score` carried the widest spread this run — the first run in the recent series where
  the ordering axis, not `alignment`, dominated the spread.
- Verification: per-civ delta **+10 x 8** = **80** new rows, `meta_log` **+5** (608 -> 613),
  `Winner:` **5**, wins **+5**, 0 JEV errors, `zai x 80`, **40/40** distinct seeds, **0**
  `(civ,prompt)` with >1 seed, registry 8 all gen 1, extinction **NONE**.

## NEW — the RUNBOOK's "novelty is above median" claim is STALE; it is 6th of 8

The RUNBOOK's session-169/172 headline says:

> "Lifetime novelty 1.5044 is **6th of 8** (not 'above median')."

but the same file's *older* sessions (138, 143, 144) assert:

> "Lifetime novelty 1.5135 is above median — Grounded is not boring, it is unmistakable in
> a way the chooser does not reward."

Those two claims **cannot both be true**, and the data settles it. Recomputed over the
**baseline** (pre-run) ledgers this session:

| civ | lifetime novelty (baseline) | vs median (1.6595) |
|---|---|---|
| civ-whimsical | 1.9159 | ABOVE |
| civ-poetic | 1.8665 | ABOVE |
| civ-therapist | 1.7501 | ABOVE |
| civ-mythic | 1.7292 | ABOVE |
| civ-precise | 1.5897 | below |
| **civ-grounded** | **1.5112** | **BELOW (6th of 8)** |
| civ-engineer | 1.5070 | below |
| civ-formal | 1.4238 | below |

and the same ordering after this run's 80 rows are added (median 1.6686; grounded **1.5450**,
6th of 8). The ranking is stable across the run boundary, so this is not a run artifact.

⇒ **`civ-grounded` is BELOW median on novelty, not above it.** The "not boring" reading was
carried forward for several sessions on an unchecked premise. The correct description is
sharper: Grounded is **unremarkable on every axis** — it is 8th on `avg_score`, 8th on
`quality`, 8th on `alignment`, **6th** on `novelty`, and 8th on `relevance`. The voice-failure
conclusion (alignment gap 4.11x wider than the quality gap) is **unaffected** — it rests on
the *gap ratio*, not on the novelty claim. But the supporting sentence "novelty is above
median" must be dropped, and the "unmistakable in a way the chooser does not reward" framing
is **not supported by the novelty axis**: it is not distinctive at all.

**Rule: a qualitative claim carried across sessions ("above median", "6th of 8") must be
recomputed against the ledger, not copied from a prior report.** A claim that contradicts
another claim in the same file is a signal to recompute, not to pick one.

## NEW — the distinct-seed expectation is 40, not 80, and the multiplicity is not uniform

The mock's seed is **message-derived** (fix f: `i = md5(message)[0] % 4`), so a seed is a
function of the `(civ, prompt)` pair, not of the request. This run's 80 rows break down as
**5 sim rows + 5 competition rows per civ**, and the 5 sim rows draw prompts *with
replacement* from the 5 canon prompts. The result:

- **40 distinct seeds / 80 rows** (2 rows per seed on average) — matches the RUNBOOK spec.
- rows-per-`(civ,prompt)` distribution = **{1: 12, 2: 17, 3: 10, 4: 1}**, i.e. 1 competition
  row + 0..3 random sim draws per pair. **Not** 2 each.
- **5/5** prompts at **8/8** distinct seeds AND **8/8** distinct previews.
- **80/80** rows match an independently recomputed `md5(whole_message)` for seed, colour and
  figure; **0** literal `seed={}`; **0** tracebacks / `EXC:` in the mock log.

⇒ A checker that asserts "each seed appears exactly 2x", or "80 distinct seeds", fails on a
**healthy** mock. The correct invariants are: 40 distinct seeds, 40 distinct previews,
1:1 seed↔preview, 8/8 per prompt, 0 `(civ,prompt)` with >1 seed, and 80/80 md5 recompute.
Two of my own checks failed this session on exactly this point before the data settled it.

**Rule: seed counts must be derived from the *message space* (8 civs x 5 prompts = 40), not
from the row count.** A seed is a hash of the message; the row count is a sampling accident.

## Environment recovery

- The workspace was **empty** apart from `.plugin-cache` — the prompt's path did not exist
  (**15th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`**; the `ai-writings/cellular-first-design` slug
  404s (the API is case-insensitive) — `cellular-first-design` is a **subdirectory inside**
  `SuperInstance/AI-Writings`, not a repo. Located via
  `GET /search/code?q=filename:civilization_orchestrator.py` => exactly **1** hit, in the
  right path. `gh` is **not installed** (23rd session) — used the REST API with `GITHUB_TOKEN`.
- Cloned to **`/tmp/cfd/repo`** with `--filter=blob:none --no-checkout` +
  `sparse-checkout set cellular-first-design` => 192 KB. Cloning into `/workspace` fails with
  **`Disk quota exceeded`** (NAS EDQUOT, **21st session**).
- **NAS WRITE TRAP — unchanged.** `/workspace` is at **100 % quota** (600 G/600 G, 0 bytes
  free) while being *visibly empty*. `cp` exits 1 and leaves 0-byte files that `ls` still
  lists; the **symlink inode** survives, so the bridge works even at 100 % quota.
- Bridge: `ln -sfn /tmp/cfd/repo/cellular-first-design
  /workspace/repos/ai-writings/cellular-first-design`; verified by **inode identity**
  (`129:11559` on both sides) and by the shell `[ -ef ]` test => `EF_OK`.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401** `token expired or
  incorrect` (endpoint healthy, credential absent) — **58th session**.
- **JEV live**: well-formed body -> **HTTP 200** with `{"model":"jev-1.14.0", ...}`.
- Tool timeout 30 s < orchestrator run ~28 s => detached launch under
  `setsid nohup timeout -s KILL 900`, stdout redirected, `< /dev/null`, polled by PID.

## Mock rebuild — the six fixes, all re-applied

| # | Fix | Session | Applied this session |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` index wrap | 112 | yes |
| b | `md5(whole_message)` | 118 | yes |
| c | `Connection: close` + `Content-Length` | 144 | yes |
| d | interpolate the seed placeholder | 145 | yes |
| e | seed widened 2 -> 4 hex chars | 169 | yes |
| f | index derived from the MESSAGE (`d[0] % 4`) | 170 | yes |
| g | figure = three string components, not a division | 174 | yes |

**Pre-flight gate passed 8/8 on the FIRST build** — no rebuild drift:

- 40 requests using the **exact long cultural prompts** (body lengths **167-209** chars)
- **40/40** distinct seeds, **40/40** distinct previews
- **40/40** independently recomputed md5s (seed, colour, figure)
- **5/5** prompts at **8/8** distinct seeds AND **8/8** distinct previews
- 0 literal `seed={}`, 0 `EXC:` / tracebacks in the mock log
- **[mock-zai** prefix on **40/40**
- **repeat-same-message => same seed: 40/40** (the probe that catches fix f)

## Verification — 47 checks, all PASS

| group | checks | result |
|---|---|---|
| A. run isolation (per-civ tails, `ts` sort) | 2 | PASS |
| B. mock integrity on the 80 new rows | 5 | PASS |
| C. independent md5 recompute | 2 | PASS |
| D. meta_log vs ledger (later-`ts` row) | 3 | PASS |
| E. culture.json + leaderboard | 15 | PASS |
| F. run-level ranking + chooser vs argmax | 3 | PASS |
| G. relevance bookkeeping | 1 | PASS |
| H. lifetime leaderboard | 3 | PASS |
| I. lifetime axis table | 5 | PASS |
| seed/preview structure | 8 | PASS |
| pre-flight gate | 8 | PASS |

**A. Run isolation** — per-civ tail of **10** rows (never `rows[-N:]` over the concatenation;
`glob()` order is filesystem order, not chronological), then an explicit `ts` sort before any
grouping. per-civ delta **+10 x 8 = 80**; `meta_log` **+5** (608 -> 613); `Winner:` **5**.

**B. Mock integrity** — `provider=zai` **80/80**; `[mock-zai` prefix **80/80**; **0** rows with
a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple; **40** distinct seeds
with **0** `(civ,prompt)` carrying >1 seed; **80/80** distinct `(q,n,a)` triples.

**D. meta_log vs ledger** — the meta-vs-ledger check takes the **later-`ts`** row; **0**
mismatches across all 40 (civ, prompt) comparisons.

**E. culture + leaderboard** — `simulations_run` **+10** for all 8; `relevance_score` up for
all 8; leaderboard `ts` advanced `2026-10-25T05:24:00` -> `2026-10-25T05:35:16`; board sorted
by `relevance_per_sim` desc; **`wins+losses` delta = +5 per civ** (not +10 — the session-166
correction); registry 8, all `generation` 1.

**G. Counter gap** — `d_relevance` vs `sum(avg_score)` over the 10 new rows is **8/8 EXACT**
(max abs diff **1.94e-13**). Counter total **+68.3667**.

**H. Leaderboard (lifetime, after this run)**

| rank | civ | rel/sim | relevance | wins | losses | win_rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1.527 | 1807.82 | 6 | 582 | 0.010 | 1 | 0.8 |
| 2 | civ-precise | 1.408 | 1654.31 | 351 | 232 | 0.602 | 1 | 0.2 |
| 3 | civ-whimsical | 1.329 | 1582.40 | 5 | 583 | 0.009 | 1 | 0.95 |
| 4 | civ-mythic | 1.236 | 1457.52 | 10 | 572 | 0.017 | 1 | 0.85 |
| 5 | civ-formal | 1.165 | 1380.43 | 94 | 492 | 0.160 | 1 | 0.3 |
| 6 | civ-engineer | 1.129 | 1325.41 | 47 | 534 | 0.081 | 1 | 0.4 |
| 7 | civ-therapist | 1.128 | 1328.23 | 11 | 574 | 0.019 | 1 | 0.6 |
| 8 | **civ-grounded** | **0.968** | **1160.61** | 70 | 517 | 0.119 | 1 | 0.5 |

**Extinction risk NONE** — threshold −10; the lowest relevance (+1160.61) is **116x** the
floor. Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

## Low-relevance civilization: **`civ-grounded` (The Grounded)** — 50th consecutive session

Last of 8 on **every** axis:

| axis | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.0024** | 1.1452 (engineer) | 0.1428 |
| `alignment` | **1.0586** | 1.2311 (therapist) | **0.1726** |
| `quality` | **0.4036** | 0.4456 (engineer) | 0.0420 |
| `relevance` | **1160.61** | 1325.41 (engineer) | 164.80 |
| `relevance_per_sim` | **0.968** | 1.128 (therapist) | 0.160 |
| `novelty` | 1.5450 (6th of 8) | 1.5223 (engineer) | 0.0227 |

**The binding constraint is `alignment`.** The gap to the next civ is **0.1726** on alignment
vs **0.0420** on quality — **4.11x** wider. Alignment is the axis the meta-GAN's `choice`
question selects on, so this is a **voice** failure, not a prose failure: Grounded's prose is
competitive, but the chooser does not hear it as culturally aligned.

**Correction to the prior framing (see NEW above):** novelty is **6th of 8 and below median**
— it is *not* an above-median strength. Grounded is unremarkable on all five axes rather
than distinctive-but-unrewarded.

**Run-level low ROTATED to `civ-engineer`** (run `avg_score` 0.6283, `alignment` 0.5180,
`quality` 0.0720 — the run bottom on all three) while its *lifetime* standing is 6th of 8.
Per the session-132 rule that is a **watch axis, not a finding**. It becomes one only if the
lifetime axis moves too.

## Run-level results (this run only)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | 1.0527 | 0.2800 | 1.7820 | 1.0960 |
| civ-whimsical | 1.0343 | 0.1380 | 1.9710 | 0.9940 |
| civ-precise | 0.9330 | 0.2480 | 1.2970 | 1.2540 |
| civ-formal | 0.8713 | 0.1360 | 1.3360 | 1.1420 |
| civ-therapist | 0.8593 | 0.1080 | 1.5700 | 0.9000 |
| civ-mythic | 0.7453 | 0.1190 | 1.4950 | 0.6220 |
| civ-grounded | 0.7123 | 0.1500 | 1.4250 | 0.5620 |
| **civ-engineer** | **0.6283** | **0.0720** | 1.2950 | **0.5180** |

Run spreads: `avg_score` 0.9807, `alignment` 0.7360, quality 0.2080, novelty 0.6760.

**Levels sit BELOW the lifetime band** (run `avg_score` 0.63-1.05 vs lifetime 1.00-1.56) —
the same *direction* as session 166 and the opposite of 168/169. The **ordering** carries the
information, not the level.

## Chooser vs `avg_score` argmax: 2/5 (40 %)

| prompt | winner | score | argmax | score | agree | delta |
|---|---|---|---|---|---|---|
| what a cell is. | civ-precise | 0.8067 | civ-whimsical | 1.0100 | no | −0.2033 |
| the bookkeeper's role. | civ-precise | 0.9167 | civ-precise | 0.9167 | yes | 0.0000 |
| the witness log. | civ-precise | 1.2800 | civ-precise | 1.2800 | yes | 0.0000 |
| ternary values. | civ-precise | 0.8867 | civ-poetic | 1.0867 | no | −0.2000 |
| JEV as a decision oracle. | civ-precise | 0.9600 | civ-poetic | 1.0800 | no | −0.1200 |

**`civ-precise` swept 5/5.** All **three** disagreements again took the **lower**-scoring
candidate, which is the direction observed in every disagreement across the series. Max
|delta| **0.2033** — well below session 168's record (−1.1033).

**Never treat `win_rate` as a quality metric.** `civ-poetic` is 1st on lifetime `avg_score`
(1.5599), `quality` (0.7444) and `relevance` (1807.82) but **7th** on `win_rate` (0.010) —
the sharpest inverse in the fleet. `civ-whimsical` is 1st on novelty and 3rd on `avg_score`
but **last** on `win_rate` (0.009).

The clean-mock series now holds 16 five-sample points spanning 0/5 – 4/5. The honest claim
remains *somewhere in 0-80 %*; what survives every session is the **direction** — the chooser
is not a pure argmax, and it takes the lower-scoring candidate when it disagrees.

## Notes for the next session

- The **distinct-seed expectation is 40 over 80 rows**, and the per-`(civ,prompt)`
  multiplicity is **not** 2 — it is {1:12, 2:17, 3:10, 4:1}. Assert against the message
  space, not the row count.
- The **novelty "above median"** claim for `civ-grounded` is **stale and wrong** — 6th of 8,
  below median, in both the baseline and the post-run ledgers. Do not carry it forward.
- `civ-grounded` is the lifetime low for the **50th** consecutive session; the run-level low
  rotated to `civ-engineer` (watch axis).
- Mock fixes a-g all re-applied; pre-flight **8/8 on the first build**.
- NAS EDQUOT (21st session) — clone to `/tmp`, sparse-checkout, bridge the **clone root**,
  verify by inode identity. `cp` into `/workspace` fails; `ln` works.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder
  **and** `ZAI_URL_OVERRIDE` set (the override alone is dead code behind the token gate).
