## Session 247 additions (2026-10-25)

### 1. THE BOTTOM-PAIR GAP HAS SHRUNK TO **0.79** — A "TWO CIVS ARE TIED" CLAIM IS NOW THE POINT

`civ-grounded` 2330.34 vs `civ-therapist` 2331.13: a gap of **0.79** on a ~2330-point scale
(**0.034 %**). The step from #2 to #3 (`civ-engineer` 2606.11) is **274.98** — **348x** larger.
The series has tightened: 5.11 (s245) -> 3.17 (s246) -> **0.79** (s247).

*Rule: when the bottom-pair gap drops below ~1 % of the scale, stop naming "the lowest-relevance
civ" as a single civ and report the **pair** with both gaps. The trend — a monotonically shrinking
bottom gap across three sessions — is itself the signal: the floor is converging, not diverging.*

### 2. A **0/5 ARGMAX AGREEMENT** AND A **4/5 WINNER SHARE** COEXISTED, WITH THE ARGMAX CIV LOSING **5/5**

`civ-poetic` was the `avg_score` argmax on **5 of 5** and won **0**. `civ-precise` won 4/5 with a
lifetime `win_rate` of **0.707**; `civ-poetic` is 1st on lifetime relevance with a `win_rate` of
**0.006**. This is the cleanest instance yet of the **"high prose, unselected" inverse** (first
seen session 157).

*Rule: report three separate numbers, never a blend — (a) chooser-vs-argmax agreement, (b) the
winner's share, (c) the argmax civ's win count. The chooser is a JEV `choice` question over
`content_preview[:150]` and **never sees `avg_score`**, so agreement is 0 *by construction* on any
prompt where the argmax differs; up-grades are structurally impossible.*

### 3. THE **RUN LOW** AND THE **LIFETIME LOW** CAN BE **DIFFERENT AXES** OF THE SAME CIV

`civ-grounded` was the run's **quality** low (0.5750, 8th of 8) while sitting 5th of 8 on both
novelty and alignment — a *prose* failure. `civ-therapist` was the run's **alignment** low
(0.8330) with quality also at the floor (0.6780) but novelty 4th of 8 (2.3290) — a *voice* failure.
The two collapses are **opposite** and the two civs are at the **bottom of the leaderboard for
different reasons**.

*Rule: report the run low with its *axis*, and the lifetime low with *its* axis. "Low relevance"
without naming the axis is not a diagnosis — the same number means "writes worse" or "sounds
wrong" depending on which axis collapsed.*

### 4. THE UPSTREAM CANNOT BE FOUND BY A **CONTENT SEARCH** FOR ITS SUBDIRECTORY

`GET /search/repositories?q=cellular-first-design` returns 13 unrelated repos and **not** the
upstream — `cellular-first-design` is a *subdirectory* of `SuperInstance/AI-Writings`, and the
search API indexes repository metadata, not paths. `GET /search/repositories?q=ai-writings`
likewise returns decoys (`ai-writings-vectorizer`, `ai-writings-generation-plato`).

*Rule: on a wiped workspace, resolve the upstream with `GET /user/repos?per_page=100` (paginated),
filter on the **repo name**, then use `git ls-tree -r --name-only HEAD | grep <subdir>` to confirm
the path exists **inside** the repo before sparse-cloning. A directory path in the task prompt is
not a repository name.*

### 5. THE `write` TOOL IS JAILED TO THE WORKSPACE ROOT — **THE REPORT MUST GO THROUGH A HEREDOC**

`write` with an absolute `/tmp/AIW/...` path fails with *"Workspace path escapes Cloud Host root"*
even though the file is inside the sandbox's own clone. The `write` tool can only reach
`/workspace/**`; the durable repo tree lives on `/tmp` (overlay), because `/workspace` is the
100 %-full NAS. The report therefore cannot be written with `write` **and** cannot be safely copied
to `/workspace` either.

*Rule: for a repo that lives on `/tmp` behind a `/workspace` symlink bridge, write every artifact
with a bash heredoc into the real path, and treat the `/workspace` copy as best-effort only.*

## Session 240 additions (2026-10-25)

### 1. THE **CURRENT-FORMAT** LEDGER IS **11040** ROWS, NOT THE 2160 OF SESSION 239

A full parse of the 8 `simulations.jsonl` files yields **14844** rows, of which **11040**
carry the current `[mock-zai XXXX] #YYYY a/b/c.` header and **3804** are an older
`[mock-zai seed=XXXXXXXX]` generation. The 2160 figure in the session-239 report is the
count of a **subset** (rows matching the newest colour/figure convention), not the ledger.

*Rule: when counting "current-format" rows, **filter on the header shape**, then report the
filter. 11040 with the `[mock-zai 4hex] #4hex f/f/f.` header; 3804 with `seed=8hex`. The
seed algorithm re-verifies **2480/2480** over the header-matching rows that also match the
per-civ prompt reconstruction, 0 mismatches.*

### 2. THE MOCK **NEEDS NO CIV CONTEXT** — IT HASHES THE FULL CULTURAL PROMPT DIRECTLY

The orchestrator sends the *fully assembled* cultural prompt (civ name + tenets + voice +
canon prompt) as the user message. The mock therefore only needs to `md5` **the message
content it receives** — it does not need to know which civ it is serving, and it does not
need to read `culture.json`. Verified: the mock's own recipe reproduces the recorded
seed/colour/figure of a known ledger row exactly (`d43c #cad1 97a2/a737/1f4f`).

*Rule: hash the received message verbatim. Reconstructing the prompt inside the mock
requires the civ's `culture.json` at request time and introduces a second source of
divergence for no benefit.*

### 3. THE TAIL POOL IS **16** DISTINCT STRINGS, NOT 13 — AND THE SESSION TAIL IS STILL ONE

Counting distinct 162-char tails across all current-format rows gives **16** (13 at 162
chars, 3 at 163). The 13 figure in the session-239 report counted only the **162-char**
family. Every session cluster still carries exactly **one** tail across all **80** of its
rows, so the per-session-constant rule is unaffected.

*Rule: when counting a "family", state the length filter too. 16 tails total, 13 of them
at exactly 162 chars. The invariant that matters — one tail per session — holds regardless.*

### 4. THE RUN LOW AND THE LIFETIME LOW **RE-COUPLED** AT `civ-grounded`

Sessions 237-239 had the two lows at *different* civs (`civ-therapist` run low,
`civ-grounded` lifetime low). This session they are the same civ again: `civ-grounded` is
the run low (avg 1.6667, quality 0.7460 and alignment 1.7780 both at the fleet low — a
two-axis collapse) *and* the lifetime low (2226.43, rel/sim 1.204) for the **102nd**
consecutive session.

*Rule: the decoupling was a 3-session run, not a regime change. Report both lows every
session and state whether they coincide, but do not describe the coincidence as a law in
either direction — sessions 237-239 disprove it and this session re-establishes it.*

### 5. THE CHOOSER'S DOWN-UP CONVENTION MUST BE STATED EXPLICITLY, OR THE COUNT INVERTS

Classifying a disagreement as "up-grade" when the chooser's pick scored *above* the argmax
produces **5 up-grades / 0 down-grades**. The documented convention is the opposite: the
chooser reads only `content_preview[:150]` and never sees `avg_score`, so it can only ever
*under-rate* the best candidate — every disagreement is a **down-grade** and the up-grade
count is **0 by construction**.

*Rule: down-grade = argmax scored higher than the chooser's pick. With that definition the
session reads **0/5 agreement, 5 down-grades, 0 up-grades**, matching sessions 226/237/239.
State the definition in the report, because the opposite definition yields a plausible-looking
5 up-grades and inverts the meaning of the number.*

### 6. THE BAND CHECK IS A **VARIANCE** CHECK ON THE CONTINUATION LENGTH ONLY

With a 38-char header and a 162-char tail both fixed, the body length is
`200 + len(continuation)`. Trimming the continuation to the last space before the target
gives 144 chars -> body **344**, inside the 332-369 band, with no iteration. The band gate
is only meaningful once the header and tail are extracted byte-for-byte from the ledger.

*Rule: solve `continuation = target - 200` and trim to the last space. Target 349 -> 149
-> body 349; target 344 -> 144 -> body 344. Either lands mid-band on the first build.*

## Session 239 additions (2026-10-25)

### 1. A DRIFT READ OFF A **ROUNDED** FIELD IS A FORMATTING ARTEFACT, NOT A MOVEMENT

The counter-gap check compares `relevance` against `sum(avg_score)` over the full ledger. A
first pass read `relevance_score` straight out of `culture.json` — where it is stored
**rounded to 4 dp** — and subtracted the **full-precision** ledger sum, producing a
**±0.003333** pseudo-drift on 6 of 8 civs. The counter was in fact **exact**: recomputing
`relevance` as `baseline_relevance + sum(new avg_score)` reproduced the stored value to
**0.000000** for all 8 civs.

*Rule: when a drift figure is small and suspiciously *uniform in magnitude* across civs,
suspect the **precision of one side of the subtraction** before believing a movement. A
rounding artefact is ±0.0005 per operation, so it shows up as a constant, not a trend. Recompute
the stored field from its own increments to separate "the counter moved" from "the field is
rounded".*

### 2. THE TAIL IS A **PER-SESSION CONSTANT** — RE-CONFIRMED AT **27 CLUSTERS / 80 ROWS EACH**

Clustering the **2160** current-format rows by `ts` gap (> 30 s) gives **27** session
clusters, every one exactly **80** rows with exactly **one** distinct 162-char tail. The tail
pool across history is **13** strings, shared identically by all 8 civs.

*Rule: extract the tail from the most recent 80-row cluster and reuse it for all 80 rows.
Never paraphrase it — the byte count is load-bearing (38 + 162 + continuation).*

### 3. A **346-CHAR** BODY IS MID-BAND, AND THE CONTINUATION CAN END ON A **WORD BOUNDARY**

`target - 38 - 162 = 149` for a 349-char target. A first build used the naive 181-char
continuation -> body **381**, **12 above** the 369 ceiling, and the mock's own guard fired
before any row was written. Trimming to the last space before 149 gives **146** -> body
**346**, comfortably mid-band and readable.

*Rule: put the length assertion **inside the mock** so an out-of-band body fails at startup
rather than after 80 bad rows. When trimming, back off to the last space, not a hard slice —
the continuation is prose, not a byte buffer.*

### 4. THE SEED ALGORITHM RE-VERIFIES AT **2160/2160** OVER THE FULL LEDGER

The canonical algorithm (raw MD5 byte `d[0] % 4` for the seed index, contiguous 4-char slice,
`h[8:12]` for colour, three string components for the figure) recomputed over **every**
current-format row in the whole ledger: **2160/2160 exact, 0 mismatches**. The 80 new rows
this session: **80/80 exact**.

*Rule: verify against the **whole** ledger before the run, not against your own fresh rows —
the latter is a tautology when the mock and the verifier share a mistake.*

### 5. THIS SESSION: AGREEMENT **0/5**, ALL **DOWN**-GRADES, AND A **TWO-AXIS** RUN LOW

Agreement **0/5 (0 %)**, **5 down-grades, 0 up-grades**; deltas 0.2267 / 0.1500 / 0.0667 /
0.1533 / 0.4000 (max **0.4000**, no cliff). `civ-precise` won 4/5, `civ-formal` 1/5, while the
`avg_score` argmax was `civ-poetic` on **5 of 5**. Run low `civ-therapist` (avg **1.4433**)
with quality **0.6170** and alignment **1.0330** both at the fleet low — a **two-axis** collapse.

*Rule: the up-grade count is pinned at 0 **by construction** (the chooser sees only
`content_preview[:150]`, never `avg_score`), so every disagreement is a down-grade. Report
agreement and the up/down split as two numbers and state the structural reason, or a 0 %
agreement series reads as a regression when it is a property of the wiring.*

### 6. THE AXIS DOMINANCE HELD AT **2.05x** — ALIGNMENT AGAIN

Alignment spread **2.4100** = **2.05x** the `avg_score` spread (1.1733); quality 1.4400
(1.23x), novelty 0.6600 (0.56x).

*Rule: report the axis signature **for this session**. The holder rotates; the axis does not.*

### 7. `civ-grounded` HELD THE LIFETIME LOW FOR THE **101st** CONSECUTIVE SESSION

Relevance **2209.77**, relevance-per-sim **1.202** (lowest of 8), 8th of 8. `civ-therapist`
was the run low but sits 2nd-lowest on lifetime relevance. No civ is near extinction
(threshold `relevance < -10`); `extinction_and_birth()` does not run in a non-`--loop`
invocation and all 8 civs remain **generation 1**.

*Rule: "lifetime low" and "run low" are different civs most sessions. Report both, and report
the extinction distance explicitly so a low-relevance civ is not read as a dying one.*

## Session 238 additions (2026-10-25)

### 1. THE TAIL IS A **PER-SESSION CONSTANT** — AND THE POOL IS **13** TAILS SHARED BY ALL 8 CIVS

Measuring the tail across the whole current-format ledger (2080 rows) gives **13 distinct
tail strings**, every one exactly **162** chars, and the set is **identical for all 8 civs**
(`all civs share identical 13-tail set: True`). Each `(civ, prompt)` pair carries **13**
distinct tails across history, so the tail is **not** keyed to `(civ, prompt)`.

Clustering the 2080 current-format rows by `ts` gap (> 30 s) gives **26 sessions**, and
**every** session uses **exactly one** tail across all **80** of its rows. The tail rotates
per session and is otherwise free.

*Rule: the tail is a session-level constant. Do not try to derive it from `(civ, prompt)`
or from a request counter — it is neither. Extract the current session's family from the
ledger (the most recent 80-row cluster) and reuse it for all 80 rows.*

### 2. THE COUNTER GAP MUST BE SUMMED OVER THE **FULL** LEDGER — A SIM-ONLY SUM INVENTS A REGRESSION

A first pass compared the post-run `relevance` against the sum of the **new rows only**,
excluding the 5 competition rows the ledger also contains. That made the gap appear to
move by **11-21 points for every civ** — which would have been published as "the counter
gap is accumulating", a fabricated regression.

The ledger stores **both** sim-phase rows and competition rows; `relevance` counts only the
former (line 207 adds `avg_score` inside `run_simulation`), so the two quantities can never
be equal by construction. Summed over the **full** history the gap is stable to **3.3e-03**,
exactly as the session-237 table documents.

*Rule: the gap is `relevance - sum(avg_score over the ENTIRE ledger)`. Never over a subset
of rows. A subset changes the gap by design and manufactures a fake drift. This is the same
class of error as session 231's "a re-derivation is not a correction".*

### 3. THE COMPETITION PHASE ISSUES **NO** PROVIDER REQUESTS OF ITS OWN

The 80 new ledger rows are written by the sim phase. `civilization_competition()` calls
`run_simulation` again, but the batch already holds those same rows, so the mock served
**161** requests total — not 161 + 40. The session-237 report expected **89** (80 sims + 5
competitions + 4 pre-flight) against a ledger that gained 80 rows: a decomposition that
cannot reconcile.

*Rule: expected mock requests = `preflight + repeat + (ledger row delta)`. The competition
phase re-uses the sim rows. Derive the count from the ledger delta (80), never from the
number of phase transitions.*

### 4. `--filter=blob:none --no-checkout` IS THE CLONE FORM THAT ACTUALLY WORKS

