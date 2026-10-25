# Session 153 — clean mock #23; chooser-vs-argmax 5/5 (100 %); Grounded holds the low for the 49th session (2026-10-25)

**Run:** 8 civs x 5 sims + 5 competition prompts, `--sims 5 --prompts 5 --providers zai`,
Control B mock provider bridge, JEV live. Upstream baseline `386f103` (session 152).

**All 54 verification checks PASS.** Per-civ ledger delta **+10** x 8 = **80 rows**
(5 sim-phase + 5 competition-phase per civ), `meta_log.jsonl` **498 -> 503** (+5),
`Winner:` lines **5**, **0** JEV `error` keys, **0** rows with the 2.0/2.0/2.0 fallback
triple, **80/80** rows carry the `[mock-zai` prefix with `provider=zai`, **40/40** distinct
seeds, **0** `(civ,prompt)` combos with >1 seed, sim->competition ts gap at index 4 in
**8/8** civs (1.20 s - 23.02 s), **8/8 distinct previews on all 5 competition prompts**,
`leaderboard.json` rewritten at 01:12:47Z, `git status --porcelain` = **18** modified
(8 ledgers + 8 cultures + `meta_log.jsonl` + `leaderboard.json`).

**JEV liveness proved at the score level, not just the socket level:** the 80 new rows carry
**80 distinct `(quality, novelty, alignment)` triples** (quality 0.01-0.58, novelty
0.78-1.93, alignment 0.10-2.24) and confidences **0.53-1.00**. A silent 2.0 default would
produce one repeated triple and constant 0.5 confidence.

**Mock rebuilt from scratch** (`/tmp` was wiped) => the known mock bugs were live again in
the naive rebuild: the session-112 index wrap (`seed[i*2:i*2+2]` -> empty for `i>=4` ->
HTTP 500 with the socket still open), the session-118 md5-of-whole-message seeding, and
the session-145 literal-`{}` placeholder (every row carrying `seed={}` -> 1 distinct seed).
The session-144 `Connection: close` was re-applied too. Pre-flight: **40/40 distinct seeds,
40/40 distinct previews, 40/40 distinct template md5s, 8/8 seeds AND 8/8 previews on all
5 prompts, 0 tracebacks**, cultural prompt lengths 167-209. **The 23rd clean mock
measurement.**

**Chooser vs `avg_score` argmax: 5/5 (100 %).** `civ-precise` swept **all 5** prompts and
was argmax in all 5. This is the **joint-highest** of the clean-mock series and the first
**perfect** agreement since the fix (s.118). Clean-mock series: 0,3,1,4,4,3,0,4,4,1,2,4,4,
0,2,4,1,4,0,**5** (s.118-153) - 23 five-sample points cannot pin a rate; the honest claim
is *somewhere in 0-100 %*. The historical "chooser vs argmax ~15 %" figure was measured
under the **degenerate** mock (session 117) and is **void**; session 118's clean value of
0/5 was the first clean measurement and it has never been repeated.

**IMPORTANT — this run provides NO disagreement sample, so the standing "the chooser takes
the LOWER-scoring candidate" finding is NOT re-confirmed here.** The 5 disagreements in
previous clean sessions all had a **negative** delta (winner below argmax). With 0
disagreements, this run is **silent** on that direction. Do not read "5/5 agreement" as
refuting the low-scoring-pick finding, and do not read it as supporting it.

**`civ-grounded` (The Grounded) remains the low-relevance civ - 49 consecutive sessions
(95-153).** Last of 8 on every lifetime axis: `relevance` 970.72, `relevance_per_sim`
0.992, `avg_score` 1.0324, `alignment` 1.1621, `quality` 0.4572. The label did **not**
rotate: last before the run (965.00 / 0.996) and last after it (970.72 / 0.992).
Alignment is the dimension the meta-GAN *selects* on, so Grounded fails to *embody a
distinctive voice* - a **voice** failure, not a prose failure. The absolute gaps to the
next-lowest civ: **alignment 0.2340** (vs `civ-therapist` 1.3962) versus **quality 0.0338**
(vs `civ-formal` 0.4909) - the alignment gap is ~7x the quality gap. **Quote the absolute
gaps and the "last of 8 on both" invariant, never the ratio** (the ratio has swung 11x ->
0.4x on identical data-shape logic across sessions).

**`civ-formal` is the low-novelty axis** - lifetime novelty **1.3750** (last of 8),
alignment 1.7474 healthy. `civ-grounded` is **above median** on lifetime novelty
(1.4778, 6th of 8): Grounded is not boring, it is *unmistakable in a way the chooser does
not reward*.

**The two stable inverses hold.** `civ-poetic` = 1st on lifetime `avg_score` (1.5936) /
`quality` (0.8074) / `relevance_per_sim` (1.554) but **last on `win_rate` (0.013)** and won
**0/5** despite being 2nd on run `avg_score` - the stable selection-failure inverse.
`civ-precise` = best `win_rate` (0.573, 271/202), **highest lifetime `alignment` (2.1791)**,
1st on run `avg_score` (1.2120) at `preferred_temp` **0.2** - the mirror inverse, and the
coldest voice is what the chooser rewards. `civ-whimsical` is 2nd on lifetime `avg_score`
(1.4566) and last on `win_rate` (0.010).

**Watch-axis `civ-therapist` - 3rd session at the run bottom on `alignment`** (0.2220,
below `civ-grounded`'s 0.3590). Still mid-field on the lifetime axis (`avg_score` 1.2090,
5th of 8) => **watch axis, not a finding**. It becomes one only if the lifetime axis moves
too. `civ-grounded` was 7th of 8 on run `avg_score` (0.5720) - the run-level low
(`civ-therapist`, 0.5393) and the lifetime low (`civ-grounded`) are **different civs on
different axes**, which is the rule (session 132), not a contradiction.

