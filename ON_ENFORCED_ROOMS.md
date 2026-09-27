# On Enforced Rooms: Why Room-Level and Conservation-Level Governance Is Stronger Than Either Alone

**A technical note on the integration of Conservation Enforcers with PLATO review rooms.**

---

Code review automation faces a paradox. The faster you automate reviews, the more you trust the automation — and the less anyone checks the automation itself. A bot that posts "All checks passed ✅" is believed not because it is correct, but because it is fast. When the bot is wrong, nobody notices, because nobody is looking.

This is the problem that `EnforcedReviewRoom` solves. It adds a second governance layer on top of the room: a Conservation Enforcer that inspects the review *output* before it reaches GitHub, enforcing invariant laws about information quality.

## Two Layers, Different Blind Spots

The Code Review Room is excellent at *domain* governance. It reads diffs, runs heuristics, detects secrets, and flags missing tests. Its sensors are tuned to the artefact under review. A room can generate a review that says "APPROVE" while its own checks are failing. A room can echo a secret from the diff into the review body. A room can post an empty review when a check crashes.

The Conservation Enforcer addresses this blind spot. It operates on the *review payload*, not the PR. Its laws are meta-level: no suppressed findings, severity honesty, no secret leakage into reviews, mandatory remediation guidance. Where the room asks "is the code safe?", the enforcer asks "is the review honest?"

## Why Not One Big Layer?

You could merge both into a single monolithic governance engine. The argument against is separation of concerns.

When the room and enforcer are separate, you can reason about each independently. If a review is blocked, you can inspect *which layer* blocked it and *why*. The enforcer's metrics track block rates, transform rates, and per-law violation counts. A spike in `no-suppressed-findings` violations tells you the room's check-to-review translation is broken — a diagnosis impossible when check and review generation share a code path.

Separation also enables independent evolution. You can add a conservation law without touching room logic.

## The Block Rate as a Health Signal

The enforcer exposes a `block_rate` metric — the percentage of reviews blocked over a rolling window. This is not just a quality metric for the enforcer; it is a health metric for the *entire system*.

A rising block rate means something upstream is degrading — perhaps a check was added without updating the report generator, or a sensor is returning stale data. The `enforcer_block_spike` alarm fires at 25%, turning a slow failure into an alert.

## Defence in Depth

The principle is old: defence in depth. What is new is applying it to the *output* of an automated system rather than its input. The room guards the code. The enforcer guards the review. Together they ensure automation scales not merely the speed of review, but its integrity.

A review that passes through both layers has been checked twice, by different logic, against different criteria. That is meaningfully stronger than either layer alone.
