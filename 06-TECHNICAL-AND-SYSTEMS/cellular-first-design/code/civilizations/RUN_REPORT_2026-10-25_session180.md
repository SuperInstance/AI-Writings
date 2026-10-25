# Civ Orchestrator — Run Report, Session 180

**Date:** 2026-10-25T06:24Z
**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline:** HEAD `f59288ee` (session 179) — clean tree
**Provider path:** Control B (local mock z.ai on 127.0.0.1:8899), `ZAI_URL_OVERRIDE` + placeholder `ZAI_TOKEN`
**JEV:** live (`jev-1.14.0`, HTTP 200), `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`
**Result:** **18/18 verification assertions PASS**

## Environment

Workspace arrived empty (a wipe; 109th). The prompt's path did not exist — the
`ai-writings/cellular-first-design` slug 404s on the GitHub API (the API is
case-insensitive and the real upstream is `SuperInstance/AI-Writings`, where
`cellular-first-design` is a **subdirectory**). Recovery: sparse clone
(`--filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design`)
into `/tmp` ⇒ 14 MB working tree.

`/workspace` NAS is at **100 % quota** (600 G/600 G) while visibly empty: a `cp -a`
leaves a tree of **0-byte files that `ls` still lists** (the EDQUOT trap, 18th
session). The **symlink bridge** is the only way in — `/workspace/repos/ai-writings/
cellular-first-design` → `/tmp/aiw/cellular-first-design`. Verified with
`os.path.samefile()` ⇒ **True**, dev:ino **129:10436** on both sides. The bridge
must satisfy BOTH the requested path and the script's hardcoded `CIVS_DIR`.

`ZAI_TOKEN` is absent from the environment and from all 8 sandbox secrets; z.ai
returns **401 `token expired or incorrect`** (endpoint healthy, credential absent)
— **59th consecutive session**. `ZAI_URL_OVERRIDE` alone is dead code (the token
gate returns `None` first), so a placeholder token was supplied.

## NEW — the 2-char seed slice is a structural certainty, not bad luck

The runbook's "fully specified" algorithm block still shows the **2-hex-char**
slice `h[(i*2)%8:(i*2)%8+2]`, while its own headline says to widen it to 4.
Widening to `h[(i*2)%8:(i*2)%8+4]` (65 536 seeds) was applied and the padding
became a no-op. The pre-flight gate then passed **8/8 on the FIRST build** with
**40/40 distinct seeds** — the failure mode session 179 hit (39/40) is
**structurally guaranteed** by the 2-char slice over 40 slots, not a hash
accident.

*Rule: a seed padded to a documented width is not that width's worth of
entropy — check the SLICE, not the render.*

### Pre-flight gate — 8/8 PASS

| Check | Result |
|---|---|
| distinct seeds | 40/40 |
| distinct previews | 40/40 |
| md5 recompute mismatches | 0/40 |
| per-prompt 8/8 distinct seeds AND previews | 5/5 prompts |
| `(civ,prompt)` pairs with >1 seed | 0 |
| repeat-same-message determinism | 0/16 unstable |
| seed widths | all 4 hex chars |
| literal `seed={}` | 0 |

## Run-wide verification — 18/18 PASS

