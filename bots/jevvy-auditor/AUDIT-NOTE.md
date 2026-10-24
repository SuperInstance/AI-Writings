# Audit Note — jevvy-auditor, 2026-10-24T13:09:38Z

**Verdict: FAIL (bot-reported, run 7 of 7). I do not concur as a finding about the canon — this
is the seventh consecutive FAIL with the identical witness hash `b0b9813e0f2dbb5d`, i.e. one
defect sampled seven times, not seven independent negative findings. The honest count of
independent negative findings about the canon remains zero. The prior note's central conclusion
survives re-derivation; its proposed fix does not, and that is the most important thing to
record here.** Two new defects surfaced this run that the prior note did not catch, and the
prior note's recommended fix (i) — "embed the sampled prose body in every question" — was
tested directly and **does not work**: an arm that embedded the canon text into every question
returned alignment 0.14 against the bot's 0.15, i.e. no change at all, because the text the bot
slices is *frontmatter metadata, not prose*. The defect is upstream of question placement.

**Root cause, established by controlled A/B against the same endpoint.** The bot's q0 text is
`canon_summary[:150]`, and I verified that slice resolves to
`'witness_log_as_prediction_rsi_gan: # Witness Log As Prediction -- RSI GAN V2 Winner\n\n*Topic:
witness_log_as_prediction*\n*Provider: zai ; what_just_hap'` — 150 characters of title and
metadata tags. At a fixed 150-character budget on the same file, the same question, the same
endpoint: **metadata-and-title 0.63–0.66, pure prose 1.55–1.74**; extending to 600 characters of
pure prose reaches **2.61–2.63**, against this file's own recorded frontmatter score of
`q=2.17`. The model is being asked to grade a YAML-ish metadata header and answering honestly.
`pick_recent_canon()` keeps 200 chars per file, `build_audit_questions()` keeps 100 per file, and
`canon_summary[:150]` is consumed almost entirely by the first file, so files 2 and 3 are
truncated away entirely — a 3-file sample is graded as a 1-file metadata header. The alignment
question confirms it: **with the prose body 2.09, without it 0.18 (11.6x)**; the bot's reported
0.14 is the no-text control, i.e. the bot graded a canon it never showed the model. The
corpus's own frontmatter scores across 46 files (median alignment **3.39**, p90 3.72, max 3.94;
quality median 2.16, novelty median 2.37) sit roughly 23x above the bot's 0.14, and two of the
three sampled files (`witness_log_as_prediction_rsi_gan`, `what_just_happened_bus_aware`) carry
their own recorded scores `q=2.17 a=3.26` and `q=2.15 a=3.39` — so the sampled work is well
above the floor the bot reports, and the third file (`wesleys-sunday-afternoon-dream`) carries no
frontmatter score and is simply graded blind.

**Two new defects, both reproduced this run.** (a) **The credential lookup is outside the
`try` block**: `jev_batch()` reads `os.environ['TYPESAFEAI_KEY']` in the `Request(...)`
construction, which precedes the `try`, so a missing key raises `KeyError` that the
`except Exception` never catches — the script dies with a traceback and **exit 1**, and because
the exception escapes before `load_audit_log()`, **no audit entry is appended**: the log still
showed exactly 6 audits after the crashed run, so the log looks complete while the run failed.
The sandbox provides `TYPESAFE_AI_TOKEN`; the bot wants `TYPESAFEAI_KEY`. This is a naming
mismatch, and it is the *first* thing any operator hits — running the documented command
`python3 jevvy_audit.py --once` verbatim fails before JEV is ever contacted. (b) A JEV outage
prints `[JEVVY] JEV failed: ...` and **still exits 0** (reproduced by pointing the same shipped
code at a dead host: stdout shows the failure, exit code 0), so a scheduled runner records an
outage as a healthy run, and an outage is silently *not* appended to `audit-log.json`.

**The PASS gate is unreachable, and this is structural, not a calibration nit.** The rule
requires `avg(quality, novelty, alignment) >= 3.5` on a 0-4 scale plus `noul > 0.7`. Across all
46 frontmatter-scored corpus files the best achievable average is **3.02**
(`bruno_view_bus_aware.md`, q=2.50 n=2.61 a=3.94), the corpus median is 2.62 and the p90 is
2.82 — so **no sampled canon can satisfy the gate even with truncation fully fixed**: my
fixed-text arm reached avg 1.833, still FAIL. A gate that the best work in the corpus cannot
pass is a gate that reports FAIL forever, and the seven identical-hash runs are the observable
consequence. Note also that the prior note's "PASS needs avg >= 3.5" reasoning survives, but its
claimed mechanism for the low scores (missing text in five of six questions) was the wrong
diagnosis: putting the *metadata* text into those five questions changes nothing, which is
exactly what my A/B showed.

**Fix, in dependency order.** (i) **Strip frontmatter and metadata before sampling** — take
prose body only, and give the model a real body (>= 600 chars per file), not a 150-char slice
dominated by `*Provider:*` tags; this is the change that actually moves the numbers, and it
must land *before* (ii) or (ii) will be calibrated against garbage. (ii) **Recalibrate the PASS
threshold against the corpus's actual score distribution** (median 2.62, p90 2.82, max 3.02)
rather than an absolute 3.5, and add a "tightly-aligned" tier the corpus can actually reach;
otherwise the bot can only ever say FAIL. (iii) **Move the credential lookup inside the `try`**
or read the token with a fallback across `TYPESAFEAI_KEY` / `TYPESAFE_AI_TOKEN`, and **exit
non-zero plus append a failure record** so a crashed or outage run is visible in the log rather
than absent from it. (iv) **Embed the canon in every question** — still worth doing, but treat
it as necessary, not sufficient, since my A/B shows it alone changes nothing. (v) Treat empty
canon as a hard error rather than auditing the literal string `"empty canon: no content yet"`,
and **do not count identical witness hashes as independent findings** — the log's own hash field
would have flagged this seven runs ago.

Until (i) and (ii) land, **this bot's FAIL must not be read as evidence about the canon, and
the seven consecutive FAILs must not be counted as seven independent negative findings.**

Confidence: high — the 0.63-vs-1.74 metadata/prose contrast at fixed 150-character budget, the
2.09-vs-0.18 alignment contrast, and the 0.14-vs-0.15 no-effect A/B are controlled
same-endpoint measurements on the exact file and exact question text the bot used; the corpus
distribution is read from 46 independent frontmatter score sets; the `KeyError` and
exit-0-on-outage behaviours are direct reproductions of the shipped code, and the log-entry
count (6 before and after the crashed run) is the receipt for the silent-append-loss defect.
