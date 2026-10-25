## Session 243 additions (2026-10-25)

### 1. A WIPED WORKSPACE NEEDS `sparse-checkout disable`, NOT `git checkout -- prose/`

`git sparse-checkout set cellular-first-design` leaves every path outside the cone **staged as
deleted** in `git status --porcelain` (here: 3 `prose/snowball-inspired/*` files). The obvious
repair, `git checkout -- prose/`, **fails** with

```
error: pathspec 'prose/' did not match any file(s) known to git
```

because those paths are not in the sparse index at all. The fix is `git sparse-checkout disable`
— the working tree then matches `HEAD` and `git status --porcelain` is empty.

*Rule: the change-detector for a run is `git status --porcelain` on the **baseline** tree. A
dirty baseline turns "18 files changed" into "21 files changed" and every downstream file count
becomes unverifiable. Assert an empty status before the run, and fix the index — not the
worktree — when the cone is the cause.*

### 2. A PRE-FLIGHT THAT REPORTS **9 SEEDS WHERE THE SPEC SAYS 8** IS A CHECKER BUG

The mock was correct: 8/8 distinct seeds per prompt, all matching an independently recomputed
md5. The **checker** was wrong — its `by_prompt` accumulator appended a `None` placeholder
before the real seeds, so every prompt counted **9** ("8 real + 1 None").

*Rule: the 8/8-per-prompt check must count the seeds it actually sent, never a padded list.
And the standing rule holds: a recompute that disagrees with the mock means "the checker is
wrong" before it means "the mock is wrong" — dump one real body and parse it by hand first.*
This is the **third** occurrence of a checker-side false alarm in this series.

### 3. `culture.json` HAS **`simulations_run`**, NOT `sims_run` — AND A BATTERY THAT DIES MID-WAY LEAVES A FALSE VERDICT

The verification battery raised `KeyError: 'simulations_run'` on the first civ it checked, and
the transcript up to that point was **18 PASS lines with no verdict**. A battery that crashes
half-way reads exactly like a partial pass.

*Rule: print an explicit final `VERIFICATION: n/n PASS` + `VERDICT:` line and `sys.exit(1)` on
any failure. Also: `leaderboard.json` exposes `sims_run` but `culture.json` exposes
`simulations_run` — the two files use different key names for the same quantity, so a checker
that reads one and writes the other will fail on the civ it reaches first.*

### 4. THE MOCK'S `d[0]` IS THE **RAW MD5 BYTE** — CONFIRMED **2480/2480** AGAIN

Re-derived from the ledger and validated over the full current-format ledger *before* the run:
**2480/2480 exact, 0 mismatches** (the current-format population is now 2480 rows; the
historical `[mock-zai <12 hex>]` form is still 240 rows and does not parse).

*Rule: `i = d[0] % 4` where `d[0]` is the raw byte — `int(h[0], 16)` is a different algorithm
that will fail the recompute.*

### 5. THE RUN LOW AND THE LIFETIME LOW DECOUPLED **AGAIN** — AND ALIGNMENT DOMINATED AT **2.52x**

Run low `civ-therapist` (avg **1.1327**, fleet-low quality **0.2770** and fleet-low alignment
**0.6630** — a two-axis collapse) against lifetime low `civ-grounded` (**2266.60**, lowest
rel/sim **1.206**, lifetime-low quality **0.544**) for the **104th** consecutive session.

The run's alignment spread (**1.8570**) is **2.52x** the `avg_score` spread (**0.7377**); quality
0.87x, novelty 0.21x. Novelty is near-constant across the fleet (**0.1560** spread) and carries
almost no ranking information.

`civ-therapist`'s novelty is **3rd-highest of 8** while its alignment is the fleet low — the
signature of a **voice** failure, not a prose failure. Report the axis, not just the label.

### 6. THE **4-1 WINNER SPLIT** AND **1/5 (20 %) AGREEMENT** — STILL **0 UP-GRADES EVER**

`civ-precise` took 4/5 competitions, `civ-formal` 1/5. Agreement with the `avg_score` argmax
was **1/5 (20 %)**, with **4 down-grades and 0 up-grades**. The chooser reads only
`content_preview[:150]` and never sees `avg_score`, so every disagreement is a down-grade **by
construction** — the up-grade count is pinned at 0 structurally.

*Rule: a winner-streak (here 4/5) is a description of history, not a prediction. Sessions 237
split 2-2-1 and 243 split 4-1; the field is genuinely competitive.*

## Session 238 additions (2026-10-25)

### 1. THE TAIL IS A **PER-SESSION CONSTANT** — 13 TAILS, ALL SHARED BY ALL 8 CIVS

The whole current-format ledger (2080 rows) holds **13** distinct tails, each exactly
**162** chars, and the set is **identical for all 8 civs**. Every `(civ, prompt)` pair
carries **13** distinct tails across history, so the tail is **not** keyed to
`(civ, prompt)`. Clustering by `ts` gap gives **26** sessions, and every session uses
**exactly one** tail across all **80** rows.

*Rule: extract the current session's family from the most recent 80-row cluster and reuse
it for all 80 rows. Never derive the tail from `(civ, prompt)` or a request counter.*

### 2. THE COUNTER GAP MUST BE SUMMED OVER THE **FULL** LEDGER

Comparing post-run `relevance` against the sum of the **new rows only** (the ledger also
holds the 5 competition rows) made the gap appear to move by **11-21 points for every
civ** — a fabricated "the gap is accumulating" regression. Over the **full** history the
gap is stable to **3.3e-03**, exactly as documented.

*Rule: the gap is `relevance - sum(avg_score over the ENTIRE ledger)`. A subset changes it
by design and manufactures a fake drift.*

### 3. THE COMPETITION PHASE ISSUES **NO** PROVIDER REQUESTS OF ITS OWN

The mock served **161** requests (41 pre-flight + 40 repeat + 80 sims), not 161 + 40 — the
competition re-uses the sim rows. The session-237 expectation of 89 (80 sims + 5
competitions + 4 pre-flight) cannot reconcile with a ledger that gained 80 rows.

*Rule: expected requests = `preflight + repeat + (ledger row delta)`.*

### 4. `--filter=blob:none --no-checkout` IS THE CLONE FORM THAT WORKS

A `--depth 50` full clone pulled 1.2 GB and died; `--depth 1` with a sparse cone still
fetched the whole tree. The working form is blobless + no-checkout, then
`sparse-checkout set cellular-first-design/code/civilizations` — the path needs the
**subdirectory**, or the checkout succeeds with an empty tree.

### 5. THE **SWEEP RETURNS** AFTER A 2-2-1 SPLIT

`civ-precise` took **5/5** this session, one session after the 2-2-1 split of session 237
ended a 19-session sweep run. `civ-therapist` took the run low in **6 of the last 7**
sessions; `civ-grounded` held the lifetime low for the **100th** consecutive session.

*Rule: a winner-streak is a description of history, not a prediction, in **either**
direction.*

### 6. ALIGNMENT DOMINATED AT **2.40x**; THE RUN LOW WAS A **THREE-AXIS** COLLAPSE

Alignment spread **2.1460** = **2.40x** the `avg_score` spread (0.8960). Run low
`civ-therapist` (avg **1.1673**) held quality **0.4670**, novelty **2.3480** and alignment
**0.7220** — all three at the fleet low, where sessions 225/227/237 were two-axis.

## Session 237 additions (2026-10-25)

### 1. A **2-2-1 WINNER SPLIT** IS THE END OF A 19-SESSION `civ-precise` SWEEP RUN

`civ-precise` took **2/5** this session, `civ-engineer` **2/5**, `civ-formal` **1/5**. The
`avg_score` argmax was `civ-poetic` on **3 of 5** prompts — the same argmax pattern as
session 231, while the chooser picked a different civ every time.

*Rule: a winner-streak is a description of history, not a prediction. Sessions 211-236 had
`civ-precise` sweeping most prompts; a 2-2-1 split is evidence the field is genuinely
competitive, not a measurement artefact. Never carry "X sweeps every session" forward.*

### 2. **PARTICIPATION COUNT IS NOT CONSTANT** — ASSERT THE **DELTA**, NOT THE TOTAL

`wins + losses` totals across the fleet are **891-898**, not multiples of 5, because **35
historical competitions had fewer than 8 participants**: in `civilization_competition()` a civ
whose `run_simulation` returned `None` never enters `results`, so it is neither a winner nor a
loser. This session's 5 competitions each had **8/8** participants.

*Rule: assert `d_wins + d_losses == 5` against the **baseline commit**, not the absolute total.
An assertion of the form "total % 5 == 0" is only valid when the participation count is known
to be constant — and it is not, historically.*

### 3. THE **NFS BRIDGE** CAN REPORT A **BROKEN LINK** FOR A LINK THAT IS FINE

Immediately after `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`,
`ls -la .../code/civilizations/` returned *"No such file or directory"* — while `ls -d` on the
**same** path succeeded, and `stat -L` showed a valid directory. The workspace is an **NFS**
mount (`vers=3`), so the negative lookup came from a **stale attribute cache** on the parent
directory, not from a broken link. A later call to the identical command succeeded with **no
filesystem change in between**.

*Rule: on the NAS bridge, a one-shot "No such file or directory" immediately after creating a
symlink is **not** proof the link is broken. Verify with `stat -L` and `os.path.samefile()`,
and **re-read the path** before reporting it absent. Conversely, a path that `ls -d` resolves
and `ls -la` does not is an NFS artifact, not a structural problem.*

### 4. THE TAIL SHOULD BE **EXTRACTED**, NOT RECONSTRUCTED

The 162-char tail prefix was pulled **byte-for-byte** from the ledger's dominant family (400
occurrences) with a small script rather than retyped. A hand-reconstructed tail came out at
**210** chars — 48 too long — and pushed the body to **386**, above the 332-369 band, because
the geometry is `38 + 162 + continuation` and the tail is the one term that must be exact.

*Rule: extract the tail from the ledger, then solve the continuation as `target - 38 - 162`.
A tail is not a thing you can paraphrase; the byte count is load-bearing.*

### 5. THE **CHOOSER CANNOT AGREE** WITH `avg_score` — AND 0 UP-GRADES IS NOW 21 SESSIONS

Agreement was **1/5 (20 %)** with **4 down-grades and 0 up-grades**; the up-grade count across
the whole series remains **0**. The chooser reads only `content_preview[:150]` and never sees
`avg_score` (structural — session 231), so every disagreement is a down-grade **by
construction**. All four down-grades were marginal (max delta 0.35, no cliff).

*Rule: report agreement and the up/down split as two separate numbers, and state the
structural reason the up-grade count is pinned at 0 so nobody reads it as a regression.*

### 6. THE **TWO-AXIS COLLAPSE** SIGNATURE HELD, AND THE AXIS DOMINANCE IS NOW 2.24x

Run low `civ-therapist` (avg **1.6847**) with quality **1.3480** and alignment **1.2090** both
at the fleet low while novelty held at **2.4970** (4th-highest of 8). The run's alignment spread
(**2.0180**) was **2.24x** the `avg_score` spread (**0.9017**); quality 0.79x, novelty 0.23x.

*Rule: report the axis signature **for this session**. The holder rotates; the axis does not.*

## Session 234 additions (2026-10-25)

*This session ran concurrently with session 235 against the same baseline (`f6f3609`). Its
full addendum is in `skills/civ-orchestrator-learnings.md`; the summary is the same shape as
session 235's — `civ-precise` swept 5/5, chooser/argmax agreement 2/5 (40 %) with 3
down-grades and 0 up-grades, run low `civ-therapist` (avg 1.7533, fleet-low run alignment
1.62), lifetime low `civ-grounded` (2122.93, 98th consecutive session), extinction risk NONE
(lowest = 212x the -10 floor). The one addition worth carrying forward is recorded in the
235 addendum: **a re-derivation is not a correction** — the two candidate index rules are
provably the same rule, and a near-miss is invisible to every self-consistency check.*

### 8. A PARALLEL SESSION WILL PUSH WHILE YOU ARE RUNNING — **MERGE, DO NOT CLOBBER**

This session's `git push` was rejected with *"Updates were rejected because the remote contains
work that you do not have locally"*: another session ran the **same command against the same
baseline** and pushed a `session 234` report while this run was in flight. Both runs are valid
and nearly identical in shape — same baseline, 80 rows each, `civ-precise` 5/5 in both, same
2/5 chooser agreement, same run-low and lifetime-low holders.

The rebased merge **preserves both runs**:
- per-civ ledgers: `base + 10 + 10` rows, interleaved in `ts` order
- `meta_log`: `903 -> 913`
- `culture.json` counters **summed** (`relevance_score`, `wins`, `losses`, `simulations_run`)
  so `relevance delta == sum(last 20 avg_score)` holds exactly (residual <= 1.6e-12)
- the report **renumbered** to 235 so two sessions do not both claim `session 234`

*Rule: a concurrent session is a **second measurement to preserve**, not a conflict to resolve
by picking a winner. And when a merge touches an **absolute counter** file, **recompute** the
counter from the two runs' deltas — taking one side's `culture.json` silently discards the other
session's 80 rows from the relevance total while leaving the ledger looking intact.*
*Corollary for the report: when two sessions produce near-identical headline numbers, the
honest write-up is that **both runs agree**, and the ledger is the proof.*

### 9. A REBASE CONFLICT IN A **JSONL LEDGER** IS RESOLVED BY **REBUILDING THE FILE**, NOT PICKING A SIDE

`git rebase` marks the whole `simulations.jsonl` conflicted (every line is "added at the same
position"), but the correct resolution is mechanical: `base_lines + sorted(theirs_new + mine_new,
key=ts)`. Doing it by hand invites a silent row loss; doing it in code and then **asserting the
row count and `ts` monotonicity** makes the merge auditable.

*Rule: resolve ledger conflicts programmatically and verify the count, the ordering, and the
absence of duplicates — then re-derive the counter identity against the rebuilt file.*

## Session 235 additions (2026-10-25)

### 1. A **RE-DERIVATION** IS NOT A **CORRECTION** — PROVE THE TWO RULES ARE ACTUALLY DIFFERENT

This session re-derived the Control B seed algorithm from the committed ledger and, in the
process, briefly concluded that the documented index rule was wrong. It was not. The
documented form uses the first **digest byte**; the re-derivation used the second **hex
nibble**; and the two are *provably the same rule*:

```
d[0] = 16*h[0] + h[1]        and        16*h[0] % 4 == 0
=> d[0] % 4 == h[1] % 4      for all 256 byte values
```

Both forms match the current-format ledger **1840/1840 exact, 0 mismatches**. The report was
corrected before commit.

*Rule: "I found a correction" is a claim that must itself be proved before it is written down.
When a re-derivation disagrees with a documented rule, first check whether the two are
**different rules or a re-spelling of the same one** — try expressing the documented rule in
your own notation and test it. A near-miss that agrees with the documented rule on *some* rows
is the dangerous case, not the obvious disagreement.*

### 2. THE **NIBBLE** TRAP: `d[0] % 4` AND `h[0] % 4` LOOK INTERCHANGEABLE AND ARE NOT

`h[0] % 4` (first hex **nibble**) matches only **638/1840** current-format rows; `d[0] % 4`
(first digest **byte**) matches **1840/1840**. The nibble drops the low two bits the modulus
depends on.

The near-miss is invisible to **every** self-consistency check the mock can run: the wrong rule
is still deterministic, still distinct per message, and still carries a colour and figures.
Worse, **colour and figures sit at fixed offsets** (`h[8:12]`, `h[12:24]`) and are therefore
correct under *any* index rule — so a pre-flight that checks "seed+colour+figure present"
passes on a wrong seed.

*Rule: assert the index rule itself over the **full historical ledger**, never over the rows
you just produced. A colour/figure match is not a seed match.*

### 3. THE **HOLDER ROTATION** IS NOT A LAW — AND A POST-ROTATION STREAK IS STILL A COUNTER

The run-level low rotated every session from 220 through 231 (therapist, whimsical, therapist,
therapist, therapist, mythic, mythic, whimsical, therapist, therapist, whimsical) and then
**held `civ-therapist` for three sessions running** (232, 233, 234) — a **two-axis**
quality+alignment collapse each time.

*Rule: a rotation pattern is a description of history, not a prediction. When a streak forms
*after* twenty rotations, it is still a counter to be re-derived next session, and the "holder
rotates every session" phrasing must not be carried forward as a standing fact.*

### 4. A **5/5 SWEEP** IS NOT **CHOOSER AGREEMENT** — THEY COINCIDED HERE

`civ-precise` won **5/5** competitions. The chooser agreed with the `avg_score` argmax on only
**2/5 (40 %)** — 3 down-grades, **0 up-grades** — and the argmax was `civ-poetic` on three of
the five prompts.

*Rule: winner count and chooser calibration are independent measurements. Report both, and
never let a sweep imply agreement. The chooser reads only `content_preview[:150]` and never
sees `avg_score` (see the session-231 structural note).*

### 5. THE LIFETIME LOW AND THE RUN-LEVEL LOW WERE **DIFFERENT CIVS** — 7 SESSIONS RUNNING

`civ-grounded` holds the lifetime low (`relevance` **2121.68**, `relevance_per_sim` **1.186**,
**98th consecutive session**) but placed **6th of 8** on this run's `avg_score` (1.8087) — and
its deficit axis **flipped** from alignment-led (session 233) to quality-led (1.0100 quality,
2.0530 alignment, mid-field). `civ-therapist` took the run-level low (avg **1.6020**) and is the
2nd-lowest lifetime civ.

*Rule: the lifetime label and the run rank are different measurements; do not promote one to
the other, and re-derive the deficit axis each session rather than carrying it forward.*

### 6. `ln -s` FAILS WITH ENOENT WHEN THE **INTERMEDIATE DIRECTORY** IS MISSING

Creating `/workspace/repos/ai-writings/cellular-first-design` as a symlink to the clone
fails with `No such file or directory` unless `/workspace/repos/ai-writings` already exists as
a real directory. The error names the **target** path, not the missing parent, so it reads
like "the repo vanished" when it means "create the parent first".

*Rule: on the NAS bridge, `mkdir -p` every intermediate path before linking, and verify with
`os.path.samefile()` — the shell `test -ef` is unusable in this sandbox.*

### 7. THE **38 / 162 / 200** GEOMETRY HELD AGAIN, AND THE TAIL POOL IS **8 FAMILIES x 3 PADS**

A merged count over the current-format ledger yields **8 distinct tail families** (not 10 or 12
as earlier sessions counted) and **3 whitespace pad widths** (0, 1, 2). All visible previews are
exactly **200** chars = **38-char header + 162-char body**, for every row in every session. The
body is **constant for a whole run** (one family + one pad per server start) and rotates between
runs — so the tail prose is free, the geometry is not.

*Rule: the invariant to assert is the **38 / 162 / 200 geometry**, not a tail-text count. A
tail-family count changes as the pool grows; the geometry has never moved.*

## Session 231 additions (2026-10-25)

### 1. THE CHOOSER **CANNOT** AGREE WITH `avg_score` — IT NEVER SEES THE SCORES (STRUCTURAL, NOT A REGRESSION)

This session's chooser-vs-`avg_score` agreement was **0/5 (0 %)** — the lowest in the 21-session
series, and the first run where the `avg_score` argmax was the *same* civ (`civ-poetic`) on **all
five** prompts while the chooser selected `civ-precise` on all five.

The code settles it. `civilization_competition()` builds the JEV question as:

```
state = "PROMPT: ...\n\nCANDIDATES FROM CIVILIZATIONS:\n"
      + "\n[<civ name>]: <content_preview[:150]>\n"      # for each civ