- **Extinction risk NONE** - threshold -10; lowest relevance +970.72 (97x above the floor).
  Registry 8 civs, `max_civs` 12. All 8 civs still `generation=1`; birth/extinction only
  under `--loop`.
- **Counter gap is a FIXED per-civ offset, byte-identical to sessions 147/148/149/150** -
  whimsical +63, grounded +43, formal +42, poetic +37, engineer +22, mythic +20,
  therapist +17, precise +16, **TOTAL +260**. So it is a per-civ constant, not an
  accumulating leak. `save_state()` has no lock => `relevance_per_sim` is **not
  recomputable from the ledger** by an auditor.
- **Dimension-spread discipline (6th consecutive observation):** this run's cross-civ
  spreads were `alignment` **1.6340**, `avg_score` 0.6727, `novelty` 0.5950, `quality`
  **0.1460**. `quality` collapsed again to a 0.055-0.201 band (18 of the last 19
  clean-mock sessions) and `alignment` again carried the widest spread **and** is again
  the axis the chooser selects on. **The quality collapse is a LEVEL that moves, not a
  stable property** - rank on cross-civ spreads, never on absolute quality levels, and
  never on a single run's low.
- **Absolute run levels depressed vs lifetime** (run `avg_score` 0.539-1.212 vs lifetime
  1.03-1.59) - a level shift in the JEV scorer's output for this batch, **not a civ
  effect**; the cross-civ *ordering* carries the information.
- **Re-confirmations:** NAS EDQUOT total (14th session) - `git clone` straight into
  `/workspace` dies with `Disk quota exceeded`; clone to `/tmp` (overlay, 28 G free), then
  bridge the **nested** `cellular-first-design` dir with `ln -s` (NOT `ln -sfn`, which
  replaces a symlink with a real directory); verified by `stat -L -c '%d:%i'` on both
  sides (**129:3669** both sides) + `-ef` (EF_OK) + `readlink -f`; never flatten the
  nested tree; `gh` not installed (29th session) - use `GET /user/repos?per_page=100`
  with `GITHUB_TOKEN` and match on `AI-Writings`; tool timeout 30 s < run wall time
  (~45 s) - detached launch, then poll `ps` + the log; `ZAI_URL_OVERRIDE` alone is dead
  code (needs `ZAI_TOKEN`); `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`;
  JEV liveness = 422 on a malformed `questions`; z.ai = 401 `token expired or incorrect`
  (credential gap, endpoint healthy) - **45th session**.
- **NEW - `civilizations.json` is multi-line JSON, not JSONL.** A `json.loads(line)` reader
  raises `JSONDecodeError: Expecting value: line 2 column 1`. Use `json.load(open(...))`.
  (Session 121 noted this; it is re-confirmed here and the failure mode is loud, not silent.)
- **NEW - the per-civ "8 distinct previews" check must group ACROSS civs, not within one
  civ.** Grouping per civ can never yield 8 (a civ contributes one row per prompt), so the
  check reports a false failure on 8/8 civs. The correct assertion is: for ONE competition
  prompt, the set of `content_preview` over all 8 civs has size 8. The RUNBOOK's
  `assert len({r["content_preview"] for r in new_competition_rows}) == 8` is written against
  the *cross-civ* row set and is correct; a per-civ reader of the same rule is not.

## Run detail

| civ | run avg | run quality | run novelty | run alignment | lifetime avg | lifetime alignment | wins | win_rate |
|---|---|---|---|---|---|---|---|---|
| civ-precise | 1.2120 | 0.1980 | 1.5820 | 1.8560 | 1.4169 | 2.1791 | 271 | 0.573 |
| civ-formal | 0.9723 | 0.1680 | 1.3660 | 1.3830 | 1.2045 | 1.7474 | 77 | 0.162 |
| civ-poetic | 0.8923 | 0.2010 | 1.1780 | 1.2980 | 1.5936 | 2.1129 | 6 | 0.013 |
| civ-whimsical | 0.6873 | 0.1200 | 1.3470 | 0.5950 | 1.4566 | 1.7896 | 5 | 0.010 |
| civ-engineer | 0.6463 | 0.0760 | 1.4050 | 0.4580 | 1.1766 | 1.5870 | 39 | 0.083 |
| civ-mythic | 0.6140 | 0.1280 | 0.9870 | 0.7270 | 1.3002 | 1.6066 | 9 | 0.019 |
| civ-grounded | 0.5720 | 0.0550 | 1.3020 | 0.3590 | 1.0324 | 1.1621 | 68 | 0.143 |
| civ-therapist | 0.5393 | 0.0650 | 1.3310 | 0.2220 | 1.2090 | 1.3962 | 9 | 0.019 |

## Environment

- Sandbox was **wiped**; `/workspace` held only `.plugin-cache`. The requested path
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist.
- Upstream owner is **`SuperInstance/AI-Writings`** (3.7 GB, pushed 2026-10-25T01:04:50Z),
  not `ai-writings/cellular-first-design` (404). Found via `GET /user/repos?per_page=100`
  paginated 1-8; `gh` is not installed.
- Clone used `--filter=blob:none --no-checkout --depth 1` + `git sparse-checkout set
  --cone cellular-first-design/code/civilizations` (the **cone** form works when the leaf
  is a directory, contrary to the session-151 `--no-cone` note, which applies to
  non-directory leaves). Working tree **188 KB** of `.git` + a 6.2 MB civ subtree.
- NAS quota: `git clone` into `/workspace` fails with `Disk quota exceeded`; only the
  symlink bridge works. `mkdir` in `/workspace` succeeds, `cp` truncates to 0 bytes.
