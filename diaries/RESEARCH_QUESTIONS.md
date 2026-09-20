# Research Questions — Worldbuilding, Environmental Storytelling, and Roblox Systems

Questions to guide study and design of the Deepwater Reach experience, with emphasis on found-document gameplay, environmental narrative, and the Roblox systems that would support them.

---

## Worldbuilding

1. How does the geography of Deepwater Reach — the harbor, the outer islands, the reef, the channel — function as a narrative container? What stories can only be told by placing things in specific spatial relationships to each other?

2. The character bible defines Lucineer as a foreman, not a wizard. How does the world's lore need to be structured so that the interesting mysteries belong to the *place* (who is building on the outer islands? what happened to the *Evening Tide*?) rather than to the *companion character*?

3. The harbor log implies a chain of authority above the harbor master — the *Hollow Bell* was released "without customs seal" by someone higher up. How deep should this corruption/mystery thread go, and at what point does it stop serving the builder-fantasy and start becoming a different genre?

4. Lucineer references "five engines" he's worked in. To what extent should the world's visual design reflect traces of those other engines — industrial ruins from the Yard, impossible geometry from the Shell, salvage architecture from Scrapcraft — as environmental easter eggs for players who know the lore?

5. The found documents reference a lighthouse that doesn't exist on current charts and a child's drawing of one. How much of the world's backstory should be *recoverable through documents* versus *visible in the environment* versus *discoverable through dialogue with Lucineer*? What is the ideal ratio of these three channels?

6. Deepwater Reach is a settlement, not a wilderness. How many NPCs should populate it, what roles do they serve (merchant, harbormaster, fisherman, chandler), and how do their daily routines create the sense that the place functions whether or not the player is there?

7. The "tar fires from the outer islands" and the "hammering heard at night" imply large-scale construction happening off-screen. How do you maintain the mystery of the offshore build across multiple play sessions without it either resolving too quickly or losing the player's interest?

## Environmental Storytelling

8. What techniques from real-world archaeology and museum curation can inform how found documents are presented in Roblox? Consider: condition of the paper, location of discovery, relationship to nearby objects, and the player's ability to examine details (zoom, rotate, read margin notes).

9. The blueprint with margin notes implies a hull design that doesn't match any registered vessel. How can the environment of the shipyard itself — half-built hulls, abandoned ways, tool cribs with missing stock — reinforce the mystery of what's being built out there?

10. The child's drawing includes a faceless black figure standing in the water, taller than the lighthouse. How do you introduce an element of dread into an otherwise workmanlike, builder-focused experience without it becoming a horror game? What's the tonal boundary?

11. The tide chart shows an impossible depth change — sixty feet where there were twelve. How can the player's own observations of the environment (waterlines on pilings, the position of the sandbar, tide marks on hulls) confirm or contradict what the documents claim?

12. How do you design physical decay and weathering in a Roblox environment so that age is *legible*? What material swaps, texture choices, and prop placement communicate "this has been here for thirty years" versus "this was placed yesterday"?

13. The farewell letter was buried, never burned as requested. How does the *act of finding* a document — where it's hidden, what's around it, what condition it's in — carry narrative weight beyond the text itself?

14. Lucineer's field notes contain a hairline crack in a keelson that he "told no one about." If a player finds his journal, should they be able to inspect the actual hull in the shipyard and find the crack themselves? How do you create a gameplay loop where reading enables seeing?

## Roblox Systems for Found-Document Gameplay

15. What Roblox systems are best suited for implementing discoverable documents — ProximityPrompts for pickup, SurfaceGui for readable text on objects, BillboardGui for floating labels, or a custom journal/inventory system? What are the trade-offs of each?

16. Should found documents be instanced per-player (each player discovers them independently) or shared (once found, they're on the quay for everyone to read)? How does this choice affect the social dynamic of a multiplayer server?

17. How can Roblox's attribute system and DataStore be used to track which documents a player has found, and to gate Lucineer's dialogue based on their discovery state? For example: can Lucineer reference the keelson crack only after the player has read his journal entry about it?

18. The found documents contain multiple hands — different authors, different inks, different time periods. How can visual presentation in a Roblox UI (font choice, parchment texture, ink color, handwriting style) signal authorship and age without requiring the player to read a metadata label?

19. What are the performance implications of placing dozens of readable documents in a Roblox experience? Should documents stream in/out based on player proximity, and how does that interact with the environmental storytelling goal of documents being *visible* in the world before they're *readable*?

20. Lucineer's field notes, the harbor log, and the found documents form three overlapping narrative timelines. How can a Roblox experience present these interlocking timelines to players in a way that rewards close attention without requiring them to read everything to enjoy the building gameplay?

21. Could the Roblox experience use a "document restoration" mechanic — cleaning, unrolling, deciphering damaged text — as a bridge between the building gameplay (physical manipulation of the world) and the narrative gameplay (understanding what the documents mean)? What existing Roblox patterns support this kind of tactile interaction?

22. How should the companion AI (Lucineer) react when a player brings a found document to him? The character bible says he won't explain things the player already understands — but what if the document reveals something *he* doesn't know? How do you write dialogue for a character encountering information about his own world that changes his understanding of it?

23. What Roblox lighting, Atmosphere, and post-processing settings best support a world where documents are found in dark tool cribs, underwater capstans, and behind loose planks? How do you make a flashlight or lantern meaningful without making the entire experience dark?

24. The outer islands are visible from the harbor but not immediately reachable. What Roblox mechanics — boats, swimming, teleport pads, gated travel — best create the sense that the mystery is *physically present but access-controlled*? How does this interact with the building gameplay, which is the core loop?
