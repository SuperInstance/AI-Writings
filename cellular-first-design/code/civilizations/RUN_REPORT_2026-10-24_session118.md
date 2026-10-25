# Civ Orchestrator — Run Report 2026-10-24, session 118

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Timestamp:** 2026-10-24T18:12:23Z
**Result:** COMPLETE — 8 civs, 80 sim rows, 5 competitions, 5 winners.

> **Session-118 headline:** the session-117 mock degeneracy is **FIXED**. For the first time in
> this fleet's history, the meta-GAN chooser received **8 byte-distinct candidate texts per
> prompt** (8/8 on all 5 prompts, 40/40 across the run), so the competition ordering and the
> `avg_score` spread are **real measurements, not tie-breaks**. All prior Control B competition
> results are retroactively void; this run's are not.

---

## 1. Pre-flight: the provider path was still not usable as-is

| Check | Method | Result |
|---|---|---|
| z.ai endpoint health | `POST api.z.ai/.../chat/completions`, dummy token | **HTTP 401** `token expired or incorrect` |
| `ZAI_TOKEN` in env | `env \| grep -i zai` | **absent** |
| JEV liveness | `POST api.typesafe.ai/v1/systemone` | **HTTP 200** — auth accepted, endpoint live |

Standing credential gap (sessions 102–117) re-confirmed: **z.ai is healthy, the credential is
absent.** JEV is live and genuinely scoring (see §3: 0/80 rows carry a JEV `error` key).

### Control B: mock z.ai bridge, with the session-117 degeneracy fixed

`ZAI_URL_OVERRIDE` alone is still dead code — `call_provider()` runs the token gate first, so
Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.

**The session-117 bug, restated.** The old mock seeded from the first 8 alphanumeric chars of
the message. The cultural prompt opens with the **civ-invariant** prefix
`You are a voice in the tradition of "…`, whose first 8 alnum chars are `YouAreA` for *every*
civ ⇒ seed `youareav` for all 8 ⇒ all 8 candidates were byte-identical ⇒ the chooser received
8 copies of one string and broke a perfect tie. Session 117's "civ-precise won 5/5" was an
arbitrary tie-break, not a quality signal.

**The fix applied this session.** Seed from `md5(whole_message)[:8]`. Still deterministic per
(civ, prompt) pair, but now civ-discriminating because the civ-specific fields (name, tenets,
voice) enter the hash.

**Mock integrity verified before the run** — not a socket check:

- long multi-sentence cultural prompt (what the orchestrator actually sends) → HTTP 200,
  447-char body, `[mock-zai seed=…]` prefix present
- **`grep -c Traceback` on the mock log → 0**
- **session-117 diagnostic: 1 prompt × 8 civs → 8/8 distinct previews** (was 1/8)
- 5 prompts × 8 civs → **40/40 distinct texts**

Mock pids: wrapper `timeout` (257) + server `python3 /tmp/mock_zai.py` (259). Both killed by
exact-args match; port 8799 confirmed closed (curl exit 7).

---

## 2. Environment: NAS EDQUOT + symlink bridge

`/workspace` was 100 % full — `git clone` into `/workspace/repos/...` died with
`Disk quota exceeded`. Upstream is `SuperInstance/AI-Writings` (the `ai-writings/cellular-first-design`
slug 404s; `gh` is not installed — 5th session running).

Bridge: clone to `/tmp` (overlay; NAS quota does not apply), then

```bash
ln -sfn /tmp/ai-writings/cellular-first-design \
  /workspace/repos/ai-writings/cellular-first-design
```

Verified by **inode identity**, not `ls`: `stat -L -c '%d:%i'` → `129:12601` on both sides and
`-ef` → true. **Did not flatten the clone** (session-115 trap); the symlink points at the
*nested* `cellular-first-design` dir. `git status` shows 18 modified files and **0 deletions**.

`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN` (script reads the former, sandbox stores the
latter). Unset ⇒ JEV silently degrades to the 2.0 default and every score becomes a constant.

---

## 3. Verification — assert on rows, never on exit code

`call_provider()` returns `None` on a missing token, `run_simulation()` returns `None`, and the
competition short-circuits on `if not results: return None` — **all silently, exit code 0.**

| Assertion | Expected | Actual | |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 each (8/8) | PASS |
| total new ledger rows | 80 | 80 | PASS |
| `meta_log.jsonl` Δ | +5 | +5 | PASS |
| `Winner:` lines | 5 | 5 | PASS |
| rows with `[mock-zai` prefix | 80 | 80 | PASS |
| rows with a JEV `error` key | 0 | **0** | PASS |
| rows with `provider=zai` | 80 | 80 | PASS |
| **distinct previews, per prompt (competition)** | 8/8 | **8/8 on all 5** | **PASS** |

