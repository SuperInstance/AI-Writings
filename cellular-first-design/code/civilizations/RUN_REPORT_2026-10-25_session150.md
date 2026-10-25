# Civilization Orchestrator — Run Report, session 150 (2026-10-25)

**Command**

```bash
python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py \
  --sims 5 --prompts 5 --providers zai
```

**Verdict: run clean. 15/15 verification assertions PASS. 22nd consecutive clean mock measurement.**

---

## 1. Environment (the 28th session with this shape)

| Fact | Status |
|---|---|
| Requested path existed at session start | **No** — `/workspace` held only `.plugin-cache` + `.skills` |
| Upstream repo | `SuperInstance/AI-Writings` (the `ai-writings/cellular-first-design` slug 404s) |
| `gh` CLI | **Not installed** (28th session running) — used `GET /search/repositories?q=…` with `GITHUB_TOKEN` |
| NAS EDQUOT | **Total** (600 G/600 G, 0 bytes free) — clone went to `/tmp` (overlay, 28 G free) |
| Symlink bridge | `/workspace/repos/ai-writings/cellular-first-design` → `/tmp/AI-Writings/cellular-first-design`; inode identity `129:12605` on **both** sides + `-ef` = **EF_OK** |
| `TYPESAFEAI_KEY` | Exported from `TYPESAFE_AI_TOKEN` (the script reads the former) |
| `ZAI_TOKEN` | **Absent** from env and from all 8 sandbox secrets — **44th session** on this credential gap |
| z.ai endpoint | **HTTP 401** `token expired or incorrect` against a bogus bearer ⇒ endpoint healthy, credential absent |
| JEV liveness | **HTTP 422** `{"type":"dict_type"}` on a malformed `questions` ⇒ token accepted, JEV live |
| Tool timeout | 30 s < run wall time (~28 s of polling) — detached launch, then polled |

`git clone --depth 1` of the 3.7 GB repo fetched in ~25 s to a **6.2 MB** working tree — the
size is in other branches' history, not the checked-out subtree.

## 2. Control B mock — rebuilt from scratch, both historical bugs were live again

`/tmp` was wiped, so the mock was rebuilt from the RUNBOOK and **three** known defects had to
be re-applied:

| Bug | Symptom if unfixed | Fix applied |
|---|---|---|
| session-112 index wrap | `seed[i*2:i*2+2]` is empty for `i>=4` ⇒ HTTP 500 while the socket stays open | `seed[(i*2)%8:((i*2)%8)+2]` |
| session-118 md5 seeding | first-8-alnum seed ⇒ all 8 civs emit identical text ⇒ every competition result void | `md5(whole_message)[:8]` |
| session-145 literal `{}` | placeholder never interpolated ⇒ every row carries `seed={}` ⇒ 1 distinct seed | `("[mock-zai seed=%s] " % seed)` |
| session-144 `Connection: close` | a `curl` probe hangs on EOF while the server logged 200 | header set + `close_connection = True` |

### Pre-flight probe — 40/40 distinct seeds (passed, 5th time in the series it has saved a run)

The probe rebuilt the orchestrator's **exact** `cultural_prompt()` template (culture name +
tenets + voice_emphasis + prompt) for all 8 civs × 5 prompts and replayed it through the live
mock:

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

A one-word probe would have passed against a partially broken mock; only the 40/40
seed-distinctness assertion catches the silent degradations.

## 3. Verification — 15/15 PASS

| Assertion | Expected | Measured | Result |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10** each | grounded 982→992, whimsical 994→1004, formal 967→977, poetic 961→971, precise 931→941, mythic 939→949, therapist 934→944, engineer 936→946 | **PASS** |
| total new ledger rows | **80** | 80 | **PASS** |
| `meta_log.jsonl` delta | **+5** | 483 → 488 | **PASS** |
| `Winner:` lines | **5** | 5 | **PASS** |
| rows `[mock-zai`-prefixed | **80** | 80 | **PASS** |
| `provider` == `zai` | 80/80 | 80/80 | **PASS** |
| rows with a JEV `error` key | **0** | 0 | **PASS** |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | **PASS** |
| rows carrying a parseable seed | 80 | 80 | **PASS** |
| distinct seeds / 80 rows | **40** | 40 | **PASS** |
| `(civ, prompt)` combos with >1 seed | **0** | 0 | **PASS** |
| per-prompt distinct seeds AND previews | **8/8 × 5 prompts** | 8/8 on all 5 | **PASS** |
| sim→competition ts gap at index 4 | 8/8 civs | 8/8 (0.62 s intra-sim; 16.9–26.3 s sim→competition) | **PASS** |
| `leaderboard.json` rewritten | newer than pre-run | `2026-10-25T00:45:01` (pre-run `00:34:43`) | **PASS** |
| 80 rows collected from per-civ tails | 80 | 80 | **PASS** |

The `error`-key check and the 2.0/2.0/2.0 check are what prove **JEV really scored** rather
than silently returning the default. **The exit code proves nothing** — every failure mode in
this orchestrator is silent with exit code 0.

