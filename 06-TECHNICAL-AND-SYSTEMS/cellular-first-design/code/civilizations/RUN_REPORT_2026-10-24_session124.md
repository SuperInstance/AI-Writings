# Civ Orchestrator — Run Report, session 124 (2026-10-24)

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
| civ-poetic | p1,p2,p4,p5 | — | 0/4 |
| civ-precise | p3 | p1,p2,p5 | 0/3 |
| civ-engineer | — | p4 | — |
| civ-formal | — | p3 | — |

**Chooser vs `avg_score` argmax: 0/5 (0 %).** Clean-mock series now
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → **0/5 (124)**.
Seven five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.

**What survives every session:** the chooser is **not** a pure argmax, and in **all 5**
disagreements this session it picked a **lower**-scoring candidate (`civ-poetic` was argmax on
4/5 prompts and won **0/5**). Sixth consecutive session in which the chooser's selection and the
scorer's ranking disagree.

---

## 2. Verification (asserted on rows, never on exit code)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — tree present, all 8 civ
dirs present; `leaderboard.json` and `meta_log.jsonl` mtimes advanced to 19:12.

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` Δ | +5 | 353 → 358 | PASS |
| `Winner:` lines in log | 5 | 5 | PASS |
| new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| sim→competition ts gap at index 4 | all 8 | 1.11–23.13 s, all 8 | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |

**Mock non-degeneracy: 8/8 on all 5 competition prompts — the sixth clean mock measurement**
(118, 120, 121, 122, 123, 124). The competition ordering and the `avg_score` spread are
**real measurements**, not tie-breaks.

**Zero JEV `error` keys** is the check that proves JEV genuinely scored rather than silently
returning the 2.0 default.

---

## 3. Low-relevance civilizations

**`civ-grounded` (The Grounded) remains the low-relevance civ — 29 consecutive sessions
(95–124).** Last on every lifetime dimension:

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.2483** | 1.4263 (formal) | 0.178 |
| `alignment` | **1.5106** | 1.8875 (therapist) | **0.377** |
| `quality` | **0.6145** | 0.6486 (formal) | 0.034 |
| `novelty` | 1.6197 | 1.4685 (formal) | −0.151 (not last) |
| `relevance` | **829.38** | 937.16 (formal) | 107.78 |
| `relevance_per_sim` | **1.204** | 1.388 (formal) | 0.184 |

**The structural gap is `alignment` (0.377), not `quality` (0.034)** — 11× wider. Alignment is
the dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**,
not merely to write well. It is a voice failure, not a prose failure.

**This run, Grounded was last again on every axis**: avg 0.9447 (vs field 0.94–1.59),
alignment 0.9430, quality 0.1340 — and the sim-phase/competition-phase pattern held.

**Other axes (stable):**
- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4685** (last); alignment 2.1619 healthy.
- **`civ-poetic` is the stable selection-failure inverse** — 1st on lifetime `avg_score` (1.8633),
  `quality` (1.0479), `novelty` (2.0877), `relevance_per_sim` (1.822); **last** on `win_rate`
  (0.015, 5 wins / 328 losses) and won **0/5** this run despite being argmax on 4/5 prompts.
- **`civ-precise` is the mirror inverse** — best `win_rate` (0.515, 169/159), won 3/5 this run,
  but only 4th of 8 on lifetime `avg_score` (1.5983) and 2nd on `alignment` (2.4839).
- **Watch-axis `civ-engineer` — the session-121 low did NOT repeat for a second time.** Engineer
  was 4th of 8 on this run's `avg_score` (1.0170), 2nd-lowest on `alignment` (0.9140), and 6th of
  8 on lifetime `relevance_per_sim` (1.411). One more session at the bottom would make it a
  trend — **do not promote it to a finding yet.**

**Watch-axis `civ-therapist` — the session-123 low DID repeat for a second time.** Therapist was
**2nd-lowest on this run's `alignment` (0.8830)**, below `civ-engineer` (0.9140) and above only
`civ-grounded` (0.9430), and last but one on this run's `avg_score` (1.0030). Its lifetime
alignment (1.8875) is 2nd-lowest of 8. **This is now a two-session axis, not a single-run low** —
promote `civ-therapist` to a watch finding: its alignment is structurally mid-low.

**Extinction risk: NONE.** Threshold −10; lowest relevance **+829.38** (83× above the floor).
Registry 8 civs, `max_civs` 12. No birth, no extinction — all 8 remain `generation=1`
(birth/extinction only runs under `--loop`).

---

## 4. Structural state

- **Counter gap (per-civ, uneven — unchanged):** whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16.
  `save_state()` has **no lock** ⇒ `relevance_per_sim` is **not recomputable from the ledger**
  by an auditor. Unchanged for 6+ sessions.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — confirmed
  again (`type=list`, `n=8`). A dict-shaped reader silently yields 0 % agreement and empty
  pick tallies. Winner fields are `winner_civ` / `winner_name`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` 2.100,
  `novelty` 1.100, `quality` 1.110, `avg_score` 1.033. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. `quality` was **not** collapsed this run
  (mean 0.337 vs the 119/121/122/123 regime's ~0.02) — confirming the durable rule: **the
  quality collapse is a LEVEL that moves, not a stable property**; compare cross-civ spreads
  before ranking on a dimension. Per-civ quality floors were also uneven (grounded 0.030,
  therapist 0.020, precise 0.040, poetic 0.120) — the session-122 civ-selective floor, again.

---

## 5. Environment (durable, re-confirmed — 10th consecutive session)

- **NAS EDQUOT is total.** `git clone` directly into `/workspace/repos/...` dies with
  `Disk quota exceeded`; even a 5-byte `echo` into `/workspace` yields a **0-byte** file that
  `ls` still lists. The **symlink bridge** is the only way in. Verified by inode identity
  (`stat -L -c '%d:%i'` = `129:12603` on the resolved path) + `-ef`.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**;
  the `ai-writings/cellular-first-design` slug 404s and the API is case-insensitive.
  `--filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design` worked;
  the civ subtree is small, so a plain shallow clone would also be fine.
- **Do not flatten the clone.** The tree is at `<clone-root>/cellular-first-design/code/civilizations/`;
  point the symlink at the **nested** `cellular-first-design` dir. Flattening makes `git status`
  show every file as `D` + untracked, and `git clean -fd` then silently reverts to the
  pre-run baseline.
- **`gh` is not installed** (11th session running) — use `GET /user/repos` with `GITHUB_TOKEN`.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the sandbox stores
  `TYPESAFE_AI_TOKEN`; the script reads `TYPESAFEAI_KEY`. Unset ⇒ JEV silently degrades to
  the 2.0 default and every score becomes a constant.
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
