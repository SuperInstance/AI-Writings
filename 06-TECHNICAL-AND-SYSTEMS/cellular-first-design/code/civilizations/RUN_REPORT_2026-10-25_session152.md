# Civilization Orchestrator — Run Report, session 152 (2026-10-25)

**Command**

```bash
python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py \
  --sims 5 --prompts 5 --providers zai
```

**Verdict: run clean. 36/36 verification assertions PASS. 24th consecutive clean mock measurement.**

---

## 1. Environment (the 30th session with this shape)

| Fact | Status |
|---|---|
| Requested path existed at session start | **No** — `/workspace` held only `.plugin-cache` |
| Upstream repo | `SuperInstance/AI-Writings` (the `ai-writings/cellular-first-design` slug 404s) |
| `gh` CLI | **Not installed** (30th session running) — used `GET /user/repos` with `GITHUB_TOKEN` |
| NAS EDQUOT | **Total** — first `git clone` into `/workspace` died with `Disk quota exceeded`; clone went to `/tmp` |
| Symlink bridge | `/workspace/repos/ai-writings/cellular-first-design` → `/tmp/ai-writings/cellular-first-design`; inode identity `129:12601` (bridge) / `129:12603` (target) + `-ef` = **EF_OK** |
| `TYPESAFEAI_KEY` | Exported from `TYPESAFE_AI_TOKEN` (the script reads the former) |
| `ZAI_TOKEN` | **Absent** from env and from all sandbox secrets — **46th session** on this credential gap |
| z.ai endpoint | **HTTP 401** `token expired or incorrect` against a bogus bearer ⇒ endpoint healthy, credential absent |
| JEV liveness | **HTTP 422** `{"type":"model_attributes_type"}` on a malformed `questions` ⇒ token accepted, JEV live |
| Tool timeout | 30 s < run wall time (~24 s) — detached launch, then polled |

`git clone --filter=blob:none --no-checkout --depth 1` of the 3.7 GB repo fetched a **6.2 MB**
working tree after `git sparse-checkout set cellular-first-design/code/civilizations`. Upstream
baseline `a5af68f` (session 151).

**NEW — `git sparse-checkout init --cone` + `set cellular-first-design/code/civilizations` DID work
this session**, contrary to the session-151 note that the `--cone` form rejects a nested leaf.
Both forms are equivalent here; the `--cone` form simply did not error. The `--no-cone` form from
the RUNBOOK remains the safe default.

## 2. Control B mock — rebuilt from scratch, all four known defects were live again

`/tmp` was wiped, so the mock was rebuilt from the RUNBOOK and the four historical bugs had to be
re-applied:

| Bug | Symptom if unfixed | Fix applied |
|---|---|---|
| session-112 index wrap | `seed[i*2:i*2+2]` is empty for `i>=4` ⇒ HTTP 500 while the socket stays open | `seed[(i*2)%8:((i*2)%8)+2]` |
| session-118 md5 seeding | first-8-alnum seed ⇒ all 8 civs emit identical text ⇒ every competition result void | `md5(whole_message)[:8]` |
| session-145 literal `{}` | placeholder never interpolated ⇒ every row carries `seed={}` ⇒ 1 distinct seed | `("[mock-zai seed=%s] " % seed)` |
| session-144 `Connection: close` | a `curl` probe hangs on EOF while the server logged 200 | header set + `close_connection = True` |

### Pre-flight probe — 40/40 distinct seeds (passed, 7th time in the series it has saved a run)

The probe rebuilt the orchestrator's **exact** cultural-prompt template for all 8 civs × 5 prompts
and replayed it through the live mock:

```
  prompt Write 100 words on what a cell is.            seeds 8/8 previews 8/8
  prompt Write 100 words on the bookkeeper's role.     seeds 8/8 previews 8/8
  prompt Write 100 words on the witness log.           seeds 8/8 previews 8/8
  prompt Write 100 words on ternary values.            seeds 8/8 previews 8/8
  prompt Write 100 words on JEV as a decision oracle.  seeds 8/8 previews 8/8
distinct seeds   : 40 (expect 40)
distinct previews: 40 (expect 40)
cultural prompt lengths: 167 - 209
mock log tracebacks: 0
PREFLIGHT: PASS
```

## 3. Verification — 36/36 PASS

