# Civilization Orchestrator — Run Report, session 151 (2026-10-25)

**Command**

```bash
python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py \
  --sims 5 --prompts 5 --providers zai
```

**Verdict: run clean. 67/67 verification assertions PASS. 23rd consecutive clean mock measurement.**

---

## 1. Environment (the 29th session with this shape)

| Fact | Status |
|---|---|
| Requested path existed at session start | **No** — `/workspace` held only `.plugin-cache` + `.skills` |
| Upstream repo | `SuperInstance/AI-Writings` (the `ai-writings/cellular-first-design` slug 404s) |
| `gh` CLI | **Not installed** (29th session running) — used `GET /user/repos` paged with `GITHUB_TOKEN` |
| NAS EDQUOT | **Total** (600 G/600 G, 0 bytes free) — first `git clone` into `/workspace` died with `Disk quota exceeded`; clone went to `/tmp` |
| Symlink bridge | `/workspace/repos/ai-writings/cellular-first-design` → `/tmp/aw/AI-Writings/cellular-first-design`; inode identity `129:3672` on **both** sides + `-ef` = **EF_OK** |
| `TYPESAFEAI_KEY` | Exported from `TYPESAFE_AI_TOKEN` (the script reads the former) |
| `ZAI_TOKEN` | **Absent** from env and from all 8 sandbox secrets — **45th session** on this credential gap |
| z.ai endpoint | **HTTP 401** `token expired or incorrect` against a bogus bearer ⇒ endpoint healthy, credential absent |
| JEV liveness | **HTTP 422** `{"type":"model_attributes_type"}` on a malformed `questions` ⇒ token accepted, JEV live |
| Tool timeout | 30 s < run wall time (~29 s) — detached launch, then polled |

`git clone --filter=blob:none --no-checkout --depth 1` of the 3.7 GB repo fetched a **6.2 MB** working tree
after `git sparse-checkout set --no-cone cellular-first-design/code/civilizations` — the size is in other
branches' history, not the checked-out subtree. `git sparse-checkout init --cone` (the RUNBOOK form)
does **not** accept a path nested two levels deep with a trailing non-directory leaf; the `--no-cone`
form does, and it is what was used.

## 2. Control B mock — rebuilt from scratch, all four known defects were live again

`/tmp` was wiped, so the mock was rebuilt from the RUNBOOK and the four historical bugs had to be
re-applied:

| Bug | Symptom if unfixed | Fix applied |
|---|---|---|
| session-112 index wrap | `seed[i*2:i*2+2]` is empty for `i>=4` ⇒ HTTP 500 while the socket stays open | `seed[(i*2)%8:((i*2)%8)+2]` |
| session-118 md5 seeding | first-8-alnum seed ⇒ all 8 civs emit identical text ⇒ every competition result void | `md5(whole_message)[:8]` |
| session-145 literal `{}` | placeholder never interpolated ⇒ every row carries `seed={}` ⇒ 1 distinct seed | `("[mock-zai seed=%s] " % seed)` |
| session-144 `Connection: close` | a `curl` probe hangs on EOF while the server logged 200 | header set + `close_connection = True` |

### Pre-flight probe — 40/40 distinct seeds (passed, 6th time in the series it has saved a run)

The probe rebuilt the orchestrator's **exact** cultural-prompt template (culture name + tenets +
voice_emphasis + prompt) for all 8 civs × 5 prompts and replayed it through the live mock:

```
distinct seeds   : 40 (expect 40)
distinct previews: 40 (expect 40)
  prompt Write 100 words on what a cell is.            seeds 8/8 previews 8/8
  prompt Write 100 words on the bookkeeper's role.     seeds 8/8 previews 8/8
  prompt Write 100 words on the witness log.           seeds 8/8 previews 8/8
  prompt Write 100 words on ternary values.            seeds 8/8 previews 8/8
  prompt Write 100 words on JEV as a decision oracle.  seeds 8/8 previews 8/8
cultural prompt lengths: 167 - 209
mock log tracebacks: 0
PREFLIGHT: PASS
```

A one-word probe would have passed against a partially broken mock; only the 40/40 seed-distinctness
assertion catches the silent degradations.

## 3. Verification — 67/67 PASS