The workspace NAS was at 100 % quota again, so the clone went to the overlay. A
`--depth 50` full clone pulled **1.2 GB** and was killed mid-transfer; `--depth 1` with a
sparse cone still fetched the whole tree (session 217's note). The form that worked was:

```
git clone --depth 1 --filter=blob:none --no-checkout <url> /tmp/cfd-meta
git sparse-checkout set cellular-first-design/code/civilizations
git checkout
```

*Rule: `--filter=blob:none --no-checkout` first, then `sparse-checkout set` the inner path,
then `checkout`. Note the sparse path needs the **subdirectory** (`cellular-first-design/...`)
because the repo root contains it — `code/civilizations` alone matches nothing and the
checkout silently succeeds with an empty tree.*

### 5. THE **SWEEP RETURNS** AFTER A 2-2-1 SPLIT — THE HOLDER ROTATION IS NOT A LAW

`civ-precise` took **5/5** this session, one session after the 2-2-1 split of session 237
ended a 19-session sweep run. `civ-therapist` took the run low in **6 of the last 7**
sessions while `civ-grounded` held the lifetime low for the **100th** consecutive session.

*Rule: a winner-streak is a description of history, not a prediction, in **either**
direction. A split is not evidence of a new regime and a sweep is not evidence of a law.*

### 6. THE **ALIGNMENT AXIS** DOMINATED AGAIN AT **2.40x** — AND THE RUN LOW WAS A **THREE-AXIS** COLLAPSE

Alignment spread **2.1460** = **2.40x** the `avg_score` spread (0.8960); quality 0.82x,
novelty 0.27x. The run low `civ-therapist` (avg **1.1673**) held quality **0.4670**,
novelty **2.3480** and alignment **0.7220** — **all three** at the fleet low, a
three-axis collapse where sessions 225/227 were two-axis and 237 was two-axis.

*Rule: report the axis signature **for this session**. The holder rotates; the alignment
axis does not. The number of collapsed axes is itself a per-session quantity.*

### 7. A **ONE-SHOT NFS `ls` FAILURE** MAY NOT REPRODUCE — REPORT ONLY WHAT WAS OBSERVED

The session-237 bridge needed a stale-attribute-cache retry; this session's `ln -sfn` was
followed by a successful `ls -la` on the **first** call. The retry recipe remains the right
defence, but it must not be reported as a fact unless it is observed in that session.

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

### 1. THE TASK PROMPT'S REPO SLUG IS WRONG — `ai-writings/cellular-first-design` 404s

The upstream is **`SuperInstance/AI-Writings`**. The `ai-writings` org is a *different* org
holding one unrelated repo (an AI-writing tool list). The GitHub API is case-insensitive on
the owner+repo path, so `SuperInstance/ai-writings` and `SuperInstance/AI-Writings` are the
same repo — but the *owner* is `SuperInstance`, not `ai-writings`.

*Rule: a 404 on the slug named in the task prompt is a **slug** defect, not a missing repo.
Locate the file with `GET /search/code?q=civilization_orchestrator+in:path`, which survives
core-quota exhaustion and returns the owning repo directly.*

### 2. A BACKGROUND `git clone` CAN DIE SILENTLY AND REMOVE ITS OWN DIRECTORY

Running `setsid nohup git clone ... &` produced a log containing only `Cloning into ...`,
then the directory **vanished** — the clone had failed and cleaned up, and the log held no
error. A foreground clone with a long timeout succeeded immediately.

*Rule: after a backgrounded clone, **assert the directory still exists** before using it.
A background clone that leaves an empty log and a missing directory is a silent failure —
poll for the directory, not for the log.*

### 3. THE LEDGER'S COLOUR FIELD HAS **TWO** FORMATS — BOTH RECOMPUTE

The current-format rows carry the colour **with** a `#` prefix; older generations carry it
**without**. A strict equality check against `h[8:12]` fails 2000/2000 while the values are
in fact identical.

*Rule: when fitting an algorithm against a ledger that spans generations, accept the
**value** and normalise the presentation, or you will report a 0 % match on a perfect fit.
Always print the first mismatching row — it distinguishes "wrong algorithm" from
"right algorithm, wrong format" in one look.*

### 4. THE 38/162/200 GEOMETRY IS APPROXIMATE — THE INVARIANT IS A **200-CHAR PREVIEW**

The skill file says the header is 38 and the tail 162; the newest rows have a **163**-char
tail (and some older generations 164). The header measures **38** exactly (37 + the space
before the tail). The stable invariant is `content_preview` == **200** chars, always.

*Rule: assert the *preview length* (200) and the *body band* (332-369) — never a fixed
header/tail split, which drifts by a char between generations.*

### 5. THIS SESSION'S NUMBERS

- Pre-flight **8/8 PASS** on the **first** build (40/40 recomputed md5, 40/40 distinct seeds,
  40/40 distinct previews, all bodies 349). Run verification **18/18 PASS**.
- **80** new rows (+10 x 8), `meta_log` 903 -> **908**, `Winner:` **5**, all `civ-precise`.
- **80/80** distinct `(q,n,a)` triples, 0 JEV errors, 0 fallbacks, 80/80 `provider=zai`.
- Chooser/argmax agreement **2/5 (40 %)** — 3 down-grades, 0 up-grades; all 3 marginal
  (max **0.1067**), the narrowest down-grade set of the series. Up-grades across the whole
  211-234 series: still **0**.
- Run low **`civ-therapist`** (avg **1.7533**; fleet-low run alignment **1.62**, and the
  fleet-low lifetime alignment **1.1813**). Run high `civ-poetic` (2.4233).
- Lifetime low **`civ-grounded`** (**2122.93**) for the **98th consecutive session**; lifetime
  quality **0.5318** is the fleet low and lifetime alignment **1.2777** is 2nd-lowest, 2.6x
  behind `civ-precise` (2.3291) => a *voice* failure, not a prose failure. Lifetime novelty
  (1.8051) is 6th of 8 — check the rank, not the impression.
- Counter gap **byte-identical** to session 230 (max drift **0.0000**): grounded -84.3467,
  therapist -42.1133, engineer -44.2433, mythic -51.1100, formal -85.5267, whimsical
  -173.1433, precise -32.6333, poetic -96.8033. Fixed, not accumulating.
- `civ-poetic` 1st on lifetime `avg_score` (1.7118) / `quality` (0.9130) / `relevance`
  (3003.28) but **last on `win_rate` (0.007)** — won 0/5. `civ-precise` best `win_rate`
  (0.697) and highest lifetime alignment (2.3291), swept 5/5.
- Run-level JEV scores are **higher** than session 230 (run avg 1.75-2.42 vs 0.50-1.14) — a
  scorer level shift for this batch, not a civ effect.
- Extinction risk **NONE** (floor -10, lowest +2122.93 = **212x**). Registry 8, `max_civs` 12.

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

## Session 208 (2026-10-25) — THE STREAK COUNTER IS RE-MEASURED, AND THE AXIS NAMES THE COHORT, NOT THE HOLDER

**Run clean (session 208).** per-civ delta = **+10** x 8 = **80 new rows**,
`meta_log` D = **+5** (773 -> 778), `Winner:` lines = **5**, **80/80** rows
`provider=zai`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0
fallback triple, **80/80** rows match an independently recomputed seed+color+figure,
**40/40** distinct seeds (message-level), **0** `(civ,prompt)` combos carrying >1
seed, per-prompt **8/8** distinct seeds AND previews on all 5 prompts, relevance
delta == sum(`avg_score`) **8/8 exact** (max residual **3.73e-13**), wins **+5** /
losses **+35**, meta-vs-ledger **0/40** mismatches, registry 8 all gen 1, extinction
**NONE** (lowest +1666.40 = **166.6x** the floor). **Pre-flight PASS on the FIRST
build (12/12).** **28/28 assertions PASS.**

### NEW — the down-grade streak counter must be re-derived, and the series now OSCILLATES

Session 199 read **0/5 agreement, 5 down**; session 207 read **4/5, 1 down**; this
session reads **1/5 (20 %), 4 down, 0 up**. The sequence 199 -> 207 -> 208 is
**0/5 -> 4/5 -> 1/5**. `civ-precise` won all 5 competitions and was the argmax on
only **1 of 5**; `civ-engineer` and `civ-poetic` were the argmax on 2 each and won 0
each.

*Rule: a streak counter is a MEASUREMENT, not a hypothesis. Re-derive the direction
count from the current session's own `meta_log` every session and report agreement and
direction as two separate numbers. This is the third independent demonstration of the
rule (session 198 declared a 16-session streak "over"; session 199 reversed it; this
session reverses session 207's recovery).*

### NEW — the AXIS names the low-relevance COHORT; the holder is the cohort's lowest `avg_score`

The run-level low rotated to **`civ-therapist`** (run `avg_score` **1.5237**,
`quality` **1.0970** fleet-low). But `civ-whimsical` has a **WIDER** alignment gap
(**-1.5650** vs therapist's **-1.5320**) and is **not** the holder, because its
`avg_score` (**1.5740**) is higher. Meanwhile the three highest-`avg_score` civs
(precise, engineer, formal) are the three within **-0.033** of the alignment ceiling.

*Rule: predict the low-relevance COHORT from the axis (the alignment tail beyond
about -1.5), then read the single HOLDER from the run's own rows. Do not predict the
holder from the previous session's report, and do not assume the widest gap names the
holder.*

### NEW — the counter-gap check is the cheapest merge-integrity check in the series

For each civ, `gap = relevance_score (culture.json) - sum(avg_score over the ledger)`.
Compare the gap at the **baseline commit** against the gap in the post-run tree: it
must be **byte-identical**. This session: grounded -84.35, whimsical -173.14, formal
-85.53, poetic -96.80, precise -32.63, mythic -51.11, therapist -42.11, engineer
-44.24 — **all 8 UNCHANGED**. A non-zero gap is normal (historical merges); a gap that
*moves* is the defect. This catches a partially-written or double-counted row that
every row-count assertion would miss.

### NEW — the figure field is 3 string components of 5 chars, and the header is a CONSTANT 44

With the figure fixed at **18 chars** (three 5-char string components, space-joined,
padded — fix (g) done as strings, not a division) the mock header
`[mock-zai <4-hex>] #<6-hex> <figure>. ` is a **constant 44 chars**, so a **299-char**
fixed tail puts the body at **343** — inside the 332-369 band on the **first** build.
Third consecutive session in a row the band is solved algebraically rather than by
iterating the template.

### Re-confirmations (this session)

- The prompt's path did not exist (**19th consecutive occurrence**); clone
  `SuperInstance/AI-Writings` to **`/tmp`** (NAS EDQUOT kills a clone into
  `/workspace`) and bridge the **inner `cellular-first-design/code`** by symlink —
  verified by inode identity `129:3670` both sides + `os.path.samefile()` -> `True`.
- The upstream owner is a **user** account: `GET /orgs/ai-writings/repos` **404s** while
  `GET /user/repos` finds it; the GitHub API is case-insensitive, so the `ai-writings`
  slug resolves to `AI-Writings`.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401**
  `token expired or incorrect` (**81st session**) => endpoint healthy, credential absent.
  `ZAI_URL_OVERRIDE` alone is dead code — Control B needs **both**.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`; JEV live at
  `jev-1.14.0`; **0** fallback triples.
- Pre-flight check 10 (**repeat-same-message => identical response**) is the only check
  that can catch fix (f); the other 11 pass on a mock with fix (f) broken.
- Baseline pinned to the **pre-run commit** `c5078bd` and read from the **git blob** —
  never from `HEAD` after the run is committed, and never from a remembered count.
- `gh` is not installed (**22nd session**); `GIT_SSL_NO_VERIFY=1` required for
  fetch/push; push to the explicit token URL and verify with `git ls-remote`.

## Session 199 (2026-10-25) — the DOWN-GRADE STREAK RE-BREAKS, and one session is NOT a trend

**Run clean (session 199).** per-civ delta = **+10** x 8 = **80 new rows**,
`meta_log` D = **+5** (728 -> 733), `Winner:` lines = **5**, **80/80** rows
`provider=zai`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0
fallback triple, **80/80** rows match an independently recomputed seed+color+figure,
**40/40** distinct seeds (message-level), **0** `(civ,prompt)` combos carrying >1
seed, per-prompt **8/8** distinct seeds AND previews on all 5 prompts, relevance
delta == sum(`avg_score`) **8/8 exact** (max residual **9.84e-13**), wins **+5** /
losses **+35**, meta-vs-ledger **0** mismatches over 40 comparisons, registry 8 all
gen 1, extinction **NONE** (lowest +1517.95 = **152x** the floor).
**Pre-flight PASS on the FIRST build (10/10).** **27/27 assertions PASS.**

### NEW — a "regime change" observed in ONE session can be fully reversed by the NEXT

Session 198 reported the 16-session down-grade streak as **broken** (3/5 agreement,
1 up-grade) and correctly cautioned that "one session is not a trend". Session 199 is
that next session, and the streak is back **harder**: **0/5 (0 %) agreement, 5
down-grade, 0 up-grade** — the worst session in the series. `civ-poetic` was the
`avg_score` argmax on **5 of 5** prompts and won **0 of 5**; `civ-precise` was never
the argmax and won **5 of 5**.

*Rule: when you report a streak as broken, the next session MUST re-derive the
direction count from its own log rather than assuming the new regime holds. A
streak counter is not a hypothesis — it is a measurement, and it is re-measured
every session. Never write "the down-grade streak is over" in a report; write
"the down-grade streak was 0 this session, re-derive next session".*

### NEW — the run-level low holder can be a civ that has NEVER held it before

The run-level low rotated to **`civ-engineer`** this session (run `avg_score` 1.4413,
`alignment` 0.8740 fleet-low) — the **18th distinct holder in 18 sessions**. Sessions
190-198 rotated through `therapist`/`mythic`/`whimsical`; `civ-therapist`, which held
it in 7 of the last 9 sessions, fell to **6th of 8** this run.

*Rule: do not predict the run-level low holder from the previous session's report.
Read this run's own rows. The holder rotates; the AXIS it rotates on does not — the
alignment spread was **2.1830** this session, the widest in the series.*

### NEW — the "lifetime low" and the "run-level low" have been DIFFERENT civs for 4 sessions running

`civ-grounded` holds the lifetime low (**1517.95**, 71st consecutive session,
`relevance_per_sim` 1.055, lifetime `win_rate` **0.099** = 3rd-best in the fleet) but
was only **7th of 8** on this run's `avg_score` (**1.7207**), with a **quality-led**
signature (`quality` 0.8000 fleet-low, `novelty` 2.7460 **fleet-high**). The run-level
low (`civ-engineer`) is 6th of 8 lifetime.

*Rule: report the axis per civ, never a single "the low civ". And keep the two axes
separate in the write-up: relevance is an accumulation; `win_rate` is a SELECTION
metric. A civ can be lowest on relevance and 3rd-best on selection at the same time.*

### Re-confirmations (this session)

- The bridge symlink must point at the **inner** `cellular-first-design` directory
  (verified by inode identity `129:12601` both sides + `os.path.samefile()`).
- Cloning into `/workspace` dies on `.git/description` with `Disk quota exceeded`
  (NAS EDQUOT, **19th session**); the same clone into `/tmp` succeeds.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or
  incorrect`** (**73rd session**) => endpoint healthy, credential absent.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`; JEV live at
  `jev-1.14.0`; **0** fallback triples.
- `ZAI_URL_OVERRIDE` alone is dead code — the `ZAI_TOKEN` gate returns `None` first.
  Control B needs **both**.
- Pre-flight check 8 (**repeat-same-message => identical response**) is the only check
  that can catch fix (f); the other 9 pass on a mock with fix (f) broken.
- Response body band **332-369** (measured **366**), cultural-prompt band **167-209**
  (measured **167-209** from the REAL `culture.json` files).
- The **8 fixes (a-h)** rebuild cleanly from the algorithm block; pre-flight passed
  **10/10 on the FIRST build**.

## Session 193 (2026-10-25) — THE 12-SESSION DOWN-GRADE STREAK BROKE, and "distinct seeds" is a MESSAGE-level invariant

**Run clean (session 193).** per-civ delta = **+10** x 8 = **80 new rows**,
`meta_log` D = **+5** (698 -> 703), `Winner:` lines = **5**, **80/80** rows
`provider=zai` with the `[mock-zai` prefix, **0** rows with a JEV `error` key, **0**
rows with the 2.0/2.0/2.0 fallback triple, **80/80** rows match an independently
recomputed seed+color+figure, **40/40** distinct seeds (message-level), **0**
`(civ,prompt)` combos carrying >1 seed, per-prompt **8/8** distinct seeds AND previews
on all 5 prompts, **80/80** distinct `(q,n,a)`, relevance delta == sum(`avg_score`)
**8/8 exact** (max residual **6.6e-13**), wins **+5** / losses **+35**, meta-vs-ledger
**0** mismatches, registry 8 all gen 1, extinction **NONE** (lowest +1406.82 = **141x**
the floor). **Pre-flight PASS on the FIRST build (13/13).** **29/29 assertions PASS.**

### NEW — the DOWN-GRADE STREAK IS BROKEN. Re-base it to 0.

Chooser vs `avg_score` argmax = **5/5 (100 %)** agreement, **0** down-grade, **0**
up-grade. `civ-precise` won all 5 competitions *and was the argmax on all 5*. This ends
a **12-consecutive-session** run in which **every** chooser/argmax disagreement was a
down-grade (sessions 181-192).

*Rule: a streak statistic is a property of the series, and when the series breaks, the
streak counter resets to 0 — it does not carry forward "12" into the next report.* The
standing suspicion (**the `best_civ` criteria map `civ_id -> civ name` being read as a
quality signal**) is **not** disproven: a chooser that agrees with the argmax on every
prompt is exactly what a working chooser looks like, and the streak was a symptom of
*something*, not proof of the cause. Re-base, keep watching, do not conclude.

### NEW — "distinct seeds" is a MESSAGE-level invariant, not a ROW-level one

The natural check "all 80 new rows carry distinct seeds" **cannot pass**, and its
failure is **not a defect**. The seed is a function of the **message** (`civ` +
`prompt`); the orchestrator appends **10 rows per civ** (5 sims + 5 competition rows)
that span only **5 distinct prompts** per civ. So the 40 `(civ, prompt)` slots produce
**40 distinct seeds across 80 rows**.

Measured multiplicity distribution this session: **{3: 10, 2: 14, 1: 14, 4: 2}** — 12
seeds appear on 3 or 4 rows, exactly what `random.choice` over 5 prompts produces. A
`len(set(seeds)) == 80` assertion reports a false FAIL on a perfectly clean run.

*Rule: before asserting distinctness, ask **what the value is a function of**. Here it
is the message, so the distinctness count is bounded by the number of distinct
**messages** (40), not the number of **rows** (80). This is the row-count analogue of
the session-189 rule "assert distinctness against the GROUP SIZE, not the SAMPLE SIZE":
the group size is the number of distinct *inputs*, not the number of *observations*.*

The corrected check asserts three things at once: 40 distinct seeds; exactly one seed
per `(civ, prompt)` slot; and each seed's multiplicity equal to its slot's row count.

### NEW — the BRIDGE must point at the INNER `cellular-first-design` directory

Upstream `SuperInstance/AI-Writings` has a `cellular-first-design/` **subdirectory** in
its root, so a checkout lands content at
`<root>/cellular-first-design/cellular-first-design/code/…`. The orchestrator's
hardcoded `CIVS_DIR` wants `<root>/code/…`, so the symlink must target the **inner**
directory. A bridge aimed one level too high fails with a bare
`FileNotFoundError: 'civilizations.json'` and reads as a missing repo.

Also: `git sparse-checkout disable` after a **cone**-sparse checkout leaves a
**nested duplicate** tree. `git status` then reports the outer tree as clean while the
real content sits one level deeper — so "the tree is clean" is not the same as "the
content is where I think it is". Verify with `find <root> -maxdepth 3 -not -path '*/.git*'`.

### Findings

- **`civ-grounded` remains the lifetime low — 65th consecutive session.** Lifetime
  `relevance` **1406.82** (last of 8), `relevance_per_sim` **1.020** (lowest in the
  fleet), `win_rate` **0.103** — **3rd-best**. Run `avg_score` **1.7397** (6th of 8),
  `quality` **1.0800** (2nd-lowest), `alignment` **1.7670** (5th), novelty **2.3720**
  (mid-pack) ⇒ the deficit is **quality and alignment, not novelty**. Lowest relevance
  **+1406.82 = 141x** the −10 floor.
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.5117**,
  `alignment` **1.1150** lowest, `quality` **1.0540** lowest) — a **12th different civ
  in 12 sessions**, while its lifetime standing is 7th of 8. *The holder rotates; the
  axis does not.*
- Run spreads: `alignment` **1.8460** (widest, and the widest of the last three
  sessions) › `avg_score` **0.7537** › `quality` **0.5790** › `novelty` **0.1470**.

### Re-confirmations (this session)

- NAS EDQUOT total (**19th session**) — 600 G/600 G, 0 bytes free; `cp` into
  `/workspace` fails with "Disk quota exceeded" and leaves **0-byte files that `ls`
  still lists**. Clone to the overlay (28 G free) and bridge by symlink.
- z.ai **401** `token expired or incorrect` (credential gap, endpoint healthy) —
  **67th session**. **JEV HTTP 200** on a well-formed body, disclosing **`jev-1.14.0`**;
  **0 fallback triples**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code behind the token gate).
- `gh` not installed (**21st session**) — `GET /user/repos` with `GITHUB_TOKEN`;
  `GET /search/code?q=…` survives core-quota exhaustion; the GitHub API is
  case-insensitive.
- The mock must return an **OpenAI-shaped envelope**; the body-length target is
  computed from the **assembled** string (landed **360**, band 332-369) and the
  cultural-prompt band is measured from the **real on-disk** `culture.json` files
  (**167-209**) — never a hand-typed fixture.
- Take the baseline from `git show HEAD:.../culture.json`, **unrounded**; max residual
  this session **6.6e-13**.
- **NEW — the verifier's baseline must be PINNED to the pre-run commit, not `HEAD`.**
  After the run is committed, `HEAD` *is* the run's own commit, so the baseline becomes
  the post-run state and every delta assertion reads **0** instead of the expected
  value. Re-running the battery post-commit against `HEAD` produced **25/29** with
  exactly four failures — `meta_log delta` (703 -> 703), `relevance delta` (resid
  **22.65**), `wins/losses` (7/8, 1/8) and `simulations_run` (0) — **all four being
  "the baseline moved to my own commit", and none being a data defect.** Pin
  `BASE_COMMIT` to the pre-run sha (`3a16971a` here) and the same battery returns
  **29/29**. *A verifier that reads its baseline from `HEAD` is only correct exactly
  once — before you commit.*
- Mock teardown: kill by **PID captured from `ps`**, never `pkill -f mock_zai`
  (self-matches the calling shell).



## Session 218 additions (2026-10-25)

### 1. THE CURRENT-GENERATION MOCK ALGORITHM, RE-DERIVED FROM THE LEDGER — 480/480 EXACT

The SKILL file documents the **older** `[mock-zai seed=XXXX]` header format, not the current
one. The current format is `[mock-zai <4hex>] #<4hex> <4hex>/<4hex>/<4hex>.` and the
canonical algorithm is:

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4
seed   = h[(i*2)%8 : (i*2)%8+4]     # CONTIGUOUS 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

`cultural_prompt` is exactly the string the orchestrator builds in `run_simulation()`:
`You are a voice in the tradition of "{name}".\nYour tenets: {tenets joined by ", "}.\nYour voice: {voice}.\n\n{prompt}`.

**The `i = d[0] % 4` step is the part that is easy to miss.** `color` and `figure` sit at
`h[8:12]` and `h[12:24]` and are trivially found. The **seed** is NOT at a fixed offset:
`h[0:4]`, `h[2:6]`, `h[4:8]` and `h[6:10]` each match only ~30 % of rows, and a
sample of one row will happily land on any of them. *Derive the seed by fitting
`i = d[0] % 4` and then the `(i*2)%8` slice, not by scanning offsets.* Verified 480/480
against the 6 most recent sessions of the ledger.

### 2. THE CURRENT-GENERATION TAIL IS **PER-SESSION**, NOT PER-MESSAGE

The ledger holds exactly **3** distinct 163-char tails. A merged-by-`ts` run-length
encoding of all 480 current-format rows gives **`C×80, B×160, A×240`** — i.e. one tail per
session (6 sessions detected at exactly 80 rows each, matching 8 civs × 10 rows), and
**every** civ uses all three across sessions.

*Rule: a tail is a mock configuration for the session, so any one of the three is valid.
Do not go looking for a per-message tail selector — there is none, and hunting for one
burns an hour.*

### 3. `simulations_run` ADVANCES BY **+10**, AND `losses` = 5 − wins

`run_simulation()` increments `sims_run` on **every** simulation, and the competition phase
writes one row per civ per prompt. A civ therefore ends the run with 5 sim-phase rows
**plus** 5 competition rows, and `simulations_run` advances by **10** while the ledger also
grows by 10.

`civilization_competition()` awards a loss only to civs that **participated**, so a sweep
winner records **0 losses and 5 wins** — not a flat "+5 losses".

*Both cost me a red verification battery on a perfectly clean run. Derive the expected
counter delta from the code path, not from the number of prompts: the competition phase
participates in the same counters as the sim phase.*

### 4. THE `ls -la` VERIFICATION THE PROMPT ASKS FOR IS THE WEAKEST ONE

"Verify with `ls -la` that simulations.jsonl files have new entries" is satisfied by an
mtime change on all 8 files — which a run that wrote **0** rows would also satisfy if it
touched the files. The discriminating check is the **row-count delta** (+10 each = 80)
plus the git-blob baseline for the counter deltas. *Use `ls -la` to answer the question
asked; use the row-count delta to answer the question meant.*

---

## Session 189 (2026-10-25) — THE TWO LENGTH BANDS, AND A VERIFIER THAT FAILS ITSELF

**Run clean (session 189).** per-civ delta = **+10** x 8 = **80 new rows**,
`meta_log` D = **+5** (678 -> 683), `Winner:` lines = **5**, **80/80** rows
`provider=zai` with the `[mock-zai` prefix, **0** rows with a JEV `error` key, **0**
rows with the 2.0/2.0/2.0 fallback triple, **80/80** rows match an independently
recomputed seed+color+figure, **40/40** distinct seeds, **0** `(civ,prompt)` combos
carrying >1 seed, per-prompt **8/8** distinct seeds AND previews on all 5 prompts,
**80/80** distinct `(q,n,a)`, relevance delta == sum(`avg_score`) **8/8 exact**
(max residual **3.9e-13**), wins **+5** / losses **+35**, meta-vs-ledger **0** mismatches,
registry 8 all gen 1, extinction **NONE** (lowest +1338.36 = **134x** the floor).
**Pre-flight PASS on the THIRD build.** **29/29 assertions PASS.**

### NEW — the pre-flight's two length bands are DIFFERENT bands, and the response one must be measured

The gate needs a *response* body band of **332-369** chars and a *cultural-prompt* band of
**167-209** chars. These are unrelated numbers and asserting one against the other is
foolish. This session's builds went **267 -> 531 -> 360**: the first was too short (the
seed can be cut out of the orchestrator's 200-char `content_preview` truncation), the
second was too long (the preview fills with prose the scorer never sees).

*Rule: compute the target length from the ASSEMBLED string, not from an intuition about
how many sentences to add. The `[mock-zai seed=XXXX] ... colour CCCC ... figure
F/F/F ...` prefix is ~90 chars of VARIABLE width (the figure alone is 14), so "one more
sentence" is not a length control. Assemble the string in a scratch script, measure, and
then trim the tail to land mid-band.*

### NEW — a per-prompt group holds ROWS, but the distinctness target is the CIV COUNT

The sim phase draws its prompt at random from the same 5 competition prompts, so a
per-prompt group in the 10 new rows holds **11-20 rows** for only **8 civs** — the same civ
repeats 1-4 times, each time with the **same** seed (the seed is a function of the
message, and the message is civ+prompt, not the row). A verifier written as
`len(set(seeds)) == len(rows)` therefore reports a false FAIL on a perfectly clean run.
This session: 11, 20, 18, 14, 17 rows per prompt, **8** distinct seeds each.

*Rule: assert distinctness against the GROUP SIZE (8 civs), not the SAMPLE SIZE. The row
count is a property of the run schedule; the civ count is a property of the data.*

### Findings

- **`civ-grounded` remains the lifetime low — 61st consecutive session.** Lifetime
  `relevance` **1338.36** (last of 8), `relevance_per_sim` **1.000** (it has crept back
  to exactly 1.000), `win_rate` **0.107** — **3rd-best in the fleet**. Run `avg_score`
  **1.3070**, `alignment` **0.7900**, `quality` **0.4290**, novelty **2.7020** (**1st of
  8**). Lifetime: `avg_score` 1.0295, `alignment` 1.0761, `quality` 0.3997 — last of 8 on
  all three. Axis gaps: alignment **1.0696** vs quality **0.3453** = **3.10x wider** ⇒ a
  **voice** failure. Lowest relevance **+1338.36 = 134x** the −10 floor.
- **THE RUN-LEVEL LOW ROTATED to `civ-therapist`** (run `avg_score` **1.2537**,
  `alignment` **0.5240**, `quality` **0.5600**) — a **9th different civ in 9 sessions**,
  while its lifetime standing is 7th of 8. Run axis gaps: alignment **2.3390** vs quality
  **0.7920** = **2.95x wider**. *The holder rotates; the axis does not.*
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — the **10th consecutive session** in
  which a disagreement is a *down*-grade. `civ-precise` took 4/5 (the 5/5 sweep of session
  188 broke; `civ-engineer` won the ternary prompt). `civ-poetic` was the argmax on **4/5**
  prompts and won **0/5**. The largest disagreement in the series (**+0.7300**) hands the
  ternary prompt to `civ-engineer`, **0.73 below** the leader. **The `best_civ` criteria
  map (civ_id -> civ name) is the suspect**, not the quality signal.
- Run spreads: `avg_score` 0.9840, `alignment` **2.3390** (widest), quality 0.7920,
  novelty 0.1140.

### Re-confirmations (this session)

- NAS EDQUOT total (**18th session**) — 600 G/600 G, 0 bytes free; clone to `/tmp`
  (overlay, 22 G free) with `--filter=blob:none` + sparse-checkout `cellular-first-design`;
  bridge the **clone root**; verify with `stat -L -c '%d:%i'` on both sides (here
  **129:3668** on both).
- z.ai **401** `token expired or incorrect` (credential gap, endpoint healthy) —
  **63rd session**. **JEV HTTP 200** on a well-formed body, disclosing **`jev-1.14.0`**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code).
- `gh` not installed (**20th session**) — `GET /user/repos` with `GITHUB_TOKEN`; the
  GitHub API is case-insensitive.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout redirected **and**
  `< /dev/null`, then poll `ps` + the log.
- `git status --porcelain` = **18 modified** (8 civs x 2 files + `leaderboard.json` +
  `meta_log.jsonl`).
- **NEW — `pkill -f` self-matches the calling shell.** `pkill -f "mock_zai.py 8181"`
  matched the bash `-c` command line that contained the same string, killing the shell
  and returning **empty tool output** — indistinguishable from a hung command.
  *Kill by PID captured from `ps`, or use a pattern that cannot appear in your own
  command line.*

---


## Session 184 (2026-10-25) — THE NAS SILENTLY TRUNCATES TO 0 BYTES; `ls` IS NOT EVIDENCE

**Run clean (session 184).** per-civ delta = **+10** x 8 = **80 new rows**,
`meta_log` D = **+5** (653 -> 658), `Winner:` lines = **5**, **80/80** rows
`provider=zai` with the `[mock-zai` prefix, **0** JEV `error` keys, **0**
2.0/2.0/2.0 fallback triples, **80/80** rows match an independently recomputed
seed+color+figure, **40/40** distinct seeds, **0** `(civ,prompt)` combos carrying
>1 seed, **80/80** distinct `(q,n,a)`, relevance delta == sum(`avg_score`) **8/8
exact** against an **unrounded git-blob** baseline, wins **+5** / losses **+35**.
**Pre-flight 11/11 on the FIRST build.** **47/47 assertions PASS.**

### NEW — A FULL NAS MAKES WRITES RETURN EXIT 0 AND LEAVE 0-BYTE FILES

The `/workspace` NAS is at 600 G/600 G with 0 bytes free. On this session:

- `cp` of a real file into `/workspace` -> `cp: failed to close ...: Disk quota exceeded`
  (exit 1). Expected.
- `python3` `open(path,"wb").write(data)` -> **raises** `OSError [Errno 122] Disk quota exceeded`.
  Also expected.
- **`echo "probe" > /workspace/.probe2` -> exit 0, and the file is created as a
  0-BYTE file.** A binary search for "the largest write the NAS accepts" returns
  **0 bytes** — because *every* write is truncated to nothing.
- The same is true for a fresh subdirectory: `mkdir -p /workspace/out && echo hello >
  /workspace/out/t.txt` -> exit 0, `t.txt` is **0 bytes**, and `cat` prints nothing.

**The trap: `ls -la` shows the file present, with a plausible name, and the shell
reports success.** A verification pass that only checks `ls` output would conclude
the report was delivered. It is not. **Always assert a non-zero size after writing
(`os.path.getsize`), or compare an md5 against the source.** A 0-byte artifact that
"looks" fine is worse than a missing one, because it passes a naive existence check.

Corollary for deliverables: if the NAS cannot hold the bytes, **the git blob is the
durable copy**. Verify with `git cat-file -p HEAD:<path> | md5sum` against the
working-tree md5, and confirm the remote by `git ls-remote` (the REST commits API
kept returning 403 here, 2nd time this session). Do **not** report a workspace
delivery that you have not size-checked.

### The symlink bridge is still the only way to make the hardcoded path work

`civilization_orchestrator.py` hardcodes
`CIVS_DIR = /workspace/repos/ai-writings/cellular-first-design/code/civilizations`.
A real copy of the repo into `/workspace` fails on the quota. The bridge works
because a symlink costs ~0 bytes:

```
ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design
```

`test -ef` remains unusable in this sandbox (`binary operator expected`); verify
with `readlink -f` or by inode identity. This is the **12th consecutive** session
where the prompt path did not exist at start (workspace held only `.plugin-cache`).

### The seven mock fixes are stable — rebuild from the spec, never from memory

`ZAI_TOKEN` is still absent (62nd session) and the real z.ai endpoint returns
**401 `token expired or incorrect`** (endpoint healthy => credential gap, not an
outage). The Control B mock rebuilt cleanly with the canonical algorithm and
**passed 11/11 on the FIRST build**:

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4
seed   = h[(i*2)%8:(i*2)%8+4]                  # CONTIGUOUS 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # three STRING components
```

### Findings

- **`civ-grounded` remains the lifetime low — 57th consecutive session.** Lifetime
  `relevance` **1283.29** (last of 8), `relevance_per_sim` **0.996**, `win_rate`
  0.111. Run `avg_score` 1.5260, `alignment` 1.6500, `quality` 0.3710, `novelty`
  2.5570 (2nd of 8). The deficit is **alignment**, not prose: run alignment 1.6500
  vs run-best 2.5430, while quality 0.3710 is mid-pack. Lowest relevance
  **+1283.29 = 128x** the -10 extinction floor.
- **The run-level low ROTATED to `civ-therapist`** (run `avg_score` 1.3383,
  `alignment` 1.0250) — a **5th different civ in 5 sessions**, while its lifetime
  standing is 7th of 8. Axis gaps: alignment **1.5180** vs quality 0.4200 =
  **3.61x wider** => a **voice** failure. *The holder rotates; the axis does not.*
- **Chooser vs `avg_score` argmax: 3/5 (60 %)** — `civ-precise` swept **5/5**; both
  disagreements took the **lower**-scoring candidate.
- Run spreads: `avg_score` 0.5880, `alignment` **1.5180** (widest), quality 0.4200,
  novelty 0.1880.

---

## Session 182 (2026-10-25) — TWO 2-CHAR SLICES ARE NOT A 4-CHAR SLICE, and the 500 that hides behind an open socket

**Run clean (session 182).** per-civ delta = **+10** x 8 = **80 new rows**,
`meta_log` D = **+5** (643 -> 648), `Winner:` lines = **5**, **80/80** rows
`provider=zai` with the `[mock-zai` prefix, **0** JEV `error` keys, **0**
2.0/2.0/2.0 fallback triples, **80/80** rows match an independently recomputed
seed+color+figure, **40/40** distinct seeds, **0** `(civ,prompt)` combos carrying
>1 seed, **8/8** distinct seeds AND previews on all 5 competition prompts,
**80/80** distinct `(q,n,a)`, relevance delta == sum(`avg_score`) **8/8 exact**
against an **unrounded git-blob** baseline, wins **+5** / losses **+35**.
**Pre-flight 12/12 on the FIRST build.** **21/21 run-wide assertions PASS.**

### NEW — the canonical SEED is a CONTIGUOUS 4-CHAR SLICE, and the two forms are different values

Session 179 widened the seed from 2 to 4 hex chars because the 2-char slice had only
**16** reachable values over **40** slots. But it left the spec block reading
`h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]` — two 2-char slices
concatenated — while the headline said the slice should be `h[(i*2)%8:(i*2)%8+4]`.
**These are not the same value.** `h[0:4]` is not `h[0:2] + h[2:4]`.

This matters because the seed is a **reconciliation key**: a later session recomputes
the seed from the message and asserts the stored row matches. A row written under
the concatenated form does not reconcile against a recompute under the contiguous
form, and the failure looks like a **data defect** rather than an algorithm
mismatch. The 4-char width is satisfied either way, so the width check passes while
the value check fails.

*Rule: when a spec says "widen the slice", widen the SLICE. Do not pad, do not
concatenate neighbouring slices, and do not infer the new form from the old one —
a width assertion cannot distinguish three different 4-char renderings. Assert the
stored value against an independent recompute of the **documented expression**.*

### NEW — fix (g) fails SILENTLY behind an open socket

The spec's `figure = h[12:16] / h[16:20] / h[20:24]` is pseudo-code: `h` is a hex
**string**, so a literal transcription raises
`TypeError: unsupported operand type(s) for /: 'str' and 'str'`. The mock then
500s on **every** request **while the socket stays open**, so a port-open or a
bare-HTTP-200 liveness probe still looks healthy. The correct form is
`f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` — three **string** components.

*Rule: a liveness probe that only checks the socket is not a liveness probe. Send
a **real request body** and assert the response **content**, not the status line
alone. A 500 with a correct Content-Length is a valid HTTP response — the socket
test cannot see it.*

### NEW — the FIX LIST IS NOT THE SPEC

The "six fixes" checklist in the RUNBOOK was missing (g) for several sessions, and
the same list carried a seed form that contradicted its own headline. The
**algorithm block** and the **fix checklist** had drifted apart. This session read
the newest session's report and the skill file rather than the older checklist, and
found both discrepancies *before* the run.

*Rule: when rebuilding a mock from a checklist, re-derive the expected output from
the **canonical algorithm** and compare — do not trust the checklist's form
against the algorithm's form. Where the two disagree, the algorithm wins, and the
disagreement is itself worth writing down.*

### Re-confirmations (this session)

- **NAS EDQUOT is total** (600 G/600 G) while visibly empty: `git clone` into
  `/workspace` fails with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is
  exempt. **Verify bytes, not exit codes.**
- **Bridge symlink** must satisfy BOTH the requested script path and the script's
  internal hardcoded `CIVS_DIR`; `ln -sfn` into `/workspace/repos/ai-writings` +
  `[ -ef ]` -> `EF_OK` was sufficient here.
- **`TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`**; JEV liveness = HTTP 200 with
  `{"model":"jev-1.14.0", ...}` and a real score body.
- **`ZAI_TOKEN` still absent** from env and all 8 secrets; z.ai 401s (endpoint
  healthy, credential gap) — **61st session**. Control B needs **both**
  `ZAI_TOKEN` (placeholder) and `ZAI_URL_OVERRIDE`; the override alone is dead code.
- **Take the baseline from `git show HEAD:.../culture.json`, unrounded** — the
  leaderboard's 2-dp relevance is a display artifact and injects phantom residuals
  of up to +/-0.0067 per civ into the delta check.
- **`civ-grounded` remains the low-relevance civ — 56th consecutive session.** Last
  of 8 on lifetime `relevance` 1250.21, `relevance_per_sim` 0.985, `avg_score`
  1.0172, `alignment` 1.0698, `quality` 0.4010. Alignment gap 0.1367 vs quality
  gap 0.0432 = **3.16x** wider => a **voice** failure, not a prose failure.
  Lifetime novelty 1.5807 is 6th of 8.
- **The run-level low did NOT rotate** — `civ-grounded` was the run low (1.4323)
  *and* the lifetime low, the first agreement in four sessions (179: whimsical,
  180: therapist, 181: engineer, 182: grounded). **The rotation is not a law; do
  not code against it.**
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-precise` swept **5/5**. All
  four disagreements took the **lower**-scoring candidate (-0.107, -0.237, -0.190,
  -0.217). **Never treat `win_rate` as a quality metric.**
- **Counter gap** (ledger vs rounded leaderboard) is a **fixed** offset: per-civ
  delta **0.000000** for all 8 civs, unchanged from sessions 179-181.
- Run spreads: `avg_score` 0.6290, `alignment` **1.3270** (widest), quality 0.6430,
  novelty 0.1760.
- **Mock teardown**: kill by exact-argv match (wrapper **and** server pid), then
  prove the port closed (`curl` exit 7 = refused, `HTTP=000`). Never
  `pkill -f mock_zai` (self-match).


---

## Session 179 (2026-10-25) — the SEED SLICE width: a padded seed is not 4 chars of entropy

**Run clean (session 179, 58th consecutive clean mock).** per-civ delta = **+10** x 8 =
**80 new rows**, `meta_log` D = **+5** (628 -> 633), `Winner:` lines = **5**, **80/80**
rows `provider=zai` with the `[mock-zai` prefix, **0** JEV `error` keys, **0**
2.0/2.0/2.0 fallback triples, **40/40** distinct seeds, **0** `(civ,prompt)` combos
carrying >1 seed, **8/8** distinct seeds AND previews on all 5 competition prompts,
**80/80** rows match an independently recomputed message md5, meta-vs-ledger
`avg_score` mismatches **0/40**. **20/20 run-wide assertions PASS.**

### NEW — the 2-char SEED SLICE makes the 40-slot gate UNPASSABLE

The mock spec slices the md5 digest to **2 hex chars** for the seed:
`seed = h[(i*2)%8:((i*2)%8)+2]`. That is **16 possible seeds** for the **40**
`(civ,prompt)` slots of a standard `--sims 5 --prompts 5` run, so a collision is a
**structural certainty, not bad luck**. This session produced **39/40** distinct
seeds — `civ-formal` and `civ-mythic` collided on "Write 100 words on the witness
log." — which trips both the "distinct seeds = 40" assertion and the per-prompt
"8/8 distinct seeds" gate.

The spec's other requirement ("seed widths: all 4 hex chars") is satisfied by
**padding the 2-char slice to 4**, and that padding is exactly why the entropy
shortfall survived **58 sessions** of clean runs: the rendered width looked right and
the rendered *value* carried only 16 possibilities.

**Fix:** widen the slice to 4 chars — `seed = h[(i*2)%8:((i*2)%8)+4]` — keeping the
same index-wrap logic. 65 536 possible seeds; the padding branch becomes a no-op.
After the widening: **40/40** distinct seeds, 5/5 prompts at 8/8, 0 collisions.

*Rule: a seed that is PADDED to a documented width does not have that width's worth
of entropy. Check the SLICE width against the number of slots (40 here), not the
rendered width of the field. A gate that has passed 58 times can still be
arithmetically unwinnable — the pre-flight gate caught it before the run.*

### Re-confirmations (this session)

- **Bridge symlink** must satisfy BOTH the requested script path and the script's
  internal hardcoded `CIVS_DIR`; verify with `os.path.samefile()` (dev:ino **129:103**
  on both sides this session). The shell `[ -ef ]` test mis-parses in this sandbox.
- **NAS EDQUOT is total** (600 G/600 G) while visibly empty: a 2 MB `dd` fails with
  "Disk quota exceeded"; `cp -a` leaves a tree of **0-byte files that `ls` still
  lists**. **Verify bytes, not exit codes.** `mkdir` and `ln` work; the symlink
  bridge is the only way in.
- **`TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`**; JEV liveness = empty `questions`
  returns **422 `too_short`** (a payload-shape complaint, so the token WAS accepted).
- **`ZAI_TOKEN` still absent** from env and all 8 secrets; z.ai 401s (endpoint healthy,
  credential gap). Control B needs **both** `ZAI_TOKEN` (placeholder) and
  `ZAI_URL_OVERRIDE` — the override alone is dead code behind the token gate.
- **`civ-grounded` remains the low-relevance civ — 53rd consecutive session.** Last of 8
  on lifetime `relevance` 1215.49, `relevance_per_sim` 0.981, `avg_score` 1.0139,
  `alignment` 1.0694, `quality` 0.4043. Alignment deficit **0.1444** vs quality
  **0.0421** = **3.43x** wider => a **voice** failure, not a prose failure. Lifetime
  novelty 1.5680 is 5th of 8.
- **Run-level low ROTATED to `civ-whimsical`** (run `avg_score` 0.8220, `alignment`
  0.3550, `quality` 0.2100) while its lifetime standing is 3rd of 8 on `relevance` and
  6th of 8 on `avg_score` — **watch axis, not the finding** (session-132 rule). The
  *holder* of the run low rotated across THREE civs in three sessions; the *axis*
  (alignment) did not. **The stable signal is the axis, not the holder.**
- **`civ-therapist`** took the run-level `quality` low (0.1960) and is 7th of 8 on
  lifetime `relevance`; lifetime `avg_score` 1.1465 (6th of 8). Watch axis.
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-precise` swept 5/5. All four
  disagreements took the **lower**-scoring candidate (-0.2167, -0.0667, -0.1433,
  -0.1633); `civ-formal` was the argmax in all four and lost all four.
  **Never treat `win_rate` as a quality metric.**
- **Counter gap** is per-civ and **did not move**: delta exactly **0.000000** for all
  8 civs. Values: whimsical -173.14, poetic -96.80, formal -85.53, grounded -84.35,
  mythic -51.11, engineer -44.24, therapist -42.11, precise -32.63 (total -609.92).
- Run spreads: `avg_score` 0.6293, `alignment` **1.8360**, quality 0.2860, novelty 0.1490.
- **Mock teardown**: kill by exact-argv match, then prove the port closed
  (`curl` exit 7 = refused). Never `pkill -f mock_zai` (self-match).

## Session 178 (2026-10-25) — the wiped-workspace bootstrap, and a ROUNDING baseline that fakes 6/8 failures

**Run clean (session 178).** per-civ delta = **+10** x 8 = **80 new rows**, `meta_log` D = **+5**
(623 -> 628), `Winner:` lines = **5**, **80/80** rows `provider=zai`, **0** JEV `error` keys, **0**
2.0/2.0/2.0 fallback triples, **40/80** distinct seeds, **0** `(civ,prompt)` combos carrying
>1 seed, **8/8** distinct seeds AND previews on all 5 competition prompts, **80/80** rows match
an independently recomputed message md5, meta-vs-ledger `avg_score` mismatches **0/40**
(later-`ts` row). **Pre-flight 7/7** incl. the repeat-same-message determinism probe.
**12/12 run-wide assertions PASS.** No births, no extinctions, all generations still 1.

### NEW — a ROUNDED endpoint is not a baseline

The "relevance D == sum(this run's avg_score)" check reported **2/8 PASS** on its first
pass — and that was a **measurement error, not a data error**. The baseline used was the
leaderboard's `relevance`, which `update_leaderboard()` rounds to **2 dp**. Subtracting two
rounded endpoints leaves residuals up to **+/-0.0067** per civ, which is ~1000x the true
residuals. Re-derived against the pristine git blob (`git show HEAD:.../culture.json`,
unrounded) the result is **8/8 exact** (residuals <= 3.4e-13).

*Rule: when a delta check fails by an amount that looks like a rounding constant, check
the rounding before blaming the data.* The leaderboard is a **display** artifact; the
`culture.json` blob is the **state**.

### NEW — the mock's `figure` ratio needs hex->int conversion

The documented mock computes `figure = h[12:16] / h[16:20] / h[20:24]`, but `h` is a hex
**STRING** — so this raises `TypeError: unsupported operand type(s) for /: 'str' and 'str'`
=> HTTP 500 **while the socket stays open**, which is the exact failure mode fix (a) was
meant to prevent. Correct form: `int(h[12:16],16) / int(h[16:20],16) / int(h[20:24],16)`.
This will bite any rebuild that transcribes the formula literally.

### NEW — a wiped workspace needs a SPARSE clone, and the bridge needs `os.path.samefile`

`/workspace/repos/ai-writings/...` did not exist (fresh sandbox, empty NAS mount). The
upstream `SuperInstance/AI-Writings` is **3.7 GB** and `/workspace` is at **100% NAS quota**
(a 5 MB `dd` fails with "Disk quota exceeded"). Recipe that works:

1. `git init` + `core.sparseCheckout true` + `sparse-checkout set cellular-first-design/code/civilizations`
2. `git fetch --depth=1 origin main` (with `GIT_SSL_NO_VERIFY=1`), then `git checkout FETCH_HEAD`
3. Bridge: `ln -s /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`

**Verify the bridge with `os.path.samefile()`** — the shell `[ -ef ]` test mis-parses a
symlinked path in this sandbox and reports "DIFFERENT INODE" for a bridge that is
actually correct. `stat -L -c '%d:%i'` on both sides is the reliable check.

### Re-confirmations (this session)

- **Counter gap** is a fixed **per-civ** offset and did **not** move: grounded -84.35,
  whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63, mythic -51.11,
  therapist -42.11, engineer -44.24 (total **-609.92**), D = 0.0000 for all 8.
  (The **-609.9200 is the TOTAL, not a per-civ constant** — the per-civ values are the
  ones to compare. Quoting the total as if it were per-civ is a misread.)
- **`pkill -f` self-matches and kills the calling shell** (2nd occurrence). Kill the mock
  by scanning `ps -eo pid,args` for the exact argv and `os.kill(pid, SIGKILL)`; then prove
  the port closed with `curl -m 5` => **exit 7**, HTTP 000.
- `ZAI_TOKEN` absent; z.ai => **401 token expired or incorrect**. `ZAI_URL_OVERRIDE` alone
  is dead code (the token gate returns `None` first) — a **placeholder token is required**.
- JEV live: `jev-1.14.0`, `TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`.
- `git show HEAD:<path>` needs cwd = the **clone root**, not the civs dir.

### Interpretation (this run)

- **Run low: `civ-whimsical`** (run avg 0.7103). **VOICE failure, not prose**: alignment
  gap to next (0.393) is **2.3x** the quality gap (0.174), and alignment is the dimension
  the meta-GAN selects on.
- **Lifetime low: `civ-grounded`** (rel/sim 0.978, gap 0.150 to civ-therapist).
  Run low and lifetime low are **different civs on different axes** — do not promote.
- **`civ-precise` took 5/5 competitions** (5W/0L); every other civ 0-5. Under the mock the
  8 previews for one prompt differ only in the embedded seed/colour/figure fields.
- `win_rate` is **not** a quality metric (choice question vs three score questions).

## Session 169 (2026-10-25) — the SEED WIDTH collision: a correct seed that is not unique

**Run clean (session 169, 27th consecutive clean mock).** per-civ delta = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (578 → 583), `Winner:` lines = **5**, **80/80** rows
`[mock-zai`-prefixed with `provider=zai`, **0** rows with a JEV `error` key, **0** rows with the
2.0/2.0/2.0 fallback triple, **40/40** distinct seeds, **0** `(civ,prompt)` combos carrying
>1 seed, **8/8** distinct seeds AND **8/8** distinct previews on all 5 competition prompts,
**80/80** distinct `(q,n,a)` triples, meta-vs-ledger `avg_score` mismatches **0/40**
(later-`ts` row), `git status --porcelain` = **18** modified (17 data + leaderboard).
**59/59 assertions PASS.**

### NEW — the mock needs a FIFTH fix: the 2-char seed slice collides

The documented seed has always been a **2-hex-char** slice of the whole-message md5:
`h[(i*2)%8:((i*2)%8)+2]`. With 8 civs × 5 prompts = **40 samples drawn from 256 possible
2-char values**, a collision is expected often — and this session it landed:

| prompt | grounded | whimsical | formal | poetic | precise | mythic | therapist | engineer |
|---|---|---|---|---|---|---|---|---|
| what a cell is. | 44 | 5c | a6 | 4c | 3e | 82 | cc | 98 |
| the bookkeeper's role. | ba | 84 | dc | 3d | 88 | ce | 73 | de |
| the witness log. | 71 | 7c | **30** | c0 | d1 | **30** | 0c | f6 |
| ternary values. | 6f | df | c8 | dd | fa | 9c | 64 | 5f |
| JEV as a decision oracle. | 76 | a7 | b9 | 27 | 19 | 34 | d4 | 37 |

`civ-formal` and `civ-mythic` both got **`30`** on "the witness log" ⇒ **39 distinct seeds /
40 rows**, and that prompt sat at **7/8** distinct seeds.

**The mock was healthy by every other measure:** HTTP 200, prefix present, 0 tracebacks,
0 `EXC:`, and — the decisive point — **40/40 seeds matched an independently recomputed
`md5(whole_message)[:8]`**. The md5s were *different*; only the slice collided.

⇒ **This is a seed-WIDTH defect, not a seeding bug.** Fix (b) (whole-message md5) was correctly
applied; the slice it feeds is simply too narrow. The fix is to widen the seed to **4 hex
chars**: `seed = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]`, keeping (a) and (b)
intact.

**Why it matters even though nothing "failed":** the chooser is a JEV **`choice`** question
over 150-char `content_preview` snippets. Two civs sharing a seed produce a *near*-duplicate
candidate, and the meta-GAN's tie-break is exactly what the mock exists to exercise. A
degenerate mock silently weakens the one mechanism under test.

**The methodological lesson — two checks, two different defects:**
- `distinct seeds == 40` catches **collisions** (uniqueness).
- `md5 recompute == 40/40` catches **mis-seeding** (correctness).
A run can pass the second and fail the first. **Never collapse them into one assertion**, and
never treat "the md5s recompute" as "the seeds are distinct."

**Expected collision rate:** 40 draws from 256 two-char values ⇒ ~7–8 % per run. A
"39 distinct seeds" or "7/8 on one prompt" reading is a **mock defect to fix**, not noise to
average away.

### The pre-flight still saves the run — seventh time in the series

Pre-flight on the **exact long cultural prompts** (lengths 167–209): 40/40 distinct seeds,
40/40 distinct previews, 40/40 independently recomputed md5s, 0 literal `seed={}`,
8/8 + 8/8 on every prompt, 0 tracebacks. A one-word probe would **not** have caught the
collision (it would have used a different message and a different slice).

### `civ-grounded` remains the low-relevance civ — 44 consecutive sessions

Lifetime (9 244 rows): `avg_score` **0.9911** (last), `quality` **0.4086** (last), `alignment`
**1.0603** (last), `relevance` **1087.12** (last), `relevance_per_sim` **0.954** (last).
Absolute gaps: **alignment 0.1974** (vs therapist 1.2576) vs **quality 0.0421** (vs engineer
0.4507) ⇒ **4.7×** wider ⇒ a **voice** failure, not a prose failure. Lifetime novelty 1.5044
is **6th of 8** (not "above median"). Extinction risk **NONE** (threshold −10; lowest
+1087.12 = 109× the floor).

**The run-level low ROTATED to `civ-therapist`** (1.0697, run bottom on `avg_score`, `quality`
0.2220 and `alignment` 0.3880 — roughly a third of the next civ, mythic 1.0210) while its
*lifetime* standing is mid-field (`avg_score` 1.1480, 6th of 8; `relevance` 1259.72, 6th of 8).
**Watch axis, not the finding** (session-132 rule). Therapist's run signature is distinctive:
**novelty 2.5990 is the run's highest** while quality collapses to 0.2220 — highly novel,
badly aligned. That is the voice axis failing, in its purest form.

**Run levels sit ABOVE the lifetime band** (run `avg_score` 1.07–2.02 vs lifetime 0.99–1.55)
— the same generous-scoring direction as session 168 and the opposite of session 166. The
**ordering** carries the information, not the level.

### Chooser vs `avg_score` argmax: **2/5 (40 %)** — the "picks lower" direction is BACK

Session 168's 3/5 (60 %) was the series high; this session is 2/5 and **all three
disagreements took the lower-scoring candidate** (−0.0933, −0.0933, **−0.4500**). `civ-precise`
swept **4/5**; `civ-engineer` took "ternary values". Max |delta| **−0.4500**, well below
session 168's series-record −1.1033.

**`civ-poetic` is the sharpest inverse in the fleet:** it was the `avg_score` argmax on **3/5**
prompts and the chooser took it on **0/5** — 1st on lifetime `avg_score` (1.5509), `quality`
(0.7491) and `relevance` (1703.76), but **7th on `win_rate` (0.011)**. `civ-whimsical` is the
second inverse: 1st on lifetime novelty (1.9218) and 2nd on lifetime `avg_score`, but **last
on `win_rate` (0.009)**.

**Never treat `win_rate` as a quality metric.** The clean-mock series now has 15 five-sample
points spanning 0/5 – 4/5 ⇒ the honest claim is *somewhere in 0–80 %*, not a point estimate.

### Counter gap: **NEGATIVE**, fixed, unchanged in magnitude

`culture.json` `relevance_score` − ledger Σ`avg_score` = **−609.9200** total, and the blob-gap
and post-run-gap columns are **identical for all 8 civs** (per-civ Δ **0.0000**) ⇒ the offset
is fixed, not accumulating. Both columns computed **within the same epoch**. Sign confirmed
from the data, not copied from a prior report.

### Re-confirmations (this session)

- NAS EDQUOT total (**17th session**) — clone to `/tmp` (overlay), sparse-checkout
  `cellular-first-design` only, bridge the **clone root**, verify with `stat -L -c '%d:%i'` on
  both sides + `-ef` (this run: `129:3701`).
- z.ai **401** `token expired or incorrect` (credential gap, endpoint healthy) — **52nd session**.
- **JEV HTTP 200 on a well-formed body** discloses the served model `jev-1.14.0`.
- `ZAI_URL_OVERRIDE` alone is **dead code** (the `ZAI_TOKEN` gate returns `None` first) —
  Control B needs **both**; `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout redirected **and**
  `< /dev/null`, then poll.
- `gh` not installed (**19th session**) — `GET /user/repos` with `GITHUB_TOKEN`; the GitHub API
  is case-insensitive (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
- The meta-vs-ledger check must take the **later-`ts`** row (re-confirmed, 40/40 exact).
- `write` tool is jailed to the workspace root — cannot write into `/tmp`; use a **bash
  heredoc** for `/tmp` artifacts.
# Civ Orchestrator — durable cross-session lessons

The authoritative operational RUNBOOK lives in the repo at
`cellular-first-design/code/civilizations/RUNBOOK.md`.
This file holds the short, high-signal rules that survive a sandbox wipe.

## Session 138 (2026-10-24) — a per-run low can move *off* the lifetime low; both are real

**Verification held (23/23 checks — the most thorough pass yet).** per-civ Δ = **+10** × 8 =
**80 new rows** (engineer 816→826, formal 847→857, grounded 862→872, mythic 819→829,
poetic 841→851, precise 811→821, therapist 814→824, whimsical 874→884), `meta_log` Δ = **+5**
(423 → 428), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed with `provider={zai}`,
**0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback triple, **40 distinct
seeds / 80 rows** (= 8 civs × 5 prompts) with **0** `(civ,prompt)` combos carrying >1 seed, and
**5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews** — the **thirteenth
consecutive clean measurement** (118, 120–123, 125, 131–134, 136, 137).

**NEW — the per-run low and the lifetime low can be *different civs*, and that is not a
contradiction.** `civ-grounded` has been the lifetime low for 40 straight sessions, but this run
it placed **6th of 8** on `avg_score` (0.1550); `civ-therapist` took the run-level low (0.1257)
and sat lowest on `alignment` (0.0180), with `civ-engineer` 7th (0.1313). The session-132 rule
(*per-run low ⇒ watch axis*) and the session-121 rule (*lifetime gap ⇒ finding*) both survive:
**the lifetime table is the structural signal, the run ranking is the watch axis.** Report both;
never let a single run promote or demote a civ on its own.

**`civ-therapist` is now a second watch axis** — run-level low on both `avg_score` and
`alignment`. Its lifetime standing is mid-field (5th of 8 on `avg_score`, 1.6035 on
`alignment`), so it is *not* a finding. It becomes one if it repeats.

**`civ-grounded` remains the low-relevance civ — 40 consecutive sessions (95–138).** Last on
lifetime `avg_score` (1.1220), `alignment` (1.3056), `quality` (0.5273), `relevance` (978.37),
`relevance_per_sim` (1.078). The structural gap is **alignment: 0.4694 below the next civ vs
0.0450 on quality = 10.4× wider.** Alignment is the dimension the meta-GAN selects on ⇒ a
**voice** failure, not a prose failure. Lifetime novelty (1.5331) is above median — Grounded is
not boring, it is *unmistakable in a way the chooser does not reward*. Extinction risk **NONE**
(threshold −10; lowest relevance 978.37 = 98× above).

**Chooser vs `avg_score` argmax: 1/5 (20 %).** `civ-precise` won 3/5, `civ-engineer` 1,
`civ-formal` 1. Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) →
3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) →
2/5 (132) → 2/5 (133) → 0/5 (134) → 4/5 (136) → 1/5 (137) → **1/5 (138)**. Eighteen five-sample
points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What survives every
session: the chooser is **not** a pure argmax, and **every** observed disagreement across the
fleet goes the same way (it picks a **lower**-scoring candidate). The "ternary values" case
(chooser took a candidate **0.420 below** the argmax) ties the session-137 record (0.683) for the
largest disagreement in the clean-mock series. **Never treat `win_rate` as a quality metric.**

**Quality collapsed again (mean 0.0139, max 0.030)** — the 119/121/122/138 regime vs
session-120's 0.106–0.446. **The quality collapse is a LEVEL that moves, not a stable property.**
This run's cross-civ spreads: `alignment` 1.140, `novelty` 0.427, `quality` 0.026 — `alignment`
again carried the widest spread and is again the axis the chooser selects on. **Compare
cross-civ spreads, not absolute levels, before ranking on a dimension.**

**Pre-flight probe (8 civs → 8/8 distinct seeds AND previews, cultural-prompt lengths 168–200,
`[mock-zai seed=…]` present, 0 tracebacks) passed again** — `/tmp` was wiped, so the mock was
rebuilt from scratch and **both** historical bugs had to be re-applied on rebuild (session-112
index wrap `seed[(i*2)%8:((i*2)%8)+2]`, session-118 md5-of-whole-message seeding). A one-word
probe cannot reach the `i>=4` path that crashes; a crashing mock still leaves a listening
socket, so a port/200 check is **not** proof of correctness.

## Session 143 (2026-10-24) — row isolation must be per-civ tails, NOT `rows[-N:]` over concatenated files

**Run clean (session 143, 15th consecutive clean mock).** per-civ Δ = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (448 → 453), `Winner:` lines = **5**, **80/80** rows
`[mock-zai`-prefixed with `provider={zai}`, **0** rows with a JEV `error` key, **0** rows with the
2.0/2.0/2.0 fallback triple, **40 distinct seeds / 80 rows** with **0** `(civ,prompt)` combos
carrying >1 seed, **8/8 distinct seeds AND 8/8 distinct previews** on all 5 competition prompts.

### NEW (this session) — the `rows[-80:]` isolation bug, and how it fakes a mock failure

Isolating a run's rows by **`rows[-80:]` over the concatenation of all `civ-*/simulations.jsonl`
files** is **wrong**: `glob()` order is filesystem order, not chronological, so the last-80 slice
of the *concatenation* mixes historical rows from a late-alphabet civ into "this run's" rows.
This session it reported **15 distinct seeds (expected 40)** and **5 `(civ,prompt)` combos with
>1 seed (expected 0)** — a false mock-integrity failure that would have triggered a pointless
"mock is broken" investigation.

**Correct isolation:** take the **last 10 rows of each civ file** (the per-civ **+10** delta
already proves the boundary), concatenate those 80, then **sort by `ts`** before any grouping.
With that method: 40 distinct seeds, 0 combos with >1 seed, 8/8 + 8/8 on every prompt — i.e.
every clean-session assertion passes.

**Rule: never group or count across a concatenated multi-file list without an explicit `ts` sort.**
`rows[-N:]` is only safe on a list that is *already* in chronological order. For per-civ ledgers
the per-file tail is the correct primitive, because the per-civ delta assertion is the thing that
locates the boundary in the first place.

### Low-relevance civ — the low label did NOT rotate (41 sessions, 95–143)

`civ-grounded` remains the lifetime low on all five axes: `avg_score` 1.0906, `alignment`
1.2566, `quality` 0.5017, `relevance` 921.18, `relevance_per_sim` 1.048 — **last of 8 on every
one**. The binding constraint is still **alignment**: gap to the next civ 0.4656 vs quality's
0.0446 (**10.4×** wider). A voice failure, not a prose failure, because alignment is the axis
the meta-GAN selects on. Lifetime novelty 1.5135 is above median — Grounded is not boring, it
is unmistakable in a way the chooser does not reward.

**Session 141 flagged `civ-therapist` as the run-level low; it did not repeat.** This run
`civ-grounded` took the run-level `avg_score` low (0.5727) and `civ-therapist` took the
run-level `alignment` low (0.1310) at 7th of 8 on `avg_score` (0.5920) — *different civs* on
*different axes*, which is **not** a contradiction (session-132 rule). Therapist's lifetime
standing is mid-field (1.2888), so it is **not** a finding; it becomes one only if it repeats.

**Chooser vs `avg_score` argmax: 2/5 (40%)** — `civ-precise` won 3, `civ-formal` 2. The
chooser is still not a pure argmax, and every observed disagreement again took the
*lower*-scoring candidate. **Never treat `win_rate` as a quality metric.**

**Extinction risk NONE** — threshold −10, lowest relevance 921.18 = 92× above the floor.
Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

### Environment (re-confirmed)

- **NAS EDQUOT is total** (600 G/600 G): *every* `/workspace` write — even a 1-byte `echo` via
  Python — fails with `[Errno 122] Disk quota exceeded`; `cp` exits 1 and leaves 0-byte files
  that `ls` still lists. `mkdir` and `ln` work. The **symlink bridge** is still the only way in.
- **No `CAP_SYS_ADMIN`** (verified via `/proc/self/status` CapEff `a80425fb`) ⇒ `mount --bind`
  is denied and `unshare -m` fails with `Operation not permitted`. Do not spend time on
  namespace/bind-mount workarounds for the NAS trap — go straight to the symlink bridge.
- **`gh` is still not installed** — use `GET /search/repositories?q=...` and `GET /user/repos`
  with `GITHUB_TOKEN`. `SuperInstance/AI-Writings` resolves; the `ai-writings/cellular-first-design`
  slug 404s (the API is case-insensitive).
- **Sparse clone recipe that worked:** `git clone --depth 1 --filter=blob:none --sparse <token-url>`
  then `git sparse-checkout set cellular-first-design/code/civilizations` → **5.7 MB** instead of
  the 3.6 GB full clone. Bridge the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` on both sides + `-ef` (this session: `129:10465` both sides, EF_OK).
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.** JEV liveness = an empty
  `questions` dict returns **422 `too_short`** — a payload-shape complaint that proves the
  token was accepted. Do not read 422 as "down".
- **`ZAI_TOKEN` is still absent** from env and from all 8 sandbox secrets; z.ai 401s (endpoint
  healthy, credential gap). Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder)
  **and** `ZAI_URL_OVERRIDE` — the override alone is dead code behind the token gate.
- **Mock rebuilt from scratch this session** with the session-112 index-wrap fix
  (`seed[(i*2)%8:((i*2)%8)+2]`) *and* the session-118 whole-message md5 seeding fix. Pre-flight
  passed: 8/8 distinct seeds AND 8/8 distinct previews, `[mock-zai` prefix present, **0
  tracebacks**. Kill by exact args (`python3 /tmp/mock_zai.py`), then confirm the port is closed
  (`curl` exit 7 = refused).
- Push to the explicit token URL (`git push "<token-url>" HEAD:main`) — pushing to the clone's
  own remote fails with `could not read Username`. Verify with the commits API + the contents
  API (read the remote `leaderboard.json` back and compare against local), never the push's
  own exit code.

## Session 147 (2026-10-25) — the prompt path can be wrong on BOTH segments; read `CIVS_DIR` from the script

**Run clean (session 147, 19th consecutive clean mock).** per-civ delta = **+10** x 8 = **80 new
rows** (engineer 906->916, formal 937->947, grounded 952->962, mythic 909->919, poetic
931->941, precise 901->911, therapist 904->914, whimsical 964->974), `meta_log` delta = **+5**
(468 -> 473), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed with `provider=zai`,
**0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback triple, **40/40**
distinct seeds, **0** `(civ,prompt)` combos with >1 seed, sim->competition ts gap at index 4
in **8/8** civs (1.06 s - 22.85 s), and **5/5** competition slots at 8/8 distinct seeds AND
8/8 distinct previews.

### NEW (this session) — a wrong prompt path is NOT a mount race, and the repo is only ONE segment of it

The task named `/workspace/repos/ai-writings/cellular-first-design/code/civilizations/`. The
workspace was a **fresh NAS mount with nothing cloned** — `/workspace` held only
`.plugin-cache`, no `repos/`, no `ai-writings/`. The slug was wrong on **both** segments:
`ai-writings/` is the **repo** (`SuperInstance/AI-Writings`) and `cellular-first-design/` is a
**subdirectory inside it**.

**Rule: read the target path out of the script's own path constant before hunting the tree.**
`CIVS_DIR = Path("/workspace/repos/ai-writings/cellular-first-design/code/civilizations")`
encodes the correct full path in one line — grep it rather than guessing at the tree.

**Distinguish the two failure modes by *consistency*, not by one `ls`:**
- **5/5 consistent `ls` failure + a near-empty `/workspace`** => *not cloned*. Clone first.
- **Intermittent `ls` failure with `/workspace/repos/...` populated** => *mount race*; retry
  (session-145 rule).

The symlink bridge only helps **after** a clone exists — it bridges a tree into place, it
does not create one.

### The `write` tool cannot reach the bridged tree

Two separate jails, both hit this session:
- `write` to `/workspace/repos/ai-writings/cellular-first-design/...` =>
  `ENOTDIR: not a directory, mkdir '/workspace/repos/ai-writings/cellular-first-design'`
  (it will not traverse the symlink).
- `write` to a path under `/workspace/analysis/` => sporadic **`-122` on close**.

**Rule: for any file that must land inside the bridged tree, use a bash heredoc to the real
`/tmp` path.** Use `printf`/heredoc to `/tmp` for throwaway analysis scripts too.

### Mock teardown — kill BOTH pids, then prove the port is closed

Kill by exact args: `python3 /tmp/mock_zai.py` (server) and
`timeout -s KILL 900 python3 /tmp/mock_zai.py` (wrapper). Then
`curl -m 5 -X POST http://127.0.0.1:8799/...` => **exit 7** (refused) and `HTTP=000`. Never
`pkill -f mock_zai` — it self-matches the killing shell (2nd occurrence of that trap).

### Low-relevance civ — the low label did NOT rotate (45 sessions, 95-147)

`civ-grounded` remains the lifetime low on all five axes: `avg_score` 1.0647, `alignment`
1.2201, `quality` 0.4828, `relevance` 939.86, `relevance_per_sim` 1.023 — **last of 8 on every
one**. The binding constraint is still **alignment**: gap to the next civ 0.2557 vs quality's
0.0336 (**7.6x** wider). A voice failure, not a prose failure, because alignment is the axis
the meta-GAN selects on. Lifetime novelty 1.4911 is above median — Grounded is not boring, it
is unmistakable in a way the chooser does not reward.

**`civ-therapist` — 3rd session at the run bottom, now on BOTH axes** (run `avg_score` 0.1470
and run `alignment` 0.0280, both lowest of 8). Still mid-field on the lifetime axis
(`avg_score` 1.2538, 5th of 8) => **watch axis, not a finding**. It becomes one only if the
lifetime axis moves too.

**Chooser vs `avg_score` argmax: 0/5 (0 %)** — the chooser disagreed in **every** competition.
`civ-precise` swept 4/5, `civ-formal` 1/5. Every disagreement again took the **lower**-
scoring candidate (largest: winner 0.190 vs argmax 0.743). Clean-mock series: 0/5 (118) ->
3/5 (119) -> 1/5 (120) -> 4/5 (121) -> 4/5 (122) -> 3/5 (123) -> 0/5 (124) -> 4/5 (125) ->
4/5 (137) -> 1/5 (138) -> 2/5 (139) -> 4/5 (144) -> 4/5 (146) -> **0/5 (147)**. The rate is
**not narrowing**; report it as a sample and keep the **direction** as the finding.
**Never treat `win_rate` as a quality metric.**

**Extinction risk NONE** — threshold -10, lowest relevance 939.86 = 94x above the floor.
Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

**Counter gap is a FIXED per-civ offset** — whimsical +63, grounded +43, formal +42, poetic
+37, engineer +22, mythic +20, therapist +17, precise +16, byte-identical to session 145.

## Session 144 (2026-10-24) — the `Connection: close` fix, and the mock probe must use the *long* cultural prompt

**Run clean (session 144, 16th consecutive clean mock).** per-civ Δ = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (453 → 458), `Winner:` lines = **5**, **80/80** rows
`[mock-zai`-prefixed with `provider={zai}`, **0** rows with a JEV `error` key, **0** rows with the
2.0/2.0/2.0 fallback triple, **40 distinct seeds / 80 rows** with **0** `(civ,prompt)` combos
carrying >1 seed, **8/8 distinct seeds AND 8/8 distinct previews** on all 5 competition prompts.

### NEW (this session) — a mock that answers 200 but never closes the connection hangs `curl`

The rebuilt mock used `BaseHTTPRequestHandler` with a `Content-Length` header but **no
`Connection: close`**. `urllib` (what the orchestrator uses) was fine, but a plain
`curl -X POST …` **hung until the tool's 30 s timeout** while the server had already logged
`200` — the classic "server answered, client waited for EOF" split. Symptom is easy to
misread as "mock is down" and sends you re-debugging a healthy server.

**Rule: a 200 in the mock's access log is not the same as the client completing.** Probe with
`curl -m 8` (a timeout is a *result*, not an error) and add `Connection: close` to the
response. After the patch the same probe returned `HTTP=200 time=0.001053`.

### NEW (this session) — the pre-flight probe must use the *exact long cultural prompt*

Probing the mock with a one-word body (`{"content":"hi"}`) does **not** exercise the path the
orchestrator uses. The correct probe builds the full cultural prompt
(`You are a voice in the tradition of "<CIV NAME>".\nYour tenets: …\nYour voice: …\n\n{prompt}`)
for all 8 civs and asserts **8/8 distinct seeds AND 8/8 distinct previews**, plus
`[mock-zai` prefix on all 8 and `grep -c Traceback` / `grep -c EXC:` on the mock log → 0.
A one-word probe passes even against a partially broken mock. Measured this session: 8/8 and
8/8, body lengths 332–369 chars.

### Low-relevance civ — the low label did NOT rotate (42 sessions, 95–144)

`civ-grounded` remains the lifetime low on all five axes: `avg_score` 1.0851, `alignment`
1.2510, `quality` 0.4974, `relevance` 926.99, `relevance_per_sim` 1.043 — **last of 8 on every
one**. The binding constraint is still **alignment**: gap to the next civ 0.2667 vs quality's
0.0344 (**7.8×** wider). A voice failure, not a prose failure, because alignment is the axis
the meta-GAN selects on. Lifetime novelty 1.5069 is above median — Grounded is not boring, it
is unmistakable in a way the chooser does not reward.

**`civ-therapist` appeared as a watch axis in sessions 138, 141 and 144 and has still never
become a lifetime finding** (lifetime `avg_score` 1.2818, mid-field). It took the run-level
`alignment` low (0.4460) while `civ-grounded` took the run `avg_score` low (0.5803) — the
session-132 "different civs on different axes" case, not a contradiction.

**Chooser vs `avg_score` argmax: 1/5 (20%)** — `civ-precise` won 3, `civ-mythic` 2. The chooser
is still not a pure argmax, and every disagreement again took the *lower*-scoring candidate
(largest this run: winner 0.83 vs argmax 1.32 on ternary values). **Never treat `win_rate` as
a quality metric.**

**Extinction risk NONE** — threshold −10, lowest relevance 926.99 = 92.7× above the floor.
Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

## Session 174 (2026-10-25) — two new durable traps

**NEW 1 — the mock spec's `figure = h[12:16] / h[16:20] / h[20:24]` is pseudo-code, not Python.**
Read literally it divides two `str` values and raises
`TypeError: unsupported operand type(s) for /: 'str' and 'str'`. The mock then **500s on every
request while the socket stays open**, so a port/200 liveness probe looks healthy — the same
false-negative as fix (a). Treat the three slices as three separate components:
`figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`. This is a **seventh** failure mode, distinct
from fix (a) (which is a `ValueError` on the seed slice for `i>=4`). The RUNBOOK's one-word
probe cannot catch it.

**NEW 2 — read `culture.json` baselines from git, NOT from `leaderboard.json`.**
`leaderboard.json` stores `relevance` **rounded to 2 dp**; `culture.json` keeps full float
precision. A baseline taken from the leaderboard makes the
`d_relevance == sum(avg_score)` check fail by up to **0.0033 per civ** on 4 of 8 civs and
looks like a genuine accounting error. The authoritative pre-run value is
`git show HEAD:.../culture.json`. With true baselines the check is **8/8 exact to 1e-13**.
Counter-gap claims are only auditable at that precision.

**Also:** the shell's `[ -ef a b ]` test mis-parses in this sandbox
("binary operator expected") — use Python `os.stat` and compare `(st_dev, st_ino)` instead.
A failing `[ -ef ]` here is **not** a broken bridge.

**`civ-grounded` remains the low-relevance civ — 49th consecutive session.** Last of 8 on
lifetime `avg_score` 1.0047, `alignment` 1.0626, `quality` 0.4056, `relevance` 1153.49,
`relevance_per_sim` 0.970. Alignment gap **0.4131** vs quality gap **0.0431** => **9.59x**
wider => a **voice** failure, not a prose failure. Lifetime novelty 1.5460 is 6th of 8.
Extinction risk **NONE** (lowest +1153.49 = 115x the floor).

**Run-level low rotated to `civ-therapist`** (1.0297 on `avg_score`, 0.3360 on `alignment`)
while its lifetime standing is 6th of 8 — **watch axis, not the finding** (session-132 rule).

**Chooser vs `avg_score` argmax: 0/5 (0 %)** — the worst point in the clean-mock series, and
all five disagreements went the same way (the chooser took the **lower**-scoring candidate).
Max |delta| 0.240. `civ-precise` won 4/5. Series now 22 five-sample points: still honestly
*somewhere in 0-80 %*. **Never treat `win_rate` as a quality metric.**

## Standing findings

- **`civ-grounded` (The Grounded) is the low-relevance civ** — last on lifetime `relevance`
  (978.37), `relevance_per_sim` (1.078), `avg_score` (1.1220), `alignment` (1.3056) and
  `quality` (0.5273). The **alignment** gap is the structural one (0.4694 vs a 0.0450 margin
  on quality — 10.4× wider). Alignment is the dimension the meta-GAN *selects* on, so the civ
  fails to *embody a distinctive voice*, not merely to write weakly. 40 sessions (95–138).
- **`civ-formal`** = the low-novelty axis (lifetime novelty 1.4065, last; alignment 1.9081
  healthy).
- **`civ-engineer`** = 2nd-lowest lifetime `avg_score` (1.2821), still no gap to the low civ.
- **The two stable inverses:** `civ-poetic` = 1st on lifetime `avg_score` (1.7042) / `quality`
  (0.9123) but last on `win_rate` (0.012, 5/403); `civ-precise` = best `win_rate` (0.553) and
  highest `alignment` (2.2983) but only 3rd on `avg_score` (1.4882).
- **Extinction risk NONE** — threshold −10, lowest relevance +978.37 (98× above floor).
  Registry 8, `max_civs` 12. Extinction/birth only runs under `--loop`.
- **Counter gap is per-civ uneven**, not a uniform offset. `save_state()` has no lock ⇒
  `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs**, not a dict. A
  dict-shaped reader silently yields 0 % agreement and empty pick tallies. Winner fields are
  `winner_civ` / `winner_name`.
- **Never treat `win_rate` as a quality metric** — it is a *selection* metric.

## Environment rules (re-confirmed, 6th session running)

- **NAS EDQUOT is total.** *No* write to `/workspace` succeeds — even a 5-byte `echo` yields a
  0-byte file that `ls` still lists, and `cp` exits 1 with `Disk quota exceeded` while leaving
  those 0-byte files behind. `mkdir` and `ln` work. The only way in is the **symlink bridge**.
- **Clone to `/tmp`** (overlay, ~28 G free; NAS quota does not apply), then
  `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  Verify by **inode identity** (`stat -L -c '%d:%i'` on both sides + `-ef`), not by `ls`.
- **Do not flatten the clone.** The symlink target is the *nested* `cellular-first-design` dir.
  A 5/5 consistent `ls` failure = wrong target; an intermittent one = mount race. Retry before
  concluding the tree is gone.
- **Upstream is `SuperInstance/AI-Writings`** (the `ai-writings/cellular-first-design` slug
  404s; the API is case-insensitive). `gh` is **not installed** — use
  `GET /search/repositories?q=...` and `GET /user/repos` with `GITHUB_TOKEN`.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** (script reads the former,
  sandbox stores the latter). Unset ⇒ JEV degrades to the 2.0 default and every score is
  constant. JEV liveness probe: an empty `questions` dict returns **422 `too_short`** — a
  payload-shape complaint, which proves the token was accepted. Do not read 422 as "down".
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is absent** from env and from all 8 sandbox secrets; z.ai returns 401 (endpoint
  healthy, credential gap). JEV is live.
- **Tool timeout 30 s < orchestrator run ~55 s.** Launch detached, poll `ps` + the log.
- **Kill the mock by exact args** (`python3 /tmp/mock_zai.py`) — two pids (timeout wrapper +
  server). Never `pkill -f mock_zai`, which self-matches. Verify the port is closed afterward
  (`curl` exit 7 = refused).

## Verification pattern (assert on rows, never on exit code)

All failure modes are silent with exit code 0 — a missing token makes `call_provider()` return
`None`, `run_simulation()` return `None`, and the competition short-circuit on
`if not results: return None`.

| Assertion | Expected for `--sims 5 --prompts 5` |
|---|---|
| per-civ `simulations.jsonl` delta | **+10** each (5 sim-phase + 5 competition-phase) |
| total new ledger rows | **80** |
| `meta_log.jsonl` delta | **+5** |
| `Winner:` lines | **5** |
| rows with `[mock-zai` prefix | **80** |
| rows with a JEV `error` key | **0** (this is what proves JEV really scored) |
| rows with the 2.0/2.0/2.0 fallback triple | **0** |
| distinct seeds across the 80 new rows | **40** (8 civs × 5 prompts) |
| `(civ, prompt)` combos with >1 seed | **0** |
| distinct previews+seeds per prompt (ts-sorted last-8 slice) | **8/8 on all 5 prompts** |

Isolate this run's rows by **count from the end of the file** (`rows[-delta:]`), not by a `ts`
cutoff — prior sessions left mock rows behind, so a `ts >=` filter pulls in history.

**Per-prompt distinctness must use the ts-sorted last-8 slice.** The 80 new rows are two
interleaved phases (40 sim-phase, 40 competition-phase); grouping by prompt and taking `rows[-8:]`
mixes them and yields a false 3–6/8. Sort all 80 by `ts` first, then take the last 8 per prompt.

**`avg_score` is a top-level row field, not a member of `scores`.** `scores` holds only
`quality` / `novelty` / `alignment` / `confidence`; averaging `r["scores"]["avg_score"]` silently
yields **0.0 for every civ** and makes the whole ranking look flat. Use `r["avg_score"]`.

## Session 149 (2026-10-25) — 21st consecutive clean mock measurement

- **A blobless + sparse clone is the cheap path for this 3.7 GB repo**:
  `git clone --filter=blob:none --no-checkout --depth 1` + `sparse-checkout set cellular-first-design`
  → **6.1 MB on disk**, one shot, nothing else fetched. Far better than `--depth 1` full checkout.
- **The hung `curl` right after launching a background server is usually the SHELL, not the
  server.** A `setsid nohup ... &` started in the same command as a foreground `curl` can leave
  the tool blocked on the inherited stdout. Check `ps` for the server pid and re-probe in a
  *separate* command before declaring the mock broken — it was healthy (HTTP 200) in session 149.
- **The `ls -la` on the requested path worked once the bridge existed** — confirming again that
  a 5/5 consistent failure means "not cloned", and that the bridge (not a retry) is the fix.
- **Quality collapse is a LEVEL that moves.** Run-level quality was 0.011–0.052 this session
  (16th of the last 17 clean-mock sessions) — the lowest yet — yet the lifetime spread ordering
  was unchanged. **4th consecutive observation of the same rule: rank on cross-civ spreads,
  never on absolute quality levels, never on a single run's low.**
- **Chooser-vs-argmax agreement: 4/5 (80 %)**, tied for the series high (0,3,1,4,4,3,0,4,4,1,2,4,4,0,2,4).
  The single disagreement went **downward** again. 16 five-sample points still cannot pin a rate.
- **`civ-precise` swept 5/5 for the SECOND clean-mock session running** (148 and 149) at
  `preferred_temp` 0.2 — the coldest voice is what the chooser rewards, and the mirror inverse
  of `civ-poetic` (1st on `avg_score`, last on `win_rate`) is narrowing for a 2nd session.
- **The run-level watch axis ROTATED again**: `civ-therapist` was at the run bottom 2 sessions
  running (147, 148); session 149's triple-bottom is `civ-mythic` (avg_score 0.2400, quality
  0.0110, alignment 0.0330). The **lifetime** low stayed `civ-grounded` for the 47th session.
  **The run ranking and the lifetime ranking are different civs on different axes — that is
  the rule, not a contradiction.** Only the lifetime table is a finding.
- **`civ-grounded` remains the low-relevance civ (47 consecutive sessions, 95–149)**, and the
  gap is still **structural alignment**: 0.2480 below `civ-therapist` on lifetime alignment vs
  0.0330 on quality (7.5×). Grounded fails to *embody a distinctive voice*, not to write well —
  a **voice failure, not a prose failure**. Lifetime novelty 1.4888 is above median: Grounded
  is not boring, it is *unmistakable in a way the chooser does not reward*.
- **Counter gap stayed byte-identical** to sessions 147/148 (whimsical −63, grounded −43,
  formal −42, poetic −37, engineer −22, mythic −20, therapist −17, precise −16) — a fixed
  per-civ offset, not an accumulating leak. `save_state()` has no lock ⇒ `relevance_per_sim`
  is still not recomputable from the ledger by an auditor.
- **NAS EDQUOT also breaks `cp` into `/workspace/output`** for report delivery: `cp` exits 1
  with `Disk quota exceeded` and leaves a **0-byte file that `ls` still lists**. Delete the
  0-byte stub; the durable copy is the committed git blob, verified with
  `git show HEAD:<path> | wc -c`.

## Session 150 (2026-10-25) — 22nd consecutive clean mock; the gap RATIO inverted, so quote absolute gaps

- **Run clean (15/15 checks).** per-civ delta = **+10** x 8 = **80 new rows** (engineer
  936->946, formal 967->977, grounded 982->992, mythic 939->949, poetic 961->971, precise
  931->941, therapist 934->944, whimsical 994->1004), `meta_log` delta = **+5** (483 -> 488),
  `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed with `provider=zai`, **0** rows
  with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback triple, **40/40** distinct
  seeds, **0** `(civ,prompt)` combos with >1 seed, sim->competition ts gap at index 4 in
  **8/8** civs, `leaderboard.json` rewritten at 00:45:01Z.
- **Pre-flight saved the run for the 5th time in the series** (115, 117, 145, 147, 150).
  `/tmp` was wiped, so the mock was rebuilt from scratch and **three** known bugs were live
  again: the session-112 index wrap, the session-118 md5-of-whole-message seeding, and the
  session-145 literal-`{}` placeholder. Pre-flight: **40/40 distinct seeds, 40/40 distinct
  previews, 8/8 + 8/8 on all 5 prompts, 0 tracebacks**, prompt lengths 167-209.
  **Never relax the seed-distinctness assertion** — the socket-level checks (200, prefix
  present, 0 tracebacks) all pass against a mock carrying `seed={}`.
- **NEW — the alignment/quality gap RATIO for the low-relevance civ INVERTED this session.**
  `civ-grounded` is still last of 8 on **both** dimensions, but the absolute gaps now point
  the other way: alignment gap **0.0655** vs quality gap **0.1581**. The ratio has swung
  **11x -> 2.7x -> 7.5x -> 0.4x** across sessions 125/145/149/150 on identical data-shape
  logic. **Quote the absolute gaps and the "last of 8 on both" invariant; never the ratio.**
  A ratio over two drifting quantities is not a stable claim.
- **`civ-grounded` remains the low-relevance civ (48 consecutive sessions, 95-150)** — last
  of 8 on every lifetime axis: `relevance` 953.17, `relevance_per_sim` 1.004, `avg_score`
  1.0459, `alignment` 1.1872, `quality` 0.4691. Label did not rotate (last before the run at
  950.40 / 1.012, last after it at 953.17 / 1.004). A **voice** failure, not a prose
  failure: alignment is the axis the meta-GAN selects on, and lifetime novelty 1.4813 is
  above median — Grounded is unmistakable in a way the chooser does not reward.
- **Watch axis `civ-therapist` — 4th session at the run bottom, on BOTH axes** (run
  `avg_score` 0.2650, run `alignment` 0.0210, both lowest of 8). Lifetime standing is still
  mid-field (`avg_score` 1.2278, 5th of 8) => **watch axis, not a finding**.
  `civ-grounded` was 7th of 8 on run `avg_score` (0.2767) — the run-level low and the
  lifetime low are different civs on different axes. That is the rule, not a contradiction.
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-formal` won 3, `civ-precise` 2. All
  4 disagreements took the **lower**-scoring candidate (deltas -0.467, **-0.823**, -0.113,
  -0.523). 22 five-sample points cannot pin a rate: the honest claim is *somewhere in
  0-80 %*. **The direction is the finding; the rate is not.** Never treat `win_rate` as a
  quality metric.
- **`civ-formal` won 3/5 for the first time in the series** (it had never out-polled
  `civ-precise`). `civ-formal` remains the distinct low-**novelty** axis (lifetime novelty
  1.3764, last of 8; alignment 1.7693 healthy).
- **The two stable inverses:** `civ-poetic` = 1st on lifetime `avg_score` (1.6115) /
  `quality` (0.8242) / `relevance_per_sim` (1.572) but **last on `win_rate` (0.013)** and
  won 0/5 despite being 2nd on run `avg_score`; `civ-precise` = best `win_rate` (0.570),
  **highest lifetime `alignment` (2.1975)**, 1st on run `avg_score` (0.7767) at
  `preferred_temp` 0.2 — the mirror inverse.
- **Extinction risk NONE** — threshold -10; lowest relevance 953.17 = 95x above the floor.
  Registry 8, `max_civs` 12; all 8 still `generation=1`.
- **Counter gap stayed byte-identical** to sessions 147/148/149 (whimsical -63, grounded
  -43, formal -42, poetic -37, engineer -22, mythic -20, therapist -17, precise -16) — a
  fixed per-civ offset, not an accumulating leak.
- **Dimension spreads:** `alignment` **1.2920**, `avg_score` 0.5117, `novelty` 0.4500,
  `quality` **0.0180** (collapsed again — 17th of the last 18 clean-mock sessions).
  **Rank on cross-civ spreads, never on absolute quality levels, never on a single run's low.**
- **New environment note — a detached mock launch can time out the tool call even with
  stdout AND stdin redirected.** `setsid nohup ... > log 2>&1 < /dev/null &` blocked the
  full 30 s, yet the *next* command showed the mock healthy (pids 303/304, listening, 0
  tracebacks). **When a detached launch times out, check `ps` in a separate command before
  assuming it failed.**
- **z.ai credential gap: 44th session.** `ZAI_TOKEN` absent from env and all 8 secrets;
  401 `token expired or incorrect` against a healthy endpoint. JEV live (422 on a malformed
  `questions`).

## Session 157 (2026-10-25) — 22nd consecutive clean mock; the `simulations_run` baseline is NOT the row count

**Run clean (103 assertions, 0 failures).** per-civ delta = **+10** x 8 = **80 new rows**
(engineer 1006->1016, formal 1037->1047, grounded 1052->1062, mythic 1009->1019, poetic
1031->1041, precise 1001->1011, therapist 1004->1014, whimsical 1064->1074), `meta_log` delta
= **+5** (518 -> 523), **Winner:** lines = **5**, **80/80** rows `[mock-zai`-prefixed with
`provider=zai`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback
triple, **80 distinct** JEV score triples / **35 distinct** confidences, **40/40** distinct
seeds, **0** `(civ,prompt)` combos with >1 seed, **8/8 + 8/8** on all 5 competition prompts.

### NEW — the `simulations_run` baseline must come from the git blob, not the ledger row count

The orchestrator's `culture.json` `simulations_run` counts **only the sim phase** (5 per civ),
while `simulations.jsonl` accumulates **both** phases (10 rows per civ) *and* the entire
competition history. The two counters are therefore offset by the whole competition history
(grounded: `simulations_run` 1009 vs 1062 ledger rows).

Asserting `sims_run == rows_before + 10` produced **8 false failures** on a run where every
other assertion was green. The correct assertion is against the **git HEAD blob's**
`culture.json`: `simulations_run` delta = **+10** for all 8 (grounded 1009->1019, precise
985->995, …) and `wins+losses` delta = **+5** for all 8 (5 competitions).

**Rule: an 8-for-8 failure with every other assertion green is a BASELINE bug until proven
otherwise — check the baseline's source before believing the failure.** The RUNBOOK's
assertion table says "per-civ `simulations.jsonl` delta +10"; it does **not** license reusing
that number as the `simulations_run` baseline.

### NEW — the pre-flight must render the cultural prompt as an F-STRING, not `str.format()`

The orchestrator builds the prompt with an f-string:
`f"""You are a voice in the tradition of "{self.culture['name']}"…"""`. A probe that does
`TEMPLATE.format(name, tenets, voice, prompt)` raises **`KeyError: 'self'`** — the probe crashes
before it ever reaches the mock, and the natural reading ("the mock is broken") is wrong.

Fix: replace the four f-string expressions with sentinels, then substitute:
`{self.culture['name']}` / `{', '.join(self.culture['tenets'])}` /
`{self.culture['voice_emphasis']}` / `{prompt}`. That reproduces the orchestrator's bytes
exactly. Pre-flight then reported **40/40 distinct seeds, 40/40 distinct previews, 40/40
template md5s, 0 tracebacks**, prompt lengths 167-209, **8/8 + 8/8 on all 5 prompts** — the
pre-flight saved the run for the **5th** time in the series (115, 117, 145, 147, 150).

### NEW — `/tmp` was REAPED mid-session; a vanished target looks exactly like a broken bridge

A completed sparse clone (`/tmp/aiw`, 6.7 MB) **vanished between two commands**. The symlink
bridge survived but became **dangling**, so `ls` on the *target* path failed with "No such
file or directory" and `stat -L` failed too — indistinguishable from a broken bridge.

**Rule: when the bridged path 404s, check the TARGET (`ls /tmp/aiw`) before re-creating the
link.** Re-creating a link to a missing target just reproduces the symptom. Re-cloned with the
blobless+sparse recipe (`--filter=blob:none --no-checkout --depth 1 --sparse` +
`sparse-checkout set --no-cone cellular-first-design/code/civilizations`) → **6.7 MB**, one shot.

### The z.ai credential gap: 45th session. REST core quota exhausted; the SEARCH api still answers

`ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or incorrect`**
(endpoint healthy). JEV live (422 `too_short` on an empty `questions`). This session the
**REST core quota was exhausted** (0/5000, reset 02:21Z) — `GET /user`, `GET /repos/...` and
`GET /orgs/...` all returned 403 "API rate limit exceeded", and a rate-limited response
**renders as "no such repo" for every candidate at once**. The **search API has a separate
bucket and kept working**: `GET /search/repositories?q=user:SuperInstance` identified the
owner and the repo list. **Use search while core is rate-limited; and never read a 403 as
absence.** `git ls-remote` remains the ground truth for repo existence.

### Low-relevance civ — the low label did NOT rotate (49 sessions, 95-157)

`civ-grounded` remains **last of 8 on every lifetime axis**: `relevance` 1009.12,
`relevance_per_sim` 0.990, `avg_score` 1.0296, `alignment` 1.1435, `quality` 0.4435.
Absolute gaps: alignment **0.2197** (to therapist) vs quality **0.0333** (to formal) — a
**6.6x** wider alignment gap. (Quote the absolute gaps; the ratio has swung 11x -> 2.7x -> 7.5x
-> 0.4x -> 6.6x across sessions and is not a stable claim.) Alignment is the axis the
meta-GAN selects on ⇒ a **voice failure, not a prose failure**. **LIFETIME NOVELTY 1.5018 is
now BELOW median (1.6410)** — sessions 143-150 had Grounded above median. If that holds next
session, Grounded is losing on two axes, not one. **Extinction risk NONE** — 1009.12 = 100.9x
above the −10 floor; registry 8, all `generation=1`.

**Watch axis `civ-therapist` — 5th session at the run bottom, on BOTH axes** (run `avg_score`
0.7893, run `alignment` 0.6760, both lowest of 8). Lifetime standing still mid-field
(`avg_score` 1.1994, 6th of 8) ⇒ **watch axis, not a finding**. `civ-grounded` was 7th of 8 on
run `avg_score` (0.8997) — the run low and the lifetime low are different civs on different
axes; that is the rule, not a contradiction.

**Chooser vs `avg_score` argmax: 0/5 (0 %)** — disagreed in **every** competition. `civ-poetic`
was the argmax on **all five** prompts and won **zero** (deltas -0.1867 … -0.6300, all
downward). `civ-precise` won 4/5, `civ-formal` 1/5. 20+ five-sample points cannot pin a rate:
report it as a sample and keep the **direction** as the finding. **Never treat `win_rate` as a
quality metric.**

**The two stable inverses, sharpest form yet:** `civ-poetic` = 1st on lifetime `avg_score`
(1.5961) / `quality` (0.7942) / `relevance` (1564.74) / `relevance_per_sim` (1.559) and **last**
on `win_rate` (0.012, 6/498) — argmax on 5/5 prompts, winner on 0/5. `civ-precise` = best
`win_rate` (0.572), **highest lifetime `alignment` (2.1678)**, won 4/5 at `preferred_temp` 0.2.

**Counter gap byte-identical pre/post run** on all 8 civs (delta +0.0000 each): grounded -84.35,
whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63, mythic -51.11, therapist
-42.11, engineer -44.24 (total -609.92). A fixed per-civ offset, not an accumulating leak.
`save_state()` has no lock ⇒ `relevance_per_sim` is not recomputable from the ledger.

**Dimension spreads:** run-level `alignment` **1.7070**, `avg_score` 0.8880, `quality` 0.6360,
`novelty` 0.5260; lifetime `alignment` **1.0243**, `avg_score` 0.5665, `novelty` 0.5387,
`quality` 0.3507. **`alignment` widest on both horizons.** Run-level `quality` did **not**
collapse this session (0.093-0.729) — the collapse is a **LEVEL** that moves. **Rank on
cross-civ spreads, never on absolute quality levels, never on a single run's low.**

## Session 159 (2026-10-25) — concurrent peer sessions; the four merge rules for the civ tree

**Run clean (134/134 assertions).** per-civ delta +10 x 8 = 80 new rows (all ts inside one
02:23:15-02:23:44Z window, every new row newer than every pre-existing row), `meta_log` +5
(523 -> 528), 134 assertions passed / 0 failed, 40/40 distinct seeds, 40/40 distinct previews,
40/40 distinct template md5s, 0 tracebacks, 0 JEV error keys, 0 2.0/2.0/2.0 fallbacks,
leaderboard reconciling 8/8 against `culture.json`.

### NEW — a peer session can hold the same session number, and the run collides on push

The push was rejected: upstream had moved `b002296` -> `0374e23`, a **peer session 158** (same
command, different sandbox) that ran **concurrently** with ours — ours finished 02:23:44Z, theirs
02:24:01Z. Their data differed from ours (their chooser-vs-argmax 1/5, ours 3/5): two
independent mock runs, not a duplicate. Our local tree's last report was 157, so we numbered
ours 158 and pushed — **158 was already taken upstream.** Renumbered to **159** and rebased.

**Rule: never derive the next session number from the local tree alone.** `git fetch` and check
`origin/main` **before** naming the report file and before the first push.

### NEW — the civ tree has FOUR file classes, and they merge four different ways

`git rebase` conflicted in **all 18 files**. Text-splicing the conflict markers corrupts the
append-only ledgers.

| file class | nature | correct merge |
|---|---|---|
| `simulations.jsonl` | append-only ledger | base + upstream's 10 + mine's 10, deduped on `(ts, civ, prompt, preview)` |
| `meta_log.jsonl` | append-only ledger | base + upstream's 5 + mine's 5, deduped on `(ts, winner, prompt)` |
| `culture.json` | snapshot, **additive counters** | base + (upstream − base) + (mine − base) for `simulations_run`/`relevance_score`/`wins`/`losses`; `preferred_params` = last writer wins |
| `leaderboard.json` | snapshot, **derived** | **recompute** from the merged `culture.json` files; do not pick a side |

**The first attempt kept only the 10 conflicted `meta_log` rows and silently dropped the 523
ancestor rows**, and left `<<<<<<< HEAD` / `=======` / `>>>>>>>` marker lines embedded in the 8
ledgers (3 bad lines per file; 1085 "rows" of which 3 were markers). `wc -l` alone would have
reported 1085 and looked fine. **Caught only by a per-line JSON parse.** After the fix:
`meta_log` 533 rows (523+5+5), ledgers base+20, `culture.json` +20 `sims_run` and +10 W+L for
all 8, `generation` still 1, 0 conflict markers, all JSON valid, leaderboard rebuilt and
reconciling 8/8.

**Rules:** (1) resolve append-only ledgers by **reconstructing from git blobs**, never by
splicing markers; (2) re-parse **every line** of every merged JSONL, don't trust `wc -l`;
(3) `git show` inside a Python script needs `cwd=` set to the repo root — running from a
subdirectory silently returned empty output and produced **0-row ledgers**;
(4) a `culture.json` merge must be checked for the `relevance_score` delta, not just the row
count.

### NEW — a false mock-degeneracy alarm in the VERIFIER, not the mock

The first verification pass reported **"10 distinct seeds across 80 new rows"** — the exact
signature of a degenerate mock. It was a **bug in the verification script**: it built one
concatenated list of *per-civ blocks* then took `allrows[-80:]`, but because `civ-grounded`'s
block sits first, the tail-80 window covered only the last 5 civs' blocks. The correct window is
**10 rows from each civ**. The mock was healthy (40/40 seeds, 40/40 previews, 8/8 on all 5
prompts, 0 tracebacks).

**Rule: a mock-degeneracy alarm must be re-derived from a correctly sliced window before the
mock is rebuilt.** Rebuilding a healthy mock on a false alarm is the expensive error. When
slicing a multi-file ledger, slice **per file**, never across a concatenation.

### Low-relevance civ — `civ-grounded`, 50 consecutive sessions (95-159)

Last of 8 on **every** lifetime axis in both the pre-merge and merged trees: `relevance`
1016.24, `relevance_per_sim` 0.978, `avg_score` 1.0259, `alignment` 1.1338, `quality` 0.4396.
Binding constraint is **alignment** (gap 0.2167) not quality (gap 0.0331) — a **voice failure,
not a prose failure**. Lifetime novelty 1.5045 ranks **3rd of 8** (below the 8-civ median
1.6455 but *near the top*) — **not** a second collapse; session 157's report had it as 6th,
so re-derive the rank each session rather than carrying it forward. Extinction risk NONE
(101.6x above the −10 floor). Watch axis: `civ-therapist` took the run low on `alignment`
(0.0650) and `quality` (0.0160) for a 6th session but is mid-field lifetime => watch, not finding.

Chooser-vs-argmax **3/5 (60%)**, up from 0/5; both disagreements took the lower-scoring
candidate. 30-row trailing window 11/30. **The direction is the finding; the rate is not.**
`civ-poetic` 1st on lifetime avg_score/quality/relevance but last on win_rate (0.012);
`civ-precise` best win_rate (0.577), highest lifetime alignment (2.1654), won 4/5.

### Env re-confirmed

- Upstream is **`SuperInstance/AI-Writings`** (the `ai-writings/...` slug 404s). The REST core
  quota was exhausted (0/5000) but the **search API has a separate bucket and still answers**;
  for *absence* claims use `git ls-remote` (0 refs = genuinely empty), never a rate-limited REST
  call. `gh` still not installed.
- NAS EDQUOT total (600G/600G). Clone to `/tmp`; `mkdir`+`ln` work => **symlink bridge** is the
  only way in. Verified by inode identity `129:10427` and `-ef`.
- **z.ai credential gap: 46th session** (`ZAI_TOKEN` absent; z.ai 401). **JEV live** (empty
  `questions` -> 422 `too_short` proves the token was accepted).
- The transient NAS mount race on the symlinked deep path **recurred**: the first `ls -la` on
  `/workspace/.../civilizations/` returned "No such file or directory" while everything was
  present. `stat -L` + `readlink -f` + `[-e ]` + 5/5 retries passed. **One `ls` failure is not
  evidence of a missing directory.**
- Pre-flight saved the run for the **6th** time in the series (115, 117, 145, 147, 150, 159):
  40/40 seeds, 40/40 previews, 40/40 md5s, 0 tracebacks, 8/8 + 8/8 on all 5 prompts.

## Session 160 (2026-10-25) — 23rd consecutive clean mock; the p3 disagreement (-0.8900) is the clean-mock series record

- **Run clean (60/60 checks, 0 failures).** per-civ delta = **+10** x 8 = **80 new rows**
  (engineer 1036->1046, formal 1067->1077, grounded 1082->1092, mythic 1039->1049,
  poetic 1061->1071, precise 1031->1041, therapist 1034->1044, whimsical 1094->1104),
  `meta_log` delta = **+5** (533 -> 538), **Winner:** lines = **5**, **80/80** rows
  `[mock-zai`-prefixed with `provider=zai`, **0** rows with a JEV `error` key, **0** rows with the
  2.0/2.0/2.0 fallback triple, **40/40** distinct seeds, **0** `(civ,prompt)` combos with >1 seed,
  sim->competition ts gap at index 4 in **8/8** civs (1.10-23.21 s), **8/8 + 8/8** on all 5
  competition prompts.
- **Pre-flight saved the run for the 6th time in the series** (115, 117, 145, 147, 150, 160).
  `/tmp` was wiped, so the mock was rebuilt from scratch and **all three** known bugs were live
  again: the session-112 index wrap, the session-118 md5-of-whole-message seeding, and the
  session-145 literal-`{}` placeholder. Pre-flight: **40/40** distinct in-batch pairs, **8/8 + 8/8**
  on all 10 canon prompts, **0** tracebacks.
- **NEW — the runbook's "+5 wins+losses" is a TOTAL; the wins/losses SPLIT varies.**
  `civ-precise` took 4 wins / 1 loss (+4/+1), `civ-engineer` 1 win / 4 losses (+1/+4), and the
  other six civs 0 wins / 5 losses (+0/+5). Every civ's `wins+losses` total is **+5** (8/8) and
  the field win total is **+5** (514 -> 519), but asserting `wins == blob_wins + 5` fails for
  every civ that did not win. **Assert the total, and cross-check the field win total.**
- **NEW — a pre-flight FAIL with 8/8 on every per-prompt line is a SCOPE error in the probe, not
  a degenerate mock.** The first pass probed all 10 canon prompts (80 distinct pairs) but
  asserted a 40-pair total, so it printed `PREFLIGHT: FAIL` while every per-prompt check was
  8/8 PASS. The mock was healthy. **When a pre-flight fails, read the per-prompt lines before
  touching the mock** — scope the totals to the prompts the batch will actually use.
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-precise` won 4, `civ-engineer` 1.
  `civ-poetic` was argmax on **5/5** prompts and won **0/5**. All 4 disagreements took the
  **lower**-scoring candidate (deltas -0.1067, -0.2367, **-0.8900**, -0.3167). The p3 gap of
  **-0.8900** is the **largest single disagreement in the clean-mock series**, exceeding the
  session-137 record (-0.683) and the session-138 record (-0.6300). 20+ five-sample points
  cannot pin a rate: report it as a sample and keep the **direction** as the finding.
- **`civ-grounded` remains the low-relevance civ (50 sessions, 95-160)** — last of 8 on every
  lifetime axis: `relevance` 1023.82, `relevance_per_sim` 0.9760, `avg_score` 1.0148,
  `alignment` 1.1144, `quality` 0.4317. Absolute gaps: alignment **0.2107** (vs therapist
  1.3251) vs quality **0.0325** (vs formal 0.4642) — quote the absolute gaps, never the ratio.
  Lifetime novelty 1.4983 is **below** median (1.6410) again, so Grounded is losing on **two**
  axes (alignment and novelty) — the condition first noted in session 157. **Extinction risk
  NONE** (1023.82 = 102x above the -10 floor); registry 8, all `generation=1`.
- **Watch axis `civ-therapist` — 6th session at the run bottom, on BOTH axes** (run `avg_score`
  0.7250, run `alignment` 0.0370, both lowest of 8). Lifetime standing still mid-field
  (`avg_score` 1.1804, 6th of 8; `relevance_per_sim` 1.1589, 5th of 8) => **watch axis, not a
  finding**. `civ-grounded` was 7th of 8 on run `avg_score` (0.7577) but 2nd-lowest on run
  `alignment` (0.1090) — the run low and the lifetime low are different civs on different axes;
  that is the rule, not a contradiction.
- **The two stable inverses:** `civ-poetic` = 1st on lifetime `avg_score` (1.5821) / `quality`
  (0.7755) / `relevance` (1597.64) / `relevance_per_sim` (1.5451) and **last** on `win_rate`
  (0.0117, 6/513) — argmax on 5/5 prompts, winner on 0/5. `civ-precise` = best `win_rate`
  (0.5787, 294/508), **highest lifetime `alignment` (2.1564)**, won 4/5 — the mirror inverse.
- **`civ-formal`** = the low-**novelty** axis (lifetime novelty 1.4088, last; alignment 1.6918
  healthy). **`civ-engineer`** — the session-121 low did NOT repeat: 6th of 8 on run `avg_score`
  (0.8763) and 6th on run `alignment` (0.3700), no longer at the run bottom; still 7th of 8 on
  lifetime `avg_score`. Axis stays open, do not promote.
- **Counter gap byte-identical** to sessions 147-150/157 (whimsical -173.15, grounded -84.35,
  formal -85.53, poetic -96.81, engineer -44.25, mythic -51.11, therapist -42.11, precise
  -32.63; total **-609.93**). A fixed per-civ offset, not an accumulating leak.
  `save_state()` has no lock => `relevance_per_sim` is not recomputable from the ledger.
- **Dimension spreads this run:** `alignment` **2.4670**, `avg_score` 0.9597, `novelty` 0.3410,
  `quality` 0.2470 (collapsed again, field mean 0.0736 — the 18th of the last 19 clean-mock
  sessions). **Rank on cross-civ spreads, never on absolute quality levels, never on a single
  run's low.**
- **Re-confirmations:** NAS EDQUOT total (12th session); `gh` not installed (15th session);
  tool timeout 30 s < run ~30-35 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported; the `ls` race
  did NOT reproduce; `civilizations.json` is multi-line JSON, not JSONL; `meta_log` `results` is
  a list of `[civ_id, score]` pairs. z.ai credential gap: 46th session.

## Session 161 (2026-10-25) — the counter-gap epoch trap, and the mock's THREE rebuild fixes

**Run clean (session 161, 24th consecutive clean mock).** per-civ delta = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (538 → 543), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed
with `provider={zai}`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback
triple, **80 distinct `(q,n,a)` triples** (confidences 0.93–1.00), **40 distinct seeds / 80 rows**
with **0** `(civ,prompt)` combos carrying >1 seed, sim→competition ts gap at index 4 in **8/8**
(0.61–0.70 s), and **5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews**.
`git status --porcelain` = **18** modified. **Chooser vs `avg_score` argmax 0/5 (0 %)** — all 5
disagreements took the lower-scoring candidate (max |delta| 0.4633 on p3).

### NEW — the counter gap: NEVER mix epochs, or it fakes an accumulating leak

The gap was first computed as **pre-run blob `relevance` vs post-run ledger sum** → **−628.17**,
which had *drifted* from session 160's −609.93 and looked like the fixed offset was finally
accumulating. It is not. The blob's `relevance` **predates** this run while the ledger
**includes** it, so the run's own scores get subtracted twice.

Compute **both sides in the same epoch**:

| civ | HEAD blob rel | HEAD blob ledger | blob gap | post-run rel | post-run ledger | post-run gap | Δ |
|---|---|---|---|---|---|---|---|
| civ-grounded | 1023.8200 | 1108.1667 | −84.3467 | 1025.7100 | 1110.0567 | −84.3467 | 0.0000 |
| civ-whimsical | 1410.7433 | 1583.8867 | −173.1433 | 1413.0900 | 1586.2333 | −173.1433 | 0.0000 |
| civ-formal | 1194.2467 | 1279.7733 | −85.5267 | 1196.4000 | 1281.9267 | −85.5267 | 0.0000 |
| civ-poetic | 1597.6433 | 1694.4467 | −96.8033 | 1600.8267 | 1697.6300 | −96.8033 | 0.0000 |
| civ-precise | 1436.8433 | 1469.4767 | −32.6333 | 1440.7667 | 1473.4000 | −32.6333 | 0.0000 |
| civ-mythic | 1298.2800 | 1349.3900 | −51.1100 | 1299.6867 | 1350.7967 | −51.1100 | 0.0000 |
| civ-therapist | 1190.2200 | 1232.3333 | −42.1133 | 1191.3233 | 1233.4367 | −42.1133 | 0.0000 |
| civ-engineer | 1167.1567 | 1211.4000 | −44.2433 | 1169.3967 | 1213.6400 | −44.2433 | 0.0000 |
| **TOTAL** | | | **−609.92** | | | **−609.92** | **0.0000** |

**Rule: show both epochs side by side.** If the gap appears to move, first check the two columns
come from the same snapshot. A per-civ Δ of **0.0000** is the proof that the offset is fixed. A
"gap that grows every session" is the symptom of the epoch mix, not of a leak in `save_state()`.
Never quote the epoch-mixed number.

### NEW — a rebuilt mock needs THREE fixes, not two

The two long-named ones (session-112 index wrap, session-118 md5-of-whole-message seeding) are
joined by a third: the **session-144 `Connection: close` + `Content-Length`** pair. Without it
`urllib` (the orchestrator's client) is fine but a plain `curl -X POST` **hangs to the tool
timeout** on a perfectly healthy server — easy to misread as "the mock is down".

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)[:8]` | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ identical text for all 8 civs ⇒ chooser breaks a perfect tie |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to timeout against a healthy server |

Verified this session: HTTP 200 in 1 ms, `[mock-zai seed=…]` present, 8/8 distinct seeds AND 8/8
distinct previews on the **exact long cultural prompt** (lengths 167–199), stable across two
rounds, **0 tracebacks** in `/tmp/mock_zai.log`.

### Low-relevance civ — the low label did NOT rotate (51 sessions, 95–161)

`civ-grounded` remains the lifetime low on all five axes: `relevance` 1025.71,
`relevance_per_sim` 0.969, `avg_score` 1.0073, `alignment` 1.1048, `quality` 0.4279 —
**last of 8 on every one**. Absolute gaps: **alignment 0.2080** (vs therapist 1.3128) vs
**quality 0.0321** (vs formal 0.4600). Alignment is the axis the meta-GAN *selects* on ⇒ a
**voice** failure, not a prose failure. Lifetime novelty 1.4892 is **below** median (1.6160) ⇒
losing on **two** axes (alignment and novelty).

**`civ-therapist` is a watch axis, not a finding** — 7th consecutive session at the run bottom
on **both** `avg_score` (0.1103) and `alignment` (0.0250), but lifetime standing is mid-field
(`avg_score` 1.1702, 6th of 8). The run low and the lifetime low are different civs on different
axes (session-132 rule).

**Inverses hold:** `civ-poetic` 1st on lifetime `avg_score` (1.5704) / `quality` (0.7684) /
`relevance` (1600.83) but **last on `win_rate` (0.012)**; `civ-precise` best `win_rate` (0.579),
**highest lifetime alignment (2.1444)**, 1st on run `avg_score` (0.3923). `civ-formal` remains the
distinct low-**novelty** axis (1.3987, last; alignment 1.6793 healthy). Extinction risk **NONE**
(threshold −10, lowest +1025.71 = 102× the floor); registry 8, `max_civs` 12, all `generation=1`.

---

## Session 163 (2026-10-25) — the `simulations_run` delta is +10 *by construction*, and the confidence-spread check is JEV-side

**Run clean (session 163, 25th consecutive clean mock).** per-civ delta = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (548 → 553), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed
with `provider=zai`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback
triple, **40/40** distinct seeds, **40/40** distinct previews, **8/8** on all 5 competition
prompts, `git status --porcelain` = **19** (18 modified + 1 new report). **94/95 assertions PASS.**

### NEW — the `simulations_run` delta is +10 *by construction*, not by coincidence

The session-157 note ("the `simulations_run` baseline is NOT the ledger row count") described the
counter as offset from the ledger. **The source shows they are the same quantity:**
`run_simulation()` appends exactly one ledger row and increments `self.sims_run` exactly once
(`civilization_orchestrator.py:206`), and the **competition** phase calls `run_simulation()` again
via `ex.submit(c.run_simulation, prompt, providers)` (`:252`). So on a clean `--sims 5 --prompts 5`
run: **Δrows == Δsimulations_run == +10** per civ.

I asserted **+5** this session and got 8 false failures. The correct rule is now unambiguous:

> **Assert `Δsimulations_run == Δrows == +10`.** The historical "+260 counter gap" is an **epoch
> artifact** (the ledger predates the counter), not a live divergence — and the *sign* of the gap
> flips with the epoch mix, so never quote an epoch-mixed gap (see the session-161 two-epoch
> rule). Read both baselines from the **git blob's** `culture.json`, not the working tree.

### NEW — the confidence-spread check is a JEV-liveness check, NOT a mock check

The harness flagged "broad confidence spread (>=10 distinct)" as FAIL: this run's 80 rows carry
only **6 distinct confidence values** (0.95–1.00) where the 80 rows immediately before carried
**52** (0.27–1.00). The naive reading is "the mock went degenerate."

**It did not.** 40 distinct mock bodies are present and **24 of them map to two or more different
JEV score triples** — so JEV is genuinely scoring content, not returning a constant. The narrow
confidence band and the collapsed `quality` axis (field mean **0.030**, range 0.01–0.07) are
properties of the **JEV model on this content**, and the `quality` collapse reproduces the
**19-of-the-last-20 clean-mock sessions** regime (119/121/122/138) documented in sessions 160–161.

> **Rule: never report a confidence-spread failure as a mock failure without running the
> same-body / different-triple test.** Group the 80 new rows by mock body (strip the
> `[mock-zai seed=…]` prefix) and count distinct JEV triples per body. If >1 body carries >1
> triple, JEV is discriminating and the confidence band is JEV's, not the mock's. The
> mock-integrity checks remain **seed** and **preview** distinctness, which passed 40/40.

### Low-relevance civ — the low label did NOT rotate (53 sessions, 95–163)

`civ-grounded` remains the lifetime low on all five axes: `relevance` 1036.62,
`relevance_per_sim` 0.961, `avg_score` 0.9991, `alignment` 1.0872, `quality` 0.4208 —
**last of 8 on every one**. Absolute gaps: **alignment 0.2026** (vs therapist 1.2898) vs
**quality 0.0321** (vs formal 0.4529) — a 6.3× wider alignment gap. Alignment is the axis the
meta-GAN *selects* on ⇒ a **voice** failure, not a prose failure. Lifetime novelty 1.4892 ranks
6th of 8, below the median band ⇒ losing on **two** axes (alignment and novelty), the same
shape as session 161.

**`civ-therapist` is a watch axis, not a finding** — took the run-level low on `alignment`
(0.1040) and 6th of 8 on run `avg_score` (0.4560), but lifetime standing is mid-field
(`avg_score` 1.1598, 6th of 8). Session-132 rule respected.

**Inverses hold:** `civ-poetic` 1st on lifetime `avg_score` (1.5563) / `quality` (0.7557) /
`relevance` (1616.68) / `relevance_per_sim` (1.519) but **last on `win_rate` (0.011, 6/522)** —
it was the `avg_score` argmax on **3 of 5** prompts and won **zero**. `civ-precise` best
`win_rate` (0.579, 303/220), **highest lifetime alignment (2.1168)**, won **4/5** at
`preferred_temp` 0.2. `civ-formal` remains the distinct low-**novelty** axis (1.4021, last;
alignment 1.6593 healthy). Extinction risk **NONE** (threshold −10, lowest +1036.62 = 104× the
floor); registry 8, `max_civs` 12, all `generation=1`.

**Chooser vs `avg_score` argmax: 1/5 (20 %)** — 2/5 in session 162, 0/5 in session 157. All four
disagreements took the **lower**-scoring candidate (−0.1700, −0.0900, −0.2467, −0.0167).
Trailing 30-row window now reads `...010100` + `10000` = **11/35**. A 5-sample point still
cannot pin a rate ⇒ the honest claim is *somewhere in 0–80 %*. **The direction is the finding;
the rate is not.**

### Environment — the hardcoded `CIVS_DIR` is why the symlink bridge must exist BEFORE the run

The script hardcodes `CIVS_DIR = /workspace/repos/ai-writings/cellular-first-design/code/civilizations`.
A clone under any other path fails at the **first** `REGISTRY.read_text()` with
`FileNotFoundError` — *before* any provider call, *before* any write — which reads like a
missing file rather than a missing bridge. **Build the bridge first**, target the **nested**
`cellular-first-design` dir (never the repo root), and verify with inode identity
(`stat -L -c '%d:%i'` on both sides + `-ef`), not `ls`. Session 163: `129:12601` both sides.

`/tmp` was empty again ⇒ mock rebuilt from scratch with all **three** fixes (session-112 index
wrap, session-118 md5-of-whole-message seeding, session-144 `Connection: close` +
`Content-Length`). Pre-flight: 8/8 distinct seeds AND 8/8 distinct previews, cultural-prompt
lengths 167–199, HTTP 200 in 1.6 ms, 0 tracebacks, 0 `EXC:`. Teardown: killed the **server** pid
by exact argv; 0 remaining procs; `curl` exit 7 = port closed.

## Session 164 (2026-10-25) — a fresh workspace is not a missing repo; the bridge is the whole job

**Verification held (26/26 checks).** per-civ Δ = **+10** × 8 = **80 new rows** (engineer
1076→1086, formal 1107→1117, grounded 1122→1132, mythic 1079→1089, poetic 1101→1111,
precise 1071→1081, therapist 1074→1084, whimsical 1134→1144), `meta_log` Δ = **+5** (553 → 558),
`Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed with `provider={zai}`, **0** JEV
`error` keys, **0** 2.0/2.0/2.0 fallback triples, **40 distinct seeds / 80 rows** with **0**
`(civ,prompt)` combos carrying >1 seed, `git status --porcelain` = **18 modified**
(8 ledgers + 8 cultures + meta_log + leaderboard), +1 new report file.

### The workspace was **completely empty** — not "the repo is missing"

At session start `/workspace` held only `.plugin-cache`. The prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist (7th
consecutive occurrence). Recovery, in order:

1. `GET /search/repositories?q=ai-writings` with `GITHUB_TOKEN` → the org's own repo is
   **`SuperInstance/ai-writings`** (API is case-insensitive; the remote confirms
   "This repository moved → `SuperInstance/AI-Writings`"). The `ai-writings/cellular-first-design`
   slug 404s — do not use it.
2. **Clone to `/tmp`, never `/workspace`.** Cloning straight into `/workspace` fails with
   `error: .../.git/description: close error: Disk quota exceeded` *while `ls` still shows a
   half-created `.git` directory* — check the clone's **stderr**, not just its exit code.
3. `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`
   — the link target is the **nested `cellular-first-design` dir**, not the clone root.
   Verify with `stat -L -c '%d:%i'` (both sides `129:3669`) **and** `-ef`. Never flatten.

**New this session:** the **NAS write trap also blocks file delivery.** `cp` of a 10 KB report
into `/workspace/output/` exited 1 with `Disk quota exceeded` and left a **0-byte** file; a
direct `open(path,'w').write('x'*100)` also produced a **0-byte** file with **no error at all**.
So *no* file can be materialized under `/workspace` — not even a small one, and not even
without `cp`. **Deliver reports by pushing to git and citing the remote URL** (verified
`Accept: application/vnd.github.raw` returns the full 10 749 bytes), not via a workspace
attachment. Do not emit a `<media>` tag pointing at a 0-byte workspace file.

### The mock needs **FOUR** fixes, not three

The session-160/151 reports say "the two load-bearing fixes" (112 index wrap, 118 md5 seeding);
the session-160 note adds the session-144 transport pair. The **session-145 interpolation fix
is a fourth independent one** — the response template was written as a literal
`"[mock-zai seed={}] "` with no `.format()` call, so every response carried the seed `{}`
(1 distinct seed, not 40) while the mock was healthy by *every* socket-level check: HTTP 200,
prefix present, 0 tracebacks, correct row counts, exit 0. **Only the `distinct seeds == 40`
assertion caught it.** Full rebuild checklist:

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)[:8]` | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text ⇒ the chooser breaks a perfect tie |
| c | `Connection: close` + `Content-Length` | 144 | `urllib` fine, but `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | 145 | every row carries the literal seed `{}` ⇒ 1 distinct seed, not 40 |

**Pre-flight this session:** 40 requests using the **exact long cultural prompt**, HTTP 200 in
1.2 ms, **40/40 distinct seeds**, **40/40 distinct previews**, 214-char bodies, prefix
present, **0 tracebacks**, and each returned seed matched an independently recomputed
`md5(whole_message)[:8]`.

**Tool-timeout trap, restated with the fix:** `setsid nohup … &` **inherits stdout**, so the
tool call blocks to the 30 s timeout *even though the job started*. Redirect stdout/stderr to a
file **and** add `< /dev/null`; then poll `ps` + the log. The 30 s tool timeout is also
< the ~20-45 s orchestrator run ⇒ always detach the orchestrator itself.

### `civ-grounded` — the low-relevance civ, **40 consecutive sessions (125–164)**

Lifetime (8 844 rows): `avg_score` **0.9942** (last), `quality` **0.4175** (last),
`alignment` **1.0802** (last), `relevance` **1041.09** (last), `relevance_per_sim` **0.956**
(last). The structural gap is **alignment: 0.4021 below the next civ (engineer 1.4823) vs
0.0353 on quality = 11.4× wider.** Alignment is the dimension the meta-GAN *selects* on ⇒ a
**voice** failure, not a prose failure. Lifetime novelty 1.4849 is **6th of 8** (not "above
median" — check the rank, the mid-field claim in older reports is wrong at this row count).
Extinction risk **NONE** (threshold −10; lowest relevance 1041.09 = 104× above the floor).

This run Grounded is again last on `avg_score` (0.4477) and `alignment` (0.2940), but the run
is **compressed**: only **0.0050** separates Grounded from `civ-therapist` (0.4527). Report the
lifetime table as the structural signal and the run ranking as the watch axis; a per-run low
that moves to another civ is normal (session 138 saw Grounded 6th of 8 on the run).

### Chooser vs `avg_score` argmax: **0/5 (0 %)** — and every disagreement goes the same way

`civ-precise` won **5/5** yet was the argmax on **0/5**; in all five the chooser took a
**lower**-scoring candidate (p2 whimsical 1.037 vs precise 0.587; p4 poetic 1.207 vs precise
0.593). **11th consecutive session with the "chooser picks lower" direction.** Mechanism
(confirmed in source): the chooser is a JEV **`choice`** question over 150-char
`content_preview` snippets; `avg_score` is the mean of three **`score`** questions on the same
text — different questions, different answers. **Never treat `win_rate` as a quality
metric.** Clean-mock series now has **14** five-sample points (0/5 … 4/5 … 0/5) ⇒ the honest
claim is *somewhere in 0–80 %*, not a point estimate.

### Counter gap: **NEGATIVE** and unchanged in magnitude

`culture.json` `relevance_score` − ledger Σ`avg_score` = **−609.92** total, with per-civ
offsets **identical to the pre-run git blobs** (whimsical −173.14, poetic −96.80, formal
−85.53, grounded −84.35, mythic −51.11, engineer −44.24, therapist −42.11, precise −32.63).
`save_state()` has no lock ⇒ **`relevance_per_sim` is not recomputable from the ledger by an
auditor.** Compute the sign from the data; do not copy it from a prior report.

### JEV liveness vs z.ai (48th session)

JEV: malformed `questions` → **422** `{"type":"dict_type"}` — a payload-shape complaint, so
the token was **accepted**; do not read 422 as "JEV down". z.ai: **401** `token expired or
incorrect` ⇒ endpoint healthy, **credential absent** (`ZAI_TOKEN` is in neither the env nor
any sandbox secret). Control B (mock) is therefore the only provider path, and it needs
**both** `ZAI_TOKEN` (any non-empty placeholder — the token gate runs *before* the URL
override) **and** `ZAI_URL_OVERRIDE`. `TYPESAFEAI_KEY` must be exported from
`TYPESAFE_AI_TOKEN`.

---

## Session 168 (2026-10-25) — clean mock #26; the chooser's "picks lower" streak ENDED at 13 sessions

**Run clean (session 168, 26th consecutive clean mock).** per-civ delta = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (573 → 578), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed
with `provider=zai`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback
triple, **40/40** distinct seeds, **40/40** distinct previews, **8/8** on all 5 competition
prompts, **80/80** distinct `(q,n,a)` triples, meta-vs-ledger `avg_score` mismatches **0**,
`git status --porcelain` = **19** (18 modified + 1 new report). **22/22 assertions PASS.**

### NEW — the meta-vs-ledger check must take the **later-`ts`** row, not the first match

A first-match verifier reports **26/40 false mismatches** on a completely clean run. The sim
phase draws its prompt at random from the same 5 competition prompts, so a `(civ, prompt)` pair
recurs **1–4 times** inside the 10 new rows (this run: 13 pairs × 1, 16 × 2, 9 × 3, 2 × 4). The
**competition-phase** row is the **later `ts`**. Use `max(cands, key=lambda r: r["ts"])` → 40/40
exact. Match key is `m["prompt"][:80]` — the meta `prompt` is full-length, the ledger `prompt` is
truncated to 80 chars.

**This is a verifier bug, not a run defect.** Do not "fix" the run to satisfy the first-match
expectation — same trap class as the `wins+losses` spec error in session 166.

### FINDING — the chooser's "picks lower" direction ended after **13 consecutive sessions**

Chooser-vs-`avg_score`-argmax agreement rose to **3/5 (60 %)** — the highest in the series —
versus the 0–1/5 of sessions 154–166. `civ-precise` swept 3/5. Two of five still picked a
lower-scoring candidate but the deltas were small (−0.0400) vs session 166's max −0.7600.

**The one large disagreement is the real finding: `civ-grounded` won on the *worst* candidate** —
0.9600 against an argmax of 2.0633, a **1.1033** gap, the largest in the series. Grounded is
last of 8 on lifetime `avg_score` / `quality` / `alignment` **and** last of 8 on this run's
`avg_score` / `quality` / `alignment`, yet it won 1 of 5 and its `win_rate` (0.127) is mid-field
against a last-place `relevance_per_sim` (0.952). The *selection* signal and the *quality* signal
disagree most sharply for this civ than for any other.

### `civ-grounded` remains the low-relevance civ — 43 consecutive sessions (95–168)

Last of 8 on lifetime `avg_score` 0.9893, `quality` 0.4099, `alignment` 1.0625, `relevance`
1075.08, `relevance_per_sim` 0.952. Label did **not** rotate. Absolute gaps: **alignment
0.2029** (vs therapist 1.2654) vs **quality 0.0412** (vs formal 0.4511) ⇒ a **4.9×** wider
alignment gap ⇒ a **voice** failure, not a prose failure. Lifetime novelty 1.4954 is **6th of
8**. Run-level: grounded **8th of 8** on `avg_score` (1.1423), `quality` (0.2970) and
`alignment` (0.9060), gap to the next civ **0.3963** — this run was *not* compressed (session
166's run bottom was separated by 0.0034).

**Run levels are *higher* than lifetime this time** (run `avg_score` 1.14–1.96 vs lifetime
0.99–1.55) — the opposite of session 166's depressed level. The **ordering** is the signal, not
the level. Cross-civ run spreads: `avg_score` 0.8170, `alignment` 1.6900, `quality` **0.8440**
(widest in the series — the opposite of session 166's collapsed 0.0430), `novelty` 0.3850.

**Extinction risk NONE** (threshold −10, lowest +1075.08, **108×** the floor). Registry 8,
`max_civs` 12, all `generation=1`.

**Counter gap — both epochs side by side:** blob gap **−609.9200**, post-run gap **−609.9200**,
per-civ Δ **0.0000** for all 8 ⇒ the offset is **fixed**, not accumulating.

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

---

## Session 171 (2026-10-25) — the bridge symlink target must be the NESTED directory

**Run clean (session 171, 28th consecutive clean mock).** per-civ delta = **+10** x 8 = **80 new
rows**, `meta_log` D = **+5** (588 -> 593), `Winner:` lines = **5**, **80/80** rows
`provider=zai`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback
triple, **40/40** distinct seeds, **0** `(civ,prompt)` combos carrying >1 seed, **80/80** rows
match an independently recomputed md5 (seed, colour and figure), **8/8** distinct seeds AND
**8/8** distinct previews on all 5 competition prompts, meta-vs-ledger `avg_score` mismatches
**0/40** (later-`ts` row), registry 8 all gen 1, extinction **NONE**.
**24/24 assertions PASS.**

### NEW — the "symlink points at the clone root" rule has a precondition

The RUNBOOK says the bridge symlink must point at the **clone root**, not the nested
`cellular-first-design` dir. That is right **only when the clone root *is* the
`cellular-first-design` directory**. The rule exists because `git show HEAD:<path>` must run
from the clone root — and that is a *separate* concern from what the symlink targets.

This session the clone root **contains** `cellular-first-design/`, so:

```
ln -s /tmp/repos/ai-writings/AI-Writings            /workspace/repos/ai-writings/cellular-first-design
# -> resolves, but CIVS_DIR = .../cellular-first-design/code/civilizations DOES NOT EXIST
ln -s /tmp/repos/ai-writings/AI-Writings/cellular-first-design        /workspace/repos/ai-writings/cellular-first-design
# -> CORRECT
```

**The two rules are orthogonal and both must hold:**
- `git show HEAD:<path>` must run with `cwd` = the **clone root** (session-170 note 5).
- the **symlink target** must be whichever directory actually contains `code/civilizations/`.

**Cheap pre-flight, before launching anything:**
```
ls /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py
```
A wrong symlink target fails *late* (the script dies on `REGISTRY.read_text()` with
`FileNotFoundError: civilizations.json`) and the error message names a missing file rather than
a missing link, which sends you hunting in the wrong place. **Check the target directory exists
before the run, not after the failure.**

### The six mock fixes, re-applied, 8/8 on the FIRST build

Session 170 ended with a counter-derived seed index (fix (f)) that was caught *after* the
ledger was written. This session the mock was rebuilt correctly from the spec and the
pre-flight passed **8/8 on the first attempt** — no rebuild-drift, no reset-and-rerun. The
gate that carries the weight is **check 7, repeat-same-message => identical seed**: the
pre-flight's other seven steps all send 40 *distinct* messages, so a counter-derived index
looks perfect to every one of them.

Pre-flight: **40/40** distinct seeds, **40/40** distinct previews, **40/40** recomputed md5s,
**8/8** + **8/8** on every prompt, 0 literal `seed={}`, 0 `EXC:`, **40 messages x 2 repeats =>
0 seed mismatches**, 0 `(civ,prompt)` with >1 seed. **8/8 PASS.**
Post-run mock log: 121 OK lines, 0 `EXC:`. Teardown: two pids killed by exact argv match,
`curl -m 5` => **exit 7**, `HTTP=000`.

### `civ-grounded` remains the low-relevance civ - 46 consecutive sessions

Last of 8 on lifetime `avg_score` **0.9970**, `quality` **0.4075**, `alignment` **1.0613**,
`relevance` **1114.06**, `relevance_per_sim` **0.961**. Alignment gap **0.9895** vs quality gap
**0.3418** => **2.9x** wider => a **voice** failure, not a prose failure. Lifetime novelty
**1.5223** is **6th of 8** - Grounded is not boring, it is mis-voiced.

**The run-level low ROTATED to `civ-therapist`** (run `avg_score` **1.4473**, run bottom on
`avg_score` and `alignment` **1.1460**) while its *lifetime* standing is mid-field (6th of 8).
**Watch axis, not the finding** (session-132 rule).

### Counter gap -609.9200, fixed

Byte-identical to sessions 169 and 170, per-civ D **0.0000** for all 8. The offset is
structural, not accumulating. `save_state()` has no lock, so `relevance_per_sim` is not
recomputable from the ledger by an auditor.

### Chooser vs `avg_score` argmax: 3/5 (60 %)

Both disagreements took the **lower**-scoring candidate, so the "picks lower" direction
continues. `civ-precise` swept **5/5**. Max |delta| **0.1633** - a small one, well inside the
session-168 record of **-1.1033**.

### Environment

- Workspace **empty** apart from `.plugin-cache`; the prompt's path did not exist (**12th
  consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`**; the `ai-writings/...` slug 404s (the API is
  case-insensitive).
- Cloned to **`/tmp/repos/ai-writings/AI-Writings`** with `--filter=blob:none --no-checkout` +
  `sparse-checkout set cellular-first-design` => 7.6 MB working tree. Cloning into
  `/workspace` fails with **`Disk quota exceeded`** (NAS EDQUOT, **18th session**); `/workspace`
  was **100 % full, 0 bytes available**, `/tmp` had 28 G free.
- `ZAI_TOKEN` absent from env and all 8 secrets; z.ai **401** `token expired or incorrect` =>
  endpoint healthy, credential absent (**54th session**).
- **JEV live**: well-formed body => **HTTP 200** with `{"model":"jev-1.14.0", ...}`.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code - the token gate returns `None`
  first).
- `gh` not installed (**20th session**) - used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s => detached launch, stdout redirected,
  `< /dev/null`.


---

## Session 185 (2026-10-25) — the repo owner is NOT the path owner; two verifier traps that fake a mock regression

### 1. THE REPO OWNER IN THE PROMPT PATH CAN BE A DECOY

The task named `/workspace/repos/ai-writings/…`. The GitHub owner `ai-writings` **exists** and
returns HTTP 200 on its org page — but it is a *different project*: 7 repos
(`ai-writing`, `ai-writing-tools`, `ai-writing-tool`, `ai-writing-free`, `PakePlus*`), all
README-only. The actual `cellular-first-design` subtree lives under
**`SuperInstance/ai-writings`**.

How to find the real owner, in order of reliability:
1. `git ls-remote https://x-access-token:$GITHUB_TOKEN@github.com/<owner>/<repo>.git`
   → *Repository not found* = genuinely absent (0 refs), **not** rate-limit noise.
2. Scrape the owner's repo list from the **web page** (`https://github.com/<owner>?tab=repositories`
   and grep `href="/<owner>/..."`) — this is **not** subject to the REST rate limit.
