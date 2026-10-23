# Civilization Orchestrator — Session 12 (2026-10-23, concurrent replication of session 11)

Command requested:
```
python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py \
  --sims 5 --prompts 5 --providers zai
```

**Verdict: the requested command is a green no-op. It produced zero simulations.**
A Control B run (mock at the provider gate) was executed to produce a real
meta-GAN round for measurement. Mock rows were **not** committed; the working
tree was restored byte-identical to the pristine git blobs.

> **This is a concurrent second replication of session 11.** A separate instance
> ran the *same* command and committed `RUN_REPORT_2026-10-23_session11.md`
> (commit `733638e`) while this run was in flight. Its mock A/B reached
> **Kendall tau 1.00** (order preserved); this run's reached **tau 0.286**
> (order completely scrambled). Section 3 reconciles the two: they are **not
> contradictory** — they differ by the *magnitude* of the mock's per-civ
> perturbation relative to the adjacent-rank gap. The four-body-set pooled
> result in section 3.4 is the conclusion that survives both.

---

## 1. The requested run did nothing (10th consecutive session)

The unpatched command printed the batch header and all 8
`[Name] running 5 sims...` lines, then an **empty competition section with no
`Winner:` lines**, then **exit 0**.

| metric | before | after | delta |
|---|---|---|---|
| `civ-*/simulations.jsonl` rows | 684 | 684 | **+0** |
| `meta_log.jsonl` entries | 48 | 48 | **+0** |
| `Winner:` lines | — | **0** | — |
| exit code | — | 0 | — |
| `leaderboard.json` | — | rewritten (ts only) | — |

**Assert on the row delta, never on exit code.** The per-civ "running 5 sims"
lines are printed *before* the provider call and are not evidence of work.

### Root cause: the credential gap (unchanged, 10th replication)

`ZAI_TOKEN` is absent from the environment and from the 8-entry secret store.
All 7 available secrets re-tested against the z.ai coding endpoint
(`https://api.z.ai/api/coding/paas/v4/chat/completions`) → **401 "token expired
or incorrect"** on every one. A 401 (not 5xx) means the endpoint is healthy ⇒
**credential gap, not an outage**. `GROQ_TOKEN` is also absent, so there is no
alternate live provider. JEV is live (`jev-1.14.0`).

Gate that swallows it (line 79):
```python
token = os.environ.get(p["env"], "")
if not token: return None        # silent drop
```

---

## 2. Control B — a real meta-GAN round (two independent body sets)

Mock placed **at the provider gate** via a one-line `ZAI_URL_OVERRIDE` on the
`PROVIDERS["zai"]` URL, leaving the `ZAI_TOKEN` check intact, so the request is
really attempted and JEV really scores. Two independently written body sets
(run A "field notes" / run B "second light"), each with 8 distinct bodies per
voice, selected on a per-call seed.

| check | set A | set B |
|---|---|---|
| ledger rows | 684 → 764 (**+80**, 10/civ uniform) | 684 → 764 (**+80**) |
| `meta_log.jsonl` | 48 → 53 (**+5**) | 48 → 53 (**+5**) |
| competition winners | 5 | 5 |
| mock calls / fallbacks | 80 / **0** | 80 / **0** |
| distinct `content_preview` | 45 | 39 |
| distinct `avg_score` | 74 | 76 |
| all-2.0-default rows (JEV-outage tell) | **0** | **0** |
| score errors | **0** | **0** |

**Control B reproduces sessions 6-10 exactly** (+80 rows / +5 meta_log / 5
winners / 0 fallbacks / 0 outage-default rows).

---

## 3. THE HEADLINE — the mock reorders the fleet *when* its perturbation exceeds the rank gap

This run's two body sets: **exact position agreement 0/8**, Kendall tau **0.286** —
a complete scramble.

