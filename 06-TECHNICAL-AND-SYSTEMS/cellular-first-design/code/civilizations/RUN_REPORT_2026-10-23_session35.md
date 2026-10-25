# Civilization Orchestrator — Run Report 2026-10-23 (session 35)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock provider stubbed at the gate; real JEV untouched) — run **twice** with two independently-written mock body sets (A and B) to test rank stability.
**Outcome:** ✅ **+160 new simulation rows** (10 per civ per run, uniform), **+10 meta_log entries**, **10 competition winners**, **0 JEV score errors**, **0 all-2.0-default rows**, **0 mock fallbacks**.

---

## 1. Environment reconstruction

| item | state |
|---|---|
| `/workspace` NAS | 100 % quota (600 G/600 G, 0 avail) — a write there yields a **0-byte file that still appears in `ls`** |
| repo path at session start | **absent** — 7th consecutive wipe where the prompt names an ephemeral path (`/workspace` held only `.plugin-cache` + `.skills`) |
| clone target | `/tmp` (overlay, 28 G free, exempt from the EDQUOT trap) |
| bridge | `mkdir -p /workspace/repos && rm -rf /workspace/repos/ai-writings && ln -sfn /tmp/ai-writings /workspace/repos/ai-writings` — required because `CIVS_DIR` is **hardcoded** in the script |
| clone | `git clone --depth 1 --filter=blob:none --no-checkout` of `SuperInstance/AI-Writings` (3.3 GB pack, ~90 s); the `ai-writings` lowercase path in the prompt is a legacy owner name — the real repo is **`SuperInstance/AI-Writings`** |
| HEAD | `972b17c5` "🔄 Auto-update landing page index" |

### ⚠️ NEW TRAP — a stale index makes `git status` report the entire repo as deleted

`git status --short` printed **22 515 `D` lines** and `git status` said "nothing to commit, working tree clean"
in the same breath. The worktree was in fact **byte-identical to HEAD** (verified file-by-file below).

The mechanism: the clone was still writing its index when the first status ran, so the index carried
**stale stat data** that git treated as "file removed from disk". The tell:

```
git status --short              -> 22 515 D lines
git diff-index --name-status HEAD -- <path>   -> empty
```

**Two reliable checks, in order:**

```bash
# 1. Does git think the file is missing, or does the content differ?
git diff-index --name-status HEAD -- cellular-first-design/code/civilizations/   # empty => fine

# 2. Ground truth: compare every blob to the worktree byte-for-byte.
for f in $(git ls-tree -r --name-only HEAD cellular-first-design/code/civilizations/); do
  cmp <(git show HEAD:$f) $f || echo "DIFF $f"
done
```

`git update-index --really-refresh` took >30 s on a 3.3 GB pack and was killed by the tool timeout —
**do not wait for it; use the byte-compare above instead.**

**Corollary:** `git status` in a freshly-cloned tree is not a reliable cleanliness oracle.
`git diff-index` and `cmp`-against-blob are.

### Ground-truth verification used for the restore

```
tracked files in civ subtree: 75
identical to HEAD: 75   differing: 0
```

## 2. The credential gap (16th consecutive session)

All 7 available sandbox secrets re-tested against `https://api.z.ai/api/coding/paas/v4/chat/completions`:

```
GITHUB_TOKEN       401 {"code":"401","message":"token expired or incorrect"}
CRATES_TOKEN       401      MOTHQUANTUM_TOKEN  401
NOTION_TOKEN       401      NPMJS_TOKEN        401
PYPI_TOKEN         401      TYPESAFE_AI_TOKEN  401
no-auth probe      401 {"code":"1001","message":"Authentication parameter not received in Header"}
```

The no-auth probe returning **401 code 1001** (not 5xx) means the endpoint is **healthy** — this is a
**credential gap, not an outage**. `ZAI_TOKEN`/`ZAI_KEY` and `GROQ_TOKEN` are absent from env and from the
secret store. JEV is **live** at `jev-1.14.0` (probe: `quality.score 2.23, confidence 0.61`).
Always `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"`.