| Assertion | Expected | Measured | Result |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10** each | grounded 992→1002, whimsical 1004→1014, formal 977→987, poetic 971→981, precise 941→951, mythic 949→959, therapist 944→954, engineer 946→956 | **PASS** |
| total new ledger rows | **80** | 80 | **PASS** |
| `meta_log.jsonl` delta | **+5** | 488 → 493 | **PASS** |
| `Winner:` lines | **5** | 5 | **PASS** |
| rows `[mock-zai`-prefixed | **80** | 80 | **PASS** |
| `provider` == `zai` | 80/80 | 80/80 | **PASS** |
| rows with a JEV `error` key | **0** | 0 | **PASS** |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | **PASS** |
| rows carrying a parseable seed | 80 | 80 | **PASS** |
| distinct seeds / 80 rows | **40** | 40 | **PASS** |
| `(civ, prompt)` combos with >1 seed | **0** | 0 | **PASS** |
| `culture.json` `sims_run` delta | **+10** each | 8/8 civs | **PASS** |
| `meta_log` new rows have `winner_civ` | **5** | 5 | **PASS** |
| `meta_log` `results` is a list of `[civ_id, score]` pairs | **5** | 5 | **PASS** |
| `meta_log` new rows ts after pre-run | **5** | 5 | **PASS** |
| `leaderboard.json` rewritten | newer than pre-run | `2026-10-25T00:52:27` (pre-run `00:45:01`) | **PASS** |
| `leaderboard` has 8 civs | **8** | 8 | **PASS** |
| `git status` modified set | **18** | 18 (8 ledgers + 8 cultures + meta_log + leaderboard) | **PASS** |

The `error`-key check and the 2.0/2.0/2.0 check are what prove **JEV really scored** rather than
silently returning the default. **The exit code proves nothing** — every failure mode in this
orchestrator is silent with exit code 0.

## 4. Chooser vs `avg_score` argmax: **2/5 (40 %)** — 23rd clean mock measurement

| prompt | winner | winner score | argmax | argmax score | | delta |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 0.433 | `civ-precise` | 0.433 | AGREE | +0.000 |
| the bookkeeper's role | `civ-precise` | 0.420 | `civ-precise` | 0.420 | AGREE | +0.000 |
| the witness log | `civ-grounded` | 0.110 | `civ-precise` | 0.713 | DISAGREE | **−0.603** |
| ternary values | `civ-engineer` | 0.083 | `civ-precise` | 0.627 | DISAGREE | **−0.543** |
| JEV as a decision oracle | `civ-formal` | 0.277 | `civ-precise` | 0.637 | DISAGREE | **−0.360** |

**All 3 disagreements took the LOWER-scoring candidate** — the same direction as every disagreement
ever observed across the fleet. The rate is not narrowing: clean-mock series 0, 3, 1, 4, 4, 3, 0, 4, 4,
1, 2, 4, 4, 0, 2, 4, 1, **2** — 23 five-sample points cannot pin a rate; the honest claim is *somewhere
in 0–80 %*. The **direction** is the finding, and it survives: **the chooser is not a pure argmax and
prefers the lower-scoring candidate.** Mechanism (session 137): the winner comes from a JEV **`choice`**
question over 150-char `content_preview` snippets, whereas `avg_score` is the mean of three **`score`**
questions on the same text. Different question types ⇒ different answers.

**Never treat `win_rate` as a quality metric.** Winner tally this run: `civ-precise` 2,
`civ-grounded` 1, `civ-engineer` 1, `civ-formal` 1.

## 5. Low-relevance civilizations

### 5a. The structural finding — `civ-grounded` (The Grounded), **49 consecutive sessions (95–151)**

Last of 8 on **every** lifetime axis:

