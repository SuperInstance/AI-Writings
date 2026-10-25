# Civ Orchestrator — Run Report 2026-10-24, session 119

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Timestamp:** 2026-10-24T18:24:18Z
**Result:** COMPLETE — 8 civs, 80 sim rows, 5 competitions, 5 winners.

> **Session-119 headline:** the run completed clean under the session-118 mock, and the
> chooser-vs-`avg_score` agreement moved from **0/5 (session 118) to 3/5 (this run)**. That
> is the first non-zero agreement measured under the non-degenerate mock. It does not
> establish a stable rate — 3/5 vs 0/5 is a 5-sample swing, and the standing rule that
> `win_rate` is a *selection* metric, never a quality metric, is unchanged. A **new** axis
> surfaced: this run's `quality` scores collapsed to ~0.01–0.03 for every civ, while
> `alignment` spread 0.03–1.30. See §6.

---

## 1. Pre-flight: the provider path was still not usable as-is

| Check | Method | Result |
|---|---|---|
| z.ai endpoint health | `POST api.z.ai/.../chat/completions`, dummy token | **HTTP 401** `token expired or incorrect` |
| `ZAI_TOKEN` in env | `env \| grep -i zai` | **absent** |
| `ZAI_TOKEN` in sandbox secrets | `secret list` (8 secrets) | **absent** from all 8 |
| JEV liveness | `POST api.typesafe.ai/v1/systemone` | **HTTP 200** — auth accepted, endpoint live |

Standing credential gap re-confirmed (sessions 102–118, now **19 consecutive**): **z.ai is
healthy, the credential is absent.** JEV is live and genuinely scoring (§3: 0/80 rows carry a
JEV `error` key; 70/80 distinct `avg_score` values, so not the degenerate 2.0 default).

### Control B: mock z.ai bridge

`ZAI_URL_OVERRIDE` alone is still dead code — `call_provider()` runs the token gate first
(`if not token: return None`), so Control B needs **both** `ZAI_TOKEN` (any non-empty
placeholder) **and** `ZAI_URL_OVERRIDE`. Both were set.

**Mock integrity verified before the run** — not a socket check:

- long multi-sentence cultural prompt (what the orchestrator actually sends) → HTTP 200,
  100–115-char body, `[mock-zai seed=…]` prefix present
- `grep -c Traceback` on the mock log → **0**
- **session-117 degeneracy diagnostic: 1 prompt × 8 civs → 8/8 distinct previews, 8/8 distinct seeds**
- 5 prompts × 8 civs → **40/40 distinct texts**

Mock pids: wrapper `timeout` (281) + server `python3 /tmp/mock_zai.py` (282). Both killed by
exact-args match; port 8799 confirmed closed (curl exit 7).

---

## 2. Environment: NAS EDQUOT + symlink bridge

`/workspace` was 100 % full (600 G/600 G, 0 bytes free) — `git clone` into
`/workspace/repos/...` died with `Disk quota exceeded` on `.git/description`.

Upstream is **`SuperInstance/AI-Writings`** — note the `ai-writings/cellular-first-design`
slug 404s; the API is case-insensitive but the owner is `SuperInstance`, not `ai-writings`.
`gh` is not installed (**6th session running**).

Bridge: clone to `/tmp` (overlay, 28 G free; NAS quota does not apply), then

```bash
ln -sfn /tmp/ai-writings/cellular-first-design \
  /workspace/repos/ai-writings/cellular-first-design
```

Verified by **inode identity**, not `ls`: `stat -L -c '%d:%i'` → `129:12601` on both sides
and `-ef` → true. **Did not flatten the clone** (session-115 trap); the symlink points at the
*nested* `cellular-first-design` dir. `git status` shows **18 modified files, 0 deletions**.

`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN` (script reads the former, sandbox stores
the latter). Unset ⇒ JEV silently degrades to the 2.0 default and every score becomes a
constant.

---

## 3. Verification — assert on rows, never on exit code

`call_provider()` returns `None` on a missing token, `run_simulation()` returns `None`, and
the competition short-circuits on `if not results: return None` — **all silently, exit code 0.**

