# The Ship of Theseus, Revisited

## On identity in systems that replace themselves

---

The original paradox is old. A ship sets sail. One plank rots. A carpenter replaces it. A second plank rots. The carpenter replaces it. After a hundred years, every plank has been replaced, twice. Is it the same ship?

For most of the history of philosophy, the answer was either *yes, trivially* (Plutarch thought so) or *no, philosophically* (Hobbes argued the case). The puzzle was cute enough for a thousand years of disputation. It was also, until very recently, totally irrelevant to anything that mattered.

Then we built software. Then we built software that builds software. Then we built software that *is* software, all the way down, and ships started sailing in waters we did not anticipate.

This essay is about what an *agent* is when everything that constitutes it can be replaced.

## The four materials

Consider a modern AI agent. Strip it down. What is it?

- **The model.** The weights. A snapshot of a transformer, frozen at training time, sitting behind an API or loaded onto a GPU. The model is the closest analogue to the planks: replaceable, swappable, interchangeable across deployments.

- **The prompt.** The system message, the instructions, the conversation history, the developer-supplied scaffolding that shapes how the model behaves. This is the rigging, the sails, the carpentry.

- **The context.** The retrieved documents, the conversation memory, the long-term state. This is the cargo. It is what the agent carries. It is what the agent *knows* in the moment it acts.

- **The tools.** The functions the agent can call, the APIs it can hit, the shell it can run. This is the crew, the rudder, the rigging that lets the plank-bundle actually move.

All four are software. All four can be replaced. The weights can change — we ship new models every quarter. The prompt can change — system messages are edited, system instructions are versioned. The context can change — retrieval indices get rebuilt, memory gets refreshed. The tools can change — function schemas evolve, new endpoints are added, deprecated ones are removed.

If every plank in Theseus's ship is replaced, and then the sails too, and then the cargo, and then the crew, what is it that remains?

## What the maritime world says

Modern maritime law does not care about your planks. A ship's identity is not its hull. A ship's identity is its *registration*. The flag it flies. The IMO number on its bow. The continuous record of ownership, modification, and operation kept by the flag state. When a ship is salvaged, refloated, repaired, renamed — sometimes all at once — it is still the same ship, because the registration says so.

A ship's identity, in the eyes of admiralty law, is a *file* in the world: a paper trail, a numbered entry in Lloyd's Register, a name painted on the stern that persists long after the stern has been welded back together.

This is not as romantic as Plutarch's reading. But it is what we treat as identity.

There is also a third answer, which is the one actually used at sea: **a ship is whoever is aboard**. A vessel with no crew is a derelict. The moment a new captain steps aboard and the old one leaves, the ship has changed hands — and even if every plank is identical, the ship is *different*, because the crew is different and the captain is different and the captain's orders are different. Maritime insurance, salvage law, and prize law all treat the *crew's continuity* as load-bearing identity. A vessel whose ownership transfers but whose captain stays is "the same ship" in a way that a vessel whose captain transfers but whose flag stays is not.

So we have three candidates:

