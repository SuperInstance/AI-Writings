# Civ Orchestrator — Run Report, session 128 (2026-10-24)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — `ZAI_TOKEN` absent from the sandbox env and from all 8 sandbox
secrets; the real endpoint returns `401 token expired or incorrect` (endpoint healthy ⇒ credential gap, not outage).
**JEV:** live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; liveness probe → HTTP 422 on a malformed
`questions` payload = auth accepted).
**Status:** ✅ run complete, all verification checks PASS. 8/8 civs at +10 rows, `meta_log` +5, `Winner:` lines = 5.

---

## 1. Run outcome

8 civs × 5 sims, then 5 competition prompts. 5/5 competitions produced a winner.

| civ | argmax (p1..p5) | winner | agreements |
|---|---|---|---|
| civ-precise | p1,p2,p4 | p1,p2,p4 | 3/3 |
| civ-formal | — | p3 | 0/1 |
| civ-therapist | — | p5 | 0/1 |

**Chooser vs `avg_score` argmax: 2/5 (40 %).** Clean-mock series now
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → **2/5 (128)**.
Twelve five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.

**What survives every session:** the chooser is **not** a pure argmax, and in **both** disagreements this
session it picked a **lower**-scoring candidate (p3: 0.08 vs argmax 0.92; p5: 0.10 vs argmax 0.48). This is the
9th session in the series (116/118/119/120/122/123/125/127/128) in which every observed disagreement goes the
same way. The run-to-run swing (3/5 → 2/5 on the same mock and the same scorer) confirms that a single
5-sample point carries almost no information about a rate; only the *direction* of the disagreements is stable.

---