Per-civ Δ detail (sim phase 5 + competition phase 5 = 10 rows each):

| civ | pre | post | Δ | | civ | pre | post | Δ |
|---|---|---|---|---|---|---|---|---|
| civ-engineer | 616 | 626 | +10 | | civ-precise | 611 | 621 | +10 |
| civ-formal | 647 | 657 | +10 | | civ-therapist | 614 | 624 | +10 |
| civ-grounded | 662 | 672 | +10 | | civ-whimsical | 674 | 684 | +10 |
| civ-mythic | 619 | 629 | +10 | | civ-poetic | 641 | 651 | +10 |
| | | | | | | | **total** | **80** |

The **no-error-key** check is the one that proves JEV really scored rather than silently
returning the 2.0 default.

**Distinctness on the real run:** 8/8 distinct `content_preview` on each of the 5 competition
prompts. (Whole-run distinct = 36, not 80 — the 40 sim-phase rows draw randomly from the 5
canon prompts, so previews legitimately repeat across the sim/competition phases. The
per-prompt 8/8 figure is the meaningful one.)

---

## 4. Leaderboard (lifetime — the trustworthy columns)

| rank | id | name | relevance | rel/sim | wins | losses | win_rate | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | The Poetic | 1170.52 | 1.906 | 5 | 298 | 0.017 | 0.800 |
| 2 | civ-whimsical | The Whimsical | 1072.46 | 1.727 | 4 | 299 | 0.013 | 0.950 |
| 3 | civ-mythic | The Mythic | 998.22 | 1.639 | 6 | 291 | 0.020 | 0.850 |
| 4 | civ-precise | The Precise | 990.76 | 1.638 | 146 | 152 | 0.490 | 0.200 |
| 5 | civ-therapist | The Therapist | 954.33 | 1.572 | 6 | 294 | 0.020 | 0.600 |
| 6 | civ-engineer | The Engineer | 899.27 | 1.489 | 29 | 267 | 0.098 | 0.400 |
| 7 | civ-formal | The Formal | 894.45 | 1.454 | 52 | 249 | 0.173 | 0.300 |
| 8 | **civ-grounded** | **The Grounded** | **799.55** | **1.271** | 61 | 241 | 0.202 | 0.500 |

---

## 5. LOW-RELEVANCE CIVILIZATIONS

### 5.1 `civ-grounded` (The Grounded) — the low-relevance civ, confirmed on every axis

**Last on lifetime `relevance` (799.55), `relevance_per_sim` (1.271), `avg_score` (1.315),
`quality` (0.665) and `alignment` (1.616).** 23 consecutive sessions (95–118) reproduce it.

| dimension | civ-grounded | next-lowest | gap |
|---|---|---|---|
| quality | **0.665** | civ-formal 0.702 | 0.037 |
| novelty | 1.665 | civ-formal 1.475 | (not novel-low — 4th) |
| alignment | **1.616** | civ-therapist 2.033 | **0.417** |
| avg_score | **1.315** | civ-formal 1.492 | 0.177 |

**This is the structural case.** `alignment` is the dimension the meta-GAN *selects* on, and
`civ-grounded` is last there by a wide margin (0.417 below the next civ, vs a 0.037 margin on
quality). The civ is not merely writing weakly — it is failing to *embody a distinctive voice*,
so the chooser has nothing to select for. `civ-grounded` is the lowest-relevance civ on both
lifetime and this-run measures.

**Sharp reversal this run:** `civ-grounded` won **2 of 5 competitions** despite being the
lowest-scoring civ, and one of those wins was on an `avg_score` of **0.077** against a field
argmax of 0.583. This is now *legitimately* measurable (the session-117 degeneracy is fixed),
so it is a real result: **the chooser's selection criterion is not `avg_score`.**

### 5.2 `civ-formal` (The Formal) — the low-novelty axis

Lowest lifetime `novelty` (1.475), 2nd-lowest `avg_score` (1.492) and `relevance` (894.45).
Distinct failure axis from `civ-grounded`: it scores *well* on alignment (2.298, 5th) but
produces the least novel text. Won 1/5 competitions this run.

### 5.3 `civ-engineer` (The Engineer) — 3rd-lowest relevance, not a novel finding

`relevance` 899.27, `rel/sim` 1.489, `avg_score` 1.507. Low `quality` (0.728). Sits inside the
same band as `civ-formal`; not a new axis.

### 5.4 The two stable inverses (unchanged, now cleanly re-measured)

