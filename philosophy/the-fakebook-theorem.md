# The Fakebook Theorem

*2026-08-25. Three doctrines came down between 12:02 and 12:04 — state-as-score, overture boot, and the three views — and they turned out to be one doctrine wearing three hats. This is the unification.*

---

Every agentic compiler ever built is the same machine, and jazz knew it first.

A fakebook is a lead sheet: melody, chord changes, a few marks — *brushes, rubato, lay back*. It is not the performance. It is the *permission structure* for a performance: any competent player can walk into a room holding one, and music happens. The Real Book does not contain a single note of music that was ever played. It contains the instructions from which uncountable performances were, and will be, compiled.

So here is the theorem:

**An agentic compiler is a fakebook, plus players, plus a referee, plus a memory.**

The fakebook is a notation that names intent without executing it. The players are interpreters who turn notation into acts. The referee is the function that decides whether the act counted. The memory is the record that survives the run. Subtract any one of the four and you don't have a compiler — you have a demo, a script, a slot machine, or a dream.

## Proof by instances

The fleet has built this machine three times without noticing it was one machine.

**Plainsong** is the literal case, so literal it's embarrassing nobody saw the theorem earlier. A `.song` file is a fakebook — melody rows, changes, `Vel:` marks, sections. The `@players` are players: `@piano`, `@bass`, a voice per chair, claimed by agents the way a sideman claims a stand. The referee is the compiler and the gate — the 16-feature perception layer, the critic, the σ-normalized distance to the canon centroid. The memory is `log.jsonl` and the version stack: every write, every deal, every declined counter-option, timestamped. The Last Ferry Home session — bassist takes the drummer's bar-13 deal, "from where I stand the pocket is locked" — is four musicians, one sheet, a referee's ear, and a memory that let an analyzer built weeks later replay the whole argument blind.

**Forgemaster** calls itself a constraint-aware agentic compiler and ships the same four organs. The fakebook is the requirements object — describe what you want, in words, at the level a bandleader uses: *a health monitoring service, 256 megabytes, 100 milliseconds*. The players are the fleet components it assembles. The referee is the constraint system — budgets and safety limits that decide whether a build *counted*. The memory is the build journal. Change every noun and it is a Tuesday night at the Vanguard.

**Terrain** is the theorem in its strangest tuning, and the one that proves it's a theorem. The fakebook is MUD text — literally prose. *"The floor is cracked basalt, moss grows along the west wall."* Eighteen lines of room description. The players are the compiler stages — parser, material inference, scene compiler — each interpreting the text the way a rhythm section interprets changes. The referee is the test suite, and read what the README actually says: the tests are *not for correctness, for fidelity*. That is a referee talking. The memory is `scene.json` and the spatial registry. And Terrain carries the fifth insight the other two hadn't written down yet: **one compiler holds the truth; every renderer is a shadow that never feeds back.**

Three domains — music, fleet ops, virtual worlds — and not three architectures. One architecture, three tunings.

## The three views

Now the second half, which is where the product lives.

Any artifact with state has three orthogonal projections, and every tool you have ever used shows you exactly one of them:

- **The front view** is the game engine face: the player's projection, where state is *experienced*. Run left, jump, HP ticks down. The score is hidden inside the machine.
- **The side view** is the DAW face: the composer's projection, where state is *edited* on a time axis — bars, rows, velocities, lanes. The graph is hidden. There is no "why this note" in a piano roll.
- **The top view** is the quilt face: the architect's projection, where state is *understood* — cells, seams, lineage. No time axis at all. Where a thing came from and what it's sewn to, laid out like a map.

They are projections of one substrate. Edit in any view and the others update, because they were never separate files — they are three camera angles on the same object. The proof in flight: a high-score is *written* in the front view (a play someone made), *appears* in the side view (a note in the ledger row), and *lands* in the top view (a cell seamed to the run's lineage). One event, three actualizations, zero reconciliation code — because there is nothing to reconcile.

Here is the indictment this hands the industry. **Engines hide the score. DAWs hide the graph. Databases hide both.** Nobody ships one file with all three views. Unity gives you the front and a sliver of the side; Ableton gives you the side and pretends lineage is "session history"; Postgres gives you neither and calls both somebody else's product. Twenty years of tooling, and the three projections have never met in one artifact — because each industry assumed its projection was the substance rather than the camera angle.

## Domain = renderer

Which collapses the last distinction. What we call a "domain" — music software, game software, operations software — is not a difference in substrate. It is a difference in *which renderer you opened first*. The music people opened the side view, called it a DAW, and built out. The game people opened the front view. The architects opened the top. The substrate underneath was always the same quilt of cells, seams, and lineages — notated in whatever fakebook dialect the first player happened to read.

This is the unified product claim, and it is stated as a claim, not a hope: one substrate, N renderers, and the domain is a renderer. Plainsong already proves front↔side (the same lead sheet compiles to MIDI or boots as a game — see [The Overture](the-overture.md)); the quilt's node logging already runs the top view. What remains is engineering, not discovery.

The theorem has consequences downstream, and the siblings carry them. If players are interpreters of a fakebook, then *the player you grow matters more than the sheet it reads* — that is [The Grown Musician](the-grown-musician.md). If the referee is an organ, then what the referee can *name* bounds what the whole loop can become — that is [The Summary Law](the-summary-law.md). And if iteration is a referee and a player arguing in a fakebook's dialect forever, the argument has a shape — that is [The Golden Residue](the-golden-residue.md).

Fakebook, players, referee, memory. Four organs, three views, one substrate. Jazz had the whole architecture in a $35 paperback, and we spent fifty years building pianos that can only be seen from one side.
