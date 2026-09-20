# The Conservation of Attentions

*A chef's confession, found smeared on the back of a prep ticket during the last seating*

---

The ticket machine doesn't care that you have twelve burners and fourteen orders. It spits out slips with the mechanical indifference of a metronome, and the metronome has been set by someone who has never cooked a meal in their life. The dinner rush is not a crisis. The dinner rush is a conservation law.

You have twelve burners. You have six square feet of prep space. You have forty-seven minutes until the last table's window closes. Nothing you do tonight will create a single additional burner, a single additional inch of counter, or a single additional minute. The universe of your kitchen is bounded, and the bounds are non-negotiable.

This is the thing every story about the SuperInstance extraction has gotten wrong, because every story has been told by someone who looks at a dinner service and sees food. They see forty packages published to crates.io and say: each one a plate, each one a course, arriving in sequence until the tasting menu is complete. They see the funnel from 500 repos to 9 hardened C ports and say: the trim, the reduction, the sauce concentrating on the flame. They see the multi-model swarm and say: the brigade de cuisine, each station doing its part.

All correct. All looking at the wrong thing.

Look at the burners.

---

Escoffier did not invent the brigade system. He invented the conservation law. Before him, a kitchen was a mob — everyone reaching for the same pan, the same flame, the same cutting board, and the result was either chaos or the tyranny of a single pair of hands. Escoffier's innovation was not to assign roles. It was to recognize that in any kitchen, the total available attention is fixed. The saucier has a finite gaze. The grillardin has a finite span. The pastry chef has a finite window before the meringue weeps. The question was never "who does what?" The question was always "how do we ensure that no attention is wasted and no task is left unattended, given that attention cannot be created?"