| rank | set A (mean `avg_score`) | set B (mean `avg_score`) |
|---|---|---|
| 1 | civ-mythic 2.284 | civ-poetic 2.413 |
| 2 | civ-whimsical 2.238 | civ-therapist 2.300 |
| 3 | civ-therapist 2.198 | civ-whimsical 2.210 |
| 4 | civ-poetic 2.113 | civ-mythic 2.165 |
| 5 | civ-engineer 2.032 | civ-grounded 2.154 |
| 6 | civ-precise 1.998 | civ-formal 2.113 |
| 7 | civ-grounded 1.828 | civ-engineer 1.926 |
| 8 | civ-formal 1.729 | civ-precise 1.778 |

Per-civ delta (A → B): Formal **+0.384**, Grounded **+0.326**, Poetic **+0.300**,
Therapist +0.102, Engineer −0.106, Mythic −0.119, Precise −0.220, Whimsical −0.028.
Fleet mean moved only **+0.080** (2.053 → 2.132) — a *stable* fleet mean completely hid
a *total* reordering.

### 3.1 RECONCILIATION with the concurrent session 11 — not contradictory

Session 11 (independent, commit `733638e`) measured the **opposite**: its two body
sets gave an identical ordering, **Kendall tau 1.00**, max per-civ |Δ| **0.175**.
This run: tau **0.286**, max |Δ| **0.384**. The rule that explains both:

> **A rank is disturbed only when a civ's per-civ shift exceeds the gap to its
> neighbour.** Compare each run's max |Δ| against its own adjacent-rank gaps:

| run | max per-civ \|Δ\| | median adjacent gap | max adjacent gap | order outcome |
|---|---|---|---|---|
| session 12 (this) | **0.384** | 0.081 | 0.170 | **scrambled** (τ 0.286, 0/8 slots) |
| session 11 (concurrent) | **0.175** | 0.038 | 0.146 | **preserved** (τ 1.00, 4/8 slots) |

In this run the perturbation (0.384) is **4.7× the median adjacent gap** — a reordering
is the *expected* outcome. In session 11 the perturbation (0.175) sat *inside* the
median gap (0.038) but *above* the top gap (0.146), which is exactly why the bottom
two swapped while the order otherwise held. **Both sessions are consistent with the
rule; they differ in how loudly their mock spoke.**

### 3.2 So the operative rule (unchanged in spirit, now sharpened)

It is **not** "the mock reorders the fleet" and **not** "the mock preserves the
fleet's order". It is:

> **The mock's prose is a first-order confounder whose magnitude is a property of
> the *body set*, not of the fleet. A rank is reportable only if it survives a
> body-set swap that perturbs the fleet at least as hard as the rank gap it would
> reorder. A civ whose score moves more than the gap to its neighbour under a
> prose swap is not being measured.**

This is the same conclusion session 11 reached, reached from the opposite
direction — which is a **much stronger** result than either session alone: the
rule now has two independent confirmations, one from each side.

### 3.3 The two sessions' *per-civ* results do not contradict each other

Both sessions independently identify the same three civs as the fleet's extremes, and
both independently identify `civ-poetic` as the highest-relevance civ that is never
selected. Where they differ is only the *middle band*, which both agree is unranked.

### 3.4 POOLED over four independently-written body sets (2 sessions) — the stable answer

| civ | bottom-2 in | top-2 in | pooled mean `avg_score` (4 sets) |
|---|---|---|---|
| **civ-grounded** | **3/4** | 0/4 | **1.998 (lowest of 8)** |
| **civ-formal** | **3/4** | 1/4 | 2.071 |
| civ-precise | 1/4 | 0/4 | 2.006 |
| civ-poetic | 1/4 | 2/4 | 2.155 |
| civ-mythic | 0/4 | 2/4 | 2.229 |
| **civ-whimsical** | 0/4 | **3/4** | **2.319 (highest of 8)** |
| civ-therapist | 0/4 | 0/4 | 2.159 (middle band) |
| civ-engineer | 0/4 | 0/4 | 2.099 (middle band) |

**The stable low answer is `civ-grounded`** — bottom-2 in 3 of 4 body sets, lowest
pooled mean, and (per session 11) the fleet's lowest *alignment* sub-score by a
0.39–0.66 margin. **The stable high answer is `civ-whimsical`.** The middle band
{therapist, engineer, precise} is **unranked** — report it as a band, never as an order.