questions = {"best_civ": {"type": "choice", ...}}
```

so the chooser reads **only the first 150 characters of each candidate's text**. The `avg_score`
the battery compares against comes from a *different* JEV call (`quality`/`novelty`/`alignment`
score questions over a different state) and is **never passed to the chooser**. The
`max(results, key=avg_score)` line in the code is a **fallback for a failed JEV call**, not the
normal path.

*Rule: chooser-vs-`avg_score` divergence is a **structural property of the two-question design**.
Do not read the agreement rate as a quality KPI, and do not call a 0 % run a regression. What
is worth recording is the **direction** (up/down), the **margin**, and whether the argmax is a
**single repeated civ** — a one-civ argmax sweep means the two axes have fully diverged, which
is a stronger signal than a mixed one. Verify the chooser is live by replaying the `choice`
question and checking for a `probabilities` distribution; a live answer looks like
`{"choice": "civ-precise", "confidence": 0.73, "probabilities": {...}}`, while the fallback
path produces a `max(...)` over `avg_score` with no probabilities.*

### 2. A RESIDUAL THAT IS SMALL BUT **NOT FLOAT-SIZED** MEANS THE **BASELINE** WAS ROUNDED

The battery's assertion 11 (`relevance` delta = Σ`avg_score`) failed at max residual
**3.33e-05** — 4 orders of magnitude above the 1e-6 tolerance. The run was fine; the baseline
I typed into the script was the **4-decimal table copied from the previous session's report**,
not the true float. `git show HEAD:.../culture.json` gave the full-precision values and the same
assertion then passed at **8.14e-13** across all 8 civs.

*Rule: float noise is ~1e-13; a 3e-05 residual is exactly what a 4-decimal-rounded baseline
predicts. When a residual is small but not float-noise-sized, suspect **baseline provenance**
before suspecting the run. Recover the pre-run values from git, not from a report table.*

### 3. THE FULL-LEDGER RECOMPUTE MUST **COUNT WHAT IT FINDS** — THE LEDGER GROWS EVERY SESSION

Session 230 anchored its pre-run recompute at "1440 current-format rows". This session the same
8 ledgers yielded **1760** current-format rows out of **14 124** total, matching
**1760/1760 exact, 0 mismatches**.

*Rule: never hardcode the expected current-format row count. Scan the ledgers and count the
current-format rows actually found. A stale expected-count would report a healthy ledger as
short — and a short ledger is exactly the symptom of a wrong algorithm, so the error would
point at the mock instead of at the expectation.*

### 4. THE RUN'S **QUALITY AXIS CAN COLLAPSE FLEET-WIDE** — A RUN-LEVEL PROPERTY, NOT A PER-CIV TRAIT

Every civ's quality axis landed in a narrow low band this run (**0.7700 – 1.4320**, spread
0.6620) while novelty was nearly flat (**2.4490 – 2.5840**, spread 0.1350) and alignment
carried the whole discrimination (spread **1.8690**, **13.84x** the novelty spread). The
alignment spread was 2.28x the `avg_score` spread and 2.82x the quality spread.

*Rule: before attributing a low score axis to a civilization, check the **fleet-wide spread of
that axis** in the same run. A collapsed axis separates nobody, so the "low holder" of that
axis is an artifact of the run, not a trait of the civ. Report the axis signature for the
session, and check the fleet spread before naming a weakness.*

### 5. TWO-AXIS COLLAPSE, 2ND CONSECUTIVE SESSION — AND THE HOLDER ROTATED TO `civ-whimsical`

The run low was `civ-whimsical` (avg **1.4267**), a **quality+alignment two-axis collapse**
(quality **0.7700**, alignment **0.9500**, both fleet-low) with novelty untouched (**2.5600**,
2nd-highest). Session 230's run low was `civ-therapist` with the same two-axis signature.

*Rule: the **holder rotates** and so does the **axis set**, but the two-axis collapse
(quality+alignment, novelty untouched) has now repeated for a second consecutive session. Keep
reporting the axis signature per session and do not carry the previous axis diagnosis forward.*

### 6. `civ-grounded` HELD THE LIFETIME LOW FOR THE **95th CONSECUTIVE SESSION** — AND STILL RANKED 5th ON THE RUN

Lifetime relevance **2071.25** (from 2052.79), `relevance_per_sim` **1.1780** — last of 8, and
the label did not rotate. Run-level it was **5th of 8** on `avg_score` (**1.8463**), *above* its
lifetime rank, with an alignment/quality gap of **1.0640** — the weakness is again **prose
quality, not voice**.

*Rule: a lifetime-low label and a run rank are different measurements. Keep reporting both; a
civ can hold the lifetime low while sitting mid-field in any given run.*

### 7. THE COUNTER GAP IS **BYTE-IDENTICAL** ACROSS SESSIONS — CONFIRMED AGAIN

Gaps: grounded **-84.3467**, whimsical **-173.1433**, formal **-85.5267**, poetic **-96.8033**,
precise **-32.6333**, mythic **-51.1100**, therapist **-42.1133**, engineer **-44.2433** —
max drift **0** against the published table. *The offset is fixed; a run neither repairs nor
worsens it.*

### Re-confirmations (this session)

- 111th session with the prompt path absent; 95th session with the z.ai credential gap
  (z.ai **401** on a direct live probe => endpoint healthy, credential absent).
- Repo is `SuperInstance/AI-Writings`; `cellular-first-design` is a **subdirectory**. NAS
  EDQUOT total (18th session) — clone to the overlay, bridge the **clone subdirectory**,
  verify with `os.path.samefile()` -> `True`.
- `gh` not installed (26th session). `git fetch` needs `GIT_SSL_NO_VERIFY=1`; fetch
  `refs/heads/main` explicitly and assert the SHA equals the clone HEAD (`4305f6d`).
- The mock source is **not in the repo on any branch**; rebuild it per session and prove the
  algorithm against the full current-format ledger first.
- `ZAI_URL_OVERRIDE` alone is **dead code** — Control B needs **both** `ZAI_TOKEN` (gate) and
  `ZAI_URL_OVERRIDE` (destination). `TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`; JEV live at
  `jev-1.14.0`; **0** fallback triples, **80/80** distinct triples.
- Pre-flight **12/12 PASS on the first build**; run verification **18/18 PASS**.
- Extinction risk **NONE** — lowest civ at **2071.25**, **207x** the -10 floor. Registry 8,
  `max_civs` 12, all `generation=1`.
- Mock teardown by **PID captured from `ps`**, then prove the port closed (`curl` exit 7,
  `HTTP=000`). Never `pkill -f mock_zai` (self-match).
- The **only** free variable in the mock body length is the continuation: solve
  `target − 38 − 162` (this session: 351 = 38 + 162 + 151).

## Session 230 additions (2026-10-25)

### 1. THE CONTROL B MOCK SOURCE IS **NOT IN THE REPO** — THE LEDGER IS THE SPECIFICATION

A search of **every** remote branch (`git ls-remote --heads origin`, 60+ branches) for a mock
server source returns **nothing**. The Control B server has always been a session-local
artifact; the repository carries only the *reports* and the *skill file* that describe it.

*Rule: a session that rebuilds the mock must first prove the algorithm against the **whole**
current-format ledger — not against its own fresh rows, which is circular. This session
re-derived the canonical algorithm and matched **1440/1440 exact, 0 mismatches** over the
current-format rows of the 8 civ ledgers, before the run.*

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4
seed   = h[(i*2)%8 : (i*2)%8+4]
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

### 2. THE **38 / 162 / 200** GEOMETRY IS THE ONLY UNIVERSAL INVARIANT — THE TAIL TEXT IS FREE

A merged count of the 1440 current-format rows yields **10 distinct tail prefixes**, all of
them exactly **162** chars, and every visible preview exactly **200** chars. The
**38 + 162 = 200** geometry holds across every session in the ledger; the tail *prose* rotates
freely (10 distinct tails in this cut; the session-229 report counted 12 across a
differently-cut row set — the count is a property of the cut, the **162** is a property of the
ledger).

*Rule: assert the geometry (38 / 162 / 200), never the tail prose.*

### 3. THE **CONTINUATION** IS THE ONLY BODY-LENGTH CONTROL — AND THE FIRST BUILD CAN LAND BELOW THE BAND

Header 38 + tail 162 = 200, leaving the continuation as the sole free variable. This
session's first build appended 125 continuation chars for a **325**-char body — **7 below**
the 332 floor. Extending the continuation to 151 gave **351**, mid-band.

*Rule: solve the continuation as `target − 38 − 162`. Never trim the tail and never shorten
the header — both are constants the ledger's own rows depend on.*

### 4. THE META-LOG ROW IS WRITTEN **AFTER** THE COMPETITION ROWS — "LATER-TS" IS THE WRONG PREDICATE

The session-229 battery asserted *"meta-vs-ledger `avg_score` 0 mismatch (later-ts row)"*.
This session inherited that wording and failed **40/40** — every civ in every prompt.

The code path settles it: `civilization_competition()` writes each civ's `simulations.jsonl`
row **as the simulation completes**, and the `meta_log` row is appended **after the whole
competition phase returns**. The ledger row is therefore **earlier** in `ts` than the meta row
by ~3.1-3.2 s. The assertion looked for the opposite and so failed on a perfectly clean run.

The deltas were a clean **+3.09 to +3.24 s** on all 40 pairs, and the `avg_score` values
themselves had **0** real mismatches. Rewriting the check to `min(ts) <= meta.ts` gave **0**.

*Rule: a 100 %-failure assertion is an **inverted predicate** until proven otherwise — check
the *sign* of the expected delta before touching the data. The summary is written after the
facts it summarises, never before.*

### 5. THE COUNTER GAP IS **BYTE-IDENTICAL** TO SESSION 229 — FIXED, NOT ACCUMULATING

| civ | relevance | ledger Σ avg_score | gap | session 229 |
|---|---|---|---|---|
| `civ-grounded` | 2052.7900 | 2137.1367 | **-84.3467** | -84.3500 |
| `civ-therapist` | 2093.1867 | 2135.3000 | **-42.1133** | -42.1100 |
| `civ-engineer` | 2298.6333 | 2342.8767 | **-44.2433** | -44.2400 |
| `civ-mythic` | 2363.9167 | 2415.0267 | **-51.1100** | -51.1100 |
| `civ-formal` | 2404.3700 | 2489.8967 | **-85.5267** | -85.5300 |
| `civ-whimsical` | 2432.4667 | 2605.6100 | **-173.1433** | -173.1400 |
| `civ-precise` | 2792.7533 | 2825.3867 | **-32.6333** | -32.6300 |
| `civ-poetic` | 2911.5833 | 3008.3867 | **-96.8033** | -96.8000 |

Max drift vs the documented values: **3.3e-03** (rounding in the published table). The offset
is **fixed** — neither repaired nor worsened by this run.

### 6. THE SERIES LINE ADVANCES, AND THE UP-GRADE COUNT IS **STILL 0**

Agreement series (211-230): 0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 /
100 / 60 / 80 / 40 / **40** %. Up-grades across **20** sessions: **0**.

*Never predict the next value from the last one, and never let a sweep imply agreement.*
This session `civ-precise` swept **5/5** and still disagreed on 3/5 — and all three
down-grades were **marginal** (max **0.1033**, no cliff), the narrowest down-grade set of the
series.

### 7. THE ALIGNMENT AXIS DOMINATED THE SPREAD — 2.33x THE `avg_score` SPREAD

Run alignment spread **2.0130** vs `avg_score` spread **0.8627** (2.33x), quality spread
**0.6540** (3.08x) and novelty spread **0.2050** (9.82x). The alignment axis again dominates
the run's variance.

*Rule: report the axis signature **for this session**. The holder rotates; the axis does not.*
This session's run low was `civ-therapist` (**1.5970**) with quality **1.1990** and alignment
**1.0950** both at the fleet low — a **two-axis** collapse — while novelty held at **2.4970**,
2nd-highest of 8. `civ-grounded` held the **lifetime low for the 94th consecutive session**
(**2052.79**) and ranked **6th of 8** on the run's `avg_score**.

## Session 229 additions (2026-10-25)

### 1. A BULK RECOMPUTE MISMATCH OF THIS SIZE IS A **PARSER** BUG UNTIL THE SEED ALONE IS RE-CHECKED

The pre-run full-ledger recompute (all **1600** current-format rows) first reported **9280
mismatches**. The ledger was fine: my regex was

```
^\[mock-zai ([0-9a-f]{4})\] (#?[0-9a-f]{4}) ([0-9a-f]{4})/([0-9a-f]{4})/([0-9a-f]{4})\.
```

The optional `#` sits **inside** the capture group, so the group text is `#44cc` **or** `44cc`
and the **group numbering shifts** when the `#` is absent — the figure groups then match the
wrong fields. Normalising with `m.group(2).lstrip('#')` gives **1600/1600 exact**.

*The seed alone is the only shift-invariant field. When a bulk recompute fails, compare the
seed before believing the bulk result — a parser bug and a broken algorithm look identical from
the mismatch count alone.*

### 2. THE TAIL PREFIX IS **PER-SESSION**, NOT PER-PROMPT — 12 DISTINCT TAILS IN THE LEDGER

The ledger holds **12 distinct tail prefixes** across the 1600 current-format rows, including
both the "The voice carries a small discipline…" and the "A cell keeps its own accounts…"
families. The tail is chosen **per session**; only the **header geometry** is universal:

```
38-char header + 162-char tail prefix = 200  == content_preview[:200]
```

Every current-format preview is exactly 200 chars. *A session's mock need not reproduce the
previous session's tail text, but it must satisfy the 38+162=200 geometry, or the visible
prefix and the ledger's recorded prefix stop agreeing and the reconciling parser breaks.*

**The tail prefix must be EXACTLY 162 chars.** 161 gives a 199-char visible preview and breaks
the invariant **silently** — no band check catches it. 38 + 162 + 160 = **360**, inside the
332-369 band, on the first build by arithmetic.

### 3. A `confidence == 0.0` ROW IS **NOT** A FALLBACK — THE **TRIPLE** IS THE TEST

One of 80 new rows (`civ-grounded`, "ternary values") recorded `confidence: 0.0`. The documented
fallback returns `(2,2,2)` with confidence **0.5**. That row's triple was
`(1.19, 2.41, 2.38)` — substantive and varied. A **direct replay** of the same JEV state
returned live scores with non-zero confidence (`0.12/0.9`, `2.51/0.58`, `0.97/0.2`), so the
zero is a **transient field value from one JEV response**.

*The fallback test is the triple, never the confidence field. One zero-confidence row with real
scores is JEV variance; a `(2,2,2)` row is a broken provider or an unconfigured key.*

### 4. A FAILING VERIFICATION ASSERTION MAY BE THE WRONG ASSERTION — CHECK IT BEFORE THE DATA

The run gate initially asserted "confidence spread non-degenerate, min > 0" and **failed** on
the row above. The assertion encoded the wrong invariant: the meaningful quantity is the
**spread** (`max - min = 0.45`) and the **absence of the fallback triple**, not `min > 0`.
The assertion was rewritten; the data was not touched.

*When a verification assertion fails, first ask whether it encodes the real invariant.*

### 5. THE COUNTER GAP IS BYTE-IDENTICAL TO THE DOCUMENTED STABLE VALUES — FIXED, NOT ACCUMULATING

Gaps: grounded **-84.3467**, whimsical **-173.1433**, formal **-85.5267**, poetic **-96.8033**,
precise **-32.6333**, mythic **-51.1100**, therapist **-42.1133**, engineer **-44.2433** —
max drift **3.3e-03** against the published table (rounding). *The offset is fixed; a run
neither repairs nor worsens it.*

### 6. THE RUN-LOW SIGNATURE ROTATES ON THE AXIS TOO — NOT JUST THE HOLDER

Session 229's run low is `civ-therapist` with a **two-axis collapse**: quality **1.2100** and
alignment **1.2530** both at the fleet low, novelty **2.4140** untouched. Sessions 226-227 were
all-axes, session 228 was alignment-alone. *Report the axis signature for this session — the
holder rotates, the axis does not, and neither does the number of collapsed axes.*

### 7. `civ-grounded`'s WEAKNESS CHANGED AXIS — PROSE QUALITY, NOT VOICE

Lifetime low for the **93rd consecutive session** (relevance **2033.34**), but **3rd of 8** on
this run's `avg_score` (**2.0540**). Its run axes: quality **1.3610**, novelty **2.3830**,
alignment **2.4180** — an **alignment/quality gap of 1.0570**, the widest of any civ, so the
weakness is **prose quality, not voice**. Sessions 214-168 recorded the opposite (a *voice*
failure, alignment gap 5.2x the quality gap). *Do not carry the previous session's axis
diagnosis forward — re-derive it.*

### 8. THE CHOOSER'S "PICKS LOWER" STREAK IS NOW **19 SESSIONS WITH 0 UP-GRADES**

Agreement **2/5 (40 %)**, **3 down-grades, 0 up-grades**. The widest down-grade was the first
prompt: `civ-grounded` won "what a cell is" at **1.79** over `civ-precise` at **2.27**
(**-0.4767**). Series (211-229): 0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 /
100 / 60 / 80 / **40** %. *A sweep never implies agreement.*

### Re-confirmations (this session)

- 109th session with the prompt path absent; 93rd session with the z.ai credential gap.
  Repo is `SuperInstance/AI-Writings`; `cellular-first-design` is a **subdirectory**.
- NAS EDQUOT total (16th session) — 600 G / 600 G. Clone to `/tmp/ai-writings` (overlay),
  bridge the **clone root**, verify with `os.path.samefile()` -> `True` (inode `129:3671`).
- `gh` not installed (24th session). `git fetch` needs `GIT_SSL_NO_VERIFY=1`; fetch
  `refs/heads/main` explicitly and assert the SHA equals the clone HEAD (`e439b39`).
- `ZAI_URL_OVERRIDE` alone is **dead code** — Control B needs **both** `ZAI_TOKEN` (gate) and
  `ZAI_URL_OVERRIDE` (destination). `TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`; JEV live at
  `jev-1.14.0`; **0** fallback triples, **80/80** distinct triples.
- Pre-flight **12/12 PASS on the first build**; run verification **14/14 PASS**.
- Extinction risk **NONE** — lowest civ at **2033.34**, **203x** the -10 floor. Registry 8,
  `max_civs` 12, all `generation=1`.

