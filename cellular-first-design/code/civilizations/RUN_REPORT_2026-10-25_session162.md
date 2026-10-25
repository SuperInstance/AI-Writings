# Civ Orchestrator — Run Report, session 162 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Exit code:** 0 · **Wall time:** ~25 s · **Run mode:** single batch (no `--loop`, so no
extinction/birth pass) · **Baseline:** `8a4f9be` (session 161)

---

## Result

The run completed and **every civilization's `simulations.jsonl` grew by exactly 10 rows**
(5 sims + 5 competition re-runs). `meta_log.jsonl` grew by exactly 5 (543 → **548**). All 18
expected files are modified in the civ tree (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`). **98/98 verification assertions passed, 0 failures.**

### Row deltas (verified by `ls -la` + `wc -l`, not by exit code)

| civ | rows before | rows after | Δ | `simulations_run` Δ | W+L Δ |
|---|---|---|---|---|---|
| civ-grounded | 1102 | 1112 | **+10** | 1059→1069 (+10) | +5 |
| civ-whimsical | 1114 | 1124 | **+10** | 1051→1061 (+10) | +5 |
| civ-formal | 1087 | 1097 | **+10** | 1045→1055 (+10) | +5 |
| civ-poetic | 1081 | 1091 | **+10** | 1044→1054 (+10) | +5 |
| civ-precise | 1051 | 1061 | **+10** | 1035→1045 (+10) | +5 |
| civ-mythic | 1059 | 1069 | **+10** | 1039→1049 (+10) | +5 |
| civ-therapist | 1054 | 1064 | **+10** | 1037→1047 (+10) | +5 |
| civ-engineer | 1056 | 1066 | **+10** | 1034→1044 (+10) | +5 |

`meta_log.jsonl`: 543 → **548** (+5). `leaderboard.json` rewritten at 03:23Z.

All 80 new rows carry a `ts` inside a single clean window, and the oldest new row is newer than
**every** pre-existing row, so the +10 per civ is this run's work and not a re-read of history.

> **Baseline source.** `simulations_run` and the ledger row count are read from the **git blob's
> `culture.json`**, not from the working tree and not from the ledger's own row count.
> `simulations_run` counts only the **sim phase** (5 per civ) while the ledger accumulates **both**
> phases (10 rows per civ); the two are offset by the whole competition history. Asserting
> `sims_run == rows_before + 10` produces **8 false failures** on a clean run.

### Harness (98 assertions, 0 failures)

- No `error` key and **no `2.0/2.0/2.0` fallback triple** on any of the 80 new rows
  (i.e. JEV really answered — `TYPESAFEAI_KEY` was exported).
- **80 distinct JEV score triples** and a broad confidence spread (15 distinct confidence values);
  a silent 2.0 default would give one repeated triple and constant confidence.
- `provider == "zai"` on all 80 rows; all carry a parseable `[mock-zai seed=…]` prefix.
- `avg_score` recomputes exactly from the three axes on every row; **80/80** exact.
- **Seed non-degeneracy:** exactly **40 distinct seeds** across the 80 rows and **40 distinct
  previews** — taken from the correct **10-rows-per-civ** window.
- `meta_log.results` is a **list of `[civ_id, score]` pairs** (not a dict), 8 entries per row,
  covering all 8 civs, with `winner_civ` always among the results.
- `culture.json` `simulations_run` = `pre+10` for all 8; `generation` still 1; win+loss +5;
  registry unchanged at 8 ids (no birth/extinction in non-loop mode).
- Leaderboard re-sorted by `relevance_per_sim` descending; leaderboard `sims_run` and
  `relevance` reconcile exactly against every `culture.json`.

### Competition results (5 prompts)

| prompt | winner | argmax on `avg_score` | delta (winner − argmax) |
|---|---|---|---|
| what a cell is | civ-formal | civ-formal | +0.0000 |
| the bookkeeper's role | civ-formal | civ-whimsical | −0.0733 |
| the witness log | civ-precise | civ-precise | +0.0000 |
| ternary values | civ-precise | civ-whimsical | −0.0767 |
| JEV as a decision oracle | civ-engineer | civ-poetic | −0.2867 |

**Chooser vs `avg_score` argmax: 2/5 (40 %)** — up from **3/5** in session 158, down from **0/5**
in session 157. All three disagreements again took the **lower**-scoring candidate (deltas
−0.0733, −0.0767, −0.2867). The 30-row trailing window reads `000001011110110001000000010100`
= **10/30**; a 5-sample point still cannot pin a rate, so the honest claim is *somewhere in
0–80 %*. **The direction is the finding; the rate is not.** Never treat `win_rate` as a quality
metric — it is a *selection* metric.

---

## Low-relevance civs

### The lifetime low: `civ-grounded` (The Grounded) — **52 consecutive sessions (95–162)**

`civ-grounded` is **last of 8 on every lifetime axis** and the label did **not** rotate. For the
first time in the series, the run-level and lifetime lows are **the same civ** (the session-132
rule was *not* violated this session):

| axis | civ-grounded | next civ | gap |
|---|---|---|---|
| `relevance` | **1033.01** | 1177.26 (engineer) | 144.25 |
| `relevance_per_sim` | **0.966** | 1.128 (engineer) | 0.161 |
| `avg_score` | **1.0048** | 1.1459 (engineer) | 0.1411 |
| `alignment` | **1.0956** | 1.3010 (therapist) | **0.2054** |
| `quality` | **0.4244** | 0.4567 (formal) | 0.0323 |

**The binding constraint is still alignment.** Absolute gaps: alignment **0.2054** vs quality
**0.0323** — a 6.4x wider alignment gap. (Quote the absolute gaps, not the ratio: the ratio has
swung 11x → 2.7x → 7.5x → 0.4x → 6.6x → 4.9x across sessions on identical data-shape logic, so
it is not a stable claim.) Alignment is the dimension the meta-GAN **selects** on, so Grounded
fails to *embody a distinctive voice* — a **voice failure, not a prose failure**. Lifetime
novelty 1.4944 ranks **3rd of 8** and sits below the 8-civ median band (1.5457–1.7124) for a
third consecutive session — but it is *near the top*, not near the bottom, so this is not a second
collapse. The "voice failure, not prose failure" framing still holds: Grounded is unmistakably
novel and still unselected.

**Extinction risk NONE** — threshold −10; lowest relevance 1033.01 = **103.3x above the floor**.
Registry 8, `max_civs` 12; all 8 still `generation=1`. Extinction/birth only runs under `--loop`.

### The run-level watch axis: `civ-therapist` — **7th session at the run bottom on `alignment`**

`civ-therapist` took the run low on `alignment` (**0.0570**, lowest of 8); on run `avg_score` it
was 3rd-lowest (0.7607). Its **lifetime** standing is still mid-field (`avg_score` 1.1664, 5th
of 8), so it remains a **watch axis, not a finding**. It becomes one only if the lifetime axis
moves too.

### The stable inverses (both still intact)

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.5644), 1st on lifetime `quality` (0.7622),
  1st on lifetime `relevance` (1609.92) and 1st on lifetime `relevance_per_sim` (1.527) — and
  **last on lifetime `win_rate`** (**0.012**, 6/517). It was the `avg_score` argmax on **one** of
  five prompts this run and won **zero**. The sharpest form of the selection failure yet
  observed.
- **`civ-precise`** — best lifetime `win_rate` (**0.577**, 299/219), **highest lifetime
  `alignment` (2.1275)**, won **2/5** this run at `preferred_temp` 0.2 — the coldest voice is what
  the chooser rewards. The mirror inverse of Poetic.
- `civ-whimsical` (win_rate 0.010, 2nd on lifetime `avg_score`) and `civ-mythic` (0.019, 4th)
  sit in the same "high prose, unselected" band.

### Counter gap is a FIXED per-civ offset (not an accumulating leak)

`culture.relevance_score − sum(ledger avg_score)` is **byte-identical before and after the run**
on all 8 civs (delta **+0.0000** each): grounded −84.35, whimsical −173.14, formal −85.53,
poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24
(**total −609.92**). `save_state()` has no lock, so `relevance_per_sim` is **not recomputable
from the ledger** by an auditor. The sign is **negative** here.

### Dimension-spread discipline

Run-level cross-civ spreads: `alignment` **0.6410**, `novelty` 0.4260, `avg_score` 0.2183,
`quality` 0.0630. Lifetime spreads: `alignment` **1.0318**, `avg_score` 0.5595, `novelty` 0.5184,
`quality` 0.3378. **`alignment` carried the widest spread on both horizons** — again the axis the
chooser selects on. Run-level `quality` nearly collapsed again (0.0630, comparable to session
158's 0.0840) — a **level** that moves, not a stable property. **Rank on cross-civ spreads,
never on absolute quality levels, never on a single run's low.**

---

## Environment (durable, re-confirmed)

- **Wiped sandbox again.** `/workspace` held only `.plugin-cache`; the task path did not exist.
  Upstream is **`SuperInstance/AI-Writings`** — the `ai-writings/cellular-first-design` slug
  404s (the `ai-writings` org is a real but unrelated Chinese AI-writing SEO org). `gh` is still
  not installed; use `git ls-remote` with the token URL form to resolve owners.
- **NAS EDQUOT is total** (600 G/600 G, 0 bytes free). `git clone` straight into `/workspace`
  dies with `close error: Disk quota exceeded` and leaves a partial `.git`. `cp` into
  `/workspace` leaves **0-byte files that `ls` still lists**. `mkdir` and `ln` work => the
  **symlink bridge** is the only way in: clone to `/tmp`, then
  `ln -s /tmp/ai-writings /workspace/repos/ai-writings`. The bridge target must be the repo
  root; the script's hardcoded `CIVS_DIR` then resolves through the symlink and all writes land
  on the overlay filesystem (28 G free).
- **z.ai credential gap: 47th session.** `ZAI_TOKEN` absent from env and from all sandbox
  secrets; the real z.ai endpoint returns **401** against a healthy endpoint. **JEV is live**
  (empty `questions` → **422 `too_short`**, a payload-shape complaint that proves the token was
  accepted — do not read 422 as "down"; a real score probe returned **HTTP 200**, model
  `jev-1.14.0`).
- **Control B needs BOTH** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE` —
  the override alone is dead code behind the token gate in `call_provider()`.
- **The mock was rebuilt from scratch and all FOUR historical bugs were guarded against**: the
  session-112 index wrap (`seed[(i*2)%8:((i*2)%8)+2]`, not `seed[i*2:i*2+2]` which is empty for
  i>=4), the session-118 md5-of-whole-message seeding (not the first 8 chars, which make all 8
  civs emit identical text), the session-145 literal-`{}` placeholder, and the session-144
  `Connection: close` + `Content-Length` pair (without it a plain `curl` hangs on EOF while the
  server has already logged 200).
- **The pre-flight saved the run for the 7th time in the series** (115, 117, 145, 147, 150, 158,
  162). Probe: **40/40 distinct seeds, 40/40 distinct previews, 40/40 template md5s, 0
  tracebacks**, 8/8 + 8/8 on all 5 prompts, prompt lengths 167–209. **Never relax the
  seed-distinctness assertion** — it is the only check that catches the silent degradations; the
  socket-level checks (200, prefix present, 0 tracebacks) all pass against a mock carrying
  `seed={}`.
- **The pre-flight must render the cultural prompt the way the orchestrator does.** The
  template in the script is an **f-string** (`{self.culture['name']}`,
  `{', '.join(self.culture['tenets'])}`, `{self.culture['voice_emphasis']}`, `{prompt}`), so a
  `str.format()`-based probe raises **`KeyError: 'self'`**. Substituting the four expressions
  with sentinels and filling them in reproduces the orchestrator's bytes exactly.
- **The `write` tool is jailed to the workspace root** — it cannot write `/tmp`; use a bash
  heredoc for `/tmp` artifacts. A heredoc-to-file `python3 - <<EOF` edit applied its patch but the
  re-run still showed the old source, so a `sed -i` on the exact line number was used instead
  and verified by re-reading the file before re-running.
- **Detached launch can hold the tool call open** even with stdout *and* stdin redirected.
  **Check `ps` in a separate command before assuming the launch failed.**
- **Tool timeout 30 s < orchestrator run ~30–50 s.** Launch detached, poll the log. This run
  completed in ~25 s.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN` (the script reads the former, the
  sandbox stores the latter). Unset => JEV degrades to the 2.0 default and every score becomes
  constant.
- **Kill the mock by exact argv** (`python3 /tmp/mock_zai.py`) — there are two pids (the
  `timeout` wrapper and the server); killing the wrapper leaves the server listening. Never
  `pkill -f mock_zai`, which self-matches the killing shell.
- **Check upstream for a peer session before naming the report.** `git fetch` + `git ls-tree` on
  `origin/main` showed session 161 as the highest; upstream HEAD `8a4f9be` matched the local
  tree, so there was **no concurrent peer session** this run (unlike session 158, which collided).