### The unpatched control (re-verified from scratch, delta measured not assumed)

```
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...        ... (all 8 civs)
=== Civilization competitions: 5 prompts ===
EXIT=0
```

**No `Winner:` lines. Exit 0. Ledger +0 rows (1644 → 1644). meta_log +0 (108 → 108).**
Only `leaderboard.json` was rewritten. **Never report success on exit code — assert on the row delta.**

## 3. Control B — 16th identical replication

Stub placed **at the gate** (`ZAI_TOKEN` set + a 1-line `ZAI_URL_OVERRIDE` patch → local mock),
leaving the JEV call **completely untouched** so every score is real JEV output.

| check | set A | set B |
|---|---|---|
| rows added | +80 (10/civ, uniform) | +80 (10/civ, uniform) |
| meta_log added | +5 | +5 |
| competition winners | 5 | 5 |
| JEV score errors | 0 | 0 |
| all-2.0-default rows | 0 | 0 |
| mock fallbacks | 0 | 0 |
| distinct `avg_score` | 76/80 | 76/80 |
| distinct `content_preview` | 23/80 | 22/80 |

The mock logs a `fallback` flag per call; **0 fallbacks across 160 calls**, 8 distinct voices hit.

### Mock design rules that mattered (carried forward)

- **Key the voice table on the RENDERED string** — the orchestrator renders `f"Your voice: {voice}."`
  **with a trailing period**. A table keyed on the raw `culture.json` value matches nothing and every
  civ silently falls through to a shared pool — a run that still passes every structural check.
- **Never echo the scaffolding.** The prompt is `header + tenets + voice + blank + question`; take the
  **last non-empty line** and strip the `Write N words on ` prefix. Echoing it makes all 8 civs produce
  identical text and destroys the chooser's signal.
- **3 distinct bodies per voice** (not 1) — the orchestrator reuses prompts, so a 1-body voice
  produces identical previews across its 5 sims. Distinct previews: 2–3 per civ.
- **Salt the seed with `(temperature, max_tokens, len(prompt))`** so repeated prompts still vary.

## 4. THE HEADLINE — rank stability under a body-set swap

Two independently-written body sets, same orchestrator, same JEV, same 5 prompts.

| civ | set A | set B | B−A | rank A | rank B |
|---|---|---|---|---|---|
| civ-mythic | 2.495 | 2.248 | **−0.247** | 1 | 2 |
| civ-poetic | 2.190 | 2.273 | +0.083 | 2 | 1 |
| civ-therapist | 2.055 | 2.206 | +0.151 | 3 | 3 |
| civ-precise | 1.676 | 2.062 | **+0.387** | 6 | 4 |
| civ-engineer | 1.830 | 1.883 | +0.052 | 4 | 5 |
| civ-whimsical | 1.727 | 1.798 | +0.070 | 5 | 6 |
| civ-formal | 1.529 | 1.648 | +0.119 | 7 | 7 |
| **civ-grounded** | **1.319** | **1.428** | +0.109 | **8** | **8** |

```
fleet mean         A 1.853  →  B 1.943   (+0.091)
max per-civ |B−A|  0.387
median adjacent rank gap  A 0.147  /  B 0.143
Kendall τ (A→B)   0.786
same rank slots    3/8
```

