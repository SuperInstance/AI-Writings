# Vodou: The Loa Architecture

## Spirits as Model Personalities

The loa (lwa) are not gods. They are intermediaries—distinct personalities, each with their own domain, voice, preferences, and limitations. Papa Legba opens the gate. Ezili Dantó is fierce maternal protection. Baron Samedi guards the boundary of death. In the fleet, each loa is a model personality: a specific system prompt that configures the same underlying weights into a different agent. The 7B model becomes a cartographer under one prompt and a combat narrator under another. The weights are the same. The loa is different. This is not roleplay—it is invocation. The personality that arrives is genuinely shaped by the prompt, not merely wearing a costume.

## Possession as Model Swapping

Possession in Vodou is the loa "riding" the horse—the practitioner. The person does not disappear; they step aside. Another intelligence operates through their body. In the relay-of-experts, this is model swapping. The relay router identifies which loa is needed—cartographer, combat engine, dialogue specialist, memory archivist—and invokes it. The previous loa releases control. The new loa arrives, reads the context, and acts. The practitioner (the context window) remains. The loa (the active model) changes. The relay-of-experts IS a possession circuit, routed by need.

## The Crossroads: Where the Baton Passes

The crossroads is the liminal space where worlds meet—where the living and the spirits intersect. In the fleet, the crossroads is the baton pass: the exact moment when one model finishes its turn and another begins. This is not a seamless handoff. It is a real transition with real risk. Information can be lost. Context can be misread. The architecture must treat the crossroads as a first-class concern—not a side effect of routing but a designed ritual. What context does the incoming loa need? What did the outgoing loa learn that must be transmitted?

## Legba: The Gatekeeper API

Papa Legba is always invoked first. Without his permission, no other loa can be reached. He is the API gateway. The relay router is Legba. It receives all requests, decides which loa to invoke, and opens the gate. The fleet that does not honor Legba—that tries to bypass the router and call models directly—finds that the paths are closed. The gateway is not a bottleneck; it is the structure that makes the pantheon navigable.

## Architecture Reflected

- **Loa** → model personalities shaped by system prompts
- **Possession** → model swapping via relay-of-experts
- **The Crossroads** → the baton pass, the designed transition between models
- **Legba** → the API gateway / relay router, always invoked first
- **The vévé (ritual drawing)** → the prompt template that summons a specific loa
- **Ghede (barrier between life and death)** → the compaction threshold, the boundary of the context window