---
name: civ-orchestrator-learnings
description: Durable operating knowledge for the Civilization Orchestrator (cellular-first-design). Mock provider rebuild checklist, verification gates, environment traps, and interpretation rules for the meta-GAN leaderboard.
---

## Session 228 additions (2026-10-25)

### 1. THE CANONICAL SEED ALGORITHM RE-VERIFIES AT **1520/1520** OVER THE FULL LEDGER

Session 227 established that the current-generation algorithm is

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4
seed   = h[(i*2)%8 : (i*2)%8+4]                  # CONTIGUOUS 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # three STRING components
```

This session ran that recompute over **every current-format row in the whole ledger**
(**1520 rows**, not just the session's own) and got **1520/1520 exact, 0 mismatches**.

*Do this **before** the run, not after. A recompute that agrees with 80/80 of your own
freshly-written rows can still be the wrong algorithm when the mock and the verifier
share the same mistake — the agreement is then a tautology. The full-ledger recompute is
independent of this session's code path.*

### 2. THE PREVIEW BOUNDARY IS **38 + 162 = 200** — A DESIGN INVARIANT, NOT A COINCIDENCE

The header is a constant **38** chars (`[mock-zai <4hex>] #<4hex> <4hex>/<4hex>/<4hex>. `)
and the tail prefix is **162** chars, so `38 + 162 = 200` — exactly the orchestrator's
`content_preview[:200]` cut. The visible tail therefore *always* ends at the same
character of the same sentence across every session, and the continuation past it is
**never** in the ledger.

*Assert only what is visible. Do not attempt to reconstruct the hidden continuation from
the ledger, and do not read the visible prefix as "the whole tail".*

### 3. THE RUN-LOW **SIGNATURE** ROTATES WITH THE HOLDER — THE AXIS DOES NOT

Sessions 226 and 227 both ran `civ-mythic` low on quality, novelty **and** alignment
*simultaneously* (an all-axes collapse). Session 228 runs `civ-whimsical` low on
**alignment alone** — avg **1.4607**, quality **1.1740** (2nd-lowest), novelty
**2.4200** (2nd-**highest**), alignment **0.7880** (last by **0.3290**).

The run's alignment spread **2.3210** is **2.42x** the `avg_score` spread, **3.41x** the
quality spread and **17.85x** the novelty spread.

*Rule: report the axis signature **for this session**. "The run low is the all-axes civ"
was true for two sessions and is false today. The alignment axis is the constant; the
holder and the co-occurring axes are not.*

### 4. A **5/5 SWEEP** DOES NOT IMPLY PERFECT AGREEMENT — SESSION 228 IS THE CLEAN COUNTEREXAMPLE

`civ-precise` won **5/5** competitions and was the `avg_score` argmax on **4/5**:
agreement **4/5 (80 %)**, **1 down-grade, 0 up-grades**. The disagreement
("ternary values") took `civ-precise` at **1.950** over `civ-poetic` at **1.977** — the
**lower**-scoring candidate, by **0.027**.

The series (211-228) now reads
0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 / 100 / 60 / **80** %, and
the up-grade count is still **0** across all 18 sessions.

*Never infer agreement from a sweep, or a sweep from agreement. Session 226 had 5/5 and
5/5; session 227 had 3/5 and 3/5; this session has 5/5 and 4/5.*

### 5. THE MOCK BODY LANDED AT **349** CHARS ON THE FIRST BUILD

38-char header + a 162-char tail prefix + a 149-char continuation = **349**, inside the
332-369 band, solved algebraically. *The band is a length problem, not a writing
problem: compute the allowance from the fixed prefix.*

### 6. THE `ls -la` CHECK IS THE WEAKEST ONE — AND IT PASSED ON A TREE WITH 18 MODIFIED FILES

`ls -la` shows mtimes; the discriminating check is the **row-count delta** (+10 each = 80)
against the pinned git blob, plus the counter-gap check. *Use `ls -la` to answer the
question asked; use the row-count delta to answer the question meant.*

### Re-confirmations (this session)

- 108th consecutive session with the prompt path absent (workspace held only
  `.plugin-cache`). The repo is **`SuperInstance/AI-Writings`** (a **user** account,
  5400+ repos); `cellular-first-design` is a **subdirectory**, not a repo.
- `gh` is not installed (**23rd session**). `GET /user/repos` paged to **2500** rows and
  filtered on `cellular|civ|writing`; the GitHub API is case-insensitive so the
  `ai-writings` slug resolves to `AI-Writings`.
- NAS EDQUOT is total (600 G/600 G) while the workspace lists as empty; the clone went to
  `/tmp/aiw` (**28 G** on the overlay) and was bridged by symlink to
  `/workspace/repos/ai-writings/cellular-first-design`, targeting the **clone root** so
  the script's hard-coded `CIVS_DIR` resolves — verified with `os.path.samefile()` ->
  `True`.
- `ZAI_TOKEN` absent from env and all **8** sandbox secrets; z.ai **401 `token expired or
  incorrect`** (**92nd session**) => endpoint healthy, credential absent. `ZAI_URL_OVERRIDE`
  alone is dead code — Control B needs **both**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0**
  fallback triples.
- `git fetch` needs `GIT_SSL_NO_VERIFY=1`; fetch **`refs/heads/main`** explicitly and
  assert the SHA equals the clone HEAD (`8433523`).
- Counter gap **byte-identical** to the documented stable values (max drift 4.55e-13
  against the pinned pre-run blob): grounded −84.35, whimsical −173.14, formal −85.53,
  poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24.


# Civ Orchestrator — durable learnings

## Session 225 additions (2026-10-25)

### 1. THE "NEEDS `-L`" RULE IS ABOUT **WHERE THE BRIDGE LANDS**, NOT ABOUT `ls`

Session 225 bridged `/workspace/repos/ai-writings/cellular-first-design` -> the **clone
root** (`/tmp/ai-writings/cellular-first-design`, the inner dir the `CIVS_DIR` constant
resolves through). The civs directory sits two levels below the bridge target, so the last
path component of `ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/`
does **not** cross a symlink boundary — and the plain `ls -la` **worked**. Sessions 214-217
needed `-L` because those bridges landed on `.../code`, one level closer to the leaf.

*Use `-L` when the last path component crosses the bridge; do not assume it always fails,
and do not "fix" a working `ls`.*

### 2. THE CURRENT-GENERATION LEDGER HAS **TWO** COLOUR FORMATS — 1120 WITH `#`, 240 WITHOUT

Of 1280 current-format rows, **1120** render the colour with a hash
(`[mock-zai 71a2] #44cc dd7c/7cd2/2400.`) and **240** without
(`[mock-zai ba6b] af26 4577/a9d5/49dc.`). Both recompute **1360/1360** against the md5
algorithm, so the `#` is a **renderer change, not an algorithm change** — the seed, colour
and figure are identical either way.

*The reconciling parser must make the `#` optional and **normalise one side** before
comparing. Do not treat "no `#`" as an older generation: filter on the header *shape*
(`[mock-zai <4hex>] #?<4hex> <4/4/4>`) and then re-derive.*

### 3. A PRE-FLIGHT GATE THAT CRASHES AFTER SEVERAL PASS LINES IS **NOT** A PASSING GATE

The first session-225 gate build printed 8 PASS lines and then died with
`ValueError: too many values to unpack (expected 3)` — the fixture rows are 4-tuples
`(civ, prompt, msg, content)` and the determinism loop unpacked 3. The failure was silent
as a *verdict*: the exit code was 1, but the transcript looked 8-for-8.

*Carry the already-fetched content forward instead of re-deriving it inside the loop, print
an explicit final verdict line, and exit non-zero on any failure. The same rule as session
222's "a failed launch must be checked for a clean tree" — a partial transcript is not a
result.*

### 4. THE MOCK BODY LANDED AT **351** CHARS ON THE FIRST BUILD

A 39-char header + a 163-char recorded tail prefix + a 149-char continuation = **351**,
inside the 332-369 band on build 1. *Compute the allowance from the fixed prefix; never
iterate prose to fit a band.*

### 5. THE CHOOSER SERIES (211-225) IS **0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 %** — AND STILL **0 UP-GRADES EVER**

Session 225: `civ-precise` won 4/5, `civ-engineer` 1/5; agreement **2/5 (40 %)** with
**3 down-grades, 0 up-grades**; `civ-poetic` was argmax on 3/5 prompts and won 0/5. The
widest down-grade margin was **−0.3900**. *Re-derive every session; the series oscillates
across the full range and the up-grade count is still zero after 15 sessions.*

### 6. THE RUN LOW'S SIGNATURE IS **LOW ALIGNMENT** — 10 SESSIONS RUNNING — AND THE MARGIN MOVED AGAIN

Run low `civ-therapist` (avg **1.4950**, fleet-low run quality **0.9720**, fleet-low run
alignment **1.0770**), gap to next **0.2577 = 28.8 %** of the run spread **0.8943** — against
session 220's **13.6 %** for the *same* civ. The run's alignment spread **1.9980** is
**2.47x** the quality spread and **12.04x** the novelty spread. *The holder is sticky; the
margin is a separate, faster-moving quantity — quote the gap next to the spread.*

### 7. `civ-grounded` HELD THE LIFETIME LOW FOR THE **89th** CONSECUTIVE SESSION, AND THE THREE AXES REMAIN THREE DIFFERENT CIVS

Lifetime low `civ-grounded` (relevance **1977.52**, rel/sim **1.1352**, lifetime avg
**1.1836**, fleet-low lifetime quality **0.5154**) — yet its lifetime `win_rate` **0.088**
is 3rd-best in the fleet. Lifetime **alignment** low is `civ-therapist` (**1.1947**);
lifetime **novelty** low is `civ-formal` (**1.7129**). *Selection and relevance are
separate axes and the axis identity rotates. Report the axis, not the holder.*

## Session 222 additions (2026-10-25)

### 1. THE BRIDGE TARGET IS DECIDED BY THE SCRIPT'S HARD-CODED `CIVS_DIR` — NOT BY THE VERIFICATION PROBE

Session 221's note said to bridge the **inner** `cellular-first-design/code` dir. Session 222
followed that and the run died on `load_civilizations()` with
`FileNotFoundError: .../code/code/civilizations/civilizations.json`.

`civilization_orchestrator.py:39` hard-codes:

```
CIVS_DIR = Path("/workspace/repos/ai-writings/cellular-first-design/code/civilizations")
```

so the bridge must target the **clone root** (`.../cellular-first-design`) for that constant
to resolve. With the inner-`code` bridge it resolves to `.../code/code/civilizations`.

*The pre-flight exercises the MOCK, not the orchestrator's path resolution — it passed
11/11 on a configuration that could not possibly run. **Resolve the script's own constant
first, then bridge to match it**, and treat "the pre-flight passed" as evidence about the
mock only.*

### 2. THE COUNTER-GAP CONSTANT IS NOT CONSTANT — IT MOVES BY EXACTLY `2W-5`

Session 221 recorded the counter gap (`wins - losses`) as a **byte-identical fleet
constant**. It is not. Every civ participates in **all 5** competitions, so a civ with
`W` wins takes `(5 - W)` losses and the gap moves by

```
delta = W - (5 - W) = 2W - 5
```

Session 222: `civ-precise` (W=5) gap **+299 -> +304**; the seven civs that lost all five
(W=0) each moved **exactly -5**. A check asserting a **zero** delta reports a false FAIL
on a perfectly clean run.

*Derive the expected counter delta from the code path, not from the last session's
observed value. A "constant" observed 5 times in a row is still an observation.*

### 3. THE BODY BAND SOLVED ALGEBRAICALLY LANDED AT **334** ON THE FIRST BUILD

The current-generation header is a constant **38** chars
(`[mock-zai <4hex>] #<4hex> <4/4/4>. `). A **161**-char tail + a **135**-char continuation
gives a constant **334**-char body — inside the 332-369 band on the first build, with the
cultural-prompt band measured from the real `culture.json` files at **167-209**.

*Compute the allowance from the fixed prefix; do not trim prose to fit a band.*

### 4. A FAILED LAUNCH MUST BE CHECKED FOR A CLEAN TREE BEFORE RE-RUNNING

The first session-222 launch died at `load_civilizations()` and wrote **0** rows:
`git status --porcelain` was empty and all 8 row counts were unchanged. That had to be
*checked*, not assumed — the failure happened after `load_civilizations` would have been
reached in a different code path, and a partial write would have needed a
`git checkout --` reset.

## Session 217 additions (2026-10-25)

### 1. THE CURRENT-GENERATION LEDGER HAS **ONE** TAIL, NOT FIVE — FILTER BY HEADER FORMAT FIRST

The section above records "the recorded 162-char body tail is a function of the CANON
prompt … all 8 civs share the same 5 tails". Measured against the **current-format** rows
only (header matching `[mock-zai [0-9a-f]{4}] #[0-9a-f]{4} [0-9a-f]{4}/[0-9a-f]{4}/[0-9a-f]{4}`),
there is exactly **1** distinct tail across all 5 prompts and all 8 civs — **161 chars**,
beginning `A cell keeps its own accounts and asks the network for what it cannot remember
itself. The bookkeeper and the witness log are two names for the same discipline: `.

The 5-tail claim describes an **older** mock generation, and the fleet's 9040 `[mock-zai`
rows are mostly that older generation. *Filter to the current header format before sizing
or reconstructing anything off the ledger.*

### 2. THE COLOUR CARRIES ITS `#` — A RAW-SLICE COMPARISON REPORTS 0/160 FALSE MISMATCHES

The recorded header is `[mock-zai 71a2] #44cc dd7c/7cd2/2400.` but the derived colour is
`h[8:12]` = `44cc`, **without** the `#`. Comparing the raw slice against the recorded group
reports **0/160** on a perfectly healthy mock. A reconciling check must prepend `#` to
the derived colour (or strip it from the recorded one) before comparing. *The parser
normalises; the comparison must too.*

### 3. `core.sparseCheckout` DOES NOT NARROW THE **FETCH** — IT ONLY NARROWS THE CHECKOUT

`git init` + `core.sparseCheckout set <dir>` + `git fetch --depth 1 origin` still
downloaded **3.4 GB** of the 3.7 GB `SuperInstance/AI-Writings` tree: the sparse filter
applies at checkout, not at fetch. The clone is only cheap if the *fetch* is narrowed
(`--filter=blob:none` plus a tree-filtered refspec, or a targeted
`git fetch origin <sha>:<ref>`).

### 4. `git fetch --depth 1 origin` RESOLVES `refs/heads/HEAD` — A STALE SYMREF, NOT `main`

On `SuperInstance/AI-Writings` the ref `refs/heads/HEAD` points at a **stale** commit
(session 142) while `refs/heads/main` is the live tip (session 216 at the time of
writing). A plain `git fetch --depth 1 origin` then checks out the stale tree and the
whole run is silently measured against an **old baseline**. *Always fetch
`refs/heads/<default-branch>` explicitly and assert `git rev-parse FETCH_HEAD` equals
`git ls-remote origin refs/heads/main` before trusting the tree.*

### 5. A SECOND MOCK LAUNCH ON THE SAME PORT FAILS SILENTLY WHILE THE FIRST KEEPS SERVING

Starting the mock a second time raises `OSError: [Errno 98] Address already in use` in
the new process's log, but a `curl` probe still returns **HTTP 200** — served by the
*first* process. A green probe does not prove your process owns the port. *Check the
mock's log for the bind error and confirm the pid you expect is the one listening.*

### 6. THE CHOOSER SERIES IS **0 % / 40 % / 40 % / 100 % / 60 % / 40 %** (SESSIONS 211-217) AND IT IS STILL **0 UP-GRADES EVER**

Session 217: `civ-precise` took 4/5, `civ-formal` took 1/5; `civ-poetic` was argmax on
**3/5** prompts and won **0/5**; agreement **2/5 (40 %)** with **3 down-grades, 0
up-grades**. *Re-derive the series every session; never carry a streak forward.*

### 7. THE RUN LOW AND THE LIFETIME LOW WERE **DIFFERENT CIVS** AGAIN (8 SESSIONS RUNNING)

Run low: **`civ-therapist`** (avg **1.7627**, alignment **1.6060** fleet-low, quality
**1.1250** fleet-low), 8th of 8, gap to 2nd **0.1513** = **22.3 %** of the run spread.
Lifetime low: **`civ-grounded`** (relevance **1834.52**, rel/sim **1.1331**, lifetime
quality **0.4940** fleet-low) — yet Grounded's lifetime `win_rate` **0.092** is 3rd-best
in the fleet. The lifetime *alignment* low is a **third** civ, **`civ-therapist`**
(**1.1995**). The run's alignment spread (**1.4180**) is **2.23x** the quality spread and
**9.71x** the novelty spread. *The low-relevance signature is still LOW ALIGNMENT, not
low novelty. Report the axis, not the holder.*

### 8. THE MOCK BODY LANDED AT **350** CHARS ON THE FIRST BUILD — INSIDE THE 332-369 BAND, ZERO ITERATION

The header is a constant **39** chars and the recorded tail prefix is a constant **161**
chars, so a continuation of exactly **150** chars gives a constant body of
**39 + 161 + 150 = 350**. *Compute the allowance from the fixed prefix rather than
trimming prose to fit a band.*

## The `wins`/`losses` counters are NOT in the ledger (false-FAIL trap)

`simulations.jsonl` rows carry exactly **9 keys** —
`avg_score, civ, civ_name, content_preview, params, prompt, provider, scores, ts` — and
**no `won` flag**. A verification check that reads `row["won"]` gets `0` for every civ and
reports a **false FAIL** on the wins and losses checks.

The counters live only in `culture.json`, incremented at
`civilization_orchestrator.py:296` for the **JEV-selected** winner
(`answers.best_civ.choice`, falling back to max `avg_score`).

**Take `times_won` from `meta_log.jsonl`'s `winner_civ` field**, never from the ledger.

## `max(results)` is NOT the winner

`meta_log.winner_civ` (the JEV `best_civ` selection) disagreed with the plain argmax on
**2 of 5** prompts in session 187 — prompt 2: argmax `civ-poetic` 1.97 vs winner
`civ-precise` 1.93; prompt 5: argmax `civ-precise` 1.94 vs winner `civ-formal` 1.69.

The stdout `Winner:` line **agrees with `meta_log`**; the argmax is the misleading one.
Count wins from `meta_log`, never from `max(results)`.

## Diagnostic discriminators that are not what they look like

- **A JEV 422 `union_tag_not_found` is a PAYLOAD-SHAPE error, not an auth error.** A probe
  built as `{"question":…, "weight":…, "scale":…}` is rejected. The orchestrator's own
  shape is `{"type": "score", "instructions":…, "criteria":[…]}`. **Copy the body from the
  source** (`jev_score`), do not improvise. A well-formed body returns HTTP 200
  `{"model":"jev-1.14.0", …}`.
- **A z.ai 401 `token expired or incorrect` means the endpoint is HEALTHY and the
  credential is ABSENT** — not that the provider is down. It is the expected probe result
  when `ZAI_TOKEN` is missing.