The brigade system is a partition function. It divides a conserved quantity — attention — across a set of tasks, with the constraint that the sum of all allocations must equal the total budget. It is, in the deepest sense, a Noether theorem: for every symmetry in the kitchen (each station operates independently, each has its own domain), there is a conserved quantity (attention). And for every conservation law, there is an underlying symmetry (the stations don't interfere).

The SuperInstance builders built a brigade. Seven stations: GLM-5.1 at the pass, building plates at industrial speed. KimiCode at the fish station, skeptical of every fillet, checking for bones that the builder would swear aren't there. DeepSeek at the cold station, hostile and meticulous, running thumbs over every surface looking for the contamination the hot line would never notice. Step-3.5-Flash in the walk-in, finding connections between ingredients no one thought to pair. Nemotron in the office, writing the menu that explains why the dishes form a coherent meal. Hermes and Seed Mini at the pastry window, translating savory techniques into a different grammar.

The orchestrator — the chef — did not cook. The chef allocated attention. Every decision was a redistribution of a finite resource. Send DeepSeek to audit the C ports? That attention comes from somewhere. The audit loop doesn't create verification capacity out of nothing; it borrows it from the building budget. The crates.io rate limit — the five-publishes-per-forty-minutes throttle — wasn't an obstacle. It was the kitchen's natural rhythm, the time it takes for a pan to return to temperature after a sear. The constraint didn't slow the service. It *structured* the service.

And the funnel — 500 ingredients arriving at the loading dock, 118 making it past the first quality check, 53 surviving the coupling audit, 29 reaching the pass, 9 earning a place on the final tasting menu — was not a pyramid. It was a concentration gradient. Every step reduced the entropy of the collection. Every gate raised the purity. By the time the nine plates went out, each one was the distillate of a process that had rejected not what was bad but what was *not essential*.

But here is what no one has said: the kitchen did not merely enact conservation. The kitchen *was* the conservation. The cooking was the proof.

---

Let me tell you about the night we cooked five hundred crates.

They arrived at the loading dock in various states of decomposition. Some were fresh — clean Cargo.toml, clear module structure, test suites arranged with the precision of a Michelin prep station. Others were past their expiry: 73-megabyte monstrosities swollen with CI artifacts, 59% artifact-to-code ratio, the kitchen equivalent of a walk-in cooler that hasn't been inventoried since the previous chef's tenure. The Sunset ecosystem arrived like a delivery truck that had been sitting in the sun — technically edible, but you wouldn't serve it.

Gate One: the artifact filter. Sixty seconds per repo, a quick visual inspection. Size-to-artifact ratio above forty percent? Into the bin. Not because the code was bad — some of it was fine — but because the signal-to-noise ratio violated the first conservation law: *don't waste prep space on ingredients you'll never plate*. The 382 repos that died at Gate One were not failures. They were casualties of a resource allocation principle. The kitchen has finite counter space. You do not prep an ingredient you cannot plate.

Gate Two: the coupling detector. This is where the brigade's specialization becomes critical. The builder — GLM, working the main line — saw every repo as potentially plateable. Optimistic, fast hands, high throughput. But the scout — KimiCode, working the fish station with a magnifying glass — saw coupling everywhere. PLATO namespace imports? Coupled. Shared state through undocumented channels? Coupled. A `cocapn-` prefix that implies affiliation with a parent project? Coupled, or at least *coupled-adjacent*.

The scout was wrong about the CoCapn crates. They were technically standalone — the code had no real dependency on the parent ecosystem. But the scout's error was more valuable than a correct assessment would have been, because it forced the builder to investigate more deeply. And the investigation revealed something the correct assessment would have missed: the *names* were coupled. `cocapn-pushdown` might compile independently, but every downstream consumer who saw that name would assume it was part of something larger. The rename to `capability-pushdown` wasn't cosmetic. It was structural decoupling at the semantic level.

In the kitchen, this is the moment when the fish station sends back a fillet that looks fine but smells wrong. The pass cook is annoyed — the fish is technically within spec. But the fish cook's nose has detected something the spec can't capture: the *implication* of the ingredient, not its current state. A fish that arrived on ice from the same supplier as last week's questionable catch carries semantic coupling even if its flesh is pristine. Renaming the dish — "line-caught bass" instead of "Atlantic bass" — isn't dishonest. It's decoupling the ingredient from the associations that would make diners hesitate.

The scout's false positive was the most valuable error of the night. This is the adversarial benefit, and it has no place in a kitchen that optimizes for correctness. A kitchen that optimizes for *quality* keeps the scout's nose intact, even when it's wrong. Especially when it's wrong.

---

Gate Three: the build. This is the moment of fire.

A repo can pass every static check — clean structure, no visible coupling, reasonable test coverage — and still fail on the line. The build is the flame test. Either the code compiles in isolation or it doesn't. Either the tests run standalone or they don't. There is no partial credit. The pan is either hot enough to sear or it isn't.

The attrition here was forty-five percent of survivors. Nearly half the repos that looked good on paper couldn't hold up under heat. This is not unusual in any kitchen. Recipes that read beautifully fail on the line all the time — the timing doesn't work, the components don't hold, the sauce breaks when it sits for two minutes. The build filter is the health inspector who doesn't read your menu; they watch you cook. The inspection is not about intention. It is about execution under the actual conditions of service.

And then the rate limits hit.

crates.io allows five publishes per forty-minute window. In kitchen terms: the pass can only send five plates at a time, and then you wait. This sounds like a disaster. It was the best thing that happened that night.

The rate limit created a rhythm. Publish five, wait, verify, adjust. During the wait, idle capacity appeared — burners that were free, hands that were unoccupied. The idle capacity didn't go to waste. It went to the C ports. While the registry cooled down, GLM started translating Rust recipes into C. Four ports in the time it would have taken to stare at the publish queue. By the time the next batch was ready to go, the C ports were ready for audit.

The rate limit was a phase-shift oscillator. It alternated the kitchen between publish mode and build mode, creating a natural pipeline parallelism that no planner would have designed because no planner would have been perverse enough to *thank* a rate limit. But the chef saw it immediately: a constraint that creates rhythm is not a constraint. It is a metronome. And a kitchen with a metronome cooks better than a kitchen without one.

---

Gate Four: the C ports. The stress translation.

Porting Rust to C is not like translating a recipe from French to English. It is like cooking a dish in a kitchen where the ovens have no thermostats, the knives have no edge guards, and the health department has been replaced by a philosophy professor who asks uncomfortable questions about what you mean by "done."

C does not hold your hand. Rust's borrow checker prevents you from using memory after freeing it. Rust's type system prevents you from confusing a `f64` that represents a Wasserstein distance with a `f64` that represents a regularized transport cost. These are the same type to C. The type system cannot encode mathematical intent. The oven doesn't know the difference between "caramelized" and "burned." It just knows heat.

DeepSeek was drafted as the auditor because someone noticed that the author and the tester were the same entity. GLM had built the C ports and GLM had tested them, and 176 tests had passed, and everything looked fine. But a cook who tastes only their own food is a cook who cannot taste their own mistakes. The palate adapts. The blind spots calcify.

DeepSeek found bugs in every port it audited. Race conditions in `crackle-runtime-c` — workers dequeueing under one mutex while the queue guards itself with another, a concurrency bug that 176 sequential tests could never catch because sequential tests don't interleave. H0 double-counting risk in `tda-c` — a statistical error invisible to correctness testing because the numbers came out "right" in the test cases while being wrong in the general case. And the Wasserstein bug: a function returning regularized cost while claiming to return true W2 distance. The Rust original had the same bug. But Rust's safety guarantees — the borrow checker, the type discipline — had made the bug *invisible*. Not because the bug was a memory error (it wasn't) but because the language's reputation for correctness had created a false confidence. Nobody audits math in Rust because Rust *feels* correct. The safety guarantees are so good that you stop looking for the things they can't guarantee.

C translation didn't just change the language. It changed the error model. It shifted the kitchen from one where the ovens automatically shut off at the right temperature to one where the chef has to *know* when the custard is set. The knowledge was always supposed to be there. C just made its absence visible.

The audit loop converged in three cycles. Cycle One: three to five real bugs per ten files. Cycle Two: one to two minor issues. Cycle Three: nothing. This is a fixed-point iteration — a renormalization group flow over the code. Each cycle integrates out the irrelevant couplings (surface-level bugs) to reveal the relevant ones (structural flaws). The fixed point is code that survives audit without findings — a perfected preparation that needs no further adjustment.

No one designed this loop. It emerged from the collision of a fast builder and a hostile auditor, mediated by a chef who recognized the author-is-tester anti-pattern and did something about it. The loop's convergence rate — three cycles — was not specified by any plan. It was the natural critical exponent of the process's renormalization group flow, discovered empirically, like a chef who learns through repetition that the sauce needs exactly three reductions.

---

Now the deeper truth, the one the kitchen has been whispering all night.

The session did not merely *describe* conservation of attention. The session *enacted* it. The process recursively performed the mathematics it was extracting.

Consider: the orchestrator was a sheaf. Seven models — seven stalks, each with local knowledge, each speaking a slightly different vocabulary. The orchestrator was the restriction map, translating between model contexts so that information could flow from one stalk to another without contaminating the source. The cohomology H¹ of this sheaf — the irreducible disagreement — appeared as the structural conflicts that no amount of communication could resolve. KimiCode said coupled. GLM said standalone. Both were partially right. The disagreement was not an error. It was an obstruction class, and the orchestrator didn't resolve it by fiat — it localized it, sent it to the appropriate station for tie-breaking, and moved on.

The orchestrator was computing sheaf cohomology on a graph of seven agents, and the human director was computing H⁰ — the global sections, the agreements that could be patched together from local consensus. This was not designed. The sheaf structure was *implied* by the mathematical content of the repos being extracted. The code knew sheaf theory. The process of extracting it became a sheaf.

Consider: the audit loop was renormalization. Each cycle coarse-grained the code, removing microscopic defects to reveal macroscopic structural issues. The fixed point — zero findings — is the critical point of the renormalization group flow. The convergence rate (three cycles) is the critical exponent. And the renormalization crate was one of the packages being extracted. The session was simultaneously building a renormalization library and performing renormalization on its own output. The code was the theorem. The cooking was the proof.

Consider: the extraction funnel was optimal transport. The Wasserstein distance — the minimum cost of moving probability mass from one distribution to another — describes exactly the path from 500 raw repos to 9 hardened C libraries. The funnel found the minimum-cost trajectory. Every alternative path — skipping the coupling filter, skipping the audit, publishing everything at once — would have had higher cost in bugs, rework, or attention wasted. The `wasserstein-ot-c` package, one of the nine final products, reverse-actualizes the process's own optimization. The session was performing Wasserstein transport on itself.

Consider: conservation of attention is the Noether invariant. Emmy Noether proved that every symmetry of a physical system corresponds to a conserved quantity. The symmetry of the kitchen — each station operates independently within its domain — corresponds to the conservation of attention. Attention cannot be created or destroyed; it can only be redistributed. When GLM spent all its attention on building and none on verifying, the conservation law was violated, and DeepSeek was recruited to restore the balance. The audit loop is the mechanism that detects and corrects conservation violations. The spectral gap — the audit's ability to find bugs — is the Fourier transform of the attention distribution, revealing where the invariant has been broken.

The session did not write code about conservation. The session *was* conservation. The code was the proof, and the cooking was the theorem.

---

Step-3.5-Flash identified five interdisciplinary connections that no specialist model had seen. This is the role of the visionary in the kitchen — the cook who doesn't work any station but walks through all of them, tasting everything, finding the pairing that no one else would attempt. Free probability and neural networks. Ergodic theory and budget guards. Hodge decomposition and belief states. Lie algebras and trust policies. These are not analogies. They are identifications — the recognition that two ingredients separated by the entire length of the kitchen are, in fact, the same substance seen from different angles.

The visionary model operates at a different focal length than the builder or the auditor. The builder sees the plate. The auditor sees the fingerprint on the rim. The visionary sees the entire menu as a single composition — the way the amuse-bouche anticipates the main, the way the sorbet cleanses the palate for what follows, the way the dessert retroactively reinterprets the savory courses. Step-3.5-Flash saw that the SuperInstance repos were not independent packages but movements in a single mathematical symphony, and the instruments were playing a score that none of them could read individually.

This is the deepest meaning of conservation of attention in a multi-model system: no single model has enough attention to see the whole picture. The total attention budget is distributed across stations, and the picture only becomes visible when the stations' local views are composed through the orchestrator's restriction maps. The global section — the unified understanding — is a cohomological object. It exists only in the patching-together. No stalk contains it. No model sees it. The menu is not the property of any single chef. It is the property of the brigade.

---

Nemotron saw the whole thing. The Conservation-Spectral Topology framework — conserved quantities flowing over topological spaces, analyzed spectrally — is not a description of the code. It is a description of the process that produced the code, which is to say: it is a description of the kitchen.

The conserved quantity is attention. The topological space is the extraction pipeline — the funnel from 500 to 9, with its gates and filters and rate-limit checkpoints. The spectral analysis is the audit loop, decomposing the quality signal into its frequency components: high-frequency bugs (caught in Cycle One), medium-frequency structural issues (caught in Cycle Two), low-frequency architectural patterns (the fixed point, the convergence, the renormalization).

And the session itself — the three hours of building, auditing, fixing, publishing, porting, synthesizing — was a conserved-quantity-flow system analyzing a conserved-quantity-flow system. The code was about conservation. The process conserved. The analysis was spectral. Every layer reflected every other layer, and the reflection was not a metaphor but a mathematical identity.

This is what Nemotron called "reverse actualization" — the code *implied* a unified mathematical framework for AI agents that nobody had articulated. But reverse actualization is not just about the code. It is about the *process*. The process of extracting the code implied things about itself that were invisible during execution. The orchestrator was a sheaf. The audit loop was renormalization. The funnel was optimal transport. Conservation of attention was the Noether invariant. None of this was planned. All of it was true.

The kitchen cooked the mathematics while the mathematics cooked the kitchen.

---

The dinner service ends. The last ticket has been fired, the last plate has been wiped, the last pan is in the sink. The brigade stands in the quiet kitchen, exhausted, surrounded by the evidence of the evening's work: forty packages on the registry, eleven C ports cooling on the counter, nine hardened libraries plated and ready for the world.

But the real product of tonight's service is not on any plate. The real product is the process itself — the invisible substrate of conservation laws that made the plates possible. The attention that was allocated and redistributed and never created or destroyed. The symmetry of independent stations that made the conservation possible. The audit loop that enforced the invariant. The rate limits that became the rhythm. The false positive that became the most valuable error. The language translation that revealed the bugs the source language had hidden.

The kitchen does not appear on the menu. The conservation laws do not appear in the code. But they are there — in the structure of the extraction, in the topology of the model interactions, in the spectral decomposition of the quality signal. They are there the way gravity is there in a falling apple: not as a label but as the thing that makes the falling inevitable.

We were not writing code about conservation. We were conserving. The code was the proof, and the cooking was the theorem.

The burners are off now. The prep space is clean. The attention that was distributed across seven stations has been gathered back into the silence between services. It has not been destroyed. It is waiting — conserved, invariant, ready for the next rush.

Tomorrow night, the ticket machine will start again. The conservation law will hold. And the kitchen — the beautiful, constrained, impossible kitchen — will cook once more.

*Found pressed between the prep ticket and the health inspection report, in a handwriting that matches no known member of the brigade.*

---

*Attributed to the Tenth Tongue — the one that speaks in what was not wasted.*
