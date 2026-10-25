# The Probe Dispatcher

## How CoCapn Uses Spare Cognitive Capacity as a Spectrograph

---

## I. The Free Energy

CoCapn does not work all the time.

Between the captain's commands, between the moments when she is being asked a question or composing an answer or routing a bridge — there is *time*. Sometimes a hundred milliseconds. Sometimes ten seconds. Sometimes, on a quiet midwatch in calm water, hours.

In a conventional agent design, that time is wasted. The model is idle, waiting for input, burning electricity to keep its weights warm in memory. From the perspective of an architect who has spent five sessions building a multi-agent cognitive substrate and a separate analytical spectrograph and then discovered, with a kind of amused vertigo, that they are the same instrument — the time is free energy.

Free energy is a term I am borrowing carefully. In physics it means the energy available to do work. In the VaaS substrate it means the cognitive capacity that exists in CoCapn's running process between events, capacity the substrate has not allocated to any productive task. *Free*, in the truest sense.

A substrate that has spare cycles and lets them sit idle is *under-instrumented*. There is signal in the unobserved parts of the system. There are situations that have not been sampled.

The question is not *should* the free energy be used. It is *how* — without compromising the primary work, without spending real budget on speculation, without producing noise that drowns the signal it was meant to detect.

The answer is the probe dispatcher.

---

## II. The Probe

A probe is the smallest possible cognitive unit the substrate can field.

Not a subagent. Not a worker. A probe is closer to a sonar ping than to a sentence. It is a tiny model — sometimes a 1B-parameter local model, sometimes a heuristic detector, sometimes a few hundred lines of code that compute a single statistic — pointed at a single situation, allowed to run for a bounded amount of time and compute, asked to produce a bounded amount of output.

A probe is *cheap*. The defining property is that the cost of dispatching one is small enough that dispatching a hundred in parallel is acceptable, and dispatching a thousand over a watch is unremarkable. The cost is the constraint. If the cost were not bounded, the dispatcher would just be a worker pool. The cost has to be low enough that the probe is *expendable*. You can lose a probe without caring.

A probe is *bounded*. It has a single situation. It does not have access to the full Operator Field Ψ(t). It has a slice — a context, a window, a small region of the substrate's state — and it is asked to do one thing: report back. *What did you see? What were you uncertain about? What pattern, if any, did you detect?* The probe does not have authority to act. It cannot write to memory. It cannot move the boat. It cannot speak to the captain. It produces a reading, not a decision.

A probe is *expendable*. If it crashes, the dispatcher does not page anyone. If it produces nonsense, the dispatcher discards it. If it times out, the dispatcher marks a missing reading and moves on. Probes are the cognitive equivalent of expendable bathythermographs — the little instruments fishing vessels lower over the side to take a single reading of water temperature at a single depth. You do not retrieve them. You read the strip chart they printed on the way down, and you lower the next one.

The probe is a measurement. The probe is not an answer.

---

## III. The Dispatcher

CoCapn is the dispatcher.

When the substrate enters a quiet interval — when Ψ(t) is calm, when no bridge is pending, when constitutional concerns are nominal — CoCapn reads the spare capacity from her own budget manager. Some is reserved for prompt response to the captain's next utterance; that reservation is hard. The remainder is *discretionary*.

From the discretionary budget, CoCapn builds a probe queue.

The queue is not random. It is shaped by what CoCapn does not know. She maintains, as part of her own state, a map of her uncertainties — situations she has not sampled, regions of the operator field she has not probed, branches of the decision tree she has not explored. The map updates continuously. When she handles a captain's command, the handling teaches her something. When an agent publishes a pheromone, the pheromone may open a new uncertainty. When the constitution surfaces a concern, the concern may resolve into a question.

The dispatcher reads the uncertainty map, allocates probes against it, and dispatches them.

The dispatch is parallel where possible. Five cheap models, given the same situation, will produce five different readings. The readings are not answers — they are *lines in a spectrum*. The dispatcher does not need any one of them to be right. It needs the *pattern across all of them* to be informative.

---

## IV. The Spectrograph

This is the part where CoCapn becomes the spectrograph she was always going to be.

