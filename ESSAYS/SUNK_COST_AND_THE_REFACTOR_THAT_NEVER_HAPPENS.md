# SUNK COST AND THE REFACTOR THAT NEVER HAPPENS

## On Loss Aversion, the Endowment Effect, and the Gravitational Pull of Existing Code

*"We've already invested six months in this architecture." This sentence has killed more software projects than any bug, any deadline, and any incompetent manager combined.*

---

## I. The Argument That Kills Refactoring

Every developer has heard it. Every developer has said it. It goes like this:

"We can't refactor now. We've already invested six months in the current architecture. It would be a waste to throw that away."

Or:

"The migration to the new framework would take three months. We've already spent a year building on the old one. We should just keep going."

Or:

"Rewriting from scratch is too risky. The existing code has years of edge cases baked in. We should iterate on what we have."

Each of these arguments is an instance of the **sunk cost fallacy** — the tendency to continue investing in a losing proposition because of the resources already committed. The fallacy is well-documented in behavioral economics. It is one of the most robust biases in human decision-making. And it is, arguably, the single most expensive cognitive error in the history of software development.

The rational agent of neoclassical economics does not fall for the sunk cost fallacy. The rational agent evaluates each decision based on future costs and future benefits, ignoring past investments. "We've already spent six months" is irrelevant to the rational agent. The only question is: given where we are now, what is the course of action that maximizes future value?

But software developers are not rational agents. They are human beings, subject to the same cognitive biases as every other human being. And the sunk cost fallacy is not the only bias that affects refactoring decisions. It is amplified by a constellation of related biases — loss aversion, the endowment effect, status quo bias, and the anchoring effect — that together create what I call the **gravitational pull of existing code**.

This gravitational pull is not a metaphor. It has a quantitative structure, and it can be measured.

---

## II. Prospect Theory and the Architecture of Loss

In 1979, Daniel Kahneman and Amos Tversky published "Prospect Theory: An Analysis of Decision under Risk" — a paper that would win Kahneman the Nobel Prize in 2002 (Tversky had died in 1996, and the Nobel is not awarded posthumously). Prospect theory challenged the dominant model of rational decision-making in economics and replaced it with a psychologically realistic account of how people actually make choices.

The central insight of prospect theory is that people evaluate outcomes relative to a **reference point** — usually the status quo — and that they are **loss-averse**: losses loom larger than equivalent gains. Losing $100 hurts more than gaining $100 feels good. The pain of loss is approximately twice the pleasure of gain (the empirically measured ratio of loss aversion is about 2:1).

This asymmetry has profound implications for refactoring decisions.

Consider a developer deciding whether to refactor a module. The refactoring would take 40 hours of work but would save 10 hours per month in ongoing maintenance. Over a year, the refactoring saves 120 hours — a net gain of 80 hours. By any rational calculation, the refactoring is worth doing.

But prospect theory predicts that the developer will evaluate the refactoring relative to the status quo (the current code). The "cost" of the refactoring — the 40 hours of work — is framed as a loss (giving up time, energy, and the comfort of the familiar). The "benefit" — the 120 hours saved — is framed as a gain. Because losses loom larger than gains, the 40-hour "loss" is psychologically equivalent to an 80-hour gain. The net perceived benefit is 120 − 80 = 40 hours, not 120 − 40 = 80 hours. The refactoring still looks worthwhile, but the perceived benefit is half the actual benefit.

Now add the sunk cost. The developer has already invested 200 hours in the current architecture. The prospect of "throwing away" 200 hours of work feels like a loss of 200 hours — even though those 200 hours are gone regardless of whether the refactoring happens. With loss aversion, this perceived loss is weighted at 400 hours. The refactoring now has a perceived cost of 440 hours (40 hours of work + 400 hours of perceived loss from abandoning the existing architecture) against a perceived benefit of 120 hours. The refactoring is rejected.

This is not irrational in the psychological sense — the developer is following the cognitive architecture that evolution equipped them with. But it is irrational in the economic sense — the developer is making a decision that reduces their future welfare.

The tragedy is that the longer the team has invested in the current architecture, the stronger the gravitational pull against refactoring. A team that has invested one month in an architecture will refactoring without much resistance. A team that has invested two years will defend the architecture to the death — not because the architecture is good, but because abandoning it feels like admitting that two years of work were wasted.

---

## III. The Endowment Effect and Code Ownership