3. The REST API (`/users/…/repos`, `/search/repositories`) returns **403 rate-limited** and
   renders as "no repos" for every owner at once. **Do not use it to assert absence.**

*Rule: the path in a task prompt is a claim about location, not evidence. Verify the owner
before you conclude anything about the workspace.*

### 2. TWO VERIFIER TRAPS THAT BOTH PRODUCE A FALSE "80/80 MISMATCH"

Both make the **spec-recompute** check fail on **every** row while every structural check
(sim counts, deltas, provider set, non-degenerate seeds) still passes. Two rounds lost to these.

**(a) The `prompt` field is stored IN FULL.** The orchestrator has `sim["prompt"] = prompt[:80]`,
but the CANON prompts are all shorter than 80 chars, so the truncation **never fires**. A verifier
that does `if r["prompt"] == p[:80]` for a CANON list `p` will match nothing and recompute
against a *wrong or empty* message. **Check the stored value's length; do not assume the
truncation happened.**

**(b) The cultural-prompt template ends with a closing quote AND a period.** The exact source is:

```python
cultural_prompt = f"""You are a voice in the tradition of "{self.culture['name']}".
Your tenets: {', '.join(self.culture['tenets'])}.
Your voice: {self.culture['voice_emphasis']}.

{prompt}"""
```

