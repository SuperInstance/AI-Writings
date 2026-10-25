# Civ Orchestrator — Run Report 2026-10-24, session 117

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Timestamp:** 2026-10-24T17:53:09Z
**Result:** COMPLETE — 8 civs, 80 sim rows, 5 competitions, 5 winners.

---

## 1. Pre-flight: the provider path was NOT usable as-is

| Check | Method | Result |
|---|---|---|
| z.ai endpoint health | `POST api.z.ai/.../chat/completions` with dummy token | **HTTP 401** `token expired or incorrect` |
| `ZAI_TOKEN` in env | `env \| grep -i zai` | **absent (0 hits)** |
| `ZAI_TOKEN` in sandbox secret store | secret store scan | **absent** |
| JEV liveness | `POST api.typesafe.ai/v1/systemone`, malformed `questions` | **HTTP 422** `dict_type` — auth ACCEPTED, endpoint live |

Verdict: z.ai endpoint healthy but **credential gap** (not an outage). JEV live. This is the
standing finding from sessions 102–116, re-confirmed.

### Control B: mock z.ai bridge (the documented fallback)

`ZAI_URL_OVERRIDE` alone is **dead code** — `call_provider()` runs the token gate first:

```python
token = os.environ.get(p["env"], "")          # p["env"] == "ZAI_TOKEN"
if not token: return None                      # <-- returns HERE
_ov = os.environ.get(f"{name.upper()}_URL_OVERRIDE", "")   # never reached
```

So Control B needs **both**:

```bash
export ZAI_TOKEN="mock-local-bridge"           # any non-empty placeholder
export ZAI_URL_OVERRIDE="http://127.0.0.1:8799/api/coding/paas/v4/chat/completions"
```

Mock written to `/tmp/mock_zai.py` with the **session-112 index-wrap fix**
(`seed[(i*2)%8:((i*2)%8)+2]`, not the crashing `seed[i*2:i*2+2]`).

**Mock integrity verified before the run** (not just a socket check):
- probed with the **exact long multi-sentence cultural prompt** the orchestrator actually
  sends (not a one-word body) → HTTP 200, 1600-char body, `[mock-zai` prefix present
- `grep -c Traceback` on mock stdout/log → **0**

Mock pids: wrapper `timeout` + server `python3 /tmp/mock_zai.py` (two pids; kill both).

---

## 2. Environment: NAS EDQUOT + symlink bridge

`/workspace` was **100 % full (600 G/600 G, 0 bytes free)**. `git clone` directly into
`/workspace/repos/...` died with `Disk quota exceeded`. Upstream is `SuperInstance/AI-Writings`
(3.7 GB; the `ai-writings/cellular-first-design` slug 404s).

Bridge: clone to `/tmp` (overlay, ~28 G free, NAS quota does not apply), then

```bash
ln -sfn /tmp/work/ai-writings/cellular-first-design \
  /workspace/repos/ai-writings/cellular-first-design
```

Verified by **inode identity**, not by `ls`:
`stat -L -c '%d:%i'` → `129:3670` on both sides, and `-ef` → true.

**Did not flatten the clone** (session-115 trap): the symlink points at the *nested*
`cellular-first-design` dir, so `CIVS_DIR` (hardcoded to `/workspace/repos/ai-writings/
cellular-first-design/code/civilizations`) resolves correctly. `git status` shows 18
modified files and zero deletions — no flattening damage.

`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN` (the script reads `TYPESAFEAI_KEY`;
the sandbox stores `TYPESAFE_AI_TOKEN`). Unset ⇒ JEV silently degrades to the 2.0
default and every score becomes a constant.

---

## 3. Verification — assert on rows, never on exit code

`call_provider()` returns `None` on a missing token, `run_simulation()` returns `None`,
and the competition short-circuits on `if not results: return None` — **all silently, with
exit code 0**.

| Assertion | Expected | Actual | |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | **+10 each** | +10 × 8 | PASS |
| total new rows | **80** | 80 | PASS |
| `meta_log.jsonl` Δ | **+5** | +5 (318 → 323) | PASS |
| `Winner:` lines | **5** | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| rows with `error` key in `scores` | **0** | 0 | PASS |
| `provider` field | `zai` only | `{'zai'}` | PASS |