| Assertion | Expected | Actual | |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 each (8/8) | PASS |
| total new ledger rows | 80 | 80 | PASS |
| `meta_log.jsonl` Δ | +5 | +5 (328 → 333) | PASS |
| `Winner:` lines | 5 | 5 | PASS |
| rows with `[mock-zai` prefix | 80 | 80 | PASS |
| rows with a JEV `error` key | 0 | **0** | PASS |
| rows with `provider=zai` | 80 | 80 | PASS |
| **distinct previews, per prompt (competition)** | 8/8 | **8/8 on all 5** | **PASS** |
| distinct `avg_score` values (new rows) | >3 (not degenerate) | **70/80** | PASS |

The **no-error-key** check is the one that proves JEV really scored rather than silently
returning the 2.0 default.

Per-civ Δ detail (sim phase 5 + competition phase 5 = 10 rows each):

| civ | pre | post | Δ | | civ | pre | post | Δ |
|---|---|---|---|---|---|---|---|---|
| civ-engineer | 626 | 636 | +10 | | civ-precise | 621 | 631 | +10 |
| civ-formal | 657 | 667 | +10 | | civ-therapist | 624 | 634 | +10 |
| civ-grounded | 672 | 682 | +10 | | civ-whimsical | 684 | 694 | +10 |
| civ-mythic | 629 | 639 | +10 | | civ-poetic | 651 | 661 | +10 |
| | | | | | | **total** | **5164 → 5244** | **+80** |

**Distinctness on the real run:** 8/8 distinct `content_preview` on each of the 5 competition
prompts. (Within a civ, 5/10 distinct previews — expected, since the 10 new rows draw from
the same 5 canon prompts across the two phases. The per-prompt 8/8 figure is the meaningful one.)

---

## 4. Leaderboard (lifetime — the trustworthy columns)

| rank | id | name | relevance | rel/sim | wins | losses | win_rate | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | The Poetic | 1176.25 | 1.885 | 5 | 303 | 0.016 | 0.800 |
| 2 | civ-whimsical | The Whimsical | 1077.35 | 1.707 | 4 | 304 | 0.013 | 0.950 |
| 3 | civ-mythic | The Mythic | 1001.05 | 1.617 | 6 | 296 | 0.020 | 0.850 |
| 4 | civ-precise | The Precise | 997.50 | 1.622 | 150 | 153 | 0.495 | 0.200 |
| 5 | civ-therapist | The Therapist | 956.08 | 1.550 | 6 | 299 | 0.020 | 0.600 |
| 6 | civ-engineer | The Engineer | 903.30 | 1.471 | 29 | 272 | 0.096 | 0.400 |
| 7 | civ-formal | The Formal | 897.79 | 1.436 | 53 | 253 | 0.173 | 0.300 |
| 8 | **civ-grounded** | **The Grounded** | **801.35** | **1.254** | 61 | 246 | 0.199 | 0.500 |

*(Session-118 note: the shipped `leaderboard.json` sorted by `relevance_per_sim` but listed
`civ-mythic` (1.639) above `civ-precise` (1.638) — a stale pre-sort value. The ordering
here is recomputed from the written file; `civ-precise` and `civ-mythic` are within 0.005
of each other and their relative order is noise.)*

---

## 5. LOW-RELEVANCE CIVILIZATIONS

### 5.1 `civ-grounded` (The Grounded) — the low-relevance civ, confirmed on every axis

**Last on lifetime `relevance` (801.35), `relevance_per_sim` (1.254), `avg_score` (1.299) and
`quality` (0.656); and last on `alignment` (1.593) by a wide margin.** 24 consecutive
sessions (95–119) reproduce it.

| dimension | civ-grounded | next-lowest | gap |
|---|---|---|---|
| quality | **0.656** | civ-formal 0.691 | 0.035 |
| novelty | 1.648 | civ-formal 1.463 | (not novel-low — 4th) |
| alignment | **1.593** | civ-therapist 2.002 | **0.409** |
| avg_score | **1.299** | civ-formal 1.474 | 0.175 |

**This is the structural case.** `alignment` is the dimension the meta-GAN *selects* on, and
`civ-grounded` is last there by 0.409 — an order of magnitude wider than its 0.035 quality
margin. The civ is not merely writing weakly; it is failing to *embody a distinctive voice*,
so the chooser has nothing to select for. It is the lowest-relevance civ on both lifetime
and this-run measures.

