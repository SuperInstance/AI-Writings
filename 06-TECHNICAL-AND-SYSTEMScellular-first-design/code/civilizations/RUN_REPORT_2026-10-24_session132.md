# Civ Orchestrator — RUN_REPORT session 132 (2026-10-24)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

Upstream `SuperInstance/AI-Writings` @ `b1b02c3` (session 131 baseline), sparse clone to `/tmp`,
symlink bridge at `/workspace/repos/ai-writings/cellular-first-design` (inode `129:10434`, `-ef` OK).
Control B mock provider on `127.0.0.1:8799` (ZAI_TOKEN + ZAI_URL_OVERRIDE both set).

## Verification — all checks passed

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` Δ | +5 | 393 → 398 | PASS |
| `Winner:` lines | 5 | 5 | PASS |
| total new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with JEV `error` key | 0 | 0 | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |
| competition prompts at 8/8 distinct seeds | 5/5 | 5/5 | PASS |
| mock tracebacks in `/tmp/mock_zai.log` | 0 | 0 | PASS |

Per-civ ledger deltas: civ-engineer 756→766, civ-formal 787→797, civ-grounded 802→812, civ-mythic 759→769, civ-poetic 781→791, civ-precise 751→761, civ-therapist 754→764, civ-whimsical 814→824.

## Pre-flight (before the run, per the session-118/131 rule)

`/tmp` was wiped this session, so the mock was rebuilt from scratch and **both** historical
mock bugs had to be re-applied on rebuild:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — a plain `seed[i*2:i*2+2]` is empty for `i>=4`,
  raises `ValueError`, and the bridge answers HTTP 500 **while the socket stays open** (a 200
  probe on a one-word body looks healthy and misses it).
- session-118 md5-of-whole-message seeding — seeding from the first 8 alnum chars of the message
  yields `youareav` for all 8 civs (the cultural prompt opens with the civ-invariant
  `You are a voice in the tradition of "…"`), making all 8 candidates byte-identical and voiding
  every competition result.

Pre-flight probe against the **live** mock with the exact long cultural prompt:
8/8 distinct seeds, 8/8 distinct previews, HTTP 200, 1174–1574-char bodies,
`[mock-zai seed=…]` prefix present, **0 tracebacks**.

## Low-relevance civilization — `civ-grounded` (The Grounded)

**`civ-grounded` is the low-relevance civ — 35 consecutive sessions (95–132).** Last on lifetime
`avg_score`, `quality`, `alignment`, `relevance` and `relevance_per_sim`.

| dimension | civ-grounded | next best | gap |
|---|---|---|---|
| lifetime `alignment` | 1.3865 | 2.3553 | **0.9687** |
| lifetime `quality` | 0.5637 | 0.9656 | 0.4019 |
| lifetime `avg_score` | 1.1660 | 1.7519 | 0.5859 |

**The structural gap is `alignment`: 0.9687 below the field, versus 0.4019 on quality — 2.4× wider.**
Alignment is the dimension the meta-GAN *selects* on, so Grounded fails to *embody a distinctive
voice* — a **voice** failure, not a prose failure. Its tenets ("concrete images, everyday language,
specific examples, no abstractions") and voice ("warm, factual") are the least differentiating
prompt in the field.

### Run-level note: `civ-therapist` took the run low this session

| civ | run `avg_score` | run `alignment` | lifetime `avg_score` | lifetime `alignment` |
|---|---|---|---|---|
| civ-precise | 0.3683 | 0.7470 | 1.5193 | 2.3553 |
| civ-poetic | 0.3620 | 0.7030 | 1.7519 | 2.3025 |
| civ-whimsical | 0.3400 | 0.5020 | 1.6244 | 2.0286 |
| civ-mythic | 0.2600 | 0.4480 | 1.4727 | 1.8565 |
| civ-engineer | 0.1657 | 0.1420 | 1.3284 | 1.8623 |
| civ-formal | 0.1550 | 0.0850 | 1.3311 | 1.9875 |
| civ-grounded | 0.1290 | 0.0770 | 1.1660 | 1.3865 |
| civ-therapist | 0.1117 | 0.0240 | 1.3942 | 1.7119 |

`civ-therapist` was **last** on this run's `avg_score` (0.1117) and `alignment` (0.0240), and
2nd-lowest on lifetime `alignment` (1.7119). It is 8th of 8 on **both** the run score and the run
alignment, and its run/lifetime alignment ratio (0.014) is the field's worst. But its lifetime
`avg_score` is 5th of 8 (1.3942) — a mid-field citizen, not a structural loser. This is a
**per-run low**, and the session-121/122/123 lesson applies: *do not promote a single-run low to a
finding without a lifetime-level gap.* `civ-therapist` stays a **watch axis**, distinct from
`civ-grounded`'s structural finding.

**Run-level `avg_score` and `alignment` rankings are identical (Spearman ρ = +1.000)** across all 8
civs; at the lifetime level ρ = +0.738. The run's score dimensions moved together.

## The chooser: `civ-precise` swept 5/5, and it was *not* the argmax

| prompt | ranked (avg_score desc) | winner | winner's rank |
|---|---|---|---|
| 0 | poetic=0.59, whimsical=0.44, mythic=0.34, precise=0.27, engineer=0.22, formal=0.19, therapist=0.14, grounded=0.13 | **civ-precise** | 4/8 |
| 1 | poetic=0.46, mythic=0.33, precise=0.27, whimsical=0.19, engineer=0.17, therapist=0.14, formal=0.14, grounded=0.10 | **civ-precise** | 3/8 |
| 2 | precise=0.78, mythic=0.56, poetic=0.21, engineer=0.19, formal=0.12, whimsical=0.10, grounded=0.07, therapist=0.06 | **civ-precise** | 1/8 |
| 3 | whimsical=0.52, precise=0.33, poetic=0.30, mythic=0.18, engineer=0.16, formal=0.14, grounded=0.14, therapist=0.09 | **civ-precise** | 2/8 |
| 4 | precise=0.38, whimsical=0.34, poetic=0.33, grounded=0.24, formal=0.20, engineer=0.16, therapist=0.13, mythic=0.05 | **civ-precise** | 1/8 |

**Chooser vs `avg_score` argmax: 2/5 (40 %).** Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120)
→ 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128)
→ 4/5 (130) → **2/5 (132)**. Fourteen five-sample points cannot narrow a rate; the honest claim is
*somewhere in 0–80 %*.

**The stable direction holds: in all 3 disagreements this session the chooser picked a
*lower*-scoring candidate** — the same direction as 116/118/119/120/122/123/125/131 (11th consecutive
session with that direction). `civ-precise` won 5/5 while ranking **4th** (0.273 vs poetic 0.587)
on prompt 0 and **3rd** (0.267 vs poetic 0.463) on prompt 1. The chooser reads the *text* through JEV;
it does not read `avg_score`.

Note the counter-intuitive pairing: `civ-precise` is **3rd of 8 on lifetime `avg_score`** (1.5193)
but **1st of 8 on lifetime `alignment`** (2.3553) and **1st of 8 on this run's `avg_score`**
(0.3683). The chooser tracks *alignment*, and `civ-precise` wins on exactly that axis.

## The two stable inverses (re-confirmed)

- **`civ-poetic`** = 1st on lifetime `avg_score` (1.7519) / `quality` (0.9656) / `novelty` (1.9876) /
  `alignment` (2.3025), but **last on `win_rate`** (0.013, 5/368) and won **0/5** this session
  despite argmaxing 3/5. A **selection** failure, not a quality collapse.
- **`civ-precise`** = best `win_rate` (0.546, 201/167), won **5/5**, 1st on lifetime `alignment`
  (2.3553) but only 3rd on lifetime `avg_score` (1.5193). The mirror inverse.

**Never treat `win_rate` as a quality metric** — it is a *selection* metric.

## Axis-specific lows (distinct axes, not one loser)

- `civ-grounded` = the low-`alignment` / low-`avg_score` civ (structural, 35 sessions).
- `civ-formal` = the low-**novelty** axis (lifetime novelty 1.4121, last; alignment 1.9875 healthy).
- `civ-therapist` = this session's run-level low (watch axis).
- `civ-engineer` = 5th of 8 on run `avg_score` (0.1657) but 5th of 8 on lifetime `avg_score`
  (1.3284) — no lifetime-level gap. The session-121/122/123 single-run low has now appeared in
  3 of the last 5 sessions, but still without a lifetime gap. **Do not promote it.**

## Extinction risk: NONE

Threshold −10; lowest raw relevance `civ-grounded` **+862.47** (**86.2× above the floor**). Registry 8 civs, `max_civs` 12, all 8 still
`generation=1` — birth/extinction only runs under `--loop`.

## Counter gap (unchanged)

| civ | ledger rows | registry `simulations_run` | gap |
|---|---|---|---|
| civ-engineer | 766 | 744 | +22 |
| civ-formal | 797 | 755 | +42 |
| civ-grounded | 812 | 769 | +43 |
| civ-mythic | 769 | 749 | +20 |
| civ-poetic | 791 | 754 | +37 |
| civ-precise | 761 | 745 | +16 |
| civ-therapist | 764 | 747 | +17 |
| civ-whimsical | 824 | 761 | +63 |
| **total** | | | **+260** |

`save_state()` rewrites `culture.json` with no lock ⇒ `relevance_per_sim` is **not recomputable
from the ledger** by an auditor. The gap is per-civ uneven (+16..+63), not a uniform offset.

## Score-dimension spreads (cross-civ, not absolute levels)

`alignment` **0.7230** > `avg_score` 0.2567 ≈ `novelty` 0.2050 > `quality` **0.0090**.
`alignment` again carried the widest spread and is again the axis the chooser selects on.
`quality` collapsed again (0.007–0.016) — the 119/121/122/123/125/126/130/131 regime, against
session-120's 0.340 and session-127's 1.063. **The quality collapse is a LEVEL that moves, not a
stable property** — compare cross-civ spreads, not absolute levels, before ranking on a dimension.

Absolute run levels are depressed vs lifetime (run `avg_score` 0.112–0.368 vs lifetime 1.17–1.75) —
a level shift in the JEV scorer's output for this batch, **not a civ effect**; the cross-civ
*ordering* carries the information.

## Re-confirmations

- **NAS EDQUOT is total (18th session).** No write to `/workspace` succeeds — even a 5-byte
  `echo` yields a 0-byte file that `ls` still lists, and `cp` into `/workspace` exits 1 with
  `Disk quota exceeded` on every file. `mkdir` and `ln` work ⇒ the **symlink bridge** is the only
  way in. Verified by inode identity (`stat -L -c '%d:%i'` = `129:10434` on both sides, `-ef` OK).
- **`gh` is not installed (18th session).** `GET /user/repos?per_page=100` + `GET /search/repositories`
  with `GITHUB_TOKEN` locate upstream. The `ai-writings/cellular-first-design` slug 404s;
  **`SuperInstance/AI-Writings`** resolves (3.7 GB; the API is case-insensitive).
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the script reads the former.
  Unset ⇒ JEV silently degrades to the 2.0 default and every score becomes a constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — the token gate returns `None` first. Control B needs
  **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **Tool timeout 30 s < run ~45 s.** Launch detached with stdout redirected to a file, then poll
  `ps` + the log. The launch call itself returns; the child inherits stdout, so redirect it.
- **`ps | grep <script>` self-matches the launching shell.** Use `ps -eo pid,args | awk '/mock_zai/ && !/awk/'`
  and match the exact args (`python3 /tmp/mock_zai.py`); the `timeout` wrapper is a separate pid —
  kill both.
- **`civilizations.json` is multi-line pretty-printed JSON, not JSONL** — use `json.loads(read())`.
- **Never flatten the clone.** The symlink target is the **nested** `cellular-first-design` dir;
  flattening makes `git status` show every file deleted and points `CIVS_DIR` one level too deep.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs**, not a dict — a dict-shaped
  reader silently yields 0 % agreement and empty pick tallies.
- **The `ls` race did not reproduce** — the bridge passed 5/5 on the first attempt.

## Files changed

`civ-*/simulations.jsonl` (+10 rows each), `meta_log.jsonl` (+5), `leaderboard.json` (rewritten),
`civ-*/culture.json` (relevance/wins/losses counters).