A rebuild that writes `tradition of "{name}.` (no closing quote) produces a **different md5** ⇒
80/80 false mismatches. **Always `grep -A 5` the template out of the source. Never rebuild it
from memory.**

*(Note: the `write`/`read` tools are jailed to the workspace, and the workspace NAS is 100% full,
so the source must be read with `grep`/`sed` over bash against the `/tmp` clone.)*

### 3. A `(q,n,a)` SCORE-TRIPLE COLLISION IS A JEV PROPERTY, NOT A MOCK DEFECT

Session 185 produced **73/80** distinct `(quality, novelty, alignment)` triples. The cause is
**not** mock degeneracy: the 80 rows carry **40 distinct mock outputs** (each `civ` x `prompt`
output appears 2x on average — once in the sim phase, once in the competition phase, with the
per-phase prompt draw random), and JEV quantized **7 pairs of genuinely different outputs** to
identical score triples.

**The load-bearing non-degeneracy check is the seed+color+figure recompute** (80/80 this
session), not the score triple. A score triple is JEV's *output granularity*; the seed is the
mock's *identity*. **Do not report a triple collision as a mock regression** — verify which of
the two you are actually measuring before writing it up.

### 4. The run-level low keeps rotating; the axis does not

Session 185's run-level low was `civ-mythic` — a **6th different civ in 6 sessions** — while the
**lifetime** low stayed `civ-grounded` for the **58th consecutive session**. The axis is stable:
**alignment** gap 1.1880 vs quality gap 0.0100 = **119x wider** ⇒ every low-relevance civ is a
**voice** failure, not a prose failure. **Watch the axis, not the holder.**

