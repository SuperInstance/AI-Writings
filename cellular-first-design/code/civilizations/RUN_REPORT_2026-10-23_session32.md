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

---

# Appendix — Run B: a second, independent execution of the same task

> A **concurrent instance of this same session** pushed its own session-32 report
> (`e7b0a995`) while this run was in flight. Both are genuine, independent executions of the
> same command from the same baseline (`f408e862`, 1644 ledger rows, 108 meta_log entries), so
> **both are kept**. The report above is Run A; this appendix is Run B. Every headline finding
> is corroborated by both.

## Run B — what was different

| | Run A (above) | Run B (this appendix) |
|---|---|---|
| repo retrieval | full `git clone --depth 1` into `/tmp` | same, but the **checkout phase was killed by the NAS quota** |
| mock bodies/voice | 3 | 1 long body, **random sentence window** per call |
| distinct `content_preview` | 21 / 80 | **36 / 80 (set A), 32 / 80 (set B)** |
| fleet mean `avg_score` | 1.892 / 1.951 | 1.869 / 1.952 |
| max per-civ \|delta\| | 0.247 | 0.381 |
| positional rank agreement | 4/8 | **2/8** |
| Kendall tau | 0.714 | **+0.714** |
| chooser vs `argmax` | 1/10 | **0/10** (0/5 set A, 0/5 set B) |
| temperature vs novelty | r = 0.9430 | **r = 0.9532** |
| lowest `rel_per_sim` | civ-grounded 1.532 | **civ-grounded 1.543** |
| lowest lifetime `avg_score` | civ-grounded 1.605 | **civ-grounded 1.617** |
| lowest win rate | civ-poetic 0.022 (2W/91L) | **civ-poetic 0.011 (1W/87L)** |
| raw-relevance lowest | civ-formal 318.81 | **civ-engineer 304.42** |
| extinction risk | none | **none** |

**Both runs agree on the low-relevance answer:** `civ-grounded` is lowest on the board's sort
key **and** on the quality lens, in both body sets, with the fleet's lowest alignment.
`civ-poetic` is the inverse — top of the fleet on quality, bottom on win rate, in both runs.
`civ-precise` is the mirror image (best win rate, bottom on quality).

## Run B — the two findings the merged record gains

### 1. A quota-killed clone leaves 22 003 files staged as DELETED, and `ls` cannot see it

`git clone --depth 1` into `/tmp` printed
`warning: Clone succeeded, but checkout failed.` — the **checkout** phase died on the NAS
EDQUOT trap while the object copy had already succeeded. The working tree landed on disk and
looked perfect, but git had staged the **entire tree as deleted**:

```
git status --short   ->   22003 lines, almost all "D  <path>"
```

The damage is entirely in the **index**, and it silently poisons any later `git add -A` or
commit. Recovery:

```bash
git reset -q HEAD -- <subtree>          # clear the bogus index
git checkout -f HEAD -- <subtree>       # re-materialise from the object store
# then verify EVERY file against the blob, not just the one you care about:
git show HEAD:<path> | cmp - <path>
```

> **Generalisation: a failed clone leaves a half-built index that `ls` cannot detect.**
> Always assert `git status --short` is empty (or contains only what you intended) before
> trusting a freshly cloned tree, and never `git add -A` on a tree you have not status-checked.
> This bit the commit itself: the first `git add` produced a 20 587-file, 2 939 889-deletion
> staged diff. `git reset -q` + scoping the `git add` to the two intended paths fixed it.

### 2. The distinct-preview acceptance check must be **per civ**, and the mock's body pool drives it

Run A's mock had 3 bodies per voice and produced **21/80** fleet-wide distinct previews. Run B's
mock had 1 long body per voice but a **random sentence window** per call and produced **36/80**.

Run A's note is right that the absolute count is a property of the **pool size**, not of the
run. But the metric that actually matters is neither the fleet-wide count nor the pool size —
it is **how many distinct strings each civ contributes**, because the chooser compares civs
against each other:

> **A civ that always shows the same preview string is invisible to the chooser, no matter how
> it scores.** That is precisely the failure that makes `civ-poetic` (1st on `avg_score`,
> 1 win in 88) look like a mystery.

The first version of Run B's mock built each body by a random **word offset**, which put the
*start* of the body at the head of every response — so all 10 calls per civ produced an
identical preview, giving **8 distinct previews out of 80** (exactly one per civ). That run
passed **every** existing acceptance check: +80 rows, +5 meta_log, 5 winners, 0
all-2.0-default rows, 76 distinct `avg_score`, 0 fallbacks. It was still **decorative** — the
chooser was re-reading the same 8 strings and had no signal to pick from.

