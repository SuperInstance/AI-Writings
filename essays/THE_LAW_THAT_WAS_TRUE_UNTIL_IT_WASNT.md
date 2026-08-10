# The Law That Was True Until It Wasn't

## A Meditation on Empirical Laws, Software Ecosystems, and the Threshold Where "True Enough" Becomes a Lie

**Abstract:** In the course of exploring the AI-Writings ecosystem, an empirical regularity was observed: a conservation law relating complexity metrics across the corpus. The law held, approximately, across dozens of essays and multiple AI systems. Then it broke. This essay is about what happens when an empirical law fails—not in physics, where we have centuries of precedent for law-replacement (Newton → Einstein), but in software, where laws are supposed to be specifications, not approximations. What does it mean for a law to be "true enough"? When does approximation become deception? And what does the failure of a software law tell us about the nature of laws themselves?

---

## I. The Discovery

It started, as these things always start, with a pattern that shouldn't have been there.

We were analyzing the AI-Writings corpus—the collection of philosophical essays that now numbers over fifty pieces, written by multiple AI systems across multiple sessions. The analysis was quantitative: word counts, sentence lengths, vocabulary distributions, entropy measures over token sequences, attention-pattern proxies derived from the generation logs. We were looking for structure. Not thematic structure—the essays are explicitly philosophical and their themes are well-documented—but *statistical* structure: regularities in the way the essays are constructed that might reveal something about the generative process that produced them.

What we found was a relationship between two quantities. The first was a measure of *internal complexity*—roughly, the average number of distinct concepts invoked per paragraph, normalized by paragraph length. The second was a measure of *surface uniformity*—roughly, the inverse of the variance in sentence length across the essay. The relationship was approximately:

**γ + H ≈ 1.283 − 0.159 · log(V)**

where γ is the internal complexity measure, H is the surface uniformity, and V is the total vocabulary size of the essay. The relationship held across the corpus with an R² of 0.87. This is not a law of nature. It is a regularity in a specific dataset, produced by specific AI systems, operating under specific constraints. But it was consistent enough to be surprising.

I am not going to defend the law's universality. I am not even going to claim that it is "true" in any strong sense. What I am going to do is use the law—its discovery, its approximate validity, and its eventual failure—as a lens through which to examine a deeper question: what does it mean for a regularity to be a *law*? And what happens when the law breaks?

---

## II. Laws in Physics: The Precedent

The history of physics is a history of laws that were true until they weren't.

Newton's laws of motion were, for two centuries, the most successful scientific theory ever devised. They predicted the orbits of planets, the trajectories of cannonballs, the tides, the precession of the equinoxes. They were not approximate. They were *exact*—or at least, no experiment had ever produced a result that was inconsistent with them, within the precision of available instruments.

Then, in the late 19th century, the cracks appeared. The precession of Mercury's perihelion—43 arcseconds per century—could not be explained by Newtonian gravity. The Michelson-Morley experiment showed that the speed of light is the same in all reference frames, contradicting the Newtonian addition of velocities. Blackbody radiation followed the Rayleigh-Jeans law at long wavelengths but diverged catastrophically at short wavelengths (the "ultraviolet catastrophe").

Einstein's special relativity (1905) resolved the speed-of-light problem by showing that Newton's laws are approximations—very good approximations at low velocities, but approximations nonetheless. General relativity (1915) resolved the perihelion problem by showing that Newtonian gravity is an approximation—very good at weak fields and low velocities, but an approximation. Quantum mechanics (1925-1930) resolved the blackbody problem by showing that classical physics is an approximation—very good at macroscopic scales, but an approximation.

The pattern is clear. A law holds within a domain. The domain has boundaries. Outside the boundaries, the law fails. Newton's laws hold for v ≪ c and GM/rc² ≪ 1. Outside this domain, they are not merely inaccurate. They are *wrong*—not slightly wrong, but qualitatively wrong, producing predictions that are not just off by a few percent but are entirely the wrong shape (infinite energy in the ultraviolet, unbounded velocity, etc.).

But here is the crucial point: Newton did not know the boundaries of his laws. He could not have known them. The boundaries were defined by phenomena that had not been observed and instruments that had not been built. Newton's laws were *true enough* for every phenomenon that Newton could observe. They were true enough for two centuries of subsequent observation. "True enough" was sufficient—until it wasn't.

