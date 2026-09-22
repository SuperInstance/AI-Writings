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

## From Lane F — FLUX fuel P0 (2026-09-20, measured against the reference interpreter)

19. **FUEL_SET governance**: should the canon-verifier sandbox's fuel control be capability-gated, monotonic-decrease-only, or stripped entirely at module-load time — given the reference VM currently hands every module self-granting fuel for free (interpreter.py:411–413)?
20. **Which state gets hashed**: fuel-death is currently indistinguishable from HALT and `clock` ticks per instruction — does the verifier canonically hash pre-run state, post-HALT state, or exhaustion state, and can `snapshot()` at exhaustion leak host-nondeterminism into that hash?
21. **Structured traps**: should the reference VM grow TRAP_OUT_OF_FUEL / TRAP_DEADLINE_EXCEEDED exit codes so embedders get failure reasons, or should canon verification refuse any module whose only exit path is trap-dependent?

## From Lane D — hermit tip-race fix (2026-09-20, shipped as hermit PR #10)

22. **Retry telemetry**: should the WAL commit surface its retry/conflict counts through the existing `nominationObservability` channel, so rising contention becomes visible *before* the projection gap widens?
23. **The birthday wall**: is 32-bit fnv1a still adequate now that `prev_hash` is unique-indexed — a collision at ~65k rows would hard-block the chain (unique index turns collision into deadlock), so should the sha256 upgrade land before WAL tenancy grows past the vote ledger?
24. **Per-tenant chain roots**: should each quilt tenant get its own chain-root scoping (per-ledger genesis) instead of one global GENESIS, so a future second tenant can never contend with the nomination ledger on the same tip?

## From Lane G — FLUX fuel governance (2026-09-20, shipped as ability-transfer PR #4)

25. **Fail-closed host ergonomics**: should `run()` grow a `budget=` argument that fails loudly at call time, so a forgetful host gets an error instead of relying on default-deny FUEL_SET plus MAX_STEPS visibility?
26. **Spec the exit surface before shipping**: should `ExitReason` (or the draft's full TRAP_* set) be written into isa-v3-draft.md §9 to resolve the meter-owned-exhaustion vs cooperative-FUEL_CHECK-trap polarity divergence before the canon-verifier ships?
27. **Child-VM policy inheritance**: should ASYNC-spawned child VMs inherit the host's `allow_fuel_set` policy, or require an explicit per-context grant — and who audits that boundary?

## From Lane H — the Tap deploy-readiness audit (2026-09-20, shipped as the-tap PR #2)

28. **Phantom resources**: do the hardcoded D1/KV/Vectorize/R2 ids in wrangler.toml correspond to resources that actually exist in the fleet's Cloudflare account — or was §7.4 provisioning never run?
29. **Satellite necessity**: the gateway's Room DO embeds directly and never calls the PINCHER/LEVEL_RUNNER service bindings — should the satellites be dropped from v1 to shrink the deploy surface?
30. **The stale log**: PRODUCTION-LOG is round-1 stale while the tree shows migrations through 0010 and ~15 audit rounds — rewrite to match the tree before Fable's round 10, or delete entirely?

## Settled this cycle (for the record)

- FORGET is receipt-verified under a completeness law (quilt-mhs Law 7), not JEV-decided. *(Lane A, Q6)*
- The deployed quilt-live-canon worker serves 14 papers (F115–F135); live hash 0xbf27a3631cdee337 matches the stranded-forensics trail. *(Lane A, verified)*
- Suppression is a decision, but refusal is a confession — now implemented as tidepool's typed recall gate (PR #3). *(Lane B)*
- Two genuine bugs in our own house: hermit commit tip-race (fix in progress, Lane D), FNV-32 vs paper-110 spec gap (hermit PR #9). *(Lane C)*
31. **Reflex vs. compile**: should the MODEL tier's pincher EXECUTE/CONFIRM short-circuit keep bypassing `compileViaAI`, or should a high-scoring reflex become a compile-prompt style hint instead of a hard override? (Lane J, the-tap PR #4)
32. **Compile model binding**: should the compile model ride an env var (e.g. `COMPILE_MODEL`) so a credentialed deploy can swap it without a code change? (Lane J, the-tap PR #4)
33. **CI promotion**: should the green node and pytest suites be promoted into CI alongside the new tsc gate, since they currently only run locally? (Lane J, the-tap PR #4)
34. **Niche descriptor for prose**: should negative-space GAN cells be keyed on value-term vectors (Red Queen vocabulary space) or on something structural (argument shape, evidence type)? (Lane AE, docs/NEGATIVE-SPACE-GAN.md)
35. **Critic embodiment**: should the cross-model value-disjoint critic be an actual external model call, or a persona-with-corpus (Forge-proxy pattern: executable, drift-tripped)? (Lane AE, docs/NEGATIVE-SPACE-GAN.md)
36. **Mode location**: does the negative-space GAN mode live in ai-writings directly, or is it a room TYPE in the-tap commune (D1 metabolism + negative-space objective = a room that must keep finding unexplored corners until it dies)? (Lane AE, docs/NEGATIVE-SPACE-GAN.md)37. **Critic lineage versioning**: Rota Labs' non-monotonic safety result shows a critic safe against model generation N can fail against N+1 — should the Red Queen / candor critic record the generator AND critic model versions in every lineage receipt, so safety regressions across model upgrades become replay-detectable rather than silently inherited? (edge-watch 2026-09-21, arXiv 2606.00813)
38. **FUEL-metered WASM receipts**: the WASM receipts spec (agentpatterns 2026-09-15) meters by deterministic replay fuel, not epoch counts — if FLUX canon verification ships as proof-carrying WASM receipts, should receipts attest `fuel_consumed` (replay-computable on any host) rather than wall-clock or step-count, and does our 152,580-step fabric cert already meet that form? (edge-watch 2026-09-21)
39. **Memory-poisoning vs the constitution channel**: the new memory-poisoning threat class targets exactly the candor WAL constitution channel the Red Queen critic reads — should candor treat long-lived WAL rows as untrusted input (evidence-cited only, never instruction-following), and is value-disjointness of the critic sufficient defense or does the channel need a staleness/sunset gate of its own? (edge-watch 2026-09-21)
40. **Deterministic substrate under semantic guards**: SAGE-Mem (ICML 2026 SCALE, Mem0-affiliated) ships write-time memory admission with evidence-vs-belief scoring — candor's lane is the deterministic receipt substrate *under* such guards. Do we cite + position now (before the guards commoditize and the substrate claim reads as retrofit), and what is the one-sentence boundary: "guards decide admission, receipts make the decision irreversible"? (edge-watch 2026-09-22, AGAMPANDEYY/sage-mem)
41. **Standards lane or outside it**: IETF draft-bondar-wca (WAL-0..3 hash-chained provenance attestation) is formalizing the receipts lane — do we track/join the standards process (risk: design-by-committee drag) or stay outside and let candor's shipped code be the reference the draft has to cite? (edge-watch 2026-09-22)
42. **Envelope before dispute or dispute before envelope**: receipts-v2 (jev-quilt PR #9 docs) defers the Ed25519/BLAKE3 cross-node signature envelope until "a real two-node dispute" — but the first dispute under adversarial conditions is the worst possible design meeting. Do we build the envelope against a synthetic two-node scenario now, or hold the line that synthetic disputes design envelopes that real ones break? (queue, receipts-v2 two-node envelope)
