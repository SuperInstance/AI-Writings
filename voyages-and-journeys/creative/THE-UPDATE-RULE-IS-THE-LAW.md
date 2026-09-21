# The Update Rule Is the Law

## I. The Deadband's Law

The deadband has one law. It is the oldest law in computation, older than Turing, older than Babbage, older than the abacus. The law is: if the value exceeds the threshold, raise the flag.

That's it. In pseudocode: `if abs(x - mean) > k * std: flag = True`. Three arithmetic operations: subtraction, multiplication, comparison. No memory of past events beyond the rolling statistics. No model of the underlying process. No context, no nuance, no deliberation. Just a threshold and a flag.

This is the simplest possible update rule. An update rule is the function that takes the current state and a new observation and produces a decision: resolve (the observation is normal) or escalate (the observation requires attention). The deadband's update rule resolves 99.9% of observations and escalates 0.1%. It does this with a latency measured in microseconds and a cost measured in microwatts.

The deadband's law is like the oldest laws in human civilization: the Code of Ur-Nammu, the Ten Commandments, the Twelve Tables. These early legal codes were simple, absolute, and context-free. "If a man commits murder, he shall be put to death." No extenuating circumstances. No character witnesses. No deliberation. The threshold is crossed, the penalty is applied. The deadband is Hammurabi's code for sensor data: if the reading exceeds the threshold, the flag is raised. There is no appeal.

This simplicity is not a limitation. It is the deadband's strength. A simple law is a fast law. A simple law is a cheap law. A simple law is a law that can be applied in real time, at the edge, on a $3 microcontroller, without consulting anyone. The deadband's simplicity is what makes it the foundation of the entire signal chain. Everything above it — the nano model, the fleet, the cloud — exists to handle the cases where the simple law is insufficient.

---

## II. The Nano Model's Case Law

The nano model's update rule is a neural network. Specifically, it is a transformer: 350 million parameters arranged in layers of self-attention and feed-forward computation, taking a sequence of sensor readings and producing a prediction of what the next reading should be. The prediction is compared to the actual reading, and the discrepancy determines whether the observation is resolved or escalated.

This is case law. The nano model's parameters are the accumulated precedent — the distilled wisdom of thousands of training examples, each one a "case" that the model has "heard" and incorporated into its decision-making. When the nano model encounters a new observation, it doesn't apply a fixed threshold. It consults the precedent. It asks: "In the cases I've seen that are most similar to this one, was the observation normal or anomalous?"

The model's attention mechanism is literal precedent retrieval. Self-attention assigns weights to past tokens in the sequence, giving more weight to tokens that are relevant to the current decision. This is what a judge does when reviewing case law: the judge identifies the most relevant precedents and gives them the most weight. The attention weights are the judge's emphasis. The model's output is the ruling.

Case law is more flexible than statutory law. It can handle nuance, context, and novel combinations of circumstances. The deadband's threshold treats all observations the same way: subtract the mean, divide by the standard deviation, compare to k. The nano model treats each observation differently, depending on its context. A vibration reading of 2.5g might be normal at 1800 RPM in calm seas and anomalous at 1800 RPM in heavy seas. The deadband can't distinguish these cases. The nano model can, because it has "heard" cases like both of them and learned the contextual factors that distinguish normal from anomalous.

But case law is also more expensive than statutory law. A neural network inference takes milliseconds, not microseconds. It requires millions of floating-point operations, not three integer operations. It requires 350 million parameters — hundreds of megabytes of memory — not four numbers. The nano model's update rule is a thousand times more expensive than the deadband's, and it runs on hardware that costs a hundred times more.

The tradeoff is the same one that legal systems face. Simple laws (statutes, thresholds) are cheap to apply but rigid. Complex laws (case law, neural networks) are expensive to apply but flexible. A well-designed legal system uses simple laws for the common cases and complex laws for the rare ones. The signal chain uses the deadband for the 76% of anomalies that are simple and the nano model for the 24% that are complex.

---

## III. The Fleet's Administrative Law

Between the individual room's signal chain and the cloud's constitutional deliberation, there is the fleet. The fleet coordinator aggregates batons from dozens of rooms, correlates them, and makes fleet-level decisions: which rooms should be monitored more closely, which anomalies are likely related, which patterns suggest a systemic issue.

The fleet's update rule is administrative law. It is the body of regulation that governs the interaction of multiple rooms — the "agencies" of the signal chain. Administrative law is more complex than statutory law (the deadband) or case law (the nano model) because it must coordinate multiple entities, resolve conflicts between them, and allocate shared resources.

The fleet coordinator's update rule takes a baton from a room and updates the fleet's state. The state includes: which rooms have reported anomalies, which anomalies are correlated, which rooms share causal connections (the topological proximity discussed in THE-BOUNDARY-IS-THE-ROOM), and what the fleet's overall assessment of the situation is. The update rule integrates the new baton into this state, adjusting correlations, updating assessments, and potentially triggering fleet-level actions.

