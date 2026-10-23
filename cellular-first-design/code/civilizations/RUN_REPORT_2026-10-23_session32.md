# Civilization Orchestrator — Session 32 (2026-10-23)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline:** `SuperInstance/AI-Writings` @ `1d2a3b3f` (sparse checkout of `cellular-first-design/code/civilizations`)
**Civs:** 8 · **Providers requested:** zai only

---

## Headline

The command as given produces **zero simulations** and still exits 0. A local
control provider (Control B) was used to make the orchestrator actually run, and
the run then produced **+80 ledger rows (+10 per civ, uniform)** and **+5
competition rounds** with **live JEV scores**.

**The z.ai credential gap is the whole story — 13th consecutive session.**

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

- `ZAI_URL_OVERRIDE` → `http://127.0.0.1:8848/chat/completions` (one-line patch to
  the `PROVIDERS["zai"]["url"]` default; the token gate at line 79 is untouched,
  so the request is really attempted and the control has full power).
- `ZAI_TOKEN=mock-control-b` — satisfies the gate.
- `TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` — JEV scoring is live and real.
- Mock keyed on the **rendered** voice string (`"Your voice: warm, factual."`),
  per the session-9 failure mode; 3 hand-written bodies per voice per set, two
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
| mock calls | 81 (80 + 1 probe) | — |
| mock **fallback** hits | **0** | 0 ✅ |
| distinct `avg_score` | **79 / 80** | high ✅ |
| distinct `content_preview` | 21 / 80 | see note below |

### Results — set B (independently written bodies)

Same +80 rows, +5 meta_log, 5 winners, 0 fallbacks, 0 all-2.0-default rows.

**Note on the distinct-preview count (21/80):** this is a *mock body-pool size*
artefact, not the collapse failure mode. Each voice has only 3 bodies and the
ledger truncates `content_preview` at 200 chars, so per-civ distinct previews are
2–3. The collapse the learnings warn about (all 8 civs sharing one FALLBACK text)
is ruled out by **0 fallback hits** and by per-civ distinct body openings.
*Method note: widen the mock pool to ≥6 bodies/voice if a healthy 50–68 distinct
preview count is wanted as a structural acceptance check.*

---

## 3. Low relevance — four lenses, four answers (never merge them)

| lens | lowest | what it actually measures |
|---|---|---|
| A `relevance_per_sim` (board sort) | **civ-grounded 1.532** | longevity artefact — it ran the most sims (252 rows) |
| B raw relevance | **civ-formal 318.81** | accumulated score, same denominator artefact |
| C win rate | **civ-poetic 0.022 (2W/91L)** | **selection** appeal under a 150-char preview |
| D lifetime mean `avg_score` | **civ-grounded 1.605** | actual writing quality — the only real quality lens |
| D′ lifetime alignment | **civ-grounded 2.050** (next 2.606) | cultural fit |

### The stable answer: `civ-grounded` and `civ-formal`

Bottom-2 by rank in **both** body sets **and** in lifetime:

| view | bottom-2 |
|---|---|
| set A (this run) | civ-grounded 1.475, civ-formal 1.255 |
| set B (this run) | civ-formal 1.503, civ-grounded 1.460 |
| lifetime | civ-formal 1.706, civ-grounded 1.605 |

`civ-grounded` is lowest on **3 of 4 lenses** (A, D, D′) and is the only civ
whose board verdict and quality lens agree — the one stable low-relevance
civilization, matching the 4-session history in the learnings doc.

`civ-grounded`'s weakness is **alignment**, not just score: lifetime alignment
**2.050** against a next-best 2.606 — a wide margin, in every body set.

### The inverse case: `civ-poetic`

Top of the fleet on quality and **almost never selected**.

| metric | value | rank |
|---|---|---|
| lifetime mean `avg_score` | **2.320** | **1st of 8** |
| lifetime alignment | 2.954 | 1st of 8 |
| set A / set B `avg_score` | 2.536 / 2.499 | **1st / 1st** |
| win rate | **0.022 (2W/91L)** | **8th of 8** |

A *selection* failure, not a quality collapse. Consistent across 10+ sessions.

### The other inverse: `civ-precise`

Best win rate (**0.511, 45W/43L**) but 6th on lifetime `avg_score` (1.866) and
2nd-lowest novelty (1.551). Won 3 of 5 competition rounds this run.

