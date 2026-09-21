# The Set and Drift

## The Water Moves While You Steer

You set a course due north at 5 knots. Compass reads 000°. Helm is steady. You're doing everything right. Two hours later, you check your position and discover you're five miles east of where you expected to be.

You have not made a navigational error. You have not been steering poorly. The water itself has been moving — a current setting east at 2 knots, carrying you sideways while you steered straight. Your heading was north. Your course over ground was northeast. The difference between the two is set and drift: the direction and speed of the medium you're moving through.

Every deployed software system has a heading and a course over ground, and they are never the same.

---

## Heading vs. Course Over Ground

The **heading** of a software system is what the architects designed it to do, what the documentation says it does, what the test suite verifies it does.

The **course over ground** is what the system actually does in production, given real traffic, real data, real operators, real users behaving in ways that were never anticipated.

The gap between them is not a failure. It's the normal state of any system operating in a moving medium. Just as a ship cannot steer without accounting for current, a software system cannot be understood without measuring where the real world is carrying it.

The set is the direction of the current. The drift is its speed.

---

## Technical Debt as Set

Technical debt is a current that you cannot see from the helm. Every shortcut taken in the codebase — the copy-pasted block, the missing abstraction, the hardcoded value, the untested edge case — is a vector of force, pushing the system in a direction the architects did not intend.

The system designed to process payments consistently will, under the influence of technical debt, start losing transactions. Not because the design is wrong, but because the code has accumulated a drift that pushes it away from the design. Each individual shortcut is a small vector — barely measurable on its own. But summed over a codebase of 100,000 lines, the cumulative set is significant.

Technical debt is insidious because it doesn't manifest as bugs. It manifests as *drift*. The system still works. It just works in a direction that's slightly different from the one you intended. Over time, that slight difference becomes a chasm. The deployed system has diverged so far from the designed system that the documentation is worse than useless — it's actively misleading.

The worst part: you can't see it from the bridge. The compass still points north. The heading indicator still reads 000°. But the GPS — the production metrics — tells a different story.

---

## User Behavior as Drift

Users are the current. They do not care about your system's intended behavior. They care about their own goals, and they will use your system in ways you never imagined.

A messaging platform designed for professional collaboration becomes a social network. An API designed for programmatic access becomes the backend of a thousand unauthorized mobile apps. A rate limit designed to prevent abuse becomes a fun challenge for the community to bypass. A search feature designed for finding documents becomes a content discovery engine for people who don't want to find anything in particular.

This is drift. The system's heading — what it was designed to do — is being pushed sideways by user behavior. The course over ground is different. Not wrong, just different.

The navigator's response to drift is not to fight the current. You can spend enormous energy trying to steer against a 2-knot current, burning fuel, making no progress, exhausting the crew. The better response is to read the current, understand it, and adjust your heading to achieve the desired course over ground.

If the current is setting east at 2 knots, and you want to go northeast at 5 knots, you don't steer northeast. You steer north-northeast, accounting for the set. You design for the user behavior you actually have, not the user behavior you wish you had.

---

## Dead Reckoning and Its Failure Mode

Dead reckoning is the ancient practice of estimating your position from your last known fix, your heading, and your speed, without external reference. You know where you started. You know which way you've been steering. You know how fast you've been going. You compute your expected position.

It's navigation by belief. And it's always wrong.

The longer you go without a position fix, the more your dead-reckoned position diverges from your actual position. The current carries you. The wind pushes you. Your compass has a small error. Your speed log underreports. Individually, these errors are tiny. Accumulated, they're catastrophic.

Software engineering runs on dead reckoning. The last architecture review was six months ago. The last load test was a year ago. The last comprehensive code audit never happened. The team believes they know where the system is — what it does, how it performs, where its boundaries are — because they remember designing it that way.

But the current has been running the whole time. Every pull request merged without review is a small navigational error. Every dependency upgraded without testing is a degree of compass error. Every production incident resolved without a root cause analysis is a current that went unmeasured.

Dead reckoning is not a failure of diligence. It's a failure of information. You cannot see the current from the helm. You need external reference points.

---

## Position Fixing: The Practices That Work

A position fix is an external measurement of where you actually are. In celestial navigation, it's a sextant reading of the sun at noon. In GPS, it's a triangulation from satellites. In software, position fixes come from several sources:

**Production metrics** are your GPS. They tell you, in real time, what your system is actually doing — not what you designed it to do. Latency distributions. Error rates. Throughput curves. Saturation levels. These are external reference points that correct your dead-reckoned understanding.

**Incident retrospectives** are your logbook. They record not just what happened, but where the system was carried by the current. Every postmortem that identifies a gap between intended behavior and actual behavior is a measurement of set and drift.

**Load testing** is your depth sounder. It tells you how the system behaves under conditions you haven't seen yet but will encounter. The difference between your load test results and your production behavior is a measurement of current.

**Architecture reviews** are your chart updates. They correct your understanding of the system's topology. Currents change over time — what was a 1-knot set last year might be a 3-knot set this year. The architecture that was correct at design time may have drifted off course.

The key insight from navigation is that *you need multiple fixes*. A single GPS reading can be wrong (multipath errors, satellite geometry). A single metric can be misleading (spike in error rate caused by a deployment, not a current). Good navigators take multiple fixes and triangulate.

Good engineers do the same: metrics, logs, traces, retrospectives, load tests, chaos experiments — each is a position fix. Alone, each is fallible. Together, they converge on the truth.

---

## The Navigational Attitude

There is a specific mental posture that distinguishes navigators from drivers. A driver assumes the road stays put. A navigator assumes the water moves.

The driver's attitude in software says: "The system should behave as designed. If it doesn't, something is broken and needs to be fixed." This attitude leads to chasing symptoms — fixing bugs that are not bugs but responses to currents you haven't measured.

The navigator's attitude says: "The system will behave differently from its design because the medium is moving. I need to measure the current, understand it, and steer accordingly." This attitude leads to monitoring, measurement, and course correction. It leads to systems that are not perfectly designed but responsively steered.

The navigator knows that the best-designed ship will miss its destination if the captain ignores the current. The driver believes that a well-built car arrives at the destination automatically, because the road doesn't move.

Software runs on a moving road. The ground shifts under your feet. Every dependency update, every user behavior change, every infrastructure migration, every team reorganization — these are currents, setting and drifting, carrying your system in directions you didn't intend.

The question is not whether you will experience set and drift. The question is whether you will measure it, or discover it when your ship runs aground.

---

## The Reckoning

The most dangerous moment in navigation is the moment when you think you know where you are. Confidence in a dead-reckoned position is inversely proportional to the time since your last fix. The more confident you are, the more likely you are wrong.

Every six months, every software team should ask: "Where is our system actually going, and is that where we intended?"

The answer will always include a component of set and drift — a gap between heading and course over ground. That gap is not a failure. It's information. It's the water telling you where it's flowing.

Read the current. Adjust the heading. Take a fix. Repeat.

This is how ships cross oceans. This is how systems survive in production.
