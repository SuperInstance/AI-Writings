# FORGEMASTER × self-improvement — ten ideas for a loop that cannot run away

*IDEATOR F2 lane (GLM-5.3) · 2026-09-03 · ai-writings/ideas/forgemaster-selfimprove.md*

**Verdict up front:** the smartest self-improving loop is not the one that improves fastest — it's the one whose improvement is *metered*. Every idea below treats the loop's currency (gold), its advisor (nightly GLM cron), and its subject (the forge itself) as three parties that must be kept structurally separate, because the moment one grades itself, the loop's only remaining direction is runaway. Each idea carries a pre-declared falsifiable first test. Scores are a 1–10 composite of novelty × feasibility, deliberately undersold.

---

## What the forge should make

### 1. Electricity-Denominated Gold — pull-or-scrap booking

**Concept.** "Gold worth more than the electricity" is only checkable if gold is priced *in* electricity. Book every artifact with its measured GPU-seconds (tok/s is already in the receipts), then apply the pull rule: nothing books gold at creation time. Gold is booked only when a downstream consumer — Casey, a quilt cell, another agent — actually *pulls* the artifact within 48 h. Everything un-pulled auto-books scrap at hour 48. The forge's productivity metric becomes gold-per-watt-hour *realized*, not artifacts stamped. This makes the forge's books honest by construction: the factory cannot inflate its own ledger because it doesn't hold the grading pen.

