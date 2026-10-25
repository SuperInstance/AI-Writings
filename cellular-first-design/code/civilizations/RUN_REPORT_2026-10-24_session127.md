# Civ Orchestrator — Run Report, session 127 (2026-10-24)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — `ZAI_TOKEN` absent from the sandbox env and from all sandbox
secrets; the real endpoint returns `401 token expired or incorrect` (endpoint healthy ⇒ credential gap, not outage).
**JEV:** live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; liveness probe → HTTP 422 on a malformed
`questions` payload = auth accepted).
**Status:** ✅ run complete, all verification checks PASS. 8/8 civs at +10 rows, `meta_log` +5, `Winner:` lines = 5.

---

## 1. Run outcome

8 civs × 5 sims, then 5 competition prompts. 5/5 competitions produced a winner.

| civ | argmax (p1..p5) | winner | agreements |
|---|---|---|---|
| civ-precise | p1,p2,p3 | p1,p2,p3 | 3/3 |
| civ-poetic | p4,p5 | — | 0/2 |
| civ-therapist | — | p4 | 0/1 |
| civ-whimsical | — | p5 | 0/1 |

**Chooser vs `avg_score` argmax: 3/5 (60 %).** Clean-mock series now
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → **3/5 (127)**.
Ten five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.

**What survives every session:** the chooser is **not** a pure argmax, and in **every** disagreement this
session it picked a **lower**-scoring candidate (p4: 1.763 vs 2.260; p5: 1.937 vs 2.683). This is the 8th
session in the series (116/118/119/120/122/123/125/127) in which every observed disagreement goes the same
way. The run-to-run swing (4/5 → 1/5 → 3/5 on the same mock and the same scorer) confirms that a single
5-sample point carries almost no information about a rate; only the *direction* of the disagreements is stable.

---

