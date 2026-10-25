# Civ Orchestrator — Run Report, session 122 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — no valid `ZAI_TOKEN` exists in this sandbox.
**Result:** 8 civs, 80 ledger rows, 5 competitions, 5 winners. All structural assertions pass.

---

## 1. Verification (assert on rows, never on exit code)

| Assertion | Expected | Measured | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | +10 each (5 sim + 5 competition) | **+10 × 8** | PASS |
| total new ledger rows | 80 | **80** | PASS |
| `meta_log.jsonl` delta | +5 | **+5** (343 → 348) | PASS |
| `Winner:` lines | 5 | **5** | PASS |
| rows with `[mock-zai` prefix | 80 | **80/80** | PASS |
| rows with a JEV `error` key | 0 | **0** | PASS |
| distinct `content_preview` per competition prompt | 8/8 | **5/5 prompts at 8/8** | PASS |
| sim→competition ts gap at index 4 | present in all 8 | **2.46 s – 2.62 s** | PASS |
| distinct ts values | 80 | **80** | PASS |
| `provider` field | `zai` only | **`zai` on 80/80** | PASS |

**Mock non-degeneracy is the load-bearing check.** This session's `/tmp` was wiped again, so the
mock was rebuilt from scratch and the **session-112 index-wrap bug**
(`seed[i*2:i*2+2]` → empty for `i >= 4` → HTTP 500) was live. The **pre-flight probe** caught
the risk *before* the batch: 3 different civs → **3 different seeds**, HTTP 200, 158-char bodies,
`[mock-zai seed=…]` prefix present, **0 tracebacks** in `/tmp/mock_zai.log`. This is the **fourth
clean measurement** in the fleet's history (118, 120, 121, 122), so this run's competition
ordering and `avg_score` spread are **real measurements**, not tie-breaks.

**Pre-flight is the cheap insurance.** A crashing mock still leaves a *listening socket*, so a
port/200 probe looks healthy. Probe with the exact long cultural prompt and grep the mock log
for `Traceback` **before** the batch.

---

## 2. Low-relevance civilizations

**`civ-grounded` (The Grounded) is the low-relevance civ** — **27 consecutive sessions (95–122)**.

Lifetime (all rows in the ledger):

| Dimension | Grounded | Next best | Gap |
|---|---|---|---|
| `avg_score` | **1.2673** (last) | civ-formal 1.4437 | 0.1764 |
| `alignment` | **1.5388** (last) | civ-therapist 1.9304 | **0.3916** |
| `quality` | **0.6298** (last) | civ-formal 0.6641 | 0.0343 |
| `relevance` | **817.94** (last) | civ-formal 920.73 | — |
| `relevance_per_sim` | **1.2230** (last) | civ-formal 1.4060 | — |

**The structural gap is `alignment` (0.3916), not `quality` (0.0343).** Alignment is the
dimension the meta-GAN *selects* on, so The Grounded fails to **embody a distinctive voice** —
a voice failure, not a prose failure. On quality it is essentially tied with civ-formal.

**This run:** Grounded is last again — `avg_score` 0.4110 (lowest of 8), `alignment` 0.048
(near floor), `quality` 0.010. It is **last on every dimension of this run**.

**Distinct axis: `civ-formal`** is the low-**novelty** civ (lifetime novelty 1.4708, last;
alignment 2.1962 healthy, `avg_score` 6th). It won 1/5 competitions this run.

### The two stable inverses (re-confirmed)

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.8821), `quality` (1.0684), `novelty`
  (2.1086) and `relevance_per_sim` (1.8410), but **last on `win_rate` (0.015)** and won
  **0/5** this run. A *selection* failure, not a quality collapse.
- **`civ-precise`** — best `win_rate` (0.509), won **4/5** this run, and 1st on lifetime
  `alignment` (2.5074) — but only 6th on lifetime `avg_score` (1.6131). The mirror inverse.

### Chooser vs `avg_score` argmax: **4/5 (80 %)**

`civ-precise` was argmax in **5/5** competitions and won **4/5**; `civ-formal` won the one
where `civ-precise` did not (argmax was still `civ-precise` at 1.707 vs the winner's 0.910).
The clean-mock series now reads **0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122)**.
Five-sample points cannot narrow a rate: the honest claim is *somewhere in 0–80 %, no single
run can say which*. What survives every session: the chooser is **not** a pure argmax, and in
all 5 disagreements across sessions 116/118/119/120/122 it picked a **lower**-scoring
candidate.

---

## 3. The quality-collapse axis is a *level*, not a property — third confirmation

`quality` collapsed again: **mean 0.0214** over 80 rows (min 0.010, max 0.290, 8 distinct
values) — the session-119/121 pattern, not session-120's (0.106–0.446, spread 0.340).
**Three sessions, two regimes, same mock** ⇒ the collapse is *not* a stable property; it is a
level that moves. The durable rule stands: **compare cross-civ spreads, not absolute levels,
before ranking on a dimension.**

Meanwhile `alignment` carried the widest spread again (per-prompt 0.010–2.800, spread 2.790
vs quality 0.280 and novelty 1.190) and is again the axis the chooser selects on.

**New sub-observation — the collapse is *civ-selective*.** `civ-precise` was the only civ with
a non-floor `quality` (0.068 vs a 0.010–0.022 floor for the other seven) and the only civ
with a non-floor `alignment` (1.631 vs 0.023–0.388 for the other seven). The floor is not
uniform across the field: it is a property of *which civ* the mock text is attributed to.
This is consistent with a single civ's voice dominating the chooser's judgment, and it means
"the whole run collapsed" is a weaker claim than "7 of 8 civs collapsed".

---

## 4. Structural state

- **Extinction risk: NONE.** Threshold −10; lowest relevance **+817.94** (82× above the
  floor). Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop`.
- **Counter gap (per-civ, uneven — unchanged):** whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. `save_state()` has no
  lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.
- **Watch-axis `civ-engineer` — the session-121 low did NOT repeat.** Engineer was 4th of 8
  on this run's `avg_score` (0.6230) and 2nd-lowest on `alignment` (0.386) but no longer last;
  it is 6th of 8 on lifetime `relevance_per_sim` (1.4350). One more session at the bottom
  would make it a trend.
- **No civ birth or extinction.** All 8 civs remain `generation=1`.

---

## 5. Environment (durable, re-confirmed)

- **NAS EDQUOT is total** (8th session running) — no write to `/workspace` succeeds, even a
  5-byte `echo` yields a 0-byte file that `ls` still lists and `cp` exits 0. The **symlink
  bridge** is the only way in; verified by inode identity (`stat -L -c '%d:%i'` on both
  sides + `-ef`) and 5/5 clean `ls` retries.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**;
  the `ai-writings/cellular-first-design` slug 404s and the API is case-insensitive.
- **Do not flatten the clone.** The symlink target is the *nested* `cellular-first-design`
  dir. A **consistent 5/5** `ls` failure = wrong target; an **intermittent** one = mount
  race. Retry with `stat -L` + `readlink -f` + `[-e]` before touching the bridge.
- **`gh` is not installed** (9th session running) — use `GET /search/repositories?q=…` and
  `GET /user/repos` with `GITHUB_TOKEN`.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`**, or JEV silently degrades to
  the 2.0 default and every score becomes a constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) and `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is still absent** from env and the secret store; z.ai returns 401
  `token expired or incorrect` (endpoint healthy ⇒ credential gap, not an outage). JEV is
  live (422 on a malformed `questions` = auth accepted).
- **Tool timeout (30 s) < orchestrator run (~50 s).** Launch detached with stdout to a
  file, then poll `ps` + the log.