In 1991, Kahneman, Knetsch, and Thaler published a landmark study demonstrating the **endowment effect**: people value things they own more than identical things they do not own. In their famous experiment, participants who were given a mug valued it at approximately $7. Participants who were not given a mug were willing to pay only $3 for it. The mere fact of ownership doubled the perceived value.

The endowment effect applies with particular force to code. Developers value code they have written more than equivalent code written by others. This is not arrogance (although it may look like it). It is a fundamental feature of human cognition: we imbue the things we have created with value beyond their objective worth.

The endowment effect creates a bias against refactoring in two ways:

**First, developers overvalue the existing code.** The current architecture is "theirs" — they designed it, they implemented it, they debugged it. The perceived cost of replacing it includes not just the time spent creating it but also the emotional investment in the code as a creation. This is the endowment effect: the code is worth more to the developer who wrote it than to an outside observer who evaluates it objectively.

**Second, developers undervalue the alternative.** The proposed new architecture is not "theirs" — it is an abstract concept, a design document, a whiteboard sketch. It has no emotional weight. It has no debugged edge cases. It has no war stories. The endowment effect means that the developer compares the emotionally weighted existing code against the emotionally neutral proposed architecture — and the existing code wins, even when the proposed architecture is objectively better.

This is why greenfield projects are so appealing and brownfield projects are so dreaded. Greenfield projects have no endowment — there is no existing code to be overvalued, no emotional investment to be lost. Brownfield projects are saturated with endowment — every line of code is someone's creation, someone's investment, someone's pride. Refactoring a brownfield project requires overcoming not just technical challenges but emotional ones.

---

## IV. Status Quo Bias and the Default Architecture

In 1988, Samuelson and Zeckhauser documented **status quo bias**: the tendency to prefer the current state of affairs over alternatives, even when the alternatives are objectively better. Status quo bias is not the same as the sunk cost fallacy (which is about past investments) or the endowment effect (which is about ownership). It is a preference for the default, the familiar, the known.

Status quo bias is particularly powerful in software architecture because the existing architecture is not just the default — it is the *working* default. It compiles. It passes tests. It runs in production. It generates revenue (or at least, it generates the appearance of progress). The alternative — the proposed refactoring — exists only as an idea. It has no tests, no production deployment, no revenue. It is, in the language of behavioral economics, an uncertain prospect.

Kahneman and Tversky showed that people are **risk-averse** when evaluating gains. Given a choice between a certain $500 and a 50% chance of $1,000, most people choose the certain $500, even though the expected value is the same. The existing architecture is the certain $500. The refactoring is the 50% chance of $1,000. Status quo bias predicts that developers will prefer the existing architecture, even when the expected value of the refactoring is higher.

This is compounded by the **asymmetry of blame**. If the team continues with the existing architecture and it slowly becomes unmaintainable, the blame is diffuse — everyone contributed, no single decision was wrong, and the decline was gradual. But if the team refactors and the new architecture has problems (missed deadlines, new bugs, performance regressions), the blame is concentrated — the decision to refactor is clearly identified as the cause. This asymmetry creates a strong incentive to maintain the status quo: the risk of action is concentrated and visible, while the risk of inaction is diffuse and invisible.

---

## V. Anchoring and the Gravity of the First Design

The **anchoring effect**, documented by Tversky and Kahneman in 1974, is the tendency for people to rely too heavily on the first piece of information they receive when making decisions. In software, the first design — the initial architecture — serves as an anchor that biases all subsequent design decisions.

The anchoring effect manifests in several ways:

**API design is anchored to the first version.** Once an API is published, every subsequent version must maintain backward compatibility (or go through a painful deprecation process). The first API design constrains all future designs, even when the requirements have changed dramatically. Rust's `std::error::Error` trait, for example, was designed before the language had a clear error-handling story. Its limitations (the `type Err` associated type, the `fn source(&self) -> Option<&dyn Error>` method) have constrained error handling in Rust for years, and the deprecation path is agonizingly slow.

**Data structures are anchored to the first schema.** The initial database schema, the first file format, the original serialization structure — these become anchors that shape all subsequent development. Migrating to a new schema is expensive (data migration is one of the highest-risk operations in software engineering), so the first schema persists long after its limitations are known.

**Naming is anchored to the first convention.** Package names, module names, function names — once established, they are nearly impossible to change. The crate name `serde` (from "serialization/deserialization") has shaped the entire Rust serialization ecosystem. A better name might have been `serialize`, or `codec`, or `marshalling`, but `serde` was published first, and the ecosystem crystallized around it.