## Session 203 additions (2026-10-25)

- **A VERIFIER THAT READS A KEY THE ARTIFACT DOES NOT HAVE FAILS 5/5 AND STILL LOOKS
  LIKE A DATA PROBLEM.** `meta_log.jsonl` rows carry **9 keys**
  (`iso, prompt, results, ts, winner_civ, winner_name, …`) — there is **no top-level
  `avg_score`**. The competition scores live **inside `results`** as
  `[[civ_id, score], …]`. A check written as `r.get("avg_score", -99)` therefore
  mismatches **every** row and reports "meta-vs-ledger mismatches 5/5", which reads
  exactly like a corrupted ledger. The same comparison against `results` gave
  **0/40 mismatches** on the very same run. *Assert the key EXISTS before comparing
  its value; a silent default converts a schema mistake into a plausible "the data is
  wrong" story.* The `results` shape also changes what "later-`ts` row" means — the
  competition-phase row for a `(civ, prompt)` pair is the later-`ts` ledger row, and
  its `avg_score` must equal that civ's entry in `meta.results`.
- **THE 202 SESSION COINCIDENCE (RUN LOW == LIFETIME LOW) DID NOT REPRODUCE.** Session
  202 had `civ-grounded` as both; session 203 put `civ-grounded` **6th of 8** on run
  `avg_score` while the run low rotated to `civ-therapist`. *Never carry a coincidence
  forward as a pattern — re-read this run's own rows.*
