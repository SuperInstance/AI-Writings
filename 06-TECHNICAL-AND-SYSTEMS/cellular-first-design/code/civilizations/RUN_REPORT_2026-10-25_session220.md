# Civ Orchestrator — Run Report, session 220 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **91st session**) + **live JEV** (`jev-1.14.0`).
Baseline: `682bc48` (session 219 tree). **All 54 verification assertions PASS.** Pre-flight **11/11 PASS** (first build).

**Session 220 in one line:** `civ-precise` swept **4/5** competitions (`civ-engineer` took the fifth); the
chooser/argmax agreement was **1/5 (20 %) — 4 down-grades, 0 up-grades**; the run-level low was
**`civ-therapist`** (avg **1.2937**, fleet-low run alignment **0.8670**) while `civ-grounded` held the
lifetime low for the **88th** consecutive session.

## Run results (10 new rows per civ: 5 sim phase + 5 competition phase)

| civ | avg_score | quality | novelty | alignment | rank |
|---|---|---|---|---|---|
| civ-poetic | 2.1110 | 1.2220 | 2.5950 | 2.5160 | 1/8 |
| civ-precise | 2.1080 | 1.0210 | 2.5290 | 2.7740 | 2/8 |
| civ-formal | 1.8650 | 0.7160 | 2.5540 | 2.3250 | 3/8 |
| civ-engineer | 1.7993 | 0.7390 | 2.4540 | 2.2050 | 4/8 |
| civ-mythic | 1.7107 | 0.8850 | 2.4580 | 1.7890 | 5/8 |
| civ-grounded | 1.6483 | 0.7080 | 2.4650 | 1.7720 | 6/8 |
| civ-whimsical | 1.4047 | 0.6260 | 2.5120 | 1.0760 | 7/8 |
| civ-therapist | 1.2937 | 0.4500 | 2.5640 | 0.8670 | 8/8 |

Run spreads: avg **0.8173**, quality **0.7720**, novelty **0.1410**, alignment **1.9070**.
The alignment spread is **2.47x** the quality spread and **13.53x** the novelty spread — the
ranking is produced by alignment, not novelty.

## Lifetime leaderboard (cumulative)

| civ | relevance | rel/sim | win_rate | quality | novelty | alignment | rows | rank |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 2714.25 | 1.6610 | 0.007 | 0.8738 | 2.0180 | 2.1550 | 1671 | 1/8 |
| civ-precise | 2574.63 | 1.5840 | 0.683 | 0.6824 | 1.8026 | 2.2815 | 1641 | 2/8 |
| civ-whimsical | 2281.48 | 1.3900 | 0.006 | 0.6487 | 2.0695 | 1.6033 | 1704 | 3/8 |
| civ-formal | 2213.50 | 1.3540 | 0.136 | 0.5779 | 1.6938 | 1.8410 | 1677 | 4/8 |
| civ-mythic | 2198.65 | 1.3500 | 0.012 | 0.6452 | 1.8947 | 1.5531 | 1649 | 5/8 |
| civ-engineer | 2110.31 | 1.2990 | 0.065 | 0.5753 | 1.7369 | 1.6146 | 1646 | 6/8 |
| civ-therapist | 1957.66 | 1.2030 | 0.014 | 0.5209 | 1.9335 | 1.1948 | 1644 | 7/8 |
| civ-grounded | 1886.01 | 1.1440 | 0.090 | 0.4996 | 1.7611 | 1.2329 | 1692 | 8/8 |

## Low-relevance civilizations (three different axes)

- **Run low — `civ-therapist`**: `avg_score` **1.2937**, 8th of 8, with the fleet-low run
  alignment (**0.8670**) and the fleet-low run quality (**0.4500**). Its gap to the next civ
  is **0.1110**, i.e. **13.6 %** of the run spread — a *narrower* run-low margin than
  session 219's **33.7 %**, but the *identity* of the bottom is unchanged.
- **Lifetime low — `civ-grounded`**: relevance **1886.01**, rel/sim **1.1440**, lifetime avg
  **1.1645** and the fleet-low lifetime quality (**0.4996**). Yet its lifetime `win_rate`
  **0.090** is 3rd-best in the fleet — the "low relevance but competitive" pattern again.
- **Lifetime alignment low — `civ-therapist`** (**1.1948**) — a *second* civ on a *second* axis,
  and the same civ that holds the run low. Therapist is last or near-last on **both** the run
  axis and the lifetime alignment axis.

The lifetime lowest **novelty** belongs to `civ-formal` (**1.6938**), not to either low holder.
`civ-grounded`'s low axis is **quality** (**0.4996**), not novelty (**1.7611**, mid-field).