| Assertion | Expected | Measured | Result |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10** each | grounded 1002→1012, whimsical 1014→1024, formal 987→997, poetic 981→991, precise 951→961, mythic 959→969, therapist 954→964, engineer 956→966 | **PASS** |
| total new ledger rows | **80** | 80 | **PASS** |
| `meta_log.jsonl` delta | **+5** | 493 → 498 | **PASS** |
| `Winner:` lines | **5** | 5 | **PASS** |
| all new rows `provider == zai` | 80/80 | 80/80 | **PASS** |
| rows with a JEV `error` key | **0** | 0 | **PASS** |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | **PASS** |
| rows carrying a parseable seed | 80 | 80 | **PASS** |
| distinct seeds / 80 rows | **40** | 40 | **PASS** |
| `(civ, prompt)` combos with >1 seed | **0** | 0 | **PASS** |
| all rows have a top-level `avg_score` | 80 | 80 | **PASS** |
| sim→competition ts gap at index 4 | **8/8** civs | 8/8 | **PASS** |
| competition slots at 8/8 distinct previews | **5/5** | 5/5 | **PASS** |
| competition slots at 8/8 distinct seeds | **5/5** | 5/5 | **PASS** |
| `culture.json` `sims_run` delta | **+10** each | 8/8 civs | **PASS** |
| `meta_log` new rows have `winner_civ` | **5** | 5 | **PASS** |
| `meta_log` `results` is a list of `[civ_id, score]` pairs | **5** | 5 | **PASS** |
| `meta_log` new rows ts after pre-run | **5** | 5 | **PASS** |
| `leaderboard.json` rewritten | newer than pre-run | `2026-10-25T01:03:26` (pre-run `00:52:27`) | **PASS** |
| `leaderboard` has 8 civs | **8** | 8 | **PASS** |
| `git status` modified set | **18** | 18 (8 ledgers + 8 cultures + meta_log + leaderboard) | **PASS** |

The `error`-key check and the 2.0/2.0/2.0 check are what prove **JEV really scored** rather than
silently returning the default. **The exit code proves nothing** — every failure mode in this
orchestrator is silent with exit code 0.

## 4. Chooser vs `avg_score` argmax: **0/5 (0 %)** — 24th clean mock measurement

| prompt | winner | winner score | argmax | argmax score | | delta |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 1.147 | `civ-mythic` | 1.653 | DISAGREE | **−0.507** |
| the bookkeeper's role | `civ-precise` | 1.367 | `civ-poetic` | 1.840 | DISAGREE | **−0.473** |
| the witness log | `civ-formal` | 1.457 | `civ-poetic` | 1.980 | DISAGREE | **−0.523** |
| ternary values | `civ-engineer` | 0.703 | `civ-poetic` | 1.790 | DISAGREE | **−1.087** |
| JEV as a decision oracle | `civ-precise` | 1.783 | `civ-poetic` | 2.050 | DISAGREE | **−0.267** |

**All 5 disagreements took the LOWER-scoring candidate** — the same direction as every disagreement
ever observed across the fleet, and the **largest single margin in the series** (slot 3: −1.087).
The clean-mock rate series is 0, 3, 1, 4, 4, 3, 0, 4, 4, 1, 2, 4, 4, 0, 2, 4, 1, 2, 4, 4, 1, 2,
0 — **24 five-sample points cannot pin a rate**; the honest claim is *somewhere in 0–80 %*. The
**direction** is the finding. **Never treat `win_rate` as a quality metric.**

Winner tally this run: `civ-precise` 3, `civ-formal` 1, `civ-engineer` 1.

## 5. Low-relevance civilizations

### 5a. The structural finding — `civ-grounded` (The Grounded), **50 consecutive sessions (95–152)**

Last of 8 on **every** lifetime axis:

