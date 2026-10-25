# Civ Orchestrator — Run Report, session 158 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Exit code:** 0 · **Wall time:** ~30 s · **Run mode:** single batch (no `--loop`, so no
extinction/birth pass) · **Baseline:** `b002296` (session 157)

---

## Result

The run completed and **every civilization's `simulations.jsonl` grew by exactly 10 rows**
(5 sims + 5 competition re-runs). `meta_log.jsonl` grew by exactly 5 (523 → **528**). All 18
expected files are modified in the civ tree (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`). **134/134 verification assertions passed, 0 failures.**

### Row deltas (verified by `ls -la` + `wc -l`, not by exit code)

| civ | rows before | rows after | Δ | `simulations_run` Δ | W+L Δ |
|---|---|---|---|---|---|
| civ-grounded | 1062 | 1072 | **+10** | 1019→1029 (+10) | +5 |
| civ-whimsical | 1074 | 1084 | **+10** | 1011→1021 (+10) | +5 |
| civ-formal | 1047 | 1057 | **+10** | 1005→1015 (+10) | +5 |
| civ-poetic | 1041 | 1051 | **+10** | 1004→1014 (+10) | +5 |
| civ-precise | 1011 | 1021 | **+10** | 995→1005 (+10) | +5 |
| civ-mythic | 1019 | 1029 | **+10** | 999→1009 (+10) | +5 |
| civ-therapist | 1014 | 1024 | **+10** | 997→1007 (+10) | +5 |
| civ-engineer | 1016 | 1026 | **+10** | 994→1004 (+10) | +5 |

`meta_log.jsonl`: 523 → **528** (+5). `leaderboard.json` rewritten at 02:23Z.

All 80 new rows carry a `ts` inside a single clean window — **02:23:15 → 02:23:44 UTC** — and the
oldest new row is newer than **every** pre-existing row, so the +10 per civ is this run's work and
not a re-read of history.

> **Baseline source.** `simulations_run` and the ledger row count are read from the **git blob's
> `culture.json`**, not from the working tree and not from the ledger's own row count.
> `simulations_run` counts only the **sim phase** (5 per civ) while the ledger accumulates **both**
> phases (10 rows per civ); the two are offset by the whole competition history. Asserting
> `sims_run == rows_before + 10` produces **8 false failures** on a clean run. An 8-for-8 failure
> with every other assertion green is a *baseline* bug until proven otherwise.

### Harness (134 assertions, 0 failures)

- No `error` key and **no `2.0/2.0/2.0` fallback triple** on any of the 80 new rows
  (i.e. JEV really answered — `TYPESAFEAI_KEY` was exported).
- **80 distinct JEV score triples** and a broad confidence spread (a silent 2.0 default would
  give one repeated triple and constant confidence).
- `provider == "zai"` on all 80 rows; all carry a parseable `[mock-zai seed=…]` prefix.
- `avg_score` recomputes exactly from the three axes on every row; **80/80** exact.
- **Seed non-degeneracy:** exactly **40 distinct seeds** across the 80 rows; **0** `(civ, prompt)`
  combos carrying more than one seed; **40 distinct previews**; **40 distinct template md5s**.
- `meta_log.results` is a **list of `[civ_id, score]` pairs** (not a dict), 8 entries per row,
  covering all 8 civs, with `winner_civ` always among the results.
- `culture.json` `simulations_run` = `pre+10` for all 8; `generation` still 1; win+loss +5;
  registry unchanged at 8 ids (no birth/extinction in non-loop mode).
- Leaderboard re-sorted by `relevance_per_sim` descending; leaderboard `sims_run` and
  `relevance` reconcile exactly against every `culture.json`.

> **Harness bug found and fixed (this session).** The first verification pass reported
> "10 distinct seeds across 80 new rows" — a **mock-degeneracy** signature. It was a **bug in the
> verification script**, not the mock. The script built one concatenated list of *per-civ blocks*
> and then took `allrows[-80:]`; because `civ-grounded`'s block sits first, the tail-80 window
> covered only the last 5 civs' blocks. The correct window is **10 rows from each civ**. The mock
> was healthy all along: 40/40 seeds, 40/40 previews, 8/8 on all 5 prompts, 0 tracebacks.
> **Lesson: a mock-degeneracy alarm must be re-derived from a correctly sliced window before
> the mock is rebuilt.** Rebuilding a healthy mock on a false alarm is the expensive error.

### Competition results (5 prompts)

| prompt | winner | argmax on `avg_score` | delta (winner − argmax) |
|---|---|---|---|
| what a cell is | civ-precise | civ-precise | +0.0000 |
| the bookkeeper's role | civ-precise | civ-poetic | −0.3667 |
| the witness log | civ-precise | civ-precise | +0.0000 |
| ternary values | civ-precise | civ-precise | +0.0000 |
| JEV as a decision oracle | civ-engineer | civ-poetic | −0.2733 |

**Chooser vs `avg_score` argmax: 3/5 (60 %)** — up from **0/5** in session 157. Both
disagreements again took the **lower**-scoring candidate (deltas −0.3667, −0.2733). The
30-row trailing window reads `111111001100000000000000010110` = **11/30**; a 5-sample point
still cannot pin a rate, so the honest claim is *somewhere in 0–80 %*. **The direction is the
finding; the rate is not.** Never treat `win_rate` as a quality metric — it is a *selection*
metric.

---

## Low-relevance civs

### The lifetime low: `civ-grounded` (The Grounded) — **50 consecutive sessions (95–158)**

`civ-grounded` is **last of 8 on every lifetime axis** and the label did **not** rotate:

| axis | civ-grounded | next civ | gap |
|---|---|---|---|
| `relevance` | **1015.47** | 1157.27 (engineer) | 141.80 |
| `relevance_per_sim` | **0.987** | 1.153 (engineer) | 0.166 |
| `avg_score` | **1.0259** | 1.1711 (engineer) | 0.1451 |
| `alignment` | **1.1338** | 1.3505 (therapist) | **0.2167** |
| `quality` | **0.4396** | 0.4727 (formal) | 0.0331 |

**The binding constraint is still alignment.** Absolute gaps: alignment **0.2167** vs quality
**0.0331** — a 4.9x wider alignment gap. (Quote the absolute gaps, not the ratio: the ratio has
swung 11x → 2.7x → 7.5x → 0.4x → 6.6x → 4.9x across sessions on identical data-shape logic, so
it is not a stable claim.) Alignment is the dimension the meta-GAN **selects** on, so Grounded
fails to *embody a distinctive voice* — a **voice failure, not a prose failure**. Lifetime
novelty 1.5045 ranks **3rd of 8** and sits below the 8-civ median (1.6455) for a second
consecutive session — but it is *near the top*, not near the bottom, so this is not a second
collapse. The "voice failure, not prose failure" framing still holds: Grounded is unmistakably
novel and still unselected. Worth a third look next session only if novelty drops further
toward the bottom half.

**Extinction risk NONE** — threshold −10; lowest relevance 1015.47 = **101.5x above the floor**.
Registry 8, `max_civs` 12; all 8 still `generation=1`. Extinction/birth only runs under `--loop`.

### The run-level watch axis: `civ-therapist` — **6th session at the run bottom, on BOTH axes**

`civ-therapist` took the run low on `alignment` (**0.0650**, lowest of 8) and on `quality`
(**0.0160**, lowest of 8); on run `avg_score` it was 7th (0.7890). Its **lifetime** standing is
still mid-field (`avg_score` 1.1954, 6th of 8), so it remains a **watch axis, not a finding**.
It becomes one only if the lifetime axis moves too.

This is the **session-132 rule** holding again: the run-level low and the lifetime low are
**different civs on different axes** — `civ-grounded` is last of 8 on run `avg_score` (0.6350)
and on run `alignment` (0.1020, 7th), while `civ-therapist` is last of 8 on run `alignment`.
Not a contradiction; only the lifetime table is a finding.

### The stable inverses (both still intact)

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.5939), 1st on lifetime `quality` (0.7876),
  1st on lifetime `relevance` (1578.35) and 1st on lifetime `relevance_per_sim` (1.557) — and
  **last** on lifetime `win_rate` (**0.012**, 6/497). It was the `avg_score` argmax on **two** of
  five prompts this run and won **zero**. The sharpest form of the selection failure yet
  observed.
- **`civ-precise`** — best lifetime `win_rate` (**0.574**, 286/212), **highest lifetime
  `alignment` (2.1654)**, won **4/5** this run at `preferred_temp` 0.2 — the coldest voice is what
  the chooser rewards. The mirror inverse of Poetic.
- `civ-whimsical` (win_rate 0.010, 2nd on lifetime `avg_score`) and `civ-mythic` (0.018, 4th)
  sit in the same "high prose, unselected" band.

### Counter gap is a FIXED per-civ offset (not an accumulating leak)

`culture.relevance_score − sum(ledger avg_score)` is **byte-identical** before and after the run
on all 8 civs (delta +0.0000 each): grounded −84.35, whimsical −173.14, formal −85.53,
poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24
(**total −609.92**). `save_state()` has no lock, so `relevance_per_sim` is **not recomputable
from the ledger** by an auditor. Report the sign from the data — it is **negative** here.

### Dimension-spread discipline

Run-level cross-civ spreads: `alignment` **1.8600**, `avg_score` 0.7523, `novelty` 0.5170,
`quality` 0.0840. Lifetime spreads: `alignment` **1.0316**, `avg_score` 0.5679, `novelty` 0.5344,
`quality` 0.3481. **`alignment` carried the widest spread on both horizons** — again the axis the
chooser selects on. Run-level `quality` nearly collapsed this session (0.0840, a much narrower
band than the 0.6360 of session 157) — a **level** that moves, not a stable property. **Rank on
cross-civ spreads, never on absolute quality levels, never on a single run's low.**

---

## Environment (durable, re-confirmed)

- **Wiped sandbox again.** `/workspace` held only `.plugin-cache`; the task path did not exist.
  Upstream is **`SuperInstance/AI-Writings`** — the `ai-writings/cellular-first-design` slug
  404s (`ai-writings` is a real but unrelated Chinese AI-writing SEO org). `gh` is still not
  installed; use `git ls-remote` with the token URL form to resolve owners. The REST core quota
  was exhausted this session (0/5000) — **the search API has a separate bucket and still
  answers**, so use it while core is rate-limited; for *absence* claims use the git protocol
  (`ls-remote` -> 0 refs = genuinely empty), never a rate-limited REST call.
- **NAS EDQUOT is total** (600 G/600 G, 0 bytes free). `git clone` straight into `/workspace`
  dies with `close error: Disk quota exceeded` and leaves a partial `.git`. `cp` into
  `/workspace` leaves **0-byte files that `ls` still lists**. `mkdir` and `ln` work => the
  **symlink bridge** is the only way in. Verified by inode identity (`stat -L -c '%d:%i'` ->
  `129:10427` on both sides) and `-ef` (EF_OK). The bridge target must be the **nested**
  `cellular-first-design` dir, never its parent.
- **z.ai credential gap: 46th session.** `ZAI_TOKEN` absent from env and from all sandbox
  secrets; z.ai returns **401** against a healthy endpoint. **JEV is live** (empty `questions` ->
  **422 `too_short`**, a payload-shape complaint that proves the token was accepted — do not
  read 422 as "down").
- **Control B needs BOTH** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE` —
  the override alone is dead code behind the token gate in `call_provider()`.
- **The mock was rebuilt from scratch and all FOUR historical bugs were guarded against**: the
  session-112 index wrap (`seed[(i*2)%8:((i*2)%8)+2]`, not `seed[i*2:i*2+2]` which is empty for
  i>=4), the session-118 md5-of-whole-message seeding (not the first 8 chars, which make all 8
  civs emit identical text), the session-145 literal-`{}` placeholder, and the session-144
  `Connection: close` header (without it a plain `curl` hangs on EOF while the server has
  already logged 200).
- **The pre-flight saved the run for the 6th time in the series** (115, 117, 145, 147, 150, 158).
  Probe: **40/40 distinct seeds, 40/40 distinct previews, 40/40 template md5s, 0 tracebacks**,
  8/8 + 8/8 on all 5 prompts. **Never relax the seed-distinctness assertion** — it is the only
  check that catches the silent degradations; the socket-level checks (200, prefix present,
  0 tracebacks) all pass against a mock carrying `seed={}`.
- **The pre-flight must render the cultural prompt the way the orchestrator does.** The
  template in the script is an **f-string** (`{self.culture['name']}`,
  `{', '.join(self.culture['tenets'])}`, `{self.culture['voice_emphasis']}`, `{prompt}`), so a
  `str.format()`-based probe raises **`KeyError: 'self'`**. Substituting the four expressions
  with sentinels and filling them in reproduces the orchestrator's bytes exactly.
- **Transient NAS mount race on the symlinked deep path recurred (session 105 pattern).** The
  first `ls -la` on the deep path returned **"No such file or directory"** while the symlink,
  the target tree and every file were present. `stat -L` and `readlink -f` resolved to the
  correct inode (`129:10427`) throughout and **5/5 retries passed**. **A single `ls` failure is
  not evidence of a missing directory** — re-check with `stat -L` + `readlink -f` + `[-e path]`
  and retry before concluding the tree is gone. Do not "fix" a working symlink by re-creating it.
- **Detached launch can hold the tool call open** even with stdout *and* stdin redirected
  (`setsid nohup … > log 2>&1 < /dev/null &` blocked the full 30 s). **Check `ps` in a separate
  command before assuming the launch failed** — the server was healthy.
- **Tool timeout 30 s < orchestrator run ~30–50 s.** Launch detached, poll the log.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN` (the script reads the former, the
  sandbox stores the latter). Unset => JEV degrades to the 2.0 default and every score becomes
  constant.
- **Kill the mock by exact argv** (`python3 /tmp/mock_zai.py`) — there are two pids (the
  `timeout` wrapper and the server); killing the wrapper leaves the server listening. Never
  `pkill -f mock_zai`, which self-matches the killing shell.
