# Civ Orchestrator — Run Report 2026-10-24 (session 116)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

**Result:** ✅ Completed — 5 competitions, 80 simulations, 5 meta_log rows, all 8 ledgers +10.

**Provider path:** Control B (local mock bridge) — the `ZAI_TOKEN` credential gap is unchanged.

## 1. Preconditions

| Check | Result |
|---|---|
| z.ai endpoint health | HTTP 401 `token expired or incorrect` on a bogus-token probe ⇒ **endpoint healthy, credential gap** |
| `ZAI_TOKEN` in env | UNSET |
| `ZAI_TOKEN` in the 8 sandbox secrets | absent (MOTHQUANTUM, TYPESAFE_AI, MINIMAX, NOTION, NPMJS, CRATES, PYPI, GITHUB) |
| JEV liveness | HTTP 422 `model_attributes_type` / `dict_type` ⇒ auth OK, payload shape error only ⇒ **JEV live** |
| Mock bridge | `/tmp/mock_zai.py` on `127.0.0.1:8799`, index-wrapped seed `seed[(i*2)%8:…+2]` |
| Mock long-content probe | HTTP 200, 284-char body, `[mock-zai]` prefix present, **0 tracebacks** |
| Workspace bridge | `ln -sfn` to the **nested** `cellular-first-design` dir; inode identity `129:10423` both sides, `-ef` OK |

## 2. Ledger deltas (asserted on rows, not exit code)

| Civ | Pre | Post | Δ | mock prefix | provider=zai | JEV error |
|---|---|---|---|---|---|---|
| civ-engineer | 596 | 606 | **+10** | 10/10 ✅ | 10/10 ✅ | none |
| civ-formal | 627 | 637 | **+10** | 10/10 ✅ | 10/10 ✅ | none |
| civ-grounded | 642 | 652 | **+10** | 10/10 ✅ | 10/10 ✅ | none |
| civ-mythic | 599 | 609 | **+10** | 10/10 ✅ | 10/10 ✅ | none |
| civ-poetic | 621 | 631 | **+10** | 10/10 ✅ | 10/10 ✅ | none |
| civ-precise | 591 | 601 | **+10** | 10/10 ✅ | 10/10 ✅ | none |
| civ-therapist | 594 | 604 | **+10** | 10/10 ✅ | 10/10 ✅ | none |
| civ-whimsical | 654 | 664 | **+10** | 10/10 ✅ | 10/10 ✅ | none |

- `meta_log.jsonl` 313 → 318 (**+5**), each `results` a **list of 8** `[civ_id, score]` pairs.
- `Winner:` lines in run output = **5** (civ-precise ×3, civ-grounded, civ-mythic).
- Total new rows **80/80** carry the `[mock-zai]` prefix ⇒ auditable as mock-sourced.
- No JEV `error` key on any of the 80 new rows ⇒ scoring was real, not the 2.0 default.

## 3. LOW RELEVANCE — `civ-grounded` (The Grounded) — 15th consecutive session

`civ-grounded` is **last on lifetime `relevance` (793.86)**, on **`relevance_per_sim` (1.304)**, on
**lifetime `quality` (0.685)**, on **lifetime `alignment` (1.654)**, and on **lifetime `avg_score` (1.347)**
— last of 8 on all five. It is also last on this run's own `avg_score` (0.064).

| Metric | civ-grounded | Best | Rank |
|---|---|---|---|
| lifetime relevance | 793.86 | 1158.90 (civ-poetic) | **8/8 last** |
| relevance_per_sim | 1.304 | 1.951 (civ-poetic) | **8/8 last** |
| lifetime quality | 0.685 | 1.161 (civ-poetic) | **8/8 last** |
| lifetime alignment | 1.654 | 2.618 (civ-precise) | **8/8 last** |
| lifetime avg_score | 1.347 | 1.770 (civ-poetic) | **8/8 last** |
| this-run avg_score | 0.064 | 0.320 (civ-precise) | **8/8 last** |

Alignment is the dimension the meta-GAN *selects* on, so last-on-alignment + last-on-relevance is
**structural, not noise**. This is the 15th consecutive session reproducing it (95–116).

### Distinct-axis carve-outs (the other axes of low performance)

