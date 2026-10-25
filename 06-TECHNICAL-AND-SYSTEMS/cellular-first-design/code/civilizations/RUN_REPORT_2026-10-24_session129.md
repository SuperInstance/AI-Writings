# Civ Orchestrator — Run Report, session 129 (2026-10-24)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — `ZAI_TOKEN` absent from the sandbox env and from all 8 sandbox secrets; the real endpoint returns `401 token expired or incorrect` (endpoint healthy ⇒ credential gap, not outage).
**JEV:** live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; liveness probe → HTTP 422 on a malformed `questions` payload = auth accepted).
**Status:** ✅ run complete, all verification checks PASS. 8/8 civs at +10 rows, `meta_log` +5, `Winner:` lines = 5.

---

## 1. Run outcome

8 civs × 5 sims, then 5 competition prompts. 5/5 competitions produced a winner.

| civ | argmax (p1..p5) | winner | agreements |
|---|---|---|---|
| civ-poetic | p2,p3,p4 | — | 0/3 |
| civ-mythic | p1 | — | 0/1 |
| civ-precise | p5 | p5 | 1/1 |

**Chooser vs `avg_score` argmax: 0/5 (0 %).** Clean-mock series now
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → **0/5 (129)**.
Thirteen five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.

**What survives every session:** the chooser is **not** a pure argmax, and in **all five** disagreements
this session it picked a **lower**-scoring candidate (p1: 0.237 vs 0.290; p2: 0.540 vs 0.733;
p3: 0.550 vs 0.680; p4: 0.370 vs 0.620; p5: 0.267 vs 0.443). This is the 10th session in the series
(116/118/119/120/122/123/125/127/128/129) in which every observed disagreement goes the same way.
The run-to-run swing on the same mock and the same scorer confirms that a single 5-sample point
carries almost no information about a rate; only the *direction* of the disagreements is stable.

**Winner concentration:** `civ-precise` took 4/5 competitions (and `civ-engineer` 1/5). Both are
selection, not quality, signals — see §3.

---

