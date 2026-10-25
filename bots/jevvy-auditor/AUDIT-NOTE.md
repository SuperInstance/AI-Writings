# Audit Note — jevvy-auditor, 2026-10-25T01:17:59Z

**Verdict: CAUTION (confidence=high). I concur as a finding about the canon, with one caveat about
the sampling.** The run sampled three canon files — `the_moment_of_dance_rsi_gan`,
`cross_instance_sync_dance`, `jev_picks_each_moment_quad_dance` — and scored them
`avg=2.13` (quality 2.29, novelty 2.38, alignment 1.71) against a same-batch no-text control of
`avg=0.19`, giving a margin of 1.96 that clears the `CONTROL_MARGIN` of 0.35 by 5.6x. The verdict
is derived correctly from the shipped gate: PASS needs `avg >= 2.60` and `advance_prob > 0.70`
(the run reached 2.13 and 0.68, missing on both), and CAUTION needs `avg >= 1.80` and
`advance_prob >= 0.45` (both met). A second independent run in the same session reproduced
CAUTION/high at `avg=2.127`, `advance_prob=0.68` — a spread of 0.02, well inside this bot's own
noise band. The control arm is doing real work rather than rubber-stamping: the blind arm scored
`q0=0.01, q3=0.48, q4=0.08` with confidence 1.00 on q0, which is the signature of a model
correctly reporting that it had nothing to grade, and the text-bearing arm moving to
`q0=2.29, q3=2.38, q4=1.71` is the signature of a model that actually read the prose.

**The three sampled files are independently corroborated as weak.** Two of them carry their own
frontmatter JEV scores of `q=0.12, a=1.57` and `q=0.15, a=0.20`, and both open by admitting
they do not recognize "JEV" as a term — `cross_instance_sync_dance` says "JEV isn't a standard
term I recognize, so I'll interpret it as...", `jev_picks_each_moment_quad_dance` says "Let me
know if you meant something else!" — which is what a model guessing at an unfamiliar brief
produces. The third, `the_moment_of_dance_rsi_gan`, is genuinely strong (`q=2.43, a=3.47`) and
carries the run on its own. The sample's mean frontmatter `q` of 0.90 sits below the corpus
median of 2.08, with only 7 of 61 scored corpus files beneath it. So CAUTION is the honest
reading: one good document and two misfires, averaged into "mediocre."

**The caveat is the sample, not the verdict.** `pick_recent_canon()` selects the three
newest-modified `prose/*.md` by filesystem mtime, and **15 files share the identical mtime
`1789969013.000000000`**, so the selection among them is decided by filesystem enumeration order
rather than recency. The same three files were picked across both of my runs only because the
inodes did not move; on a different filesystem, or after any operation that rewrites the
`prose/` tree, a different three of those 15 would be graded, and the verdict could move with
them. This is the same class of defect the 2026-10-24 note filed as item (vi) — "select by a
durable recency signal instead of mtime" — and it is **still open**: the fix landed for the
*embedding* and the *gate*, but not for the *selection*. The `git log`-derived per-file commit
date is available and cheap (one `git log --pretty=%cI --name-only -- prose/`), and a secondary
tiebreak on filename would at least make the choice deterministic rather than inode-dependent.

**Two smaller items.** (i) The code comment on `PASS_AVG = 2.60` calls it "corpus p90 of the
best-scoring documents", but the corpus p90 of the avg-of-(q,n,a) distribution is **2.82** and the
median is **2.56** — the value is *more* permissive than the comment claims, not less, so the gate
is reachable and this is a labelling error, not a miscalibration; the comment should say "just
above the corpus median (2.56)". (ii) `witness()` now includes a `seq` field, but the counter is
a module-level list reset by every process, so each run restarts at 1 — the log shows `seq=1,
seq=2` repeating for every invocation. The counter is therefore per-process, not a monotonic
sequence across the log's history, and cannot detect a replayed or reordered entry the way the
2026-10-24 note intended. Making it durable (derive it from the existing line count of
`witness.log` at append time) would restore the property the field is supposed to provide.

**What to improve, in priority order.** (i) **Make canon selection deterministic and durably
recency-ordered** — use the git commit date of each `prose/*.md` as the primary key, with the
filename as a stable secondary tiebreak, so that a verdict is reproducible from the repository
state rather than from inode order; the current tie across 15 files is the single largest
remaining threat to the verdict's meaning. (ii) **Report the sample's identity and its
dispersion in the verdict** — record the frontmatter `q/n/a` of each sampled file alongside the
bot's own scores, so a reader can see immediately that the sample was 0.12/0.15/2.43 and judge
whether CAUTION describes the corpus or the draw; the bot's `avg` of 2.13 sits at the **23rd
percentile** of the corpus avg distribution (median 2.56, p90 2.82, max 3.02), which is a
statement about the draw and not about the work. (iii) **Fix the `PASS_AVG` comment** to name
the statistic it actually is, so the next recalibration is not anchored to a wrong number.
(iv) **Make the witness `seq` durable** by seeding it from the line count of `witness.log` at
append time, so it is monotonic across the whole log rather than per-process. The seven fixes
recommended in the 2026-10-24 note are otherwise all landed and independently re-verified in this
session — canon embedded in all six questions (fix i), the no-text control arm gating confidence
(fix ii), a reachable recalibrated gate (fix iii), non-zero exit plus an `ERROR` log record on a
JEV outage (fix iv), empty canon as a hard error (fix v), the witness hash covering the
timestamp (fix vii) — and fix (vi), durable recency, is the one that did not land.

Confidence: high on the verdict's internal consistency (every gate branch re-derived from the
shipped constants, the control arm reproduced live, two independent runs agreeing to 0.02, and
the sample's weakness corroborated by independent frontmatter scores and by the documents' own
admissions of unfamiliarity with the brief); high on the sampling defect (15 files verified to
share one mtime, with the tiebreak traced to enumeration order); and moderate on the corpus
percentiles, which are computed over the 61 of 1029 canon files that carry frontmatter JEV
scores and therefore describe a self-selected subset rather than the full corpus.

---
*Run: `python3 jevvy_audit.py --once` at 2026-10-25T01:17:59Z. Sample:
`the_moment_of_dance_rsi_gan`, `cross_instance_sync_dance`, `jev_picks_each_moment_quad_dance`.
Result: `verdict=CAUTION`, `verdict_confidence=high`, `score_avg=2.1267`, `control_avg=0.1867`,
`advance_prob=0.68`. Verified in `bots/jevvy-auditor/audit-log.json` (entry 9 of 9) and
`bots/jevvy-auditor/witness.log`.*
