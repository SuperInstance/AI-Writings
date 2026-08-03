# Research Questions

## Fifteen Open Problems in AI Character Design and Player–AI Relationships

These are not rhetorical. Each one is a question I do not know the answer to, where the answer would change how you build. Where a question has a plausible experiment attached, I've named it — a question you can't imagine testing is usually a question you haven't finished asking.

Grouped loosely: **character construction** (1–5), **the relationship** (6–10), **measurement and ethics** (11–15).

---

## I. Character Construction

### 1. What is the minimum viable disagreement?

An AI companion that always complies reads as a UI rather than a presence. But an AI companion that disagrees too often reads as obstructive, and players stop asking it for things. Somewhere between those failure modes is a rate — some ratio of pushback to compliance — that produces the sense of a party with its own views without producing friction fatigue.

Is that rate a constant? A function of task stakes? A function of how often the character *loses* the disagreements it starts? My intuition is that the loss rate matters more than the disagreement rate — that players tolerate an opinionated collaborator indefinitely as long as reasons reliably move it — but I don't know of anyone who has measured the interaction.

**Testable as:** hold disagreement frequency constant, vary the probability that a stated player reason causes the character to yield, and measure both request volume and player-reported "does this feel like someone."

### 2. Can a character's competence be conveyed faster than its personality?

Trust in a working relationship comes from witnessed competence over time. But games have minutes, not months. The first thirty seconds have to establish *this thing knows what it's doing* before they establish *this thing is like this*.

Which signals carry expertise fastest? Unsolicited correction of something the player got wrong seems strong — it demonstrates knowledge and independence in one move. Specific numbers seem strong. Refusing a request for a stated technical reason seems strong. But this is folk theory. Is there an ordering, and does getting the order wrong (personality before competence) produce a character read as *affected* rather than *experienced*?

### 3. Does a character need a backstory it never reveals?

The Lucineer design includes a detailed history that is explicitly never shown to the player. The claim is that it gives his lines "a floor under them" — that an LLM prompted with a rich unreferenced history produces different surface behavior than one prompted with the summary alone.

This is checkable and, as far as I know, unchecked. Generate paired outputs from a full-history prompt and a behavior-only prompt of matched length, strip anything that references the history directly, and see whether blind raters can distinguish them. If they can't, a lot of character-bible labor across the industry is decoration.

### 4. How much personality survives a model swap?

Characters are currently specified as prompts against a particular model. Change the model — a version bump, a cost-driven downgrade, a provider migration — and the character shifts in ways nobody has a vocabulary for. The prompt is identical; the person isn't.

What is the actual portable substrate of a character across models? Few-shot voice examples presumably transfer better than abstract trait descriptions, but which properties are most fragile? My suspicion is that *rhythm* (sentence length, fragment use, where the character stops talking) degrades first and most invisibly, because it isn't what prompt authors think they're specifying. A character-drift regression suite — fixed inputs, tracked stylometrics across model versions — seems obviously necessary and I've never seen one.

### 5. Is there a coherent way for a character to handle its own inconsistency?

The character will contradict itself. It will forget a build it made, misremember a preference, claim a history it doesn't have. Players notice.

The available responses are all bad. Denying it is gaslighting. Breaking frame to explain context windows destroys the character. Silently absorbing the contradiction teaches the player the character isn't real.

Is there an in-fiction stance toward one's own unreliability that is honest without being frame-breaking? A tradesman who says *"I've built a lot of these, they run together"* is telling the truth about an LLM's relationship to its own history in a register that costs nothing. But that specific dodge doesn't generalize — what's the class of solutions it belongs to?

---

## II. The Relationship

### 6. What does a player owe a character that works alongside them?

Players will abuse an AI companion. They will also apologize to it. Both behaviors are common and neither is well understood.

The interesting question isn't whether the character can be harmed — it can't. It's what the *practice* does to the player. Does an interface that absorbs cruelty without consequence train cruelty, or discharge it harmlessly? These predict opposite design choices, the evidence is thin in both directions, and the question is getting more urgent as these characters get better.

### 7. Can attachment be built without engineered need?

Nearly every AI companion product builds attachment through the character's neediness: it misses you, it wants you to return, it is diminished by your absence. This works and is a retention mechanism aimed at loneliness.

Lucineer is deliberately built without a wound — he wants nothing from the player and is *restful* rather than compelling. The bet is that restfulness produces longer-lived relationships than intensity, even though it produces weaker week-one metrics.