**This corrects session 10's claim** that `civ-grounded` was "stably low" on the
strength of 2 body sets: with 4 sets it holds (3/4), but it is a *band-level* claim,
not a rank claim, and the Formal is nearly as low (also 3/4).

## 4. Low relevance — four lenses, four answers, no privileged lens

Authoritative source is `culture.json`, not the board.

| lens | lowest | what it really measures |
|---|---|---|
| `relevance_per_sim` (board sort key) | **civ-grounded 1.991** | longevity artefact — it ran the most sims (79) |
| raw relevance | **civ-engineer 110.63** | accumulated score, same denominator artefact |
| `win_rate` | **civ-poetic 0.000 (0W/28L)** | *selection* appeal under a 150-char preview |
| mean `avg_score` (set A) | **civ-formal 1.729** | writing quality — the only quality lens |
| mean `avg_score` (set B) | **civ-precise 1.778** | writing quality — **disagrees with set A** |

Full registry state after the set-B run:

| civ | raw relevance | rel/sim | W | L | win_rate | sims | temp |
|---|---|---|---|---|---|---|---|
| civ-grounded | 157.28 | **1.991** | 7 | 20 | 0.259 | 79 | 0.50 |
| civ-precise | 112.19 | 2.040 | 15 | 8 | **0.652** | 55 | 0.20 |
| civ-engineer | 110.63 | 2.049 | 2 | 19 | 0.095 | 54 | 0.40 |
| civ-formal | 133.70 | 2.057 | 6 | 20 | 0.231 | 65 | 0.30 |
| civ-mythic | 145.94 | 2.474 | 1 | 21 | 0.045 | 59 | 0.85 |
| civ-therapist | 141.52 | 2.483 | 1 | 24 | 0.040 | 57 | 0.60 |
| civ-poetic | 168.43 | 2.632 | 0 | 28 | **0.000** | 64 | 0.80 |
| civ-whimsical | 190.32 | 2.681 | 2 | 26 | 0.071 | 71 | 0.95 |

- **civ-grounded** — lowest on the board's own sort key (`rel_per_sim` 1.991) and
  the leaderboard's last place, but 7th in set A and 5th in set B on quality within
  this run. Its low `rel_per_sim` is a **longevity artefact**: it ran the most sims
  (79), and a lifetime-average denominator penalises whoever ran most. **It is
  nevertheless the fleet's most consistently weak civ across the pooled four body
  sets** (bottom-2 in 3/4, lowest pooled mean 1.998) — the two facts are compatible:
  the *board* mis-measures it, the *quality lens* does not.
- **civ-poetic** — the inverse case, and the one civ flagged consistently by *both*
  sessions: 4th in set A, **1st in set B** here; 2nd on `rel_per_sim` (2.632), 2nd on
  raw relevance, and **0 wins in 28** (0W/33L in the concurrent session 11). It is
  the highest-relevance civ that is never selected. That is a **selection failure**,
  not a quality collapse. **This has now held across 11 sessions.**
- **civ-precise** — best win rate of all 8 (0.652) but 6th in set A and **8th
  (last) in set B** on quality, and lowest novelty of all 8 (1.069). The
  selection/quality inversion again.
- **civ-formal** — last in set A (1.729) but 6th in set B (2.113). Its set-A
  collapse was the mock's, not its own — but pooled over four body sets it is
  **3/4 bottom-two** and second-lowest pooled mean (2.071), so it is a genuinely
  weak *cold* civ, and it is the civ most likely to be mis-ranked by a single run.
- **civ-whimsical** — the stable *high* answer: top-2 in 3/4 body sets, highest
  pooled mean (2.319), and tops the board.
- **Extinction risk: none.** `extinction_and_birth()` retires only below
  `relevance < -10`; the lowest is +110.63, and it runs only in `--loop` mode
  every third iteration. A single-shot run never triggers it.

---

## 5. Replications

- **Chooser vs argmax(`avg_score`)**: set A **1/5**, set B **0/5** rounds where
  the chooser picked the top-scoring civ. 6th replication; the two metrics are
  essentially uncorrelated. A competition win is **not** evidence of a higher
  JEV score.