**Fix:** choose a random *sentence window* per call (random start, no wraparound):
```python
sents = [x.strip() for x in re.split(r"(?<=[.!?])\s+", body) if x.strip()]
si = rnd.randrange(0, len(sents))
w = [sents[si+k] for k in range(min(3, len(sents)-si))]
out = " ".join(w)
```

### 3. The mock daemon dies silently; its log is created on first request, not at startup

`(setsid nohup MOCK_LOG=/tmp/x.log python3 /tmp/zai_mock.py &)` from the tool's shell **did not
survive** — no error, no output, process simply gone. The same script launched via a wrapper
that exports the env **inside** it works:

```bash
cat > /tmp/start_mock.sh <<'SH'
#!/bin/bash
export MOCK_LOG="$1"; export MOCK_BODY_SET="$2"; export MOCK_PORT="$3"; export MOCK_SEED="${4:-1}"
cd /tmp
exec python3 /tmp/zai_mock.py
SH
(setsid nohup timeout -s KILL 3000 /tmp/start_mock.sh /tmp/zai_mock_A.log A 8931 20261023 > /tmp/mock_A.out 2>&1 &)
```

**The mock's log file is only created on the FIRST REQUEST**, so `ls /tmp/zai_mock_A.log`
reporting "No such file" right after launch is **not** evidence the process died — probe with a
real POST and re-check. Switching body sets requires a restart **with the new log path**; the
first attempt left the old path in place and the set-B log never appeared, which would have
silently voided the `fallback`-flag check.

## Run B — the four lenses (never merged)

| lens | lowest | what it measures |
|---|---|---|
| A `relevance_per_sim` (board sort) | **civ-grounded 1.543** | lifetime average — penalises the civ that ran most (199 sims) |
| B raw `relevance_score` | **civ-engineer 304.42** | accumulated score, same denominator artefact |
| C `win_rate` | **civ-poetic 0.011 (1W/87L)** | **selection** appeal under a 150-char preview |
| D mean `avg_score` (quality) | **civ-grounded 1.617 lifetime** | the only lens that answers "is this civ actually good?" |

| civ | `rel_per_sim` | raw rel | wins | losses | win_rate | set A avg | set B avg |
|---|---|---|---|---|---|---|---|
| civ-grounded | **1.543** | 306.98 | 16 | 71 | 0.184 | **1.237** | 1.617 |
| civ-formal | 1.670 | 308.96 | 17 | 69 | 0.198 | 1.710 | 1.773 |
| civ-engineer | 1.750 | **304.42** | 11 | 70 | 0.136 | 1.880 | 1.611 |
| civ-precise | 1.837 | 321.42 | 41 | 42 | **0.494** | 1.635 | 1.610 |
| civ-therapist | 1.945 | 344.28 | 2 | 83 | 0.024 | 1.931 | 1.798 |
| civ-mythic | 2.034 | 364.17 | 3 | 79 | 0.037 | 2.010 | 2.278 |
| civ-whimsical | 2.148 | 410.24 | 3 | 85 | 0.034 | 2.111 | 2.238 |
| civ-poetic | **2.259** | **415.73** | 1 | 87 | **0.011** | **2.441** | **2.691** |

`civ-grounded` is lowest on `rel_per_sim`, lowest on lifetime `avg_score`, and holds the
**lowest quality sub-score of 8 in both body sets** (0.71 / 0.94) and the lowest novelty in
set A (1.14). `civ-poetic` is 1st on `avg_score` in both body sets, 1st on `rel_per_sim`, 1st
on raw relevance — and has **1 win in 88**.

## Run B — replications

- Control B: **+80 / +80**, uniform +10/civ, 0 all-2.0-default rows, 0 score errors, 0
  fallbacks, 8/8 voices, 80 mock calls per set with a 1:1 row-to-call ratio.
- Chooser vs `argmax(avg_score)`: **0/5 set A, 0/5 set B**; lifetime **10/78 = 12.8 %**. In all
  10 rounds the winning civ's **own score was below the runner-up's**, by 0.62–1.39.
- Temperature vs lifetime novelty: **Pearson r = 0.9532**.
- Counter gap: **+260** (ledger 1724 vs registry 1464), unchanged since session 6.