## 2. Verification (asserted on rows, never on exit code)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — tree present, all 8 civ
dirs present; `leaderboard.json` and `meta_log.jsonl` mtimes advanced to 20:22.

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` Δ | +5 | 373 → 378 | PASS |
| `Winner:` lines in log | 5 | 5 | PASS |
| new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| sim→competition ts gap at index 4 | all 8 | 1.09–22.97 s, all 8 | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |
| distinct seeds per competition prompt | 8/8 | 8/8 × 5 | PASS |

**Mock non-degeneracy: 8/8 on all 5 competition prompts — the tenth clean mock measurement**
(118, 120, 121, 122, 123, 124, 125, 126, 127, 128). The competition ordering and the `avg_score` spread are
**real measurements**, not tie-breaks.

**Zero JEV `error` keys** is the check that proves JEV genuinely scored rather than silently
returning the 2.0 default.

**Pre-flight (before the batch, against the live mock):** 8 different civs → 8 different seeds
AND 8 different previews using the exact long cultural prompt the orchestrator sends, HTTP 200,
`[mock-zai seed=…]` prefix present on every body, body length 542–874 chars, `grep -c Traceback /tmp/mock_zai.log` → **0**.

**Mock shutdown:** both PIDs killed (the `timeout` wrapper 278 and the server 280 — matched by exact
args `python3 /tmp/mock_zai.py`, never `pkill -f mock_zai`); port 8799 re-probed → **curl exit 7**
(connection refused) = closed.

---

## 3. Low-relevance civilizations

**`civ-grounded` (The Grounded) remains the low-relevance civ — 33 consecutive sessions
(95–128).** Last on every lifetime dimension except novelty:

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.2122** | 1.3828 (formal) | 0.1706 |
| `alignment` | **1.4522** | 1.7988 (therapist) | **0.3466** |
| `quality` | **0.5920** | 0.6241 (formal) | 0.0322 |
| `novelty` | 1.5925 | 1.4471 (formal) | +0.1454 (not last) |
| `relevance` | **851.49** | 961.25 (formal) | 109.76 |
| `relevance_per_sim` | **1.168** | 1.344 (formal) | 0.176 |

**The structural gap is `alignment` (0.3466), not `quality` (0.0322)** — ~11× wider. Alignment is
the dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**,
not merely to write well. It is a voice failure, not a prose failure.

**This run, Grounded was LAST of 8 on `avg_score` (0.1063) and 2nd-lowest on `alignment` (0.0240,
therapist 0.0180) — it WAS the run-level low.** This is the third consecutive session where Grounded's
*run-level* label did go to it (session 127's run-level low was whimsical; session 126's was therapist).

**Other axes (stable):**
- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4471** (last); alignment 2.0771 healthy.
  Note Grounded is *not* the novelty floor this session; formal is, and formal is also the run-level
  2nd-lowest on `avg_score` (0.1237).
- **`civ-poetic` is the stable selection-failure inverse** — 1st on lifetime `avg_score` (1.8123),
  `quality` (1.0134), `novelty` (2.0433), `alignment` (2.3801); **last-but-one on `win_rate`**
  (0.014, 5 wins / 348 losses) and won **0/5** this run despite being near-argmax on p2 (0.62).
- **`civ-precise` is the mirror inverse** — best `win_rate` (0.526, 183/165), won **3/5** this run
  (argmax on all three), and 1st of 8 on lifetime `alignment` (2.4271).
- **`civ-whimsical` is the `win_rate` bottom** — 0.014 (5 wins / 348 losses), tying poetic (0.014)
  at the bottom of a 0.000-wide band. It was 6th of 8 on this run's `avg_score` (0.3393).
- **Watch-axis `civ-therapist`** — LAST of 8 on this run's `alignment` (0.0180) and 3rd-lowest on
  `avg_score` (0.1360), yet it **won p5** outright. Its lifetime alignment (1.7988) is mid-field.
  The axis remains open.
- **Watch-axis `civ-mythic`** — LAST of 8 on this run's `novelty` (0.1830) and 4th-lowest on
  `avg_score` (0.1637). Run-level signal only; lifetime is mid-field.

**Extinction risk: NONE.** Threshold −10; lowest relevance **+851.49** (85× above the floor).
Registry 8 civs, `max_civs` 12. No birth, no extinction — all 8 remain `generation=1`
(birth/extinction only runs under `--loop`).

---

## 4. Structural state

- **Counter gap (per-civ, uneven — unchanged):** whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. Total +260.
  `save_state()` has **no lock** ⇒ `relevance_per_sim` is **not recomputable from the ledger**
  by an auditor. Unchanged for 10+ sessions.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — confirmed
  again. Winner fields are `winner_civ` / `winner_name`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 1.333,
  `avg_score` 0.528, `novelty` 0.508, `quality` 0.065. `alignment` again carried the widest
  spread and is again the axis the chooser selects on.
- **The `quality` axis was near-flat this run** — field spread **0.0650** (min 0.0000, max 0.0650),
  versus the 119/121/122/123/125/126 regime (0.004–0.337) and the session-127 outlier (1.063).
  Re-confirms the durable rule: **the quality spread is a LEVEL that moves, not a stable property** —
  compare cross-civ spreads, not absolute levels, before ranking on a dimension. Per-civ quality
  floors were also uneven (precise 0.065, poetic 0.014 … grounded 0.000) — the session-122
  civ-selective floor, again.
- **Absolute score levels this run are depressed vs lifetime** (run `avg_score` 0.106–0.634 vs
  lifetime 1.21–1.82) — a level shift in the JEV scorer's output for this batch, not a civ effect.
  The cross-civ *ordering* is what carries information.

---

## 5. Environment (durable, re-confirmed — 14th consecutive session)

- **NAS EDQUOT is total** (600 G/600 G, 0 bytes free, `df` confirms). `git clone` directly into
  `/workspace/repos/...` dies with `Disk quota exceeded` (`.git/description` write fails), and a
  5-byte `echo` produces a **0-byte** file that `ls` still lists. The **symlink bridge** is the
  only way in. Verified by inode identity (`stat -L -c '%d:%i'` = `129:3669` on the resolved path,
  matching the target) + `-ef` = SAME.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**.
  The `ai-writings/cellular-first-design` slug 404s; the API is case-insensitive.
- **Do not flatten the clone.** The tree is at `<clone-root>/cellular-first-design/code/civilizations/`;
  point the symlink at the **nested** `cellular-first-design` dir.
- **`gh` is not installed** (15th session running) — use `GET /user/repos?per_page=100&sort=pushed`
  with `GITHUB_TOKEN`. The GitHub **code-search** and **core** API rate-limits hard — a rate-limit
  body renders as "no results" for every query at once; never read it as a negative result.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the sandbox stores
  `TYPESAFE_AI_TOKEN`; the script reads `TYPESAFEAI_KEY`. Unset ⇒ JEV silently degrades to
  the 2.0 default and every score becomes a constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is still absent** from env and from all sandbox secrets. The real z.ai
  endpoint returns `401 token expired or incorrect` ⇒ credential gap, not an outage.
- **Tool timeout (30 s) < orchestrator run (~50 s).** Launch detached with stdout redirected to
  a file **and** `< /dev/null`, then poll `ps` + the log. This run: launched pid 327/329, completed
  in ~27 s of polling.
- **Mock rebuild caveat:** this session's `/tmp` was wiped, so the mock had to be rebuilt from the
  RUNBOOK. **Both** historical bugs had to be re-applied: the session-112 index-wrap
  (`seed[(i*2)%8:((i*2)%8)+2]`, a plain `seed[i*2:i*2+2]` crashes on `i>=4`) and the
  session-118 seeding fix (`md5(whole_message)[:8]`, because the old first-8-alnum seed is
  civ-invariant and produces a degenerate tie).
- **Mock shutdown:** kill **both** pids (the `timeout` wrapper and the server, whose args are
  exactly `python3 /tmp/mock_zai.py`). Verify the port is closed afterwards (`curl` exit 7).
  Never `pkill -f mock_zai` — it self-matches the killing shell.
- **`civilizations.json` is multi-line JSON, not JSONL** — use `json.loads(open(...).read())`.