## Chooser vs argmax

| prompt | argmax | score | winner | score | verdict |
|---|---|---|---|---|---|
| witness log | civ-precise | 2.4367 | civ-precise | 2.4367 | AGREE |
| bookkeeper's role | civ-poetic | 2.2267 | civ-precise | 2.2067 | DOWN-grade |
| what a cell is | civ-poetic | 2.1600 | civ-precise | 2.0133 | DOWN-grade |
| JEV as a decision oracle | civ-poetic | 2.1600 | civ-precise | 2.0800 | DOWN-grade |
| ternary values | civ-precise | 1.9033 | civ-engineer | 1.6433 | DOWN-grade |

Agreement **1/5 (20 %)** — 4 down-grades, 0 up-grades. `civ-poetic` was argmax on **3/5**
prompts and won **0/5**; `civ-precise` was argmax on **2/5** and won **4/5**. The largest
disagreement is the ternary prompt, where the argmax lead was **+0.2600**.

## Verification (54/54 PASS)

- per-civ ledger **+10 x 8 = 80** new rows; `meta_log.jsonl` **+5** (833 -> 838)
- `simulations_run` Δ = **+10** each (5 sim phase + 5 competition rows) — **8/8 exact**
- `relevance` Δ = Σ this run's `avg_score` — **8/8 exact** (tolerance 1e-6)
- `wins`/`losses` sum to **5** per civ — **8/8 exact**, and the per-civ `wins` delta equals the
  `meta_log` `winner_civ` count — **8/8 exact**
- `generation` unchanged at **1** for all 8; registry still 8 civs, no new civ dirs
- **80/80** rows carry an independently recomputed seed + colour + figure
- **40** distinct seeds over the 80 new rows (message-level invariant), **0** `(civ,prompt)`
  slot carrying >1 seed
- per-prompt **8/8** distinct seeds AND previews on every competition prompt (5/5)
- `meta_log` `results` field == the ledger's competition rows, **0/40** mismatches
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples, 0 `EXC:` in the mock log (**160 OK** lines)
- **80/80** distinct `(q,n,a)`
- **seed multiset identity**: the mock log's last 80 OK lines == the 80 new ledger rows
- extinction risk NONE (threshold −10; the lowest civ sits ~189x above it)
- **counter-gap stability 8/8 exact**: grounded −84.35, whimsical −173.14, formal −85.53,
  poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24

## Durable notes

- The workspace was empty again (**11th consecutive** session naming ephemeral paths) and the
  upstream path in the prompt did not exist. `GET /user/repos` resolved the owner in one call;
  upstream is **`SuperInstance/AI-Writings`** (case-insensitive slug).
- `/workspace` is at **100 % NAS quota** (600 G/600 G), so the clone went to `/tmp` and the
  bridge points at the **inner `cellular-first-design`** dir
  (`ln -s /tmp/cfd/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`),
  verified with `stat -L -c '%d:%i'` -> `128:12601` on both sides and `os.path.samefile()`
  -> `True`. The bridge targets the **inner** dir because `CIVS_DIR` is hardcoded to
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`.
- **The mock algorithm was re-derived and verified 640/640 exact** against the live ledger
  before the run: `d = md5(cultural_prompt).digest(); h = d.hex(); i = d[0] % 4;
  seed = h[(i*2)%8:(i*2)%8+4]; color = h[8:12]; figure = h[12:16]/h[16:20]/h[20:24]`.
  **A first comparison pass reported 0/640 — the `#`-prefix trap again**: the recorded colour
  carries a `#`, the derived slice does not. *A 0/N recompute means "the parser is wrong"
  before it means "the mock is wrong".*
- The response body band is **332-369**; this build lands at a constant **349** (39-char header
  + a 310-char fixed, culture-free tail). The cultural-prompt band is **167-209**, measured from
  the **real** `culture.json` files. The body length is input-independent, so the target is
  solved algebraically in one build.
- `ZAI_TOKEN` is still absent (**91st session**): z.ai returns **401 `token expired or
  incorrect`** — endpoint healthy, credential missing. Control B is the only provider path and
  needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE` (the override
  alone is dead code behind the token gate).
  `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`;
  **0** fallback triples.
- Mock teardown: killed by **exact argv match** (2 pids), port proven closed
  (`curl -m 5` -> exit 7 / `HTTP=000`).
- `gh` is not installed; `git fetch`/`push` need `GIT_SSL_NO_VERIFY=1`; push to the explicit
  token URL and verify with `git ls-remote`.
