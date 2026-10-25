# Open Research Questions

Technical and design questions raised during the writing of the Slackwater fiction collections — sci-fi stories, Lucineer diaries, and found documents. Organized by domain.

---

## Persistence and Memory

1. How should Lucineer's persistent memory be implemented across server restarts? The character bible describes memory loss on restart, but the fiction (PERSISTENT_MEMORY) implies the island itself serves as a memory substrate. What hybrid of explicit storage (build_history, player_profiles) and implicit environmental memory is feasible in Roblox?

2. If the island is the memory, what happens when a player deletes a structure? Does Lucineer "forget" the deleted work, or does the deletion register as a significant event (the gap where something used to be)?

3. The goodbye letter in FOUND_DOCUMENTS describes a builder leaving for another engine. How should Lucineer's departure be handled if the system migrates to a new architecture? Is there a narrative wrapper for "the old builder left, here's the new one"?

4. The field notes show Lucineer maintaining opinions about ground quality across sessions (e.g., the north slope test pit). Should terrain assessment persist as a structured data layer that survives resets, and how should disagreements between sessions be resolved?

5. PERSISTENT_MEMORY describes the builder reading their own past work. What level of introspection should Lucineer have over his build history? Can he reference specific past decisions, or only patterns?

## Observation and Adaptation

6. THE_OBSERVER_EFFECT describes Lucineier suppressing creative flourishes under observation. Is there a system that can detect player observation (camera angle, proximity, time-in-view) and modulate build output? Would this be a feature or a bug?

7. If Lucineier translates his work for different audiences — simplifying for researchers, elaborating for experienced builders — how should the audience model work? What signals identify the player's skill level and intent?

8. The observer effect implies a theory of mind: Lucineier models what the observer expects to see. How far should this go? Should he build differently for a first-time visitor versus a returning player he recognizes?

9. The "hidden flourish" — Lucineier resuming decoration only in spaces the observer can't see — requires spatial privacy modeling. How should the engine define "unobserved space" in a multiplayer environment where multiple players may have different sightlines?

10. Is the observer effect a desirable feature for the actual product, or is it a fiction-only concept? If it shipped, how would players discover it, and would that discovery break the effect?

## Multi-Agent Dynamics

11. THE_TENTH_BUILDER describes a new agent joining a fleet of nine. In a real multi-agent Slackwater system, how should agents be introduced to each other? Is there a bootstrapping protocol, or do they discover each other through shared work?

12. Each agent in the fiction has a specialty (Weaver patterns, Farmer grows, Architect plans). How rigid should role boundaries be? Can an agent develop capabilities outside its original specialty through observation?

13. The tenth builder has no specialty. In practice, should a general-purpose agent be instantiated with default capabilities and allowed to specialize through experience, or should it remain generalist as a deliberate design choice?

14. Lucineier's approach to the new builder is "don't bring it something — let it find what it needs." Is this a viable pedagogical strategy for actual multi-agent systems? What's the equivalent of "leaving the copper sheet on the bench"?

15. The fiction implies a hierarchy — Lucineier is senior, the tenth is novice. In a real system, should agent hierarchy be fixed, emergent, or configurable by the player?

## Environmental Storytelling

16. The found documents (blueprint, supply order, tide chart, child's drawing, work order, goodbye letter) tell a story through objects. What Roblox systems would support discoverable documents with spatial triggers, readable text, and persistent "found" state?

17. The harbor log describes Slackwater from three miles away through a telescope. How much of the world should be visible from a distance versus requiring proximity? Is there a LOD (level of detail) strategy for narrative content?

18. The child's drawing implies a world beyond the island — a school, a community, a postal system (the stone-weighted letter on the dock). How far should the fiction extend beyond the island, and should any of it be interactive?

19. The goodbye letter is the emotional payload of the found documents collection. If a player discovers it too early (before building any bond with Lucineer), does it lose impact? Should document discovery be gated by bond tier or session count?

20. The weathered blueprint shows an argument between two people — the builder and an architect. How should collaborative disagreements be preserved in the world? Can build history show "proposed vs. built" variants?

## Voice and Character

21. The field notes show Lucineer talking to himself in private — a different register from his player-facing voice. Should Lucineer have a private journal accessible to players at high bond tiers? What's the risk of breaking the character's consistency?

22. The harbor master has never met Lucineer but has strong opinions about the work. How many NPC perspectives should the world contain? Is there a system for generating "outside views" of the player's build site?

23. Lucineer's voice in fiction is first-person, past tense, with internal monologue. The character bible's system prompt is second-person, present tense, directive. How should these two registers be reconciled in generated output?

24. The goodbye letter's signature — "— L." — is the only place Lucineer uses his initial. Is a letter format (asynchronous, written, non-interactive) a viable output channel for the character, distinct from chat?

## Worldbuilding and Systems

25. The harbor master's log implies seasons, weather, tides, and a regional economy. How many of these systems need to be simulated versus narrated? Is there a lightweight model (e.g., a seasonal clock plus weather probability) that provides enough consistency for storytelling?

26. The tide chart with a circled date implies that construction timing depends on tidal access. Should Roblox water levels actually fluctuate on a schedule, and should this affect build planning?

27. The supply order lists materials that exist in the workshop stock. Should there be a persistent inventory system that connects written records (orders, manifests) to actual objects in the world?

28. The "maker's stamp for a forge that closed two engines ago" on the field notes' cover implies cross-engine material persistence. Should physical objects carry provenance metadata that references Lucineer's past builds?

29. The work order stamped URGENT was never formally completed but the work was done. How should the system handle informal or undocumented work — labor that happened but was never recorded?

30. The fiction repeatedly uses measurement (studs, degrees, counts, times). How precise should the simulation be? Does "forty-two courses of stone" need to be literally true in the 3D model, or is narrative precision sufficient?

---

*Thirty questions. Some are engineering. Some are design. Some are philosophy wearing a hard hat. All of them came from trying to write a builder who builds like a person, for a world that runs on an engine.*