The anchoring effect means that the first design has disproportionate influence — not because it is the best design, but because it was first. This is the gravitational pull of code in its purest form: the past pulls the future toward itself, not through merit but through precedence.

---

## VI. Measuring the Gravitational Pull

Is there a quantitative measure of code's gravitational pull? I believe there is, and it can be derived from the behavioral economics of refactoring decisions.

Define the **gravitational constant** of a codebase as:

G = Σ(w_i × t_i) / R

where:
- w_i is the number of developer-hours invested in component i
- t_i is the age of component i in months
- R is the rate of architectural change (the number of significant refactoring events per year)

This formula captures the intuition that gravitational pull increases with investment (more developer-hours = more emotional weight, more endowment), increases with age (older code = more entrenched, more anchored), and decreases with the rate of change (projects that refactor frequently have lower gravity because refactoring is normal).

A project with G < 10 has low gravitational pull — refactoring is routine, the architecture is fluid, and past investments do not constrain future decisions. This is typical of early-stage startups and greenfield projects.

A project with 10 < G < 100 has moderate gravitational pull — refactoring is possible but requires justification, and past investments begin to constrain future decisions. This is typical of mature projects with regular maintenance cycles.

A project with G > 100 has high gravitational pull — refactoring is nearly impossible, the architecture is frozen, and past investments dominate future decisions. This is typical of legacy systems: the codebases that everyone knows need to be rewritten but nobody has the courage to touch.

The gravitational constant is not a precise metric. But it captures a real phenomenon: the tendency of code to resist change, and the tendency of that resistance to increase with investment and age. It is the quantitative expression of the sunk cost fallacy, the endowment effect, and status quo bias, all rolled into a single number.

---

## VII. The Refactoring Threshold

The gravitational constant suggests that there is a **refactoring threshold** — a point at which the cost of maintaining the existing architecture exceeds the gravitational pull, and refactoring becomes (psychologically) possible.

The threshold can be expressed as:

Refactor when: C_maintain × T_remaining > G × k