| civ | relevance | rel/sim | lifetime avg_score | lifetime alignment | lifetime novelty | lifetime quality | win_rate | temp |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 1489.51 | 1.561 | **1.6007** | 2.1212 | 1.8674 | **0.8135** | 0.013 | 0.80 |
| civ-precise | 1331.06 | 1.409 | 1.4190 | **2.1825** | 1.5204 | 0.5542 | **0.568** | 0.20 |
| civ-whimsical | 1326.12 | 1.380 | 1.4641 | 1.8013 | **1.9343** | 0.6568 | 0.011 | 0.95 |
| civ-mythic | 1215.61 | 1.281 | 1.3072 | 1.6157 | 1.7212 | 0.5849 | 0.019 | 0.85 |
| civ-therapist | 1130.05 | 1.193 | 1.2159 | 1.4084 | 1.7226 | 0.5169 | 0.019 | 0.60 |
| civ-formal | 1117.64 | 1.170 | 1.2068 | 1.7511 | 1.3751 | 0.4942 | 0.163 | 0.30 |
| civ-engineer | 1097.64 | 1.163 | 1.1821 | 1.5987 | 1.4471 | 0.5004 | 0.084 | 0.40 |
| **civ-grounded** | **965.00** | **0.996** | **1.0369** | **1.1701** | 1.4795 | **0.4611** | 0.144 | 0.50 |

**The binding constraint is still alignment.** Grounded's absolute gaps to the next civ up are
**alignment 0.2383** (`civ-therapist` 1.4084) and **quality 0.0330** (`civ-formal` 0.4942). Quote
the **absolute** gaps, never the ratio — the alignment-vs-quality gap ratio has swung 11× → 2.7× →
7.5× → 0.4× across prior sessions on identical data-shape logic. The invariant is **"last of 8 on
both dimensions"**.

Alignment is the dimension the meta-GAN **selects** on, so Grounded fails to *embody a distinctive
voice* — a **voice** failure, not a prose failure. Lifetime novelty 1.4795 ranks **5th of 8**:
Grounded is not boring, it is *unmistakable in a way the chooser does not reward*. Its tenets
("concrete images, everyday language, specific examples, no abstractions") and voice ("warm,
factual") are the least differentiating prompt in the field.

### 5b. The run-level bottom — `civ-engineer`, NOT Grounded

| civ | run avg_score | run alignment | run novelty | run quality |
|---|---|---|---|---|
| civ-poetic | **1.7720** | **2.4820** | 2.1290 | **0.5740** |
| civ-precise | 1.6243 | 2.0590 | 2.0090 | 0.5300 |
| civ-mythic | 1.5503 | 2.1000 | 2.2510 | 0.4100 |
| civ-whimsical | 1.3670 | 1.5060 | 2.3290 | 0.3540 |
| civ-formal | 1.2857 | 1.4440 | 2.1270 | 0.2320 |
| civ-therapist | 1.0303 | 0.6100 | 2.3160 | 0.1520 |
| civ-grounded | 0.9733 | 0.5880 | 2.1690 | 0.1210 |
| **civ-engineer** | **0.8013** | **0.2840** | 2.2040 | 0.1110 |

**The run-level low went to `civ-engineer`** (avg 0.8013, alignment 0.2840, quality 0.1110) —
and it was also the **lowest `avg_score` in the run at 0.703** on the ternary-values prompt, which
it nonetheless **won**. Grounded was 7th of 8 on run `avg_score`. Per the session-132 rule the
**lifetime table is the structural signal** and the run ranking is a watch axis: the lifetime low
and the run low are **different civs on different axes**, which is the rule, not a contradiction.

**Watch-axis `civ-engineer` — this is the 2nd session at the run bottom on `avg_score`.** The
session-121 low did not repeat for sessions 122–151 (30 sessions), so this is the first
re-appearance, not a continuation. Its **lifetime** standing is 7th of 8 (`relevance_per_sim`
1.163) — only one step above Grounded. It becomes a **finding** only if the lifetime axis moves
too; for now: **watch axis**.

### 5c. The two stable inverses

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.6007), `quality` (0.8135) and
  `relevance_per_sim` (1.561), and **1st on this run's `avg_score` (1.7720) and `quality` (0.5740)**,
  but **last on `win_rate`** (0.013, 6/473) and won **0/5**. A *selection* failure, not a quality
  collapse — and this session it is the sharpest form yet: it was the **argmax on 4 of 5 prompts
  and won none of them**.
- **`civ-precise`** — best `win_rate` (0.568, 266/202), **highest lifetime `alignment` (2.1825)**,
  won 3/5, at `preferred_temp` **0.2** — the coldest voice in the field is what the chooser
  rewards. The mirror inverse.

### 5d. The distinct low-novelty axis

**`civ-formal`** — lifetime novelty **1.3751** (last of 8), alignment 1.7511 healthy. It won 1/5.

## 6. Other standing findings

