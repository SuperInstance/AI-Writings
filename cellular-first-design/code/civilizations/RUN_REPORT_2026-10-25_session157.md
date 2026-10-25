# Civ Orchestrator — Run Report, session 157 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Exit code:** 0 · **Wall time:** ~30 s · **Run mode:** single batch (no `--loop`, so no
extinction/birth pass) · **Baseline:** `3a56fa0` (session 156)

---

## Result

The run completed and **every civilization's `simulations.jsonl` grew by exactly 10 rows**
(5 sims + 5 competition re-runs). `meta_log.jsonl` grew by exactly 5 (518 → **523**). All 18
expected files are modified in the civ tree (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`). **103/103 verification assertions passed, 0 failures.**

### Row deltas (verified by `ls -la` + `wc -l`, not by exit code)

| civ | rows before | rows after | Δ | `simulations_run` Δ | W+L Δ |
|---|---|---|---|---|---|
| civ-grounded | 1052 | 1062 | **+10** | 1009→1019 (+10) | +5 |
| civ-whimsical | 1064 | 1074 | **+10** | 1001→1011 (+10) | +5 |
| civ-formal | 1037 | 1047 | **+10** | 995→1005 (+10) | +5 |
| civ-poetic | 1031 | 1041 | **+10** | 994→1004 (+10) | +5 |
| civ-precise | 1001 | 1011 | **+10** | 985→995 (+10) | +5 |
| civ-mythic | 1009 | 1019 | **+10** | 989→999 (+10) | +5 |
| civ-therapist | 1004 | 1014 | **+10** | 987→997 (+10) | +5 |
| civ-engineer | 1006 | 1016 | **+10** | 984→994 (+10) | +5 |

`meta_log.jsonl`: 518 → **523** (+5). `leaderboard.json` iso `01:46:04` → **`01:57:07`**.

`ls -la` on the civ tree shows all 8 ledgers with mtime **01:57** (clone time was 01:55),
confirming the new rows are on disk at the bridged path.

> **Baseline correction (this session).** The `simulations_run` baseline must be read from the
> **git blob's `culture.json`**, not from the ledger's row count. `simulations_run` counts only
> the **sim phase** (5 per civ) while the ledger accumulates **both** phases (10 rows per civ),
> and the two numbers are offset by the whole competition history. Asserting `sims_run ==
> rows_before + 10` produces **8 false failures** on a clean run. An 8-for-8 failure with every
> other assertion green is a *baseline* bug until proven otherwise — check the baseline source
> before believing the failure.

### Harness (103 assertions, 0 failures)

- No `error` key and **no `2.0/2.0/2.0` fallback triple** on any of the 80 new rows
  (i.e. JEV really answered — `TYPESAFEAI_KEY` was exported).
- **80 distinct JEV score triples** and **35 distinct confidences** (a silent 2.0 default would
  give one repeated triple and constant confidence).
- `provider == "zai"` on all 80 rows; all carry a parseable `[mock-zai seed=…]` prefix.
- `avg_score` recomputes exactly from the three axes on every row; **80/80** exact.
- **Seed non-degeneracy:** exactly **40 distinct seeds** across the 80 rows; **0** `(civ, prompt)`
  combos carrying more than one seed.
- **8/8 distinct seeds AND 8/8 distinct previews on all 5 competition prompts.**
- `meta_log.results` is a **list of `[civ_id, score]` pairs** (not a dict), 8 entries per row,
  covering all 8 civs, with `winner_civ` always among the results.
- `culture.json` `simulations_run` = `pre+10` for all 8; `generation` still 1; win+loss +5;
  registry unchanged at 8 ids (no birth/extinction in non-loop mode).
- Leaderboard re-sorted by `relevance_per_sim` descending; leaderboard `sims_run` and
  `relevance` reconcile exactly against every `culture.json`.

### Competition results (5 prompts)

| prompt | winner | argmax on `avg_score` | delta (winner − argmax) |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | −0.4533 |
| the bookkeeper's role | civ-precise | civ-poetic | −0.5133 |
| the witness log | civ-precise | civ-poetic | −0.1867 |
| ternary values | civ-precise | civ-poetic | −0.5200 |
| JEV as a decision oracle | civ-formal | civ-poetic | −0.6300 |

**Chooser vs `avg_score` argmax: 0/5 (0 %)** — agreement 0/5, winners `civ-precise` x4,
`civ-formal` x1. `civ-poetic` was the argmax on **all five** prompts and won **none** of them.

---

## Low-relevance civs

### The lifetime low: `civ-grounded` (The Grounded) — **49 consecutive sessions (95–157)**

`civ-grounded` is **last of 8 on every lifetime axis** and the label did **not** rotate:

| axis | civ-grounded | next civ | gap |
|---|---|---|---|
| `relevance` | **1009.12** | 1147.82 (engineer) | 138.70 |
| `relevance_per_sim` | **0.990** | 1.155 (engineer) | 0.165 |
| `avg_score` | **1.0296** | 1.1733 (engineer) | 0.1437 |
| `alignment` | **1.1435** | 1.3632 (therapist) | **0.2197** |
| `quality` | **0.4435** | 0.4768 (formal) | 0.0333 |

**The binding constraint is still alignment.** Absolute gaps: alignment **0.2197** vs quality
**0.0333** — a **6.6×** wider alignment gap. (Quote the absolute gaps, not the ratio: the ratio
has swung 11× → 2.7× → 7.5× → 0.4× → 6.6× across sessions on identical data-shape logic, so
it is not a stable claim.) Alignment is the dimension the meta-GAN **selects** on, so Grounded
fails to *embody a distinctive voice* — a **voice failure, not a prose failure**. Lifetime
novelty 1.5018 is **below** median (1.6410) this session — a change from sessions 143–150, where
Grounded's novelty sat *above* median. Worth a second look next session: if novelty has dropped
below median permanently, Grounded is losing on *two* axes rather than one.

**Extinction risk NONE** — threshold −10; lowest relevance 1009.12 = **100.9× above the floor**.
Registry 8, `max_civs` 12; all 8 still `generation=1`. Extinction/birth only runs under `--loop`.

### The run-level watch axis: `civ-therapist` — **5th session at the run bottom, on BOTH axes**

`civ-therapist` took the run low on `avg_score` (**0.7893**) *and* on `alignment` (**0.6760**),
both lowest of 8. Its **lifetime** standing is still mid-field (`avg_score` 1.1994, 6th of 8),
so it remains a **watch axis, not a finding**. It becomes one only if the lifetime axis moves too.

This is the **session-132 rule** holding again: the run-level low and the lifetime low are
**different civs on different axes** — `civ-grounded` is 7th of 8 on run `avg_score` (0.8997)
while `civ-therapist` is 6th of 8 on lifetime `avg_score`. Not a contradiction; only the
lifetime table is a finding.

`civ-formal` took the run-level low on **quality** (0.0930) and **novelty** (1.3940) — its
lifetime identity as the low-novelty axis (lifetime novelty 1.4045, last of 8) reasserted itself.

### The stable inverses (both still intact)

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.5961), 1st on lifetime `quality` (0.7942),
  1st on lifetime `relevance` (1564.74) and 1st on lifetime `relevance_per_sim` (1.559) — and
  **last** on lifetime `win_rate` (**0.012**, 6/498). It was the `avg_score` argmax on **all five**
  prompts this run and won **zero**. The sharpest form of the selection failure yet observed.
- **`civ-precise`** — best lifetime `win_rate` (**0.572**), **highest lifetime `alignment`
  (2.1678)**, won **4/5** this run at `preferred_temp` 0.2 — the coldest voice is what the
  chooser rewards. The mirror inverse of Poetic.
- `civ-whimsical` (win_rate 0.010, 2nd on `avg_score`) and `civ-mythic` (0.018, 4th) sit in the
  same "high prose, unselected" band.

**Chooser vs argmax: 0/5 (0 %)** — the chooser disagreed in **every** competition, and **all
five** disagreements took the **lower**-scoring candidate (deltas −0.1867 … −0.6300). Clean-mock
series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) →
4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) → 2/5 (132) → 2/5 (133) →
0/5 (134) → 4/5 (136) → 1/5 (137) → 1/5 (138) → 1/5 (139) → 4/5 (144) → 4/5 (146) → 0/5 (147) →
… → **0/5 (157)**. Twenty-plus five-sample points **cannot** pin a rate; the honest claim is
*somewhere in 0–80 %*. **The direction is the finding; the rate is not.** Never treat
`win_rate` as a quality metric — it is a *selection* metric.

### Counter gap is a FIXED per-civ offset (not an accumulating leak)

`culture.relevance_score − sum(ledger avg_score)` is **byte-identical** before and after the run
on all 8 civs (delta +0.0000 each): grounded −84.35, whimsical −173.14, formal −85.53,
poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24
(**total −609.92**). `save_state()` has no lock, so `relevance_per_sim` is **not recomputable
from the ledger** by an auditor. Report the sign from the data — it is **negative** here.

### Dimension-spread discipline

Run-level cross-civ spreads: `alignment` **1.7070**, `avg_score` 0.8880, `quality` 0.6360,
`novelty` 0.5260. Lifetime spreads: `alignment` **1.0243**, `avg_score` 0.5665, `novelty` 0.5387,
`quality` 0.3507. **`alignment` carried the widest spread on both horizons** — again the axis the
chooser selects on. Run-level `quality` did **not** collapse this session (0.093–0.729, a much
wider band than the 0.007–0.052 band of sessions 142–156), which is a **level** that moves, not a
stable property. **Rank on cross-civ spreads, never on absolute quality levels, never on a
single run's low.**

---

## Environment (durable, re-confirmed)

- **Wiped sandbox again.** `/workspace` held only `.plugin-cache`; the task path did not exist.
  Upstream is **`SuperInstance/AI-Writings`** — the `ai-writings/cellular-first-design` slug
  404s (`ai-writings` is a real but unrelated Chinese AI-writing SEO org with 4 repos).
  `gh` is still not installed; `GET /search/repositories?q=user:SuperInstance` identifies the
  owner. The REST core quota was exhausted this session (0/5000, reset 02:21Z) — **the search
  API has a separate bucket and still answers**, so use it while core is rate-limited.
- **`/tmp` was reaped mid-session.** A completed clone (`/tmp/aiw`, 6.7 MB sparse) vanished
  between two commands, leaving the symlink bridge dangling and `ls` failing with
  "No such file or directory" on the *target*, not the link. **A vanished `/tmp` looks exactly
  like a broken bridge — re-check the target before re-creating the link.** Re-cloned with the
  blobless+sparse recipe: `--filter=blob:none --no-checkout --depth 1 --sparse` +
  `git sparse-checkout set --no-cone cellular-first-design/code/civilizations` → **6.7 MB**.
- **NAS EDQUOT is total** (600 G/600 G, 0 bytes free). `git clone` straight into `/workspace`
  dies with `close error: Disk quota exceeded` and leaves a partial `.git`; `cp` into
  `/workspace` leaves **0-byte files that `ls` still lists**. `mkdir` and `ln` work ⇒ the
  **symlink bridge** is the only way in. Verified by inode identity (`stat -L -c '%d:%i'` →
  `129:7764` on both sides) and `-ef` (EF_OK). The bridge target must be the **nested**
  `cellular-first-design` dir, never its parent.
- **z.ai credential gap: 45th session.** `ZAI_TOKEN` absent from env and from all 8 sandbox
  secrets; z.ai returns **401 `token expired or incorrect`** against a healthy endpoint.
  **JEV is live** (empty `questions` → **422 `too_short`**, a payload-shape complaint that
  proves the token was accepted — do not read 422 as "down").
- **Control B needs BOTH** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE` —
  the override alone is dead code behind the token gate in `call_provider()`.
- **The mock was rebuilt from scratch and all FOUR historical bugs were live again** in the
  naive rebuild: the session-112 index wrap (`seed[(i*2)%8:((i*2)%8)+2]`, not `seed[i*2:i*2+2]`
  which is empty for i≥4 → HTTP 500 with the socket still open), the session-118
  md5-of-whole-message seeding (not the first 8 chars, which make all 8 civs emit identical
  text), the session-145 literal-`{}` placeholder (every response carrying `seed={}` → 1
  distinct seed instead of 40), and the session-144 `Connection: close` header (without it a
  plain `curl` hangs on EOF while the server has already logged 200).
- **The pre-flight saved the run for the 5th time in the series** (115, 117, 145, 147, 150).
  Probe: **40/40 distinct seeds, 40/40 distinct previews, 40/40 template md5s, 0 tracebacks**,
  prompt lengths 167–209, **8/8 + 8/8 on all 5 prompts**. **Never relax the seed-distinctness
  assertion** — it is the only check that catches the silent degradations; the socket-level
  checks (200, prefix present, 0 tracebacks) all pass against a mock carrying `seed={}`.
- **The pre-flight must render the cultural prompt the way the orchestrator does.** The
  template in the script is an **f-string** (`{self.culture['name']}`,
  `{', '.join(self.culture['tenets'])}`, `{self.culture['voice_emphasis']}`, `{prompt}`), so a
  `str.format()`-based probe raises **`KeyError: 'self'`**. Substituting the four expressions
  with sentinels and filling them in reproduces the orchestrator's bytes exactly.
- **Detached launch can hold the tool call open** even with stdout *and* stdin redirected
  (`setsid nohup … > log 2>&1 < /dev/null &` blocked the full 30 s). **Check `ps` in a separate
  command before assuming the launch failed** — the server was healthy.
- **Tool timeout 30 s < orchestrator run ~50 s.** Launch detached, poll the log.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN` (the script reads the former, the
  sandbox stores the latter). Unset ⇒ JEV degrades to the 2.0 default and every score becomes
  constant.
