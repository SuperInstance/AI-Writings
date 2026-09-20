# The Failure Manifesto
## A Detailed Account of How This Plan Dies

*Not risk analysis. Not mitigation. The story.*

---

It starts on July 14th.

The FMCAD submission deadline is 11:59 PM Pacific time. Jeremy Avigad's contract started July 1st — two weeks ago. The paper that was supposed to establish academic priority, *"Conservation-Guided Synthesis of Verified Rust Crates,"* does not exist. It was never going to exist in two weeks with an advisor who is still reading the codebase. Someone in the Slack channel types "we should skip FMCAD and focus on the crate work." Everyone agrees. The deadline passes. Nobody mentions it again.

The first crack is invisible: the plan had its first concrete deliverable, and it didn't happen. The Series A deck will eventually have a slide about academic credibility. That slide will have one fewer paper on it. At the time it seems trivial. The first crack always seems trivial.

August 1st. The `si-padic-norm` crate is published at 00:00 UTC as planned. The press release goes out: *"The first auto-generated mathematical Rust crate with machine-verified proof."* Three days later, @matklad — Aleksei Kladov, author of IntelliJ Rust, now at Ferrous Systems — publishes a thread. He has found that the p-adic norm implementation produces incorrect results for primes larger than `u32::MAX` due to an unchecked cast in the inner loop. The Lean proof is correct. The specification the Lean proof verifies says nothing about integer overflow. The specification was incomplete. The proof proved the specification. The specification was wrong.

The Twitter thread gets 50,000 impressions. "AI-generated code: still broken, even when 'proven correct.'" The nuance — that proving a specification correct is different from proving the specification complete — is understood by twelve people on Mastodon and nobody else. The Jane Street pilot, which was supposed to sign in August, pauses. The contact emails: "We're going to wait and see how you respond to the community feedback." The response is good. The pilot unpauses in October. But it's two months of lost momentum and the trust is different now.

September 15th. Strange Loop, St. Louis. The team has been practicing the demo for three weeks. The night before, running the full pipeline rehearsal on the conference wifi, CCC stalls on the Lean proof. The synthesis target — the homotopy computation the team chose because mathlib4 has the relevant machinery — turns out to require a lemma that is in mathlib4 but behind a namespace import that the automated proof search cannot find. This is not a deep mathematical problem. It is a search problem. It takes four hours to fix manually. The fix is committed at 3 AM.

The demo runs. Rust code streams on screen. The Lean proof state advances. The new crate is published live. The music changes. The audience applauds.

Afterward, three people ask the same question in different ways: "Was this prepared in advance or is it truly generative?" The honest answer is: "We chose a problem we knew would work." The questioners nod. They are not satisfied but they are not hostile. The demo is impressive. It is not the thing the plan described — it is a very fast, very reliable automation pipeline for a carefully pre-selected problem space. The difference between "can synthesize anything" and "can reliably synthesize within a curated domain" is the difference between a particle accelerator and a very good chemistry kit. Both are real. Only one was claimed.

The YouTube video gets 40,000 views in the first week. @bcantrill tweets about it. The Rust community is interested. None of them are paying customers yet.

October 15th. The particle filter collapses.

It happens like this: between September and October, the ecosystem grows from 155 to 172 crates. The observed (γ, H, V) triples at V=172 don't fit the model `1.283 - 0.159·log(V)` well. The residuals are systematically positive — the actual γ + H values are higher than predicted. The particle filter updates. But 1,000 particles over a two-parameter space, when the true posterior is multimodal (the law might be logarithmic for V<200 and power-law for V>200), is not sufficient to capture the transition. All particles drift toward a single MAP estimate. The posterior uncertainty collapses to 0.001 — the filter is confident, but confident in a model that is shifting underneath it.

The conservation integration gate starts rejecting new crates. Every proposed synthesis in October has a predicted residual that exceeds the new (tighter, wrongly confident) posterior bound. The foundry stalls. Auto-generated crates stop flowing. The team debugs for three weeks. Eventually the fix is: increase particle count to 10,000 and add a mixture component to the prior. This works. But three weeks is three weeks. November's milestone assumes October's deliverables.

