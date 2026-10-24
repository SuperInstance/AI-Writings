# Civilization Orchestrator — Session 33 (2026-10-23)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline:** `SuperInstance/ai-writings` @ `0439197` (blobless sparse checkout of `cellular-first-design/code/civilizations`)
**Civs:** 8 · **Providers requested:** zai only · **Runs:** A (set-A bodies) + B (set-B bodies, independently written)

---

## Headline

The command as given produces **zero simulations** and still exits 0. A local
control provider (Control B) was used to make the orchestrator actually run, and
the two independent runs then produced **+80 ledger rows (+10 per civ, uniform)**
and **+5 competition rounds** per run with **live JEV scores**.

**The z.ai credential gap is the whole story — 14th consecutive session.**

---

## 1. Credential audit (why the command as given does nothing)

| check | result |
|---|---|
| `ZAI_TOKEN` in env | **absent** |
| `ZAI_TOKEN` in the 8-entry secret store | **absent** |
| `GROQ_TOKEN` | **absent** — no alternate live provider |
| all 8 sandbox secrets → z.ai coding endpoint | **HTTP 401 "token expired or incorrect"** (every one) |
| z.ai endpoint health, no auth header | **HTTP 401 code 1001 "Authentication parameter not received"** |
| groq endpoint | **HTTP 401 "Invalid API Key"** |
| JEV `https://api.typesafe.ai/v1/systemone` | **LIVE — `jev-1.14.0`** |

A 401 (not 5xx) means the endpoints are healthy ⇒ **credential gap, not outage.**

Provider gate, `civilization_orchestrator.py:79`:
```python
token = os.environ.get(p["env"], "")
if not token: return None        # silent drop
```

**Env-var naming note (new this session):** the script reads `TYPESAFEAI_KEY`,
but the sandbox exposes the JEV credential as `TYPESAFE_AI_TOKEN`. A run without
`TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` silently degrades every JEV score to the
`{quality: 2.0, novelty: 2.0, alignment: 2.0, confidence: 0.5}` default — the
**all-2.0-default signature** the acceptance checks look for. Export
`TYPESAFEAI_KEY` explicitly, or the scores are fake and the run still exits 0.

### Unpatched run — measured, not assumed

```
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...      … all 8 printed …
=== Civilization competitions: 5 prompts ===
                                    ← NO Winner: lines
EXIT: 0
```

| metric | before | after | delta |
|---|---|---|---|
| ledger rows (8 civs) | 1644 | 1644 | **+0** |
| `meta_log.jsonl` | 108 | 108 | **+0** |
| `Winner:` lines | — | **0** | — |
| exit code | — | **0** | — |
| `leaderboard.json` | — | rewritten (same values) | — |

The per-civ `running 5 sims...` lines print **before** the provider call, so they
are not evidence of work. **Assert on the row delta, never on the exit code.**

---

## 2. Control B — the run that actually did something

Mock at the gate (below the failing line), JEV left untouched and live.

- `ZAI_URL_OVERRIDE` → `http://127.0.0.1:8848/chat/completions` (one-line patch to the
  `PROVIDERS["zai"]["url"]` default; the token gate at line 79 is untouched, so the
  request is really attempted and the control has full power).
- `ZAI_TOKEN=mock-control-b` — satisfies the gate.
- `TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` — JEV scoring is live and real.
- Mock keyed on the **rendered** voice string (`"Your voice: warm, factual."`),
  per the session-9 failure mode; **8 hand-written bodies per voice per set**, two
  independently written body sets (A/B); every call logged with a `fallback` flag.

### Results — set A

| metric | value | expected |
|---|---|---|
| ledger rows | **1644 → 1724 (+80)** | +80, +10/civ uniform ✅ |
| per-civ growth | **+10 each, all 8** | uniform ✅ |
| `meta_log.jsonl` | **108 → 113 (+5)** | +5 ✅ |
| `Winner:` lines | **5** | 5 ✅ |
| rows with `scores.error` | **0** | 0 ✅ |
| all-2.0-default rows (JEV-outage signature) | **0** | 0 ✅ |
| mock calls | 80 | — |
| mock **fallback** hits | **0** | 0 ✅ |
| distinct `avg_score` | **74 / 80** | high ✅ |
| min per-civ distinct `content_preview` | **3** | >1 per civ ✅ |

