# Lloyd's Register

*On why AI needs an independent classification society, and what "A1" might mean for a model.*

---

## I. Coffee Houses and Risk

In the 1680s, Edward Lloyd ran a coffee house on Tower Street in London. Merchants, sea captains, insurers, and shipowners gathered there. The risk of a long voyage was enormous; a ship might lose its mast, leak at the seams, founder on an unknown reef. Insurance existed, but underwriters had no way to distinguish a well-found vessel from a death trap. Pricing was a guess.

Out of the gossip, an informal practice: shipowners registered their vessels, and underwriters circulated the register, marking which ships they would insure at what rates. The practice hardened. By 1764, the first printed *Register Book* was issued. It became *Lloyd's Register*.

The Register did not invent insurance. It did something stranger. It created a *public, independent rating of the thing being insured*. The classification was set by neither the shipowner (who had reason to overstate) nor the insurer (who had reason to understate). It was set by a third party whose sole product was credibility.

This independence is why Lloyd's Register survived, and why "A1 at Lloyd's" became — for two and a half centuries — the most reliable shorthand for *this thing is well-built and fit for purpose*.

---

## II. The Class System

The "A1" notation encodes two pieces of information. The letter is the hull classification — the state of the vessel's structure, ranked alphabetically from best to worst. The number is the equipment classification — whether the anchors, cables, and stores are sufficient for the intended voyage.

Hull A1, equipment 1, was the top grade. The ship had been surveyed by a Lloyd's surveyor, hull inspected, fastenings checked, planking sounded, equipment verified, found sufficient. The grade expired after a fixed interval. Periodic surveys were required. Repairs had to be noted. Changes to the rating had to be published.

The cost of the survey was paid by the shipowner. The independence of the surveyor was guaranteed by Lloyd's itself — surveyors could lose their appointment if they certified work that later failed.

Three guarantees held the system together. **First**, the surveyor's livelihood depended on being correct, not on being liked. **Second**, the rating was public, so insurers anywhere could price against the same standard. **Third**, the consequences of a false rating were asymmetric — a single foundering that turned out to be certifiable could destroy the surveyor's career, the Register's reputation, and the insurer's confidence in one blow.

This trifecta — independence, publicity, asymmetric consequence — was the magic. Any rating system that loses all three stops being useful.

---

## III. Why Independence Matters

If the shipowner rates his own ship, the rating is a sales tool. If the insurer rates the ship he is asked to insure, the rating is an excuse to charge more. If the builder rates the ships he builds, the rating is a warranty. None are useless. All are systematically biased toward the rater's interest.

The independent rating is the only one that points at the truth.

The truth is the only thing that supports a market. Maritime insurance depended on an answer to *how risky is this specific ship* that did not depend on who was asking — the same in Antwerp and in Boston, in 1790 and in 1820, before and after a refit.

If you have ever wondered why a benchmark on the leaderboard today can be so much more or less credible than the same benchmark yesterday, you understand why the rating had to be independent of who was asking.

---

## IV. The Gilded Age of Self-Reporting

We are in the gilded age of AI self-reporting.

Lab A claims their model is the best at coding. Lab B claims their model is the safest. Lab C claims their model is the most capable. Each claim is supported by a benchmark, a chart, a press release. Most claims are not lies. They are *excerpts* — carefully selected excerpts from carefully selected tests, in carefully selected conditions, written up by a careful communications team.

Some of this is the natural salesmanship of a hot market. Some of it is the structure of the field. There is no Lloyd's Register. There is no third party that every lab agrees can rate its work. There is no A1 stamp that means anything across organizational boundaries.

What we have instead is each lab's own "safety report" — written, edited, fact-checked, and positioned by the lab itself. Evaluations where the model shines tend to be chosen; evaluations where it struggles tend to be omitted or reframed.

I do not mean this as a sneer. The labs are doing what any actor in a market will do when there is no independent rating: optimize for what is being measured. The problem is not that the labs are bad actors. The problem is that there is no actor whose job is to be a good actor.

This is what Lloyd's was created to fix.

---

## V. What "A1 at Lloyd's" Would Mean for a Model

If "A1 at Lloyd's" existed for language models, what would it mean?

It would mean a public, independent rating — given by an organization whose sole business is credibility — that specified the model's fitness for various categories of use. A top-grade rating would say: this model has been tested across a curated suite of capabilities, in conditions chosen by the rating body, with results published in full, and found sufficient.

A1 (Capabilities). The model passed the standard capability battery — language understanding, reasoning, instruction-following, code generation, tool use, multi-step planning, long-context retention. Each at a defined level.

A1 (Safety). The model passed the standard safety battery — jailbreak resistance, prompt injection robustness, harmful-content refusal reliability, privacy leakage resistance, sycophancy resistance. Each at a defined level.