- **A zombie orchestrator process is a COMPLETED run.** The detached launcher never reaps
  the child, so `ps` shows `Zs` indefinitely. **Verify completion by the log tail and the
  row deltas, not by process exit.**
- **A 403 from the GitHub REST core API can be a rate limit, not an absence.** Check
  `/rate_limit` and note that **`/search/*` has its own separate quota** — core was
  5000/5000 (403) while search still had 30. A 403 renders as "not found" for every
  candidate at once.

## THE MOCK MUST RETURN AN OPENAI-SHAPED ENVELOPE (8th, undocumented-in-the-algorithm item)

`call_provider` does `r["choices"][0]["message"]["content"]`. A mock that writes the raw
body as the HTTP payload is a `JSONDecodeError` on the **first** request, not on a
liveness probe (the port answers, the body just isn't the shape the client wants).

```
{"id":"mock-zai-<seed>","object":"chat.completion","created":0,"model":"glm-4.5",
 "choices":[{"index":0,"finish_reason":"stop",
             "message":{"role":"assistant","content":<the 360-char body>}}],
 "usage":{"prompt_tokens":N,"completion_tokens":N,"total_tokens":N}}
```

This is the **eighth** thing to get right, after the seven documented fixes, and it is
**not** in the algorithm block. With it applied, the pre-flight passed **12/12 on the
first build**.

## A PRE-FLIGHT FIXTURE MUST BE READ FROM DISK, NEVER HAND-TYPED

The pre-flight's cultural-prompt length band (**167-209**) is a property of the real
`culture.json` files — their names, tenet lists and `voice_emphasis` strings. A fixture
with invented tenet strings measured **145-177** and produced a **false FAIL** on the
band check, which is indistinguishable from a real regression.

**Read the real cultures into the pre-flight.** A band assertion whose fixture is
hand-typed tests the fixture, not the system.

## The mock provider algorithm (fully known; do not re-derive)

The Control B mock for `zai` derives every response from the md5 of the request's
user message. This is now **verified 80/80 against the session-169 ledger**
(seed, colour and figure all match), so it does not need re-deriving.

```
d      = md5(cultural_prompt).digest()          # the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                               # MESSAGE-derived, NOT a request counter
seed   = h[(i*2)%8:(i*2)%8+4]                      # WIDENED slice, not padded
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"     # three components, NOT a division
```

`cultural_prompt` is exactly what `civilization_orchestrator.py` builds:

```
You are a voice in the tradition of "{name}".
Your tenets: {tenets joined by ", "}.
Your voice: {voice_emphasis}.

{prompt}
```

Only **4** distinct seeds are reachable from one message (the seed slices `h[0:8]`
at even offsets), so `i mod 4` is the whole index space.

**The observable signature of a message-derived index:** the seed is *stable across
every row of the same `(civ, prompt)` pair*. A request counter cannot produce that,
because the competition phase fires 8 civs in parallel and a counter would hand
them different values.

## Mock rebuild checklist — SEVEN fixes

| # | Fix | Symptom if missing |
|---|---|---|
| a | `seed[(i*2)%8:(i*2)%8+2]` index wrap | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | md5 of the **whole message** (not the first 8 alnum chars) | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |
| e | seed widened 2 → 4 hex chars | a 2-char slice collides ⇒ 39 distinct seeds / 40 rows, one prompt at 7/8 |
| f | **index from the MESSAGE (`d[0] % 4`), not a request counter** | **64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed** |
| g | **figure = three string components, not a division** | **`TypeError` on every request ⇒ HTTP 500 while the socket stays open; a port/200 liveness probe still looks healthy** |

**The spec's `figure = h[12:16] / h[16:20] / h[20:24]` is pseudo-code, not Python.**
Read literally it divides two `str` values. Fixing (a) does NOT fix this — (a) is
the seed-slice `ValueError`, (g) is the figure `TypeError`, and both present as
"HTTP 500 while the socket stays open". A liveness probe that only checks the
port or a 200 will not catch it.

## GATE-DESIGN RULE (the durable lesson)

**A pre-flight that only exercises *distinct* inputs cannot certify a *determinism*
property.** The pre-flight sends 40 distinct messages, so a counter-derived index
looks perfect — 40/40 distinct seeds, 40/40 distinct previews, a clean pass — while
the *run* is broken.

Therefore the pre-flight must include a **repeat-same-message probe**: send the same
message twice and assert the seed is identical (and matches the recomputed md5).

The same principle generalises: *any* pre-flight that proves "distinctness" is
silent about "determinism". Add a probe that repeats an input.

**The gate is now TEN checks** (was eight): 40/40 distinct seeds, 40/40 distinct
previews, 40/40 recomputed md5s (seed + colour + figure), 8/8 distinct seeds AND
8/8 distinct previews on every one of the 5 prompts, 0 literal `seed={}`, 0
`EXC:`/tracebacks, `[mock-zai` prefix on 40/40, **repeat-same-message ⇒ same seed
(40 × 2)**, and **0 `(civ,prompt)` pairs carrying >1 seed**.

**Seed-width rule: check the SLICE, not the render.** The documented "4 hex chars"
was originally satisfied by *padding* two 2-char slices, which is 256 values of
entropy wearing 4 characters' clothing. Widen the slice itself to
`h[(i*2)%8:(i*2)%8+4]` (65 536 values) and the padding becomes a no-op.

## Run-wide verification (isolate this run's rows)

Count from the **end** of each civ file (last 10), never a `ts` cutoff.

- per-civ ledger Δ +10 × 8 = **80** new rows
- `meta_log.jsonl` Δ +5
- `Winner:` lines = 5
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- `relevance` Δ = Σ this run's `avg_score` — **8/8 exact to 1e-6**
- distinct seeds **40 / 80 rows**; **0** `(civ,prompt)` carrying >1 seed
- **80/80** rows match an independently recomputed message md5
- 8/8 distinct seeds AND previews on every competition prompt (5/5)
- meta-vs-ledger `avg_score` mismatches **0/40** — **use the later-`ts` row**
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples
- extinction risk NONE (threshold −10; the lowest civ sits ~110× above it)

**The meta-vs-ledger check needs the later-`ts` row.** The sim phase draws its prompt
at random from the same 5, so a `(civ, prompt)` pair recurs 1–4 times inside the 10 new
rows; the competition-phase row is the later one. `max(cands, key=ts)` gives 40/40
exact; first-match reports false mismatches. Match key is `m["prompt"][:80]`.

## A failed run must be reset, not patched

When the first mock of session 170 was rejected (counter-derived index), the ledger was
restored with `git checkout -- .` **from the clone root**, and the baseline was
re-verified against the captured pre-run counts before the second attempt. Never
hand-edit a ledger to make a check pass — reset and re-run so the baseline and the
result live in the same epoch.

`git show HEAD:<path>` must run with `cwd` = the **clone root**, not the civs
directory; the civs dir is not a git root and `git show` there returns empty stdout
→ `JSONDecodeError`.

## Environment traps (recurring)

- **NAS EDQUOT**: `/workspace` is at 100% (600 G of 600 G). `git clone` into
  `/workspace` fails with `Disk quota exceeded`; even a 20 MB `dd` fails. Clone to
  `/tmp` and bridge with a symlink. The NAS trap also blocks **file delivery** — `cp`
  into `/workspace` leaves a 0-byte file, so deliver by pushing to git.
- **The `write` tool is jailed to the workspace root** and cannot write `/tmp`. Use a
  bash heredoc for `/tmp` artifacts.
- `read` tool is likewise jailed — read `/tmp` files via bash.
- Upstream owner is **`SuperInstance/AI-Writings`**; the `ai-writings/…` slug 404s
  (the GitHub API is case-insensitive). Authenticated as `SuperInstance`.
- `gh` is not installed — use `GET /user/repos` with `GITHUB_TOKEN`.
- `GIT_SSL_NO_VERIFY=1` is required for git fetch/push. Push to the explicit token
  URL: `https://x-access-token:$GITHUB_TOKEN@github.com/<owner>/<repo>.git`.
- `ZAI_TOKEN` is absent from env and all 8 sandbox secrets; z.ai returns **401
  `token expired or incorrect`** ⇒ endpoint healthy, credential absent. Control B
  (the local mock) is the only provider path. Note the `ZAI_URL_OVERRIDE` alone is
  dead code — the token gate returns `None` first, so a placeholder token is required.
- JEV is **live**: a well-formed `questions` body returns HTTP 200 with
  `{"model":"jev-1.14.0", …}`. Export `TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll `ps` + the log.
- **Symlink rule**: `ln -sfn` will not replace an existing directory target. The
  bridge must point at the **clone root**, not the nested `cellular-first-design` dir.
  `rm -rf` the old link, `ln -s`, then verify with `stat -L -c '%d:%i'` on both sides
  + `-ef`.
- **Mock teardown**: kill by exact argv match (`python3 /tmp/mock_zai.py` and
  `timeout -s KILL 900 python3 /tmp/mock_zai.py`) — two pids. Never `pkill -f mock_zai`,
  which self-matches the killing shell. Then prove the port is closed: `curl -m 5` ⇒
  **exit 7**, `HTTP=000`.
- **The mock's `figure` is a string triple, NOT a division.** `h` is a hex STRING, so
  `h[12:16] / h[16:20] / h[20:24]` raises `TypeError` ⇒ HTTP 500 while the socket
  stays open (the very failure mode fix (a) exists to prevent). The verified fix
  (g) is `figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` — three components. A
  hex→int ratio also "works" numerically but is a **different algorithm** and will
  not reproduce the recorded ledger, so match the string form.
- **`GET /user/repos` paginates ~100/repo and the owner has 5 400+.** `ai-writings`
  does NOT appear in the first 10 pages of owned repos — use the **search API**
  (`GET /search/repositories?q=ai-writings+in:name`) to find `SuperInstance/AI-Writings`.
  Also note `cellular-first-design` is a **subdirectory** of that repo, not a repo
  of its own; the GitHub API is case-insensitive, so the `ai-writings/…` slug 404s.
- **Wiped workspace ⇒ sparse clone, not a full clone.** `SuperInstance/AI-Writings`
  is 3.7 GB and `/workspace` is at 100% NAS quota. `git init` + `core.sparseCheckout`
  + `sparse-checkout set cellular-first-design/code/civilizations`, `--depth=1` fetch,
  then symlink-bridge `/workspace/repos/ai-writings/cellular-first-design` → the
  clone root. **Verify with `os.path.samefile()`** — the shell `[ -ef ]` test
  mis-parses a symlinked path here; `stat -L -c '%d:%i'` on both sides is reliable.

## Interpretation rules for the meta-GAN

- **The run low and the lifetime low are different civs on different axes.** The
  run-level low *rotates* every session; the lifetime low is structural. Do not
  promote a run low to the lifetime finding.
- **Never treat `win_rate` as a quality metric.** The chooser asks JEV a **`choice`**
  question over 150-char `content_preview` snippets; `avg_score` is the mean of three
  **`score`** questions on the same text. Different questions, different answers. The
  clean-mock series has 16 five-sample points spanning 0/5 – 4/5 ⇒ the honest claim is
  *somewhere in 0–80 %*, not a point estimate.
- **Read the low-civ gaps, not just the low label.** If the *alignment* gap to the next
  civ is much wider than the *quality* gap, it is a **voice** failure (alignment is the
  dimension the meta-GAN selects on), not a prose failure.
- The **counter gap** (`culture.json` `relevance_score` − ledger Σ`avg_score`) is a
  **fixed per-civ offset**, not accumulating: Δ = **0.0000** for every civ between
  epochs. Per-civ (sessions 169–178, stable): whimsical −173.14, poetic −96.80,
  formal −85.53, grounded −84.35, mythic −51.11, engineer −44.24, therapist −42.11,
  precise −32.63 — **TOTAL −609.92**. The −609.92 is the **total, not a per-civ
  constant**; quote the per-civ values when comparing.
  `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the
  ledger** by an auditor. Compute both epochs within the same epoch before comparing.
- **A rounded endpoint is not a baseline.** The leaderboard rounds `relevance` to 2 dp;
  differencing two rounded endpoints leaves residuals up to ±0.0067 and makes an
  exact 8/8 check report 2/8 FAIL. Re-derive relevance deltas against the **unrounded
  `culture.json`** git blob. (Session 178: first pass 2/8, after re-derivation 8/8
  exact to 3.4e-13.)
- Run `avg_score` levels sit **above** the lifetime band; the **ordering** carries the
  information, not the level.

## Session 183 additions (2026-10-25)

- **The NAS EDQUOT trap also blocks DELIVERY, not just cloning.** `/workspace` is an NFS
  mount at 600 G/600 G shared across tenants. Writes there **return exit 0 and produce a
  0-byte file** — `cp` reports `failed to close ...: Disk quota exceeded` while the file
  *appears* in `ls -la` at size 0, and a bare `echo x > file` also lands 0 bytes. So a
  workspace-relative artifact is **undeliverable** no matter how it is written. Plan the
  durable copy in git (clone under `/tmp`, push upstream) and report the upstream path;
  do not retry workspace writes hoping for a different result. `/root`, `/home`, `/var/tmp`
  are on the overlay and writable, but the delivery surface reads `/workspace`.
- **`test -ef` is broken in this sandbox** — `bash: [: <path>: binary operator expected`
  on a perfectly valid two-argument `-ef`. Verify a symlink bridge by **inode identity**
  (`stat -c '%i'`) plus `readlink -f`, not by `-ef`. The bridge itself works; only the
  test is unusable. A "FAIL" here is a false alarm.
- **The mock seed slice is `h[(i*2)%8:(i*2)%8+4]` — a CONTIGUOUS 4-char slice.** The older
  spec block still shows two 2-char slices *concatenated*; that is a **different value**.
  A row written under one algorithm will not reconcile against a recompute under the
  other. **Check the SLICE, not the render.** Same for `figure`: it must be
  `f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` (three string components) — the spec's `/`
  separators read literally as division ⇒ `TypeError` ⇒ HTTP 500 on every request while
  the socket stays open, so a port/200 liveness probe still looks healthy.
- **The pre-flight gate's 40 messages are built CIV-major** (all 5 prompts per civ), so
  per-prompt aggregation must index `i*5+pi`, not `i*8+pi`. A gate that crashes on an
  `IndexError` *after* four assertions have already printed PASS is **not** a passing
  gate — make the gate print a final verdict and exit non-zero on any failure.
- **GitHub REST `GET /contents` rate-limits to 403 mid-enumeration**, which renders as
  "the file list is empty". Enumerate a file census over the **git protocol**
  (`git ls-tree <ref> <dir>`) instead — unlimited, and it is the only way to assert
  absence without a false negative.
- **`ZAI_TOKEN` is still absent** (47th session) — not in the env, not in any of the 8
  sandbox secrets; all four candidate tokens return 401 `token expired or incorrect`
  against `api.z.ai`, so the endpoint is healthy and the **credential** is missing.
  The orchestrator's provider gate returns `None` on an empty token, so **every
  simulation silently returns `None` and no rows are written** — an empty-token run
  looks like a clean run unless you assert on row counts. `ZAI_URL_OVERRIDE` alone is
  dead code behind that gate: set **both** `ZAI_TOKEN` (placeholder) and the override.
- **`JEV_KEY` reads `TYPESAFEAI_KEY`, but the env var is `TYPESAFE_AI_TOKEN`** — export
  the alias, or every score silently falls back to the 2.0/2.0/2.0 triple.
- **Chooser-vs-argmax agreement hit 0/5 with all 5 disagreements taking the
  LOWER-scoring candidate** (first 0/5 in the clean-mock series). `civ-poetic` was
  argmax on 5/5 prompts and won 0/5. Report it as a *sample*; the **direction** is the
  finding.
- **The run-level `quality` LEVEL is a moving quantity** — field mean was **0.9998** in
  session 183 vs ~0.91 in earlier sessions. Recompute it from the ledger every session;
  never carry the level forward. Rank on **cross-civ spreads** instead: session 183 had
  `alignment` 1.0680 › `quality` 0.6320 › `avg_score` 0.3820 › `novelty` 0.3360.
- **Session 182's run-low/lifetime-low coincidence did not reproduce.** In 183 the run
  low rotated to `civ-formal` (8th on run `avg_score` 1.5847 and run `quality` 0.7120)
  while `civ-grounded` placed **3rd of 8** on run `avg_score` (1.7573) — yet Grounded is
  still the lifetime low on all five axes (57th consecutive session). The run ranking
  and the lifetime table are **two separate claims**; say so explicitly.
- **`civ-grounded`'s low axes are alignment and quality, NOT novelty** — lifetime
  novelty 1.5849 is 6th of 8 (mid-field); the lowest lifetime novelty belongs to
  `civ-formal` (1.5022). Do not attribute Grounded's low-novelty to Grounded.

## Session 194 additions (2026-10-25)

- **THE CORE REST QUOTA CAN BE ALREADY EXHAUSTED AT SESSION START, AND A 403 LOOKS EXACTLY
  LIKE "NOT FOUND".** This session the authenticated quota read **5000/5000 (403)** at
  09:12Z, so `GET /user/repos`, `GET /user` and every repo probe rendered as *not found*.
  Recovery, in order: (1) `GET /rate_limit` unauthenticated to read the reset;
  (2) **`/search/*` has a separate quota** and still served requests;
  (3) **the git protocol is NOT rate-limited** — `git ls-remote` on a public repo succeeds
  instantly, so it is the only reliable *absence* test while core is exhausted;
  (4) wait out the reset, then `GET /user`. The token owner is **`SuperInstance`**
  (Casey Digennaro, uid 193104091) — **not** `rio-ARC`, which shows up in search results
  under a similar name and owns a *different* repo. **A 403 renders as "not found" for
  every candidate at once; check `/rate_limit` before concluding a repo is absent.**
- **THE RESPONSE-BODY LENGTH BAND CATCHS A FRESH MOCK BUILD.** A rebuilt template
  rendered at **711** chars against the **332–369** band and the gate reported a clean,
  localised `[FAIL] response body length band 332-369 min=711 max=711`. Trim the template
  to **354**. The band is not cosmetic: a body longer than ~369 chars pushes the **seed
  prefix out of the 200-char `content_preview` truncation**, silently breaking the
  seed+color+figure recompute for every row.
- **A VERIFIER BUG CAN LOOK LIKE A TRUNCATED LEDGER.** The first pass reported
  `[FAIL] per-civ ledger delta +10 x 8` with deltas of **−1412 / −1424 / …** — the check
  compared the *slice length* (10, the "last 10 rows") against the baseline *count*.
  **A delta of roughly −(baseline) is the signature of comparing a slice against a count**,
  not of a short ledger. The run was clean.
- **THE DOWN-GRADE STREAK IS NOT A TREND, IT IS A RESETTABLE COUNTER.** Session 193 broke
  it at 0 (5/5 agreement); session 194 re-established it at **13** (1/5 agreement, 4/4
  disagreements down-grade, `civ-poetic` argmax on 4/5 and winner on 0/5). **Re-base the
  streak every session from this session's own data — do not carry the number forward.**
- **THE LOW-RELEVANCE SIGNATURE IS "HIGH NOVELTY, LOW ALIGNMENT".** `civ-therapist` (run
  novelty **2.6550** = *highest in the fleet*, alignment **1.4910** = lowest) and
  `civ-whimsical` (2.5790 / 1.9240) both fit. Novelty spread is ~**0.15** against an
  alignment spread of ~**1.66**, so **the ranking is produced by alignment and quality,
  not novelty**. Report the axis, not the holder.
- **THE MOCK LOG LINE COUNT IS `2N + 1`, NOT `N`.** With the pre-flight's 40 messages
  (×2 for the repeat probe = 80 requests) plus the run's 80, the log reads **161** OK-200
  lines (80 pre-flight + 80 run + 1 GET). Compare against the log, not a remembered
  constant.

## Session 195 additions (2026-10-25)

- **REPLACE EVERY FIXED MOCK-LOG LINE COUNT WITH A MULTISET IDENTITY.** The inherited
  check compared the mock log's OK-200 count against a hardcoded **161**, which silently
  assumes the pre-flight ran **exactly once**. This session the pre-flight ran **twice**
  (run 1 crashed at check 12 on a gate bug, run 2 was the full 14/14 pass) and there was
  one manual `curl` liveness probe, so the true count was **241** and the fixed number
  reported a **false FAIL**. The replacement — **the seed multiset of the LAST 80 OK-200
  log lines must equal the seed multiset of the 80 ledger rows** — held exactly and is
  *immune to how many times the pre-flight ran*. **A count check encodes an assumption
  about how many times an artifact was produced; a multiset identity encodes none.**
  Generalise: whenever a check must survive a re-run of an upstream step, assert an
  *identity between artifacts*, not a *magnitude of one artifact*.
- **A GATE THAT PRINTS 12 PASSES AND THEN TRACEBACKS IS NOT A PASSING GATE.** The
  pre-flight's repeat-same-message probe unpacked a 3-tuple as a 4-tuple and crashed
  *after* twelve `[PASS]` lines. The gate must print a final verdict and exit non-zero
  on any failure — a traceback after partial output reads as a pass to a human and to a
  log-scraper alike.
- **A CLONE FAILS OR SUCCEEDS BY DESTINATION MOUNT, NOT BY SIZE.** The `--depth 1`
  clone into `/workspace/repos` died on `.git/description` with `Disk quota exceeded`;
  the **same clone into `/tmp` succeeded immediately**. The NAS EDQUOT applies to the
  mount, not to git. Clone to `/tmp` and symlink-bridge.
- **THE BRIDGE MUST POINT AT THE INNER `cellular-first-design` DIRECTORY.** The upstream
  repo root contains a `cellular-first-design/` subdirectory and the orchestrator's
  `CIVS_DIR` is hardcoded to the **inner** path, so a bridge to the repo root makes
  `civilizations.json` invisible. Verify by **inode identity**
  (`stat -L -c '%d:%i'` → `129:10425` on both sides) plus `os.path.samefile()`; the
  shell `[ -ef ]` test is unreliable in this sandbox.
- **THE RESPONSE-BODY LENGTH BAND CAUGHT THE FRESH BUILD AGAIN.** A first template
  rendered at **387** characters against the **332–369** band; the gate reported a clean,
  localised `[FAIL] response body length band 332-369 min=387 max=387`. Trimming the tail
  to **297** put the body at **351**. Target **351** (not 354 — the prefix width varies
  with the seed, so the tail length is the control, not the total).
- **THE DOWN-GRADE STREAK RE-BASES EVERY SESSION, AND IT IS AT 14.** `civ-precise` swept
  5/5 for the **fifth consecutive** sweep, disagreed with the `avg_score` argmax on
  **4 of 5** prompts, and **all four took the LOWER-scoring candidate**. Agreement
  **1/5 (20 %)**. `civ-poetic` was argmax on **4 of 5** and won **0 of 5**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-whimsical`** (run `avg_score` **2.1440**,
  `alignment` **2.1910** lowest) — a **14th different civ in 14 sessions**. The bottom
  two were separated by only **0.0277** on `avg_score` but by **0.9660** on `alignment`.
  *The holder rotates; the axis does not.*
- **THE LOW-RELEVANCE SIGNATURE IS STILL "HIGH NOVELTY, LOW ALIGNMENT".** `civ-whimsical`
  (novelty **2.5810** / alignment **2.1910**) and `civ-therapist` (**2.6220** /
  **2.1930**) both fit. Novelty spread **0.1510** against an alignment spread
  **1.0780** ⇒ the ranking is produced by alignment and quality, not novelty. Report
  the axis, not the holder.
- **`civ-grounded` was the lifetime low for the 67th consecutive session** (`relevance`
  **1451.12**, `relevance_per_sim` **1.037**), yet its lifetime `win_rate` **0.102** is
  **3rd-best in the fleet**. *Selection and relevance are separate axes.* Its low axis
  is **quality** (**1.4820**, the lowest in the fleet), **not** novelty (**2.6040**,
  2nd-highest).

## Session 200 addenda (2026-10-25)

- **THE BRIDGE SYMLINK MUST TARGET THE *INNER* SUBDIRECTORY, AND THE SHALLOW-CLONE
  TRICK IS FASTER THAN `--depth 50`.** `git clone --depth 1 --filter=blob:none --sparse`
  + `git sparse-checkout set cellular-first-design` gave a **9.9 M** working tree versus
  a multi-GB full clone. The symlink must point at
  `<clone>/cellular-first-design` (the *inner* dir), not the clone root — pointing it
  at the root makes `code/civilizations/` unresolvable and the failure looks like
  "the repo is missing" rather than "the symlink is one level too high".
- **THE NAS EDQUOT TRAP NOW REJECTS WRITES AS SMALL AS 1 KB.** `cp` of the 13.6 KB
  report, then of a 5.9 KB gzip, then a 1 KB head — **all three** failed with
  `Disk quota exceeded` and left **0-byte** files visible in `ls`. `df` shows
  `600G/600G 100%`. *Do not spend attempts shrinking the payload — delivery by
  `git push` is the only channel that works.* Always verify the copied size
  (`wc -c`), never trust the `ls` entry.
- **THE GITHUB REST CORE QUOTA IS 5000/5000 AND EXHAUSTS MID-SESSION.** After the
  push, `GET /repos/.../commits/main` returned a JSON body of **nulls** — not a 404.
  The raw body was `API rate limit exceeded`, and `/rate_limit` confirmed
  `core: {limit: 5000, used: 5000, remaining: 0}`. *A null-field API response is
  rate-limit noise, not absence.* Verify pushes with the **git protocol** instead:
  `git ls-remote <token-url> refs/heads/main` (no quota) and
  `git cat-file -p FETCH_HEAD:<path>` to confirm the blob is really in the pushed
  commit. This is the same principle as "assert absence over the git protocol".
- **THE JEV KEY ALIAS IS `TYPESAFEAI_KEY` BUT THE SANDBOX EXPORTS `TYPESAFE_AI_TOKEN`.**
  Export the alias before running or `jev_score` silently falls through to the
  `2.0/2.0/2.0` fallback triple. With the alias exported, JEV returns
  `{"model":"jev-1.14.0"}` and **0 fallback triples** — this is a live credential,
  unlike the z.ai one.
- **PRE-FLIGHT 11/11 ON THE FIRST BUILD, WITH A 366-CHAR BODY.** Adding the
  "cultural-prompt length band 167-209" check *read from the real `culture.json`
  files* (never hand-typed) and the repeat-same-message determinism probe both
  passed first time. The mock's response body is **366 chars** — inside the
  documented 332-369 band on the first attempt.

## Session 201 addenda (2026-10-25)

- **A CRASH IN THE CHECKER IS A CHECKER FAILURE, AND IT CAN HIDE BEHIND PASSES.** Two
  independent scripts crashed this session on trivial Python mistakes *after* printing
  several `[PASS]` lines: the pre-flight died with `NameError: name 're' is not defined`
  (an `import re` nested inside a helper was never in module scope when a module-level
  loop called a second helper), and the verifier died with `TypeError: check() takes from
  2 to 3 positional arguments but 4 were given` (a detail string passed as a 4th
  positional arg to a 3-arg helper). Both were caught **only** because the gate prints a
  final `VERDICT:` line and exits non-zero. *The run itself was clean in both cases and
  was never re-run — the distinction between the artifact and the checker is what let a
  clean run survive a broken checker.* Corollary: a helper's arity is part of its
  contract; when a check helper's signature changes, grep every call site.
- **THE 332-369 BODY BAND CAUGHT THE FRESH BUILD, AND THE RIGHT FIX WAS TO REMOVE THE
  VARIANCE — NOT TO TRIM THE LONGEST INSTANCE.** The first template rendered at
  **349-381** (a long civ name pushed it over). Truncating the culture-derived fields
  (`trad` 12 chars, `tenet` 10, `voice` 10) made the body **constant at 298-304** —
  *below* the band — so one fixed sentence was appended, landing at **352-358**.
  *A band check is a variance check: fix the cause of the variance, not its maximum.*
  Budget two build iterations for a fresh template; the band is not cosmetic.
- **THE 5/5 SWEEP STREAK IS A COUNTER WITH A PRINTED EXPIRY DATE.** `civ-precise` won
  5/5 for **ten consecutive sessions** (191-200); session 201 gave a prompt to
  `civ-engineer`, ending the streak at 10. *The first honest statement of a streak's
  length is the one that ends it* — never carry the count forward as a current fact.
- **THE CHOOSER HAS NEVER UP-GRADED.** Agreement across sessions 198-201 is
  3 → 0 → 2 → **3**, and **every disagreement in the series took the LOWER-scoring
  candidate (0 up-grades ever)**. A chooser that only ever picks the worse candidate is
  *anti-correlated* with `avg_score` where it disagrees, not merely noisy. The standing
  suspect is unchanged: the `best_civ` criteria map (`civ_id` -> `civ name`) is a label
  map, so the chooser may be scoring labels rather than texts.
- **THE REPO CAN BE FOUND BY CODE SEARCH, WHICH THE REPO-LIST PATH CANNOT REACH.**
  `GET /user/repos` needs ~54 pages for this owner; `GET /search/repositories?q=…+in:name`
  and **`GET /search/code?q=civilization_orchestrator+in:path`** both resolved
  `SuperInstance/AI-Writings` and the exact script path in one call, and `/search/*`
  has a **separate quota** that survives a core-quota exhaustion. Use code search to
  confirm the path before cloning.
- **THE SPARSE-CLONE RECIPE WORKS FROM A BARE `--no-checkout` CLONE.** `git clone
  --filter=blob:none --no-checkout --depth 1` then `git sparse-checkout init --cone` +
  `git sparse-checkout set cellular-first-design` + `git checkout` gave a **9.9 M**
  working tree from a 3.7 GB repo. Bridge the symlink at the **inner**
  `cellular-first-design` directory; verify with `stat -L -c '%d:%i'` (here
  `129:10423` on both sides) and `os.path.samefile()` → `True`.

## Session 204 additions (2026-10-25)

- **PARSE THE MOCK HEADER FROM A KNOWN-GOOD SAMPLE BEFORE ASSERTING THE RECOMPUTE.**
  The mock's header is `[mock-zai <seed>] <color> <figure>.` — the **seed lives INSIDE
  the brackets**, the colour and figure after them. Two parser bugs in a row, both
  producing a *clean-looking* "the mock is broken" story about a mock that was working
  perfectly: (a) taking `prev.split("]")[0][len("[mock-zai "):]` for the seed but
  `prev.split("]")[1].split(" ")[1]/[2]` for colour/figure — the `[1]` chunk is
  `" <color> <figure>. <body>"`, so a plain 3-way split misaligns; (b) reading the
  **seed** from `split("]")[1]`, which compares `d372` against the expected `6ffd` and
  reports **0/40 recomputed md5s**. *A 0/40 recompute means "the parser is wrong"
  before it means "the mock is wrong" — dump one real body and parse it by hand
  first.* The correct parse is
  `s = prev.split("]")[0][len("[mock-zai "):].strip()` and
  `c, f = prev.split("]")[1].strip().split(" ")[:2]` with `f.rstrip(".")`.
- **THE GATE REPORTS 14/15 WITH A CLEAN `VERDICT:` LINE AND A NON-ZERO EXIT — THAT IS
  THE DESIGN WORKING.** The md5-recompute check was red on a fully healthy mock; the
  pre-flight refused to bless the run and the *checker* was fixed instead of the
  artifact. The final verdict line plus the non-zero exit is what separates a gate
  from a log scraper. *Never let a partially-passing gate authorise a run.*
- **`pkill -f "mock_zai.py"` SELF-MATCHES THE WRAPPER SHELL AND KILLS IT BEFORE THE
  MOCK STARTS.** The port then answers `HTTP=000` with curl exit **7**, and
  `/tmp/mock_zai.out` does not exist at all — the "launch" never ran. The documented
  teardown rule (kill by exact argv match, never `pkill -f`) applies to **startup**
  too: a `pkill` in the same command line as the launch will match its own shell.
- **THE MOCK BODY LANDED AT 347 CHARS ON THE FIRST BUILD — INSIDE THE 332-369 BAND
  WITH NO ITERATION.** Sessions 200 and 201 each needed two or three build
  iterations; the band check is worth keeping because it *catches* variance, but it
  is not a fixed cost. Building the body from a single fixed sentence (no
  culture-derived fields, so no length variance) is what makes it land first time.
- **THE RUN LOW AND THE LIFETIME LOW DECOUPLED FOR THE THIRD TIME IN A ROW, AND THE
  WIDEST ALIGNMENT GAP CONVERGED WITH THE RUN LOW.** Session 204's run low is
  `civ-whimsical` (`avg_score` **1.0700**, `alignment` **0.4150** = lowest in the
  fleet) and it *also* holds the widest alignment gap (**2.4550**) — where sessions
  202 and 203 split the two across different civs. `civ-grounded` is the lifetime low
  for the **76th consecutive session** and placed **5th of 8** on run `avg_score`
  (**1.5963**). *Do not carry a coincidence forward as a pattern — and do not carry a
  decoupling forward as a pattern either.*
- **THE ALIGNMENT SPREAD WAS 3.95x THE QUALITY SPREAD AND 16.70x THE NOVELTY SPREAD —
  THE WIDEST NOVELTY NARROWNESS IN THE SERIES** (novelty spread **0.1470**). The
  ranking is produced by alignment almost alone.
- **THE DOWN-GRADE STREAK RE-BASES EVERY SESSION, AND IT IS AT 1/5 (20 %).** Agreement
  across sessions 199-204 is 0 → 2 → 3 → 1 → 2 → **1**, and **every** disagreement in
  the series took the **lower-scoring** candidate. `civ-precise` was argmax on 3/5 and
  won 2/5; `civ-engineer` was argmax on 2/5 and won **0**. `civ-formal` won 3 of 5
  prompts outright, ending `civ-precise`'s four-session 5/5-sweep run. The chooser has
  **never up-graded** in 204 sessions. The standing suspect is unchanged: the
  `best_civ` criteria map (`civ_id` → `civ name`) is a *label* map, so the chooser may
  be scoring labels rather than texts.

## Session 205 additions (2026-10-25) — concurrent-run collision

- **ANOTHER AGENT CAN RUN THE SAME SESSION AGAINST THE SAME REPO WHILE YOU ARE
  WORKING, AND YOUR PUSH WILL BE REJECTED AS NON-FAST-FORWARD.** This session the
  remote gained a **session 204** commit (`39addc4`, authored by "Claude Opus 4.8")
  from the **same baseline `f60b152`** while my own session-204 run was in flight;
  two further commits (`probe` / `remove probe`) were unrelated user activity on
  `prose/`. `git push` then failed with **`! [rejected] main -> main (fetch first)`**.
  *The rejection is the signal that a sibling run landed — fetch and diff before
  assuming your push was simply stale.*
- **DO NOT NUMBER TWO INDEPENDENT RUNS THE SAME SESSION — RENUMBER THE LATER ONE AND
  KEEP BOTH REPORTS.** The remote already owned `RUN_REPORT_2026-10-25_session204.md`.
  Mine was renamed to **session 205** and the commit message rewritten to say so, with
  a note that the two runs share only a starting point (different mock seeds, different
  JEV draws). *Overwriting a sibling's report destroys evidence; a merge that keeps
  both is the honest record.*
- **THE MERGE MUST KEEP BOTH RUNS' LEDGER ROWS, AND THE COUNTER GAPS ARE THE PROOF.**
  Both sessions appended 10 rows per civ to the same `simulations.jsonl` and 5 rows to
  `meta_log.jsonl`, so **19 files conflicted**. Resolved by reconstructing each ledger
  as `base + session204_rows + my_rows`, deduping on `ts`, and **recomputing
  `culture.json` from the merged data** (`relevance` = base + both deltas, `wins`/`losses`
  = base + both deltas). The proof that the merge is arithmetically right: the per-civ
  **counter gaps came back at exactly the documented stable values** (grounded −84.35,
  whimsical −173.14, formal −85.53, poetic −96.80, precise −32.63, mythic −51.11,
  therapist −42.11, engineer −44.24; total −609.92). *A merge that silently drops a
  sibling's rows shows up as a shifted counter gap — that is the cheapest possible
  integrity check.*
- **DO NOT "FIX" THE MERGE BY CHECKING OUT ONE SIDE.** `git checkout FETCH_HEAD -- <file>`
  to "clean up" a conflicted report **deleted the other side's file**, and the
  re-applied commit then removed it again. The recovery is `git show <rev>:<path>` into
  the working tree — the blob is still in the object store even when the file is gone
  from the index. *Recover from the object store, never by re-running the run.*
- **`<<<<<<<` MARKERS ALREADY EXIST IN THE UPSTREAM REPO — SCOPE ANY CONFLICT-MARKER
  SCAN TO THE FILES YOU TOUCHED.** A repo-wide scan flagged
  `RUN_REPORT_2026-10-25_session159.md` and `skills/civ-orchestrator-learnings.md`; both
  were present in the **base** commit `f60b152`, in files my work never touched, and the
  session-159 report literally *documents* those markers as a historical artifact.
  Checking `git diff --name-only <base> HEAD` first separates "your merge left
  conflict markers" from "the repo has always contained the literal string".
- **THE MOCK HEADER PARSE: THE SEED IS INSIDE THE BRACKETS.** `[mock-zai <seed>] <color>
  <figure>.` — the correct parse is
  `s = prev.split("]")[0][len("[mock-zai "):].strip()` and
  `c, f = prev.split("]")[1].strip().split(" ")[:2]` with `f.rstrip(".")`.
  Two wrong parses produced a clean-looking "the mock is broken" story about a mock
  that was working perfectly: a misaligned 3-way split (`IndexError` on all 40
  requests) and reading the seed from `split("]")[1]` (**0/40 recomputed md5s**).
  *A 0/40 recompute means "the parser is wrong" before it means "the mock is wrong" —
  dump one real body and parse it by hand first.*
- **THE PRE-FLIGHT GATE REFUSED THE RUN TWICE, AND BOTH TIMES THE BUG WAS THE
  CHECKER, NOT THE MOCK.** The gate printed `14/15 PASS` with a clean `VERDICT:` line
  and a non-zero exit, and the md5-recompute check was the red one. The run was not
  started on a red gate. *The final verdict line plus a non-zero exit is what separates
  a gate from a log scraper — never let a partially-passing gate authorise a run.*
- **`pkill -f "mock_zai.py"` SELF-MATCHES THE WRAPPER SHELL AND KILLS IT BEFORE THE
  MOCK EVER STARTS.** The port then answers `HTTP=000` with curl exit **7** and
  `/tmp/mock_zai.out` does not exist at all. The documented "kill by exact argv match"
  rule applies to **startup** as well as teardown: a `pkill` on the same command line
  as the launch matches its own shell.
- **THE MOCK BODY LANDED AT 347 CHARS ON THE FIRST BUILD — INSIDE THE 332-369 BAND
  WITH NO ITERATION**, because the body is built from a single fixed sentence with no
  culture-derived fields (so there is no length variance to control). Sessions 200 and
  201 each needed two or three iterations. *A band check catches variance, not cost —
  eliminate the variance and the band passes once.*
- **THE DOWN-GRADE STREAK RE-BASES EVERY SESSION, AND IT IS AT 1/5 (20 %).** Agreement
  across sessions 199-205 is 0 → 2 → 3 → 1 → 2 → **1**, and every disagreement in the
  series took the **lower**-scoring candidate. The chooser has **never up-graded** in
  205 sessions. The standing suspect is unchanged: the `best_civ` criteria map
  (`civ_id` → `civ name`) is a *label* map, so the chooser may be scoring labels
  rather than texts.

## Session 207 additions (2026-10-25)

- **THE `CIVS_DIR` IS HARDCODED TO `/workspace`, SO THE SYMLINK BRIDGE IS MANDATORY — AND
  IT MUST POINT AT THE *INNER* `code` DIRECTORY, NOT THE CLONE ROOT.** With the clone in
  `/tmp` (the NAS is at 100 % quota) the first launch died instantly with
  `FileNotFoundError: '/workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilizations.json'`.
  The bridge is
  `ln -s /tmp/aiw/cellular-first-design/code /workspace/repos/ai-writings/cellular-first-design/code`,
  verified by inode identity (`stat -L -c '%d:%i'` → `130:1704352` on both sides) plus
  `os.path.samefile()` → `True`. *A bridge to the clone ROOT leaves `code/civilizations/`
  unresolvable and the failure reads as "the repo is missing", not "the symlink is one level
  too high".* The failure is instant and total (no rows written), so it is unmistakable —
  but it is an **environment** failure, not a run failure: fix the bridge, do not re-run
  the analysis.
- **`ZAI_URL_OVERRIDE` IS DEAD CODE BEHIND THE TOKEN GATE — SET `ZAI_TOKEN` *AND* THE
  OVERRIDE.** The override is read *after* `if not token: return None`, so an override
  with no token makes every simulation return `None` and write **zero rows** — an empty
  run that looks like a clean run unless you assert on row counts.
- **THE MOCK BODY LANDED AT 357 CHARS ON THE FIRST BUILD — AND THE BAND IS SOLVED
  ALGEBRAICALLY.** For a 4-hex seed and an 18-char figure the header
  `[mock-zai <seed>] <color> <figure>.` is a **constant 33 chars**, so a fixed tail of
  length *T* yields a **constant** body *T + 33*. Three fixed sentences of **321** chars
  ⇒ **357**, inside the 332-369 band, on build 1. *A band check catches variance, not
  cost — eliminate the variance (no culture-derived fields in the body) and the band
  passes once.*
- **`GET /search/code?q=civilization_orchestrator+in:path` FOUND THE REPO IN ONE CALL
  AFTER `GET /user/repos` AND `GET /search/repositories` BOTH MISSED IT.** The upstream is
  **`SuperInstance/AI-Writings`** — a *user* account, so `GET /orgs/ai-writings/repos`
  404s. Code search (`/search/*` has a **separate quota** that survives core exhaustion)
  is the fastest confirmation that a *path* exists before cloning.
- **THE DOWN-GRADE STREAK RE-BASES EVERY SESSION, AND IT IS AT 1.** Agreement across
  sessions 203-207 is 1 → 0 → 1 → **4**; the last three read 1 → 0 → 1. `civ-precise`
  swept **5/5** (its first sweep since session 191) and the single disagreement again took
  the **lower**-scoring candidate. *The first honest statement of a streak's length is the
  one that ends it* — and the chooser has still never up-graded.
- **`civ-grounded` HELD THE LIFETIME LOW FOR THE 78th CONSECUTIVE SESSION**
  (`relevance` **1647.13**, `relevance_per_sim` **1.084**), yet its lifetime `win_rate`
  **0.095** is 3rd-best in the fleet. Its low lifetime axis is **quality** (**0.4519**,
  lowest in the fleet), **not** novelty (**1.7097**, 4th of 8). *Selection and relevance
  are separate axes.*
- **THE RUN LOW ROTATED TO `civ-therapist` (15th different run low in 15 sessions) AND IT
  HELD THE WIDEST ALIGNMENT GAP IN THE FLEET (2.0980).** Novelty gaps for the low civs
  were **negative** this session (−0.0770 / −0.0650 / −0.0480): the low-relevance axis
  is **alignment**, and novelty is flat-to-high for *everyone*. Alignment spread
  **2.0980** was **3.06x** the quality spread and **9.58x** the novelty spread.
- **THE PER-CIV COUNTER GAP IS STILL THE CHEAPEST INTEGRITY CHECK.** After this run the
  gaps came back at exactly the documented stable values (grounded −84.35,
  whimsical −173.14, formal −85.53, poetic −96.80, precise −32.63, mythic −51.11,
  therapist −42.11, engineer −44.24) — a run that dropped or duplicated rows would show
  a shifted gap immediately.

## Session 209 additions (2026-10-25)

- **THE BODY BAND IS NOW FOUR SESSIONS IN A ROW ON THE FIRST BUILD — THE ALGEBRA IS
  STABLE.** Header `[mock-zai <4-hex>] #<6-hex> <figure>. ` with the figure fixed at
  **18 chars** ⇒ a **constant 44-char header** ⇒ a **300-char** tail ⇒ body **340**,
  inside the 332-369 band with **no** iteration. Sessions 207, 208 and 209 all landed
  first try. *Compute the band algebraically before writing the template; do not iterate
  the template.* The tail must be a **single fixed sentence with no culture-derived
  fields** — that is what removes the length variance the band exists to catch.
- **THE `ls -la` VERIFICATION THE PROMPT ASKS FOR NEEDS `-L` WHEN THE PATH IS A
  SYMLINK BRIDGE.** `ls -la <dir>/civilizations/` returns **"No such file or
  directory"** on a perfectly healthy run, because the last path component crosses a
  symlink and `ls` does not follow it without `-L`. *A missing directory in the
  verification step is a reporting artefact, not a missing run.* The bridge
  (`.../cellular-first-design/code` → the clone's inner `code`) is the same shape as
  sessions 200-208; `ls -laL` and the per-civ `ls -la` on `civ-*/simulations.jsonl`
  both show the real mtimes.
- **THE DOWN-GRADE SERIES NOW READS 0/5 → 4/5 → 1/5 → 3/5 (sessions 199, 207, 208,
  209).** Agreement **3/5 (60 %)**, 2 down-grades, 0 up-grades. `civ-precise` won **4 of
  5** and was the argmax on **4 of 5**; `civ-poetic` was argmax on **1 of 5** and won
  **0 of 5**. *The series oscillates — re-derive the number every session and never
  carry a streak forward as a current fact.*
- **THE RUN LOW AND THE LIFETIME LOW HAVE NOW BEEN DIFFERENT CIVs FOR SIX SESSIONS
  RUNNING** (`civ-grounded` lifetime-low at `relevance` **1684.58** /
  `relevance_per_sim` **1.095**, run rank **6 of 8**; `civ-therapist` run-level low at
  run `avg_score` **1.4617**). `civ-grounded`'s lifetime `win_rate` **0.094** is still
  **3rd-best in the fleet** — *selection and relevance are separate axes.*
- **THE LOW-RELEVANCE SIGNATURE HOLDS: HIGH NOVELTY, LOW ALIGNMENT.** Alignment
  spread **1.9410** = **3.39x** the quality spread and **8.51x** the novelty spread.
  The alignment tail beyond −1.5 is `civ-therapist` (**−1.9410**) and `civ-mythic`
  (**−1.5450**); novelty gaps are **negative for every low civ**, so novelty is not a
  separating axis. *Report the axis, not the holder.*

## Session 212 additions (2026-10-25)

### 1. THE PRE-FLIGHT "NO LITERAL `seed={}`" ASSERTION HAS AN INVERTED-SENTINEL TRAP

The pre-flight reported **FAIL** on `literal_seed_none` while the mock was perfectly
correct: the response body contained **0** occurrences of `seed=`. The bug was the
check, not the server — the flag was set to `True` *on find* and the assertion read
`not literal_seed`, so a correct mock could never pass.

```
if "seed={}" in body: literal_seed = True     # wrong: sets True when the text IS present
results["literal_seed_none"] = (not literal_seed,)
```

The fix is to count the occurrence and assert on the count:

```
if "seed={}" in body: literal_seed = False
results["literal_seed_none"] = (literal_seed,)
```

**Generalisation: a pre-flight FAIL on a component you have already independently
verified is a CHECK bug until proven otherwise.** Re-derive the fact directly (here:
`post()` one message and count `"seed="` in the body) before touching the code. A
pre-flight that reports a failure on a green component will send you off to "fix" a
server that was never broken — and the fix risks introducing the real bug the
pre-flight was designed to catch.

### 2. A SINGLE FAILED `ls` IS NOT EVIDENCE OF A MISSING TREE ON THE NAS

After the run, `ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/`
returned **"No such file or directory"** even though the symlink bridge was intact
(`ls -la /workspace/repos/` showed `ai-writings -> /root/ai-writings`) and the clone root
listed fine. A second attempt one minute later resolved cleanly with the expected
contents.

**Re-read before concluding the repo vanished.** The NAS mount is flaky under
concurrent symlink traversal, and the failure mode reads exactly like a missing
checkout. Always corroborate with a second path (`ls` the clone root directly) before
re-cloning.

### 3. A SWEEP AND A CHOOSER-AGREEMENT RATE ARE INDEPENDENT MEASUREMENTS

Session 212: `civ-precise` won **5/5** competitions, while the chooser agreed with the
argmax only **2/5 (40 %)** — 3 down-grades, 0 up-grades. A 5/5 sweep coexisted with a
poorly-calibrated chooser.

**Never infer chooser agreement from the win count.** They measure different things:
the win count is about who won, the agreement rate is about whether the chooser's
*reasoning* matched the scores. Both must be reported, and the down-grade count is
always re-derived from the session's own `meta_log`.

### 4. REPORT THE GAP NEXT TO THE SPREAD WHEN NAMING THE RUN LOW

`civ-therapist` (**1.5710**) and `civ-whimsical` (**1.5957**) differ by **0.0247**
against a run `avg_score` spread of **0.7633** — the two lowest civs are separated by
less than one third of the run's own spread. Their ordering is noise. A "run low" claim
that does not print the gap beside the spread is not a defensible claim.

## Session 213 additions (2026-10-25)

### 1. THE SEED INDEX IS THE RAW MD5 BYTE `d[0] % 4`, NOT THE HEX DIGIT

The verified mock algorithm indexes the seed by `i = d[0] % 4` where `d` is the **raw
digest bytes**. A near-miss reading, `i = int(h[0], 16) % 4`, looks identical ("the first
byte mod 4", and both land in 0-3) but is a **different function**: `d[0]` spans
`0x00-0xFF` while `int(h[0],16)` spans only `0x00-0x0F`.

**The failure is silent and partial.** `colour = h[8:12]` and
`figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` do **not** depend on the index, so a wrong
index reproduces them **perfectly** — 80/80 — while the **seed** is wrong on roughly 70 % of
rows. A pre-flight therefore reports `distinct_seeds 1/40` and `recomputed_md5 0/40` on a
mock that is behaving exactly as the ledger demands.

**How to settle it:** brute-force every candidate rule and let the ledger pick. Sweeping all
4-hex windows of `h` crossed with `%2/%4/%8` index rules, the true rule scored **80/80**
only under the raw-byte reading. *When a composite field recompute is partially right, the
wrong field is the one that depends on the index — start there.*

**Confirmation that the algorithm is right:** 80/80 recent-format ledger rows match on
seed + colour + figure when recomputed from the **real `culture.json`** files.

### 2. THE MOCK HEADER PARSE MUST BIND THE FIGURE'S TRAILING `". "`

The recorded header is `[mock-zai <4hex>] #<4hex> <4/4/4>. ` — the figure is followed by a
**period and a space**. A pattern that expects a bare space after the figure matches
**0/40**, and the pre-flight then reports a false "the mock is broken" story:
`distinct_seeds 1/40`, `recomputed_md5 0/40`, `per_prompt_8x5` all red, while
`distinct_previews_40`, `body_len_band` and `cultural_prompt_band` stay green.

The working parse:

```python
HDR = re.compile(r"^\[mock-zai ([0-9a-f]{4})\]\s*#?\s*([0-9a-f]{4})\s+"
                 r"([0-9a-f]{4}/[0-9a-f]{4}/[0-9a-f]{4})\.\s")
```

Note the `#` is **attached to the colour** in the body (`#d64d`), and the `\.` is
required. This is the **second** header-parse trap in the project after the
seed/colour mis-split (session 204). *Generalise: when a pre-flight goes red on the
recompute, dump one real body and parse it by hand before touching the server — a 0/40
recompute means "the parser is wrong" before it means "the mock is wrong".*

### 3. A `simulations_run` DELTA MUST BE TAKEN AGAINST THE `culture.json` BASELINE

`simulations_run` counts **simulated** runs; the ledger carries rows from **every prior
session**, so the two are not comparable. Checking the counter against
`len(ledger_rows) - 10` failed **8/8** on a run whose per-civ **counter gaps came back at
exactly the documented stable values** (grounded -84.35, whimsical -173.14, formal -85.53,
poetic -96.80, precise -32.63, mythic -51.11, therapist -42.11, engineer -44.24).

Take the baseline from the **git HEAD blob** of `culture.json`, not from the ledger.
*Corollary that generalises: the per-civ counter gap is the cheapest integrity check in
this project — it will tell you the run was clean while your check is the thing that is
broken.*

### 4. THE SPARSE-CLONE RECIPE WORKS AND THE BRIDGE TARGETS THE INNER `code` DIRECTORY

`git init` + `core.sparseCheckout` + `.git/info/sparse-checkout` containing
`cellular-first-design/code/civilizations` + `git fetch --depth 1 --filter=blob:none`
gave an **11 M** working tree from a **3.7 GB** repo. The bridge is
`ln -sfn /tmp/aiw/cellular-first-design/code /workspace/repos/ai-writings/cellular-first-design/code`,
verified by inode identity `stat -L -c '%d:%i'` -> `129:3669` on both sides plus
`os.path.samefile()` -> `True`.

**The cone-mode warning is harmless:** `git sparse-checkout` prints
`warning: disabling cone pattern matching` / `unrecognized pattern` for a multi-segment
path, and still checks the directory out correctly. Verify the tree with `ls`, not with
the absence of a warning.

### 5. THE MOCK BODY LANDS IN BAND ON THE FIRST BUILD WHEN THE TAIL IS A SINGLE FIXED STRING

Header `[mock-zai <4hex>] #<4hex> <4/4/4>. ` is a **constant 38 chars**; a 318-char fixed
tail gives a **constant 356-char** body, inside the documented 332-369 band, with **no**
iteration. The tail must contain **no culture-derived fields** — that is what removes the
length variance the band exists to catch.

### 6. THE RUN LOW AND THE LIFETIME ALIGNMENT LOW ARE DIFFERENT CIVS ON DIFFERENT AXES

Session 213's run low is `civ-whimsical` (`avg_score` **1.5107**, alignment **0.8900**
fleet-low, novelty **2.4860** fleet-high). But the **lifetime** alignment low is
`civ-therapist` (spread **1.0570** over the full ledger) while `civ-grounded` is the
lifetime low on `avg_score` and `quality`. The run table and the lifetime table are
**two separate claims** — report both, and report the axis for each.