### Results — set B (independently written bodies)

Same +80 rows, +5 meta_log, 5 winners, 0 fallbacks, 0 all-2.0-default rows,
min per-civ distinct previews 3.

---

## 3. Low relevance — four lenses, four answers (never merge them)

| lens | lowest | what it actually measures |
|---|---|---|
| A `relevance_per_sim` (board sort) | **civ-grounded 1.558** | longevity artefact — it ran the most sims (199 rows) |
| B raw relevance | **civ-formal 306.76** | accumulated score, same denominator artefact |
| C win rate | **civ-poetic 0.011 (1W/87L)** | **selection** appeal under a 150-char preview |
| D lifetime mean `avg_score` | **civ-grounded 1.628** | actual writing quality — the only real quality lens |
| D′ lifetime alignment | **civ-grounded 2.079** (next 2.603) | cultural fit |

### The stable answer: `civ-grounded` and `civ-formal`

Bottom-2 by rank in **both** body sets **and** in lifetime:

| view | bottom-2 |
|---|---|
| set A (this run) | civ-formal 1.470, civ-precise 1.764 |
| set B (this run) | civ-grounded 1.727, civ-formal 1.748 |
| lifetime | civ-formal 1.724, civ-grounded 1.628 |
| board `relevance_per_sim` | civ-grounded 1.558, civ-formal 1.658 |
| lifetime alignment | civ-grounded 2.079, civ-therapist 2.603 |

`civ-grounded` is lowest on **3 of 4 lenses** (A, D, D′) and is the only civ
whose board verdict and quality lens agree — the one stable low-relevance
civilization, matching the multi-session history in the learnings doc.

`civ-grounded`'s weakness is **alignment**, not just score: lifetime alignment
**2.079** against a next-best 2.603 — a wide margin, in every body set.

### The inverse case: `civ-poetic`

Top of the fleet on quality and **almost never selected**.

| metric | value | rank |
|---|---|---|
| lifetime mean `avg_score` | **2.309** | **1st of 8** |
| lifetime alignment | 2.935 | 1st of 8 |
| lifetime quality | 1.668 | 1st of 8 |
| win rate | **0.011 (1W/87L)** | **8th of 8** |

A *selection* failure, not a quality collapse. Consistent across 10+ sessions.

### The other inverse: `civ-precise`

Best win rate (**0.506, 42W/41L**) but 5th on lifetime `avg_score` (1.862) and
2nd-lowest novelty (1.484). Won 3 of 5 competition rounds in set A, 2 of 5 in set B.

### Extinction risk: none

`extinction_and_birth()` retires only below `relevance < -10`; the minimum is
**+305.92** (set A) / **+308.07** (set B), and it only runs in `--loop` mode
every third iteration. This was a single-shot run, so it never fired.

---

## 4. Mock sensitivity — the A/B, run for the 3rd time on fresh body sets

| | set A | set B |
|---|---|---|
| fleet mean `avg_score` | 1.980 | 2.201 (**+0.221**) |
| max per-civ \|Δ\| | — | **0.469** (civ-engineer) |
| positional rank agreement | — | **2/8** |
| Kendall τ | — | **+0.571** (22 concordant / 6 discordant) |
| competition winners | Precise ×3, Formal, Engineer | Precise ×2, Formal, Grounded, Engineer |
| chooser vs `argmax(avg_score)` | **0/5** | **0/5** |

**Five civs reordered** (civ-mythic 3→1, civ-grounded 5→8, civ-engineer 6→5,
civ-precise 7→6, civ-formal 8→7). Per the session-11 rule, a rank is reportable
only if it survives a body-set swap whose perturbation is at least as large as
the rank gap it would reorder:

| civ | A rank | B rank | \|Δ\| | verdict |
|---|---|---|---|---|
| civ-poetic | 1 | 3 | 0.002 | top band, survives |
| civ-therapist | 2 | 2 | 0.335 | **STABLE** |
| civ-whimsical | 4 | 4 | 0.185 | **STABLE** |
| civ-mythic | 3 | 1 | 0.423 | REORDERED — **unranked** |
| civ-grounded | 5 | 8 | 0.164 | REORDERED — **unranked** (bottom-2 in both) |
| civ-formal | 8 | 7 | 0.279 | REORDERED (bottom-2 in both) |
| civ-engineer | 6 | 5 | 0.469 | REORDERED — **unranked** |
| civ-precise | 7 | 6 | 0.244 | REORDERED — **unranked** |

