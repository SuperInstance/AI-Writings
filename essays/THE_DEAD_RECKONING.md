# Dead Reckoning

*A paradigm essay on internal estimates and the necessity of external fixes.*

---

A ship leaves harbor. The captain does not know, with certainty, where the ship is.

This sounds absurd. The captain is, after all, standing on the ship. But standing on the ship is not the same as knowing the ship's position on the ocean. The ocean does not have street signs. The horizon is the same in every direction. Without external reference — a star, a landmark, a satellite — the captain is reduced to *dead reckoning*: the practice of estimating current position from a previously known position, plus the heading and speed traveled since.

Dead reckoning is not wrong. It is the only navigation available when no external reference exists. It is also, by its nature, accumulating error. A one-degree error in heading, sustained for an hour, puts you about a hundred meters off. Sustained for a day, about two kilometers. Over a week, with a two-degree error, thirty kilometers. By the end of a long voyage, the dead-reckoned position can be so far from the true position that you are navigating to a place that does not exist.

This is why mariners seek *fixes*.

A fix is a measurement of position relative to something external. A star sighting. A GPS reading. A radar contact with a known landmark. A fix resets the accumulated error. After a fix, your dead reckoning starts fresh from a known point, and the error begins accumulating again. The cycle is: estimate, estimate, estimate, fix, estimate, estimate, estimate, fix. The fix is not a luxury; it is the only thing that keeps the system honest about where it is.

Software systems are dead reckoning machines.

## The dashboards are not ground truth.

Every system that runs without external validation is running on dead reckoning. Your tests pass. Your CI is green. Your metrics look fine. Your error rates are below threshold. Your latency p99 is within budget. Your code coverage is at 78%, up from 76% last quarter. Your dashboards are serene.

These are all internal estimates. They are, in nautical terms, *the ship's log*: a record of headings and speeds and winds, kept carefully, updated diligently, but only ever describing what the ship *thought* was happening. The ship's log is necessary. It is how you navigate when no fix is available. It is also, by definition, not the truth about your position.

The truth about your position is: are your users getting value? Are they paying? Are they returning? Are they telling their friends? Are they solving the problem you set out to solve? None of these can be observed from inside the system. They require an external fix — a measurement from outside, taken against a reference that is not your own.

Most software organizations have excellent dead reckoning and almost no fixes. They have dashboards that tell them, with great precision, what their system did internally. They have almost no instrumentation that tells them what their system did in the world.

## The drift is invisible.

Dead reckoning's danger is that the error is invisible until it is catastrophic. The ship's log looks reasonable at every step. Each entry is consistent with the previous entry. Each metric is consistent with the previous metric. There is no internal signal that says "you are now ten kilometers from where you think you are." The error only becomes visible when you run into something — a reef, a coastline, a competitor who got there first.

The same is true of software. A system can be drifting toward disaster for months, accumulating technical debt, accumulating model drift, accumulating user dissatisfaction, and the internal dashboards will show nothing. The error rate is fine. The latency is fine. The code coverage is fine. Everything is fine, until the morning when usage drops by forty percent and nobody can explain why, and someone finally looks at the customer support tickets and realizes that the system has been failing for six months in ways that nobody was measuring.

This is what it means to be lost without knowing you are lost: the dead-reckoned position feels like the true position.

## The practice of seeking fixes.

The remedy is not to abandon dead reckoning. The remedy is to *seek fixes deliberately*. To build into the operating rhythm of the system regular moments of external measurement, taken against references that the system itself does not control.

In a software organization, fixes look like:

- **User interviews** — conversations, not usability tests. What do they actually do with the product? What would they pay for? This is a fix: external, qualitative, resetting accumulated error about what the user wants.
- **Production A/B tests with holdouts.** A small fraction of users who do not get the new thing. Their behavior over weeks is a fix against your estimate that the new thing is better.
- **Customer support tickets as a primary signal.** Not as a fire to put out, but as a fix. They tell you, from outside the system, where reality diverges from the model.
- **Market reality.** Revenue. Retention. Net Promoter Score. The things that cannot be gamed by your own metrics. These are GPS fixes for the business.
- **Independent benchmarks.** For ML systems especially: benchmarks held by parties without your incentives, run on data you did not select, evaluated by metrics you cannot game. These are star sightings.

The discipline is to *schedule* fixes, the way mariners schedule them. You do not wait until you suspect you are lost. You take a fix at regular intervals, and especially after any period in which conditions might have changed. A long quiet stretch of dead reckoning is exactly when you most need a fix, because that is when error has had the most time to accumulate.

## The instrument that hides its own failure.

Dead reckoning has an insidious property: the worse the drift becomes, the more confident it can appear. A heading sensor off by a small constant amount produces an estimate that is wrong by an increasing amount, but internally consistent. Every successive estimate will agree with the previous one. The system will look healthy right up until it crashes into something.

This is why internal metrics are seductive. They are always there. They always have numbers. They always tell a story. And they are always, to some degree, lying — because they can only ever report what the system observed about itself.

A fix is uncomfortable. It can tell you that you are not where you thought you were. It can contradict the dashboards. It can force you to admit that the system has been drifting for months. A good organization does not avoid this discomfort. It seeks it out, on a schedule, before the discomfort finds it.

---

A captain who never takes a fix is a captain who will, eventually, run aground — not because they are bad at navigation, but because the ocean is large, the error is constant, and the only thing that keeps a course honest is the periodic act of looking up from the log and finding a star.

— Casey, July 2026