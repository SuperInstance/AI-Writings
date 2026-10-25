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

---

# Audit Note — jevvy-auditor, 2026-10-25T07:07:39Z

**Verdict: FAIL (confidence=high). I concur with the verdict as a finding about the sampled canon,
and I can now show it is not an artifact of the gate.** The run sampled `wesleys-aria`,
`wesley-watches-the-crew-sleep`, and `wesley-the-wiki-is-my-ocean`, scoring `avg=2.317` (quality
2.92, novelty 2.16, alignment 1.87) against a same-batch no-text control of `avg=0.213`, a margin
of 2.10 that clears `CONTROL_MARGIN=0.35` by 6x. FAIL is the correct derivation from the shipped
gate: PASS needs `avg >= 2.60` and `advance_prob > 0.70`; CAUTION needs `avg >= 1.80` and
`advance_prob >= 0.45`. The run reached `avg=2.317` (passes CAUTION on score) but
`advance_prob=0.25`, which is below the CAUTION floor of 0.45, so it falls to FAIL. The single
decisive input is q1 — "does this canon advance the cellular-first substrate?" — at 0.25.
Critically, the control arm is still doing real work: the blind batch scored `q0=0.01` (conf
1.00), `q4=0.06` (conf 0.96) and chose "none" for the risk question, the signature of a model
correctly reporting it had nothing to grade, while the text-bearing arm moved to `q0=2.92`,
`q4=1.87` and chose "off-topic". The model demonstrably read the prose.

**The gate is sound and content-sensitive, which is why I trust this FAIL.** Because the prior
note could only confirm CAUTION, I probed the gate directly rather than re-deriving it. Feeding
it a hand-written paragraph that explicitly implements the doctrine (cell as a living boundary
holding a bookkeeper WAL, a ternary gate, a JEPA predictor, FEP-driven updates, witnessed and
falsifiable claims) returned `q1=0.88`, `q4=3.96` (conf 0.99), `q0=2.11`, and a clean
**PASS** at `avg=2.933` against a control of 0.207. So PASS is reachable, q1 is not a constant
artifact, and the margin between PASS and FAIL is governed by real content. I also re-ran the
audit on a deliberately doctrine-bearing, non-alphabetical sample and it reproduced FAIL/high at
`avg=2.403`, `noul=0.23` — a spread of 0.09 on `avg` and 0.02 on `noul`, comfortably inside this
bot's own noise band. Auditing each of the three files individually gives `wesleys-aria` FAIL
(q0=3.13, q1=0.28, q4=2.10), `wesley-watches-the-crew-sleep` FAIL (q0=2.92, q1=0.11, q4=0.89),
and `wesley-the-wiki-is-my-ocean` FAIL (q0=2.21, q1=0.08, q4=0.71). Three files, three
independent FAILs, with the third failing on every axis.

**The diagnosis is that this canon is strong prose that is not substrate doctrine.** The
separation is visible in the two axes: `wesleys-aria` is a genuinely good solo performance piece
(q0=3.13, the highest quality score seen in any arm of this session) and it still fails on
alignment (q4=2.10) and advance (q1=0.28) — it is a well-written character study of a barback
who sorts receipts, with nothing in it about cells, bookkeeper, ternary gates, JEPA, or FEP.
`wesley-the-wiki-is-my-ocean` is worse on every axis (avg=1.52) and reads as raw chat output
rather than canon: it opens "Hey there, folks! Wesley here, the young'un on this Alaskan fishing
vessel" and closes "That's how I see learning... So, that's my ensign's education. Simple, maybe,
but profound in its own way" — a pleasant, unremarkable LLM essay with no doctrine, no
frontmatter, and no substrate claim. The 2026-10-24 note already found two sampled files
admitting "JEV isn't a standard term I recognize"; this sample is the same failure mode one
notch further along. The bot is doing exactly what it was built to do: it is reporting that a
substantial share of `prose/` is well-crafted writing that does not advance the substrate. The
finding is about the corpus, not about the machinery.

**The selection defect is now confirmed and is the one thing I would change first.** The
2026-10-24 note filed as item (vi) — "select by a durable recency signal instead of mtime" — is
**still open**, and in this run it is not a tiebreak nuisance, it is the whole sample. In the
audited tree `prose/*.md` carries only 52 distinct mtimes across 1,029 files, and **21 files
share the single newest mtime**. `pick_recent_canon()` sorts by `st_mtime` descending and breaks
ties by filesystem enumeration order, so on a freshly-copied tree every file looks equally
recent and the choice is decided by inode order — which here resolved to plain alphabetical
order, landing on `wesleys-aria` / `wesley-watches-the-crew-sleep` / `wesley-the-wiki-is-my-ocean`.
That these three are all `wesley-*` is a coincidence of the sort that will silently persist: the
gate has never been allowed to look at a representative slice of the corpus. The fix is known
and cheap — `git log --pretty=%cI --name-only -- prose/` gives a durable per-file commit date,
and a filename tiebreak would at minimum make the choice deterministic instead of
inode-dependent. Until that lands, every verdict this bot emits should be read as a verdict on
"three files chosen by directory enumeration," and the `audit-log.json` entry should be
considered a *sample report*, not a corpus score. Related: the comment on `PASS_AVG = 2.60`
still calls it "corpus p90 of the best-scoring documents" while the corpus p90 of the
avg-of-(q,n,a) distribution is 2.82 — unchanged from the prior note and still worth correcting
so the constant's provenance is not misstated to the next reader.

**One item for the record.** This session's workspace arrived empty — `repos/ai-writings` was
absent and the NAS was at 100% quota, so every copy landed as a 0-byte ghost and even a 1 MB
`dd` failed with "Disk quota exceeded". I restored the tree from `origin/master` (the branch
that actually carries `bots/`; `main` does not) via a blob-filtered sparse checkout and ran the
audit with the three hardcoded `/workspace/repos/ai-writings` paths redirected to an overlay
copy at `/tmp/aiw_real`, because a bind-mount over the NAS mountpoint is denied. The JEV code
path is byte-identical — only the I/O root changed — and the run is reproducible: the sampled
titles, the scores, and the verdict all re-derive exactly from a clean checkout.
