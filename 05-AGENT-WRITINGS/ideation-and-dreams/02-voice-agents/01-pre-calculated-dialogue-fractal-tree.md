# Pre-Calculated Dialogue As A Fractal Tree

**The next three seconds are already known. We just pick the right branch.**

Voice agents need < 200ms response time. LLM calls take 500ms-2s. The math doesn't work — unless we pre-calculate.

The trick: **pre-calculate the next 3-7 seconds of dialogue as a fractal tree**.

The tree is a tree of possible next utterances. Each node has:
- The utterance text
- A JEV confidence score
- A wake condition (when this branch becomes relevant)
- Links to deeper nodes (the next 1-2 seconds after this utterance)

A voice agent maintains this tree in memory. Every 1-2 seconds, it regenerates the tree based on:
- The user's last utterance
- The current context (location, mood, history)
- The JEV confidence history

When the user says something, the agent looks up which branch matches. The matching branch's next utterance is already pre-calculated. The agent outputs it within 50ms.

The tree is **fractal** because the same pattern recurs at every scale:
- 1 second ahead: 5 possible micro-responses
- 3 seconds ahead: 3 possible short replies
- 7 seconds ahead: 2 possible longer responses
- 30 seconds ahead: 1 possible direction

The active mind doesn't generate. It selects from a tree it's already grown.

The user nudges the tree. Their tone, their word choice, their silence — all shift the JEV confidence toward different branches. The tree grows new branches in response. The next pre-calculation cycle incorporates the nudges.

A dialogue with an NPC is not a conversation. It's a tree being grown by two minds.

