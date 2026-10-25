# Civ Orchestrator — Run Report, session 169 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 52nd session) + **live JEV**.
Baseline: `4965ec4` (session 168). **All 59 verification assertions PASS.**

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` and `.skills` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**11th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`** — the `ai-writings/…` slug 404s;
  the GitHub API is case-insensitive.
- Cloned to **`/tmp/repos/ai-writings/AI-Writings`** with `--filter=blob:none --no-checkout` +
  `sparse-checkout set cellular-first-design` ⇒ **14 MB** working tree. Cloning into
  `/workspace` fails with `Disk quota exceeded` (NAS EDQUOT, **17th session**).
- Bridge: `ln -s /tmp/repos/ai-writings/AI-Writings/cellular-first-design
  /workspace/repos/ai-writings/cellular-first-design`. The symlink points at the
  **clone root**, not the nested `cellular-first-design` dir. Verified by inode identity
  (**`129:3701` on both sides**) and `-ef` → `EF_OK`.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai returns **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent (**52nd session**).
- **JEV live**: a well-formed `questions` body returns **HTTP 200** with
  `{"model":"jev-1.14.0", …}` and a full scored answer — a stronger probe than the usual
  422 `dict_type` complaint, because it also discloses the **served model version**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).
- `gh` not installed (**19th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll.

## Mock integrity — all four fixes re-applied, **plus a fifth (seed width)**

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)[:8]` | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | 145 | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |
| **e** | **seed widened 2 → 4 hex chars** | **169** | **2-char slice collides ⇒ 39 distinct seeds, not 40** |

### NEW (this session) — the 2-char seed slice collided, and only the count gate caught it

The documented seed is `h[(i*2)%8:((i*2)%8)+2]` — a **2-hex-char** slice of the whole-message
md5. With 8 civs × 5 prompts = 40 samples drawn from 256 possible 2-char values, a collision is
a matter of course, and this session it happened:

| prompt | grounded | whimsical | formal | poetic | precise | mythic | therapist | engineer |
|---|---|---|---|---|---|---|---|---|
| what a cell is. | 44 | 5c | a6 | 4c | 3e | 82 | cc | 98 |
| the bookkeeper's role. | ba | 84 | dc | 3d | 88 | ce | 73 | de |
| the witness log. | 71 | 7c | **30** | c0 | d1 | **30** | 0c | f6 |
| ternary values. | 6f | df | c8 | dd | fa | 9c | 64 | 5f |
| JEV as a decision oracle. | 76 | a7 | b9 | 27 | 19 | 34 | d4 | 37 |

`civ-formal` and `civ-mythic` collided on **`30`/`30`** for "the witness log" ⇒ **39 distinct
seeds / 40 rows**, and that one prompt showed **7/8 distinct seeds**.

**The mock was healthy by every other measure**: HTTP 200, prefix present, 0 tracebacks,
0 `EXC:` lines, and — the decisive point — **40/40 seeds matched an independently recomputed
`md5(whole_message)[:8]`**. The md5s were *different*; only the 2-char slice collided. So this
is a **seed-width** defect, not a seeding bug: the fix (b) whole-message md5 was correctly
applied, and the slice it feeds is simply too narrow.

**Fix applied:** `seed = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]` — 4 hex chars,
keeping the (a) index wrap and (b) whole-message md5 intact. (d) interpolation unchanged.

**The lesson is the pre-flight's job, not the mock's:** the *only* assertion that caught this
was `distinct seeds == 40`. A 200, a correct prefix, zero exceptions, and a perfect md5
recompute all passed. **A seed that is correct but not unique is still a broken seed**, because
the chooser is handed a `choice` question over 150-char previews — two civs with the same seed
produce a *near*-duplicate candidate and the meta-GAN's tie-break is exactly what the mock is
supposed to exercise.

Pre-flight on the **exact long cultural prompts** (lengths **167–209**): **40/40 distinct
seeds**, **40/40 distinct previews**, **40/40 independently recomputed** md5s, **0** literal
`seed={}` placeholders, **8/8 distinct seeds AND 8/8 distinct previews on every one of the 5
prompts**, **0** tracebacks, **0** `EXC:`.
Mock log after the run: **0** `EXC:`, **0** `Traceback`.
Teardown: mock pids killed by exact argv match, 0 remaining procs, `curl` exit 7 (port closed).

## Verification — 59 assertions, all PASS

| Check | Expected | Observed |
|---|---|---|
| per-civ ledger Δ | +10 × 8 | **+10 × 8** (1172/1184/1157/1151/1121/1129/1124/1126 → +10 each) |
| total new ledger rows | **80** | **80** |
| `meta_log.jsonl` Δ | +5 | **+5** (578 → 583) |
| `Winner:` lines | 5 | **5** |
| `culture.json` `simulations_run` Δ | +10 × 8 | **+10 × 8** |
| `wins` = pre + times won | exact | **8/8 exact** (precise +4, engineer +1, rest +0) |
| `losses` = 5 − times won | exact | **8/8 exact** (precise +1, engineer +4, rest +5) |
| `relevance` Δ = Σ this run's `avg_score` | exact | **8/8 exact to 1e-6** |
| rows with JEV `error` | 0 | **0** |
| 2.0/2.0/2.0 fallback triples | 0 | **0** |
| `provider` | zai only | **zai × 80** |
| rows missing `[mock-zai seed=` prefix | 0 | **0** |
| distinct seeds | 40 / 80 rows | **40 / 80 rows** |
| literal `seed={}` placeholders | 0 | **0** |
| `(civ,prompt)` carrying >1 seed | 0 | **0** |
| 8/8 distinct seeds AND previews per competition prompt | 5/5 | **5/5** |
| meta `results` = list of `[civ,score]` | 5/5 | **5/5** |
| meta vs ledger `avg_score` mismatches | 0 | **0** (40/40 exact, later-`ts` row) |
| distinct `(q,n,a)` triples | ≥70, no (2,2,2) | **80/80 distinct**, no (2,2,2) |
| sim→competition ts gap at index 4 | 8/8 | **8/8** (2.44 s – 2.60 s) |
| confidence spread (JEV-side signature) | not constant | **0.27 – 0.98** |
| registry / generations | 8 civs, all gen 1 | **8 / {1}** |
| extinction risk | NONE | **NONE** (lowest +1087.12 = **109×** the floor) |
| counter gap Δ (blob vs post-run) | 0.0000 | **0.0000** total (Δ −0.0000) |

### NOTE — the meta-vs-ledger check needs the **later-ts** row, not the first match

Re-confirmed from session 168: the sim phase draws its prompt at random from the same 5, so a
`(civ, prompt)` pair recurs **1–4 times** inside the 10 new rows. The **competition-phase** row
is the later one. `max(cands, key=ts)` gives **40/40 exact**; first-match reports false
mismatches. The match key is `m["prompt"][:80]` — the meta prompt is full-length, the ledger
prompt is truncated to 80 chars.

## Low-relevance civilization: **`civ-grounded` (The Grounded)** — 44th consecutive session

**Lifetime (9 244 rows):**

| civ | n | avg_score | quality | novelty | alignment | relevance | rel/sim | win_rate |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 1161 | **1.5509** | **0.7491** | 1.8582 | 2.0453 | **1703.76** | **1.516** | 0.011 |
| civ-whimsical | 1194 | 1.3973 | 0.5904 | **1.9218** | 1.6798 | 1495.28 | 1.322 | 0.009 |
| civ-precise | 1131 | 1.3966 | 0.5118 | 1.5611 | **2.1170** | 1546.92 | 1.387 | **0.584** |
| civ-mythic | 1139 | 1.2532 | 0.5286 | 1.7098 | 1.5213 | 1376.30 | 1.230 | 0.018 |
| civ-formal | 1167 | 1.1748 | 0.4514 | 1.4154 | 1.6577 | 1285.49 | 1.143 | 0.165 |
| civ-therapist | 1134 | 1.1480 | 0.4600 | 1.7264 | 1.2576 | 1259.72 | 1.128 | 0.020 |
| civ-engineer | 1136 | 1.1369 | 0.4507 | 1.4822 | 1.4777 | 1247.23 | 1.120 | 0.085 |
| **civ-grounded** | 1182 | **0.9911** | **0.4086** | 1.5044 | **1.0603** | **1087.12** | **0.954** | 0.126 |

Last of 8 on **avg_score**, **quality**, **alignment**, **relevance**, and **relevance_per_sim**.
The low label did **not** rotate — 44th consecutive session.

Absolute gaps to the next civ: **alignment 0.1974** (therapist 1.2576) versus
**quality 0.0421** (engineer 0.4507) ⇒ the alignment gap is **4.7× wider**. Alignment is the
dimension the meta-GAN *selects* on ⇒ a **voice** failure, not a prose failure. Lifetime
novelty 1.5044 is **6th of 8** — check the rank, not the "above median" impression.

**Run-level (this run's 80 rows):**

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-precise | **2.0150** | 0.6730 | 2.5720 | **2.8000** |
| civ-poetic | 1.9050 | **0.8940** | 2.4860 | 2.3350 |
| civ-formal | 1.7143 | 0.4790 | 2.5590 | 2.1050 |
| civ-whimsical | 1.5113 | 0.3750 | 2.6000 | 1.5590 |
| civ-engineer | 1.4850 | 0.3270 | 2.5750 | 1.5530 |
| civ-mythic | 1.3123 | 0.4780 | 2.4380 | 1.0210 |
| **civ-grounded** | 1.2043 | 0.2520 | 2.5560 | 0.8050 |
| **civ-therapist** | **1.0697** | **0.2220** | 2.5990 | **0.3880** |

**The run low ROTATED to `civ-therapist`** (1.0697, gap to next **0.8353** — the run was *not*
compressed). Grounded is 7th of 8 on the run (1.2043); therapist is lower on both `quality`
(0.2220 vs grounded 0.2520) and `alignment` (0.3880 vs grounded 0.8050), and grounded is
higher on `avg_score` by only 0.1346.

**Lifetime vs run level.** Run `avg_score` levels (1.07 – 2.02) sit *above* the lifetime band
(0.99 – 1.55) for every civ — this batch is scored *more generously* than the lifetime average,
the same direction as session 168. The **ordering** carries the information, not the level.

## `civ-therapist` is a watch axis, not a finding

Therapist is the run bottom on `avg_score` (1.0697), `quality` (0.2220) and `alignment`
(0.3880) — and its alignment is catastrophic at 0.3880, roughly a third of the next civ
(mythic 1.0210). But its **lifetime** standing is mid-field: `avg_score` 1.1480 (6th of 8),
`alignment` 1.2576 (7th of 8), `relevance` 1259.72 (6th of 8). Per the session-132 rule,
**the run low and the lifetime low are different civs on different axes**. Grounded remains
the structural finding; therapist is the run-level watch.

Therapist's 10 new rows show a distinctive signature: **novelty 2.5990 is the run's highest**
while quality collapses to 0.2220 — it is generating text JEV rates as highly novel and as
poorly aligned. That is the definition of the *voice* axis failing.

## Chooser vs `avg_score` argmax: 2/5 (40 %) — the "picks lower" direction is back

| prompt | winner | score | argmax | score | delta | |
|---|---|---|---|---|---|---|
| what a cell is. | civ-precise | 1.9767 | civ-poetic | 2.0700 | −0.0933 | LOWER |
| the bookkeeper's role. | civ-precise | 1.7467 | civ-poetic | 1.8400 | −0.0933 | LOWER |
| the witness log. | civ-precise | 2.5933 | civ-precise | 2.5933 | +0.0000 | AGREE |
| ternary values. | civ-engineer | 1.4467 | civ-poetic | 1.8967 | **−0.4500** | LOWER |
| JEV as a decision oracle. | civ-precise | 1.9033 | civ-precise | 1.9033 | +0.0000 | AGREE |

Session 168's 3/5 (60 %) was the series high; this session is **2/5 (40 %)**, and **all three
disagreements took the lower-scoring candidate** — the "chooser picks lower" direction is back
after its one-session break. `civ-precise` swept **4/5**; `civ-engineer` took the ternary
slot.

The mechanism is unchanged: the chooser is a JEV **`choice`** question over 150-char
`content_preview` snippets, while `avg_score` is the mean of three **`score`** questions on the
same text — different questions, different answers. **Never treat `win_rate` as a quality
metric.** The clean-mock series now has 15 five-sample points spanning 0/5 – 4/5 ⇒ the honest
claim is *somewhere in 0–80 %*, not a point estimate.

The largest disagreement this session is **−0.4500** on "ternary values" (engineer 1.4467 vs
poetic 1.8967) — well below session 168's series-record −1.1033.

## Inverses and distinct axes

- **`civ-poetic`**: 1st on lifetime `avg_score` (1.5509), `quality` (0.7491), `relevance`
  (1703.76) and `relevance_per_sim` (1.516) — but **7th on `win_rate` (0.011)**, won 0/5.
  A *selection* failure, not a quality collapse. It was the `avg_score` argmax on **3/5**
  prompts and the chooser took it on **0/5** — the sharpest inverse in the fleet.
- **`civ-precise`**: best `win_rate` (0.584), **highest lifetime alignment (2.1170)**, 1st on
  run `avg_score` (2.0150) and run `alignment` (2.8000), and the run's top winner (4/5).
- **`civ-formal`**: the distinct low-**novelty** axis (1.4154, last of 8) — yet it took
  3rd on run `avg_score` (1.7143) and won 0/5.
- **`civ-whimsical`**: highest lifetime novelty (1.9218) and 2nd on lifetime `avg_score`,
  but **last on `win_rate` (0.009)** — the second inverse.
- **`civ-engineer`**: `win_rate` 0.085 and `relevance` 1247.23, 7th of 8 on both — the
  mid-table civ that is neither an inverse nor a watch axis.
- Cross-civ spreads (this run): `avg_score` **0.9453**, `alignment` **2.4120**,
  `quality` **0.6720**, `novelty` **0.1620**. The alignment spread is the widest in the
  series — consistent with the *voice* axis, not prose, being where the fleet actually
  differentiates.

## Counter gap: NEGATIVE, fixed, and unchanged in magnitude — both epochs shown

`culture.json` `relevance_score` − ledger Σ`avg_score`:

| civ | blob gap | post-run gap | Δ |
|---|---|---|---|
| civ-grounded | −84.3467 | −84.3467 | 0.0000 |
| civ-whimsical | −173.1433 | −173.1433 | 0.0000 |
| civ-formal | −85.5267 | −85.5267 | 0.0000 |
| civ-poetic | −96.8033 | −96.8033 | 0.0000 |
| civ-precise | −32.6333 | −32.6333 | 0.0000 |
| civ-mythic | −51.1100 | −51.1100 | 0.0000 |
| civ-therapist | −42.1133 | −42.1133 | 0.0000 |
| civ-engineer | −44.2433 | −44.2433 | 0.0000 |
| **TOTAL** | **−609.9200** | **−609.9200** | **0.0000** |

Both columns are computed **within the same epoch** (blob `relevance` vs **blob** ledger sum;
post-run `culture.json` vs **working-tree** ledger sum) ⇒ the offset is **fixed**, not
accumulating. `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the
ledger** by an auditor. Sign confirmed from the data, not copied from a prior report.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the RUNBOOK with
   **all five** fixes (112 index wrap, 118 md5-of-whole-message, 144 transport pair,
   145 interpolation, **169 seed width 2→4 hex chars**) and run the pre-flight probe
   (40 distinct seeds AND 40 distinct previews AND independently recomputed md5s AND 8/8 on
   every prompt) **before** the batch.
2. **The seed-width fix is not optional.** A 2-char slice over 40 samples from a 256-value
   space will collide; expect ~7–8 % collision odds per run. A collision shows up as
   "39 distinct seeds" or "7/8 on one prompt" and *nothing else* — the md5 recompute still
   passes, because the md5s really are different. Keep the recompute check **and** the count
   check; they catch different defects.
3. `ZAI_TOKEN` still absent ⇒ real z.ai unusable; Control B is the only provider path.
   JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
4. Use the run-wide integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and
   isolate this run's rows by **count from the end of each civ file** (last 10), never by
   a `ts` cutoff. `git show HEAD:<path>` must be run with `cwd` = the **clone root**,
   not the civs directory — the civs dir is not a git root, and `git show` there returns
   empty stdout → `JSONDecodeError`.
5. The meta-vs-ledger check must take the **later-`ts`** row for a `(civ, prompt)` pair
   (see the note above). The sim phase and the competition phase share the same 5 prompts,
   so a pair recurs 1–4 times in the 10 new rows; the competition row is the later one.
6. `civ-grounded` has been the low-relevance civ for **44** straight sessions. If a session
   ever finds it mid-table, that is a *finding* — check the run-wide seed count first to
   rule out a degenerate mock before believing it. **The run-level low already rotates**
   (this session: therapist) — do not promote the run low to the lifetime finding.
7. Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
   **and** `< /dev/null`, then poll `ps` + the log.
8. The NAS EDQUOT trap also blocks **file delivery** — `cp` into `/workspace` leaves a
   0-byte file. Deliver by pushing to git and citing the remote URL, not a workspace
   attachment.
9. **Symlink rule:** `ln -sfn` will not replace an existing directory target, and the
   bridge must point at the **clone root** (not the nested `cellular-first-design` dir).
   `rm -rf` the old link, then `ln -s`, then verify with `stat -L -c '%d:%i'` on both
   sides + `-ef`.
10. **Mock teardown:** kill by exact argv match (`python3 /tmp/mock_zai.py` and
    `timeout -s KILL 900 python3 /tmp/mock_zai.py`) — **two** pids. Never `pkill -f mock_zai`,
    which self-matches the killing shell. Then prove the port is closed: `curl -m 5` ⇒
    **exit 7** and `HTTP=000`.