- **`civ-formal`** — lowest lifetime `novelty` (1.512).
- **`civ-precise`** — highest `win_rate` (0.483) but 4th on `relevance_per_sim`; a *selection* win, not a quality win.
- **`civ-poetic`** — the stable inverse: 1st on `relevance_per_sim` (1.951) and 1st on lifetime quality
  (1.161), but `win_rate` 0.017. A *selection* failure, not a quality collapse.

## 4. Full leaderboard (post-run)

| # | Civ | Relevance | Sims | Rel/sim | Wins | Losses | Win rate |
|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1158.90 | 594 | 1.951 | 5 | 288 | 0.017 |
| 2 | civ-whimsical | 1064.00 | 601 | 1.770 | 4 | 289 | 0.014 |
| 3 | civ-mythic | 992.94 | 589 | 1.686 | 6 | 281 | 0.021 |
| 4 | civ-precise | 979.51 | 585 | 1.674 | 139 | 149 | 0.483 |
| 5 | civ-therapist | 950.35 | 587 | 1.619 | 6 | 284 | 0.021 |
| 6 | civ-engineer | 891.47 | 584 | 1.526 | 29 | 257 | 0.101 |
| 7 | civ-formal | 886.54 | 595 | 1.490 | 51 | 240 | 0.175 |
| 8 | civ-grounded | 793.86 | 609 | 1.304 | 59 | 233 | 0.202 |

## 5. This run's competition results

| # | Prompt | Winner | Winner's score | Top score | argmax agreed? |
|---|---|---|---|---|---|
| 1 | what a cell is | **The Precise** (civ-precise) | 0.347 | 0.347 | ✅ |
| 2 | the bookkeeper's role | **The Precise** (civ-precise) | 0.210 | 0.437 (civ-poetic) | ❌ |
| 3 | the witness log | **The Grounded** (civ-grounded) | 0.040 | 0.533 (civ-precise) | ❌ |
| 4 | ternary values | **The Precise** (civ-precise) | 0.283 | 0.283 | ✅ |
| 5 | JEV as a decision oracle | **The Mythic** (civ-mythic) | 0.223 | 0.317 (civ-whimsical) | ❌ |

**Chooser vs `avg_score` argmax = 2/5 (40%)** — consistent with the ~15 % historical rate.

**Notable:** in competition 3, `civ-grounded` won with the **lowest** score in the field (0.040 vs a
0.533 top). The chooser is judging the mock's text, not the numeric score, so a low-scoring civ can
still win. This is a direct illustration of why `win_rate` is unsafe as a standalone quality proxy.

## 6. Structural findings (unchanged)

- **Counter gap:** ledger rows exceed registry `simulations_run` by **+260** in total
  (5004 ledger rows vs 4744 registry sims). `save_state()` rewrites `culture.json` with no lock ⇒
  `relevance_per_sim` is **not recomputable from the ledger** by an auditor.
- **Extinction risk: NONE** (threshold −10; lowest raw relevance ≈ +794). Registry 8 civs,
  `max_civs` 12. Extinction/birth only runs under `--loop`.

## 7. Method notes (session 116)

- **The NAS EDQUOT trap is still total.** `/workspace` is 600 G/600 G, 0 bytes free. A direct
  `git clone` into `/workspace/repos/...` fails with `Disk quota exceeded`; `cp` into the NAS
  silently truncates files to 0 bytes. The **symlink bridge is the only way in**, and the target
  must be the **nested** `cellular-first-design` dir (not the clone root, not a flattened tree).
- **A plain `git clone --filter=blob:none` of `SuperInstance/AI-Writings` into `/tmp` succeeded and
  checked out the whole tree**; the civ subtree is small, so the simple clone needs no
  `sparse-checkout` dance.
- **`/tmp` is not subject to the NAS quota** (overlay, ~28 G free) — confirmed again this session.
- **`gh` is not installed** (3rd session running); `GET /user/repos` + the search API with
  `GITHUB_TOKEN` locate the upstream. `SuperInstance/ai-writings` resolves; the 3.7 GB upstream is
  `SuperInstance/AI-Writings` (case-insensitive on the API).
- **Tool timeout is 30 s**, shorter than the ~45 s run. Launch detached, redirect stdout to a file,
  and poll with `ps` + the log — do not expect the launch call to block.
