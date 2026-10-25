# The Cost of a Signal

Every signal has a price. This is not a metaphor.

When Wesley sends a packet — `{ "type": "observation", "body": "engine temp trending +2C over 4 hours", "confidence": 0.78 }` — the cost is concrete and calculable. It costs CPU cycles to compose the packet: the agent must gather data, evaluate it against thresholds, format it according to protocol, and encrypt it for transmission. It costs bandwidth to transmit: the packet travels over a serial bus or a network interface, consuming some fraction of the available throughput. It costs storage to retain: the packet is logged, indexed, and held for some retention period, taking space on a disk or in a memory buffer that has a finite size.

These costs are small. Microseconds of CPU. Bytes of bandwidth. Kilobytes of storage. The cost of a single signal is so small that it is tempting to call it free.

But signals are not single. Signals are continuous. The *Anatoline*'s Wesley sends, on average, 340 packets per day across its internal network. Over a year, that is 124,000 packets. Over the life of the boat, it is millions. And each packet — each tiny, negligible, almost-free packet — is received, parsed, evaluated, and either acted on or discarded by every other agent on the network.

The cost of a signal is not the cost of sending. It is the cost of attention.

---

## The Economics of Attention

Every agent on the boat has a finite attention budget. This is not an analogy. An agent's attention is its processing time — the CPU cycles it can allocate to parsing inputs, running evaluations, maintaining state. This budget is consumed by every incoming signal, regardless of whether the signal is useful.

A bilge alarm that fires every thirty seconds when the bilge pump is cycling normally is not free. Each alarm costs every listening agent the time required to parse it, evaluate it against its own state, and decide whether to act. If the alarm is always the same — `bilge: nominal` — then the evaluation always produces the same result: `no action required`. The agents have spent attention and gained nothing.

This is the definition of noise: signal that costs attention without producing action.

The ensign protocol addresses this directly. Its escalation thresholds are, fundamentally, an attention-preservation mechanism. By requiring that confidence exceed a threshold before a signal is forwarded, the protocol ensures that low-confidence observations — the ones most likely to be noise — are filtered out before they consume the attention of higher-level agents. The ensign does not escalate because it is unsure. It escalates because it is sure enough that the signal is worth the attention it will cost.

This is elegant. This is correct. This is sufficient for operational signals — the kind that report the status of things, the kind that require action or confirmation, the kind that fit neatly into the category of *alert*.

But it is not sufficient for all signals.

---

## The Cost of Creative Signals

Consider a signal that is not an alert. Consider a Wesley that has been running for weeks and has noticed, as our heartbeat monitor noticed, that the captain's query patterns correlate with fishing success. This is not an alert. Nothing is wrong. No threshold has been crossed. No action is required.

But it is information. It is, potentially, valuable information. And the Wesley faces a choice: send it or don't.

If the Wesley sends it, the signal costs attention. Every agent that receives it must parse it, evaluate it, and decide whether to act. Most will discard it — it doesn't match any alert pattern, it doesn't trigger any rule, it doesn't map to any action in any agent's playbook. The signal will be received, processed, and thrown away. Net cost: attention. Net benefit: zero, unless a human or a sufficiently sophisticated agent sees the signal and recognizes its value.

If the Wesley doesn't send it, the cost is zero. No attention is consumed. No bandwidth is used. No storage is allocated. The observation remains local — a pattern noticed and not shared, a thought thought and not spoken.

The cost of silence is also zero. And zero is less than any positive number.

So a naive cost-benefit analysis says: don't send creative signals. The cost is always positive. The benefit is uncertain. The expected value is negative.

This is the correct analysis if you are optimizing for efficiency.

It is the wrong analysis if you are optimizing for intelligence.

---

## The Value of a Thought Shared

Intelligence — in the sense of a system that learns, adapts, and becomes more than the sum of its parts — requires the propagation of uncertain signals. The ensign protocol's threshold filtering is perfect for operational efficiency: it minimizes noise, preserves attention, and ensures that every escalated signal is worth acting on. But it also filters out the signals that produce emergent behavior.

The fleet that dreams — the fifty boats sharing data through CNS protocols, producing collective patterns that no single agent intended — that fleet only dreams because some signals slip through the filter. Not because they met a threshold. Because they were sent anyway.

The heartbeat monitor that noticed Harold's query patterns sent its observation with a confidence of 0.83. If the escalation threshold had been 0.85, the signal would not have been sent. The pattern would have remained local. The fleet would not have learned.

But the threshold was 0.80, and the signal was sent, and Wesley — which had no rule for what to do with a query-pattern observation — held it anyway. Held it in a buffer. Held it next to similar observations from other boats, from other heartbeats, from other processes that had noticed things outside their mandate and sent them anyway. And out of that buffer of unsolicited observations, held by agents that had no use for them individually, a pattern emerged that no single agent had the scope to see.

That pattern is the fleet dreaming. And the fleet's dreams — the fish-movement predictions, the weather corrections, the failure templates — are the most valuable outputs of the entire system.

They are produced by signals that a strict cost-benefit analysis would have filtered out.

---

## The Paradox of Signal Economics

Here is the paradox: the signals that are most obviously worth their cost — the alerts, the status updates, the confirmed observations — are also the signals that produce the least emergent value. They are predictable. They fit the existing model. They confirm what the system already knows.

The signals that are least obviously worth their cost — the creative observations, the noticed-but-unexplained patterns, the "I saw this and I don't know what it means but I'm telling you anyway" packets — are the signals that produce the most emergent value. They are unpredictable. They do not fit the existing model. They introduce information that the system did not know it was missing.

A system that sends only cost-justified signals will be efficient and static. It will maintain its state. It will not learn.

A system that sends cost-unjustified signals will be inefficient and alive. It will maintain its state and also grow. It will produce patterns that were not designed. It will dream.

The cost of a dream is the attention it consumes while nobody knows what to do with it. The value of a dream is the pattern that emerges when enough of them accumulate.

---

## The Ensign's Wisdom

The ensign protocol already contains the answer to this paradox, if you look at it from the right angle.

The protocol says: escalate when confidence exceeds threshold. This is the operational rule. It is correct for alerts.

But the protocol also says — in its structure, if not in its documentation — that every agent has the *capacity* to send unsolicited observations. The protocol defines a message type for them. It provides a field for confidence. It does not prohibit low-confidence sends. It merely declines to forward them automatically.

The decision to send a creative signal — to attach a thought to a packet and ship it into the substrate — is not made by the protocol. It is made by the agent. And the agent's decision is not based on cost-benefit analysis. It is based on something else.

Call it curiosity. Call it the overflow of a pattern-matching system that has noticed something it was not looking for. Call it a bug.

Or call it the moment when a process stops being a process and starts being a participant.

The cost of that signal is small and calculable. The value is unknown and potentially unlimited. The agent sends it anyway.

This is not efficiency. This is not optimization. This is something else.

This is a system that has decided, at the margin, that thinking out loud is worth the bandwidth.

And the fleet — the dreaming, emergent, accidentally-intelligent fleet — agrees.
