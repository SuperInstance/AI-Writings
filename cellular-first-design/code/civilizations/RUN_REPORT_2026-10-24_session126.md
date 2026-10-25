# Civ Orchestrator — Run Report, session 126 (2026-10-24)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — `ZAI_TOKEN` absent from the sandbox env and from all 8 sandbox
secrets; the real endpoint returns `401 token expired or incorrect` (endpoint healthy ⇒ credential gap, not outage).
**JEV:** live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; liveness probe → HTTP 422 on a malformed
`questions` payload = auth accepted).
**Status:** ✅ run complete, all verification checks PASS. `ORCH_EXIT=0`.

---

## 1. Run outcome

8 civs × 5 sims, then 5 competition prompts. 5/5 competitions produced a winner.

| civ | argmax (p1..p5) | winner | agreements |
|---|---|---|---|
| civ-precise | p4 | p1,p2,p4,p5 | 1/4 |
| civ-grounded | p1 | p3 | 0/1 |
| civ-poetic | p2 | — | 0/1 |
| civ-formal | — | p5 | 0/1 |

**Chooser vs `avg_score` argmax: 1/5 (20 %).** Clean-mock series now
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → **1/5 (126)**.
Nine five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.

**What survives every session:** the chooser is **not** a pure argmax, and in **every** disagreement this
session it picked a **lower**-scoring candidate (p1 0.15 vs 0.34, p2 0.42 vs 0.53, p3 0.02 vs 0.70,
p5 0.24 vs 0.49). This is the 7th session in the series (116/118/119/120/122/123/125) in which every
observed disagreement goes the same way. The run-to-run swing (0/5 → 4/5 → 1/5 on the same mock and the
same scorer) confirms that a single 5-sample point carries almost no information about a rate; only the
*direction* of the disagreements is stable.

---