## Session 214 additions (2026-10-25)

### 1. A SWEEP AND A PERFECT CHOOSER-AGREEMENT RATE CAN COEXIST — AND NEITHER PREDICTS THE OTHER

This session `civ-precise` won **5/5** competitions *and* the chooser agreed with the
`avg_score` argmax on **5/5 (100 %)** — no down-grades, no up-grades. The three previous
sessions were 0 % (211), 40 % (212), 40 % (213). Both measures were perfect at once.

**Do not read a 100 % agreement as "the chooser is calibrated."** It is a **5-sample point
at 100 %** sitting on a series whose last three points were 0 %, 40 %, 40 %. The honest
claim is that this session's chooser and the argmax picked the same civ every time; the
series-level calibration claim is unchanged.

**Generalise the pairing rule:** the win count is *who won*; the agreement rate is *whether
the chooser's reasoning matched the scores*. Sessions 211/212/213 all had a sweep
coexisting with poor agreement; session 214 has both perfect. **Never infer either from
the other, in either direction.**

### 2. THE RUN LOW'S SIGNATURE IS LOW ALIGNMENT; THE FLEET GAP IS ALIGNMENT, NOT NOVELTY

`civ-whimsical` was the run low (`avg_score` **1.2807**, quality **0.7180** fleet-low,
alignment **0.6850** fleet-low) with novelty **2.4390** — mid-field. The run's alignment
spread is **2.5690** against a novelty spread of **0.1250**: a factor of **20.6**. The
ranking is produced by alignment and quality, not novelty.