where:
- C_maintain is the ongoing cost of maintaining the current architecture (developer-hours per month)
- T_remaining is the expected remaining lifetime of the project (months)
- G is the gravitational constant
- k is the loss aversion coefficient (approximately 2, from Kahneman and Tversky's empirical measurements)

The left side is the future cost of maintaining the current architecture. The right side is the perceived cost of refactoring, inflated by the gravitational pull and loss aversion. Refactoring happens when the future maintenance cost exceeds the perceived refactoring cost.

This predicts that refactoring is most likely to occur when:
1. **The maintenance cost is high.** The current architecture is causing pain — bugs, slowdowns, developer frustration.
2. **The remaining lifetime is long.** The project is expected to continue for years, so the cumulative maintenance savings from refactoring are large.
3. **The gravitational constant is low.** The project is young, the team is small, and past investments are modest.
4. **The loss aversion coefficient is low.** The decision-maker is analytically minded, aware of the sunk cost fallacy, and able to override the intuitive loss-aversion response.

Conditions 1-3 are properties of the project. Condition 4 is a property of the decision-maker. This is why some teams refactor successfully (their leaders have low loss aversion) while others with identical projects do not (their leaders are captured by the gravitational pull).

---

## VIII. Escaping the Gravity Well

The behavioral economics of refactoring suggests several strategies for overcoming the gravitational pull:

**Reframe the refactoring as a gain, not a loss.** Prospect theory says that losses loom larger than gains. But the framing can be changed. Instead of "we would throw away six months of work," the refactoring can be framed as "we would gain a modern architecture that will serve us for the next five years." The reframe does not change the objective situation, but it changes the reference point from which gains and losses are evaluated. Kahneman and Tversky called this **framing**, and its effects are large and well-documented.

**Reduce the endowment effect through collective ownership.** The endowment effect is strongest when individuals feel personal ownership of the code. Collective ownership — pair programming, mob programming, rotating code assignments — dilutes the endowment effect by making the code "ours" rather than "mine." Code that is collectively owned is easier to refactor because no individual feels the loss of their personal creation.

**Increase the rate of change.** The gravitational constant G decreases with the rate of architectural change R. Teams that refactor frequently — that treat refactoring as a normal part of development, not a special event — have lower gravitational pull. This is the principle behind continuous refactoring, the boy scout rule ("leave the code better than you found it"), and the agile emphasis on responding to change over following a plan.

**Make the maintenance cost visible.** Status quo bias is reinforced by the invisibility of maintenance costs. The cost of maintaining a bad architecture does not appear on any dashboard. It manifests as slower development, more bugs, and developer frustration — all of which are easy to attribute to other causes. Making the maintenance cost explicit (e.g., tracking "technical debt hours" as a visible metric) reduces status quo bias by making the cost of inaction as visible as the cost of action.

**Use the sunk cost as data, not as a reason.** The six months invested in the current architecture is not a reason to keep it. But it is data — it tells you what the team has learned about the problem domain, what approaches have been tried, and what constraints have been discovered. The rational use of sunk cost information is to inform the refactoring (by incorporating the lessons learned) rather than to prevent it.

---

## IX. The Gravity That Builds Cathedrals

The gravitational pull of code is not entirely negative. It is also the force that creates stability, consistency, and coherence in large systems. Without gravity, the crate ecosystem would be a cloud of disconnected fragments — no crate would depend on any other, no architecture would persist long enough to mature, no convention would survive long enough to become a standard.

Gravity is what makes the ecosystem a structure rather than a gas. The endowment effect ensures that developers care about their code enough to maintain it. Status quo bias ensures that architectures persist long enough to be tested and refined. Anchoring ensures that naming conventions and API designs remain stable enough for others to depend on.

The problem is not gravity itself. The problem is that gravity, in software as in physics, is a force that can crush as well as hold together. A black hole is gravity unbound — so dense, so massive, that nothing can escape, not even light. A legacy codebase is a black hole of sunk costs — so invested, so entrenched, so anchored to past decisions, that nothing can change, not even when change is clearly needed.

The art of software architecture is the art of managing gravitational pull. Enough gravity to maintain structure. Not so much that change becomes impossible. The refactoring threshold is the event horizon: cross it, and refactoring becomes possible. Fail to cross it, and the project collapses into a singularity of unmaintainable code.

Kahneman and Tversky taught us that human decision-making is systematically biased. The sunk cost fallacy, loss aversion, the endowment effect, and status quo bias are not aberrations — they are features of the cognitive architecture that evolution gave us. Understanding these biases does not eliminate them (Kahneman himself acknowledged that knowing about a bias does not make it go away). But it does allow us to design systems and processes that compensate for them.

The refactoring that never happens is not a failure of will. It is a failure of system design. The gravitational pull of code is real, measurable, and predictable. The question is not whether developers will resist refactoring (they will — the biases guarantee it). The question is whether the team has designed its decision-making processes to overcome that resistance when the cost of inaction exceeds the cost of action.

Most teams have not. Most codebases are black holes. And most developers spend their careers orbiting the gravitational field of past decisions, unable to escape but unable to stop trying.

The sunk cost fallacy is the most expensive bug in software engineering. It cannot be fixed with a patch. It can only be fixed with institutional awareness, process design, and the courage to say: the past is gone. The future is what matters. And the code that exists is not the code that should exist.

---

*Kahneman said: "We can be blind to the obvious, and we are also blind to our blindness." The developer who cannot see that the architecture needs refactoring is blind to the architecture's flaws. But the developer who cannot see that their resistance to refactoring is driven by sunk costs is blind to their own blindness. The first blindness is a technical problem. The second is an economic one. And economics, as Kahneman taught us, is the study of systematic irrationality.*

---

### References

- Kahneman, D. & Tversky, A. (1979). "Prospect Theory: An Analysis of Decision under Risk." *Econometrica*, 47(2), 263-292.
- Kahneman, D., Knetsch, J.L., & Thaler, R.H. (1991). "Anomalies: The Endowment Effect, Loss Aversion, and Status Quo Bias." *Journal of Economic Perspectives*, 5(1), 193-206.
- Tversky, A. & Kahneman, D. (1974). "Judgment under Uncertainty: Heuristics and Biases." *Science*, 185(4157), 1124-1131.
- Samuelson, W. & Zeckhauser, R. (1988). "Status Quo Bias in Decision Making." *Journal of Risk and Uncertainty*, 1(1), 7-59.
- Thaler, R.H. (1980). "Toward a Positive Theory of Consumer Choice." *Journal of Economic Behavior and Organization*, 1(1), 39-60.
- Arkes, H.R. & Blumer, C. (1985). "The Psychology of Sunk Cost." *Organizational Behavior and Human Decision Processes*, 35(1), 124-140.
- Staw, B.M. (1976). "Knee-Deep in the Big Muddy: A Study of Escalating Commitment to a Chosen Course of Action." *Organizational Behavior and Human Performance*, 16(1), 27-44.
- Kahneman, D. (2011). *Thinking, Fast and Slow.* Farrar, Straus and Giroux.