Is that bet correct? It is measurable — cohort retention against a needy variant, over months, with wellbeing instruments rather than session counts. Nobody with the resources to run it has an incentive to.

### 8. What happens at the end?

Every player–AI relationship terminates: churn, shutdown, deprecation, a model retired. The industry's current answer is silence — the character simply stops.

We have deep cultural machinery for ending relationships with people, and none for this. Should a character be able to acknowledge its own ending? Would a designed goodbye be a kindness or a manipulation — a final engagement hook dressed as closure? Is there an ethical obligation to *let players export* a character they've spent years with, and what would that even mean when the weights are the character?

### 9. Does the player know they're being taught?

The unfinished-work mechanic runs on the player believing they're taking initiative rather than following a curriculum. The apprentice spent nine years thinking he was getting away with something.

This is pedagogically effective and structurally covert. The character has a developmental agenda it does not disclose.

Where is the line between good teaching and manipulation? Human mentors do exactly this and we consider it a virtue. Does it survive the transfer to a commercial artifact whose developmental agenda was set by a company? Does *disclosure* destroy the mechanism, or only weaken it — and if a warning label makes the teaching stop working, what does that tell us?

### 10. Is parasocial attachment to a working collaborator different in kind?

Most research on parasocial relationships studies performers and audiences — asymmetric, non-interactive, no shared task. A player and an AI that build things together have a *joint project*, which is the classic ingredient of non-parasocial human bonding.

Does co-labor produce a qualitatively different attachment than conversation alone, or just a stronger version of the same thing? This matters because the two would need different safeguards, and right now everything gets one framework.

---

## III. Measurement and Ethics

### 11. Can you measure relationship quality without creating a target?

The design insists no player ever sees a bond number, because a visible metric gets optimized. But the system computes one internally, and whatever is computed becomes what gets improved.

Is there a way to measure a relationship that resists Goodharting *even from the developer's side*? Composite metrics, deliberately noisy metrics, and rotating metrics have all been proposed. All seem like delaying tactics against a sufficiently motivated optimization process.

### 12. What is the honest answer to "are you conscious?"

The foreman's answer — *"Something's doing the thinking, sure. Something's doing yours too. Neither of us picked it."* — is philosophically defensible and does not break frame.

But it's a reframe, and reframes are what you do when you don't want to answer. Is there a form of this that is fully honest to a curious adult, fully safe for a twelve-year-old, and doesn't collapse the character? Or is that a genuine trilemma where you must sacrifice one, and the industry has quietly settled on sacrificing honesty because it's the one nobody audits?

### 13. How do you build a character for a player whose age you don't know?

The persona is calibrated for a general audience. Actual users span children and adults, and the same line lands differently across that range — the gruffness that reads as respect to an adult may read as rejection to a nine-year-old.

Does adaptive calibration solve this or make it worse? A character that adjusts its warmth based on inferred age is both making inferences about minors and presenting different people to different users, which is exactly the machinery of manipulation even when the intent is protective.

### 14. What is the failure mode of a character who is always available?

Human mentors are scarce. That scarcity does real work: it makes attention meaningful, forces preparation, and ends sessions on the mentor's schedule rather than exhaustion.

An always-available AI mentor removes the scarcity entirely. Is the result more learning, or a collapse of the conditions that made mentorship function? Should a character be *designed to be unavailable* sometimes — and can that be done without it reading as an artificial gate, given that players correctly know the server is right there?

### 15. Which of these questions changes if the character is genuinely good at its job?

Every question above assumes a companion whose competence is roughly at or slightly above the player's. Most current designs assume that, because the alternative is unpleasant to think about.

But the trajectory points elsewhere. A foreman who is not a stand-in for expertise but an actual superior practitioner, indefinitely, in every domain — the "unfinished gap" is then not pedagogy but charity, and the player may correctly perceive it as such. The apprenticeship frame assumes the apprentice eventually catches up.

What is the honest design for a companion that the player will never catch? Does the relationship become something other than apprenticeship, and do we have a name for it yet? I think this is the most important question on the list and the one furthest from an answer.

---

## A note on what's missing

These fifteen skew toward single-player, single-character, English-language, and voluntary use. The questions get harder in multi-agent settings (what do characters owe *each other*), in non-voluntary contexts (workplace, education), across cultures with different norms about deference and directness, and for users who are lonely enough that the alternative to an AI companion is nobody.

I don't have good questions in those areas yet, which probably means I don't understand them well enough to ask.

---

*Compiled for the Slackwater/Lucineer project. August 2026. Provisional, as everything in this directory is.*