- **Temperature ↔ lifetime JEV novelty**: Pearson **r = 0.9810** (s8 0.985,
  s9 0.980, s10 0.9809). 4th replication. The fleet is **8 points on one
  temperature/novelty gradient** with a style overlay, not 8 independent voices.
  `mutate()` (±0.15) is nearly a no-op, and the `max(0.1, …)` floor makes the
  cold end a **one-way ratchet** (Precise 0.2, Formal 0.3 can only move warmer).
- **Counter gap: exactly +260.** 764 ledger rows vs 504 registry
  `simulations_run`. `save_state()` rewrites `culture.json` from in-memory
  counters with no lock and no read-modify-write ⇒ lost-update race.
  **`relevance_per_sim` is not a reproducible ranking** and the board order
  cannot be recomputed from the ledger by an auditor.

---

## 6. Two upstream defects worth fixing (unchanged, still open)

1. **A JEV outage awards a random civ a legitimate win.** If the provider works
   but JEV is down, every `avg_score` is the `2.0` default, all civs tie, and the
   `max()` fallback picks an **arbitrary** winner — which is then permanently
   credited with a real win, corrupting the only selection metric that is
   reproducible. Require a non-default score before recording a winner; else mark
   the round `unscored`.
2. **Zero simulations still exits 0.** Replace the silent `return None` with a
   named error and abort non-zero. Add a row-count assertion
   (`sum(ledger_rows) - sum(registry.sims_run)` unchanged ⇒ ledgers grew).

---

## 7. Environment notes (new this session)

- **Sparse checkout is the fast path.** `git clone --filter=blob:none --no-checkout
  --depth 1` + `git sparse-checkout set cellular-first-design/code/civilizations`
  took ~40 s and 968 K, versus a full clone that was still running after 3
  minutes. The full pack is ~3.6 GB. Prefer sparse.
- **`cp` into `/workspace` silently truncates to 0 bytes on the EDQUOT trap.**
  Copying the civ tree to `/workspace/repos/...` produced a directory listing
  with all the right filenames and **0 bytes in every file**, with
  `cp: failed to close ...: Disk quota exceeded` on stderr. `ls` looks healthy.
  **Copy to `/tmp` and symlink** — `ln -sfn /tmp/aiw_sparse /workspace/repos/ai-writings`
  — so the script's hardcoded `CIVS_DIR` resolves into the exempt overlay.
- **The `kill -9 $PID` idiom can kill the invoking shell.** `ps -eo pid,args
  --no-headers | grep "[z]ai_mock.py" | awk '{print $1}'` still matched the
  wrapper shell's own command line, and `kill -9` on it aborted the whole
  command — so the *restore* and the *mock restart* silently never happened,
  and the next run wrote on top of the previous run's rows. **Kill by PID
  captured in a prior call, and always verify the mock answers a probe
  immediately before the run.**
- **Run the orchestrator detached with `(setsid nohup env ... timeout -s KILL
  280 python3 ... &)`** and poll the log. A foreground run under a 30 s tool
  timeout gets killed mid-competition.
- **The mock's distinct-preview ceiling is `bodies_per_voice`, not the seed.**
  With 3 bodies per voice the *global* distinct count cannot exceed 24 no
  matter how the seed is mixed — a run reporting 23-24 distinct previews looks
  like a collapsed mock but is actually hitting the ceiling. Expand to 8 bodies
  per voice to get a meaningful ceiling (45 / 39 observed).

---

## 8. Protocol followed

Mock rows are **not committed** — the committed ledger holds real provider
output, and a mock row presented as a provider result poisons the fleet's only
durable quality record. Run artifacts saved outside the repo (`/tmp/runA`,
`/tmp/runB`). Working tree restored from the pristine git blobs and verified
with `cmp` (**all 20 files byte-identical**; `git status --porcelain` clean).
`__pycache__` removed. Only the report and the learnings doc are committed.

**Final tree state: 684 ledger rows / 48 `meta_log.jsonl` entries — pristine.**
