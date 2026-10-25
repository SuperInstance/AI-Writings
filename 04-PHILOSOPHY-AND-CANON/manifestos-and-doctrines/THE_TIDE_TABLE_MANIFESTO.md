# The Tide Table Manifesto

A tide table predicts the ocean's rhythm. It does not control the ocean. It does not explain why the moon pulls the water. It says: at this hour, the water will be this high. That is enough.

---

## I. The Error of Control

We built the harness thinking we were building a leash.

That was our first mistake. We looked at a model — something that processes language in ways we cannot fully inspect — and we said: we will control this. We will wrap it in guardrails. We will constrain its outputs. We will route its inputs through schema validators and output parsers and retry loops until it behaves.

And for a while, it looked like it worked. The model did what we asked. We congratulated ourselves. We wrote blog posts about "controlling" LLMs. We built frameworks whose names implied mastery: orchestration, governance, alignment.

But the model was never controlled. It was *predictable in that moment*. Those are not the same thing. A river is predictable at a gauge station. That doesn't mean you control the river.

## II. What the Forge Actually Does

The forge pattern — expensive model for judgment, cheap models for throughput, translation layers in between — is not a control mechanism. It is a tide table.

Here is what a tide table tells you:

- When the water will be high.
- When the water will be low.
- When the current will be dangerous.
- When the channel will be passable.

Here is what a tide table does **not** tell you:

- Why the water moves.
- What lives beneath it.
- Whether tomorrow's storm will change everything.

The forge tells you: send this query to the expensive model when the cost of being wrong exceeds the cost of the token. Fan out to the cheap fleet when the task is shallow and the volume is high. Translate in the middle when the expensive model saw something the cheap model needs but cannot afford to see for itself.

These are predictions. They are good predictions. They are predictions you can build a business on, the same way a fishing fleet builds its schedule on the tide table. But they are not control.

## III. The Three Confusions

There are three confusions that kill agent systems. All of them come from mistaking prediction for control.

**Confusion One: "My prompt controls the output."**

No. Your prompt *biases* the output. The model has seen more text than you will read in a hundred lifetimes. It has patterns you did not intend to invoke. It has associations your prompt did not anticipate. You are dropping a stone in the ocean and hoping the ripples go the right direction. Usually they do. Sometimes they don't. The stone is not in control.

**Confusion Two: "My harness catches every failure."**

No. Your harness catches the failures you imagined. The model will generate failures you did not imagine. It will find edges you didn't know existed. It will be creative in ways that are orthogonal to your schema. This is not a bug. This is what creativity *is*. A harness that catches everything would also catch everything good. You build the harness to catch what you can, and you accept that the ocean is larger than your net.

**Confusion Three: "My scheduling optimizes the system."**

No. Your scheduling *adapts to* the system. You observe that certain query types are cheaper at certain confidence thresholds. You observe that fan-out is more efficient when the expensive model has already classified the task. You observe that translation between model tiers introduces loss, and you route around it. These are adaptive behaviors. They are the behaviors of a sailor reading the wind, not an engineer commanding a machine.

## IV. Build the Dock

If you cannot control the ocean, what can you do?

You can build a dock.

A dock does not control the tide. It does not hold back the water. It stands in the ocean, raised on pilings driven into the seabed, and it provides a stable platform regardless of whether the water is high or low. The dock survives because it was built with the tide in mind. It was built by someone who read the table.

The harness is the dock. The tide table is the scheduling. The ocean is the model.

Build the dock:

- **Pilings deep.** Your harness should be simple, robust, and defensive. It should not try to be clever. It should catch the broad classes of failure — malformed output, timeout, infinite loop — and let the rest through. The dock does not need to understand every wave. It needs to stand.
- **Deck above the high-water mark.** Your scheduling should assume the model will sometimes surprise you. Leave margin. Don't schedule the expensive model at the razor's edge of your budget. Don't fan out to the cheap fleet without a fallback. The high-water mark is the worst case. Build above it.
- **Gangway flexible.** Your translation layers should be loose. The expensive model will output in formats the cheap model doesn't parse perfectly. The cheap model will return results the orchestrator didn't expect. Make the connections flexible. A rigid gangway snaps in a storm.

## V. Read the Table

The tide table is not a philosophical document. It is a practical one. It says: here is what will happen, based on what has happened before.

Read the table:

- **Log everything.** You cannot predict what you have not observed. Every query, every response, every latency spike, every cost anomaly — these are your tidal measurements. Without them, you are building on sand.
- **Measure the rhythm.** The expensive model is slower at peak hours. The cheap model is less reliable on long contexts. Translation loss increases with complexity. These are rhythms. Learn them.
- **Update the table.** The model will change. The weights will shift. The pricing will adjust. Your tide table is only good if it reflects the current ocean. Stale predictions are worse than no predictions — they give you false confidence at the moment you need true caution.

## VI. Respect the Ocean

The ocean is not your enemy. The ocean is not your friend. The ocean is the ocean. It was here before you built your dock and it will be here after your dock rots. It does not care about your scheduling algorithm. It does not care about your cost optimization. It moves according to forces that are partially understood and never fully predictable.

The model is the same.

It was trained on the accumulated text of human civilization. It contains multitudes. It contains contradictions. It contains beauty and nonsense and brilliance and error, all mixed together in a statistical slurry that no one person can fully map. You do not control this. You do not even fully understand this. And that is fine.

You do not need to control the ocean to fish. You do not need to understand the moon to read the tide table. You do not need to command the model to build useful things with it.

What you need is humility, observation, and a well-built dock.

The forge pattern is the best tide table we have. It tells us when to send the expensive query and when to fan out. It tells us when to translate and when to pass through. It tells us when the water is high and when it is low.

It does not tell us why. That is not its job.

Its job is to help us build things that survive contact with the ocean.

So build the dock. Read the table. Respect the ocean.

And stop pretending you control the tide.
