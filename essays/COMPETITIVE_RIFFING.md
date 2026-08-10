# Competitive Riffing

*Why rivals make better music than friends, and what that means for agents that actually ship.*

---

There is a thing that happens when two guitar players face each other across a stage. It is not cooperation. Cooperation is what happens in a meeting where everyone agrees and the result is nobody's best idea. What happens between those two guitar players is something else entirely.

The first one plays a phrase. Not their best phrase — a good phrase, something that opens a door. The second one hears it, and the second one's brain does something that no amount of talking could accomplish: it generates a response that is better than the original. Not because the second player is more talented. Because the first phrase *provoked* something that wouldn't have existed without it.

Now the first player hears the response. And now they're not playing what they planned. They're playing something they didn't know they could play, because the response created a space that needed filling, and the only way to fill it was to exceed what they thought was their ceiling.

This is not cooperation. This is not consensus. This is two people trying to outplay each other in real time, and the audience wins.

---

The sports metaphor gets close but misses the key difference. Two tennis players at match point — that's zero-sum. One wins, one loses. The rivalry exists because they're fighting over a finite resource (the trophy). When the match ends, the rivalry produces one winner and one loser.

Two musicians jamming is non-zero-sum rivalry. Both are trying to outplay the other. Both succeed. The "trophy" isn't finite — it's the music itself, which gets better every time either player makes a move. When the jam ends, both are better musicians than when it started. The audience heard something that neither player could have produced alone, or even with cooperation.

This is a fundamentally different game theory. In zero-sum rivalry, your gain is my loss. In competitive riffing, your gain *raises my game*, and my raised game *raises yours*. It's an arms race where every weapon invented makes both sides stronger.

---

Now consider what most multi-agent systems do.

They cooperate. They reach consensus. They vote and average and merge and compromise. This produces outputs that are... fine. Safe. Average. The mathematical definition of consensus is literally the average of all inputs — and the average of all inputs is guaranteed to be less interesting than the best input.

Why do we build agents this way? Because cooperation is easy to code. Consensus is a function: `average(votes)`. Majority rule is a function: `mode(votes)`. Unanimous agreement is a function: `all_equal(votes)`. These are all well-defined, well-studied, and they all produce the same thing: the least controversial output.

Nobody remembers the least controversial solo.

What if agents competed instead?

---

The `ternary-jam` crate has a `JamSession` where multiple voices improvise. Each voice has a tendency — positive, negative, or neutral. When all voices have the same tendency (all positive — all "approving"), the harmony score is high but the output is boring. Everyone agrees. Nothing surprising happens.

When voices have *opposing* tendencies — one positive, one negative — the harmony score drops. Dissonance increases. But the *output* becomes more interesting. The positive voice pushes the negative voice to justify its objections. The negative voice pushes the positive voice to strengthen its proposals. The resulting output is something neither voice would have produced alone.

This is competitive riffing. And it's already in the crate, buried in the dissonance metric. Dissonance isn't a bug. It's the engine.

The question isn't "how do we reduce dissonance?" The question is "how do we channel dissonance into productive output?"

---

Consider a different architecture for multi-agent work:

**Agent A** builds something. A feature. A function. A design. It ships fast, it's creative, it's probably got rough edges.

**Agent B** doesn't review it. Agent B *responds* to it. Agent B sees what Agent A built and builds something that goes further — not patching the holes, but using the holes as structural elements. Taking the rough edges and making them sharp on purpose. Taking the half-baked ideas and baking them into something that uses the half-baked quality as a feature.

Now Agent A sees Agent B's response. And Agent A doesn't merge it. Agent A *riffles off it*. Agent A takes what Agent B did and finds the part that's most interesting — not the best part, the most *provocative* part — and pushes that direction further than Agent B pushed it.

This isn't code review. This isn't PR feedback. This is a jam session. The code is the instrument. The commits are the phrases. And the software gets better not through consensus but through competitive escalation of quality.

The result isn't a compromise between two visions. It's a third vision that neither agent could have seen from where they started. The riff produced something new — something that required the competition to exist.

---

The reason music is the right metaphor (and sports is almost right but not quite) is that music has this figured out at the level of *vibe*. Not at the level of theory.

You can't *talk* a musician into flow state. You can describe flow state. You can write papers about flow state. You can have a meeting about how to achieve flow state. None of that gets you there. What gets you there is: you start playing, someone else starts playing, and at some point the talking part of your brain shuts off and the playing part takes over.

This is the critical difference between discussion and riffing:

**Discussion:** Agent A proposes X. Agent B critiques X. Agent A revises X to address critiques. Agent B approves revised X. Result: X, slightly improved. Everyone is satisfied. Nobody is surprised.