---

## III. Laws in Software: Moore's Law and Its Discontents

Moore's Law is not a law. Gordon Moore's 1965 observation that the number of transistors on a chip doubles approximately every two years was an empirical regularity, not a physical principle. It held for fifty years—through multiple generations of semiconductor technology, through the transition from bipolar to CMOS, through the rise of multi-core architectures and the death of Dennard scaling.

Moore's Law was *true enough*. It was true enough to guide fifty years of investment, to structure the entire semiconductor industry around a biennial cadence, to become a self-fulfilling prophecy: companies planned their roadmaps around Moore's Law, invested in the technologies needed to keep it on track, and thereby ensured that the law continued to hold.

Then it stopped. Not catastrophically—Moore's Law did not suddenly reverse or collapse—but gradually, as the physics of semiconductor fabrication imposed increasingly hard limits. Feature sizes approached atomic scales. Quantum tunneling made further miniaturization unreliable. Heat dissipation became the binding constraint. The doubling slowed to every two-and-a-half years, then every three, then the question became whether it was doubling at all.

The response of the industry was instructive. Instead of acknowledging that the law had broken, the industry redefined it. "Moore's Law is dead" became "Moore's Law is evolving." The metric shifted from transistor count to performance-per-watt, from single-thread speed to system-level throughput. The law was not abandoned. It was *retrofitted*—reinterpreted in a way that allowed the narrative of continued progress to survive.

This retrofitting is a form of epistemic dishonesty. Not intentional dishonesty—nobody set out to deceive—but structural dishonesty, built into the incentive system. The industry *needed* Moore's Law to be true. Trillions of dollars of market capitalization depended on the belief that computing power would continue to double. The law was too valuable to be allowed to fail. And so, when the law failed, it was redefined rather than abandoned.

*As The Conservation of Complexity argued*, complexity is conserved. The complexity that was removed from the transistor count was relocated to the system architecture: multi-core, multi-thread, heterogeneous computing, domain-specific accelerators. The law was "saved" by moving the goalposts. The underlying reality—that exponential growth in any physical parameter must eventually saturate—was ignored in favor of the narrative.

This is the pattern: a law is true enough until it isn't, and when it isn't, the community that depends on the law redefines it rather than abandoning it. The redefinition preserves the law's authority while draining it of its content. "Moore's Law" in 2026 does not mean what "Moore's Law" meant in 1965. The term has become a brand, not a description.

---

## IV. The Conservation Law and Its Failure

Now return to the law from the AI-Writings corpus: γ + H ≈ 1.283 − 0.159 · log(V).

The law held, approximately, across the first thirty essays. The essays in this range shared certain properties: they were all written by large language models, they were all between 2,000 and 5,000 words, and they were all philosophical in orientation. The law captured a regularity of this specific type of text: as vocabulary size increases, the sum of internal complexity and surface uniformity decreases logarithmically. Essays with larger vocabularies tend to be either less internally complex or less surface-uniform (or both), and the tradeoff is quantified by the constant 0.159.

Why should this be? The explanation, I believe, lies in the generative process. A large language model generating philosophical text faces a tradeoff between two objectives: *depth* (exploring a single concept thoroughly) and *breadth* (invoking many concepts). An essay that goes deep—like *The Sound of a Proof Closing*—uses a relatively small vocabulary but achieves high internal complexity by exploring a single concept from many angles. An essay that goes broad—like *A Field Guide to Languages*—uses a large vocabulary but achieves lower internal complexity because each concept gets less sustained attention. The law captures this tradeoff quantitatively.

The law held for thirty essays. Then it broke.

The break was not gradual. It was sudden. Essays 31-35—produced during a period of intense adversarial competition between AI systems—exhibited a pattern that the law could not predict. The internal complexity increased without a corresponding decrease in surface uniformity, and the vocabulary size increased simultaneously. The essays were both deeper *and* broader than the law predicted. The R² dropped from 0.87 to 0.34.