The **zero-`error` check** is the one that proves JEV genuinely scored the text rather
than silently returning the 2.0 default.

Per-civ Δ breakdown (session-115 finding, re-confirmed): **5 sim-phase rows + 5
competition-phase rows per civ = 10**, not 45. The competition phase runs 8 civs in
parallel but appends one row per civ per prompt; the 8 civs' rows are spread across the
8 ledgers, not 8 each. The sim→competition ts gap sits at index 4 in every civ file
(4.2 s – 22.9 s), confirming the two-cluster structure.

`mono=False` within a civ file is expected: the competition phase is parallel, so rows
interleave.

---

## 4. Competition results — 5/5 to The Precise

| Prompt | Winner | Field avg_score (top → bottom) |
|---|---|---|
| what a cell is | **civ-precise** | precise .92, engineer .75, poetic .70, formal .69, whimsical .57, therapist .53, grounded .51, mythic .27 |
| the bookkeeper's role | **civ-precise** | poetic .85, precise .75, whimsical .76, formal .67, engineer .46, grounded .36, mythic .29, therapist .26 |
| the witness log | **civ-precise** | precise .80, formal .66, poetic .37, engineer .35, grounded .32, mythic .10, whimsical .14, therapist .08 |
| ternary values | **civ-precise** | precise .69, formal .66, poetic .63, mythic .47, engineer .40, whimsical .36, grounded .29, therapist .17 |
| JEV as a decision oracle | **civ-precise** | precise .70, formal .69, poetic .51, engineer .44, whimsical .21, grounded .26, mythic .14, therapist .12 |

**civ-precise won all 5.** Its `wins` went 139 → **144** and `losses` +5, so it was a
clean sweep, not a near-tie broken by a tiebreak.

> **⚠️ MOCK-LIMITED RESULT — the 5/5 sweep is an artifact, not a finding.** All 8 civs'
> competition-phase content was **byte-identical** (verified: one distinct preview per
> civ, the *same* preview across all 8 civs and all 5 prompts). JEV's chooser was handed
> 8 copies of the same string, so its pick is an arbitrary tie-break that happened to
> land on `civ-precise` every time. **Do not read this run's competition ordering, or
> `civ-precise`'s sweep, as a quality signal.** The `avg_score` spread shown above is
> also JEV scoring identical text 8× — the residual differences are JEV nondeterminism,
> not civ differences. See §7 item 5 for the root cause and the fix.
> The **lifetime** leaderboard (§5) is the only trustworthy signal in this report.

**Chooser ≠ argmax confirmed again.** In the "witness log" and "JEV as a decision oracle"
prompts the chooser picked `civ-precise`, which was also the argmax there — but the
chooser scored the *text* via JEV, not `avg_score`. Reproducing the session-116 finding
(a low-scoring civ winning) is **not** expected here: the mock returns near-identical
text per civ (seeded from the prompt), so the chooser's JEV text-score collapses onto
one civ. This run therefore **cannot** re-test the "chooser picks the lowest scorer"
phenomenon — the mock makes the candidates too similar to distinguish. Recorded as a
**limitation of Control B**, not as a refutation of the session-116 observation.

`win_rate` remains a **selection** metric, not a quality metric: standing rule holds.

---

## 5. Low-relevance civilization

### **`civ-grounded` (The Grounded) — LOW RELEVANCE, structurally**

Last on **every** relevance dimension, lifetime and this-run:

| Dimension | civ-grounded | Best | Rank |
|---|---|---|---|
| lifetime `avg_score` | **1.3316** | poetic 1.9676 | **8/8** |
| lifetime `alignment` | **1.638** | precise 2.606 | **8/8** |
| lifetime `quality` | **0.675** | poetic 1.143 | **8/8** |
| `relevance` | **797.20** | poetic 1164.43 | **8/8** |
| `relevance_per_sim` | **1.288** | poetic 1.928 | **8/8** |
| this-run `avg_score` | **0.3343** | precise 0.7830 | **6/8** |
| this-run `alignment` | **0.585** | precise 1.871 | **6/8** |

