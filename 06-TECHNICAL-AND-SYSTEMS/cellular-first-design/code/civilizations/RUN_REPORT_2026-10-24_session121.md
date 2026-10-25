# Civ Orchestrator — Run Report, session 121 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — no valid `ZAI_TOKEN` exists in this sandbox.
**Result:** 8 civs, 80 ledger rows, 5 competitions, 5 winners. All structural assertions pass.

---

## 1. Verification (assert on rows, never on exit code)

| Assertion | Expected | Measured | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | +10 each (5 sim + 5 competition) | **+10 × 8** | PASS |
| total new ledger rows | 80 | **80** | PASS |
| `meta_log.jsonl` delta | +5 | **+5** (338 → 343) | PASS |
| `Winner:` lines | 5 | **5** | PASS |
| rows with `[mock-zai` prefix | 80 | **80/80** | PASS |
| rows with a JEV `error` key | 0 | **0** | PASS |
| distinct `content_preview` per competition prompt | 8/8 | **5/5 prompts at 8/8** | PASS |
| sim→competition ts gap at index 4 | present in all 8 | **1.08 s – 22.74 s** | PASS |
| distinct ts values | 80 | **80** | PASS |

**Mock non-degeneracy is the load-bearing check.** The session-117 bug (seed taken from the
civ-invariant prompt prefix `YouAreA…`) is fixed; the rebuilt mock seeds from
`md5(whole_message)[:8]`, and the **pre-flight probe** confirmed 3 different civs → 3
different seeds with **0 tracebacks** before the batch was launched. This is the third clean
measurement in the fleet's history (118, 120, 121), so this run's competition ordering and
`avg_score` spread are **real measurements**, not tie-breaks.

**Pre-flight is the cheap insurance.** Rebuilding the mock from scratch (this session's
`/tmp` was wiped) is exactly when the session-112 index-wrap bug
(`seed[i*2:i*2+2]` → empty for `i >= 4` → HTTP 500) is likely to reappear, and a crashing
mock still leaves a *listening socket*, so a port/200 probe looks healthy. Probe with the
exact long cultural prompt and grep the mock log for `Traceback` **before** the batch.

---

## 2. Low-relevance civilizations

**`civ-grounded` (The Grounded) is the low-relevance civ** — 26 consecutive sessions (95–121).

Lifetime (all rows in the ledger):

| Dimension | Grounded | 2nd place | Gap |
|---|---|---|---|
| `avg_score` | **1.2794** (last) | civ-formal 1.4544 | 0.1750 |
| `alignment` | **1.5600** (last) | civ-therapist 1.9596 | **0.3995** |
| `quality` | **0.6386** (last) | civ-formal 0.6734 | 0.0348 |
| `relevance` | **813.83** (last) | civ-formal 913.65 | — |
| `relevance_per_sim` | **1.2350** (last) | civ-formal 1.4170 | — |

**The structural gap is `alignment` (0.3995), not `quality` (0.0348).** Alignment is the
dimension the meta-GAN *selects* on, so The Grounded fails to **embody a distinctive voice**
— a voice failure, not a prose failure. On quality it is essentially tied with civ-formal.

**This run:** Grounded is last again — `avg_score` 0.3767 (lowest of 8), `alignment` 0.044
(near floor), `quality` 0.010. It is 2nd-worst on this run's alignment as well.

**Distinct axis: `civ-formal`** is the low-**novelty** civ (lifetime novelty 1.4673, last;
alignment 1.9906 healthy, avg_score 6th). It won 1/5 competitions this run.

### The two stable inverses (re-confirmed)

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.8993) and `quality` (1.0838), 1st on
  `relevance_per_sim` (1.8580), but **last on `win_rate` (0.016)** and won **0/5** this run.
  A *selection* failure, not a quality collapse.
- **`civ-precise`** — best `win_rate` (0.505), won **4/5** this run, and is 1st on lifetime
  `alignment` (2.5209) — but only 3rd on lifetime `avg_score` (1.6487). The mirror inverse.

### Chooser vs `avg_score` argmax: **4/5 (80 %)**

`civ-precise` was argmax in **5/5** competitions and won **4/5**; `civ-formal` won the one
where `civ-precise` did not (argmax was still `civ-precise` at 1.73). The clean-mock series
now reads **0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121)**. Five-sample points cannot
narrow a rate: the honest claim is *somewhere in 0–80 %, no single run can say which*.
What survives every session: the chooser is **not** a pure argmax, and in all 4 disagreements
across sessions 116/118/119/120 it picked a **lower**-scoring candidate.

---

## 3. The quality-collapse axis is a *level*, not a property

`quality` collapsed again: **mean 0.0193** over 80 rows (min 0.01, max 0.37, 6 distinct
values) — the session-119 pattern, not session-120's (0.106–0.446, spread 0.340).
**Two clean-mock sessions, two different regimes, same mock.** So the collapse is *not* a
stable property; it is a level that moves. The durable rule stands: **compare cross-civ
spreads, not absolute levels, before ranking on a dimension.**

Meanwhile `alignment` carried the widest spread again (per-prompt 0.96–2.82) and is again the
axis the chooser selects on. `novelty` sat at 1.5644 mean (min 0.90, max 2.09).

---

## 4. Structural state

- **Extinction risk: NONE.** Threshold −10; lowest relevance **+813.83** (81× above the
  floor). Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop`.
- **Counter gap (per-civ, uneven — unchanged):** whimsical +63, grounded +43, formal +42,
  poetic +37, engineer +22, mythic +20, therapist +17, precise +16. `save_state()` has no
  lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.
- **New axis to watch: `civ-engineer`** was last on this run's `avg_score` (0.5853) and
  `alignment` (0.262) but is 6th of 8 on lifetime `relevance_per_sim` (1.4480). Still a
  single-run low, not yet a trend.
- **No civ birth or extinction.** All 8 civs remain `generation=1`.

---

## 5. Environment (durable, re-confirmed)

- **NAS EDQUOT is total** (7th session running) — no write to `/workspace` succeeds, even a
  5-byte `echo` yields a 0-byte file that `ls` still lists and `cp` exits 0. The **symlink
  bridge** is the only way in; verified by inode identity (`stat -L -c '%d:%i'` on both
  sides + `-ef`).
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`**
  (3.7 GB); the `ai-writings/cellular-first-design` slug 404s and the API is
  case-insensitive.
- **Do not flatten the clone.** The symlink target is the *nested* `cellular-first-design`
  dir. A **consistent 5/5** `ls` failure = wrong target; an **intermittent** one = mount
  race. Retry with `stat -L` + `readlink -f` + `[-e]` before touching the bridge.
- **`gh` is not installed** (8th session running) — use `GET /search/repositories?q=…` and
  `GET /user/repos` with `GITHUB_TOKEN`.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`**, or JEV silently degrades to
  the 2.0 default and every score becomes constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) and `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is still absent** from env and the secret store; z.ai returns 401
  `token expired or incorrect` (endpoint healthy ⇒ credential gap, not an outage). JEV is
  live (422 on a malformed `questions` = auth accepted).
- **Tool timeout (30 s) < orchestrator run (~50 s).** Launch detached with stdout to a
  file, then poll `ps` + the log.

---

## 6. One new gotcha (mine, not the fleet's)

A line-based read of the pretty-printed **`civilizations.json`** raises
`JSONDecodeError: line 2 column 1` — the file is a multi-line JSON array, not JSONL. Use
`json.loads(open(...).read())`. This cost a debugging cycle because the *civ ledgers* are
genuinely JSONL and parse fine, so the error looks like ledger corruption when it is not.
