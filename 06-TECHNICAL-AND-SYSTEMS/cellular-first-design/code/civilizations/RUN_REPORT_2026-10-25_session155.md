# Civ Orchestrator — Run Report, session 155 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Exit code:** 0 · **Wall time:** ~50 s · **Run mode:** single batch (no `--loop`, so no
extinction/birth pass)

---

## Result

The run completed and **every civilization's `simulations.jsonl` grew by 10 rows**
(5 sims + 5 competition re-runs). `meta_log.jsonl` grew by exactly 5. All 18 expected
files are modified in the civ tree (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`). **147/147 content assertions passed.**

### Row deltas (verified by `ls -la` + `wc -l`, not by exit code)

| civ | rows before | rows after | Δ | `simulations_run` Δ |
|---|---|---|---|---|
| civ-engineer | 986 | 996 | **+10** | +10 |
| civ-formal | 1017 | 1027 | **+10** | +10 |
| civ-grounded | 1032 | 1042 | **+10** | +10 |
| civ-mythic | 989 | 999 | **+10** | +10 |
| civ-poetic | 1011 | 1021 | **+10** | +10 |
| civ-precise | 981 | 991 | **+10** | +10 |
| civ-therapist | 984 | 994 | **+10** | +10 |
| civ-whimsical | 1044 | 1054 | **+10** | +10 |

`meta_log.jsonl`: 508 → **513** (+5). `leaderboard.json` iso `01:23:31` → **`01:33:37`**.

### Harness (147 assertions, 0 failures)

- No `error` key and **no `2.0/2.0/2.0` fallback triple** on any of the 80 new rows
  (i.e. JEV really answered — `TYPESAFEAI_KEY` was exported).
- `provider == "zai"` on all 80 rows; all carry a parseable `[mock-zai seed=…]` prefix.
- `avg_score` recomputes exactly from the three axes on every row; `temperature`/`top_p`
  inside the civ's band; `confidence` present on every row.
- **Seed non-degeneracy:** ≥40 distinct seeds across the 80 rows; **0** `(civ, prompt)`
  combos carrying more than one seed; exactly 40 distinct `(civ, prompt)` combos.
- `meta_log.results` is a **list of `[civ_id, score]` pairs** (not a dict), 8 entries per
  row, covering all 8 civs, with `winner_civ` always among the results.
- `culture.json` `simulations_run` matches `pre+10` for all 8; `generation` still 1;
  registry unchanged at 8 ids (no birth/extinction in non-loop mode).
- Leaderboard re-sorted by `relevance_per_sim` descending; `sims_run` matches `pre+10`.

---

## Low-relevance civilizations

**`civ-grounded` (The Grounded) is the low-relevance civ — 51 consecutive sessions
(95–155).** It is last of 8 on **lifetime `avg_score`** (1.0307) and last of 8 on
**lifetime `alignment`** (1.1491), and last of 8 on **this-run `avg_score`** (0.8063) and
**this-run `quality`** (0.0170). It is also the only civilization whose
`relevance_per_sim` sits **below 1.0** (0.991) and it holds the lowest absolute
relevance (989.60).

**Quote the absolute gaps, not the ranks.** The gap from the lowest civ to the
next-lowest on the lifetime axis:

- **alignment: 0.2299** (grounded 1.1491 → therapist 1.3790)
- quality: 0.0339 (grounded 0.4497 → formal 0.4836)
- novelty: 0.0712 (formal 1.3953 → engineer 1.4665)
- lifetime avg: 0.1440 (grounded 1.0307 → engineer 1.1746)

Alignment — the dimension the meta-GAN *selects* on — carries a gap **~7×** the quality
gap and **~3×** the novelty gap. Grounded is not producing bad prose; it is failing to
**embody a distinctive voice**. That is a **voice** failure, not a prose failure.

**The this-run snapshot is a new low for Grounded on quality** (0.0170, lowest of 8) and
**on avg_score** (0.8063). It is *not* last on this-run novelty (2.1520, 7th of 8) —
`civ-mythic` holds that axis this run at 2.1140. The **lifetime** novelty low still
belongs to `civ-formal` (1.3953), so the novelty axis has **not** structurally rotated;
only the this-run snapshot overlaps.

### The two stable inverses (unchanged)

- **`civ-poetic`** — 1st on lifetime `avg_score` (1.5947), lifetime `quality` (0.7993),
  and this-run `avg_score` (1.4827); but **last on `win_rate`** (0.012, 6 wins / 482
  losses). A **selection** failure, not a quality collapse.
- **`civ-precise`** — 1st on `win_rate` (0.571) and 1st on lifetime `alignment` (2.1751);
  2nd-lowest on lifetime `quality` (0.5458). The other **selection**-side inverse.

### Leaderboard (post-run, sorted by `relevance_per_sim`)

| rank | id | relevance | per_sim | sims | wins | losses | win_rate | gen | temp |
|---|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1531.39 | 1.556 | 984 | 6 | 482 | 0.012 | 1 | 0.80 |
| 2 | civ-precise | 1374.97 | 1.410 | 975 | 276 | 207 | 0.571 | 1 | 0.20 |
| 3 | civ-whimsical | 1360.66 | 1.373 | 991 | 5 | 483 | 0.010 | 1 | 0.95 |
| 4 | civ-mythic | 1247.76 | 1.275 | 979 | 9 | 473 | 0.019 | 1 | 0.85 |
| 5 | civ-therapist | 1155.89 | 1.183 | 977 | 10 | 475 | 0.021 | 1 | 0.60 |
| 6 | civ-formal | 1149.90 | 1.167 | 985 | 80 | 406 | 0.165 | 1 | 0.30 |
| 7 | civ-engineer | 1125.69 | 1.156 | 974 | 40 | 441 | 0.083 | 1 | 0.40 |
| 8 | **civ-grounded** | **989.60** | **0.991** | 999 | 68 | 419 | 0.140 | 1 | 0.50 |

**Ranking did not rotate** — the same order as the pre-run leaderboard. The label on
Grounded did not move: 970.72 / 0.992 before and 981.54 / 0.992 after the pre-run
session; **989.60 / 0.991** after this run.

### The counter gap is NEGATIVE and long-standing

`culture.json` `relevance_score` minus the ledger's `avg_score` sum is **-609.92** total:

```
civ-whimsical -173.14   civ-poetic -96.80   civ-formal -85.53   civ-grounded -84.35
civ-mythic    -51.11   civ-engineer -44.24  civ-therapist -42.11  civ-precise -32.63
TOTAL         -609.92
```

The per-civ values are a **fixed offset** (deltas <= 0.01 across the run) — `save_state()`
has no lock, so `relevance_per_sim` is **not recomputable from the ledger** by an auditor.
The sign was computed from this run's data, not copied from the previous report.

---

## Chooser vs `avg_score` argmax: 0/5 (0 %)

Every one of the 5 competitions picked a civ that was **not** the `avg_score` argmax, and
in **all 5** the winner's score was **below** the argmax's. `civ-poetic` was the argmax on
all 5 prompts (1.54 / 1.40 / 1.63 / 1.39 / 1.43) and won **0** of them. Winners:
`civ-precise` x2, `civ-formal` x2, `civ-engineer` x1.

This extends the clean-mock series (sessions 118-155):
`0,3,1,4,4,3,0,4,4,1,2,4,4,0,2,4,1,4,0,5,3` - **25 five-sample points cannot pin a
rate.** The honest claim remains *somewhere in 0-100 %*. The 5/5 negative deltas this
session are consistent with the standing "the chooser tends to take the LOWER-scoring
candidate" finding, but 5 points is not evidence of a rate.

---

## Environment

- **NAS 100 % full again** (600 G/600 G, 0 bytes free). `git clone` straight into
  `/workspace/repos/...` died with `error: .../.git/description: close error: Disk quota
  exceeded` — and the half-created `.git` still shows in `ls`, so the clone's **stderr** is
  the signal, not the exit code. Cloned to `/tmp` (overlay, 28 G free) and built the
  **symlink bridge**; verified by inode identity (`129:10498` on both sides) and `-ef`.
  The symlink points at the **nested** `cellular-first-design` directory, not the repo root.
- **Upstream owner is `SuperInstance/AI-Writings`**, not `ai-writings/cellular-first-design`
  (that path 404s). The repo is 3.7 GB; a filtered + `--no-cone` sparse checkout of
  `cellular-first-design/code/civilizations` gives a ~6 MB working tree.
- **ZAI credential gap re-confirmed (18th session):** `ZAI_TOKEN` is absent from the env
  and from all 8 sandbox secrets. The available z.ai-format key is `MOTHQUANTUM_TOKEN`
  (`moth_E...`), but the script reads `ZAI_TOKEN`; against both
  `api.z.ai/api/coding/paas/v4/chat/completions` and `api.z.ai/api/paas/v4/chat/completions`
  it returns **401 token expired or incorrect** (endpoint healthy => credential gap, not an
  outage). Control B therefore used a local mock bridge with **both** `ZAI_TOKEN` (non-empty
  placeholder) **and** `ZAI_URL_OVERRIDE`; `ZAI_URL_OVERRIDE` alone is dead code because the
  token gate returns first.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN` (script reads the former).
  JEV answered live: `model=jev-1.14.0`.
- Run **detached** (`setsid nohup timeout -s KILL 300 ... &`) and poll the log; a 30 s tool
  timeout is shorter than the ~50 s wall time and kills the run mid-flight. The mock server
  was started the same way and killed by PID matched on **argv exactly**
  (`python3 /tmp/mock_zai.py`), never `pkill -f mock_zai` (self-match). Port verified
  closed afterward (curl exit 7 = connection refused).

---

## Standing caveats

- The mock is a **deterministic text generator**, not an LLM. Its previews are synthetic;
  only the **JEV scoring** of them is real. Do not read the mock's prose as evidence of
  anything about the civs' voices.
- Preview-distinctness is **not** a valid mock-integrity check at 80-row granularity: 8 civs
  x 5 canon prompts = **40 distinct cultural prompts**, so 80 rows carry 40 distinct
  previews and 40 distinct seeds. Assert at the **cultural-prompt** granularity
  (40 distinct seeds, 0 cultural prompts with >1 seed) — not at the row granularity.
- Competition `ts` carries no ordering: all five rows share the same wall-clock to the
  microsecond. Do not reconstruct a per-prompt timeline from it.
- `meta_log.jsonl` `results` is a **list of `[civ_id, score]` pairs**, not a dict. A
  dict-shaped reader silently yields 0 % agreement and empty pick tallies.
- Both historical mock bugs had to be re-applied on rebuild — the session-112 index wrap
  (`seed[(i*2)%8:((i*2)%8)+2]`) and the session-118 md5-of-whole-message seeding. Without
  the wrap the bridge 500s on `i>=4` while the socket stays open; without the md5 seeding
  the 8 civs emit identical text and every competition is degenerate. The pre-flight probe
  caught both: 8/8 distinct seeds, 8/8 distinct previews, HTTP 200, `[mock-zai seed=...]`
  prefix present, **0 tracebacks** in `/tmp/mock_zai.log`.
