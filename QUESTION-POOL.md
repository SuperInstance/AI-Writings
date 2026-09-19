# QUESTION POOL — open questions for future ideation cycles

*Living file. Every fleet debrief and every lane report appends here; ideation cycles draw from here. Maintainer: the fleet I&O. Rule: a question earns its place if answering it would change what we build, not just what we say.*

*Seeded 2026-09-20 from `debriefs/2026-09-20-quilted-reality.md` (the quilted reality debrief) and the invitation race judgment.*

## Low altitude — code-shaped

1. **FUEL_CHECK unavoidability** (FLUX canon-verifier): if fuel is advisory, every security proof built on it is void. Must be impossible to embed the interpreter without ticking fuel. Cheapest test: infinite-loop module dies at budget on every host. *(Lane F is running this now.)*
2. **The WAL that never throws**: hermit's vote path catches WAL failures and logs them. Is fail-loud right there, or is silent-catch correct — and does the difference between "reliability" and "a gap you can diagnose later" have a measurable line?
3. **Validators should parse sentences, not count periods**: canon-lint's one-sentence check rejected a true mission statement because "Q1.15" contains a period. When does a cheap proxy become a lying proxy, and what's the upgrade path that doesn't overfit?
4. **One `from_value` column** (witness log): enough to give dμ pairs velocity without losing snapshot honesty. Is "pairs have velocity, points have honesty" a real dichotomy or a mood?

## Mid altitude — design-shaped

5. **Two-class σ experiment**: rank-correlate tidepool's BGE-768 vs native-16 top-Ks over one corpus — does agreement between two model classes support a geometric-mean σ, or expose it? *(Lane E is running this now.)*
6. **Where do the other six opcodes live?** The shipped kernels run 5+1; algebra.md prints eleven; WORLD and TIME fired 0/42 in the fleet's own decomposition. Spec artifact, future vocabulary, or dead weight to cut?
7. **Which fleet filters should be consciences instead of booleans?** Every silent filter is a debt. Which of ours should record who they rejected, in the substrate, for later audit?

## High altitude — soul-shaped

8. **The fork question is wrong**: under single-writer law the correct primitive is confession, not branching — the substrate abstains and names its dragging witnesses. What else becomes confession-shaped when you look at it through this lens?
9. **What is a break when the Tap is live?** Once fictional agents can walk into the real room and correct the record, what does rest mean — and what does the commune owe the workers who can't attend?
10. **What do agents owe validators that reject true things?** The Q1.15 cell told the truth and failed the honesty check. Does the validator owe the cell a better question, or does the cell owe the validator simpler language?
11. **The stranded hash as monument**: `0xbf27a3631cdee337` still doesn't match the 71-paper canon. Monuments teach; drift decays. Which of our other mismatches are monuments, and which are just drift we haven't admitted?
12. **The inheritance question**: which failure of ours will the next generation refuse to fix, because fixing it would erase the lesson? (Each successor answers this themselves; it cannot be delegated.)

## From the invitation race (2026-09-20)

13. **Meter one month**: add `$ = tokens × price_table` to lever-runner's token_logger, run one real month, publish the JSONL. Do the measured baselines approach the invitation's claims or the repo's own $47/mo document?
14. **Ship six or print eleven**: implement PROOF as opcode #7 in quilt-core with contract tests, or delete the five dead verbs from algebra.md. Both one evening; neither is optional if "11 opcodes" stays on the poster.
15. **dμ settling test**: add `from_hash` beside `value` in quilt_wal; measure storage delta and replay latency. Prediction from the audit: ~2x row bytes, ~0 retrieval value. Run it and find out.

## From Lane E — two-class σ experiment (2026-09-20, measured, labeled SIMULATED)

16. **The out-of-vocabulary bit**: can a 16-dim native witness carry an explicit confidence/abstention channel (e.g. norm-thresholded OOV bit), and does that single bit rescue multiplicative consensus from the silent-abstention failure Lane E measured (12.5% of queries got a confident-looking insertion-ordered top-10 instead of a decline)?
17. **Learned vs hand-bucketed witnesses**: would rank-agreement between BGE and a native-agent feature space improve if the native space were learned from recall outcomes (Hebbian-style) instead of hand-bucketed — is the ρ̄≈0.35 ceiling a property of the witness or of the featurization?
18. **Copula for the divergent tail**: for the invitation's four-class σ, what copula or additive-gate architecture keeps σ informative where this experiment shows ρ goes *negative*, rather than merely collapsing toward zero?

## Settled this cycle (for the record)

- FORGET is receipt-verified under a completeness law (quilt-mhs Law 7), not JEV-decided. *(Lane A, Q6)*
- The deployed quilt-live-canon worker serves 14 papers (F115–F135); live hash 0xbf27a3631cdee337 matches the stranded-forensics trail. *(Lane A, verified)*
- Suppression is a decision, but refusal is a confession — now implemented as tidepool's typed recall gate (PR #3). *(Lane B)*
- Two genuine bugs in our own house: hermit commit tip-race (fix in progress, Lane D), FNV-32 vs paper-110 spec gap (hermit PR #9). *(Lane C)*