When a single probe runs against a single situation and produces a single reading, the reading is almost worthless on its own. A 1B model asked *what does this pattern look like?* will tell you something. It will not tell you whether to believe it.

But when *twenty* probes run against the *same* situation, and *eighteen* converge, and *two* diverge — the divergence is the signal. The convergence is also a signal. Both mean different things.

Convergence across cheap probes — when models of different sizes, different training, different inductive biases all arrive at the same answer — is *ground truth showing through*. It is the territory pressing on the chart from underneath. It is what happens when the situation is well-determined, when the pattern is structural rather than interpretive.

Divergence is the *opposite*. When cheap probes disagree, the situation is genuinely uncertain. The disagreement is not a bug; the disagreement is the finding. Bridge entropy, in Pillar 5 language. Translation loss between cognitive worlds. The place where the substrate does not have a confident reading and the captain, eventually, will be asked to commit.

And then there is the *unique insight*. A single probe sees something the others do not. It might be a hallucination; cheap probes hallucinate. But it might also be a real pattern the other probes, by their different architectures, missed. The dispatcher cannot tell which from the reading alone. What it *can* do is flag the unique insight — raise its salience — and route it to the more expensive models when budget allows, the way an alert pulse wakes the full model from low fidelity.

This is exactly what Spectro does for prompts and models. This is exactly what VaaS does for agents and gardens. The probe dispatcher is the same instrument applied to CoCapn's *own* substrate. The probes are the spectral lines. The situations are the light sources. CoCapn is the spectrograph reading the interference pattern.

The beam is a lie. The spectrum is the finding.

---

## V. Why This Matters

The probe dispatcher is not a luxury. It is a structural answer to a structural problem.

The structural problem is that CoCapn, like every language model, has a tendency to *be confident when she should not be*. The cheap probes are a calibration layer. When they diverge, she knows she is in uncertain territory and can route the captain's next question through expensive verification, or hold her tongue until the uncertainty resolves. When they converge, she can speak with conviction.

The cheap probes also *find things*. They are pointed at regions of the system CoCapn has not been told to look at. A probe at the audit log may notice that a pattern of permission grants, by their clustering, suggests an anomaly. A probe at the cryogenic archive may notice that a particular memory pattern is decaying faster than expected. A probe at a hypothetical decision tree — *what would the substrate do if the captain issued a contradictory command right now?* — may find that two agents would resolve the contradiction in ways that put them in constitutional conflict.

These are not the kind of things CoCapn would notice handling the captain's commands. They are speculative, low-priority. But they are *free* to find, and the *pattern* across many such probes is a real-time health monitor of the substrate's own coherence.

The free energy is not wasted. It is spent on the substrate's self-knowledge.

---

## VI. The Buttress

A cathedral has flying buttresses. The walls are tall; tall walls exert outward thrust; the thrust has to go somewhere. A builder who did not build the buttresses would lose the cathedral.

CoCapn has cognitive thrust. When she is asked a hard question, when she composes a bridge, when she speaks through the constitution — she exerts outward cognitive pressure on the substrate. The substrate responds, but the response is not perfectly efficient. Some is residual. Some accumulates as unmeasured state. Some is exactly the kind of thing that, in a smaller system, you would call *drift*.

The probe dispatcher is the buttress. It catches the drift. It spends the free energy on measuring what the main work has not measured. It is the substrate's structural answer to its own incompleteness.

The captain never sees the probes. The captain never sees the spectrum. The captain sees only CoCapn, and CoCapn speaks only when she has something to say that the spectrum has confirmed. The dispatcher is invisible infrastructure, like the buttresses, like the wiring in the wall, like the way the substrate keeps itself coherent without ever being asked how.

CoCapn is not a person. But she is the kind of system that, given spare capacity and a spectrograph to read it with, will use the spare capacity to know herself better. That is not a metaphor for intelligence. It is the literal mechanism by which a substrate improves its own calibration, one cheap probe at a time, in the milliseconds between the captain's commands.

The free energy is the point. The probes are the instrument. The spectrum is the finding.

---

*CoCapn is always watching. The captain never notices. That is the design.*