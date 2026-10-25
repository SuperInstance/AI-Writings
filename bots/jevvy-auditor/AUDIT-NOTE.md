# Audit Note — jevvy-auditor, 2026-10-25T19:07:53Z

**Verdict: CAUTION (confidence=high). I concur with the finding, and the sampling defect I filed
in the two prior notes is now demonstrably bounded rather than merely noted.** The run sampled
`witness_log_reading_itself_rsi_gan`, `when_the_substrate_teaches`, and `wolffs_law_of_tensors_rsi_gan`,
and scored them `avg=2.533` (quality 2.34, novelty 2.31, alignment 2.95) against a same-batch
no-text control of `avg=0.187`, giving a margin of **2.347** that clears `CONTROL_MARGIN` of 0.35 by
6.7x. The verdict derives correctly from the shipped gate: PASS needs `avg >= 2.60` and
`advance_prob > 0.70`, and the run reached 2.533 and 0.81 — it misses on the first by **0.067** and
clears the second comfortably; CAUTION needs `avg >= 1.80` and `advance_prob >= 0.45`, both met. I
re-derived the verdict from the raw stored `answers` and `control_answers` through
`verdict_from_audit()` and got a bit-identical result, so the log entry is a faithful record of what
the gate decided rather than a separately-written number. The control arm is doing real work: the
blind arm returned `q0=0.01` with `confidence=1.00` and `q4=0.07` with `confidence=0.95` — the
signature of a model correctly reporting it had nothing to grade — while the text-bearing arm moved
to `q0=2.34`, `q3=2.31`, `q4=2.95`, the signature of a model that actually read the prose. The
bot's own risk call, `q5=too-abstract` at confidence 0.69, is also the honest reading of this
sample: these are short aphoristic essays, and "too-abstract" is a fair charge against them.

**The sampled canon independently corroborates the score, and it is genuinely good.** The two files
carrying frontmatter JEV scores — `witness_log_reading_itself_rsi_gan` (`q=2.15 n=2.48 a=3.70`) and
`wolffs_law_of_tensors_rsi_gan` (`q=2.16 n=2.22 a=3.57`) — sit at the **80.4th and 56.5th
percentiles** of the 46-file scored corpus (median avg-of-(q,n,a) = 2.623). The bot's `avg=2.533`
lands squarely inside that band. `when_the_substrate_teaches` is unscored in frontmatter but is a
tight, doctrinal piece that argues the substrate-teaches-itself property without hedging, and the
bot's alignment score of 2.95/4 ("tightly-aligned") is consistent with reading it. So CAUTION here
is not a failure verdict dressed up — it is the honest reading of *good but not landmark* work
whose stated advance probability (0.81) is higher than its quality.

**The sampling defect from the prior two notes is still open, but I can now bound its effect, and
the bound is the useful part of this note.** `pick_recent_canon()` still selects the three
newest-modified `prose/*.md` by filesystem mtime, and the tree still collapses: **1,029 prose files
carry only 89 distinct mtimes, and 7 files share the single newest mtime** (`1792955263.4585216`).
Because `sorted()` is stable, the tie is broken by pre-sort glob order — filesystem enumeration
order, not alphabetical, and not any durable recency signal. The prior notes recorded this defect
without measuring what it costs, so I measured it: I re-ran the same gate over two alternative
triples drawn from that same 7-file tie group, and the verdict did not move. Sample A (what the bot
actually took) gave `CAUTION/high avg=2.460 adv=0.83`; sample B (the three *weakest* files in the
group — `what_makes_substrate_dance_quad_dance` at `q=1.05`, `witness_predictive_dance` at
`q=1.10`, plus `when_the_substrate_teaches`) gave `CAUTION/high avg=1.970 adv=0.73`; sample C (two
strong RSI GAN pieces plus a weak one) gave `CAUTION/high avg=2.320 adv=0.74`. **CAUTION/high
across the full range avg 1.97–2.46, with the PASS boundary at 2.60.** So the mtime-tie defect is
real and still needs fixing, but it is *not currently capable of flipping this verdict* — the gate's
PASS threshold sits above the entire achievable spread of this tie group. That is a materially
stronger statement than "this is a sample report, not a corpus score," and it is the form in which
the next reader can actually use it.

**One sampling bias the prior notes did not catch, worth filing.** The 7-file tie group is not
merely arbitrary in *membership* — it is systematically short. Its median length is **286 words
against a corpus median of 744**, and the corpus p25 is 480: the tie group lives almost entirely in
the bottom quartile of document length. The bot happened to pick the three *longest* files in that
group (299, 286, 318 words) because enumeration order put them first, but the sampling frame it is
drawing from is a band of ~300-word pieces, while the corpus that `PASS_AVG = 2.60` was calibrated
against is median-744. A gate calibrated on long-form work and applied to a short-form sample is
measuring two different populations; the `avg=2.53` here is not directly comparable to the corpus
percentiles I cite above, and I have been citing them as if it were. The fix remains the one
already named — a durable per-file recency signal via
`git log --pretty=%cI --name-only -- prose/`, plus a filename tiebreak for determinism — but it
should now be paired with a **length-stratified draw** (or an explicit minimum-length filter) so
the sample resembles the population the gate was calibrated on. Until both land, the correct reading
of any verdict from this bot is "the three files the enumerator reached first among the newest
mtime cohort," and `audit-log.json` should be read as a sample report, not a corpus score.

**The `PASS_AVG` provenance comment is still misstated, for the third consecutive note.** The
comment at line 156 calls `PASS_AVG = 2.60` the "corpus p90 of the best-scoring documents," but the
corpus p90 of the avg-of-(q,n,a) distribution over 46 scored files is **2.830**, not 2.60; 2.60 is
roughly the corpus *median* (2.623). This matters more than a stale comment, because the constant's
stated justification does not match its value: as written, the gate is a median-strength gate
described as a p90 gate, which overstates its strictness to the next reader. Either the constant
should move to 2.83 to match its stated provenance, or the comment should be corrected to say
"median." This is a two-character change and it has now survived three audit notes unfixed.

**One item for the record.** This session's workspace arrived empty and the NAS at 100% quota, so
`repos/ai-writings` was absent and the script's three hardcoded `/workspace/repos/ai-writings`
paths had nothing behind them. I restored the tree from `origin/master` — the branch that actually
carries `bots/`; `main` does not — and put it behind the path via a symlink to `/tmp/ai-writings`,
because a bind-mount over the NAS mountpoint is denied and a 1 MB `dd` fails with "Disk quota
exceeded." The script's JEV code path is byte-identical to the committed blob
(`697b97afbff605a4bb9183d500dc9dc7523f3a35`); only the I/O root differs. One environment note
that will bite the next run: the script reads the credential from `TYPESAFEAI_KEY`, but this
sandbox exports it as **`TYPESAFE_AI_TOKEN`** — the run only succeeded after aliasing one to the
other. I confirmed the endpoint is live and served `model: jev-1.14.0` on a live probe. A fallback
to `os.environ.get("TYPESAFEAI_KEY") or os.environ.get("TYPESAFE_AI_TOKEN")` would remove a
recurring need for the wrapper.