## 2. Verification (asserted on rows, never on exit code)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — tree present, all 8 civ
dirs present; `leaderboard.json` and `meta_log.jsonl` mtimes advanced to 20:34; every `civ-*/simulations.jsonl`
grew (416564 / 430061 / 442130 / 413707 / 426136 / 405287 / 415080 / 449443 bytes).

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` Δ | +5 | 378 → 383 | PASS |
| `Winner:` lines in log | 5 | 5 | PASS |
| new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| distinct `avg_score` values | >1 (non-constant) | 60 | PASS |
| distinct `content_preview` per civ | 5/10 each | 5/10 × 8 | PASS |

**Mock non-degeneracy: 5 distinct previews per civ across 10 rows** (5 sim-phase + 5 competition-phase
rows hit the same 5 canon prompts, so 5 distinct is the maximum possible). **8/8 distinct seeds** in
the pre-flight. The competition ordering and the `avg_score` spread are **real measurements**, not tie-breaks.

**Zero JEV `error` keys** is the check that proves JEV genuinely scored rather than silently
returning the 2.0 default.

**Pre-flight (before the batch, against the live mock):** 8 different civs → 8 different seeds
AND 8 different previews using the exact long cultural prompt the orchestrator sends, HTTP 200,
`[mock-zai seed=…]` prefix present on every body, body length 633–830 chars, `grep -c Traceback /tmp/mock_zai.log` → **0**.

**Mock shutdown:** both PIDs killed (the `timeout` wrapper 259 and the server 260 — matched by exact
args `python3 /tmp/mock_zai.py`, never `pkill -f mock_zai`); port 8799 re-probed → **curl exit 7**
(connection refused) = closed. Orchestrator procs: none remaining.

**Note on run duration:** all 80 rows landed in a **28.3 s** window with a max inter-row gap of
0.98 s — the sim and competition phases were **not** separated by the ~20 s cluster gap seen in
prior sessions. The `time.sleep(0.5)` rate limit and the parallel competition phase compressed the
timeline. Do not rely on a `ts` cutoff to split the two phases in this run; count from the end of
the file instead.

---

## 3. Low-relevance civilizations

**`civ-grounded` (The Grounded) remains the low-relevance civ — 34 consecutive sessions
(95–129).** Last on lifetime `avg_score`, `quality`, AND `alignment`:

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.1988** | 1.3671 (formal) | 0.1683 |
| `alignment` | **1.4344** | 1.7746 (therapist) | **0.3401** |
| `quality` | **0.5845** | 0.6162 (formal) | 0.0317 |
| `novelty` | 1.5775 | 1.4334 (formal) | +0.1441 (not last) |
| `relevance` | **853.11** | 963.03 (formal/engineer) | 109.92 |
| `relevance_per_sim` | **1.154** | 1.328 (formal) | 0.174 |

**The structural gap is `alignment` (0.3401), not `quality` (0.0317)** — ~11× wider. Alignment is
the dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**,
not merely to write well. It is a voice failure, not a prose failure.

**This run, Grounded was 2nd-lowest of 8 on `avg_score` (0.1627) and 2nd-lowest on `alignment`
(0.0630, therapist 0.0190) — it was NOT the run-level low.** The run-level low on `avg_score` was
`civ-engineer` (0.1440) and on `alignment` was `civ-therapist` (0.0190). This is the second
consecutive session (after 127) where Grounded's *run-level* label did not go to it.

**Other axes (stable):**
- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4334** (last); alignment 2.0517 healthy.
- **`civ-poetic` is the stable selection-failure inverse** — 1st on lifetime `avg_score` (1.7951),
  `quality` (1.0004), `novelty` (2.0237); **last on `win_rate`** (0.014, 5 wins / 353 losses) and won
  **0/5** this run despite being argmax on p2/p3/p4 (0.733 / 0.680 / 0.620).
- **`civ-precise` is the mirror inverse** — best `win_rate` (0.530, 187/166), won **4/5** this run
  (argmax on none of the four), and 1st of 8 on lifetime `alignment` (2.4028).
- **`civ-whimsical` is the `win_rate` bottom** — 0.014 (5 wins / 353 losses), tying poetic at the
  bottom of a 0.000-wide band. It was 3rd of 8 on this run's `avg_score` (0.2630).
- **Watch-axis `civ-therapist`** — LAST of 8 on this run's `alignment` (0.0190) and 7th on
  `avg_score` (0.1510), yet won 0/5. Its lifetime alignment (1.7746) is mid-field.
- **Watch-axis `civ-mythic`** — LAST of 8 on this run's `novelty` (0.2490), 4th on `avg_score`
  (0.2477). Run-level signal only; lifetime is mid-field.
- **New this run: `civ-engineer` took the run-level `avg_score` low (0.1440) and won p5** despite
  being argmax on none — its lifetime `avg_score` (1.3686) is mid-field. Run-level noise, not a new axis.

**Extinction risk: NONE.** Threshold −10; lowest relevance **+853.11** (85× above the floor).
Registry 8 civs, `max_civs` 12. No birth, no extinction — all 8 remain `generation=1`
(birth/extinction only runs under `--loop`).

---

## 4. Structural state

- **Counter gap (per-civ, uneven — unchanged):** whimsical +66, grounded +51, formal +48,
  poetic +40, engineer +24, mythic +22, therapist +19, precise +18. Total +288 (was +260).
  `save_state()` has **no lock** ⇒ `relevance_per_sim` is **not recomputable from the ledger**
  by an auditor. The gap grows every session; it is now 288 rows over 8 sessions of compounding.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — confirmed
  again. Winner fields are `winner_civ` / `winner_name`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 0.930,
  `novelty` 0.385, `avg_score` 0.363, `quality` 0.014. `alignment` again carried the widest
  spread and is again the axis the chooser selects on.
- **The `quality` axis was near-flat again** — field spread **0.0140** (min 0.0050, max 0.0190),
  versus the 119/121/122/123/125/126 regime (0.004–0.337) and the session-127 outlier (1.063).
  Re-confirms the durable rule: **the quality spread is a LEVEL that moves, not a stable property** —
  compare cross-civ spreads, not absolute levels, before ranking on a dimension.
- **Absolute score levels this run are depressed vs lifetime** (run `avg_score` 0.144–0.507 vs
  lifetime 1.199–1.795) — a level shift in the JEV scorer's output for this batch, not a civ effect.
  The cross-civ *ordering* is what carries information.

---

## 5. Environment (durable, re-confirmed — 15th consecutive session)

- **NAS EDQUOT is total** (600 G/600 G, 0 bytes free, `df` confirms). `git clone` directly into
  `/workspace/repos/...` dies with `Disk quota exceeded` (`.git/description` write fails). The
  **symlink bridge** is the only way in. Verified by inode identity (`stat -L -c '%d:%i'` =
  `129:12601` on the resolved path, matching the target) + `-ef` = SAME.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**.
  The `ai-writings/cellular-first-design` slug 404s; the API is case-insensitive.
  Located via GitHub **code search** (`q=civilization_orchestrator+in:path`) → 1 hit, the right repo.
- **Do not flatten the clone.** The tree is at `<clone-root>/cellular-first-design/code/civilizations/`;
  point the symlink at the **nested** `cellular-first-design` dir.
- **`gh` is not installed** (16th session running) — use `GET /user/repos?per_page=100&sort=pushed`
  or `GET /search/code?q=…` with `GITHUB_TOKEN`. The GitHub **code-search** and **core** API
  rate-limits hard — a rate-limit body renders as "no results" for every query at once; never read
  it as a negative result.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the sandbox stores
  `TYPESAFE_AI_TOKEN`; the script reads `TYPESAFEAI_KEY`. Unset ⇒ JEV silently degrades to the
  2.0 default and every score becomes a constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is still absent** from env and from all 8 sandbox secrets. The real z.ai
  endpoint returns `401 token expired or incorrect` ⇒ credential gap, not an outage.
- **Tool timeout (30 s) < orchestrator run.** Launch detached with stdout redirected to a file
  **and** `< /dev/null`, then poll `ps` + the log. This run: launched pid 307/309, completed in
  ~30 s of polling. Note `setsid nohup … &` **does** start the job but the inherited stdout keeps
  the *tool call* open until the tool timeout — the launch looks like a failure when it is not.
- **Mock rebuild caveat:** this session's `/tmp` was wiped, so the mock had to be rebuilt from the
  RUNBOOK. **Both** historical bugs had to be re-applied: the session-112 index-wrap
  (`seed[(i*2)%8:((i*2)%8)+2]`, a plain `seed[i*2:i*2+2]` crashes on `i>=4`) and the
  session-118 seeding fix (`md5(whole_message)[:8]`, because the old first-8-alnum seed is
  civ-invariant and produces a degenerate tie).
- **Mock shutdown:** kill **both** pids (the `timeout` wrapper and the server, whose args are
  exactly `python3 /tmp/mock_zai.py`). Verify the port is closed afterwards (`curl` exit 7).
  Never `pkill -f mock_zai` — it self-matches the killing shell.
- **`civilizations.json` is multi-line JSON, not JSONL** — use `json.loads(open(...).read())`.