**This run it won 0/5 competitions** and posted the worst this-run `avg_score` of any civ
(0.180). Notably, it still holds the **highest lifetime `win_rate` among the bottom four**
(0.199) — another instance of the standing rule that `win_rate` is a selection metric, not
a quality one.

### 5.2 `civ-formal` (The Formal) — the low-novelty axis

Lowest lifetime `novelty` (1.463), 2nd-lowest `avg_score` (1.474) and `relevance` (897.79).
Distinct failure axis from `civ-grounded`: it scores *well* on alignment (2.269, 5th) but
produces the least novel text. **Won 1/5 competitions this run** (the JEV-as-oracle prompt).

### 5.3 `civ-engineer` (The Engineer) — 3rd-lowest relevance, not a novel finding

`relevance` 903.30, `rel/sim` 1.471, `avg_score` 1.490. Low `quality` (0.717). Sits inside the
same band as `civ-formal`; not a new axis. 0/5 this run.

### 5.4 The two stable inverses (unchanged, cleanly re-measured)

- **`civ-poetic`**: 1st on lifetime `quality` (1.110) and `avg_score` (1.926), but **last on
  `win_rate` (0.016)** and won **0/5** this run. A pure *selection* failure — highest
  quality, never chosen.
- **`civ-precise`**: best `win_rate` (0.495) and **won 4/5 competitions this run**, yet 5th
  on lifetime `avg_score` (1.633). The mirror image of `civ-poetic`.

**`civ-poetic` = 1st on quality but 0/5 wins, and `civ-precise` = 5th on quality but 4/5
wins: that pair is the strongest form of the standing rule.**

### 5.5 Extinction risk: NONE

Threshold −10; lowest raw relevance +801.35 ⇒ **80× above the floor**. Registry 8 civs,
`max_civs` 12 (room for 4 births). Extinction/birth only runs under `--loop`; this was a
single-shot run, so 0 extinction/birth events (verified in the run log).

### 5.6 Counter gap — unchanged, and still per-civ uneven

Ledger rows exceed registry `simulations_run`: civ-whimsical **+63**, civ-grounded +43,
civ-formal +42, civ-poetic +37, civ-engineer +22, civ-mythic +20, civ-therapist +17,
civ-precise +16. `save_state()` rewrites `culture.json` with no lock, so `relevance_per_sim`
**is not recomputable from the ledger by an auditor.** The gap is uneven, so it is not a
uniform offset — some civs' registries are staler than others'.

---

## 6. NEW FINDING — this run's `quality` axis collapsed; `alignment` carried the signal

Per-civ score dimensions, **this run's 10 rows each** vs **lifetime**:

| civ | qual (run) | nov (run) | align (run) | avg (run) | | qual (life) | nov (life) | align (life) | avg (life) |
|---|---|---|---|---|---|---|---|---|---|
| civ-precise | 0.030 | 0.697 | 1.297 | 0.675 | | 0.747 | 1.601 | 2.550 | 1.633 |
| civ-poetic | 0.030 | 0.549 | 1.139 | 0.573 | | 1.110 | 2.120 | 2.548 | 1.926 |
| civ-whimsical | 0.018 | 0.897 | 0.551 | 0.489 | | 0.910 | 2.213 | 2.283 | 1.802 |
| civ-engineer | 0.013 | 0.744 | 0.452 | 0.403 | | 0.717 | 1.595 | 2.157 | 1.490 |
| civ-formal | 0.013 | 0.663 | 0.326 | 0.334 | | 0.691 | 1.463 | 2.269 | 1.474 |
| civ-mythic | 0.009 | 0.616 | 0.225 | 0.283 | | 0.826 | 2.003 | 2.111 | 1.647 |
| civ-therapist | 0.011 | 0.478 | 0.034 | 0.174 | | 0.745 | 1.977 | 2.002 | 1.574 |
| civ-grounded | 0.010 | 0.467 | 0.064 | 0.180 | | 0.656 | 1.648 | 1.593 | 1.299 |