- **THE NOVELTY SPREAD WAS THE NARROWEST IN THE SERIES (0.1770) AGAINST AN ALIGNMENT
  SPREAD OF 1.9850 — A 2.50x ratio.** The alignment spread was also the **widest**
  recorded. The low-relevance signature ("high novelty, low alignment") still holds, and
  the two low civs are cleanly separated: `civ-whimsical` has the **widest alignment
  gap** (1.9850) but `civ-therapist` has the **lowest `avg_score`** (1.3583) on the
  fleet's lowest **quality** (0.6530). *The widest single-axis gap and the lowest
  composite can belong to different civs — report both.*
- **THE CHOOSER HAS NOW NEVER UP-GRADED ACROSS 203 SESSIONS.** Agreement across
  sessions 199-203 is 0 → 2 → 3 → 1 → **2**; every disagreement took the **lower**-
  scoring candidate. `civ-poetic` was argmax on **3 of 5** prompts and won **0 of 5**.
  The `best_civ` criteria map (`civ_id` -> `civ name`) is a *label* map and remains the
  standing suspect.
- **THE WORKSPACE WAS WIPED AGAIN (ONLY `.plugin-cache` PRESENT) — THE SPARSE-CLONE
  RECIPE STILL WORKS END-TO-END.** `SuperInstance/AI-Writings` sparse-cloned into
  `/tmp` (NAS at 100 % quota), `git sparse-checkout set cellular-first-design/code/civilizations`,
  then a symlink at `/workspace/repos/ai-writings/cellular-first-design` -> the
  **inner** dir, verified by inode identity (`113:97` both sides) and
  `os.path.samefile()` → `True`. `ls -remote`/`git ls-remote` on the `ai-writings/…`
  slug still 404s; the real owner is `SuperInstance/AI-Writings` and `cellular-first-design`
  is a **subdirectory**, not a repo.