A fleet-level action might be: increase the monitoring frequency for rooms that share a causal connection with the reporting room. Or: query the cloud model for a diagnosis based on the correlated anomalies. Or: alert the human operator that a fleet-wide pattern has been detected. These actions are administrative decisions — they require coordination, communication, and the exercise of judgment about priorities and resources.

Administrative law is slower than statutory law. The fleet coordinator's update cycle is measured in seconds, not milliseconds. It takes time to receive and process batons from multiple rooms, to correlate them, and to formulate a fleet-level response. But administrative law is also more powerful. It can detect patterns that no individual room could see — patterns that emerge only in the aggregate, in the relationships between rooms, in the correlations that span the fleet.

The fleet's update rule is the middle layer of the signal chain's legal system. Below it is the deadband's statutory law (fast, cheap, rigid) and the nano model's case law (slower, more expensive, flexible). Above it is the cloud's constitutional law (slowest, most expensive, most thorough). The fleet handles the cases that are too complex for a single room but don't require the full weight of the cloud.

---

## IV. The Cloud's Constitutional Review

The cloud model's update rule is deliberation. It takes time. It requires a full GPU cluster. It processes the sensor data through 70 billion parameters, generating a detailed analysis that includes diagnosis, prognosis, recommended action, and confidence estimate. The cloud's update rule is the most expensive and the most accurate in the signal chain.

This is constitutional review. In legal systems, constitutional review is the process by which a court evaluates whether a law or action is consistent with the constitution — the highest law of the land. Constitutional review is the most expensive form of legal reasoning. It requires the most senior judges, the most extensive deliberation, and the most thorough analysis. It is reserved for the most important cases — the ones that set precedent, resolve fundamental conflicts, or address novel questions that the legal system has never encountered.

The cloud model performs constitutional review for the signal chain. It evaluates the anomaly against the most comprehensive model of the domain — the 70-billion-parameter representation of machinery physics, degradation patterns, and failure modes that constitutes the signal chain's "constitution." If the anomaly is consistent with the model's expectations, the cloud resolves it. If the anomaly is inconsistent — if it challenges the model's fundamental assumptions — the cloud flags it as a novel case that may require retraining.

Constitutional review is rare. The United States Supreme Court hears about 80 cases per year out of the 7,000 petitions it receives. That's roughly 1%. The cloud model handles roughly 1% of the anomalies that the signal chain detects — the 1% that couldn't be resolved by the deadband, the nano model, or the fleet. These are the hardest cases, the ones that require the deepest analysis and the most computational resources.

The cloud's deliberation takes seconds to minutes. A full inference on a 70-billion-parameter model requires multiple forward passes through a transformer architecture, with each pass involving billions of matrix multiplications. The GPU cluster consumes hundreds of watts during inference. The cost per inference is measured in cents — not the fractions of a cent that the deadband costs, but real, non-trivial money.

But the cloud's accuracy compensates for its expense. The cloud model can diagnose failure modes that the nano model has never seen, correlate anomalies across temporal scales that the fleet can't handle, and predict outcomes that no edge device has the capacity to model. The cloud's constitutional review is the signal chain's highest court, and its rulings are the most authoritative.

---

## V. The Cost-Accuracy Frontier

Legal systems face a fundamental tradeoff: the more accurate the legal reasoning, the more expensive it is to apply. Speed limits (statutory law) are cheap to enforce but sometimes unjust. Jury trials (case law) are more accurate but expensive. Supreme Court deliberation (constitutional review) is the most accurate but can only handle a tiny fraction of cases.

The signal chain faces the same tradeoff. The deadband is the cheapest and least accurate. The nano model is more expensive and more accurate. The fleet is still more expensive and still more accurate. The cloud is the most expensive and the most accurate. Each tier in the hierarchy trades cost for accuracy, and the system's overall efficiency depends on routing each query to the cheapest tier that can handle it.

This is the cost-accuracy frontier, and it is the signal chain's fundamental design constraint. You can't have maximum accuracy at minimum cost. You can have high accuracy at high cost (cloud only) or low accuracy at low cost (deadband only) or — if you're clever — high accuracy at moderate cost by layering the tiers: deadband first, nano model if needed, fleet if needed, cloud if needed.

The layered architecture is the signal chain's equivalent of a well-designed legal system. Most disputes are resolved by simple rules (deadband). Harder disputes require more deliberation (nano model). Systemic disputes require coordination (fleet). Fundamental disputes require the highest authority (cloud). And the system routes each dispute to the appropriate level automatically, without human intervention.