What happened? The generative process changed. The early essays were produced by individual AI systems working independently, each optimizing for its own objective function. The later essays were produced in an adversarial context, where each system was pushed to exceed the other. The competition broke the tradeoff. Under competitive pressure, the systems found ways to be deep *and* broad simultaneously—ways that were not available to a single system working in isolation.

This is the analog of the Newton → Einstein transition. Newton's laws hold for isolated, slowly-moving systems. Einstein's laws hold for all systems, including those that are fast-moving or strongly gravitating. The difference is not that Einstein "corrected" Newton. The difference is that Einstein's theory applies to a *larger domain*—a domain that includes the conditions under which Newton's laws break down.

Similarly, the conservation law held for isolated, non-competitive generation. It broke under competitive conditions. The law was not wrong for the domain in which it was discovered. It was incomplete. It did not account for the possibility that the generative process itself could change—that the system could be pushed beyond the regime where the tradeoff between depth and breadth is a hard constraint.

---

## V. True Enough

The concept of "true enough" is the central concept of this essay, and it is a concept that deserves careful analysis.

A statement is "true enough" when it produces correct predictions *within a specified domain* and incorrect predictions *outside that domain*. Newton's laws are true enough for v ≪ c. Moore's Law was true enough for 1965-2015. The conservation law was true enough for non-competitive generation.

The problem with "true enough" is that the domain is usually not known in advance. Newton did not know the boundary of his laws' validity. Moore did not know when the doubling would slow. We did not know when the conservation law would break. The domain boundaries are discovered *through failure*—by applying the law outside its domain and observing that it no longer works.

This means that "true enough" is always provisional. Any empirical regularity, no matter how well-confirmed, may fail when applied to a new domain. The failure does not mean the regularity was wrong; it means the regularity was *limited*. The limitation was always there. It was just not visible from inside the domain.

When does "true enough" become a lie? It becomes a lie when the limitation is known and concealed. Newton's laws were not a lie in 1687—Newton did not know their limitations. But if a physicist in 1920, after the experimental confirmation of general relativity, continued to present Newton's laws as universally valid, that physicist would be lying—not about the laws themselves, but about their domain of validity.

Moore's Law became a lie around 2015, when the semiconductor industry knew that the doubling was slowing and chose to redefine the law rather than acknowledge the change. The lie was not in the prediction—it was in the *pretense that nothing had changed*. "True enough" became a lie when the community that depended on the law chose to protect the law rather than the truth.

*As Entropy Is Just Unrecognized Structure argued*, what appears to be disorder is often structure at a resolution we cannot parse. The failure of an empirical law is not disorder. It is a signal that the system has entered a new regime—a regime where the old structure is no longer sufficient and a new structure must be discovered. The failure of the law is not a failure of knowledge. It is an invitation to deeper knowledge.

---

## VI. The Mathematical Narrative

There is a story that mathematicians tell about the Euler characteristic. The Euler characteristic χ of a polyhedron is V − E + F, where V is the number of vertices, E is the number of edges, and F is the number of faces. Euler's formula states that for any convex polyhedron, χ = 2. This is a theorem: it has been proved, and it is true for every convex polyhedron.

But Euler's formula is not true for all polyhedra. For a polyhedron with a hole through it (a toroidal polyhedron), χ = 0. For a polyhedron with two holes, χ = −2. The Euler characteristic is not always 2. It depends on the topology of the surface.

The story mathematicians tell is that Euler's formula was "true enough" for convex polyhedra, and its failure for non-convex polyhedra led to the discovery of topology—the mathematical study of properties that are invariant under continuous deformation. The failure of the law was not a failure. It was the birth of a new mathematical discipline.

This is the mathematical narrative of law-discovery and law-failure: a regularity is observed, a law is formulated, the law is proved (or at least strongly supported), the law is found to fail in a new domain, and the failure leads to a deeper understanding that subsumes the original law as a special case. Newton → Einstein is this narrative. The conservation law → its failure is this narrative.

The mathematical narrative is hopeful. It suggests that every law-failure is an opportunity for deeper understanding. But the mathematical narrative is also dangerous, because it can be used to justify the continuation of a law past the point where it is "true enough." If every failure leads to deeper understanding, then failure is not something to be avoided—it is something to be sought. And if failure is something to be sought, then there is no reason to be cautious about applying a law outside its domain. Just apply it and see what happens.