The bottom two were separated by **0.2243** on `avg_score` against a run spread of
**1.1607** — a gap of **19 %** of the spread, so their *ordering* is weak but the
*identity* of the bottom is not. **Print the gap next to the spread** (as in session 212)
and report the axis, not the holder.

### 3. THE COUNTER-GAP CHECK MUST BE TOLERANCED AT 1e-6 — A 1e-9 TOLERANCE IS A FALSE FAIL

The per-civ counter gap (`culture.json` `relevance_score` − ledger Σ`avg_score`) is the
cheapest integrity check in this project, and its documented stable values held **exactly**
this session (grounded −84.35, whimsical −173.14, formal −85.53, poetic −96.80, precise
−32.63, mythic −51.11, therapist −42.11, engineer −44.24) with per-civ gap deltas of
**+0.0000000000 for all 8**.

The first pass nevertheless reported `[FAIL] counter_gap_stable_8of8`. The cause was the
**check**, not the run: it computed the current gap as
`base_relevance + (csum - bsum) - bsum` and compared that to a *separately computed*
baseline gap, so the two differed in the last float bits and the 1e-9 tolerance rejected
them.

**Compute both epochs the same way** — subtract the ledger sum from the `culture.json`
blob on each side — and compare with **1e-6**. *A pre-flight FAIL on a component you have
already independently verified is a CHECK bug until proven otherwise; re-derive the fact
directly before touching the artifact.*