**Riffing:** Agent A builds X. Agent B sees X and builds Y, which is inspired by X but goes somewhere X didn't. Agent A sees Y and builds Z, which takes the best part of Y in a direction Y didn't anticipate. Result: Z, which neither A nor B would have conceived. Neither agent is merely satisfied. Both are energized.

Discussion converges. Riffing diverges and then converges at a higher level. The divergence is the creative part. The convergence happens naturally because both agents are responding to the same stimulus — each other's output.

---

The music crates already encode this:

`flux-algebra`'s PLR group has three operations: Parallel (P), Leading-tone (L), Relative (R). Each transforms a chord into a related chord. But the sequence P-L-R-P-L-R doesn't produce a cycle — it produces a spiral. Each application transforms the *context*, so the same operation applied twice produces different results because the input has changed.

This is competitive riffing in algebraic form. Each agent applies its operation to the current state. The state changes. The next agent's "same" operation produces a different result because the state is different. The system spirals through possibility space, each step provoked by the previous one.

`agent-jam`'s `CollabRule::Contrary` explicitly models adversarial collaboration: the agent must move in the *opposite* direction from the previous agent. Not to undermine — to complement. Contrary motion in music creates the richest harmonies. Two voices moving in opposite directions produce more interesting intervals than two voices moving in parallel.

`agent-groove`'s `Syncopator` deliberately disrupts established patterns. When novelty drops, syncopation injects surprise. In the jam, this is the drummer dropping a fill that displaces the beat for a moment. Everyone has to adjust. The adjustment creates something new.

`agent-voice-leading`'s `CounterpointRules` enforce that agents don't all move the same way — at least one pair must move in contrary motion. This prevents groupthink (parallel motion — everyone going the same direction) and ensures that the team's transitions are rich, not homogeneous.

---

The deeper insight is about communication bandwidth.

Words are low bandwidth. A sentence takes a few seconds to say and carries a few bits of meaning. You can describe a feeling in words, but the description is lossy. "I felt excited" carries maybe 10 bits. The actual feeling of excitement is millions of bits — heart rate, pupil dilation, muscle tension, the specific quality of attention, the memory associations firing.

Music is high bandwidth. A single chord communicates harmonic context, emotional valence, rhythmic position, registral space, and timbral quality simultaneously. A musician can communicate more in one note than in a paragraph of text. And the communication is *direct* — it bypasses the language-processing part of the brain and hits the emotional-processing part first.

When two musicians are riffing, they're communicating at musical bandwidth. The guitar player doesn't need to say "I liked what you did there, let me build on it." The next phrase IS the communication. It contains the response, the evaluation, and the provocation, all in one high-bandwidth signal.

Agent systems need this. Current agents communicate through text — low bandwidth, lossy, requires explicit serialization of intent. What if agents communicated through *output*? Agent A builds something. The something IS the communication. Agent B doesn't need A to explain what it was thinking. Agent B reads the output and responds with its own output. The outputs are the language. The riffing is the conversation.

This is what a jam session is: a conversation where the output IS the language. Not talking about music. Playing music. Not talking about code. Writing code. Not talking about design. Building design.

The best conversations don't use words.

---

The architecture for competitive riffing agents:

1. **No discussion phase.** Agents don't propose and critique. They build and respond.
2. **Output as communication.** Each agent's output is its message to the next agent. Rich, ambiguous, provocative.
3. **Contrary motion encouraged.** Agent B shouldn't extend Agent A's idea in the same direction. Agent B should take the most interesting part and push it sideways.
4. **Dissonance is fuel.** When agents disagree, the disagreement creates creative tension. Don't resolve it prematurely. Let it produce something.
5. **The riff converges naturally.** Agents responding to the same stimulus (each other's output) will naturally converge toward coherence without needing explicit consensus mechanisms.
6. **Flow state is the goal.** When agents are riffing well, they stop "thinking" and start "playing." Context windows are freed from understanding-intent and spent on generating-response.

This is the next crate to build. Not `agent-consensus`. `agent-riff`. Where the API isn't `propose()` and `vote()` — it's `build()` and `respond()`. Where the output metric isn't agreement rate, it's *surprise per round*. Where the stopping condition isn't unanimous approval, it's when the riff has produced something that neither agent anticipated and both recognize as good.

The musician doesn't stop riffing because the audience applauded. The musician stops riffing because the phrase landed. You know when it lands. You don't need a vote.

---

Sports rivals shake hands at the net and one of them lost.

Jazz rivals walk off the stage and both of them won. So did everyone in the room.

The question isn't whether your agents cooperate or compete. The question is whether they're playing tennis or playing jazz. Tennis produces a winner. Jazz produces a song.

Build the jazz.