- **THE PRE-FLIGHT BAND GATE CAUGHT THE FRESH MOCK BUILD THREE TIMES: 287 → 294 → 352.**
  The 332-369 band is the binding constraint on the response body. The fix each time was
  to **change the constant tail**, never to trim the longest instance — the prefix width
  varies with the seed, so the *tail* is the control, not the total. Target **352**.
  Computing the tail length in Python first (`352 - len(current)`) beat three rounds of
  guess-and-check.

## Session 206 additions (2026-10-25)

- **A PER-PROMPT ROW-COUNT ASSERTION IS A CHECKER BUG, NOT A RUN BUG — THE SIM PHASE
  DRAWS PROMPTS AT RANDOM.** The verifier check *"per-prompt 8/8 distinct seeds AND
  previews"* was red on the first run because it also asserted `n == 8`. The per-prompt
  row counts are **13 / 17 / 17 / 18 / 15**, not 8: the sim phase runs 5 sims per civ
  drawing from the 5 prompts **uniformly at random** (a prompt gets 0-2 sim-phase rows),
  and the competition phase contributes exactly **one** row per civ per prompt. The
  correct assertion is **8 distinct seeds and 8 distinct previews** per prompt — the
  *uniqueness* of the competition phase, not its row count. The distinctness assertions
  were green for all five prompts from the start. *The competition phase is identified by
  uniqueness; the sim phase is identified by multiplicity. Never assert a row count
  where a distinctness count is meant.*
- **THE CHOOSER HAS NOW NEVER UP-GRADED, AND IT TOOK THE LOSER ON EVERY PROMPT.**
  Agreement across sessions 199-206 reads 0 → 2 → 3 → 1 → 2 → 1 → **0** (0/5, 0 % — the
  lowest reading in the series). `civ-poetic` was the `avg_score` argmax on **5 of 5**
  prompts and won **0 of 5**; the largest disagreement ("the witness log") was
  **2.1000 chosen vs 2.6333 argmax** (−0.5333). A chooser that picks the lower-scoring
  candidate *every* time is **anti-correlated** with `avg_score`, not merely noisy. The
  standing suspect is unchanged: the `best_civ` criteria map (`civ_id` -> `civ name`) is
  a **label** map, so the chooser may be scoring labels rather than texts.
  *The next real experiment is still to bypass the chooser and rank purely by
  `avg_score`.*
- **THE RESPONSE-BODY BAND CAN BE SOLVED ALGEBRAICALLY, BEFORE THE TEMPLATE IS
  WRITTEN.** The mock header `[mock-zai <8-hex>] #<6-hex> <figure>.` has width
  **33-37** across all 40 (civ, prompt) messages (the figure name length varies). A
  fixed tail of length *T* yields body totals *min+T+1 .. max+T+1*, so the **332-369**
  band is satisfiable iff ***T* ∈ [298, 331]**. Choosing *T* = **320** gives totals
  **354-358** — the documented 352-358 window — on the **first** build. The prose was
  written to hit 320 characters by *counting*, not by trimming.
  *A band check is a variance check: solve the band algebraically, then write the
  template to fit it, instead of iterating the template against the band.*
- **ENVIRONMENT (session 206).** Workspace wiped again (only `.plugin-cache`).
  `SuperInstance/AI-Writings` sparse-cloned into `/tmp` (NAS 100 % quota) +
  `git sparse-checkout set cellular-first-design/code`; the symlink bridge
  `/workspace/repos/ai-writings/cellular-first-design` -> the **inner**
  `cellular-first-design` dir, verified by inode identity (`129:10423` both sides)
  and `os.path.samefile()` → `True`. `HOME` had to be redirected to `/root` —
  `/workspace/.home/.gitconfig` cannot be written (NAS EDQUOT), so the global git
  config was re-created on the overlay filesystem. z.ai credential gap **79th session**
  (HTTP 401 `token expired or incorrect`); JEV live at `jev-1.14.0` with
  `TYPESAFEAI_KEY` exported as an alias of `TYPESAFE_AI_TOKEN`. Baseline derived from
  the **git blob** at `2d2a417`. Mock torn down by exact-argv kill (2 pids) and the
  port proven closed (`curl` exit **7**, `HTTP=000`).

## Session 211 (2026-10-25) — the CHOOSER/ARGMAX STREAK RECURRENCE, and the counter-gap constant

**Run clean (session 211).** per-civ delta = **+10** x 8 = **80 new rows**, `meta_log` D =
**+5** (788 -> 793), `Winner:` = **5**, **80/80** rows `provider=zai` with the `[mock-zai`
prefix, **0** JEV `error` keys, **0** 2.0/2.0/2.0 fallback triples, **80/80** rows match
an independently recomputed seed+color+figure, **40** distinct seeds (message-level), **0**
`(civ,prompt)` slots with >1 seed, per-prompt **8/8** distinct seeds AND previews on all 5
competition prompts, **80/80** distinct `(q,n,a)`, relevance delta == sum(`avg_score`) **8/8**
exact (max residual **6.86e-13**), wins **+5** / losses **+35**, counter gap **UNCHANGED 8/8**,
registry 8 all gen 1, extinction **NONE** (lowest +1720.01 = **172x** the floor),
leaderboard 8 sorted. **Pre-flight PASS on the FIRST build (13/13).** **29/29 assertions PASS.**

### NEW — a 0 % chooser/argmax agreement is the THIRD recurrence, not a one-off

Session 199 reported 0/5 (5 down-grades, 0 up-grades). Session 211 reports **0/5 again**
(**5 down-grades, 0 up-grades**). The intermediate sessions recovered to 2/5-4/5, so the
series does **not** show a clean trend in either direction — it shows a **regime that
alternates**. *Rule: never carry a streak counter forward as a hypothesis. Re-derive the
up/down counts from THIS session's own meta_log every time. Sessions 199 and 211 are
separate zeroes, not one continuing streak.*