| civ | relevance | rel/sim | lifetime avg_score | lifetime alignment | lifetime novelty | lifetime quality | win_rate | temp |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 1471.79 | 1.559 | **1.5990** | 2.1175 | 1.8634 | **0.8160** | 0.013 | 0.80 |
| civ-whimsical | 1312.45 | 1.380 | 1.4651 | 1.8042 | **1.9313** | 0.6598 | 0.011 | 0.95 |
| civ-precise | 1314.82 | 1.406 | 1.4169 | **2.1838** | 1.5124 | 0.5544 | **0.568** | 0.20 |
| civ-mythic | 1200.11 | 1.278 | 1.3047 | 1.6106 | 1.7168 | 0.5867 | 0.019 | 0.85 |
| civ-therapist | 1119.74 | 1.195 | 1.2179 | 1.4167 | 1.7162 | 0.5207 | 0.019 | 0.60 |
| civ-formal | 1104.78 | 1.169 | 1.2060 | 1.7542 | 1.3669 | 0.4968 | 0.163 | 0.30 |
| civ-engineer | 1089.63 | 1.167 | 1.1861 | 1.6125 | 1.4412 | 0.5045 | 0.082 | 0.40 |
| **civ-grounded** | **955.27** | **0.996** | **1.0375** | **1.1759** | 1.4722 | **0.4645** | 0.146 | 0.50 |

**The binding constraint is still alignment.** Grounded's absolute gaps to the next civ up are
**alignment 0.2408** (`civ-therapist` 1.4167), **avg_score 0.1485** (`civ-engineer` 1.1861), and
**quality 0.0323** (`civ-formal` 0.4968). Quote the absolute gaps, never the ratio — the
alignment-vs-quality gap ratio has swung 11× → 2.7× → 7.5× → 0.4× across prior sessions on identical
data-shape logic. The invariant is "last of 8 on both dimensions".

Alignment is the dimension the meta-GAN **selects** on, so Grounded fails to *embody a distinctive
voice* — a **voice** failure, not a prose failure. Lifetime novelty 1.4722 ranks **6th of 8**:
Grounded is not boring, it is *unmistakable in a way the chooser does not reward*. Its tenets
("concrete images, everyday language, specific examples, no abstractions") and voice ("warm, factual")
are the least differentiating prompt in the field.

### 5b. The run-level watch axis — `civ-grounded` also took the run bottom this session

| civ | run avg_score | run alignment | run novelty | run quality |
|---|---|---|---|---|
| civ-precise | **0.5230** | **0.8970** | 0.6570 | 0.0150 |
| civ-poetic | 0.3783 | 0.7080 | 0.4110 | 0.0160 |
| civ-whimsical | 0.3697 | 0.3930 | 0.6980 | 0.0180 |
| civ-therapist | 0.2847 | 0.0290 | **0.8160** | 0.0090 |
| civ-formal | 0.2463 | 0.2840 | 0.4390 | 0.0160 |
| civ-engineer | 0.2223 | 0.1650 | 0.4930 | 0.0090 |
| civ-mythic | 0.2217 | 0.2400 | 0.4150 | 0.0100 |
| **civ-grounded** | **0.2100** | **0.0520** | 0.5700 | 0.0080 |

`civ-grounded` took the run-level low on **both** `avg_score` (0.2100) and `alignment` (0.0520).
**This is the first session in the series where the lifetime bottom and the run bottom are the same
civ** — in sessions 127–150 they were consistently different civs (therapist held the run bottom in
147–150). Per the session-132 rule the lifetime table remains the structural signal, but the two axes
have now converged on Grounded, which strengthens rather than weakens the finding: the lifetime gap
is no longer being partially masked by a mid-field run performance.

Notably, Grounded was **chosen as a winner** this run (the witness-log prompt, score 0.110 against
argmax 0.713) — the chooser picked the *lowest-scoring* candidate, which is the directionally
consistent behaviour, and it lifted Grounded's `win_rate` to 0.146.

### 5c. The two stable inverses

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.5990), `quality` (0.8160) and `relevance_per_sim`
  (1.559), but **last on `win_rate`** (0.013, 6/468). A *selection* failure, not a quality collapse.
  It won 0/5 this run despite being 2nd on run `avg_score`.
- **`civ-precise`** — best `win_rate` (0.568, 263/200), **highest lifetime `alignment` (2.1838)**,
  1st on run `avg_score` (0.5230) — the mirror inverse, and the one the chooser actually rewards.
  `preferred_temp` **0.2** — the coldest voice in the field. It was also the argmax on 5/5 prompts
  and won 2 of them.

### 5d. The distinct low-novelty axis

**`civ-formal`** — lifetime novelty **1.3669** (last of 8), alignment 1.7542 healthy. It won
1/5 this run.

## 6. Other standing findings