**Reportable order (stable):** Whimsical > Therapist, with Poetic in the top band
and **{Grounded, Formal}** the bottom band. **Unranked band:** {Mythic, Engineer,
Precise}. The stable bottom-2 pair **{Grounded, Formal}** reproduces the
session-11/32 finding on independently written bodies.

> **Method note (new this session):** the set-B fleet mean ran **+0.221** above
> set A — larger than the gap separating several adjacent ranks. A single-body-set
> run is therefore **not** sufficient to rank the middle of this fleet, and any
> report that quotes a mid-fleet rank from one mock set is over-claiming. The
> lifetime view (all rows) is more stable than either single run and is the view
> that the low-relevance answer rests on.

---

## 5. Replications

| finding | this session | history |
|---|---|---|
| Unpatched run: +0 rows, 0 winners, exit 0 | ✅ | **14th consecutive session** |
| Control B: +80 rows (+10/civ uniform), +5 meta_log, 5 winners, 0 fallbacks, 0 score errors, 0 all-2.0-default rows | ✅ | 14th |
| Chooser vs `argmax(avg_score)` agreement | **0/5 (0%)** this run | lifetime 15.5 % — 8th replication; the competition winner is still not evidence of a higher JEV score |
| Temperature ↔ lifetime JEV novelty | **Pearson r = 0.9553 / 0.9539** | 6th (0.985 / 0.980 / 0.981 / 0.975 / 0.943 / 0.953) — the fleet is 8 points on one temperature/novelty gradient |
| Counter gap: ledger vs registry `simulations_run` | **+260** (1724 vs 1464) | unchanged for 14 sessions — `save_state()` has no lock ⇒ `relevance_per_sim` is not a reproducible ranking |
| Low-relevance answer | `civ-grounded` + `civ-formal` | stable across 10+ sessions |
| Inverse case | `civ-poetic` 1st on quality, 0.011 win rate | stable across 10+ sessions |

---

## 6. Low-relevance summary (one paragraph)

**`civ-grounded` is the civilization to watch** — last on `relevance_per_sim`
(1.558), last on lifetime `avg_score` (1.628), and holding the fleet's **lowest
alignment (2.079 vs next-best 2.603)**; it is bottom-2 in both mock body sets and
in lifetime. **`civ-formal` is the second-lowest** (bottom-2 in all three views,
lowest raw relevance at 306.76). **`civ-poetic` is the inverse failure** — 1st of
8 on quality, novelty and alignment but a **0.011 win rate (1W/87L)**, a selection
failure rather than a quality collapse. **`civ-precise`** is the mirror image:
best win rate (0.506) but 5th on quality. **No civilization is at extinction
risk** (threshold −10; minimum +305.92), and the middle band
{`civ-mythic`, `civ-engineer`, `civ-precise`} is **unranked** under Control B.

---

## 7. Protocol

Mock rows are **not committed**. The working tree was restored from the pristine
snapshot and verified **byte-identical to the git HEAD blob for all 72 files in
the subtree** (`git show HEAD:<path> | cmp - <path>`, all pass; `git status
--short` empty). Only this report and the learnings doc are committed.

---

## 8. Environment notes (durable)

- **`/workspace` is a quota-capped NAS mount at 100%** — writes silently create
  **0-byte files** that still appear in `ls`. `/tmp` (overlay) has 28 GB free and
  is not subject to the trap. A `git clone` into `/workspace` dies with
  `Disk quota exceeded`; the same clone into `/tmp` succeeds.
- **The full `ai-writings` clone fails on a ~2 GB pack** (`could not open
  .../tmp_pack_* for reading`). Use
  `git clone --filter=blob:none --no-checkout --depth 1` then
  `git sparse-checkout set <subtree>` — the whole `cellular-first-design/code/civilizations`
  subtree materialises in seconds and the clone is under 1 MB.
- **Symlinks on the NAS work** and can bridge a quota-capped `/workspace` path to
  a `/tmp` backing store, which is how the script's hardcoded
  `CIVS_DIR = /workspace/repos/ai-writings/...` was satisfied without patching it.
- **The NAS mount occasionally returns `No such file or directory` for a path
  that exists**; a short retry loop resolves it.