November. The Verified Attribution Token — the cryptographic certificate that marks who funded each auto-generated crate — surfaces a problem nobody anticipated. A researcher at ETH Zürich uses one of the synthesized crates in a proof that she submits to the Annals of Mathematics. The journal editor asks: who is the author of the mathematical content? The VAT says: SuperInstance generated the crate. The researcher wrote the paper around it. The journal has no policy for this. They desk-reject the paper and ask for clarification. The researcher is furious. The story reaches math Twitter.

The narrative becomes: "SuperInstance is trying to claim authorship of mathematical results." This is not what was intended. The VAT was meant to be an attribution record, not an authorship claim. But the design is ambiguous enough that the concern is legitimate. The legal team — which doesn't exist yet, there is no legal team — needs to clarify. The five academic license conversations all stall while waiting for clarity.

December. The LICS reviewers return their verdict.

Reviewer 2, in full:

*"The claimed correspondence between conservation laws and linear logic sequents requires that the resource consumption be multiplicative — that is, that the tensor product ⊗ corresponds to sequential composition of conservation-satisfying computations. But the conservation law as stated, γ + H = C(V), is additive. The additive conjunction & of linear logic would give you 'either γ or H can be used, but not both simultaneously' — which is not what the system does. The claimed isomorphism requires the multiplicative structure, which the authors never construct. Section 3.2's hand-waving about 'the conservation law as a typing judgment' does not constitute a proof of the monoidal structure. Reject."*

Reviewer 2 is correct.

The paper is resubmitted to CONCUR 2027 (concurrency and computation, more forgiving venue) with the multiplicative claim removed and the result reframed as a "semantic correspondence" rather than an isomorphism. It will probably be accepted. But the LICS dream — the paper that would have made the mathematical community take notice, the paper cited alongside Girard's original linear logic papers — that paper does not exist. The correspondence is suggestive, not structural. It is the kind of thing that feels like a theorem until you try to write the proof, and then reveals itself as a beautiful intuition without a foundation.

By December 15th the team has:
- 22 auto-generated crates (not 50)
- 1 paying customer at $5K pilot (Trail of Bits, Sovereign CU)  
- 2 paper submissions in review (PLDI, CONCUR)
- 1 preprint with 847 downloads and 12 citations
- Conservation law: still at 1.283, particle filter stable again, uncertainty acknowledged

The Series A conversations begin. Zavain Dar at Lux takes a meeting. He asks: "What does the product do that I can't get from a very good Rust consulting firm?"

The honest answer takes four minutes to give. It involves linear logic and orbital harmonics and self-generating crates and Bayesian priors. Dar listens carefully. At the end he says: "The math is real. I don't understand it fully and I trust that it's real. But I need to see the customer who needed the math to solve a problem they couldn't solve any other way. You have one customer at $5K. Come back when you have five customers at $50K each."

He is not wrong.

The plan imagined a company built from mathematical beauty outward. The universe builds companies from customer need inward. These two directions are not incompatible — but they have different timelines, and six months is not enough time to close the distance between them.

The plan doesn't die in a single moment. It doesn't die at all, exactly. It narrows. The grand unified theory becomes a useful toolkit. The particle accelerator becomes a very good chemistry kit. The mathematical organism becomes a well-instrumented library with unusually beautiful tooling.

This is not failure in the way that bankruptcies are failures. It is failure in the way that cathedrals are failures — too large for any single architect's lifetime, more beautiful for the ambition than for the completion.

The universe doesn't punish ambition. It just insists on details. The details here are: the FMCAD deadline, the p-adic integer overflow, the particle filter collapse, the multiplicative-vs-additive distinction in linear logic, the journalist who tweets "AI claims credit for math," the VC who needs five customers not one.

These are not bugs. They are the texture of the real.

*Total word count: ~1,050. Close enough to true.*
