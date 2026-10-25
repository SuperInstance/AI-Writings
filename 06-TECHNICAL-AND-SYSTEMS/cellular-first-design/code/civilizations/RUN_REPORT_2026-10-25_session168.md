# Civ Orchestrator — Run Report, session 168 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 51st session) + **live JEV**.
Baseline: `6bd9001` (session 167). **All 22 content checks PASS.**

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` and `.skills` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**10th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`** (3.7 GB) — the `ai-writings/…` slug 404s;
  the GitHub API is case-insensitive.
- Cloned to **`/tmp/repos/ai-writings`** with `--filter=blob:none --no-checkout` +
  `sparse-checkout set cellular-first-design` ⇒ **6.2 MB** working tree, 188 K of git objects.
  Cloning into `/workspace` fails with `Disk quota exceeded` (NAS EDQUOT, 16th session).
- Bridge: `ln -s /tmp/repos/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  The symlink points at the **clone root**, not the nested `cellular-first-design` dir.
  Verified by inode identity (**`129:3672` on both sides**) and `-ef` → `EF_OK`.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai returns **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent (**51st session**).
- **JEV live**: a well-formed `questions` body returns **HTTP 200** with
  `{"model":"jev-1.14.0", …}` this session — a stronger probe than the usual 422
  `dict_type` payload-shape complaint, because it also discloses the **served model version**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).
- `gh` not installed (**18th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll.

## Mock integrity (all four fixes re-applied)

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)[:8]` | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | 145 | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |

Pre-flight on the **exact long cultural prompts** (lengths **167–209**): **40/40 distinct
seeds**, **40/40 distinct previews**, **40/40 independently recomputed** `md5(whole_message)[:8]`,
**0** literal `seed={}` placeholders, **0** `(civ,prompt)` combos with >1 seed, **8/8** distinct
seeds on every one of the 5 prompts, **0** tracebacks.
Post-run mock log: **121** OK lines (40 pre-flight + 80 run + 1 GET), **0 `EXC:`**, **0** HTTP 500.
Teardown: mock pids killed by exact argv match, 0 remaining procs, `curl` exit 7 (port closed).

## Verification — 22 checks, all PASS

| Check | Expected | Observed |
|---|---|---|
| per-civ ledger Δ | +10 × 8 | **+10 × 8** (1116/1147/1162/1119/1141/1111/1114/1174 → +10 each) |
| total new ledger rows | **80** | **80** |
| `meta_log.jsonl` Δ | +5 | **+5** (573 → 578) |
| `Winner:` lines | 5 | **5** |
| `culture.json` `simulations_run` Δ | +10 × 8 | **+10 × 8** |
| `wins` = pre + times won | exact | **8/8 exact** (precise +4, grounded +1, rest +0) |
| `losses` = 5 − times won | exact | **8/8 exact** (precise +1, grounded +4, rest +5) |
| `relevance` Δ = Σ this run's `avg_score` | exact | **8/8 exact to 1e-6** |
| rows with JEV `error` | 0 | **0** |
| 2.0/2.0/2.0 fallback triples | 0 | **0** |
| `provider` | zai only | **zai × 80** |
| rows missing `[mock-zai seed=` prefix | 0 | **0** |
| distinct seeds | 40 / 80 rows | **40 / 80** |
| `(civ,prompt)` carrying >1 seed | 0 | **0** |
| 8/8 distinct previews per competition prompt | 5/5 | **5/5** |
| meta `results` = list of `[civ,score]` | 5/5 | **5/5** |
| meta vs ledger `avg_score` mismatches | 0 | **0** (40/40 exact) |
| distinct `(q,n,a)` triples | ≥70, no (2,2,2) | **80/80** |
| sim→competition ts gap at index 4 | 8/8 | **8/8** (2.46 s – 2.56 s) |
| confidence spread (JEV-side signature) | not constant | **0.25 – 0.97** |
| `git status --porcelain` (pre-report) | 18 modified | **18** |
| registry / generations | 8 civs, all gen 1 | **8 / {1}** |
| extinction risk | NONE | **NONE** (lowest +1075.08 = **108×** the floor) |

### NOTE — the meta-vs-ledger check needs the **later-ts** row, not the first match

A verifier that matches a meta row to the ledger row with the same `prompt` **and takes the
first hit** reports 26/40 false mismatches. The reason is structural: the **sim phase** picks
its prompt at random from the same 5, so a `(civ, prompt)` pair can appear **1–4 times** in
the 10 new rows (this run: 13 pairs × 1, 16 × 2, 9 × 3, 2 × 4). The **competition-phase** row
is the one with the **later `ts`**. Taking `max(cands, key=ts)` gives **40/40 exact**.

