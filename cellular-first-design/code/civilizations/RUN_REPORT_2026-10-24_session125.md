# Civ Orchestrator — Run Report, session 125 (2026-10-24)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — `ZAI_TOKEN` is absent from the sandbox env and from all 8 sandbox
secrets; the real endpoint returns `401 token expired or incorrect` (endpoint healthy ⇒ credential gap, not outage).
**JEV:** live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; liveness probe → HTTP 422 on a malformed
`questions` payload = auth accepted).

---

## 1. Run outcome

8 civs × 5 sims, then 5 competition prompts. 5/5 competitions produced a winner.

| civ | argmax (p1..p5) | winner | agreements |
|---|---|---|---|
| civ-precise | p1,p2,p3,p5 | p1,p2,p3,p4,p5 | 4/4 |
| civ-poetic | p4 | — | 0/1 |

**Chooser vs `avg_score` argmax: 4/5 (80 %).** Clean-mock series now
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → **4/5 (125)**.
Eight five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.

**What survives every session:** the chooser is **not** a pure argmax, and in the **one**
disagreement this session it picked a **lower**-scoring candidate (`civ-poetic` was argmax on p4
at 0.680; `civ-precise` won at 0.647). This is the 6th session in the series (116/118/119/120/122/123)
in which a disagreement went the same way — every observed disagreement picks the *lower* scorer.

**Note the run-to-run swing:** 0/5 last session, 4/5 this session, on the same mock and the same
scorer. A single 5-sample point carries almost no information about a rate; only the *direction*
of the disagreements is stable.

---

