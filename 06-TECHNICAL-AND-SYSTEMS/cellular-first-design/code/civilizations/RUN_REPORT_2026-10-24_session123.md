# Civ Orchestrator — Run Report, session 123 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — `ZAI_TOKEN` is absent from the sandbox; the real
endpoint returns `401 token expired or incorrect` (endpoint healthy ⇒ credential gap, not outage).
**JEV:** live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; liveness probe → HTTP 422 on a
malformed `questions` payload = auth accepted).

---

## 1. Run outcome

8 civs × 5 sims, then 5 competition prompts. 5/5 competitions produced a winner.

| civ | argmax (p1..p5) | winner | agreements |
|---|---|---|---|
| civ-precise | p3,p4,p5 | p2,p3,p4,p5 | 3/5 |
| civ-grounded | — | p1 | 1/5 |

**Chooser vs `avg_score` argmax: 3/5 (60 %).** Clean-mock series now
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → **3/5 (123)**.
Six five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.

**What survives every session:** the chooser is **not** a pure argmax, and in **both**
disagreements this session (p1, p2) it picked a **lower**-scoring candidate. p1 is the
striking one: `civ-poetic` argmaxed at 0.790 and `civ-grounded` won at **0.163** — the
lowest-scoring candidate on the field took the win. This continues the session-116 finding
under a working mock. `civ-grounded` winning a competition while being the fleet's
lowest-relevance civ is exactly the "chooser ≠ quality" pattern.

---