## 2. Verification (asserted on rows, never on exit code)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — tree present, all 8 civ
dirs present; `leaderboard.json` and `meta_log.jsonl` mtimes advanced to 19:33.

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` Δ | +5 | 363 → 368 | PASS |
| `Winner:` lines in log | 5 | 5 | PASS |
| new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| sim→competition ts gap at index 4 | all 8 | 1.09–23.14 s, all 8 | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |

**Mock non-degeneracy: 8/8 on all 5 competition prompts — the eighth clean mock measurement**
(118, 120, 121, 122, 123, 124, 125, 126). The competition ordering and the `avg_score` spread are
**real measurements**, not tie-breaks.

**Zero JEV `error` keys** is the check that proves JEV genuinely scored rather than silently
returning the 2.0 default.

**Pre-flight (before the batch, against the live mock):** 4 different civs → 4 different seeds
AND 4 different previews using the exact long cultural prompt the orchestrator sends, HTTP 200,
`[mock-zai seed=…]` prefix present on every body, `grep -c Traceback /tmp/mock_zai.log` → **0**.

**Mock shutdown:** both PIDs killed (the `timeout` wrapper 550 and the server 551 — matched by exact
args `python3 /tmp/mock_zai.py`, never `pkill -f mock_zai`); port 8799 re-probed → **curl exit 7**
(connection refused) = closed.

---

## 3. Low-relevance civilizations

**`civ-grounded` (The Grounded) remains the low-relevance civ — 31 consecutive sessions
(95–126).** Last on every lifetime dimension:

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.2235** | 1.3986 (formal) | 0.175 |
| `alignment` | **1.4712** | 1.8344 (therapist) | **0.363** |
| `quality` | **0.5984** | 0.6313 (formal) | 0.033 |
| `novelty` | 1.6010 | 1.4570 (formal) | −0.144 (not last) |
| `relevance` | **835.74** | 944.64 (engineer) | 108.90 |
| `relevance_per_sim` | **1.179** | 1.360 (formal) | 0.181 |

**The structural gap is `alignment` (0.363), not `quality` (0.033)** — 11× wider. Alignment is
the dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**,
not merely to write well. It is a voice failure, not a prose failure.

**This run, Grounded was last again on `quality` (0.0040) and 2nd-lowest on `alignment` (0.0340,
therapist 0.0200); its `avg_score` (0.1607) was 7th of 8** (therapist lowest at 0.1450).

**Other axes (stable):**
- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4570** (last); alignment 2.1075 healthy.
- **`civ-poetic` is the stable selection-failure inverse** — 1st on lifetime `avg_score` (1.8239),
  `quality` (1.0195), `novelty` (2.0577); **last-but-one on `win_rate`** (0.015, 5 wins / 338 losses) and
  won **0/5** this run despite being argmax on p2.
- **`civ-precise` is the mirror inverse** — best `win_rate` (0.524, 177/161), won **3/5** this run,
  but only 3rd of 8 on lifetime `avg_score` (1.5695); 1st on lifetime `alignment` (2.4355).
- **`civ-whimsical` is the new `win_rate` bottom** — 0.012 (4 wins / 339 losses), displacing poetic
  (0.015). This is a *rank swap at the very bottom of a 0.003-wide band*, not a new finding.
- **Watch-axis `civ-therapist` — the two-session low DID NOT repeat for a third time.** Therapist
  was last on this run's `avg_score` (0.1450) and `alignment` (0.0200), so the *run-level* signal
  persists — but its lifetime alignment (1.8344) rose, and it is now 2nd on the lifetime `alignment`
  ranking behind only Grounded. The axis remains open; the *lowest this run* label flipped to
  therapist, so keep watching it.
- **Watch-axis `civ-engineer` — the session-121 low did NOT repeat for a third time.** Engineer was
  4th of 8 on this run's `avg_score` (0.2387), 4th on `alignment` (0.2420), 6th of 8 on lifetime
  `relevance_per_sim` (1.381). **Do not promote it to a finding yet.**

**Extinction risk: NONE.** Threshold −10; lowest relevance **+835.74** (84× above the floor).
Registry 8 civs, `max_civs` 12. No birth, no extinction — all 8 remain `generation=1`
(birth/extinction only runs under `--loop`).

---

## 4. Structural state

- **Counter gap (per-civ, uneven — unchanged):** whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. Total +260.
  `save_state()` has **no lock** ⇒ `relevance_per_sim` is **not recomputable from the ledger**
  by an auditor. Unchanged for 8+ sessions.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — confirmed
  again. Winner fields are `winner_civ` / `winner_name`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 0.987,
  `avg_score` 0.325, `novelty` 0.213, `quality` 0.012. `alignment` again carried the widest
  spread and is again the axis the chooser selects on.
- **The `quality` axis collapsed this run** — field mean **0.0098** (min 0.004, max 0.016),
  a spread of 0.012. That is the 119/121/122/123/125 regime, not session-124's 0.337, and again
  **not** session-120's 0.106–0.446. This re-confirms the durable rule: **the quality collapse is a
  LEVEL that moves, not a stable property** — compare cross-civ spreads, not absolute levels, before
  ranking on a dimension. Per-civ quality floors were also uneven
  (precise 0.016, formal 0.012, engineer 0.012, poetic 0.011, mythic 0.009, whimsical 0.007,
  therapist 0.007, grounded 0.004) — the session-122 civ-selective floor, again.

---

## 5. Environment (durable, re-confirmed — 12th consecutive session)

- **NAS EDQUOT is total** (600 G/600 G, 0 bytes free, `df` confirms). `git clone` directly into
  `/workspace/repos/...` dies with `Disk quota exceeded`. The **symlink bridge** is the only way in.
  Verified by inode identity (`stat -L -c '%d:%i'` = `129:10424` on the resolved path, matching the
  target) + `-ef` = SAME.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**;
  the `ai-writings/cellular-first-design` slug 404s and the API is case-insensitive.
  `--filter=blob:none --no-checkout` + `git checkout main -- <path>` worked; the civ subtree is
  small, so a plain shallow clone would also be fine.
- **Do not flatten the clone.** The tree is at `<clone-root>/cellular-first-design/code/civilizations/`;
  point the symlink at the **nested** `cellular-first-design` dir. Flattening makes `git status`
  show every file as `D` + untracked, and `git clean -fd` then silently reverts to the
  pre-run baseline.
- **`gh` is not installed** (13th session running) — use `GET /user/repos` with `GITHUB_TOKEN`.
  The GitHub **code-search** API rate-limits hard — use `GET /search/repositories`
  and `GET /user/repos?per_page=100` instead, and never read a rate-limit body as "no results".
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the sandbox stores
  `TYPESAFE_AI_TOKEN`; the script reads `TYPESAFEAI_KEY`. Unset ⇒ JEV silently degrades to the
  2.0 default and every score becomes a constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is still absent** from env and from all 8 sandbox secrets. The real z.ai
  endpoint returns `401 token expired or incorrect` ⇒ credential gap, not an outage.
- **Tool timeout (30 s) < orchestrator run (~45 s).** Launch detached with stdout redirected to
  a file **and** `< /dev/null`, then poll `ps` + the log. A `setsid nohup … &` launch whose
  child inherits stdout blocks the tool call until the tool timeout — this happened to the mock
  launch this session; `ps` showed the server was up regardless.
- **Mock rebuild caveat:** this session's `/tmp` was wiped, so the mock had to be rebuilt from the
  RUNBOOK. **Both** historical bugs had to be re-applied: the session-112 index-wrap
  (`seed[(i*2)%8:((i*2)%8)+2]`, a plain `seed[i*2:i*2+2]` crashes on `i>=4`) and the
  session-118 seeding fix (`md5(whole_message)[:8]`, because the old first-8-alnum seed is
  civ-invariant and produces a degenerate tie).
- **Mock shutdown:** kill **both** pids (the `timeout` wrapper and the server, whose args are
  exactly `python3 /tmp/mock_zai.py`). Verify the port is closed afterwards (`curl` exit 7).
  Never `pkill -f mock_zai` — it self-matches the killing shell.
- **`civilizations.json` is multi-line JSON, not JSONL** — use `json.loads(open(...).read())`.