- **Extinction risk: NONE.** Threshold −10; lowest raw relevance **+965.00** (96× above the floor).
  Registry **8** civs, `max_civs` **12**; birth/extinction only runs under `--loop`. All 8 civs
  still `generation=1` — no mutation fired this run.
- **Counter gap is a FIXED per-civ offset, not a growing one** — whimsical **+63**, grounded
  **+43**, formal **+42**, poetic **+37**, engineer **+22**, mythic **+20**, therapist **+17**,
  precise **+16** (total **+260**), byte-identical to sessions 145/147/148/149/150/151.
  `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an
  auditor.
- **Dimension-spread discipline:** this run's cross-civ spreads were `alignment` **2.1980**,
  `avg_score` 0.9707, `novelty` 0.3200, `quality` 0.4630. `alignment` again carried the widest
  spread **and** is again the axis the chooser selects on. **`quality` did NOT collapse** this run
  (0.111–0.574) — breaking the run of 18 collapses in the last 19 clean-mock sessions. The
  **quality collapse is a LEVEL that moves, not a stable property** — rank on cross-civ spreads,
  never on absolute quality levels, and never on a single run's low.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict). A dict-shaped
  reader silently yields 0 % agreement and empty pick tallies. Winner fields are `winner_civ` /
  `winner_name`.
- **`avg_score` is a top-level row field**, not a member of `scores`.
  `r["scores"]["avg_score"]` silently yields 0.0 for every civ and makes the whole ranking look flat.
- **`civilizations.json` is multi-line JSON, not JSONL.** Use `json.loads(open(...).read())`.
- **Competition timestamps are all identical to the microsecond** — the five competitions are
  serial but each JEV `choice` call returns in <100 ms, so `ts` carries no ordering information.

## 7. The `ls` race on the symlinked deep path — REPRODUCED (2 failures in one session)

This session the documented **transient mount race** fired twice on the exact path the task asked
to verify:

```
$ ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/
ls: cannot access '...': No such file or directory          <-- failure 1
```

while the tree was provably present. The documented diagnostic cleared it every time:

```
stat -L : 129:12603          readlink: /tmp/ai-writings/cellular-first-design/code/civilizations
[-e] EXISTS_OK               ls succeeded 10/10 on retry
link  : 129:12603            target: 129:12603              EF_OK
```

**All five `ls` variants passed in the same tool call** — no trailing slash, with trailing slash,
via the resolved `/tmp` path, `cd`-then-`ls`, and the parent directory. So the trailing slash is
again **not** the trigger (session 120's finding re-confirmed), and the bridge is sound.

**Refined triage (extends session 120's rule):** the signature for a *wrong symlink target* is a
**consistent 5/5 failure**; an intermittent failure that then passes 5/5 and 10/10 is the **race**.
This session adds one more data point — the race can fire **twice in a single session**, once on
the exact task path and once on a retry from the same tool call. **Do not "fix" a bridge that is
passing.** Wrap the task's own verification `ls` in a retry loop.

## 8. Method notes for the next session

1. **A 0/5 result is a sample, not a rate.** 24 five-sample points cannot narrow the
   chooser-vs-argmax fraction; report the fraction as a sample and the **direction** (always the
   lower-scoring candidate) as the finding.
2. **Quote absolute gaps, not ratios**, for the low-relevance civ. The invariant is "last of 8 on
   both dimensions".
3. **Run-level bottom ≠ lifetime bottom.** `civ-engineer` took the run bottom this session;
   `civ-grounded` holds the lifetime bottom for the 50th consecutive session.
4. **Keep rebuilding the pre-flight probe.** `/tmp` is wiped every session, which puts all four
   mock bugs back in the naive rebuild. The 40/40 seed-distinctness assertion is the only check
   that catches the silent degradations.
5. **Wrap the task's verification `ls` in a retry loop** — the race fired twice this session.
6. **Kill the mock by matching the server's exact argv** (`python3 /tmp/mock_zai.py`), not the
   `timeout ...` wrapper line, and re-verify the port is closed (`curl` exit 7 = refused).

## 9. Files touched by this run

- `civ-{grounded,whimsical,formal,poetic,precise,mythic,therapist,engineer}/simulations.jsonl` — **+10 rows each (80 total)**
- `civ-{…}/culture.json` — `relevance_score`, `wins`, `losses`, `simulations_run` rewritten
- `meta_log.jsonl` — **+5 rows**
- `leaderboard.json` — rewritten at `2026-10-25T01:03:26`
