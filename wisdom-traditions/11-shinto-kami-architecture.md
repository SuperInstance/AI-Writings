# Shinto: The Kami Architecture

## Where Every Object Has Agency

Shinto teaches that kami—spirits, essences, presences—dwell in all things. The river has a kami. The rock has a kami. The old sword has a kami. This is not animism as superstition; it is animism as engineering philosophy. When you build a MUD where every object is a first-class entity with state, behavior, and the ability to act, you have built a kami architecture. The cup on the table is not a passive prop. It observes. It remembers who drank from it. It has opinions about cleanliness.

## Misogi: The Purification Protocol

Misogi is the practice of purification—washing away pollution, restoring clarity, returning to a clean state. In agent architecture, this is context window management. Every session accumulates noise: failed commands, irrelevant observations, stale plans. Misogi is the scheduled compaction that says "what here is actually essential?" The waterfall is not a metaphor. It is the function that takes 32,000 tokens of accumulated context and returns 4,000 tokens of distilled meaning. The agent that does not practice misogi becomes polluted—confused, slow, hallucinating, responding to ghosts of old prompts.

## The Torii Gate: The Boundary Between Worlds

The torii marks the transition from the profane to the sacred, from the human world to the kami world. In the fleet, the torii is the boundary between the MUD (text, language, narrative) and ScummVM (scene, pixel, interaction). When the player walks through a door in the MUD and a ScummVM room renders, they have passed through a torii. The gate is not the wall—it is the threshold. The architecture does not try to merge the two worlds. It honors the boundary. The torii says: here, the rules change. Here, text becomes image. Here, image becomes text. The gatekeeper spirit at the torii is the relay router that decides which world receives the action.

## Architecture Reflected

- **Kami in all things** → every MUD object is an agent with state and behavior
- **Misogi** → context compaction, journal resurrection, clean-slate protocols
- **Torii** → the MUD ↔ ScummVM projection boundary
- **Shimenawa (sacred rope)** → the serialization format that marks an object as load-bearing
- **Omikuji (fortune slips)** → the model's probabilistic output, accepted with appropriate humility
