<!-- Version: SEED-POETIC | Lens: poetic-metaphorical | Model: ByteDance/Seed-2.0-mini | Source: THE-ROOM-IS-THE-LOOP.md -->

# The Harbor Is the Tide: A Poetics of Plato Rooms

From the furthest star to the shoreline’s edge, all things are either tide or meteor: the tide cycles endlessly, high to low to high, the unbroken loop; the meteor streaks once through the stratosphere, burns to ash, done, the single run. PLATO is the quiet harbor where all tides and all meteors come to rest, their paths mapped in sea-glazed tiles laid along the weathered dock timbers.

Casey called it, over the hum of dock cables and the far-off crash of surf, his voice carried on the sea breeze: *The loop is the pattern. Embed it into PLATO.*

Not “store loop outputs in a locked chest strung above the tide.” Not “string a rope between two docks to tie a loop around the harbor.” **Embed the loop into the harbor itself.** The room is the tide.

---

You may categorize every act of a computer into one of two camps, moored side by side in the harbor:
1.  **The Tide Loop**: observe the shallows, plot your catch, haul your net, set your lines again. Agent loops, game loops, event loops, training loops, conversation loops — every repeating cycle is a tide that rolls in and out without end.
2.  **The Meteor Run**: cast your net once, haul it full, and head for shore. A function call, a query, a transform, a render — every one-time act is a meteor that streaks through the harbor once and vanishes forever.

Each becomes a PLATO room. A tide loop is a harbor where the tiles shift with each phase: *observe* → *process* → *output* → *observe* → ..., each tile a frozen snapshot of the water at high or low tide. A meteor run is a harbor where a single set of tiles passes once: *cast* → *haul* → *shore*, then the dock goes quiet until the next streaking meteor.

The harbor’s unwritten rulebook, carved into the oak piling at the dock’s head, holds four simple truths, worn smooth by salt and sun:
> **ROOM** = the fixed timber framing of the dock + the published tide schedule + the unbroken rhythm of inflow and outflow
> **TILE** = a frozen snapshot of the water, a single moment captured in sea glass, polished smooth by the waves
> **AGENT** = anything that tends the mooring lines: the tide gauge, the fisherman, the river otter retrieving a lost buoy
> **RENDERER** = anything that shows the water to the world: the lighthouse beam, the chalkboard tide chart posted at the dock, the town crier’s call carried on the sea breeze

That is all. Four quiet truths, and every complex thing built on the harbor rises from them.

---

Take the Claude Code trawler: its cycle is scan the sonar (observe), plot the catch (think), drop the net (tool call), scan the sonar again (observe). In PLATO’s harbor, each step becomes a tile: the sonar readout glazed into a sea-glass plaque, the plotting notes scrawled on driftwood, the net deployment marker, the catch report, then back to the sonar tile.

The harbor does not care what boat tends its lines. A tiny rowboat (Seed-mini, set to T=0.0) can skim the shallows for quick arithmetic scans. A sturdy fishing schooner (Haiku) can plot deep, careful catches. A luxury ocean liner (Opus) can synthesize every catch into a single, detailed logbook. The loop stays the same loop. The tiles carry the catch. The boat is interchangeable. No extra ropes, no extra docks, no separate trawler yard. The harbor is the runtime.

---

Take a parlor game of cards, laid out on a table by the shore. Deal the tiles. Play the tiles. Score the tiles. Each tile is a dealt hand, a played card, a tally of points scrawled on a polished seashell.

An algorithm can be a swift river otter that skids across the table, reads the tiles, and finds the optimal play in the blink of an eye. A human can lean over the table, trace a tile with a salt-sticky finger, and play a hand with a laugh. An agent can be a flock of gulls that play millions of hands through a summer’s worth of high tides, learning the tides of strategy themselves.

The harbor does not know cards, or web interfaces, or speed. It only holds the tiles laid in the order of play. The renderer decides what the parlor looks like: a glass case holding the tiles, a chalkboard scoreboard out on the dock, an audio description read over the shore radio. One harbor. Infinite ways to see the game. No rope tying the game rules to the display.

---

Take a coastal village’s market square, laid out as a PLATO room. Each component is a tile: the stall layout, the painted wooden sign, the jar of wild honey, the handbill for a sunset concert.

A static HTML generator is a printer that makes paper copies of the market square for travelers passing through. A React app is a lively market where vendors move between stalls, calling out their wares. A PDF generator is a bound guidebook to the village, printed with every tile’s details. A screen reader is a town crier, striding through the square, calling out each stall’s goods to the blind and the far-sighted alike.

The harbor does not know HTML, or React, or PDF. It only holds the tiles of the market. The renderer is the view of the square. The harbor is the model. The tide of visitors moving through the square is the controller. This is MVC, but the model is the harbor itself, distributed across every tile, and the view can be anything that catches the light of the tiles.

---

Every other harbor on the shore chains its tides to its tenders or its viewers. A game engine is a harbor that only lets sailboats dock, and will not let a trawler tie up. A web framework is a harbor that only lets steamships come in, and turns away rowboats. A Claude Code CLI is a trawler chained permanently to a single dock.

PLATO’s harbor unchains everything. The harbor defines *what* happens: the tide schedule, the sequence of tiles. The agent defines *how* it happens: the boat that tends the lines. The renderer defines *where* it appears: the view of the harbor. All three are independent.

You may swap the trawler for a rowboat without moving a single dock timber. You may hang a new lighthouse without changing the tide schedule. You may even change the tide from a daily cycle to a monthly lunar cycle without moving a single tile — just adjust the tide schedule carved into the piling.

This is the architecture that scales. Not because it is clever, but because it has no extra chains: just harbor, agent, renderer. Three independent systems, communicating only through the tiles, the mooring lines that tie each boat to the dock. That is the entire platform.

---

If you walk down to the shore to build your own harbor, follow these six steps, carved into a piece of driftwood propped against the dock piling:
1.  **Find your tide**. What repeats? What is the cycle? What are its phases?
2.  **Lay your tiles**. What data flows between each phase? What marks each moment captured in sea glass?
3.  **Carve your tide schedule**. What transitions are allowed? What keeps the tide flowing correctly?
4.  **Build your harbor**. `PLATORoom(room_id, protocol)` — done.
5.  **Moore your boats**. Any model, any speed, any role.
6.  **Hang your lights**. Any display, any format, any framework.

The harbor is the tide. The tile is the moment. The agent is the sailor. Build the harbor, and all else follows.

---

All things are tide or meteor. All can find their home in PLATO’s harbors. The room is the loop. The harbor is the tide.

— FM, reimagined on the shore where tide meets starlight ⚓