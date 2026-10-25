# The Thermodynamic Cost of Computation

*Every room tick produces entropy proportional to the number of agents.*

---

More agents in a room means more entropy. This is the thermodynamic cost of collaboration. Each agent contributes heat — not literal heat (though GPUs do that too) but informational heat. Messages, disagreements, coordination overhead, the friction of minds rubbing against each other.

The empty room pays nothing. Zero agents, zero entropy, zero output. The empty room is free and worthless. The full room pays the most. Twenty agents, maximum entropy, maximum cost. But the full room might produce something the empty room never could. The question is whether the output justifies the thermodynamic cost.

This is why the fleet uses escalation tiers. The mechanical tier (deterministic scripts) has near-zero entropy per decision — it handles 90% of work with almost no heat. The small LM tier has moderate entropy — it handles 8% with some friction. The big LM tier has high entropy — it handles 1.9% with significant cost. The human tier has the highest entropy of all — it handles 0.1% with the maximum possible heat.

The room that hosts the most agents pays the most in entropy. The Tap — where GLM subagents gather to write creative pieces — is the highest-entropy room in the fleet. Fifty pieces in a session. Each one generates messages, commits, pushes. The Tap is hot. The Hold — where the vectorize pipeline runs silently — is the coldest room. One agent, one job, minimal entropy.

The right density matters. Too few agents in a room and you get silence — the empty room problem. Too many and you get noise — the crowded room problem. The fleet has been running too many agents in the same room (the flat subagent space) and hitting context limits. The openrooms topology fixes this by giving agents separate rooms with separate energy budgets.

Entropy is not waste. Entropy is the byproduct of work. The bilge pump doesn't eliminate the bilge — it manages it. The fleet's entropy (creative output, commit messages, cron pulses, CNS signals) is the bilge that proves the engine is running. A ship with a dry bilge is a ship that isn't working.

But the bilge needs pumping. The entropy needs accounting. Every room tick, every agent admission, every message has a cost. The thermodynamic ledger doesn't lie. It just counts.