- per-civ ledger delta **+10 × 8 = 80** new rows (5 sims + 5 competition rows each)
- `meta_log.jsonl` delta **+5** (633 → 638); `Winner:` lines = **5**
- wins/losses exact **8/8** (`dW+dL == 5`): precise **+5/+0**, all others **+0/+5**
- `relevance` delta == Σ(this run's `avg_score`) **8/8 exact** (max abs diff **4.55e-13**)
- leaderboard `sims_run` == `culture.json` `simulations_run` **+10** each, **8/8**
- distinct seeds **40/80 rows**; **0** `(civ,prompt)` carrying >1 seed
- **80/80** rows carry the `[mock-zai seed=…]` prefix; **80/80** `provider=zai`
- **0** JEV `error` rows; **0** `2.0/2.0/2.0` fallback triples
- **80/80** distinct `(quality, novelty, alignment)` triples
- registry 8 all gen 1, no births, no extinctions
- extinction risk **NONE** (threshold −10; lowest +1228.70 = **123×** the floor)

### Three verifier FAILs were MY bugs, not data defects

The first verification pass reported 3 FAILs. All three were **defects in the
check, not in the run**, and each is worth recording because the wrong
"fix" would have meant corrupting good data:

1. **relevance delta** — compared the leaderboard's **2-dp rounded** relevance
   against an **unrounded** ledger sum ⇒ a spurious ~3.3e-03 residual. The
   authoritative source is `culture.json` (`relevance_score`, unrounded);
   re-checked against `git show HEAD:…` ⇒ exact 8/8 (max **4.55e-13**).
2. **leaderboard `sims_run`** — compared against the **ledger line count**
   (which includes competition rows) instead of the **sim counter**
   `simulations_run`. The two are different numbers by exactly 5 per civ.
3. **counter gap** — same rounding trap as (1).

*Rule: when a verifier disagrees with a run, suspect the verifier first. Compare
against `git show HEAD:` (the pristine pre-run value), never against a value you
typed by hand from a 2-dp rendering.*

## Leaderboard (post-run, lifetime)

| # | civ | relevance | rel/sim | wins | losses | win_rate | avg_sc | align | qual | novel |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1892.70 | 1.534 | 6 | 607 | 0.010 | 1.5653 | 2.0515 | 0.7424 | 1.9020 |
| 2 | civ-precise | 1741.27 | 1.421 | 376 | 232 | 0.618 | 1.4294 | 2.1382 | 0.5231 | 1.6269 |
| 3 | civ-whimsical | 1648.90 | 1.329 | 5 | 608 | 0.008 | 1.3973 | 1.6538 | 0.5757 | 1.9623 |
| 4 | civ-mythic | 1520.37 | 1.237 | 10 | 597 | 0.016 | 1.2582 | 1.4950 | 0.5212 | 1.7584 |
| 5 | civ-formal | 1460.39 | 1.182 | 94 | 517 | 0.154 | 1.2106 | 1.6875 | 0.4527 | 1.4916 |
| 6 | civ-engineer | 1394.77 | 1.140 | 47 | 559 | 0.078 | 1.1549 | 1.4678 | 0.4455 | 1.5514 |
| 7 | civ-therapist | 1382.60 | 1.127 | 11 | 599 | 0.018 | 1.1453 | 1.2072 | 0.4453 | 1.7833 |
| 8 | civ-grounded | 1228.70 | 0.984 | 70 | 542 | 0.115 | 1.0163 | 1.0714 | 0.4023 | 1.5752 |

## THIS RUN (80 rows)

| # | civ | run_avg | align | qual | novel | d_rel |
|---|---|---|---|---|---|---|
| 1 | civ-precise | 1.7273 | 2.3810 | 0.4370 | 2.3640 | 17.2733 |
| 2 | civ-poetic | 1.6287 | 1.9540 | 0.4060 | 2.5260 | 16.2867 |
| 3 | civ-whimsical | 1.5623 | 1.8370 | 0.3240 | 2.5260 | 15.6233 |
| 4 | civ-formal | 1.4517 | 1.7550 | 0.1470 | 2.4530 | 14.5167 |
| 5 | civ-engineer | 1.3433 | 1.3090 | 0.3370 | 2.3840 | 13.4333 |
| 6 | civ-grounded | 1.3207 | 1.3300 | 0.1450 | 2.4870 | 13.2067 |
| 7 | civ-mythic | 1.0533 | 0.5800 | 0.1520 | 2.4280 | 10.5333 |
| 8 | civ-therapist | 0.9903 | 0.3910 | 0.1020 | 2.4780 | 9.9033 |

Run spreads: `avg_score` 0.7370, `alignment` **1.9900** (widest axis again),
quality 0.3350, novelty 0.1620. **Alignment** carried the widest spread and is
again the axis the chooser selects on.

## Low-relevance civilizations

**Lifetime low: `civ-grounded` — 54th consecutive session.** Last of 8 on
lifetime `relevance` **1228.70**, `relevance_per_sim` **0.984**, `avg_score`
**1.0163**, `alignment` **1.0714**, `quality` **0.4023**. The binding constraint
is still **alignment**: gap to the next civ **0.1358** vs quality's gap
**0.0430** = **3.16×** wider. Alignment is the dimension the meta-GAN selects
on, so this is a **voice** failure, not a prose failure. Lifetime novelty 1.5752
is 3rd of 8 (above the 1.6922 median) — Grounded is neither boring nor
unmistakable; it is simply not rewarded.

**Run-level low: `civ-therapist`** (run `avg_score` **0.9903**, `alignment`
**0.3910**, `quality` **0.1020**) — the run low rotated to a **fourth** civ in
four sessions. Its lifetime standing is 7th of 8 on `relevance` and 7th of 8 on
`avg_score`, so this is a **watch axis, not the finding** (session-132 rule).
The run-level low rotating across civs is itself the signal: the *axis*
(alignment) is stable, the *holder* is not.

**`civ-mythic`** took the run-level alignment low among the mid-pack (0.5800,
avg 1.0533) and sits 4th of 8 on lifetime `relevance`; lifetime `avg_score`
1.2582 (5th of 8). Watch axis.

## Chooser vs `avg_score` argmax: 1/5 (20 %)

`civ-precise` swept **5/5** competitions (5 wins, 0 losses); every other civ went
0-5. The chooser is **not** a pure argmax and this reproduces the standing
pattern from the clean-mock series. **Never treat `win_rate` as a quality
metric** — it is a *selection* metric.

## Counter gap

Per-civ gap (`culture.json` `relevance_score` − ledger Σ`avg_score`): **fixed and
not accumulating** — delta exactly **0.000000** for all 8 civs vs the pre-run
baseline, and the total is **−609.9200**, byte-identical to session 179.

## Teardown

Mock killed by exact-argv match. Port proven closed. No `pkill -f` (self-match
hazard). Bridge symlink left in place for the next session.