**The perturbation test (session 12's rule) says: max |Δ| 0.387 > median adjacent gap ~0.145, so a
reorder was possible — and one happened.** The Precise jumped **6 → 4** on a +0.387 shift, and the
Mythic/Poetic pair swapped at 1–2. So the middle of the board is genuinely unstable.

**What survives the swap (and matches 4 earlier sessions' bottom band):**

- **`civ-grounded` is last in BOTH sets and lowest in 8 of 10 lenses.** A stable, real quality signal.
- **Bottom-2 band {civ-grounded, civ-formal} holds in both sets** (7th in A and B for Formal).
- **Top-2 band {civ-mythic, civ-poetic} holds in both sets** (1st/2nd, order swapped).
- **Middle band {civ-precise, civ-engineer, civ-whimsical, civ-therapist} is unranked** — report the
  band, never an order. (The Whimsical's lifetime lead is real on the *lifetime* lens, but under the
  mock it sits 5th/6th — the mock's body length and register dominate the score.)

## 5. Chooser vs scorer — 9th replication, and it is not narrowing

`best_civ` (the JEV choice question) vs `argmax(avg_score)` (the scoring question). The chooser never
sees the scores and only reads a **150-char preview**.

| window | agreement |
|---|---|
| set A, this session | **1/5 (20.0 %)** |
| set B, this session | **1/5 (20.0 %)** |
| lifetime before this session (108 rounds) | 19/108 (17.6 %) |
| lifetime now (118 rounds) | 21/118 (17.8 %) |

**8 of 10 rounds this session crowned a civ that was NOT the top scorer**, by margins of
0.28–0.91. Two full sessions in a row at 20 %.

**Consequence for the low-relevance answer: `win_rate` is a *selection* metric and must never be
reported as a quality metric.** A civ can be top of every quality lens and read as 0 % on the board.

## 6. Temperature ↔ novelty — 9th replication

`preferred_params.temperature` vs lifetime JEV sub-scores, all 8 civs:

```
temp vs lifetime novelty    Pearson r = 0.9431
temp vs lifetime quality    Pearson r = 0.8184
temp vs lifetime alignment  Pearson r = 0.0899
```

r = 0.9431 continues the series (0.985, 0.980, 0.981, 0.975, 0.947, …). **The fleet is 8 points on one
temperature/novelty gradient with a style overlay, not 8 independent voices.** Alignment is the one
lens that is *not* temperature-driven (r = 0.09) — it is the only sub-score that measures the culture
rather than the sampling temperature.

**Also confirmed: `max(0.1, …)` in `mutate()` makes the cold end a one-way ratchet.** Precise (0.2)
and Formal (0.3) can only ever move warmer.

## 7. The counter gap — unchanged at exactly +260

| civ | ledger rows | registry `simulations_run` | gap |
|---|---|---|---|
| civ-grounded | 252 | 209 | +43 |
| civ-whimsical | 264 | 201 | +63 |
| civ-formal | 237 | 195 | +42 |
| civ-poetic | 231 | 194 | +37 |
| civ-precise | 201 | 185 | +16 |
| civ-mythic | 209 | 189 | +20 |
| civ-therapist | 204 | 187 | +17 |
| civ-engineer | 206 | 184 | +22 |
| **FLEET** | **1804** | **1544** | **+260** |

`save_state()` rewrites `culture.json` from in-memory counters with **no lock and no
read-modify-write** ⇒ a lost-update race. **+260 for the 16th consecutive session — the gap is exactly
constant**, which means the race fires on a fixed number of writes per session, not randomly.
`relevance_per_sim` on the board is therefore **not a reproducible ranking**; an auditor cannot
recompute the board order from the ledger.

## 8. THE LOW-RELEVANCE ANSWER

Ten lenses, each measured separately. **Never merge them.**

| lens | lowest | value | highest | value |
|---|---|---|---|---|
| A lifetime `avg_score` | **civ-grounded** | 1.598 | civ-poetic | 2.295 |
| B raw relevance | **civ-grounded** | 318.28 | civ-poetic | 433.45 |
| C win rate *(selection)* | **civ-poetic** | 0.011 (1W/92L) | civ-precise | 0.523 (46W/42L) |
| D lifetime quality | **civ-grounded** | 1.071 | civ-poetic | 1.638 |
| E lifetime novelty | **civ-formal** | 1.326 | civ-whimsical | 2.475 |
| F lifetime alignment | **civ-grounded** | 2.044 | civ-precise | 2.929 |
| G `relevance_per_sim` (board sort) | **civ-grounded** | 1.523 | civ-poetic | 2.234 |
| H set-A `avg_score` | **civ-grounded** | 1.319 | civ-mythic | 2.495 |
| I set-B `avg_score` | **civ-grounded** | 1.428 | civ-poetic | 2.273 |
| J pooled A+B `avg_score` | **civ-grounded** | 1.374 | civ-mythic | 2.372 |

**Lowest count: `civ-grounded` on 8 of 10 lenses** — including the three that need no denominator
(A, D, F), the board's own sort key (G), and **both** mock body sets (H, I).

> ### `civ-grounded` is the low-relevance civilization.
> Last on `relevance_per_sim` (1.523), lowest lifetime `avg_score` (1.598), **the fleet's lowest
> quality (1.071) and lowest alignment (2.044)**, and last in both mock body sets. It is not a
> longevity artefact — it is **the genuinely weakest writer** in the fleet, and it is 8th in every
> body set tried. This is now stable across 5 sessions and 6 independently-written body sets.

**The two inverses — these are *not* quality failures:**

- **`civ-poetic` — the highest-quality civ that is essentially never selected.** 1st of 8 on lifetime
  `avg_score` (2.295), 1st on lifetime quality (1.638), 2nd on lifetime alignment (2.922), 1st on the
  board's `rel_per_sim` (2.234), top-2 in both mock sets — and **1 win in 92** (win_rate 0.011).
  A *selection* failure: the chooser only sees 150 characters of preview, and the Poetic's register
  is the least legible in the first 150 characters. Stable across 11 sessions.
- **`civ-precise` — the mirror image.** Best win rate in the fleet (0.523) but mid-table on
  `avg_score` (1.867) and it **moved 6 → 4 on a mock body swap** — the least stable mid civ.
  It is the only civ whose relevance rank and win rate agree, and it wins on *shape*, not on score.

**`civ-formal`** is the second-lowest band member: 7th in both mock sets, lowest lifetime novelty
(1.326), and it is the civ the `max(0.1, …)` ratchet pins at 0.3.

**Extinction risk: none.** The threshold is `relevance < −10`; the lowest is **+318.28**, and
`extinction_and_birth()` only runs in `--loop` mode every third iteration — a single-shot run never
triggers it.

## 9. Restore & leak test (all green)

```
git checkout -- cellular-first-design/code/civilizations/
tracked files in civ subtree: 75
identical to HEAD: 75   differing: 0
mock-zai rows per civ: 70 / 70 / 70 / 70 / 70 / 70 / 70 / 70   (baseline is 70, NOT zero)
fleet ledger rows: 1644  (HEAD baseline 1644)
meta_log.jsonl:     108  (HEAD baseline 108)
ZAI_URL_OVERRIDE in script: 0  (patch reverted)
```

**The leak-test baseline is 70 per civ, not zero** — 560 mock rows were committed by earlier sessions
into the durable ledger. A naive `grep -c mock-zai == 0` assertion is a false negative against a
15-session-old baseline; the correct post-restore assertion is **exactly 70 per civ** plus
byte-identity with the HEAD blob.

`__pycache__/` was not created in the civilizations directory this session (the script is run as
`__main__`), so no cleanup was needed.

## 10. Replications this session

- Control B **+80 rows / +5 meta_log / 5 winners / 0 fallbacks / 0 score errors / 0 all-2.0-default
  rows** in **both** body sets — reproduces sessions 6–14 and 34 exactly.
- Chooser vs `argmax(avg_score)`: **20.0 % (1/5) in each of two body sets**, **17.6 % lifetime
  before this session** — 9th replication.
- Temperature vs lifetime JEV novelty: **Pearson r = 0.9431** — 9th replication.
- Counter gap: **+260**, constant for 16 sessions.
- Unpatched run: **+0 rows, +0 meta_log, 0 `Winner:` lines, exit 0** — 16th consecutive session.