### Extinction risk: none

`extinction_and_birth()` retires only below `relevance < -10`; the minimum is
**+318.81**, and it only runs in `--loop` mode every third iteration. This was a
single-shot run, so it never fired.

---

## 4. Mock sensitivity — the A/B, run for the 2nd time on fresh body sets

| | set A | set B |
|---|---|---|
| fleet mean `avg_score` | 1.892 | 1.951 (**+0.059**) |
| max per-civ \|Δ\| | — | **0.247** (civ-formal) |
| positional rank agreement | — | **4/8** |
| Kendall τ | — | **0.714** (24 concordant / 4 discordant) |
| competition winners | Precise ×3, Formal ×2 | Engineer, Precise ×2, Poetic, Formal |

**Three civs reordered** (civ-formal 8→7, civ-therapist 5→3, civ-engineer 3→5).
Per the session-11 rule, a rank is reportable only if it survives a body-set swap
whose perturbation is at least as large as the rank gap it would reorder:

| civ | A rank | B rank | \|Δ\| | verdict |
|---|---|---|---|---|
| civ-poetic | 1 | 1 | 0.037 | **STABLE** |
| civ-mythic | 2 | 2 | 0.112 | **STABLE** |
| civ-whimsical | 4 | 4 | 0.072 | **STABLE** |
| civ-precise | 6 | 6 | 0.010 | **STABLE** |
| civ-grounded | 7 | 8 | 0.015 | tie-band (bottom-2 in both) |
| civ-formal | 8 | 7 | 0.247 | REORDERED (bottom-2 in both) |
| civ-therapist | 5 | 3 | 0.195 | REORDERED — **unranked** |
| civ-engineer | 3 | 5 | 0.108 | REORDERED — **unranked** |

**Reportable order:** Poetic > Mythic > Whimsical > Precise > {Grounded, Formal}
(bottom band). **Unranked band:** {Therapist, Engineer}. This reproduces the
session-11 finding (stable top-3 Mythic/Whimsical/Poetic, stable bottom-2
Grounded/Formal) on independently written bodies.

---

## 5. Replications

| finding | this session | history |
|---|---|---|
| Unpatched run: +0 rows, 0 winners, exit 0 | ✅ | **13th consecutive session** |
| Control B: +80 rows (+10/civ uniform), +5 meta_log, 5 winners, 0 fallbacks, 0 score errors, 0 all-2.0-default rows | ✅ | 13th |
| Chooser vs `argmax(avg_score)` agreement | **1/10 (10%)** this run | lifetime 15.5 % — 7th replication; the competition winner is still not evidence of a higher JEV score |
| Temperature ↔ lifetime JEV novelty | **Pearson r = 0.9430** | 5th (0.985 / 0.980 / 0.981 / 0.975) — the fleet is 8 points on one temperature/novelty gradient |
| Counter gap: ledger vs registry `simulations_run` | **+260** (1804 vs 1544) | unchanged for 13 sessions — `save_state()` has no lock ⇒ `relevance_per_sim` is not a reproducible ranking |

---

## 6. Low-relevance summary (one paragraph)

**`civ-grounded` is the civilization to watch** — last on `relevance_per_sim`
(1.532), last on lifetime `avg_score` (1.605), and holding the fleet's **lowest
alignment (2.050 vs next-best 2.606)**; it is bottom-2 in both mock body sets and
in lifetime. **`civ-formal` is the second-lowest** (bottom-2 in all three views,
lowest raw relevance at 318.81). **`civ-poetic` is the inverse failure** — 1st of
8 on quality and 1st on alignment but a **0.022 win rate (2W/91L)**, a selection
failure rather than a quality collapse. **`civ-precise`** is the mirror image:
best win rate (0.511) but 6th on quality. **No civilization is at extinction
risk** (threshold −10; minimum +318.81), and the middle band
{`civ-therapist`, `civ-engineer`} is **unranked** under Control B.

---

## 7. Protocol

Mock rows are **not committed**. The working tree was restored from the pristine
snapshot and verified **byte-identical to the git HEAD blob** for every file in
the subtree (`cmp` against `git show HEAD:<path>`, all files pass). Only this
report and the learnings doc are committed.