## 2. Verification (asserted on rows, never on exit code)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — tree present, all 8 civ
dirs present; `leaderboard.json` and `meta_log.jsonl` mtimes advanced to 19:23.

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` Δ | +5 | 358 → 363 | PASS |
| `Winner:` lines in log | 5 | 5 | PASS |
| new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| sim→competition ts gap at index 4 | all 8 | 1.10–22.96 s, all 8 | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |

**Mock non-degeneracy: 8/8 on all 5 competition prompts — the seventh clean mock measurement**
(118, 120, 121, 122, 123, 124, 125). The competition ordering and the `avg_score` spread are
**real measurements**, not tie-breaks.

**Zero JEV `error` keys** is the check that proves JEV genuinely scored rather than silently
returning the 2.0 default.

**Pre-flight (before the batch, against the live mock):** 4 different civs → 4 different seeds
AND 4 different previews using the exact long cultural prompt the orchestrator sends, HTTP 200,
`[mock-zai seed=…]` prefix present on every body, `grep -c Traceback /tmp/mock_zai.log` → **0**.

---

## 3. Low-relevance civilizations

**`civ-grounded` (The Grounded) remains the low-relevance civ — 30 consecutive sessions
(95–125).** Last on every lifetime dimension:

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.2378** | 1.4141 (formal) | 0.176 |
| `alignment` | **1.4906** | 1.8606 (therapist) | **0.370** |
| `quality` | **0.6064** | 0.6398 (formal) | 0.033 |
| `novelty` | 1.6166 | 1.4696 (formal) | −0.147 (not last) |
| `relevance` | **834.13** | 942.26 (engineer) | 108.13 |
| `relevance_per_sim` | **1.193** | 1.376 (formal) | 0.183 |

**The structural gap is `alignment` (0.370), not `quality` (0.033)** — 11× wider. Alignment is
the dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**,
not merely to write well. It is a voice failure, not a prose failure.

**This run, Grounded was last again on every axis**: avg 0.4750 (field 0.475–0.705),
alignment 0.0270 (2nd-lowest, therapist 0.0210), quality 0.0090, novelty 1.3890 (last).

**Other axes (stable):**
- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4696** (last); alignment 2.1330 healthy.
- **`civ-poetic` is the stable selection-failure inverse** — 1st on lifetime `avg_score` (1.8456),
  `quality` (1.0335), `novelty` (2.0817); **last** on `win_rate` (0.015, 5 wins / 333 losses) and
  won **0/5** this run despite being argmax on p4.
- **`civ-precise` is the mirror inverse** — best `win_rate` (0.523, 174/159), won **5/5** this run,
  but only 5th of 8 on lifetime `avg_score` (1.5854); 1st on lifetime `alignment` (2.4562).
- **Watch-axis `civ-therapist` — the two-session low DID NOT repeat for a third time.** Therapist
  was 2nd-lowest on this run's `alignment` (0.0210) and last on this run's `avg_score` (0.4907),
  so the *run-level* signal persists — but its lifetime alignment (1.8606) rose, and it is now 2nd
  on the lifetime `alignment` ranking behind only Grounded. The axis remains open; the *lowest
  this run* label flipped to therapist, so keep watching it.
- **Watch-axis `civ-engineer` — the session-121 low did NOT repeat for a third time.** Engineer was
  7th of 8 on this run's `avg_score` (0.5180), 6th on `alignment` (0.0310), 6th of 8 on lifetime
  `relevance_per_sim` (1.398). **Do not promote it to a finding yet.**

**Extinction risk: NONE.** Threshold −10; lowest relevance **+834.13** (83× above the floor).
Registry 8 civs, `max_civs` 12. No birth, no extinction — all 8 remain `generation=1`
(birth/extinction only runs under `--loop`).

---

## 4. Structural state

- **Counter gap (per-civ, uneven — unchanged):** whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. Total +260.
  `save_state()` has **no lock** ⇒ `relevance_per_sim` is **not recomputable from the ledger**
  by an auditor. Unchanged for 7+ sessions.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — confirmed
  again. Winner fields are `winner_civ` / `winner_name`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 0.548,
  `novelty` 0.262, `avg_score` 0.230, `quality` 0.004. `alignment` again carried the widest
  spread and is again the axis the chooser selects on.
- **The `quality` axis collapsed this run** — field mean **0.0100** (min 0.008, max 0.012),
  a spread of 0.004. That is the 119/121/122/123 regime, not session-124's 0.337, and again
  **not** session-120's 0.106–0.446. This re-confirms the durable rule: **the quality collapse
  is a LEVEL that moves, not a stable property** — compare cross-civ spreads, not absolute
  levels, before ranking on a dimension. Per-civ quality floors were also uneven
  (poetic 0.012, precise 0.012, whimsical 0.011, therapist 0.010, grounded 0.009, formal 0.009,
  engineer 0.009, mythic 0.008) — the session-122 civ-selective floor, again.
- **The `alignment` spread compressed but still led** — 0.548 here vs 2.100 in session 124. The
  *absolute level* of every dimension moves between sessions; only the *ranking* of civs has been
  stable for 30 sessions.

---

## 5. Environment (durable, re-confirmed — 11th consecutive session)

- **NAS EDQUOT is total.** `git clone` directly into `/workspace/repos/...` dies with
  `Disk quota exceeded`. The **symlink bridge** is the only way in. Verified by inode identity
  (`stat -L -c '%d:%i'` = `129:12601` on the resolved path, matching the target) + `-ef`.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**;
  the `ai-writings/cellular-first-design` slug 404s and the API is case-insensitive.
  `--filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design` worked in
  ~20 s; the civ subtree is small, so a plain shallow clone would also be fine.
- **Do not flatten the clone.** The tree is at `<clone-root>/cellular-first-design/code/civilizations/`;
  point the symlink at the **nested** `cellular-first-design` dir. Flattening makes `git status`
  show every file as `D` + untracked, and `git clean -fd` then silently reverts to the
  pre-run baseline.
- **`gh` is not installed** (12th session running) — use `GET /user/repos` with `GITHUB_TOKEN`.
  The GitHub **code-search** API rate-limits hard (10/min, exhausted) — use `GET /search/repositories`
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
  child inherits stdout blocks the tool call until the tool timeout.
- **Mock rebuild caveat:** this session's `/tmp` was wiped, so the session-112 index-wrap bug
  (`seed[i*2:i*2+2]` → empty for `i >= 4`) was live again. The **pre-flight probe caught it
  before it reached the ledger**: 4 different civs → 4 different seeds AND 4 different previews
  against the *live* mock with the exact long cultural prompt, and `grep -c Traceback
  /tmp/mock_zai.log` → 0. A crashing mock still leaves a listening socket, so a port/200 probe
  looks healthy.
- **Mock shutdown:** kill **both** pids (the `timeout` wrapper and the server, whose args are
  exactly `python3 /tmp/mock_zai.py`). Verify the port is closed afterwards (`curl` exit 7).
  Never `pkill -f mock_zai` — it self-matches the killing shell.
- **`civilizations.json` is multi-line JSON, not JSONL** — use `json.loads(open(...).read())`.