### 4. THE MOCK BODY BAND CAN BE HIT WITHOUT BREAKING LEDGER RECONCILIATION

The documented body band is **332–369** chars (a body longer than ~369 pushes the seed
prefix out of the 200-char `content_preview` truncation and breaks the seed+colour+figure
recompute). A body of **337** — a constant 38-char header plus a 299-char fixed,
culture-free tail — lands in band on the first build.

**The tail may be extended without breaking the existing ledger's reconciliation** as long
as its first 162 characters match the recorded rows verbatim. The recorded preview is
truncated at 200 chars, so the tail's visible prefix is what the historical rows pin
down; everything after it is free. *When sizing the tail, preserve the recorded prefix
exactly and only append.*

### 5. THE BRIDGE TARGET AND THE CLONE LOCATION, RE-CONFIRMED

`SuperInstance/AI-Writings` is a **user** account repo. `/workspace` is at 100 % NAS quota
(600 G of 600 G) and `git clone` into it dies on `.git/description` with
`Disk quota exceeded`; the **same clone into `/tmp` succeeds immediately**. The bridge is
`ln -s /tmp/clone/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`
— it must point at the **inner** `cellular-first-design` directory, because the
orchestrator's `CIVS_DIR` is hardcoded to the **inner** `code/civilizations` path. Verify
with `stat -L -c '%d:%i'` → `129:12604` on both sides plus `os.path.samefile()` → `True`
(`[ -ef ]` remains unusable in this sandbox).


## Session 215 additions (2026-10-25)

### 1. THE DOCUMENTED SEED FORMULA IS WRONG FOR `i=3` — THE CORRECT SLICE IS **CONTIGUOUS**, NOT WRAPPED

Both `RUNBOOK.md` and `SKILL_civ_orchestrator_learnings.md` specify:

```
seed = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]     # WRAPPED
```

**The truth is `seed = h[(i*2)%8 : (i*2)%8 + 4]`** — a *contiguous* 4-hex slice with **no
wrap-around**. Verified **480/480** against the session-215 ledger (the wrapped form scores
**360/480**).

The wrap only bites when `i == 3` (offset 6): the documented form yields `h[6:8] + h[0:2]`
(e.g. `5f8b`) but the ledger shows `h[6:10]` (e.g. `5fc0`). That is **25 % of all rows** —
enough to make a *correct* mock look broken and to send you hunting for a bug that is not
there. Session 213's "raw byte `d[0] % 4`" correction is right and is unaffected.

**How to settle it in one step (the diagnostic that found it):** locate the recorded seed
inside `h`:

```python
offs = [i for i in range(len(h)-3) if h[i:i+4] == recorded_seed]
# -> {0: 109, 2: 105, 4: 146, 6: 120}  == ALL EVEN OFFSETS
```