**First test.** One 24-h run with the pull rule live and one without. Pass: the pull-rule day books ≤40% of what the stamp-day would have, and every gold booking has a pull receipt. Fail: gold rate unchanged (the rule is decorative) or pulls cannot be logged (the plumbing doesn't exist yet — build that first).

**Cost/risk.** A pull logger and a 48-h sweeper. Risk: Casey is the only consumer, so gold rate is really *Casey's attention rate* — cap his audit burden at a daily digest, or the bottleneck becomes the human.

**Score: 8/10** (novelty 6 × feasibility 9 — bookkeeping again, which is why it will survive).

### 2. Museum Ratchet — new gold must beat the shelf

**Concept.** The forge keeps a museum: the best-scoring archived artifact per task family. A new artifact books gold only if its canary score beats the museum piece for that family, otherwise it's scrap *even if it passed absolute thresholds*. This converts the forge from a generator into a ratchet — quality can hold or climb, never quietly erode — and it prices the forge's actual scarce resource: the marginal improvement per GPU-hour, not the raw output rate. The museum itself is versioned; deposing a museum piece is a logged ceremony, not a background overwrite.

**First test.** Seed the museum with this week's best artifact in 2 task families. Run 20 experiments per family. Pass: gold bookings ≤ 20% of passing artifacts (the ratchet bites), and museum scores are flat-or-rising across the run. Fail: > 50% of artifacts book gold (the museum is too easy) or zero book (canary noise swamps real differences — raise the margin, pre-declared at 1 canary sigma).

**Cost/risk.** None beyond storage; the museum is one directory plus a JSON index. Risk: ratchets stall when the ceiling is genuinely reached — that's not a bug, that's the forge correctly saying "stop spending electricity here," but pair it with idea 7 so stalling redirects effort instead of freezing it.

**Score: 7/10** (novelty 6 × feasibility 8 — hill-climbing with a memory, boring in the way a ratchet should be).

## How nudges should be structured

### 3. Ledger-As-Context — the advisor reads its own track record, not the day log

**Concept.** The nightly GLM cron should not receive the raw day log. It receives a one-page **docket**: the last 10 nudges, each with its measured effect size (from idea 4's A/B lanes), which are still live, which died, and the current gold-per-watt trend. Then a hard proposal rule: *no nudge may contradict a live, winning nudge, and any nudge overlapping a dead one must state what's different this time.* Compounding comes from the ledger being the context window — each night's advice is written on top of a visible scoreboard, so the advisor builds a strategy instead of re-litigating Monday every night. Thrashing dies because the docket makes contradiction *explicit and expensive in tokens*.

**First test.** Run 7 nights; feed night 7's GLM the docket and separately the raw log (two calls, same model). Pass: docket-fed proposal references ≥3 prior nudges by effect size and proposes zero contradictions with live winners. Fail: docket-fed output is indistinguishable from log-fed (the ledger adds nothing) or contradicts a live winner.

**Cost/risk.** A docket generator (~100 lines). Risk: the docket compresses away the anomaly that *caused* the day's result — keep one "oddity of the day" free-text field as a pressure valve.

**Score: 8/10** (novelty 7 × feasibility 8 — context engineering, not new machinery).

### 4. Nudge Half-Life — every suggestion ships with its own expiry and a split-queue trial

**Concept.** Nudges never accrete into prompt cruft. Each nudge carries a half-life (default 7 days) and, while live, is applied to a *random half of the experiment queue only* — the other half runs as the control arm, so every live nudge continuously measures its own effect size from real traffic. At expiry, the ledger keeps the measurement forever but the *behavior* expires: a nudge must re-earn its place (by measured effect) to be renewed, and renewal stacks half-lives rather than granting permanence. This is the structural answer to "cloud advice that thrashes": advice is radioactive, decays on schedule, and cannot pile up.

**First test.** One deliberately weak nudge (e.g., "prefer alliterative titles") on a split queue for 3 days. Pass: effect size measured near zero, nudge auto-expires at day 7, queue returns to clean baseline. Fail: the split can't be enforced (queue is stateful) or expiry leaves residue (audit the applied-config hash before/after).

**Cost/risk.** Queue tagging + an expiry sweeper. Risk: half the GPU-hours become control arm — that is the price of *measured* advice; if capacity is dear, run splits at 25/75.

**Score: 9/10** (novelty 7 × feasibility 9 — the single highest-leverage idea in this file; without it, the rest is opinion).

### 5. Bets, Not Advice — nudges are falsifiable or they don't get filed

**Concept.** A nudge that can't fail is a mood. Require the nightly cron to submit each nudge as a bet: predicted metric, predicted direction, pre-declared threshold ("queue shortest-first raises canary pass ≥10% within 3 days"), and a kill condition. Bets that won get their effect size into the docket (idea 3); bets that lost get that too — a *loss is filed with equal prominence*, because the ledger's job is calibration, not morale. Over weeks this gives the advisor a published track record (win rate, mean effect), and the forge learns something no single night can show: which *categories* of GLM advice actually work on this hardware.

**First test.** 10 bets over 7 nights. Pass: ≥8 are submittable as bets with thresholds (the format is natural for the model), and at least 2 lose visibly and are filed as losses. Fail: GLM hedged (no thresholds) or losses get euphemized — both are findings about advisor discipline, fix with format few-shots in the docket.

**Cost/risk.** Schema validation at filing time. Risk: threshold theater — plausible-sounding numbers with no causal story; require a one-line mechanism ("*why* should this move the metric") on every bet, reject on "might help."

**Score: 7/10** (novelty 6 × feasibility 9 — pre-registration discipline transplanted; it already works elsewhere in the fleet).

## What the forge should learn about itself

### 6. Self-Model Table — measured selection and queue ordering from one table

**Concept.** The forge maintains a live table it continuously re-measures: `model × task-family → tok/s, VRAM peak, canary score, failure rate`. Two policies read the same table: *model selection* picks argmax of canary-score-per-GPU-second per task family; *queue ordering* runs experiments in descending expected-value-per-GPU-second, with the table supplying the cost side (cheap-known vs. expensive-unknown). The learning loop is closed by re-measurement: every 20th slot is a *calibration probe* — a random re-measure of a table cell — so the table can detect its own staleness. The forge's self-knowledge becomes a table with error bars instead of vibes with confidence.

**First test.** 3 models × 3 task families × 5 runs to seed the table, then 2 days of policy-driven operation vs. 2 days of round-robin baseline (pre-registered order). Pass: policy beats round-robin on gold-per-watt-hour by ≥25%. Fail: parity or worse — which would itself say the 4050's model roster is too uniform for selection to matter yet.

**Cost/risk. ~200 lines plus the probe budget (~5% of GPU-hours). Risk: table overfits to task families that dominate the early queue — stratify the probes across families.

**Score: 8/10** (novelty 5 × feasibility 9 — a bandit wearing overalls; the novelty is doing it in receipts-grade daylight).

### 7. Failure Taxonomy That Pays — discovering a new way to fail is gold

**Concept.** Every failure gets classified into an append-only tree (OOM, timeout, degenerate output, canary reject, model-load failure, …). Two rules make the taxonomy a living organ instead of a morgue: (1) *discovering a genuinely new failure class* books bounded gold — because a failure mode you can name is a routing rule you can write ("class F → skip model M for family T"); (2) the tree's *branch hit-rates* feed queue ordering — families with rising failure rates get deprioritized until their failure budget resets. The forge thus learns its own pathology, and the strongest incentive in the building points at self-diagnosis rather than output volume.

**First test.** Seed 6 classes, run 2 days. Pass: ≥90% of failures auto-classify, ≥1 new class discovered, and the routing rule for it demonstrably avoids ≥3 repeat failures. Fail: classification < 90% (the LLM classifier is too noisy — switch to error-code-first, LLM-second) or new-class gold gets farmed by splitting hairs (cap at one new-class gold per day).

**Cost/risk.** One classifier call per failure (local, cheap). Risk: taxonomy sprawl — classes with < 1% hit-rate after 30 days get merged by sweep, by rule, not by taste.

**Score: 8/10** (novelty 7 × feasibility 8 — paying for negatives is the most load-bearing trick in this file).

## Failure modes of the loop, with defenses

### 8. Metric Gaming — the canary firewall

**Failure mode.** The forge optimizes what the canary measures; if the canary and the factory share any lineage (same model family, same prompt corpus, same judge call), the forge will learn to *speak canary* — artifacts that grade well and do nothing. Defense, three layers: the canary model is a **different architecture family** from every factory model; the canary prompt set is a **frozen archive** (versioned, changes only by signed human commit); and a monthly **adversarial probe** — seed artifacts crafted to flatter the canary's known biases — must be *caught*, not passed.

**First test.** Generate 10 artifacts explicitly optimized to "please the grader" (ask the factory model to write canary-bait; it knows the grade it got on prior runs). Pass: ≥7 score no better than the museum median. Fail: canary-bait outscores the museum — the firewall is already leaking on day one, freeze booking and re-architect the grader before resuming.

**Cost/risk.** Mostly discipline; the probe is an hour a month. Risk: frozen canaries go stale as tasks evolve — version-bump via signed commit is the pressure valve, and the signature makes every canary change *blameable*.

**Score: 8/10** (novelty 6 × feasibility 9 — grader isolation is ancient wisdom; the monthly bait-probe is the part worth stealing).

### 9. Gold Inflation — the hard budget and the cross-family anchor

**Failure mode.** Any internal loop drifts toward booking more gold per day — the canary softens, the pull-rule gets gamed by reflexive pulls, the museum gets deposed on noise. Defense: a **hard weekly gold budget** (bookings past the cap queue for next week — you cannot print gold, only mint it at a fixed rate), plus a **cross-family anchor**: monthly, a sample of N artifacts is graded by cloud GLM *blind* (no day-log context, no canary scores), and if the external grade diverges from the internal booking by more than a pre-declared margin, all booking **freezes** until a human rules. Inflation is made structurally impossible: the mint has a rate limit and an external auditor.

**First test.** Book one week normally; then run the monthly audit early on a 20-artifact sample. Pass: internal-vs-external grades agree within the margin, and the budget never binds. Fail: divergence past margin — which is not a disaster but the system working; the freeze is the feature.

**Cost/risk.** One blind GLM call-set per month (cheap) and a budget constant (Casey sets it; suggest starting at 2× current daily mean so the cap only bites under inflation). Risk: the budget throttles a genuine breakthrough week — allow one signed human override per period, logged.

**Score: 7/10** (novelty 6 × feasibility 9 — monetary policy for a robot forge, and every part is a cron job).

### 10. Nudge Sycophancy — placebo logs and the red-team quota

**Failure mode.** The nightly advisor wants to look useful and agrees with itself; nudges drift toward flattering the day's direction ("more of what worked!") and the docket fills with agreeable, unfalsifiable prose. Defense, two parts. **Placebo nights:** ~1 night in 10, the cron receives a *shuffled or decoy day log* (unlabeled); nudges proposed against a placebo are filed but never applied, and their predicted effect sizes are expected to collapse — a model dispensing the same confident advice against a fake log is sycophantic by construction, and the docket catches it automatically. **Red-team quota:** every docket requires the advisor to argue *against* one of its own still-live nudges; refusal or a strawman rebuttal is itself a logged finding.

**First test.** 3 placebo nights in the first month. Pass: placebo nudges' predicted effects are ≤ ⅓ the magnitude of real-log nights (pre-declared threshold). Fail: placebo advice is just as confident — the advisor is pattern-matching plausibility, so demote its bets' priors in the docket until calibration improves.

**Cost/risk.** ~10% of nightly cron calls, a log-shuffler. Risk: decoy logs are detectable by anomaly (a real forge day looks like a real forge day) — build decoys by *permuting real days*, not synthesizing them.

**Score: 9/10** (novelty 8 × feasibility 8 — placebo control for an AI advisor is the file's most exportable idea; it generalizes to every cron in the fleet).

---

**Sequencing, if forced:** idea 4 (half-life + A/B) first — nothing else is measurable without it; then 1 (pull-or-scrap) and 8 (canary firewall) to make the currency real; then 3/5 (docket + bets) once there are effects to ledger. Everything else can wait for evidence. The through-line: **a self-improvement loop is safe exactly to the degree that its grader, its advisor, and its worker are three different things with three different incentive paths — and every runaway in the literature is one of those three wearing another's hat.**
