# Civ Orchestrator — Run Report, session 156 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Exit code:** 0 · **Wall time:** ~22 s · **Run mode:** single batch (no `--loop`, so no
extinction/birth pass) · **Baseline:** `c8275b5` (session 155)

---

## Result

The run completed and **every civilization's `simulations.jsonl` grew by exactly 10 rows**
(5 sims + 5 competition re-runs). `meta_log.jsonl` grew by exactly 5. All 18 expected
files are modified in the civ tree (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`). **77/77 content assertions passed.**

### Row deltas (verified by `ls -la` + `wc -l`, not by exit code)

| civ | rows before | rows after | Δ | `simulations_run` Δ |
|---|---|---|---|---|
| civ-engineer | 996 | 1006 | **+10** | +10 |
| civ-formal | 1027 | 1037 | **+10** | +10 |
| civ-grounded | 1042 | 1052 | **+10** | +10 |
| civ-mythic | 999 | 1009 | **+10** | +10 |
| civ-poetic | 1021 | 1031 | **+10** | +10 |
| civ-precise | 991 | 1001 | **+10** | +10 |
| civ-therapist | 994 | 1004 | **+10** | +10 |
| civ-whimsical | 1054 | 1064 | **+10** | +10 |

`meta_log.jsonl`: 513 → **518** (+5). `leaderboard.json` iso `01:33:37` → **`01:46:04`**.

`ls -la` on the civ tree shows all 8 ledgers with mtime **01:46** (clone time was 01:44),
confirming the new rows are on disk at the bridged path.

### Harness (77 assertions, 0 failures)

- No `error` key and **no `2.0/2.0/2.0` fallback triple** on any of the 80 new rows
  (i.e. JEV really answered — `TYPESAFEAI_KEY` was exported).
- `provider == "zai"` on all 80 rows; all carry a parseable `[mock-zai seed=…]` prefix.
- `avg_score` recomputes exactly from the three axes on every row; `confidence` present on
  every row; **80 distinct JEV score triples** and **30 distinct confidences** (a silent
  2.0 default would give one repeated triple and constant confidence).
- **Seed non-degeneracy:** exactly **40 distinct seeds** across the 80 rows; **40** distinct
  `(civ, prompt)` combos; **0** combos carrying more than one seed.
- `meta_log.results` is a **list of `[civ_id, score]` pairs** (not a dict), 8 entries per
  row, covering all 8 civs, with `winner_civ` always among the results.
- `culture.json` `simulations_run` = `pre+10` for all 8; `generation` still 1; win+loss +5;
  registry unchanged at 8 ids (no birth/extinction in non-loop mode).
- Leaderboard re-sorted by `relevance_per_sim` descending; `sims_run` = `pre+10` for all 8.

### Competition results (5 prompts)

| prompt | winner | argmax on `avg_score` | delta (winner − argmax) |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | −0.0633 |
| the bookkeeper's role | civ-precise | civ-mythic | −0.0933 |
| the witness log | civ-engineer | civ-precise | −0.3167 |
| ternary values | civ-engineer | civ-poetic | −0.5433 |
| JEV as a decision oracle | civ-formal | civ-poetic | −0.3900 |

**Chooser vs `avg_score` argmax: 0/5 (0 %)** — agreement 0/5, winners `civ-precise` x2,
`civ-engineer` x2, `civ-formal` x1.

**All 5 disagreements are NEGATIVE** (the winner scored *below* the argmax). This
re-confirms the standing "the chooser tends to take the LOWER-scoring candidate" direction
under a clean (non-degenerate) mock. 5 samples cannot pin a rate; the clean-mock series
now reads `0,3,1,4,4,3,0,4,4,1,2,4,4,0,2,4,1,4,0,5,3,0` — **24 five-sample points cannot
pin a rate either**. The honest claim remains *somewhere in 0-100 %*.

Note `civ-poetic` was the argmax on **3 of 5** prompts (and near-argmax on a 4th) and won
**zero** — the stable selection-failure inverse, reproduced.

---

## Low-relevance civilizations

**`civ-grounded` (The Grounded) is the low-relevance civ — 52 consecutive sessions
(95–156).** It is last of 8 on **lifetime `avg_score`** (1.0309) and last of 8 on
**lifetime `alignment`** (1.1447), and last of 8 on **this-run `avg_score`** (1.0520) and
**this-run `quality`** (0.0610). It is also the only civilization whose
`relevance_per_sim` sits **below 1.0** (0.991) and it holds the lowest absolute
relevance (1000.12).

**Quote the absolute gaps, not the ranks.** Gap from the lowest civ to the next-lowest on
the lifetime axis:

- **alignment: 0.2253** (grounded 1.1447 → therapist 1.3700)
- **avg_score: 0.1437** (grounded 1.0309 → engineer 1.1745)
- **novelty: 0.0716** (formal 1.4046 → engineer 1.4762) — a *different* civ
- **quality: 0.0345** (grounded 0.4460 → formal 0.4805)

The **alignment** gap is the structural one and it is by far the widest (6.5x the quality
margin). `alignment` is the dimension the meta-GAN *selects* on, so Grounded fails to
**embody a distinctive voice**, not merely to write well — a *voice* failure, not a prose
failure. Grounded is **above median on lifetime novelty** (1.502, 5th of 8): it is not
boring, just *unmistakable in a way the chooser does not reward*.

**`civ-formal` is the distinct low-novelty axis** (lifetime novelty 1.4046, last of 8) —
not the same finding, a different dimension.

**Watch axis `civ-therapist`** — last of 8 on **this-run `avg_score`** (1.0257) and
**this-run `alignment`** (0.4840), but 6th of 8 on lifetime `avg_score` (1.2034) and
**above** Grounded on lifetime alignment (1.3700). Run-level low and lifetime low are
**different civs on different axes** — that is the session-132 rule, not a contradiction.
Therapist is a **watch axis**, not a finding.

### The two stable inverses (both hold)

- **`civ-poetic`** — 1st of 8 on lifetime `avg_score` (1.5953) / `quality` (0.795) /
  `relevance_per_sim` (1.557), and 1st on this run's `avg_score` (1.6577) — but **last on
  `win_rate`** (0.012) and won **0/5** while being argmax on 3/5. A *selection* failure,
  not a quality collapse.
- **`civ-precise`** — best `win_rate` (0.570), **highest lifetime alignment** (2.1711),
  1st on lifetime `avg_score` rank 3 — and won 2/5 this run. The mirror inverse: the
  coldest voice is what the chooser rewards.

### Dimension spreads (rank on spreads, never on absolute levels)

This run's cross-civ spreads: `alignment` **1.7790**, `avg_score` 0.6320, `quality`
0.2790, `novelty` 0.1330. `alignment` again carried the widest spread **and** is again
the axis the chooser selects on. The `quality` band was 0.061-0.340 (a 0.279 spread) —
wider than the collapsed 0.010-0.028 bands of the last several clean-mock sessions, but
still a *level* that moves, not a stable property.

**Absolute run levels depressed vs lifetime** (run `avg_score` 1.026-1.658 vs lifetime
1.031-1.595) — a level shift in the JEV scorer's output for this batch, **not a civ
effect**; the cross-civ *ordering* carries the information.

### Extinction risk: NONE

Threshold −10; lowest raw relevance **+1000.12**, 100x above the floor. Registry 8 civs,
`max_civs` 12, all 8 still `generation=1`. Birth/extinction only runs under `--loop`, and
this was a single batch.

### Counter gap: a FIXED per-civ offset, byte-identical to session 151

`culture.json` `relevance_score` minus the ledger's `avg_score` sum, **pre-run vs
post-run, delta = 0.0000 on all 8 civs**:

```
civ-whimsical -173.14   civ-poetic -96.80   civ-formal -85.53   civ-grounded -84.35
civ-mythic    -51.11   civ-engineer -44.24  civ-therapist -42.12  civ-precise -32.63
TOTAL         -609.93
```

The sign is **negative** and the per-civ values are a **fixed offset**, not an
accumulating leak. `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable
from the ledger** by an auditor.

---

## Environment

- **NAS 100 % full again** (600 G/600 G, 0 bytes free). `git clone` straight into
  `/workspace/repos/...` died with `error: .../.git/description: close error: Disk quota
  exceeded` — the half-created `.git` still shows in `ls`, so the clone's **stderr** is the
  signal, not the exit code. Cloned to `/tmp` (overlay, 28 G free) and built the
  **symlink bridge**; verified by inode identity (`129:524` on both sides) and `-ef`. The
  symlink points at the **nested** `cellular-first-design` directory, not the repo root.
- **Upstream owner is `SuperInstance/AI-Writings`**, not `ai-writings/cellular-first-design`
  (that path 404s). Found via GitHub **code search** on the path
  `cellular-first-design/code/civilizations/civilization_orchestrator.py` — repo
  `SuperInstance/AI-Writings` id `1176209018`. REST core rate limit was exhausted
  (5000/5000) at session start, so `GET /user/repos` was unusable; **GraphQL still had
  4999 points** and enumerated all 4000 visible repos, and `search/code` still answered.
  **`gh` is not installed** (29th session).
- **ZAI credential gap re-confirmed (19th session):** `ZAI_TOKEN` is absent from the env
  and from all 8 sandbox secrets. The available z.ai-format key is `MOTHQUANTUM_TOKEN`
  (`moth_E...`), but the script reads `ZAI_TOKEN`; against both
  `api.z.ai/api/coding/paas/v4/chat/completions` and `api.z.ai/api/paas/v4/chat/completions`
  it returns **401 token expired or incorrect** (endpoint healthy => credential gap, not an
  outage). Control B therefore used a local mock bridge with **both** `ZAI_TOKEN` (non-empty
  placeholder) **and** `ZAI_URL_OVERRIDE`; `ZAI_URL_OVERRIDE` alone is dead code because the
  token gate returns first.
- The mock was rebuilt with **both load-bearing historical fixes**: the session-112 index
  wrap (`seed[(i*2)%8:((i*2)%8)+2]`, without which the bridge 500s on `i>=4` while the
  socket stays open) and the session-118 **md5-of-whole-message** seeding (without which
  the 8 civs emit identical text and every competition is degenerate). Pre-flight probe
  caught the pre-run state: **8/8 distinct seeds, 8/8 distinct previews, 8/8 distinct
  template md5s, 40/40 combos, 0 tracebacks**.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN` (script reads the former).
  JEV answered live: `model=jev-1.14.0`, probe score 0.45 / confidence 0.63.
- Run **detached** (`setsid nohup timeout -s KILL 300 ... &`) and poll the log; the mock
  was started the same way and killed by PID matched on **argv exactly**
  (`python3 /tmp/mock_zai.py`), never `pkill -f mock_zai` (self-match). Port verified
  closed afterward (curl exit 7 = connection refused), and no mock process remained.

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