## 2. Verification (asserted on rows, never on exit code)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — tree present, all 8 civ
dirs present; `leaderboard.json` and `meta_log.jsonl` mtimes advanced to 19:53.

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` Δ | +5 | 368 → 373 | PASS |
| `Winner:` lines in log | 5 | 5 | PASS |
| new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| sim→competition ts gap at index 4 | all 8 | 1.09–23.06 s, all 8 | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |

**Mock non-degeneracy: 8/8 on all 5 competition prompts — the ninth clean mock measurement**
(118, 120, 121, 122, 123, 124, 125, 126, 127). The competition ordering and the `avg_score` spread are
**real measurements**, not tie-breaks. 40 distinct seeds across the run's 80 rows.

**Zero JEV `error` keys** is the check that proves JEV genuinely scored rather than silently
returning the 2.0 default.

**Pre-flight (before the batch, against the live mock):** 4 different civs → 4 different seeds
AND 4 different previews using the exact long cultural prompt the orchestrator sends, HTTP 200,
`[mock-zai seed=…]` prefix present on every body, `grep -c Traceback /tmp/mock_zai.log` → **0**.

**Mock shutdown:** both PIDs killed (the `timeout` wrapper 325 and the server 327 — matched by exact
args `python3 /tmp/mock_zai.py`, never `pkill -f mock_zai`); port 8799 re-probed → **curl exit 7**
(connection refused) = closed.

---

## 3. Low-relevance civilizations

**`civ-grounded` (The Grounded) remains the low-relevance civ — 32 consecutive sessions
(95–127).** Last on every lifetime dimension except novelty:

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.2267** | 1.3996 (formal) | 0.1729 |
| `alignment` | **1.4709** | 1.8237 (therapist) | **0.3528** |
| `quality` | **0.5998** | 0.6324 (formal) | 0.0326 |
| `novelty` | 1.6095 | 1.4630 (formal) | −0.1465 (not last) |
| `relevance` | **850.42** | 959.19 (engineer) | 108.77 |
| `relevance_per_sim` | **1.183** | 1.362 (formal) | 0.179 |

**The structural gap is `alignment` (0.3528), not `quality` (0.0326)** — ~11× wider. Alignment is
the dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**,
not merely to write well. It is a voice failure, not a prose failure.

**This run, Grounded was 5th of 8 on `avg_score` (1.4683) and 2nd-lowest on `alignment` (1.4510,
therapist 1.0710) — it was NOT the run-level low.** The run-level low was `civ-whimsical`
(avg 1.3997, quality 0.5640, novelty 1.9040) and `civ-therapist` on `alignment` (1.0710).
This is the second consecutive session where Grounded's *run-level* label did not go to it
(session 126's run-level low was therapist on `avg_score`/alignment).

**Other axes (stable):**
- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4630** (last); alignment 2.1036 healthy.
- **`civ-poetic` is the stable selection-failure inverse** — 1st on lifetime `avg_score` (1.8303),
  `quality` (1.0269), `novelty` (2.0619), `alignment` (2.4020); **last-but-one on `win_rate`**
  (0.014, 5 wins / 343 losses) and won **0/5** this run despite being argmax on p4 and p5.
- **`civ-precise` is the mirror inverse** — best `win_rate` (0.525, 180/163), won **3/5** this run
  (argmax on all three), but only 3rd of 8 on lifetime `avg_score` (1.5793); **1st on lifetime
  `alignment` (2.4422)**, narrowly ahead of `civ-poetic` (2.4020).
- **`civ-whimsical` is the new `win_rate` bottom** — 0.014 (5 wins / 343 losses), tying poetic
  (0.014) at the bottom of a 0.000-wide band. It was also the run-level `avg_score` low. Watch it.
- **Watch-axis `civ-therapist` — the run-level low DID repeat for a second time.** Therapist was
  last on this run's `alignment` (1.0710) and 7th of 8 on `avg_score` (1.4340), so the *run-level*
  signal persists — but its lifetime alignment (1.8237) is mid-field. The axis remains open.
- **Watch-axis `civ-engineer` — the session-121 low did NOT repeat.** Engineer was 7th of 8 on
  this run's `avg_score` (1.4547), 3rd-lowest on `alignment` (1.5260), 6th of 8 on lifetime
  `relevance_per_sim` (1.382). **Do not promote it to a finding yet.**

**Extinction risk: NONE.** Threshold −10; lowest relevance **+850.42** (85× above the floor).
Registry 8 civs, `max_civs` 12. No birth, no extinction — all 8 remain `generation=1`
(birth/extinction only runs under `--loop`).

---

## 4. Structural state

- **Counter gap (per-civ, uneven — unchanged):** whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. Total +260.
  `save_state()` has **no lock** ⇒ `relevance_per_sim` is **not recomputable from the ledger**
  by an auditor. Unchanged for 9+ sessions.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — confirmed
  again. Winner fields are `winner_civ` / `winner_name`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 1.887,
  `quality` 1.063, `avg_score` 0.897, `novelty` 0.464. `alignment` again carried the widest
  spread and is again the axis the chooser selects on.
- **The `quality` axis did NOT collapse this run** — field spread **1.063** (min 0.5640, max
  1.6270), versus the 119/121/122/123/125/126 regime (spread 0.004–0.337). This is the
  session-120/124 regime, not the collapse. Re-confirms the durable rule: **the quality
  collapse is a LEVEL that moves, not a stable property** — compare cross-civ spreads, not
  absolute levels, before ranking on a dimension. Per-civ quality floors were also uneven
  (precise 1.627, poetic 1.565 … whimsical 0.564) — the session-122 civ-selective floor, again.

---

## 5. Environment (durable, re-confirmed — 13th consecutive session)

- **NAS EDQUOT is total** (600 G/600 G, 0 bytes free, `df` confirms). `git clone` directly into
  `/workspace/repos/...` dies with `Disk quota exceeded`, and a 5-byte `echo` produces a
  **0-byte** file that `ls` still lists. The **symlink bridge** is the only way in.
  Verified by inode identity (`stat -L -c '%d:%i'` = `129:10424` on the resolved path, matching
  the target) + `-ef` = SAME.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**.
  `--filter=blob:none --no-checkout` + `git sparse-checkout set cellular-first-design` worked.
  The `ai-writings/cellular-first-design` slug 404s; the API is case-insensitive.
- **Do not flatten the clone.** The tree is at `<clone-root>/cellular-first-design/code/civilizations/`;
  point the symlink at the **nested** `cellular-first-design` dir.
- **`gh` is not installed** (14th session running) — use `GET /search/repositories?q=…` with
  `GITHUB_TOKEN`. The GitHub **code-search** and **core** API rate-limits hard — a rate-limit
  body renders as "no results" for every query at once; never read it as a negative result.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the sandbox stores
  `TYPESAFE_AI_TOKEN`; the script reads `TYPESAFEAI_KEY`. Unset ⇒ JEV silently degrades to
  the 2.0 default and every score becomes a constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is still absent** from env and from all sandbox secrets. The real z.ai
  endpoint returns `401 token expired or incorrect` ⇒ credential gap, not an outage.
- **Tool timeout (30 s) < orchestrator run (~50 s).** Launch detached with stdout redirected to
  a file **and** `< /dev/null`, then poll `ps` + the log.
- **Mock rebuild caveat:** this session's `/tmp` was wiped, so the mock had to be rebuilt from the
  RUNBOOK. **Both** historical bugs had to be re-applied: the session-112 index-wrap
  (`seed[(i*2)%8:((i*2)%8)+2]`, a plain `seed[i*2:i*2+2]` crashes on `i>=4`) and the
  session-118 seeding fix (`md5(whole_message)[:8]`, because the old first-8-alnum seed is
  civ-invariant and produces a degenerate tie).
- **Mock shutdown:** kill **both** pids (the `timeout` wrapper and the server, whose args are
  exactly `python3 /tmp/mock_zai.py`). Verify the port is closed afterwards (`curl` exit 7).
  Never `pkill -f mock_zai` — it self-matches the killing shell.
- **`civilizations.json` is multi-line JSON, not JSONL** — use `json.loads(open(...).read())`.
