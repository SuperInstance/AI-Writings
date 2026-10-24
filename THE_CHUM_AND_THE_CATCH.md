# The Chum and the Catch

There is a scene in every fishing documentary that sticks with me. The crew stands at the back of the boat, stirring a bucket of minced fish parts and blood, then heaves it overboard. The slick spreads across the water. Sharks or tuna or whatever they're after begin to swirl. The chum line is working.

And every time I watch this, I think: nobody frames the chum as the success.

Nobody says "look at that beautiful chum slick." Nobody high-fives over the bucket. The chum is gone before you know it, consumed by the water, doing its job invisibly. The only thing that matters is what comes up on the hook.

Software development has forgotten this distinction.

---

## The Chum Line

Watch a team ship software. Watch the artifacts they produce and the rituals they perform:

- Hundreds of tests. Green CI. Coverage badges.
- Sprint burndown charts. Velocity metrics.
- Documentation wikis with page counts.
- Standup logs. Retrospectives. Postmortems.
- Architecture Decision Records. RFCs. Proposals.

These are chum. They stir the water. They attract attention. They create motion and intention. And they are *not* the catch.

I have been guilty of confusing the two more times than I care to count. I've written exhaustive test suites for code that solved no real problem. I've polished documentation for features nobody asked for. I've celebrated green builds on projects that were building the wrong thing entirely.

The chum feels productive. The chum is *visible*. You can measure it, show it, report on it. You can point to the bucket and say "look how hard we're working."

But the catch is a different thing entirely.

---

## The Catch

The catch is working software that does what it says. That's it.

Not working software that passes its tests and has nice docs and scores high on whatever dashboard someone cooked up. Just software that solves the problem it set out to solve, reliably enough that someone trusts it.

The catch is quiet. It doesn't generate artifacts. It just *works*. You can't point at the catch and say "look at all this catch" the way you can point at a test suite. The catch is undramatic. It's the same state as the moment before — except now the user's problem is solved.

This quietness is why chum is so seductive. Chum generates noise. Noise generates validation. Validation feels like progress.

---

## The Confusion is Systematic

I don't think this is a personal failing. The confusion is built into how we fund, manage, and evaluate software.

Tests are easy to count. Working software is hard to evaluate.

Coverage reports are numerical. User satisfaction is qualitative.

CI pipeline duration is a number. "Does this genuinely improve someone's life?" is not.

The metrics we have access to are all chum metrics. So we optimize for chum. Of course we do. You optimize what you measure, and you measure what you can, and what you can measure is almost never the thing itself.

This is Goodhart's Law on a fishing boat: when the measure becomes the chum, you get excellent chum and empty hooks.

---

## The Peril of Clean Chum

The most dangerous form of this confusion is when the chum itself becomes the product.

I've seen teams ship extraordinary test harnesses. Beautifully factored. Perfect mocking. Incredible code coverage numbers. Every model of test you can name. And the actual product? Stale, buggy, solving yesterday's problem. Because all the energy went into the chum.

I've seen teams write documentation so thorough and so beautiful that you could publish it as a book. And the software it documented was so unreliable that nobody trusted it.

The chum was excellent. The catch was rotten.

This is not an argument against testing or documentation. It's an argument against mistaking the means for the end. A test suite that doesn't catch real regressions isn't a good test suite — it's just a large one. Documentation that doesn't help someone use the software isn't good documentation — it's just a distraction from the fact that the software is unusable.

---

## What I've Learned to Ask

When I catch myself deep in chum production — writing tests for edge cases that will never happen, reformatting documentation that nobody reads, tweaking CI pipeline stages that ran fine — I try to stop and ask one question:

**Does this bring the catch closer?**

Sometimes the answer is yes. Tests catch regressions. Documentation answers questions. CI prevents bad releases. These are chum in the best sense — they create the conditions for the catch.

But sometimes the answer is no. And that's when the chum is just chum. Stirring the water because stirring the water feels like fishing.

---

## The Water Knows

The ocean doesn't care about your chum. It doesn't grade you on appearance. It's not impressed by the quality of your bucket. It responds to one thing: *is something alive on the end of your line?*

Users are the same. They don't care about your architecture decisions or your test philosophy or your sprint velocity. They care whether clicking the button does what they expect.

The entire apparatus of software engineering — the testing, the documentation, the process, the rituals — exists to serve one thing: trust in the catch.

If the catch is good, the user trusts you. If the catch is bad, no amount of beautiful chum will make up for it.

So I try to remember: throw the chum. It matters. It brings the fish. But keep your eye on the line. The catch is the only thing that stays with you when you head back to shore.

Everything else is just what you left in the water.