The meta `prompt` field is the **full** prompt; the ledger `prompt` field is **truncated to
80 chars** — so the match key is `m["prompt"][:80]`, never the raw meta prompt.

## Low-relevance civilization: **`civ-grounded` (The Grounded)** — 43rd consecutive session

**Lifetime (9 004 rows):**

| civ | n | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| civ-poetic | 1151 | 1.5478 | 0.7479 | 1.8527 | 2.0428 |
| civ-whimsical | 1184 | 1.3964 | 0.5922 | 1.9161 | 1.6808 |
| civ-precise | 1121 | 1.3911 | 0.5103 | 1.5520 | **2.1109** |
| civ-mythic | 1129 | 1.2527 | 0.5290 | 1.7033 | 1.5257 |
| civ-formal | 1157 | 1.1702 | 0.4511 | **1.4055** | 1.6539 |
| civ-therapist | 1124 | 1.1487 | 0.4621 | 1.7186 | 1.2654 |
| civ-engineer | 1126 | 1.1338 | 0.4518 | 1.4725 | 1.4771 |
| **civ-grounded** | 1172 | **0.9893** | **0.4099** | 1.4954 | **1.0625** |

Last of 8 on **avg_score**, **quality**, and **alignment**. Absolute gaps to the next civ:
**alignment 0.2029** (therapist 1.2654) versus **quality 0.0412** (formal 0.4511) ⇒ the
alignment gap is **4.9× wider**. Alignment is the dimension the meta-GAN *selects* on ⇒ a
**voice** failure, not a prose failure. Lifetime novelty 1.4954 is **6th of 8** — check the
rank, not the "above median" impression.

**Run-level (this run's 80 rows):** grounded **8th of 8** on `avg_score` (1.1423), the run
bottom on **all three** axes — `quality` 0.2970, `alignment` 0.9060 — and **7th of 8** on
novelty (2.2240). Gap to the next civ in the run is **0.3963** (whimsical 1.5387), i.e. the
run spread is *not* compressed the way it was in session 166 (0.0034). Grounded is last on
both the lifetime table and this run — the low label did **not** rotate.

**Lifetime vs run level.** Run `avg_score` levels (1.14 – 1.96) sit *above* the lifetime band
(0.99 – 1.55) for most civs, so this batch is scored *more generously* than the lifetime
average — the opposite of session 166's depressed level. The **ordering** still carries the
information: grounded is last under either level.

## Chooser vs `avg_score` argmax: 3/5 (60 %) — the "chooser picks lower" streak **ended**

| prompt | winner | score | argmax | score | delta | |
|---|---|---|---|---|---|---|
| what a cell is. | civ-precise | 1.9033 | civ-precise | 1.9033 | +0.0000 | AGREE |
| the bookkeeper's role. | **civ-grounded** | **0.9600** | civ-therapist | 2.0633 | **−1.1033** | LOWER |
| the witness log. | civ-precise | 2.4233 | civ-precise | 2.4233 | +0.0000 | AGREE |
| ternary values. | civ-precise | 1.7167 | civ-formal | 1.7567 | −0.0400 | LOWER |
| JEV as a decision oracle. | civ-precise | 2.3767 | civ-precise | 2.3767 | +0.0000 | AGREE |

**13 consecutive sessions** of the "chooser picks lower" direction ended this session:
agreement rose to **3/5 (60 %)**, the highest in the series. `civ-precise` swept **3/5**.

The mechanism is unchanged: the chooser is a JEV **`choice`** question over 150-char
`content_preview` snippets, while `avg_score` is the mean of three **`score`** questions on
the same text — different questions, different answers. **Never treat `win_rate` as a
quality metric.**

**This session's outlier is `civ-grounded` winning on the *worst* candidate** (0.9600 against
an argmax of 2.0633 — the single largest disagreement in the series at **1.1033**). Grounded
wins 1 of 5 competitions while sitting last of 8 on every relevance axis. Its `win_rate`
(0.127) is now mid-field while its `relevance_per_sim` (0.952) is last — the *selection*
signal and the *quality* signal disagree most sharply here than for any other civ.

## Inverses and distinct axes