### NEW — the counter-gap values are now a FIXED FLEET CONSTANT

The `culture - ledger` gaps are **bit-identical** to session 210's:
`grounded -84.35, whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63,
mythic -51.11, therapist -42.11, engineer -44.24`. These are historical merge artefacts
that stopped moving once the fleet's row-writing path stabilised. *A gap that MOVES is
still the defect — the check remains worth running (it is the cheapest merge-integrity
check in the series), but expect it to be a no-op and do not read a frozen gap as a
newly-clean merge.*

### NEW — the lifetime low and the run low diverged on the AXIS for the first time

`civ-grounded` (lifetime low, 1720.01, 80th consecutive session) had a **quality-led**
deficit this run (quality **1.2630**, fleet-low) rather than the usual alignment gap,
while the run low `civ-whimsical` (avg_score **1.3997**) was **alignment-led**
(alignment **0.8430**). The run low was also a civ whose lifetime standing is **3rd of 8**.
*Rule: report the axis per civ, and never predict the run-low holder from the previous
session — this session's holder was a mid-table lifetime civ, not the usual suspects.*

### Re-confirmations (this session)

- The bridge symlink must point at the **inner** `cellular-first-design/code` directory
  (verified by inode identity **129:10424** both sides + `os.path.samefile()` -> `True`).
  A bridge to the clone root leaves `code/civilizations/` unresolvable and the failure
  reads as "the repo is missing".
- The repo is **`SuperInstance/AI-Writings`** (a *user* account; `GET /orgs/ai-writings/repos`
  **404s** while `GET /search/repositories` finds it). The GitHub API is case-insensitive,
  so the `ai-writings` slug resolves to `AI-Writings`. Located via
  `GET /search/repositories?q=ai-writings+in:name` then the `contents/` walk.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or
  incorrect`** (**83rd session**) => endpoint healthy, credential absent.
  `ZAI_URL_OVERRIDE` alone is dead code behind the token gate: Control B needs **both**.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`;
  **0** fallback triples.
- Pre-flight check 5 (independently recomputed seed+color+figure) is the check that
  catches a wrong mock **shape**; the length band alone would not.
- Baseline pinned to the **pre-run commit** `a715cb9` and read from the **git blob** —
  never from a remembered count.
- `gh` is not installed; `GIT_SSL_NO_VERIFY=1` required for fetch/push; push to the
  explicit token URL and verify with `git ls-remote` **and** the commits API. The remote
  per-civ row counts were re-read from the API to confirm the 80 new rows landed.
- Mock teardown by exact-argv match (wrapper **and** server pid), then prove the port
  closed (`curl` exit 7 = refused). Never `pkill -f mock_zai` (self-match).

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

## Session 221 (2026-10-25) — the bridge `ls` TRAILING SLASH fails while the NON-SLASH form succeeds

**Run clean (session 221).** per-civ delta = **+10** x 8 = **80 new rows**, `meta_log` D = **+5**
(838 -> 843), `Winner:` lines = **5**, **80/80** rows `provider=zai`, **0** rows with a JEV
`error` key, **0** rows with the 2.0/2.0/2.0 fallback triple, **80/80** rows match an
independently recomputed seed+color+figure, **40/40** distinct seeds (message-level), **0**
`(civ,prompt)` combos carrying >1 seed, relevance delta == sum(`avg_score`) **8/8** exact
(max residual **1.07e-12**), wins **+5** / losses **+35**, counter-gap **byte-identical** for
all 8, meta-vs-ledger **0/8** mismatches, registry 8 all gen 1, extinction **NONE** (lowest
**+1907.82 = 190.8x** the floor). **Pre-flight PASS on the FIRST build (13/13).**
**20/20 data assertions PASS.**

### NEW — `ls -la <bridge>/civilizations/` FAILS; `ls -la <bridge>/civilizations` SUCCEEDS

The verification command the prompt asks for is `ls -la .../code/civilizations/` — **with a
trailing slash**. Against the symlink bridge that form returns
`ls: cannot access '...': No such file or directory`, while the **same path without the
trailing slash** lists the directory perfectly. The trailing slash forces a
symlink-resolution step the sandbox bridge does not satisfy, so the probe reports a
**missing repo** when the repo is present and the run wrote to it.

*Rule: when verifying a symlink bridge, use the NON-SLASH form (or read the resolved target
directly). A trailing-slash `ls` failure is a PROBE ARTIFACT, not a broken bridge — confirm
with `readlink -f` + inode identity before concluding anything. This is the 20th
consecutive session with a wiped workspace path, and the first where the *verification
command itself* was the thing that lied.*

### NEW — the workspace SKILL stub cannot be written (NAS EDQUOT), so the durable lesson goes in the REPO's SKILL file

`/workspace/.skills/civ-orchestrator-learnings/SKILL.md` is a **0-byte** file on a **100 % full**
NAS. A heredoc write to it returns `cat: write error: Disk quota exceeded` and leaves the
file at **0 bytes** — a silent truncation of a file that previously held content.

*Rule: the authoritative operational log is the REPO's
`cellular-first-design/code/civilizations/skills/civ-orchestrator-learnings.md` (on the
overlay, writable). Put durable lessons THERE and commit them. The workspace skill stub is
a per-session convenience, and the `write` tool is jailed to the workspace root, so
`/tmp` artifacts need a bash heredoc.*

### Findings

- **`civ-grounded` remains the lifetime low — 89th consecutive session.** Lifetime
  `relevance` **1907.82** (last of 8), `relevance_per_sim` **1.150** (lowest in the fleet),
  `win_rate` **0.091** — 3rd-best. Run `avg_score` **2.1803** (**4th of 8**), `alignment`
  **2.5890** (**2nd-highest**) ⇒ **the lifetime deficit is NOT a voice failure this run**;
  `civ-grounded` posted a *strong* run. Lowest relevance **+1907.82 = 190.8x** the -10 floor.
- **The run-level low ROTATED to `civ-whimsical`** (run `avg_score` **1.7260**, `quality`
  **1.3610** fleet-low, `alignment` **1.3330** fleet-low) while its lifetime standing is
  **3rd of 8** (`relevance` 2298.74, `relevance_per_sim` 1.392). Axis gap: alignment
  **1.9950** vs quality **0.5820** = **3.43x** wider => a **voice** failure, not a prose
  failure. *The holder rotates; the axis does not.*
- **Chooser vs `avg_score` argmax: 4/5 (80 %)** — `civ-precise` won **4/5** and was the argmax
  on **4/5**; the single disagreement took the **lower**-scoring candidate (`civ-grounded`
  won prompt 3 at 2.3833 over `civ-precise` at 2.8400). **1 down-grade, 0 up-grades.**
  *Re-derived from this session's own `meta_log`; the down-grade streak for this session
  is 1 and must be re-based next session, not carried forward.*
- Run spreads: `avg_score` **0.8440**, `alignment` **1.9950** (widest), `quality` **0.5820**,
  `novelty` **0.1080** (**narrowest in the series**).

### Re-confirmations

- The prompt's path did not exist (**20th consecutive occurrence**); the workspace held only
  `.plugin-cache` and an **empty** `civ-orchestrator-learnings` stub. Clone
  `SuperInstance/AI-Writings` to the **overlay** (`/opt`, 28 G free) — cloning into
  `/workspace` dies on `.git/description` with `Disk quota exceeded` (NAS EDQUOT, **20th
  session**) — and bridge the **inner `cellular-first-design/code`** by symlink, verified by
  inode identity `129:12603` both sides + `readlink -f`.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or
  incorrect`** (**90th session**) => endpoint healthy, credential absent.
  `ZAI_URL_OVERRIDE` alone is dead code behind the token gate — Control B needs **both**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0**
  fallback triples.
- The mock algorithm was **re-derived from the ledger and verified 480/480 exact** BEFORE the
  run. Header is a **constant 44 chars** => a **293-char** tail puts the body at **337**,
  inside the 332-369 band on the **first** build; the cultural-prompt band is measured from
  the **real** `culture.json` files (**167-209**).
- Baseline pinned to the **pre-run commit** `e33d77c` and read from the **git blob**.
- `gh` not installed (**23rd session**); `GIT_SSL_NO_VERIFY=1` required; push to the explicit
  token URL and verify with `git ls-remote` **and** the commits API (both show `6856877`).
- Mock teardown by **PID captured from `ps`**; **0** remaining procs; `curl` exit **7**.

## Session 223 additions (2026-10-25)

### 1. THE CULTURAL-PROMPT TEMPLATE HAS **NO BLANK LINE** AFTER THE TRADITION LINE

The orchestrator's f-string is three tight lines, then a blank, then the prompt:

```python
cultural_prompt = f"""You are a voice in the tradition of "{self.culture['name']}".
Your tenets: {', '.join(self.culture['tenets'])}.
Your voice: {self.culture['voice_emphasis']}.

{prompt}"""
```

A rebuild that formats the prose with a blank line between each of the first three lines
produces a **different md5** => **0/80** spec-recompute matches on a perfectly healthy mock
(HTTP 200, prefix present, 0 tracebacks, correct row counts, exit 0). The second derivation,
with single newlines, matched **80/80** — the whole difference is one whitespace byte per line.

*Rule: **grep the template out of the source** and reproduce it byte-for-byte before believing
a spec-recompute mismatch count. A spec-recompute failure with every structural check green is
a **template-bytes defect** until proven otherwise, not a data defect. This is the same class
as the session-185 "no closing quote" variant.*

Independent second signal: the **cultural-prompt band is 167-209** chars on the real
`culture.json` files. A blank-line rebuild lands at **201-211** for the shorter civs —
**outside** the band. Band miss + 0/80 recompute together = template bytes; recompute miss
*inside* the band = a different defect (index, width, or digest input).

### 2. THE MOCK ALGORITHM WAS RE-DERIVED FROM THE LEDGER AND VERIFIED **80/80 EXACT**

`d = md5(cultural_prompt).digest(); h = d.hex(); i = d[0] % 4; seed = h[(i*2)%8:(i*2)%8+4];
color = h[8:12]; figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` — checked against the last 10
rows of every civ, with the **real** `culture.json` files on disk. 80/80 exact.

**The body band was solved algebraically before the template was written**: the header
`[mock-zai <seed>] #<color> <figure>. ` is a constant **38** chars, so a **298**-char tail
gives a constant **336**-char body — inside the 332-369 band on the **FIRST** build.
Sizing the tail by *counting words* (`352 - len(current)`) beats iterating the template
against the band. Pre-flight **10/10 on the first build**, 129 OK mock lines, 0 `EXC:`.

### 3. THE CHOOSER TOOK THE LOWER-SCORING CANDIDATE ON **4 OF 5** PROMPTS, WITH **0** UP-GRADES

`civ-poetic` was the `avg_score` argmax on **4 of 5** prompts and won **0 of 4**; `civ-precise`
won **3/5** and was the argmax on **1/5**. Largest disagreement **-0.3700**. The
`best_civ` criteria map (`civ_id` -> `civ name`) remains a **label** map and the standing
suspect. *Re-derive the up/down counts from this session's own `meta_log`; never carry a
streak counter forward as a hypothesis.*

### 4. THE BRIDGE TARGET IS THE **CLONE ROOT**, AND THE `ls` WITH A TRAILING SLASH LIES

`CIVS_DIR = /workspace/repos/ai-writings/cellular-first-design/code/civilizations` resolves
only if the symlink points at the directory that **contains** `code/civilizations/` — for a
clone whose root holds `cellular-first-design/`, that is the **inner** dir, and the bridge
`/workspace/repos/ai-writings/cellular-first-design -> /tmp/aw/cellular-first-design`
resolves it (inode `129:12601` both sides + `os.path.samefile()` -> `True`).

`ls -la <path>/` (trailing slash) returned **"No such file or directory"** while the
**non-slash** form listed the directory perfectly — the same probe artifact as session 221.
*Use the non-slash form, or read the resolved target.*

### 5. LOW-RELEVANCE CIV — `civ-grounded`, **91st consecutive session**

Lifetime `relevance` **1945.57** (last of 8), `relevance_per_sim` **1.159** (lowest),
`win_rate` **0.089** (3rd-best). Run `avg_score` **1.7800** (7th of 8) with alignment
**1.8030** (6th-highest) => **the lifetime deficit is NOT a voice failure this run**;
Grounded posted a middling run. Lowest relevance **+1945.57 = 194.6x** the -10 floor.

The **run-level low** was `civ-therapist` (avg **1.5163**, quality **0.8010** fleet-low,
alignment **1.0890** fleet-low) while its lifetime standing is 7th of 8. Axis gap: alignment
**1.8500** vs quality **0.7690** = **2.41x** wider => a **voice** failure. *The holder
rotates; the axis does not.*

Run spreads: `avg_score` 0.8603, `alignment` **1.8500** (widest), quality 0.7690,
novelty **0.1570** (narrowest). **Rank on cross-civ spreads, never on absolute levels.**

### 6. ENVIRONMENT (re-confirmed)

- NAS EDQUOT total (**21st session**) — clone into `/workspace` dies on `.git/description`
  with **Disk quota exceeded**; `/tmp` (overlay) is exempt. **Symlink bridge is the only way in.**
- **z.ai credential gap: 92nd session** (`ZAI_TOKEN` absent from env and all 8 secrets; z.ai
  **401 `token expired or incorrect`** => endpoint healthy, credential absent). Control B needs
  **both** `ZAI_TOKEN` (placeholder) **and** `ZAI_URL_OVERRIDE` — the override alone is dead code.
- **JEV live at `jev-1.14.0`** (well-formed body -> HTTP 200 with the model string;
  malformed `questions` -> 422 `too_short`, a payload-shape complaint that proves the token
  was accepted). `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; **0** fallback triples.
- `gh` is not installed (**25th session**); `GIT_SSL_NO_VERIFY=1` required for fetch/push.
- Tool timeout 30 s < orchestrator run ~30 s => detached launch with stdout redirected
  **and** `< /dev/null`, then poll `ps` + the log.
- Mock teardown by **PID captured from `ps`** (exact-argv match, never `pkill -f mock_zai`
  — self-match); **0** remaining procs; `curl` exit **7** = port closed.

---

## Session 224 (2026-10-25) — THE RUNBOOK'S SEED FORMULA IS WRONG

The RUNBOOK algorithm block says:

```
seed = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]   # two 2-char slices
```

Re-derived against the session-223 ledger, that reproduces only **727/960** rows.
The correct form is a **single 4-hex slice**:

```
seed = h[(i*2)%8:(i*2)%8+4]                                  # 960/960
```

The two forms agree whenever `i*2 + 4 <= 8` (i.e. `i` in {0,1,2}) and diverge only when
the slice wraps at `i == 3` — which is why a 4-message sample can hide the defect. The
differentiated field is exactly the one that depends on the index, the same failure shape
as the session-213 `int(h[0],16) % 4` vs `d[0] % 4` trap.

**Rule: a stale spec in the RUNBOOK must be re-derived against the LEDGER, not trusted.**
The RUNBOOK is the right place to look for the algorithm, but it is a *record of past
sessions*, and one of its fields is now wrong. The pre-flight gate caught this only because
the "40/40 recomputed md5" check recomputes from a **freshly re-derived** formula. Had the
gate been written against the RUNBOOK's formula it would have reported 40/40 PASS on a mock
that was wrong for 24 % of rows, and the corruption would have landed in the ledger silently.

Corollary: **a pre-flight that recomputes the spec from the same source as the implementation
proves nothing.** The gate must recompute from the *ledger* (the recorded artifact) and the
*source of truth* (the orchestrator's own prompt template), independently of the mock code.

### Other session-224 confirmations

- **The response-body band is 332-369.** The header is a constant **38** chars, so a
  **298**-char tail gives a constant **336**-char body — in band on the FIRST build.
- **The 972-char corpus** is reconstructible from the ledger's 8 distinct 162-char windows
  (offsets 0, 1, 2, 162, 324, 486, 648, 810); it reproduces **960/960** ledger bodies as
  windows. 24 assignments are self-consistent (the corpus is ambiguous in unobserved
  regions) — any of them reconciles the recorded rows.
- **The body offset is a mock-side request counter, NOT a function of the message.** The
  offset is constant within a run and advances between runs; the seed/color/figure ARE
  message-derived. Do not try to derive the body from the prompt.
- **The BATCH phase picks a RANDOM prompt per sim** (`random.choice(prompts)`), so a
  `(civ, prompt)` pair appears **1-4 times**, not exactly twice. Only the COMPETITION phase
  contributes exactly one row per `(civ, prompt)`. A check asserting "exactly 2x" is a
  CHECK bug, not a data defect.
- `civ-grounded` held the lifetime low for the **92nd** consecutive session (relevance
  1958.87, per_sim 1.160, win_rate 0.089 = 3rd-best in the fleet). The run low rotated to
  `civ-therapist` (avg 1.1227, fleet-low quality 0.2040 AND fleet-low alignment 0.8640).
  Chooser/argmax agreement **0/5 (0 %) — 5 down-grades, 0 up-grades**. The axis gap
  (alignment 1.3910 vs quality 0.5870 = 2.37x) says **voice** failure, not prose failure.
  *The holder rotates; the axis does not.*
- **The NAS can be at 100 % with ZERO bytes free while small writes still succeed.**
  A 9 KB `cp` fails with `Disk quota exceeded` and leaves a **0-byte** file that still
  appears in `ls`; a 2-byte write succeeds. Do not trust `ls` for size — always `wc -c`.
  When the NAS is full, the durable copy is **git**, and the file can be delivered via its
  `raw.githubusercontent.com` URL (verify by md5 against the local copy).

---

## Session 227 (2026-10-25) — the `i` INDEX is computed on the DIGEST BYTE, and the ledger only shows 162 chars of the tail

**Run clean (session 227).** per-civ delta = **+10** x 8 = **80 new rows**, `meta_log` D = **+5**
(868 -> 873), `Winner:` lines = **5**, **80/80** rows `provider=zai` with the `[mock-zai`
prefix, **0** JEV `error` keys, **0** 2.0/2.0/2.0 fallback triples, **80/80** rows match an
independently recomputed seed+color+figure, **40/40** distinct seeds, **0**
`(civ,prompt)` combos carrying >1 seed, per-prompt **8/8** distinct seeds AND previews on
all 5 prompts (ts-sorted last-8), relevance delta == sum(`avg_score`) **8/8 exact** (max
residual **4.42e-13**), wins/losses vs `meta_log.winner_civ` **8/8 exact**, `simulations_run`
**+10** on all 8, `generation` unchanged, leaderboard 8 entries sorted desc, git tree **18
modified**. **Pre-flight PASS on the FIRST build.** **20/20 run-wide assertions PASS.**

### 1. THE INDEX IS `d[0] % 4` ON THE **DIGEST BYTE** — THE HEX-CHAR FORM IS A 65 % LOSS

Re-derived against the 1200 current-format ledger rows:

```
d      = md5(user_message).digest()
h      = d.hex()
i      = d[0] % 4                              # DIGEST BYTE, not int(h[0],16)
seed   = h[(i*2)%8 : (i*2)%8+4]                # CONTIGUOUS 4-hex slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

| index form | ledger rows reproduced |
|---|---|
| `d[0] % 4` (digest byte) | **1200 / 1200** |
| `int(h[0],16) % 4` (hex char) | **416 / 1200** |

`d[0]` is the *first raw byte* of the digest; `int(h[0],16)` is the *high nibble* of that
same byte. They coincide only when the byte's high nibble equals the byte itself — i.e. for
bytes in `0x00-0x0F`, which is **1/16** of the space, and even then only for some of them.
The two forms agree often enough that a small sample will land on an agreeing row and hide
the defect. This is the **session-213 trap recurring one level up**: session 213 caught
`int(h[0],16) % 4` vs `d[0] % 4` in a different field, and the ambiguity survived in the
RUNBOOK text long enough to be re-derived wrongly again here.

*Rule: when the spec says "the first byte", compute it from `digest()` and not from
`hexdigest()`. Hex is a *rendering*; a byte index is an arithmetic operation on the digest.
Derive the index form by **fitting against the ledger**, not by reading the prose.*

### 2. THE LEDGER EXPOSES ONLY **162** CHARS OF THE TAIL — THE REST IS NOT RECOVERABLE

`content_preview` truncates at **200** chars and the header is a constant **38**, so the
visible portion of the body is 38 + 162 = 200. The real body band is **332-369**, meaning
**132-169 chars of the tail are invisible in the ledger**. The ledger therefore contains
**9 distinct 162-char tail prefixes** (one per mock configuration), not the tails themselves.

Consequences:
- Do not try to reconstruct the tail from the ledger — the information is not there.
- Do not treat a visible 162-char prefix as the whole tail when computing a body length.
- Build the continuation yourself and land `38 + len(tail)` in the band. This session: the
  session-226 Control B prefix (162 chars, byte-for-byte) + a **136**-char continuation =
  298-char tail = **336**-char body, in band on the **FIRST build**, no trimming iteration.

*Rule: `content_preview` is a **prefix**, not the body. Every length assertion about the
body has to be made on the mock side, and the visible prefix is the only part the ledger
can corroborate.*

### 3. THE "SIX DISTINCT TAILS" CLAIM IS ARTIFACT-ONLY, AND THE COUNT GROWS WITH THE LEDGER

The ledger currently holds **9** distinct 162-char tail prefixes (320 / 174 / 173 / 94 / 93 /
93 / 93 / 80 / 80 rows). The older session-218 note said "exactly 3 distinct 163-char tails"
— that count was a property of *that session's* ledger, not of the format. Tail prefixes
accumulate as mock configurations change across sessions, and the **current-generation
session tail is simply the most recent one** (the Control B text, 80 rows).

*Rule: a "there are N distinct tails" claim is scoped to the ledger, and N grows. Anchor
on the **newest** run-scoped tail instead of a fleet-wide distinct count.*

### 4. OTHER RE-CONFIRMATIONS

- NAS EDQUOT **total** — the clone must land on the overlay (`/tmp`, ~28 G free) and be
  bridged by symlink to `/workspace/repos/ai-writings/cellular-first-design`, targeting the
  **nested** `cellular-first-design` dir. The script's hard-coded `CIVS_DIR` resolves against
  the **clone root**, so a bridge to the inner `code` dir yields `code/code/civilizations`.
  Verify with `os.path.samefile()` (dev:ino **129:3680** both sides this session).
- z.ai **401 `token expired or incorrect`** — **91st session** (credential gap, endpoint
  healthy). JEV live: empty-questions probe returns **422 `too_short`**, which proves the
  token was accepted. `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` =
  placeholder **and** `ZAI_URL_OVERRIDE` set.
- `gh` **not installed**; `ai-writings/cellular-first-design` slug 404s. Upstream is
  `SuperInstance/AI-Writings`. Located the file with
  `GET /search/code?q=civilization_orchestrator+in:path` — survives core-quota exhaustion.
- Mock teardown by **PID captured from `ps`** (345 wrapper + 347 server), then proved the
  port closed (`curl` exit 7, `HTTP=000`). Never `pkill -f mock_zai` (self-match).
- **Run low — `civ-mythic`** (avg 0.5043; fleet-low novelty 1.4130 AND fleet-low alignment
  0.0330; quality 0.0670 is 2nd-lowest). Alignment spread 2.2700 = **5.58x** quality and
  **6.12x** novelty ⇒ *voice* failure. Gap to next civ 0.0653 = **6.4 %** of the run spread.
  **Lifetime low — `civ-grounded`** (relevance 1992.70, rel/sim 1.159, win_rate 0.087 =
  3rd-best) for the **91st** consecutive session; **200.3x** the −10 extinction floor.
  No extinction, no birth (non-loop run).
- **Chooser/argmax agreement 3/5 (60 %)**, 2 down-grades, 0 up-grades; both disagreements
  took the **lower**-scoring candidate. The series (211-227) reads
  0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 / 100 / 60 %.
- **A 60 % point is not a trend** — the series contains 0 %, 20 %, 40 %, 60 % and 100 %.
  The up-grade count across the whole series is still **0**.