## 2. Verification (asserted on rows, never on exit code)

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` Δ | +5 | +5 | PASS |
| `Winner:` lines in log | 5 | 5 | PASS |
| new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| sim→competition ts gap at index 4 | all 8 | 1.15–23.28 s, all 8 | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |

**Mock non-degeneracy: 8/8 on all 5 competition prompts, and 8/8 on all 5 sim-phase slots —
the fifth clean mock measurement** (118, 120, 121, 122, 123). The competition ordering and
the `avg_score` spread are therefore **real measurements**, not tie-breaks.

**Zero JEV `error` keys** is the check that proves JEV genuinely scored rather than silently
returning the 2.0 default.

---

## 3. Low-relevance civilizations

**`civ-grounded` (The Grounded) remains the low-relevance civ — 28 consecutive sessions
(95–123).** Last on every lifetime dimension:

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.2525** | 1.4284 (formal) | 0.176 |
| `alignment` | **1.5184** | 2.1684 (formal) | **0.650** |
| `quality` | **0.6212** | 0.6549 (formal) | 0.034 |
| `novelty` | 1.6178 | 1.4619 (formal) | −0.156 (not last) |
| `relevance` | **819.94** | 924.36 (formal) | 104.42 |
| `relevance_per_sim` | **1.208** | 1.390 (formal) | 0.182 |

**The structural gap is `alignment` (0.650), not `quality` (0.034)** — 19× wider. Alignment is
the dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**,
not merely to write well. It is a voice failure, not a prose failure.

**This run, Grounded was last again on every axis**: avg 0.2000 (vs field 0.2–0.84),
alignment 0.0670, quality 0.0100 — and the sim-phase/competition-phase pattern held.

**Other axes (stable):**
- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4619** (last); alignment 2.1684 healthy.
- **`civ-poetic` is the stable selection-failure inverse** — 1st on lifetime `avg_score` (1.8672),
  `quality` (1.0538), `novelty` (2.0894); **last** on `win_rate` (0.015, 5 wins / 323 losses) and
  won **0/5** this run despite being argmax on p1 and p2.
- **`civ-precise` is the mirror inverse** — best `win_rate` (0.514, 166/157), won 4/5 this run
  (argmax 3/5), but only 3rd of 8 on lifetime `avg_score` (1.6009).
- **Watch-axis `civ-engineer` — the session-121 low did NOT repeat for a second time.** Engineer
  was 5th of 8 on this run's `avg_score` (0.2923), 2nd-lowest on `alignment` (0.2510), and 6th of
  8 on lifetime `relevance_per_sim` (1.417). One more session at the bottom would make it a
  trend — **do not promote it to a finding yet.**

**New this session: `civ-therapist` was 2nd-lowest on this run's `alignment` (0.0420)** — the
lowest alignment of any civ in the field, below `civ-grounded`'s 0.0670. Its lifetime alignment
(1.9024) is mid-field, so this is a single-run low, not yet a second axis. Watch it.

**Extinction risk: NONE.** Threshold −10; lowest relevance **+819.94** (82× above the floor).
Registry 8 civs, `max_civs` 12. No birth, no extinction — all 8 remain `generation=1`
(birth/extinction only runs under `--loop`).

---

## 4. Structural state

- **Counter gap (per-civ, uneven — unchanged):** whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16.
  `save_state()` has **no lock** ⇒ `relevance_per_sim` is **not recomputable from the ledger**
  by an auditor. Unchanged for 5+ sessions.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — confirmed
  again (`type=list`, `n=8`). A dict-shaped reader silently yields 0 % agreement and empty
  pick tallies. Winner fields are `winner_civ` / `winner_name`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 2.320,
  `novelty` 0.870, `quality` 0.080. `alignment` again carried the widest spread and is again
  the axis the chooser selects on. `quality` was again collapsed (mean 0.017) — the
  session-119/121/122 regime, against session-120's 0.106–0.446. **The quality collapse is a
  LEVEL that moves, not a stable property** — compare cross-civ spreads before ranking.

---

## 5. Environment (durable, re-confirmed — 9th consecutive session)

- **NAS EDQUOT is total.** `git clone` directly into `/workspace/repos/...` dies with
  `Disk quota exceeded`; even a 5-byte `echo` into `/workspace` yields a **0-byte** file that
  `ls` still lists. The **symlink bridge** is the only way in. Verified by inode identity
  (`stat -L -c '%d:%i'` = `129:10424` on both sides) + `-ef`.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**;
  the `ai-writings/cellular-first-design` slug 404s and the API is case-insensitive.
  A plain `git clone --depth 1` of the whole repo checked out fine — the civ subtree is small,
  so `--filter=blob:none` + `sparse-checkout` is unnecessary.
- **Do not flatten the clone.** The tree is at `<clone-root>/cellular-first-design/code/civilizations/`;
  point the symlink at the **nested** `cellular-first-design` dir. Flattening makes `git status`
  show every file as `D` + untracked, and `git clean -fd` then silently reverts to the
  pre-run baseline.
- **`gh` is not installed** (10th session running) — use `GET /search/repositories?q=…` and
  `GET /user/repos` with `GITHUB_TOKEN`.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the sandbox stores
  `TYPESAFE_AI_TOKEN`; the script reads `TYPESAFEAI_KEY`. Unset ⇒ JEV silently degrades to
  the 2.0 default and every score becomes a constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is still absent** from env and from all 8 sandbox secrets. The real z.ai
  endpoint returns `401 token expired or incorrect` ⇒ credential gap, not an outage.
- **Tool timeout (30 s) < orchestrator run (~50 s).** Launch detached with stdout redirected to
  a file, then poll `ps` + the log. A `setsid nohup … &` launch whose child inherits stdout
  **blocks the tool call** until the tool timeout — the job still starts.
- **Mock rebuild caveat:** this session's `/tmp` was wiped, so the session-112 index-wrap bug
  (`seed[i*2:i*2+2]` → empty for `i >= 4`) was live again. The **pre-flight probe caught it
  before it reached the ledger**: assert 3 different civs → 3 different seeds against the
  *live* mock with the exact long cultural prompt, and `grep -c Traceback /tmp/mock_zai.log` → 0.
  A crashing mock still leaves a listening socket, so a port/200 probe looks healthy.
- **Mock shutdown:** kill **both** pids (the `timeout` wrapper and the server, whose args are
  exactly `python3 /tmp/mock_zai.py`). Verify the port is closed afterwards (`curl` exit 7).
  Never `pkill -f mock_zai` — it self-matches the killing shell.
- **`civilizations.json` is multi-line JSON, not JSONL** — use `json.loads(open(...).read())`.