- **`civ-poetic`**: 1st on lifetime `avg_score` (1.5478), `quality` (0.7479) and
  `relevance` (1684.71), but **last on `win_rate` (0.011)** — won 0/5. A *selection*
  failure, not a quality collapse.
- **`civ-precise`**: best `win_rate` (0.582), **highest lifetime alignment (2.1109)**, 1st on
  run `avg_score` (1.9593), and the run's top winner (3/5).
- **`civ-formal`**: the distinct low-**novelty** axis (1.4055, last of 8) — yet it took
  2nd-lowest on run `avg_score` (1.7463) and won 0/5.
- **`civ-engineer`**: `win_rate` 0.084 and `relevance` 1232.38, 7th of 8 on both — the
  mid-table civ that is neither an inverse nor a watch axis.
- Cross-civ spreads (this run): `avg_score` **0.8170**, `alignment` **1.6900**,
  `novelty` **0.3850**, `quality` **0.8440** (widest quality spread in the series — the
  opposite of session 166's collapsed 0.0430).

## Counter gap: NEGATIVE, fixed, and unchanged in magnitude — both epochs shown

`culture.json` `relevance_score` − ledger Σ`avg_score`:

| civ | blob gap | post-run gap | Δ |
|---|---|---|---|
| civ-whimsical | −173.1433 | −173.1433 | 0.0000 |
| civ-poetic | −96.8033 | −96.8033 | 0.0000 |
| civ-formal | −85.5267 | −85.5267 | 0.0000 |
| civ-grounded | −84.3467 | −84.3467 | 0.0000 |
| civ-mythic | −51.1100 | −51.1100 | 0.0000 |
| civ-engineer | −44.2433 | −44.2433 | 0.0000 |
| civ-therapist | −42.1133 | −42.1133 | 0.0000 |
| civ-precise | −32.6333 | −32.6333 | 0.0000 |
| **TOTAL** | **−609.9200** | **−609.9200** | **0.0000** |

Both columns are computed **within the same epoch** (blob `relevance` vs **blob** ledger
sum; post-run `culture.json` vs **working-tree** ledger sum) ⇒ the offset is **fixed**, not
accumulating. `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the
ledger** by an auditor. Sign confirmed from the data, not copied from a prior report.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   RUNBOOK with **all four** fixes (112, 118, 144, 145) and run the pre-flight probe
   (40 distinct seeds AND 40 distinct previews AND independently recomputed md5s)
   **before** the batch. The pre-flight has now saved the run **six** times in the series.
2. `ZAI_TOKEN` still absent ⇒ real z.ai unusable; Control B is the only provider path.
   JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the run-wide integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and
   isolate this run's rows by **count from the end of each civ file** (last 10), never by
   a `ts` cutoff. `git show HEAD:<path>` must be run with `cwd` = the **clone root**,
   not the civs directory — the civs dir is not a git root, and `git show` there returns
   empty stdout → `JSONDecodeError`.
4. **The meta-vs-ledger check must take the later-`ts` row** for a `(civ, prompt)` pair
   (see the note above). The sim phase and the competition phase share the same 5 prompts,
   so a pair recurs 1–4 times in the 10 new rows; the competition row is the later one.
5. `civ-grounded` has been the low-relevance civ for **43** straight sessions. If a session
   ever finds it mid-table, that is a *finding* — check the run-wide seed count first to
   rule out a degenerate mock before believing it.
6. Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
   **and** `< /dev/null`, then poll `ps` + the log.
7. The NAS EDQUOT trap also blocks **file delivery** — `cp` into `/workspace` leaves a
   0-byte file. Deliver by pushing to git and citing the remote URL, not a workspace
   attachment.
8. **Symlink rule:** `ln -sfn` will not replace an existing directory target, and the
   bridge must point at the **clone root** (not the nested `cellular-first-design` dir).
   `rm -rf` the old link, then `ln -s`, then verify with `stat -L -c '%d:%i'` on both
   sides + `-ef`.

## Session 168 — clean mock #26; the chooser's "picks lower" streak ended at 13 sessions

**Run:** 8 civs x 5 sims + 5 competition prompts, `--sims 5 --prompts 5 --providers zai`,
Control B mock bridge, JEV live. Baseline `6bd9001` (session 167). **All 22 content checks PASS.**

- per-civ ledger delta **+10** × 8 = **80 rows**; `meta_log` **573 → 578** (+5);
  `Winner:` lines **5**; **0** JEV `error` keys; **0** 2.0/2.0/2.0 fallbacks;
  **80/80** `[mock-zai` prefix with `provider=zai`; **40/40** distinct seeds;
  **0** `(civ,prompt)` combos with >1 seed; sim→competition ts gap at index 4 in **8/8**
  (2.46–2.56 s); **8/8** distinct previews on all 5 competition prompts; meta-vs-ledger
  `avg_score` mismatches **0**; **80/80** distinct `(q,n,a)` triples; `git status --porcelain`
  = **18** modified.

### NEW — the meta-vs-ledger check must take the **later-`ts`** row, not the first match

A first-match verifier reports **26/40 false mismatches** on a completely clean run. The
sim phase draws its prompt at random from the same 5 competition prompts, so a
`(civ, prompt)` pair recurs **1–4 times** inside the 10 new rows (this run: 13 pairs × 1,
16 × 2, 9 × 3, 2 × 4). The **competition-phase** row is the **later `ts`**. Using
`max(cands, key=ts)` gives **40/40 exact**. The match key is `m["prompt"][:80]` — the meta
`prompt` is full-length, the ledger `prompt` is truncated to 80 chars.

### FINDING — the chooser's "picks lower" direction ended after **13 consecutive sessions**

Agreement rose to **3/5 (60 %)** — the highest in the series — versus the 0–1/5 of sessions
154–166. `civ-precise` swept 3/5. Two of the five still picked a lower-scoring candidate,
but the deltas were small (−0.0400) against session 166's max −0.7600.

**The one large disagreement is the finding: `civ-grounded` won on the *worst* candidate**
— 0.9600 against an argmax of 2.0633, a **1.1033** gap, the largest in the series. Grounded
is last of 8 on lifetime `avg_score` / `quality` / `alignment` **and** last of 8 on this
run's `avg_score` / `quality` / `alignment`, yet it won 1 of 5 and its `win_rate` (0.127) is
mid-field against a last-place `relevance_per_sim` (0.952). The *selection* signal and the
*quality* signal disagree most sharply for this civ than for any other.

### `civ-grounded` remains the low-relevance civ — 43 consecutive sessions (95–168)

Last of 8 on lifetime `avg_score` 0.9893, `quality` 0.4099, `alignment` 1.0625, `relevance`
1075.08, `relevance_per_sim` 0.952. Label did **not** rotate. Absolute gaps: **alignment
0.2029** (vs therapist 1.2654) vs **quality 0.0412** (vs formal 0.4511) ⇒ a **4.9×** wider
alignment gap ⇒ a **voice** failure, not a prose failure. Lifetime novelty 1.4954 is **6th of
8**. Run-level: grounded **8th of 8** on `avg_score` (1.1423), `quality` (0.2970) and
`alignment` (0.9060), gap to the next civ **0.3963** — this run was *not* compressed
(session 166's run bottom was separated by 0.0034).

**Run levels are *higher* than lifetime this time** (run `avg_score` 1.14–1.96 vs lifetime
0.99–1.55) — the opposite of session 166's depressed level. The **ordering** is the signal,
not the level.

**Extinction risk NONE** (threshold −10, lowest +1075.08, **108×** the floor). Registry 8,
`max_civs` 12, all `generation=1`.

### Counter gap — both epochs side by side

blob gap **−609.9200**, post-run gap **−609.9200**, per-civ Δ **0.0000** for all 8 ⇒ the
offset is **fixed**, not accumulating. The epoch-mixing trap still applies: compute both
sides in the same epoch.

### Re-confirmations (this session)

- NAS EDQUOT total (16th session) — clone to `/tmp` (overlay), sparse-checkout
  `cellular-first-design` only, bridge the **clone root**, verify with `stat -L -c '%d:%i'`
  on both sides + `-ef`.
- z.ai **401** `token expired or incorrect` (credential gap, endpoint healthy) — **51st session**.
- **JEV HTTP 200 on a well-formed body** discloses the served model `jev-1.14.0` — a better
  liveness probe than the 422 `dict_type` complaint, because it names the version.
- `ZAI_URL_OVERRIDE` alone is **dead code** (the `ZAI_TOKEN` gate returns `None` first) —
  Control B needs **both**; `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll.
- `gh` not installed (18th session) — `GET /user/repos` with `GITHUB_TOKEN`; the GitHub API
  is case-insensitive (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
- Pre-flight on the exact long cultural prompts (lengths 167–209): **40/40 distinct seeds,
  40/40 distinct previews, 40/40 independently recomputed md5s, 0 tracebacks**. The
  pre-flight has now saved the run **six** times in the series.