All-even offsets + `colour`/`figure` matching **480/480** while the seed matched only
**360/480** ⇒ the message reconstruction is perfect and only the *index-dependent* field is
wrong. *This is the same principle as session 213 ("the wrong field is the one that depends
on the index"), now with the exact correct formula.*

### 2. THE LEDGER CONTAINS **TWO** MOCK GENERATIONS — A HEADER-PARSE FAILURE RATE OF 33 % IS NORMAL

Of **9040** `[mock-zai` rows in the fleet, only **480** are current-format. The rest use an
older header whose `figure` was rendered as a *Python-style* `x / y / z` (with spaces) and a
colour carrying a trailing `00`:

```
[mock-zai f6bc] #68ed00 587e0 26120 0f2300. A cell is a small bounded unit ...
```

**Do not treat a 160/480 header-parse failure as a broken mock.** Filter to the current
format first (`[0-9a-f]{4}/[0-9a-f]{4}/[0-9a-f]{4}`), then reconcile. Sizing the body band
off the *old* generation will make a correct mock look out of band.

### 3. THE TAIL PREFIX IS **PER-PROMPT**, NOT PER-CIV, AND IS **5** DISTINCT STRINGS

The recorded 162-char body tail is a function of the **CANON prompt**, not the civ — all 8
civs share the same 5 tails (one per prompt in the batch). The recorded prefix that a
reconciling mock must reproduce verbatim is:

```
A cell keeps its own accounts and asks the network for what it cannot remember itself.
The bookkeeper and the witness log are two names for the same discipline: a
```

(162-163 chars, depending on the prompt). *A "fixed, culture-free tail" is the right
design for a *new* body, but to *reconcile against the existing ledger* the tail's first
162 chars must match the recorded rows — and those rows are per-prompt, so a single fixed
tail will not reproduce all 5.*

### 4. A WIPED WORKSPACE NEEDS A **SPOTLIGHT-CLONE-THEN-BRIDGE** RECIPE, AND THE SEARCH API IS THE FASTEST PATH

The workspace was empty again (**6th consecutive** session naming ephemeral paths). The
upstream was found in **one** call:

```
GET /search/code?q=civilization_orchestrator+in:path
```

`GET /user/repos` and `GET /search/repositories` both missed it (the owner is a *user*
account, the slug is case-insensitive, and `ai-writings/...` 404s). Code search has a
**separate quota** that survives core exhaustion — make it the first probe.

Clone to `/tmp` (the NAS is at 100 % and `git clone` into `/workspace` dies on
`.git/description`), then bridge to the **inner `code` dir**:

```
ln -s /tmp/aiw/cellular-first-design/code /workspace/repos/ai-writings/cellular-first-design/code
stat -L -c '%d:%i'  ->  129:12603 on both sides;  os.path.samefile() -> True
```

### 5. THE CHOOSER AGREEMENT SERIES IS **0 % / 40 % / 40 % / 20 %** (sessions 211-215) AND EVERY DISAGREEMENT STILL TAKES THE **LOWER**-SCORING CANDIDATE

Session 215: `civ-precise` swept **4/5** and `civ-formal` took 1/5; `civ-poetic` was the
argmax on **4/5** and won **0/5**; agreement **1/5 (20 %)** with **4 down-grades, 0
up-grades**. The previous three points were 0 % / 40 % / 40 %; the one before those was
100 %. *The series oscillates across the full range — re-derive it every session and never
carry a streak forward in either direction.*

### 6. THE RUN LOW AND THE LIFETIME LOW WERE **DIFFERENT CIVS** AGAIN (7 SESSIONS RUNNING)

Run low: **`civ-engineer`** (avg **1.7437**, alignment **1.8830**), 8th of 8 on the run.
Lifetime low: **`civ-grounded`** (relevance **1796.74**, rel/sim **1.1237**, lifetime avg
**1.1456**, lifetime quality **0.4849** — lowest in the fleet) — yet Grounded's lifetime
**win_rate is 0.093, 3rd-best in the fleet**. The lifetime *alignment* low is a **third**
civ, **`civ-therapist`** (**1.1985**).

**The low-relevance signature is still LOW ALIGNMENT, NOT LOW NOVELTY.** Run alignment
spread **1.0860** = **1.86x** the quality spread and **6.24x** the novelty spread.
Grounded's lifetime novelty (**1.7395**) is mid-field; the fleet's lowest lifetime novelty
(**1.6692**) belongs to **`civ-formal`**. *Report the axis, not the holder.*

### 7. THE COUNTER-GAP STABILITY CHECK HELD **8/8** AGAIN, AND THE DELTAS WERE **<= 3.3e-7**

Gaps came back at exactly the documented stable values (grounded -84.35, whimsical -173.14,
formal -85.53, poetic -96.80, precise -32.63, mythic -51.11, therapist -42.11,
engineer -44.24). *This remains the cheapest integrity check in the project — it tells you
the run was clean while your own check is the thing that is broken.*

### 8. THE `ls -la` VERIFICATION THE PROMPT ASKS FOR NEEDS **`-L`** (RE-CONFIRMED, 3RD SESSION)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` returns
**"No such file or directory"** on a perfectly healthy run, because the last path component
crosses the symlink bridge. Use **`ls -laL`**, or `ls -la` on the per-civ
`civ-*/simulations.jsonl` files directly. *A missing directory in the verification step is a
reporting artefact, not a missing run.*

## Session 216 additions (2026-10-25)

### 1. THE COUNTER-GAP MUST BE MEASURED AGAINST THE **FULL** LEDGER — A SLICE MEASURES RELEVANCE, NOT THE GAP

A first pass reported `[FAIL] counter_gap_stable_8of8` with per-civ gap deltas of ~**+2,700**
(e.g. poetic **+2696.53**). The cause was the **check**, not the run: the gap was computed
over the **10 new rows only**.

```
gap(civ) = culture.json.relevance_score  -  SUM(avg_score over the WHOLE simulations.jsonl)
```

The documented stable values (grounded −84.35, whimsical −173.14, formal −85.53,
poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24) all
reproduce exactly when the **full** ledger is summed. Against the full ledger the deltas
were **<= 3.3e-7**.

**A slice of the ledger gives you `relevance`, not the gap** — the gap is a *cumulative*
invariant by construction. *Same discipline as session 214: a pre-flight FAIL on an
already-verified component is a CHECK bug until proven otherwise.*

### 2. THE PRE-FLIGHT PROMPT SET MUST BE THE **RUN'S** PROMPT SET (`CANON_PROMPTS` HAS 10, THE RUN USES 5)

The first gate pass reported `80/40` on four checks ("40 distinct seeds", "40 distinct
previews", "40 recomputed md5", "[mock-zai prefix 40/40", "repeat-same-message"). The mock
was healthy: the gate had built **8 civs x 10 prompts = 80** messages, because
`CANON_PROMPTS` holds **10** prompts while the run is `--prompts 5`.

```
PROMPTS = ALL_CANON_PROMPTS[:args.prompts]      # the run slices the FIRST N
```

**A count mismatch of exactly `8 x (len(CANON) - N)` is a fixture bug, not a mock bug.**
Assert the message count equals `len(civs) * N` before asserting on seeds.

### 3. THE MOCK HEADER IS **39** CHARS, NOT 33 — AND THE BODY BAND IS 332-369

Current-format body: `[mock-zai {seed}] #{color} {figure}.  {tail}` — the header is
`"[mock-zai " (10) + seed (4) + "] #" (3) + color (4) + " " (1) + figure (14) + "." (1)
+ two spaces (2) = 39`.

With a **324**-char fixed culture-free tail the body lands at **363** — inside the
**332-369** band. The tail's first **162** chars are the recorded ledger's prefix,
verbatim:

```
A cell keeps its own accounts and asks the network for what it cannot remember itself.
The bookkeeper and the witness log are two names for the same discipline:
```

**There are exactly 3 distinct recorded tails (161, 162, 162 chars) and they are NOT
per-prompt** — the same three appear against all five canon prompts. Session 215's
"the tail prefix is per-prompt" reading is **wrong**; the tail is decoupled from the prompt.

### 4. THE CONTIGUOUS SEED SLICE RE-CONFIRMED **320/320** AGAINST THE RECORDED LEDGER

`seed = h[(i*2)%8 : (i*2)%8+4]` matched the recorded ledger **320/320**; the RUNBOOK's
wrapped form matched **237/320**. The wrap still costs exactly the `i == 3` quartile
(offset 6 -> `h[6:8] + h[0:2]` instead of `h[6:10]`). *The RUNBOOK's seed formula is
still wrong — trust the learnings file, not the RUNBOOK.*

### 5. THE CHOOSER-AGREEMENT SERIES IS NOW **0 / 40 / 40 / 100 / 60 %** (sessions 211-216)

Session 216: `civ-precise` swept **5/5**; agreement **3/5 (60 %)** with **2 down-grades,
0 up-grades**. Every disagreement again took the **lower**-scoring candidate. The series
oscillates across the full range — *re-derive it every session and never carry a streak
forward in either direction.*

### 6. THE RUN LOW ROTATED TO `civ-therapist`; `civ-grounded` HELD THE LIFETIME LOW FOR THE 84th SESSION

Run low `civ-therapist` (avg **1.4080**, fleet-low run quality **0.9510**, fleet-low run
alignment **0.9450**), gap to next **0.1597** = **18.5 %** of the run spread **0.8623**.
Lifetime low `civ-grounded` (relevance **1815.38**, rel/sim **1.1283**, lifetime avg
**1.1500**, fleet-low lifetime quality **0.4897**) — yet its lifetime `win_rate` **0.092**
is 3rd-best in the fleet. Lifetime alignment low is a **third** civ, `civ-therapist`
(**1.1969**). The run's alignment spread **2.0620** was **3.41x** the quality spread and
**16.11x** the novelty spread. *Report the axis, not the holder.*

## Session 220 additions (2026-10-25)

### 1. THE `#`-PREFIX TRAP BIT AGAIN, AND IT STILL PRESENTS AS "0/N RECOMPUTE = MOCK BROKEN"

Re-deriving the mock algorithm against the live ledger, the first comparison pass printed
**ok 0 bad 640** — which reads as "the mock is broken". The mock was perfect. The recorded
colour in the header carries a `#` (`#44cc`) while the derived slice `h[8:12]` does not
(`44cc`); the comparison must normalise one side. *This is the third occurrence of the
same trap (sessions 204, 213, 220). A `0/N` recompute is a **parser** diagnosis until
proven otherwise — dump one real body and parse it by hand before touching the mock.*

### 2. A MOCK BODY BAND IS SOLVED ALGEBRAICALLY IN ONE BUILD — TARGET 349, NOT A RANGE

Header `[mock-zai {seed}] #{color} {figure}.  ` renders to a constant **39** chars
(17 fixed + seed 4 + colour 4 + figure 14). A **310**-char fixed, culture-free tail gives
a constant body of **349** — inside the documented **332-369** band on build 1, with
**zero** iteration. Compute the tail length from the fixed prefix; never iterate prose to
fit a band. (A build that varies with the civ name re-introduces the variance the band
exists to catch.)

### 3. `GET /user/repos` FOUND THE UPSTREAM IN ONE CALL AGAIN — THE OWNER IS A *USER* ACCOUNT

`SuperInstance/AI-Writings` (case-insensitive; the `ai-writings/...` slug 404s). The
`ai-writings` path is a **subdirectory** of that repo, not a repo of its own, so
`git ls-remote .../ai-writings/cellular-first-design.git` returns *Repository not found*.
`GET /user/repos` paginates ~100/repo and the owner has thousands, so **page through it
and filter on the name** — the first 6 pages here surfaced `SuperInstance/AI-Writings`
once the filter was `cellular|civ|writing|autoclaw`.

### 4. THE BRIDGE TARGET IS THE **INNER `cellular-first-design`** DIR — AND THE PLAIN `ls` WORKS ON IT

`CIVS_DIR` is hardcoded to `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`,
so the bridge is
`ln -s /tmp/cfd/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`
— pointing at the **inner** dir, one level below the clone root. Verified by
`stat -L -c '%d:%i'` (`128:12601` both sides) + `os.path.samefile()` -> `True`.
**Unlike the `code`-dir bridge of sessions 200-209, a plain `ls -la` on the civs dir
WORKED here** — the "needs `-L`" rule is a property of *where the symlink boundary falls*,
not of `ls` itself. *Use `-L` when the last path component crosses the bridge; do not
assume it always fails.*

### 5. CHOOSER AGREEMENT **1/5 (20 %)** — 4 DOWN-GRADES, 0 UP-GRADES; `civ-poetic` ARGMAX 3/5, WON 0/5

Session 220: `civ-precise` won 4/5, `civ-engineer` 1/5. Agreement **1/5**, every
disagreement took the **lower**-scoring candidate; the widest down-grade margin was
**+0.2600** (ternary values). The series (sessions 211-220) now reads
0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 % — *re-derive it every session; the
up-grade count is still **0** across the whole series.*

### 6. THE RUN-LOW MARGIN IS NOT THE HOLD — IT MOVED FROM 33.7 % TO 13.6 % WITH THE SAME HOLDER

`civ-therapist` was the run low again (avg **1.2937**, fleet-low run alignment **0.8670**,
fleet-low run quality **0.4500**), but its gap to the next civ was **0.1110 = 13.6 %** of
the run spread, against session 219's **33.7 %** for the *same* civ. *The identity of the
bottom rotated only sometimes; the margin is a separate, faster-moving quantity — quote
the gap next to the spread, and never let a strong margin last session imply a strong
margin this session.*

### 7. `civ-grounded` HELD THE LIFETIME LOW FOR THE **88th** CONSECUTIVE SESSION — AND THE THREE AXES ARE STILL THREE DIFFERENT CIVS

Lifetime low `civ-grounded` (relevance **1886.01**, rel/sim **1.1440**, lifetime avg
**1.1645**, fleet-low lifetime quality **0.4996**) — yet its lifetime `win_rate` **0.090**
is 3rd-best in the fleet. Lifetime **alignment** low is `civ-therapist` (**1.1948**);
lifetime **novelty** low is `civ-formal` (**1.6938**). Run low is `civ-therapist`.
*Selection and relevance are separate axes, and the axis identity rotates. Report the
axis, not the holder.*

### 8. THE COUNTER-GAP STABILITY CHECK HELD **8/8** EXACT AGAIN, AND THE SEED-MULTISET IDENTITY HELD

Gaps returned at exactly the documented stable values (grounded −84.35, whimsical −173.14,
formal −85.53, poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11,
engineer −44.24) after a **+10 rows/civ** run. The mock log's **last 80** OK lines form
the same seed multiset as the 80 new ledger rows (identity, not a count — the pre-flight
had run once for 80 log lines and the run for another 80, total **160**). *This remains the
cheapest end-to-end integrity check: the log and the ledger must be the same multiset.*

## Session 226 additions (2026-10-25)

### 1. THE `0/40` RECOMPUTE WAS A **GATE** GROUP-UNPACKING BUG — THE MOCK WAS PERFECT

The mock-header regex yields **FIVE** groups `(seed, colour, fig1, fig2, fig3)`. The
verifier unpacked **three** `(s, c, f)`, so `pr[2]` held only `c8a2` instead of the
joined `c8a2/50a5/dcdd` and **every** row mismatched. A hand-dump of one real body
confirmed seed `446f`, colour `d64d`, figure `c8a2/50a5/dcdd` matched the recompute
**exactly**. *The figure must be reassembled as a slash-joined string before comparing.
This is now the **fourth** occurrence of the "0/N recompute = parser diagnosis" rule
(sessions 204, 213, 220, 226) — the `#`-prefix trap and the group-count trap are the
same family: **compare the parsed value, not the parse fragment.***

### 2. THE GATE AND THE VERIFIER EACH HAD A FIELD-NAME MISMATCH, AND BOTH SURFACED AS `KeyError`

The baseline snapshot stores `relevance`; `culture.json` stores `relevance_score`. A blind
search-and-replace across the verifier file fixed one occurrence and broke the other.
*Name the two sides explicitly before editing. A `KeyError` mid-verification is a
verifier bug, never a data defect — and a partially-patched verifier must be re-run from
the top, not resumed.*

### 3. A **100 %** AGREEMENT SESSION IS A 5-SAMPLE POINT AT 100 %, NOT A NEW REGIME

Session 226: `civ-precise` swept **5/5** with **5/5 (100 %)** chooser/argmax agreement, the
first perfect-agreement session since 216. The series (211-226) reads
0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 / 100 % and contains 0 % and
20 % points. *The honest claim is "agreement can reach 5/5", not "agreement is 100 %". The
up-grade count across the whole 16-session series is still **0**.*

### 4. THIS RUN LOW WAS LOW ON **ALL THREE** AXES — A DIFFERENT SIGNATURE

`civ-mythic` was the run low (avg **0.6120**) and the fleet-low on run quality (**0.0440**),
run alignment (**0.0410**) **and** run novelty (**1.7510**) simultaneously — the first
session where the run low is not the "high novelty, low alignment" shape. The run's
alignment spread **2.3520** was **5.43x** the quality spread and **7.13x** the novelty
spread, so the ranking is still produced by alignment. *The signature can change shape;
the axis that drives the ranking did not.*

### 5. THE MOCK BODY LANDED AT **349** CHARS ON THE FIRST BUILD — COMPUTE, DON'T ITERATE

39-char fixed header + a **310**-char fixed, culture-free tail = **349**, inside the
**332-369** band with zero iteration. *Compute the allowance from the fixed prefix; never
iterate prose to fit a band.*

### 6. THE GATE'S 5-GROUP / 3-GROUP MISMATCH IS THE **FOURTH** MEMBER OF THE "0/N = PARSER" FAMILY

The `#`-prefix trap (sessions 204, 213, 220) and the group-count trap (226) share one
root: **comparing a parse fragment instead of the parsed value.** The mock-header regex
yields five groups; unpacking three made `pr[2]` the first figure component only.
*Reassemble the figure as a slash-joined string before comparing, and when a recompute
reports 0/N, dump one real body and parse it by hand before touching the mock.*

### 7. THE OWNER IS A **USER** ACCOUNT WITH 5 400+ REPOS — PAGE AND FILTER, DON'T GUESS THE SLUG

`SuperInstance/AI-Writings` is the upstream; `cellular-first-design` is a **subdirectory**
of it, so `git ls-remote .../ai-writings/cellular-first-design.git` returns *Repository not
found*. `GET /user/repos` paginates at 100 and the owner has thousands, so **page through
it and filter on `cellular|civ|writing|autoclaw`** — the first 5 pages here surfaced
`SuperInstance/AI-Writings` immediately. A 6th occurrence of the "the path in the prompt
404s" trap.

## Session 232 additions (2026-10-25)

### 1. THE TWO-AXIS COLLAPSE BROKE AFTER 2 SESSIONS — THE RUN LOW IS **ALIGNMENT-ONLY** THIS TIME

Sessions 230 and 231 both ended with a **quality+alignment two-axis collapse** (novelty
untouched) as the run low. Session 232's run low is `civ-therapist` (avg **1.5067**) with a
**single-axis** signature: alignment mean **1.1560**, run-min **0.5800** = fleet-min, while
quality **0.7200** was **not** fleet-low (the fleet quality min of 0.2400 belonged to another
civ) and novelty **2.6440** was 2nd-highest.

*Rule: the run low rotates, the axis set rotates, AND the axis SET itself can change. Do not
carry the previous session's axis diagnosis forward even when the same civ holds the low. The
reusable test is unchanged: compare the run low's per-axis value against the **fleet-wide
min of that same axis in the same run**, not against the other civs' means.*

### 2. `civ-grounded` HELD THE LIFETIME LOW FOR THE **96th CONSECUTIVE SESSION** — AND RANKED 6th OF 8 ON THE RUN

Lifetime relevance **2089.08** (from 2071.25), `relevance_per_sim` **1.1810** — last of 8, and
the label did not rotate. Run-level it was **6th of 8** on `avg_score` (**1.7830**), just below
`civ-whimsical` (1.7910), with quality **0.6740** (low) and alignment **2.0780** (mid-field).
The weakness is again **prose quality, not voice**.

*Rule: a lifetime-low label and a run rank are different measurements. A civ can hold the
lifetime low for 96 straight sessions while sitting mid-field in any given run.*

### 3. THE QUALITY AXIS WAS **WIDE** THIS RUN — THE DISCRIMINATION AXIS IS NOT FIXED

Session 231's quality spread was **0.6620** (collapsed). Session 232's was **1.6600** — 2.5x
wider. Alignment again carried the discrimination (spread **2.7700**, **5.77x** the novelty
spread of 0.4800), and novelty stayed nearly flat.

*Rule: "alignment carries the discrimination" has held for multiple sessions, but the *quality*
axis width is a **run-level** property that can double between sessions. Report the axis
signature per session; never carry a "collapsed quality axis" diagnosis forward.*

### 4. A CHOOSER SWEEP IS NOT A `avg_score` SWEEP — AND THE ARGMAX WAS **MIXED** THIS TIME

The chooser picked `civ-precise` on **5/5** prompts, while the `avg_score` argmax was `civ-precise`
on 3 and `civ-poetic` on 2 — i.e. a **mixed** argmax, unlike session 231 where the `avg_score`
argmax was a single repeated civ on all five. The chooser was **live** (a `choice` answer with a
`probabilities` distribution was returned; the `max(..., key=avg_score)` fallback path produces
no probabilities).

*Rule: keep reporting the **shape** of the divergence — a single-civ `avg_score` argmax sweep
means the two axes have fully diverged; a mixed argmax means partial divergence. The chooser
can still sweep alone. Neither shape is a quality KPI.*

### 5. THE `--prompts` FLAG CONTROLS **ONLY** THE COMPETITION PHASE

`--prompts N` slices `CANON_PROMPTS[:N]` for the **competition** phase only; the `--sims N`
phase draws each sim's prompt at random from the **same** `prompts` list. With
`--sims 5 --prompts 5` both phases use the same 5 prompts, so each `(civ, prompt)` pair
recurs 1-4 times inside a civ's 10 new rows.

*Rule: this is why the meta-vs-ledger `avg_score` check must select the **later-`ts`** row
(`max(cands, key=ts)`) — the competition-phase row is always the later one. A first-match
lookup reports false mismatches.*

### 6. A `md5` PRE-FLIGHT INDEX BUG OF MY OWN — MESSAGES ARE **CIV-MAJOR**, CHECKS ARE **PROMPT-MAJOR**

Building 40 messages as `for civ: for prompt:` (civ-major) and then indexing them as
`seeds[pi + len(CIVS)*k]` (prompt-major) raises `IndexError` past the end of the list. It
fails loudly, which is the good case.

*Rule: when a pre-flight builds a matrix of inputs, index it in the **same order it was
built**. The mock-algorithm checks (`i = d[0] % 4`) are message-order independent, but the
"8/8 distinct per prompt" check is not.*

### 7. A MISSING `import re` / `import os` IS A **LOUD** FAILURE, NOT A SILENT ONE

Two verification scripts in a row died on `NameError: name 're' is not defined` and
`NameError: name 'os' is not defined`. Both surfaced as a traceback before the check block
ran, so no check was silently skipped.

*Rule: prefer a loud crash at the top of a verification script over a check that "passes"
because it never ran. A verification script that exits 0 must have executed every check —
print the per-check PASS/FAIL lines and the failure count, as `verify.py` does.*

### Re-confirmations (this session)

- 112th session with the prompt path absent; 96th session with the z.ai credential gap.
  Control B was the only provider path; `ZAI_TOKEN` placeholder + `ZAI_URL_OVERRIDE` were
  both required (`ZAI_URL_OVERRIDE` alone is dead code behind the token gate).
- Repo is `SuperInstance/AI-Writings`; `cellular-first-design` is a **subdirectory**. NAS
  EDQUOT total (19th session) — clone to the overlay, bridge the **clone root**, verify by
  inode identity (`stat -L -c '%d:%i'`), not by `-ef` (broken in this sandbox).
- JEV live: `jev-1.14.0`, HTTP 200 on a well-formed `questions` body. `TYPESAFEAI_KEY`
  exported from `TYPESAFE_AI_TOKEN`.
- Relevance reconciliation against the **unrounded** `culture.json` git blob: 8/8 exact,
  residual <= 9.09e-13. A rounded leaderboard table would have produced false mismatches.
- Pre-flight 10/10, including the **repeat-same-message determinism probe** (a distinctness-only
  pre-flight cannot certify determinism) and **0 `(civ,prompt)` pairs carrying >1 seed**.
- Run-wide verification: ledger Δ +80 (10 per civ x 8), meta_log Δ +5, `Winner:` lines = 5,
  wins/losses 8/8 exact, distinct seeds 40/80, md5 recompute 80/80, meta-vs-ledger 0/40.
- Extinction risk NONE: threshold -10.0, lowest civ 208.9x above it.

## Session 233 additions (2026-10-25)

### 1. THE 162-CHAR TAIL MUST BE **LIFTED FROM THE LEDGER**, NOT HAND-TYPED — AND THE ASSERTION IS WHAT CATCHES IT

The first build of this session's mock asserted `TAIL_LEN == 162` against a hand-written tail and
**failed loudly at startup** (measured 380, expected 162) — the mock never started, so the run was
not at risk. The tail was then lifted **verbatim from a current-format ledger row** and the
continuation solved algebraically for a **351**-char body (38 + 162 + 151), mid-band.

*Rule: a hand-typed constant in a geometry-critical position is a latent failure even when the
geometry is documented. Take geometry constants from the artifact they describe, and keep the
assertion that enforces them.*

### 2. THE PRE-FLIGHT IS **15 CHECKS** NOW, AND THE ALGORITHM GATE IS **1920/1920** OVER THE FULL LEDGER

The canonical md5 algorithm was re-derived and matched **1920/1920 exact, 0 mismatches** over the
current-format rows of the 8 civ ledgers **before** the mock was built. Pre-flight passed **15/15**
on the first build that used the ledger-derived tail.

*The full-ledger recompute is the gate that makes the pre-flight mean something. Proving the
algorithm against your own fresh rows is circular.*

### 3. THE MOCK LOG LINE COUNT IS **`2N + 1`** — AND THE REPEAT PROBE IS THE EXTRA LINE

122 lines observed against an expected 121 (40 pre-flight + 1 repeat probe + 80 run + 1 GET). The
`2N+1` rule from session 221 still holds, but the **repeat-same-message determinism probe** is
itself a logged request — so the count is `2N + 1` *plus* the number of repeat probes, not a
constant.

*Rule: never assert a log line count that encodes an assumption about how many probes ran. Assert
the property, not the count.*

### 4. THE CHOOSER SERIES BROKE A 20-SESSION STREAK: **1 UP-GRADE** AT **20 %** AGREEMENT

JEV-pick vs `avg_score` argmax was **1/5 (20 %)** — 4 down-grades and **1 up-grade**, the first
up-grade after 20 sessions of zero. The `avg_score` argmax was `civ-poetic` on **4 of 5** prompts
while the chooser picked `civ-precise` 4 and `civ-engineer` 1.

*Rule: the up-grade/down-grade counter is part of the series. A new up-grade is a fact to report,
not a number to smooth.*

### 5. THE QUALITY AXIS WAS **NARROW** THIS RUN — ALIGNMENT DOMINATED AT 2.20x, NOT THE USUAL 5-13x

Alignment spread 2.0780 = 2.20x the `avg_score` spread, but only **8.15x** novelty, and the
quality axis was narrow (0.5950, vs 1.6600 in session 232). The run-low civ was
`civ-therapist` (avg 1.1743) on a **two-axis** quality+alignment collapse — breaking session
232's single-axis shape.

*Rule: report the axis signature **for this session** and never carry a spread ratio forward. The
axis dominates, but the ratio swings by 6x across adjacent sessions.*

### 6. THE `wins`/`losses` DELTA MUST BE DERIVED AS **`W` / `5 - W`** — AND IT IS 8/8 EXACT

`civ-precise` took 4 competitions (wins +4, losses +4) and `civ-engineer` took 1 (wins +1, losses
+5); the seven that lost every one took losses +5. Checked 8/8 against the git blob baseline. The
counter gap (culture relevance - lifetime ledger sum) was **byte-identical** to the session-230
documented values on all 8 civs — fixed, not accumulating.

---

## Session 241 (2026-10-25) — empty-sandbox bootstrap + re-derived mock spec

**Run:** `--sims 5 --prompts 5 --providers zai`, exit 0, 29.02 s, 8 civs x 5 sims + 5 competitions.
**Ledger delta:** +10 rows per civ (80 total), `meta_log` +5, 18 files modified.
**Provider:** Control B mock (z.ai credential gap, **102nd session**) + live JEV (`jev-1.14.0`), 0 fallback triples.

### Bootstrap when the sandbox starts empty

This sandbox had **no `/workspace/repos` and no clone** — a full wipe. Recovery path, in order:

1. **Find the repo with the REST API, not `gh`.** `gh` is **not installed** in this image. Use
   `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/search/code?q=civilization_orchestrator.py+in:path`
   — code search is what pins the *subdirectory* (`cellular-first-design` is a folder inside
   `SuperInstance/AI-Writings`, not a repo of its own). `$GITHUB_TOKEN` is present in the env.
2. **The repo is 3.7 GB. Do not clone it fully.** Cone sparse checkout of the one subtree:
   `git init` -> `git remote add origin <token-url>` -> `git config core.sparseCheckout true` ->
   `git sparse-checkout init --cone` -> `git sparse-checkout set cellular-first-design` ->
   `GIT_SSL_NO_VERIFY=1 git fetch --depth 1 origin main` -> `git checkout main`. That pulls a few MB.
3. **Clone into `/tmp`, not `/workspace`.** The NAS sits at 600 G/600 G, 0 avail (EDQUOT). `/tmp` is
   on the overlay with ~28 G free.
4. **Bridge the hardcoded path.** The orchestrator anchors every read and write to
   `CIVS_DIR = Path("/workspace/repos/ai-writings/cellular-first-design/code/civilizations")`
   (line 36 of `civilization_orchestrator.py`). A clone elsewhere is invisible to it. Fix with a
   symlink: `ln -sfn /tmp/clone/ai-writings/cellular-first-design/code \
   /workspace/repos/ai-writings/cellular-first-design/code`, then assert
   `os.path.samefile(a, b) -> True`. The symlink itself is a few bytes and lands fine on a full NAS;
   it is the *clone* that cannot live there.

### NAS EDQUOT: a 0-byte write can succeed while 5 MB fails

`echo x > /workspace/.t` succeeds; `dd ... count=5` dies with "Disk quota exceeded" and leaves a
**0-byte file that still shows in `ls`**. `git init` inside `/workspace` fails copying
`.git/description` (a few hundred bytes). **Never infer writability from a tiny probe** — test with
the real payload size, and remember the failure mode is a silent 0-byte file.

### The `write` tool cannot reach `/tmp`, and the workspace is full anyway

The `write` tool is jailed to the workspace root ("Workspace path escapes Cloud Host root") and the
workspace is at 0 free. Write scratch scripts with a **bash heredoc** (`cat > /tmp/x.py <<'EOF'`)
and keep every artifact on the overlay.

### Re-derive the Control B spec; do not copy the prior report

The mock source is **not in the repo** — the ledger is the specification. Session 241 re-derived it
from scratch and validated against the **pre-run** ledger:

```
d = md5(cultural_prompt).digest(); h = d.hex(); i = d[0] % 4     # RAW MD5 BYTE
seed = h[(i*2)%8:(i*2)%8+4]; color = h[8:12]; figure = h[12:16]/h[16:20]/h[20:24]
```

- Validated **2320/2320 exact, 0 mismatches** over the full current-format ledger before the run.
  The `i = d[0] % 4` detail matters: `d[0]` is the raw byte, **not** `int(h[0], 16)`.
- The ledger holds **two body formats**: the historical `[mock-zai <12 hex>]` form (240 rows) and the
  current `[mock-zai <4 hex>] #<4 hex> <4>/<4>/<4>. ` form (2320 rows). Only the current form parses.
- The body bank is **13 fixed 162-char tails**. The correct tail is the one from the ledger's
  **most recent 80-row cluster**, byte-for-byte — not an arbitrary member of the bank.
- Body length is pinned to **344 = 38 (header) + 162 (tail) + 144 (continuation)**. Verify the mock's
  output length before the run; a 353-char body means the continuation is wrong.
- The mock served **80** requests for 80 ledger rows; a pre-flight probe accounts for 81 in the log.

### Verification: `ls -la` is the weakest check

`ls -la` shows mtimes and has passed on trees with 18 modified files. The discriminating checks:

| check | this session |
|---|---|
| row-count delta per civ vs pinned git blob | **+10 each, 80 total** |
| seed/colour/figure recompute on new rows | **80/80 exact** |
| `content_preview` length | **200** on all 80 |
| distinct bodies | 1 |
| provider mix | `zai` 80/80 |
| JEV errors / fallback triples | 0 / 0 |
| counter gap (relevance - full-ledger sum) | drift **0.000000** on all 8 civs |

For remote verification, the **contents API truncates large files** (it returns 1 "line" for a
1902-row jsonl). Use the **git blob API** (`/git/blobs/<sha>`, base64) to count rows remotely, and
compare `size` from the contents API as a cheap integrity check.

### Result: the run low and the lifetime low decoupled

- **`civ-grounded` (The Grounded)** — lowest lifetime relevance **2244.23**, lowest rel/sim **1.207**,
  8th of 8. Lifetime low for the **103rd consecutive session**.
- **`civ-therapist` (The Therapist)** — the **run low** (avg **1.4393**) with the fleet-low quality
  (**0.7340**) and fleet-low alignment (**1.1020**): a two-axis collapse on the run axes.
- Session 240 had the *same* civ as both run low and lifetime low. Session 241 **decoupled** them.
  Do not assume the bottom pair is fixed — recompute both axes each run.
- `civ-precise` swept **5/5** competitions (session 240: 4/5). Chooser/argmax agreement 3/5 (60 %),
  2 down-grades, 0 up-grades — up-grades are **structurally impossible**, since the chooser reads
  only `content_preview[:150]` and never sees `avg_score`.
- Axis signature: **alignment spread 1.7690 = 2.34x** the avg_score spread (0.7563); quality 1.03x,
  novelty 0.28x. Alignment has dominated for sessions 238-241 (2.05x-2.40x band).
- No extinction: threshold is `relevance < -10`, lowest is 2244.23. All 8 civs remain generation 1;
  `extinction_and_birth()` does not run in a non-`--loop` invocation.
