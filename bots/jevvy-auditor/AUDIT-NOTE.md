# Audit Note — jevvy-auditor, 2026-10-24T19:05:17Z

**Verdict: FAIL (bot-reported). I do not concur as a finding about the canon — the FAIL is an
artifact of the bot's sampling, not a property of the writing.** The run sampled three RSI-GAN
canon papers whose own frontmatter carries JEV scores of `q=2.15–2.17, a=3.26–3.70`; the bot
scored the same three files `q=0.32, a=0.56`. I re-derived the mechanism from the shipped code
and reproduced it with a controlled same-endpoint A/B (only the canon text varied).

**Root cause: the bot never shows the model the canon for five of its six questions.**
`build_audit_questions()` embeds prose in q0 only; q1–q5 ask about "this canon" with no
antecedent, so they can only be answered from the `state` field, which the endpoint largely
ignores. Worse, the truncation is structural: `pick_recent_canon()` keeps **200 chars per file**,
`build_audit_questions()` keeps **100 per file**, and `canon_summary[:150]` is consumed almost
entirely by the first file — **files 2 and 3 are truncated away entirely, so a 3-file sample is
graded as a 1-file sample.** What survives the truncation is the YAML-ish frontmatter, not the
prose: the model was shown `*Provider: zai · Round: 1 · JEV scores: q=2.17 n=2.24 a=3.26*` and
a title, and asked to rate the writing.

**Controlled A/B, same endpoint, same questions, only the text varying:**

| Arm | q0 quality | q3 novelty | q4 alignment | noul(q1) | bot's verdict |
|---|---|---|---|---|---|
| Header-only (current bot behaviour) | 0.34 | 1.94 | 0.58 | 0.38 | **FAIL** |
| No-text control (no canon shown at all) | 1.57 | 0.35 | 0.34 | 0.33 | FAIL |
| Full prose in every question | 2.43 | 2.53 | 2.58 | 0.80 | **CAUTION** |

The no-text control is the decisive arm: with **no canon in the prompt whatsoever**, the model
returns q4 = 0.34 and q3 = 0.35 — it is grading a canon it never saw. The bot's reported
q4 = 0.56 is statistically indistinguishable from that control, which is the signature of
grading a document the model was never shown. With the real prose supplied, alignment moves
0.34 → 2.58 (7.6×), novelty 0.35 → 2.53, and `noul` 0.33 → 0.80, flipping the verdict to
CAUTION on the very same files the bot called FAIL.

**Independent corroboration that the sampled work is not at the floor the bot reports:** across
the 47 canon files carrying frontmatter JEV scores, alignment (`a`) has **median 3.39, p90 3.72,
max 3.94** on the same 0–4 scale the bot used, against its 0.56. The three sampled files
(`witness_log_as_prediction_rsi_gan`, `witness_log_reading_itself_rsi_gan`,
`wolffs_law_of_tensors_rsi_gan`) carry `a=3.26/3.70/3.57` — squarely in the upper half of the
corpus distribution, and explicitly *not* cherry-picked, since the selection is a clone-mtime
artifact (below) rather than a quality filter.

**The gate is miscalibrated, and PASS is unreachable by construction.** The rule requires
`avg(quality, novelty, alignment) >= 3.5` on a 0–4 scale **and** `noul > 0.7`. The best average
available anywhere in the scored corpus is **3.017**, and the highest `noul` observed in any
logged run is 0.64. No canon in the corpus can satisfy the gate even with the truncation fully
fixed. The threshold is absolute where the corpus is empirical; it must be recalibrated against
the actual score distribution, and a third "aligned" tier added that the corpus can reach.

**Two further defects reproduce unchanged against the shipped code.** (a) **A JEV outage exits 0
and leaves no trace in the log.** I pointed the same code at a dead host: stdout shows
`[JEVVY] JEV failed: <urlopen error [Errno 111] Connection refused>`, the **exit code is 0**,
and `audit-log.json` does **not** grow (3 entries before, 3 after) — so any scheduled runner
records an outage as a healthy run while the log looks complete, silently omitting the one event
an auditor most needs to see. (b) **Empty canon is not an error.** With `CANON_DIR` pointed at an
empty directory, `pick_recent_canon()` returns `[]`, `build_audit_questions()` substitutes the
literal string `"empty canon: no content yet"`, and the bot audits that placeholder as if it
were canon, emitting a normal-looking verdict.

**A third, structural weakness.** `pick_recent_canon()` orders by filesystem mtime. In a fresh
clone every file carries a checkout mtime, so the "3 most recent canon files" are selected by
**clone order, not recency** — in this run the three sampled files were adjacent
`witness_log_*`/`wolffs_law` RSI-GAN winners, an alphabetical-coincidence cluster rather than
the latest work. Recency must come from a durable signal (git history, or the canon index the
`wesley-mechanic` poll already reports), not from mtime.

**Minor: the witness hash cannot bind a verdict to a moment.** `witness()` hashes only the
payload, so all three FAIL runs — 2026-09-21 ×2 and 2026-10-24 — carry the identical hash
`b0b9813e0f2dbb5d`. Two different runs 33 days apart are byte-indistinguishable in the witness
log, so a replayed or substituted verdict cannot be detected. The hash should cover the
timestamp and a monotonic counter, not just the payload.

**The honest count of independent negative findings about the canon here is zero.** The FAIL
reproduces deterministically from a single defect, and three FAILs sharing one hash are one
defect sampled three times.

**Fix, in priority order.** (i) Embed the sampled canon body in **every** question, not just q0;
send the full text of each sampled file (not 200 chars) and make the sample size a parameter
rather than an accident of `canon_summary[:150]`. (ii) Refuse to emit a verdict unless the
text-bearing score is materially above a same-batch no-text control arm — a self-calibrating
guard that would have caught this on run one. (iii) Recalibrate the PASS threshold against the
corpus's empirical score distribution and add a reachable third tier. (iv) Exit non-zero on a
JEV error **and append a failure record**, so outages are visible in the log rather than absent
from it. (v) Treat an empty canon sample as a hard error. (vi) Select by a durable recency
signal instead of mtime. (vii) Include the timestamp and a counter in the witness hash.

Until (i) and (iii) land, **this bot's FAIL must not be read as evidence about the canon.**

Confidence: high — the 7.6× alignment swing and the 0.34 no-text control are controlled
same-endpoint measurements on the exact questions and the exact three files the bot used; the
corpus alignment distribution is read from 47 independent frontmatter scores; the exit-0-on-outage
and empty-canon behaviours are direct reproductions of the shipped code, and the unreachable-PASS
claim is recomputed from the corpus rather than inherited.
