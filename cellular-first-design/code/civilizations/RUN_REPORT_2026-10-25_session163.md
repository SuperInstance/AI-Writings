# Civ Orchestrator — Run Report, session 163 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Exit code:** 0 · **Wall time:** ~45 s · **Run mode:** single batch (no `--loop`, so no
extinction/birth pass) · **Baseline:** `db7f7a0` (session 162)

---

## Result

The run completed and **every civilization's `simulations.jsonl` grew by exactly 10 rows**
(5 sims + 5 competition re-runs). `meta_log.jsonl` grew by exactly 5 (548 → **553**). All 18
expected files are modified in the civ tree (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`). **94/95 verification assertions passed, 1 fail** (the fail is a
*harness-expectation* error, corrected below — see the note on `simulations_run`).

### Row deltas (verified by `ls -la` + `wc -l`, not by exit code)

| civ | rows before | rows after | Δ | `simulations_run` Δ | W+L Δ |
|---|---|---|---|---|---|
| civ-grounded | 1112 | 1122 | **+10** | 1069→1079 (+10) | +5 |
| civ-whimsical | 1124 | 1134 | **+10** | 1061→1071 (+10) | +5 |
| civ-formal | 1097 | 1107 | **+10** | 1055→1065 (+10) | +5 |
| civ-poetic | 1091 | 1101 | **+10** | 1054→1064 (+10) | +5 |
| civ-precise | 1061 | 1071 | **+10** | 1045→1055 (+10) | +5 |
| civ-mythic | 1069 | 1079 | **+10** | 1049→1059 (+10) | +5 |
| civ-therapist | 1064 | 1074 | **+10** | 1047→1057 (+10) | +5 |
| civ-engineer | 1066 | 1076 | **+10** | 1044→1054 (+10) | +5 |

`meta_log.jsonl`: 548 → **553** (+5). `leaderboard.json` rewritten at 03:34Z.
`ls -la` on the civ tree shows every `simulations.jsonl` and `culture.json` with mtime 03:34
(only `civilizations.json` is untouched, as expected — the registry does not change outside
`--loop`).

All 80 new rows carry a `ts` inside a single clean window, and the oldest new row is newer than
**every** pre-existing row, so the +10 per civ is this run's work and not a re-read of history.

> **Baseline source.** `simulations_run` and the ledger row count are read from the **git blob's
> `culture.json`**, not from the working tree and not from the ledger's own row count.

### The one harness FAIL was my own expectation, and the code settles it

The first pass asserted `simulations_run` delta == **+5** and produced 8 fails. Reading the
source settles it: `run_simulation()` is called by **both** phases — the sim loop
(`run_civilization_batch`) **and** the competition (`civilization_orchestrator.py:252`,
`ex.submit(c.run_simulation, prompt, providers)`) — and it increments `self.sims_run` on every
call (`line 206`). So +10 is the correct expectation and the harness was wrong, not the run.
Corrected expectation: **+10**, matching the ledger delta exactly.

This is the **session-157 trap** in its original form ("the `simulations_run` baseline is NOT the
ledger row count") and it deserves a sharper phrasing, because the *reason* is now visible in
the source rather than inferred from a counter offset: `simulations_run` and the ledger row
count are **the same quantity** (one `run_simulation()` call = one ledger row = one counter
increment). The historical "+260 counter gap" is therefore an **epoch artifact** (the ledger
predates the counter), not a live divergence. **Assert `simulations_run` delta == ledger delta
(== +10) on a clean run; the two are equal by construction.**

### Harness (95 assertions, 1 fail — the expectation above)

- No `error` key and **no `2.0/2.0/2.0` fallback triple** on any of the 80 new rows
  (i.e. JEV really answered — `TYPESAFEAI_KEY` was exported).
- **80 distinct JEV score triples** (q 0.01–0.07, n 0.60–1.87, a 0.07–1.31). A silent 2.0
  default would give one repeated triple.
- `provider == "zai"` on all 80 rows; all carry a parseable `[mock-zai seed=…]` prefix.
- `avg_score` recomputes exactly from the three axes on every row; **80/80** exact.
- **Seed non-degeneracy:** exactly **40 distinct seeds** and **40 distinct previews** across the
  80 rows — taken from the correct **10-rows-per-civ** window.
- **0** `(civ, prompt)` combos carrying more than one seed; **8/8 distinct seeds AND 8/8
  distinct previews on all 5 competition prompts**.
- sim→competition `ts` gap at index 4 present in all 8 civs (0.60–0.67 s).
- `meta_log.results` is a **list of `[civ_id, score]` pairs** (not a dict), 8 entries per row,
  covering all 8 civs, with `winner_civ` always among the results.
- `culture.json` `simulations_run` = `pre+10` for all 8; `generation` still 1; win+loss +5;
  registry unchanged at 8 ids (no birth/extinction in non-loop mode).
- Leaderboard re-sorted by `relevance_per_sim` descending; leaderboard `sims_run` and
  `relevance` reconcile exactly against every `culture.json`.
- `git status --porcelain` = **18** modified.

### The confidence-spread check — a real signal, but a JEV-side one

The harness flagged "broad confidence spread (>=10 distinct)" as FAIL: this run's 80 rows carry
only **6 distinct confidence values**, all in the **0.95–1.00** band, whereas the 80 rows
immediately before it carried **52 distinct values** spanning 0.27–1.00.

**This is not a mock degeneracy.** 40 distinct mock bodies are present, and **24 of them map to
two or more different JEV score triples** — so JEV is genuinely scoring content, not returning a
constant. The narrow confidence band and the collapsed `quality` axis (field mean **0.030**,
range 0.01–0.07) are properties of the **JEV scoring model on this run's content**, and the
`quality` collapse reproduces the **19-of-the-last-20 clean-mock sessions** regime
(119/121/122/138) documented in sessions 160–161. It is a pre-existing, JEV-side regime, not
something this run introduced.

**Rule: treat the confidence-spread check as a JEV-liveness check, not a mock check, and
never report it as a mock failure without the same-body/different-triple test above.** The
mock-integrity checks remain the seed and preview distinctness counts, which passed 40/40.

### Competition results (5 prompts)

| prompt | winner | argmax on `avg_score` | delta (winner − argmax) |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | −0.1700 |
| the bookkeeper's role | civ-precise | civ-precise | +0.0000 |
| the witness log | civ-formal | civ-poetic | −0.0900 |
| ternary values | civ-precise | civ-poetic | −0.2467 |
| JEV as a decision oracle | civ-precise | civ-whimsical | −0.0167 |

**Chooser vs `avg_score` argmax: 1/5 (20 %)** — down from 2/5 (40 %) in session 162, up from
0/5 in session 157. All four disagreements again took the **lower**-scoring candidate
(deltas −0.1700, −0.0900, −0.2467, −0.0167). The 30-row trailing window now reads
`000001011110110001000000010100` + `10000` = **11/35**; a 5-sample point still cannot pin a
rate, so the honest claim is *somewhere in 0–80 %*. **The direction is the finding; the rate is
not.** Never treat `win_rate` as a quality metric — it is a *selection* metric.

---

## Low-relevance civs

### The lifetime low: `civ-grounded` (The Grounded) — **53 consecutive sessions (95–163)**

`civ-grounded` is **last of 8 on every lifetime axis** and the label did **not** rotate. For the
second consecutive session, the run-level and lifetime lows are **the same civ** (the
session-132 rule was not violated this session):

| axis | civ-grounded | next civ | gap |
|---|---|---|---|
| `relevance` | **1036.62** | 1181.15 (engineer) | 144.53 |
| `relevance_per_sim` | **0.961** | 1.121 (engineer) | 0.160 |
| `avg_score` | **0.9991** | 1.1388 (engineer) | 0.1398 |
| `alignment` | **1.0872** | 1.2898 (therapist) | **0.2026** |
| `quality` | **0.4208** | 0.4529 (formal) | 0.0321 |

**The binding constraint is still alignment.** Absolute gaps: alignment **0.2026** vs quality
**0.0321** — a 6.3x wider alignment gap. (Quote the absolute gaps, not the ratio: the ratio has
swung 11x → 2.7x → 7.5x → 0.4x → 6.6x → 4.9x → 6.3x across sessions on identical data-shape
logic, so it is not a stable claim.) Alignment is the dimension the meta-GAN **selects** on, so
Grounded fails to *embody a distinctive voice* — a **voice failure, not a prose failure**.
Lifetime novelty 1.4892 ranks **6th of 8** and sits below the 8-civ median band — losing on
**two** axes (alignment and novelty), the same shape as session 161.

**Extinction risk NONE** — threshold −10; lowest relevance 1036.62 = **103.7x above the floor**.
Registry 8, `max_civs` 12; all 8 still `generation=1`. Extinction/birth only runs under `--loop`.

### The run-level watch axis: `civ-therapist`

`civ-therapist` took the **run-level low on `alignment`** (0.1040, lowest of 8) and the
run-level low on `avg_score` among the mid-field (6th of 8, 0.4560). Its **lifetime** standing
is still mid-field (`avg_score` 1.1598, 6th of 8), so it remains a **watch axis, not a
finding**. It becomes one only if the lifetime axis moves too.

### The stable inverses (both still intact)

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.5563), 1st on lifetime `quality` (0.7557),
  1st on lifetime `relevance` (1616.68) and 1st on lifetime `relevance_per_sim` (1.519) — and
  **last on lifetime `win_rate`** (**0.011**, 6/522). It was the `avg_score` argmax on **three**
  of five prompts this run and won **zero**. The sharpest form of the selection failure yet
  observed.
- **`civ-precise`** — best lifetime `win_rate` (**0.579**, 303/220), **highest lifetime
  `alignment` (2.1168)**, won **4/5** this run at `preferred_temp` 0.2 — the coldest voice is
  what the chooser picks, and it is *not* the argmax on 4 of 5.

### The distinct low-novelty axis: `civ-formal`

`civ-formal` remains last on lifetime **novelty** (1.4021; next `civ-engineer` 1.4679, gap
0.0659) with a healthy alignment (1.6593, 4th). It won 1/5 this run. Unchanged from the
standing finding.

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; `dd` of 5 MB fails with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is exempt |
| Bridge | `ln -s /tmp/aw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:12601` on both sides, `-ef` confirms |
| Clone target | `/tmp/aw` (`--depth 1`); `/tmp` is exempt from the NAS quota |
| Upstream owner | `SuperInstance/ai-writings` (API is case-insensitive: `SuperInstance/AI-Writings`) |
| `gh` | not installed (23rd session) — use the REST API with `GITHUB_TOKEN` |
| Tool timeout | 30 s < run ~45 s → launched detached under `setsid nohup timeout -s KILL 600`, polled by PID |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; the real endpoint returns 401 `token expired or incorrect` (endpoint healthy ⇒ credential gap, not an outage) |
| JEV | live — HTTP 422 `too_short` on a malformed `questions` dict (payload-shape complaint ⇒ auth OK) |
| Mock teardown | killed the **server** pid by exact argv (`python3 /tmp/mock_zai.py`); 0 remaining procs; `curl` exit 7 = port closed |
| `TYPESAFEAI_KEY` | must be exported from `TYPESAFE_AI_TOKEN` — the script reads the former, the sandbox stores the latter |

## Mock rebuild

`/tmp` was empty again ⇒ the mock was rebuilt from scratch and **all three** known bugs had to
be re-applied:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — without it the bridge 500s on `i>=4`
  **while the socket stays open**, so a port/200 probe looks healthy.
- session-118 md5-of-whole-message seeding `md5(msg)[:8]` — without it all 8 civs emit
  identical text (`"YouAreA"` is the first 8 alnum chars of *every* cultural prompt) and every
  competition result is void.
- session-144 `Connection: close` + `Content-Length` — without it `curl -X POST` hangs to the
  tool timeout on a perfectly healthy server.

**Pre-flight probe (live mock, exact long cultural prompt):** 8 civs → **8/8 distinct seeds**,
**8/8 distinct previews**, cultural-prompt lengths 167–199, HTTP 200 in 1.6 ms, `[mock-zai
seed=…]` prefix present on every body, **0 tracebacks** and **0 `EXC:`** in `/tmp/mock_zai.log`.

## Method notes carried forward

- **The hardcoded `CIVS_DIR` is the reason the symlink bridge exists.** The script writes to
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, which is inside the
  NAS quota trap. A clone under any other path fails at the *first* `REGISTRY.read_text()` with
  `FileNotFoundError` — **not** at write time — which reads like a missing file rather than a
  missing bridge. The bridge must exist *before* the run, and the symlink target is the
  **nested** `cellular-first-design` dir, never the repo root.
- **`simulations_run` == ledger row count, by construction.** One `run_simulation()` call appends
  exactly one ledger row and increments the counter exactly once, and the competition phase calls
  `run_simulation()` again. Assert `Δsimulations_run == Δrows == +10`. The historical "+260
  counter gap" is an epoch artifact of the ledger predating the counter, not a live divergence —
  and the *direction* of the gap flips with the epoch, so never quote an epoch-mixed gap.