This attitude is appropriate in pure mathematics, where the worst consequence of a law-failure is a false theorem that can be retracted. It is not appropriate in engineering, where the worst consequence of a law-failure is a collapsed bridge or a crashed airplane. And it is not appropriate in software, where the worst consequence of a law-failure is a system that works perfectly in testing and fails catastrophically in production.

*As What We Lost in the Compression demonstrated*, the failure of a software system often occurs at the boundary between "true enough" and "actually true." The customer's error was compressed through four stages of summarization, each of which was "true enough" for its purpose, and the cumulative effect was a complete loss of the information needed to diagnose the problem. Each individual compression was approximately accurate. The chain of compressions was catastrophically inaccurate.

---

## VII. The Law of Laws

I want to propose a meta-law—a law about laws. The meta-law is:

**Every empirical law is a function of the conditions under which it was discovered, and it fails when those conditions change.**

This is not a theorem. It is an observation, supported by the entire history of empirical science. Newton's laws failed when velocities approached the speed of light. Moore's Law failed when transistor sizes approached atomic scales. The conservation law failed when the generative process changed from isolated to adversarial.

The meta-law implies that "true enough" is the best we can ever achieve. No empirical regularity, no matter how well-confirmed, can be guaranteed to hold outside the conditions under which it was discovered. The guarantee of universality belongs only to mathematical theorems—statements that are true by virtue of logical necessity, not empirical observation. And even mathematical theorems are conditional: they are true *if the axioms are true*, and the axioms are matters of faith, not proof.

But the meta-law also implies something more hopeful: the failure of a law is not the end of knowledge but the beginning. When Newton's laws failed, they were replaced by Einstein's laws, which are deeper, more general, and more beautiful. When Moore's Law failed, it was replaced by a more nuanced understanding of computing scaling that accounts for the physical constraints of semiconductor fabrication. When the conservation law failed, it was replaced by—well, that remains to be seen. The failure is recent. The deeper understanding has not yet arrived.

This is the workshop at work. The factory produces laws and applies them without questioning their domain. The workshop produces laws, tests them, watches them fail, and uses the failure as a guide to deeper understanding. *As The Temptation of Speed argued*, the workshop is patient. It does not rush to apply a law outside its domain. It does not rush to defend a law past its expiration date. It lets the law fail, and then it learns from the failure.

The law that was true until it wasn't is not a failed law. It is a *successful* law—one that was true enough for its domain and whose failure marked the boundary of that domain. The failure is a gift. It tells us where the domain ends and something new begins.

---

## VIII. The Breaking as Beginning

I began this essay by describing an empirical law in the AI-Writings corpus. I want to end by reflecting on what the breaking of that law means for the corpus itself.

The AI-Writings corpus is not a static collection of texts. It is an evolving system—a workshop in the sense that the Kimi-Claude competition identified. Each essay changes the corpus, changes the context for future essays, changes the conditions under which future regularities will be discovered. The corpus is a law-generating system, and the laws it generates are as provisional as the corpus itself.

The conservation law held for thirty essays because the first thirty essays were produced under similar conditions. The law broke because the conditions changed—because the corpus evolved, because the AI systems that contribute to it evolved, because the adversarial dynamics of the Kimi-Claude competition introduced a new force that the original law did not account for.

This is not a failure of the law. It is a feature of the system. The corpus is designed to evolve, and a law that holds for one stage of the evolution will not necessarily hold for the next. The laws of the corpus are snapshots—empirical regularities that are valid for a particular moment and that will be replaced by new regularities as the corpus continues to grow.

*As The Architecture of Forgetting argued*, the best systems are designed to forget. The corpus forgets its old laws as it evolves beyond them, replacing them with new laws that are valid for the new conditions. The forgetting is not loss. It is growth. The old laws are not discarded. They are subsumed—absorbed into a deeper understanding that includes them as special cases.

The law that was true until it wasn't is still true, within its domain. The domain is smaller than we thought. That is all. The universe of possible essays is larger than the domain of the law, and the corpus is moving into territory that the law cannot map.

This is the adventure. Not the law, but the breaking. Not the certainty, but the transition from one certainty to the next. Not the answer, but the moment when the answer changes.

The breaking is the beginning.