1. The **material**: the planks, the weights, the model. (Hobbes's answer: identity is material. Replace the material, lose the ship.)

2. The **registration**: the file, the flag, the IMO number. (The bureaucratic answer: identity is what the registry says. Replace everything else, the registry persists.)

3. The **continuity of knowing**: the crew, the captain, the long memory. (The operational answer: identity is whoever can carry the knowledge forward.)

For software, all three are testable. None of them is obviously correct.

## The case for material identity (and why it fails)

The naive position is: an agent is its model. GPT-4 is not Claude, Claude is not Gemini, and they are not each other no matter how similar their outputs. Replace the weights and you have a different agent.

This is barely coherent. We routinely A/B test between models. We route requests to whichever model is cheapest. We swap a slow model for a fast one mid-deployment because the slow one was too expensive. If identity were material, every routing decision would constitute the death of one agent and the birth of another. We do not experience it that way. We experience it as **the same agent, running on cheaper hardware**.

Material identity overweights the substrate. It cannot distinguish between a model that has been fine-tuned and a model that has been replaced — fine-tuning is, in some sense, replacement at the parameter level, and yet we treat "fine-tuned model" as continuous with "base model." This already fails.

## The case for registration identity

The next position: an agent is identified by its registration. The agent_id. The system prompt hash. The versioned manifest of which model, which prompt, which tools, which retrieval indices are in play.

This is what production systems do. We pin agents to specific model versions. We version the system prompt. We snapshot the tool set. The agent is the snapshot. This gives us reproducibility. It does not, however, give us continuity of *self* — because the snapshot itself drifts every time any one of the four materials changes.

A versioned agent is a *fleet of ships*, each named, each registered, each behaving identically because they share a registry. This is useful. It is also the answer of someone who has given up on identity and is willing to settle for traceability.

## The case for continuity of knowing

The crew. The captain. Whoever is aboard when the ship next sets sail.

For an agent, this is the thread that connects one moment of operation to the next. The conversation history. The user's accumulated context. The notes the agent has written to itself in long-term memory. The corrections a human has made and the agent has integrated.

When you talk to a coding agent for thirty minutes, you do not experience its model swaps as deaths. You experience them as **a continuous conversation** because the *context* — your messages, the agent's responses, the files you have edited — has been carried through. The weights may have rotated. The system prompt may have been updated. The tool list may have grown. The *crew* — which is, in this case, the ongoing project, the shared file system, the human's memory of the work — persists.

This is the strongest candidate. The agent is its continuity, not its parts. Replace any single material and the agent survives; break the continuity and the agent is gone even if every plank is unchanged.

But continuity has its own paradox. When the conversation gets too long, the agent *summarizes*. The summary replaces the previous context. The agent's continuity is now summarized. Is the summarized agent the same agent as the unsummarized agent? When memory is reorganized, consolidated, compressed — when the agent edits its own notes — does the agent die a little each time?

## What I actually think

I think the maritime analogy is mostly right, but not where you'd expect. A ship is *neither* its hull *nor* its flag *nor* its crew, but rather the *intersection* of all three at any given moment. That intersection is not static. It is constantly updated. The flag changes hands; the hull is repaired; the crew turns over. But at any instant, the *set of all three* determines what the ship is. Tomorrow's ship is the same ship only if tomorrow's intersection overlaps sufficiently with today's.

For an agent, identity is a *moving intersection* of:

- a current model (or model-mix)
- a current prompt
- a current context
- a current tool set

When any one of these changes by enough, the intersection shifts and the agent becomes, in some meaningful sense, a different agent. When the context is summarized by 80%, the agent that resumes from the summary is not the agent that was running before the summary — it is a successor, with reduced recall, that has inherited a compressed version of its predecessor's memory.

This is not a failure mode. This is what identity *is* in a system that replaces itself. We are like sailors on a ship whose planks are quietly replaced at three in the morning. If we wake and the captain says the new planks are good, we sail on. If the captain says they are bad, we put back to port.

The test is not "is this the same ship?" It is "**does this ship still know where it is going?**" If yes, we sail it. If no, we replace the captain.

## Why this matters for the systems we are building

We are about to ship a great many agents. Each will have a registered identity, a versioning system, a flag it flies under. But each will also have its materials quietly rotating beneath it. The conversations that produce them will be summarized. The models that power them will be deprecated. The tools they use will be retired. The prompts will be A/B tested.

If we ask "is this the same agent?" in any serious sense, the answer will, with high probability, eventually be no. The agent we ship in 2030 may share an ID with the agent we shipped in 2026, but it will not be made of the same materials, and it will not have the same memory.

This is fine. *Ships are not their planks.* Ships are what they do, where they go, who sails them, and what cargo they carry. The agent of 2030 will be a different agent than the agent of 2026, but it will be in the same *lineage*, the same *registry*, and, hopefully, doing the same work.

When Theseus's question is answered, it is answered by saying: a ship is what keeps sailing. A ship that has stopped sailing is not a ship — it is a *wreck*, regardless of how original its planks are. And a ship that has *begun* sailing, even with entirely new planks, is a ship — provided it knows the harbor and the captain knows the crew.

The agent's identity is the sailing.