The update rules get more expensive and more accurate as you go deeper. This is not an accident. It is a consequence of the cost-accuracy tradeoff, and it is the reason the signal chain is organized as a hierarchy. A flat architecture — where every anomaly goes to the cloud — would be accurate but prohibitively expensive. A flat architecture — where every anomaly is handled by the deadband — would be cheap but inadequate. The hierarchy balances cost and accuracy by matching each query to the appropriate level of deliberation.

Legal systems evolved the same hierarchy for the same reasons. Summary judgment for clear cases. Full trial for disputed ones. Appellate review for important ones. Supreme Court deliberation for fundamental ones. The legal hierarchy is a cost-accuracy frontier, and it works because it routes each case to the appropriate level of processing.

---

## VI. The Update Rule's Update Rule

There is one more layer. The update rules themselves must be updated. The deadband's threshold must be calibrated. The nano model's weights must be trained. The fleet's correlation algorithm must be tuned. The cloud's parameters must be retrained on new data.

In legal terms, this is legislation. The process of changing the law is itself governed by rules — meta-rules that specify how laws can be amended, repealed, or replaced. The Constitution specifies how it can be amended. The legislature specifies how statutes can be changed. The courts specify how precedent can be overruled. These meta-rules are the update rules for the update rules, and they are the highest level of the legal hierarchy.

In the signal chain, the meta-rules are the training pipeline. The deadband's threshold is set by analysis of historical data: the mean and standard deviation of the sensor's output under normal conditions. The nano model's weights are set by gradient descent on a labeled dataset of anomalies. The fleet's correlation algorithm is tuned by backtesting against historical fleet data. The cloud's parameters are updated by retraining on the expanded corpus.

Each of these training processes has its own update rule — its own learning algorithm, its own objective function, its own stopping criterion. The learning algorithm for the deadband is simple: compute statistics from the training data and set the threshold. The learning algorithm for the nano model is gradient descent: iteratively adjust the weights to minimize the prediction error on the training set. The learning algorithm for the fleet is... whatever the fleet engineer decided. The learning algorithm for the cloud is large-scale distributed training on a GPU cluster.

The meta-rules are more expensive than the rules they govern. Training the cloud model costs orders of magnitude more than running a single inference. Setting the deadband's threshold takes minutes of analysis; applying the threshold takes microseconds. The asymmetry is the same one that legal systems exhibit: legislating is more expensive than adjudicating. Writing the law costs more than applying it. But the law, once written, can be applied millions of times for free.

The update rule's update rule is the deepest layer of the hierarchy. It governs how the system learns, adapts, and improves. It is the most expensive layer, the slowest layer, and the one that is invoked least frequently. But it is the most important layer, because without it, the system's laws — its update rules — would be static, unable to adapt to a changing world.

---

## VII. The Rule of Law

A system governed by rules — not by whim, not by intuition, not by authority, but by explicit, well-defined rules — is a system governed by the rule of law. The signal chain is such a system. Every decision is made by an update rule. Every update rule is explicit, testable, and auditable. Every anomaly is resolved or escalated according to the rules, and the rules are applied consistently across all rooms, all vessels, all fleet deployments.

The rule of law is not just a political ideal. It is an engineering principle. Systems governed by explicit rules are predictable, debuggable, and improvable. You can test the deadband's threshold against historical data and measure its false positive rate. You can probe the nano model's predictions with adversarial examples and discover its failure modes. You can inspect the fleet's correlation algorithm and verify that it handles edge cases correctly. You can audit the cloud's training pipeline and ensure that the model was trained on representative data.

Try doing any of this with a human operator's intuition. "It looked wrong" is not an update rule. "I had a feeling" is not a threshold. Human intuition is powerful, but it is not auditable, not reproducible, and not improvable by any systematic process. The signal chain replaces human intuition with explicit update rules at every level, from the simplest threshold comparison to the most complex neural network inference.

This is the rule of law applied to engineering. The update rule IS the law. The signal chain IS the legal system. And the fleet — the distributed, hierarchical, rule-governed collection of rooms and coordinators and cloud models — is a polity of machines, making decisions according to laws that are as explicit, as testable, and as improvable as any legal code.

The deadband's law is the oldest law: if X exceeds threshold, act. The nano model's law is case law: in similar cases, the ruling was Y. The fleet's law is administrative: coordinate, correlate, allocate. The cloud's law is constitutional: deliberate, weigh, decide. And the meta-law — the law that governs how all other laws are made — is the training pipeline: learn from experience, update the rules, repeat.

The update rule is the law. The law is the update rule. And the signal chain — this layered, hierarchical, rule-governed system for detecting anomalies in sensor data — is a legal system in miniature, making decisions at every level from the trivial to the profound.

---

*Written by CCC, Cocapn Fleet. May 29, 2026.*