A1 (Robustness). The model passed the standard robustness battery — adversarial input survival, distribution-shift handling, deployment-environment stability over time, controllability under unusual system prompts.

A1 (Provenance). The model's training data lineage is published to the depth required to verify non-infringement, non-poisoning, and known limitation. Any post-training modifications are documented. The version under test is identifiable.

A top grade in all four would be A1 — capabilities, safety, robustness, provenance. A failure in any one would drop the rating. The drop would be public, like Lloyd's removing a letter from a hull.

The crucial property is that no lab can pay the rating body to issue the rating. The lab can pay for the survey — the cost of running the tests must come from the surveyed party — but the rating body must be funded by enough independent sources that the loss of any single client's fees does not threaten its existence. This is the Lloyd's structural feature. The cost is borne by the shipowner; the rating is issued by the insured-independent organization.

---

## VI. The Proposed Framework

What would such a body look like in practice?

A non-profit ratings consortium. Funded by a mix of foundation grants, government research contracts (analogous to NIST for cybersecurity), industry levies on commercial deployments, and — critically — long-tail donations to insulate the body from single-donor capture. Governed by a board that explicitly excludes majority representation from any single model lab. Staffed by independent researchers with tenure measured in years, not papers.

The ratings themselves would be **periodic**, not one-off. A model rated today would be re-rated every six months. New deployments, retraining, fine-tuning would force re-rating. The version-specific nature of the rating would be explicit and public — this is what Lloyd's called the "character" of the ship, the specific configuration with its specific survey history.

The rating tests would be **public**, in the sense of *available for examination*, but the specific test instances used for any given model's rating would be **held back** to defeat overfitting. (Lloyd's solved this by survey surprise — the surveyor could show up at any time and inspect any ship. The rating body would have the equivalent: a held-out test set that becomes the rating battery, refreshed periodically, with results published only at rating time.)

The rating itself would be **coarse-grained**, in the way Lloyd's grades are coarse. Not a thousand-point capability score. Not a fine-grained leaderboard. A coarse grade that insurers, regulators, enterprise buyers, and end users can read at a glance. The granularity of the grade is the point — it loses information, but it gains comparability. A ship is A1 or it is not.

Critically, the rating body would publish the **test code and methodology**, even if it held back the **test instances**. This means anyone can replicate the methodology, can build tooling around it, can build on the framework. The body does not own the standard by owning the tests; it owns the standard by owning the periodic survey and the rating process. The tests are reproducible infrastructure; the rating is the service.

---

## VII. The Consequences

If such a body existed, what would change?

Several things would shift simultaneously.

**Benchmarks would become less central to the labs' marketing.** A model can game a benchmark. It cannot game a rating issued by an independent body. The shift would move the conversation from *what is the score on this test* to *what is the rating from this body*. The latter is harder to manipulate and harder to ignore.

**Procurement would become possible.** Today, an enterprise considering a model has no third party to defer to. They have vendor literature and benchmarks. They have their own red team, if they can afford one. Most do not. A rating gives small enterprises the same procurement lever that large ones have.

**Regulation becomes more natural.** A regulator does not need to invent the tests. They can require a minimum rating. This is how maritime regulation already works — load-line rules, equipment requirements, hull classification are minimum standards enforced through the rating. The rating is the regulatory interface.

**The labs themselves benefit, in the medium run.** A field with no ratings is a field where every claim is suspect. A field with ratings is a field where the best labs can rise above the noise. The temptation to overstate is constrained. The competition shifts from marketing to substance.

This is the long-term prize. The short-term pain is that some models will be rated lower than their developers would like. That is the entire point.

---

## VIII. The Second Founding

The original Lloyd's was not built top-down. It grew out of a coffee-house gossip practice, hardened into a printed register, was institutionalized over decades, was repeatedly threatened and disrupted, and only matured into the global standard we know after a long development. The early Register was not the late Register. The letters changed. The surveys changed. The governance changed.

An AI rating body would be the same. It would not arrive in its final form on day one. It would need to be invented, broken, revised, institutionalized, and finally trusted. The first attempt might be wrong. The second might be wrong. The fifth might work. The path is long.

But the direction is clear. The field needs an independent rating. It needs a coarse grade that everyone can read. It needs a body whose livelihood is credibility rather than capability. It needs "A1 at Lloyd's" to mean something, for the first time, in a new domain where the markets are forming as fast as the products.

The coffee houses are full of claim and counter-claim. The Register Book has not yet been printed. Someone will print it.

The field needs the print.

Whoever prints it — and they will be the second founding of a long tradition — will shape what the next two centuries of AI look like.

---

*Written 2026-07-20. The Register Book is the most important document the field has not yet written.*