## 4. Chooser vs `avg_score` argmax: **1/5 (20 %)** — 22nd clean mock measurement

| prompt | winner | winner score | argmax | argmax score | | delta |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 0.900 | `civ-precise` | 0.900 | AGREE | +0.000 |
| the bookkeeper's role | `civ-formal` | 0.383 | `civ-precise` | 0.850 | DISAGREE | **−0.467** |
| the witness log | `civ-formal` | 0.170 | `civ-precise` | 0.993 | DISAGREE | **−0.823** |
| ternary values | `civ-precise` | 0.553 | `civ-poetic` | 0.667 | DISAGREE | **−0.113** |
| JEV as a decision oracle | `civ-formal` | 0.327 | `civ-poetic` | 0.850 | DISAGREE | **−0.523** |

**All 4 disagreements took the LOWER-scoring candidate** — the same direction as every
disagreement ever observed across the fleet. The rate is not narrowing: clean-mock series
0, 3, 1, 4, 4, 3, 0, 4, 4, 1, 2, 4, 4, 0, 2, 4, **1** — 22 five-sample points cannot pin a
rate; the honest claim is *somewhere in 0–80 %*. The **direction** is the finding, and it
survives: **the chooser is not a pure argmax and prefers the lower-scoring candidate.**
Mechanism (session 137): the winner comes from a JEV **`choice`** question over 150-char
`content_preview` snippets, whereas `avg_score` is the mean of three **`score`** questions on
the same text. Different question types ⇒ different answers.

**Never treat `win_rate` as a quality metric.** Winner tally this run: `civ-formal` 3,
`civ-precise` 2.

## 5. Low-relevance civilizations

### 5a. The structural finding — `civ-grounded` (The Grounded), **48 consecutive sessions (95–150)**

Last of 8 on **every** lifetime axis:

| civ | relevance | rel/sim | lifetime avg_score | lifetime alignment | lifetime novelty | lifetime quality | win_rate | temp |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 1468.00 | 1.572 | **1.6115** | 2.1320 | 1.8784 | **0.8242** | 0.013 | 0.80 |
| civ-whimsical | 1308.75 | 1.391 | 1.4760 | 1.8182 | **1.9436** | 0.6661 | 0.011 | 0.95 |
| civ-precise | 1309.59 | 1.416 | 1.4264 | **2.1975** | 1.5215 | 0.5601 | **0.570** | 0.20 |
| civ-mythic | 1197.89 | 1.289 | 1.3161 | 1.6251 | 1.7305 | 0.5928 | 0.020 | 0.85 |
| civ-therapist | 1116.90 | 1.205 | 1.2278 | 1.4314 | 1.7258 | 0.5261 | 0.020 | 0.60 |
| civ-formal | 1102.32 | 1.179 | 1.2158 | 1.7693 | **1.3764** | 0.5017 | 0.163 | 0.30 |
| civ-engineer | 1087.40 | 1.177 | 1.1962 | 1.6278 | 1.4512 | 0.5098 | 0.081 | 0.40 |
| **civ-grounded** | **953.17** | **1.004** | **1.0459** | **1.1872** | 1.4813 | **0.4691** | 0.145 | 0.50 |

**The binding constraint is still alignment.** Grounded's alignment gap to the next civ is
**0.0655** (`civ-therapist` 1.4314) and its quality gap is **0.1581** — this session the
**quality** gap is the wider of the two, the first time in the series the ratio inverted
(it was 7.5× the other way in session 149). Grounded is still last on *both* axes, so the
verdict is unchanged; but the **quote the absolute gaps, never the ratio** — the ratio has
swung from 11× (s.125) to 2.7× (s.145) to 7.5× (s.149) to **0.4×** (s.150) on identical
data-shape logic. The invariant is "last of 8 on both dimensions", not the ratio.

Alignment is the dimension the meta-GAN **selects** on, so Grounded fails to *embody a
distinctive voice* — a **voice** failure, not a prose failure. Lifetime novelty 1.4813 is
**above median**: Grounded is not boring, it is *unmistakable in a way the chooser does not
reward*. Its tenets ("concrete images, everyday language, specific examples, no abstractions")
and voice ("warm, factual") are the least differentiating prompt in the field.

### 5b. The run-level watch axis — `civ-therapist`, **4th session at the run bottom**

| civ | run avg_score | run alignment | run novelty | run quality |
|---|---|---|---|---|
| civ-precise | **0.7767** | **1.3130** | 0.9890 | 0.0280 |
| civ-poetic | 0.6490 | 0.7870 | **1.1340** | 0.0260 |
| civ-engineer | 0.3750 | 0.2350 | 0.8780 | 0.0120 |
| civ-mythic | 0.3310 | 0.1640 | 0.8190 | 0.0100 |
| civ-whimsical | 0.3177 | 0.2130 | 0.7300 | 0.0100 |
| civ-formal | 0.2933 | 0.1860 | **0.6840** | 0.0100 |
| civ-grounded | 0.2767 | 0.0790 | 0.7410 | **0.0100** |
| **civ-therapist** | **0.2650** | **0.0210** | 0.7640 | 0.0100 |