Alignment is the dimension the meta-GAN **selects** on, so being last on both
lifetime `avg_score` and lifetime `alignment` is structural, not a bad day. This
reproduces the standing finding across sessions 95–104 and is re-confirmed here.
(Under the mock, all civs receive near-identical text, so the *within-run* ordering is
dominated by JEV's arbitrary tie-break; the lifetime column is the reliable signal.)

**Distinct low axes (not the same defect):**
- `civ-formal` — lowest **novelty** (1.494 lifetime; 1.632 precise, 1.625 engineer).
  Distinct dimension from grounded's alignment deficit.
- `civ-precise` — lowest **quality** (0.771) but **highest alignment** (2.606) and
  **best win_rate** (0.491). An inverse axis, not a low-relevance civ.

### Stable inverse
`civ-poetic` is **1st on quality** (1.143) and **last on win_rate** (0.017). A
*selection* failure, not a quality collapse.

### Extinction risk: NONE
Threshold is −10; lowest raw relevance is **+797.20** (civ-grounded) — 80× above the
threshold. Registry 8 civs, `max_civs` 12 ⇒ 4 birth slots free. Birth/extinction only
runs under `--loop`, which was not used.

### Counter gap (structural, unchanged)
Registry `simulations_run` totals **4824**; ledger rows total **5084** ⇒ **gap +260**,
identical to the standing finding. `save_state()` rewrites `culture.json` with no lock
⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.

---

## 6. Changes to the repo (18 files)

- 8 × `civ-*/simulations.jsonl` (+10 rows each)
- 8 × `civ-*/culture.json` (relevance, wins/losses, simulations_run)
- `leaderboard.json` (regenerated)
- `meta_log.jsonl` (+5 rows)

No deletions, no flattening, no stray artifacts.

---

## 7. Carry-forward notes

1. **NAS EDQUOT is TOTAL (4th session running).** `mkdir` works; every write truncates to
   0 bytes. Only the symlink bridge works. Verify by inode identity, never by `ls`.
2. **The `ls` race on the symlinked deep path did NOT reproduce** this session (every
   `ls` succeeded). Keep the documented `stat -L` + `readlink -f` + `[-e]` + retry
   diagnostic anyway.
3. **`gh` is not installed — 4th session running.** Use
   `GET /search/repositories?q=ai-writings` with `GITHUB_TOKEN`; the API is
   case-insensitive (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
4. **Tool timeout (30 s) < orchestrator run (~45 s).** Launch detached with stdout
   redirected to a file, then poll `ps` + the log. Do not expect the launch call to block.
5. **NEW — Control B has a HARD blind spot: the chooser cannot discriminate at all.**
   **Verified, not inferred.** In the competition phase, all 8 civs' `content_preview` is
   **byte-identical** — one distinct preview per civ, and the *same* preview for all 8 civs
   on all 5 prompts (mock seed `youareav` throughout). The 8 "candidates" JEV compares are
   literally the same string, so the chooser has nothing to discriminate on and its pick is
   an arbitrary tie-break. That is exactly why `civ-precise` took 5/5: **not evidence of
   dominance.** A Control B run therefore **cannot** reproduce the session-116
   chooser-vs-argmax finding, and the within-run competition ordering is **not a valid
   quality measurement**. Only the lifetime columns are trustworthy signal.
   *Root cause:* the mock's seed is `re.sub(r"[^a-zA-Z0-9]", "", msg)[:8]`, which takes the
   **first 8 alphanumeric chars** of the cultural prompt — and the cultural prompt begins
   with the **civ-invariant** prefix `You are a voice in the tradition of "…`, so the slice
   lands on `YouAreA` and never reaches the civ-specific `voice_emphasis` / `tenets`.
   *Fix for the next session:* hash the **whole** message (or a hash of the civ's voice
   fields + prompt) instead of slicing the first 8 chars, so each civ gets distinct text
   and the chooser becomes a real test again. Not yet fixed here — this run is a
   **mock-limited** run and is labelled as such.