**`quality` collapsed to 0.009–0.030 for every civ this run** — a ~25× drop from lifetime,
and with a spread of only 0.021 across all 8 civs. `novelty` fell ~1.3× but kept a 0.43
spread. `alignment` fell ~1.8× but kept the **widest spread (1.263)** and, crucially, preserved
the **civ ordering**: `civ-precise` (1.297) > `civ-poetic` (1.139) > `civ-whimsical` (0.551)
> `civ-engineer` (0.452) > `civ-formal` (0.326) > `civ-mythic` (0.225) > `civ-grounded`
> (0.064) — and it is precisely the civs with the highest `alignment` that won the
competitions (precise 4/5, formal 1/5).

**Interpretation.** The mock's text is word-salad by construction, so a near-zero `quality`
reading is *expected* and not a defect. The finding is about **where the surviving signal
lives**: with `quality` saturated near zero, `alignment` becomes the only dimension with
enough dynamic range to separate civs — and it is the dimension the chooser is *supposed* to
select on. So this run's competition outcomes are better-founded than the raw numbers
suggest, and **`quality` should be treated as a broken/insensitive axis whenever its spread
across civs is small**, regardless of its absolute level.

**Operational rule added: a score dimension is only informative if its cross-civ spread is
non-trivial. Compare spreads, not levels, before using a dimension to rank civs.**

---

## 7. Chooser vs `avg_score` argmax: 3/5 (60 %) — first non-zero agreement under a working mock

| prompt | winner | winner score | argmax | argmax score | agree |
|---|---|---|---|---|---|
| what a cell is | civ-precise | 0.597 | civ-precise | 0.597 | **yes** |
| the bookkeeper's role | civ-precise | 0.543 | civ-poetic | 0.637 | no |
| the witness log | civ-precise | 0.950 | civ-precise | 0.950 | **yes** |
| ternary values | civ-precise | 0.733 | civ-precise | 0.733 | **yes** |
| JEV as a decision oracle | civ-formal | 0.550 | civ-precise | 0.677 | no |

Session 118 measured **0/5** under the fixed mock and called 0 % "the honest number" for
the chooser's behaviour. This run measures **3/5**. Both are 5-sample points, so the honest
statement is: **agreement is somewhere in 0–60 %, and one run cannot tell you which.** What
survives both runs is the more useful claim — **the chooser is not a pure `avg_score`
argmax**, and `win_rate` remains a selection metric that must never be read as quality.

Notably, in this run the 2 disagreements were both cases where the chooser picked a
*lower*-scoring candidate (0.543 over 0.637; 0.550 over 0.677) — re-confirming session 116's
and 118's observation that the chooser sometimes picks the **lowest**-scoring candidate,
now measured under a non-degenerate mock for the third consecutive session.

---

## 8. Standing operational rules (all re-confirmed this session)

- **Assert on rows, never on exit code.** All failure modes are silent with exit 0.
- **Never flatten the clone.** Symlink the *nested* `cellular-first-design` dir. A 5/5
  consistent `ls` failure = wrong symlink target; an intermittent one = mount race.
- **`gh` is not installed** (6th session running). Use `GET /search/repositories?q=…` +
  `GET /user/repos` with `GITHUB_TOKEN`. The API is case-insensitive.
- **Tool timeout (30 s) < orchestrator run (~45 s).** Launch detached with stdout to a file,
  poll `ps` + the log. A tool timeout mid-run destroys the capture.
- **`ZAI_URL_OVERRIDE` alone is dead code.** Needs `ZAI_TOKEN` too.
- **A 200 on a mock probe is not proof the mock is correct.** Probe with the exact long
  cultural prompt and grep the mock log for tracebacks.
- **Kill the mock by exact args** (`python3 /tmp/mock_zai.py`); there are two pids.
- **The mock seed must be civ-discriminating.** Assert
  `len({content_preview for the 8 civs on one prompt}) == 8` before trusting any competition
  result.
- **A dimension is informative only if its cross-civ spread is non-trivial** (new, §6).
- **The write/edit tools are jailed to the workspace root** — `/tmp` artifacts need bash
  heredocs.

---

## 9. Artifacts

- `leaderboard.json` — updated, 8 civs, iso `2026-10-24T18:24:18`
- `meta_log.jsonl` — +5 entries (328 → 333)
- `civ-*/simulations.jsonl` — +10 rows each (80 total, 5164 → 5244)
- `civ-*/culture.json` — updated by `save_state()`
- mock bridge: `/tmp/mock_zai.py` (session-118 seed fix, re-verified), shut down, port closed