`civ-therapist` took the run-level low on **both** `avg_score` (0.2650) and `alignment`
(0.0210) — its **4th** session at the run bottom (147, 148, 149, 150). But its **lifetime**
standing is mid-field (`avg_score` 1.2278, 5th of 8). Per the session-132 rule, the lifetime
table is the structural signal and the run ranking is the watch axis: **`civ-therapist` stays
a watch axis, not a finding** — it becomes one only if the lifetime axis moves too.

`civ-grounded` was 7th of 8 on run `avg_score` — it did **not** take the run-level low for
the first time in 4 sessions (127 whimsical, 128/129/130/133/134/136 grounded, 138 therapist,
141 therapist, 144 grounded, 145 therapist, 147/148/149 therapist or mythic, **150 therapist**).
The lifetime low and the run-level low are **different civs on different axes** — that is
the rule, not a contradiction.

### 5c. The two stable inverses

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.6115), `quality` (0.8242) and
  `relevance_per_sim` (1.572), but **last on `win_rate`** (0.013, 6/463). A *selection*
  failure, not a quality collapse. It won 0/5 this run despite being 2nd on run `avg_score`.
- **`civ-precise`** — best `win_rate` (0.570, 261/197), **highest lifetime `alignment`
  (2.1975)**, 1st on run `avg_score` (0.7767) — the mirror inverse, and the one the chooser
  actually rewards. `preferred_temp` **0.2** — the coldest voice in the field.

### 5d. The distinct low-novelty axis

**`civ-formal`** — lifetime novelty **1.3764** (last of 8), alignment 1.7693 healthy. It won
3/5 this run, the first time in the series `civ-formal` has out-polled `civ-precise`.

## 6. Other standing findings

- **Extinction risk: NONE.** Threshold −10; lowest raw relevance **+953.17** (95× above the
  floor). Registry **8** civs, `max_civs` **12**; birth/extinction only runs under `--loop`.
  All 8 civs still `generation=1`.
- **Counter gap is a FIXED per-civ offset, not a growing one** — whimsical **+63**, grounded
  **+43**, formal **+42**, poetic **+37**, engineer **+22**, mythic **+20**, therapist **+17**,
  precise **+16** (total +260), byte-identical to sessions 147/148/149. `save_state()` has
  no lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.
- **Dimension-spread discipline (re-confirmed, 5th consecutive observation):** this run's
  cross-civ spreads were `alignment` **1.2920**, `avg_score` 0.5117, `novelty` 0.4500,
  `quality` **0.0180**. `quality` collapsed again to a 0.010–0.028 band (17th of the last 18
  clean-mock sessions) and `alignment` again carried the widest spread **and** is again the
  axis the chooser selects on. **The quality collapse is a LEVEL that moves, not a stable
  property** — rank on cross-civ spreads, never on absolute quality levels, and never on a
  single run's low.
- **Absolute run levels are depressed vs lifetime** (run `avg_score` 0.265–0.777 vs lifetime
  1.05–1.61) — a level shift in the JEV scorer's output for this batch, **not a civ effect**.
  The cross-civ *ordering* carries the information.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict). A
  dict-shaped reader silently yields 0 % agreement and empty pick tallies. Winner fields are
  `winner_civ` / `winner_name`.
- **`avg_score` is a top-level row field**, not a member of `scores`. `r["scores"]["avg_score"]`
  silently yields 0.0 for every civ and makes the whole ranking look flat.
- **`civilizations.json` is multi-line JSON, not JSONL.** Use `json.loads(open(...).read())`;
  the civ ledgers *are* JSONL.

## 7. Method notes for the next session

1. **A 1/5 → 4/5 swing between consecutive sessions on the same mock and scorer shows a
   5-sample point carries almost no information about a rate.** Report the fraction as a
   *sample*; report the direction as the finding. Never promote a single session's fraction
   to a fleet claim.
2. **Quote absolute gaps, not ratios, for the low-relevance civ.** The alignment-vs-quality
   gap ratio has swung 11× → 2.7× → 7.5× → 0.4× across four sessions on the same structural
   claim. The invariant is "last of 8 on both dimensions".
3. **Run-level bottom ≠ lifetime bottom.** Four different civs have taken the run-level low
   in the last five sessions. Only the lifetime table is a finding.
4. **Keep rebuilding the pre-flight probe.** `/tmp` is wiped every session, which puts all
   three mock bugs back in the naive rebuild. The 40/40 seed-distinctness assertion is the
   only check that catches the silent degradations.
5. **`ls -la` on the requested path is a valid end-of-run verification** once the bridge
   exists — it showed the new `leaderboard.json` mtime and the eight grown ledgers.

## 8. Files touched by this run

- `civ-{grounded,whimsical,formal,poetic,precise,mythic,therapist,engineer}/simulations.jsonl` — **+10 rows each (80 total)**
- `civ-{…}/culture.json` — `relevance_score`, `wins`, `losses`, `simulations_run` rewritten
- `meta_log.jsonl` — **+5 rows**
- `leaderboard.json` — rewritten at `2026-10-25T00:45:01`