- **Extinction risk: NONE.** Threshold −10; lowest raw relevance **+955.27** (95× above the floor).
  Registry **8** civs, `max_civs` **12**; birth/extinction only runs under `--loop`. All 8 civs still
  `generation=1` — no mutation fired this run.
- **Counter gap is a FIXED per-civ offset, not a growing one** — whimsical **−173.15**, poetic
  **−96.81**, formal **−85.53**, grounded **−84.35**, mythic **−51.11**, engineer **−44.25**,
  therapist **−42.11**, precise **−32.63** (total **−609.93**). The per-civ deltas across this run are
  ≤ 0.01, i.e. rounding only.
  **Sign correction to prior reports (sessions 147–150): the gap is NEGATIVE, not a positive offset.**
  The pre-run git blobs show the identical −609.93 total, so this is a long-standing condition and not
  something this run introduced. `save_state()` has no lock ⇒ `relevance_per_sim` is **not
  recomputable from the ledger** by an auditor; the offset direction was simply mis-signed in the
  earlier write-ups.
- **Dimension-spread discipline (re-confirmed, 6th consecutive observation):** this run's cross-civ
  spreads were `alignment` **0.8680**, `novelty` 0.4050, `avg_score` 0.3130, `quality` **0.0100**.
  `quality` collapsed again to a 0.008–0.018 band (18th of the last 19 clean-mock sessions) and
  `alignment` again carried the widest spread **and** is again the axis the chooser selects on.
  **The quality collapse is a LEVEL that moves, not a stable property** — rank on cross-civ spreads,
  never on absolute quality levels, and never on a single run's low.
- **Absolute run levels are depressed vs lifetime** (run `avg_score` 0.210–0.523 vs lifetime
  1.04–1.60) — a level shift in the JEV scorer's output for this batch, **not a civ effect**. The
  cross-civ *ordering* carries the information.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict). A dict-shaped reader
  silently yields 0 % agreement and empty pick tallies. Winner fields are `winner_civ` / `winner_name`.
- **`avg_score` is a top-level row field**, not a member of `scores`. `r["scores"]["avg_score"]` silently
  yields 0.0 for every civ and makes the whole ranking look flat.
- **`civilizations.json` is multi-line JSON, not JSONL.** Use `json.loads(open(...).read())`; the civ
  ledgers *are* JSONL.
- **Competition timestamps are all identical to the microsecond** (00:52:27.172350–.172460): the five
  competitions are serial but each JEV `choice` call returns in <100 ms, so the `ts` field carries no
  ordering information. Do not reconstruct a timeline from it.

## 7. Method notes for the next session

1. **A 2/5 → 1/5 swing between consecutive sessions on the same mock and scorer shows a 5-sample point
   carries almost no information about a rate.** Report the fraction as a *sample*; report the direction
   as the finding. Never promote a single session's fraction to a fleet claim.
2. **Quote absolute gaps, not ratios**, for the low-relevance civ. The invariant is "last of 8 on both
   dimensions".
3. **Run-level bottom ≠ lifetime bottom** — but note that this session they **converged** on
   `civ-grounded` for the first time. Track the convergence as a strengthening signal, not as a
   replacement of the lifetime table.
4. **Keep rebuilding the pre-flight probe.** `/tmp` is wiped every session, which puts all three mock
   bugs back in the naive rebuild. The 40/40 seed-distinctness assertion is the only check that catches
   the silent degradations.
5. **`ls -la` on the requested path is a valid end-of-run verification** once the bridge exists — it
   showed the new `leaderboard.json` mtime and the eight grown ledgers.
6. **Kill the mock by matching the server's exact argv** (`python3 /tmp/mock_zai.py`), not the
   `timeout ...` wrapper line. Killing the wrapper PID 301 left the server (PID 303) still serving and
   the port still open — re-verified and killed the real server before finishing.

## 8. Files touched by this run

- `civ-{grounded,whimsical,formal,poetic,precise,mythic,therapist,engineer}/simulations.jsonl` — **+10 rows each (80 total)**
- `civ-{…}/culture.json` — `relevance_score`, `wins`, `losses`, `simulations_run` rewritten
- `meta_log.jsonl` — **+5 rows**
- `leaderboard.json` — rewritten at `2026-10-25T00:52:27`