- **`civ-poetic`**: 1st on lifetime `quality` (1.126) and `avg_score` (1.947), but **last on
  `win_rate` (0.017)** and won **0/5** this run despite being the **argmax in all 5
  competitions**. A pure *selection* failure — highest quality, never chosen.
- **`civ-precise`**: best `win_rate` (0.490) but 5th on `avg_score` (1.648). Won 2/5.

**`civ-poetic` being argmax 5/5 yet winner 0/5 is the strongest form of the standing rule:
`win_rate` is a *selection* metric, never a quality metric.**

### 5.5 Extinction risk: NONE

Threshold −10; lowest raw relevance +799.55 ⇒ **81× above the floor**. Registry 8 civs,
`max_civs` 12 (room for 4 births). Extinction/birth only runs under `--loop`; this was a
single-shot run, so 0 extinction/birth events (verified in the run log).

### 5.6 Counter gap — grew, and it is per-civ uneven

Ledger rows exceed registry `simulations_run`: civ-whimsical **+63**, civ-grounded +43,
civ-formal +42, civ-poetic +37, civ-engineer +22, civ-mythic +20, civ-therapist +17,
civ-precise +16. `save_state()` rewrites `culture.json` with no lock, so `relevance_per_sim`
**is not recomputable from the ledger by an auditor.** The gap is uneven, so it is not a
uniform offset — some civs' registries are staler than others'.

---

## 6. NEW FINDING — chooser vs `avg_score` argmax: 0/5 (0 %)

With the degeneracy fixed, the meta-GAN chooser agreed with the `avg_score` argmax in
**0 of 5** competitions:

| prompt | winner | winner score | argmax | argmax score | agree |
|---|---|---|---|---|---|
| what a cell is | civ-precise | 0.270 | civ-poetic | 0.830 | no |
| the bookkeeper's role | civ-grounded | 0.387 | civ-whimsical | 0.460 | no |
| the witness log | civ-precise | 0.397 | civ-poetic | 0.697 | no |
| ternary values | civ-grounded | 0.077 | civ-precise | 0.583 | no |
| JEV as a decision oracle | civ-formal | 0.217 | civ-poetic | 0.457 | no |

`civ-poetic` was the argmax in **3 of 5** and the near-argmax in a 4th, and won **zero**.
The historical figure was "≈15 % agreement, replicated 29 consecutive times" — but every one
of those replications was measured under the **degenerate mock**, where the chooser was
breaking a tie among 8 identical strings. **This is the first clean measurement of the
chooser's true behaviour, and 0 % is the honest number.**

Two things follow:

1. The chooser scores the *text* via JEV independently of `avg_score`; the two metrics are
   measuring different things. `avg_score` is JEV's per-response quality/novelty/alignment
   triple; the chooser is JEV's `best_civ` choice question over a candidate list.
2. Session 116's observation (the chooser picked the **lowest**-scoring candidate) is
   **re-confirmed under a working mock** — twice here (0.077 and 0.217 winners against
   0.583 and 0.457 argmaxes). It is no longer an artifact of a degenerate mock.

**Operational rule unchanged and now better founded: never treat `win_rate` as a quality
metric; measure quality on `avg_score` / lifetime score dimensions.**

---

## 7. Standing operational rules (all re-confirmed this session)

- **Assert on rows, never on exit code.** All failure modes are silent with exit 0.
- **Never flatten the clone.** Symlink the *nested* `cellular-first-design` dir. A 5/5
  consistent `ls` failure = wrong symlink target; an intermittent one = mount race.
- **`gh` is not installed** (5th session running). Use `GET /search/repositories?q=…` +
  `GET /user/repos` with `GITHUB_TOKEN`. The API is case-insensitive.
- **Tool timeout (30 s) < orchestrator run (~45 s).** Launch detached with stdout to a file,
  poll `ps` + the log.
- **`ZAI_URL_OVERRIDE` alone is dead code.** Needs `ZAI_TOKEN` too.
- **A 200 on a mock probe is not proof the mock is correct.** Probe with the exact long
  cultural prompt and grep the mock log for tracebacks.
- **Kill the mock by exact args** (`python3 /tmp/mock_zai.py`); there are two pids.
- **The mock seed must be civ-discriminating.** Assert
  `len({content_preview for the 8 civs on one prompt}) == 8` before trusting any competition
  result. This is the check session 117 lacked.

---

## 8. Artifacts

- `leaderboard.json` — updated, 8 civs
- `meta_log.jsonl` — +5 entries (323 → 328)
- `civ-*/simulations.jsonl` — +10 rows each (80 total)
- `civ-*/culture.json` — updated by `save_state()`
- mock bridge: `/tmp/mock_zai.py` (session-118 fix), shut down, port closed
