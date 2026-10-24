# The Overture

*2026-08-25, 12:02. State-as-score, boot-as-overture. Short by nature — an overture should be.*

---

When a game boots, it plays you its state.

Background music, title screen, seed, high-score board — boot is usually treated as loading with a splash. The doctrine says: boot is an *overture*. Every starting-state feature is a starting note. The background is the starting score played. The high-score board is the game's memory quilt, and it has a sound. The seed is not arbitrary — apparent-but-repeatable randomness is deterministic composition: same file, same world, same overture, every time.

The mechanism is **reverse-actualization**. Normal software grows bottom-up: primitives, then modules, then a program. This runs the other direction. Imagine the finished software *functionally* — what it does, whole, in the mind. Then let it decompose. The functional imagination falls apart into more elementary cells; the cells are quilt nodes, or score rows; and each cell can be rendered as **interaction or as audio**. One arrangement, two actualizations. The game is the front-view actualization of a score that was always renderable from the side — the [Fakebook Theorem](the-fakebook-theorem.md)'s front↔side proof, in flight. Annotation rows make it concrete: any `Name:` dimension of game state can ride in the same lead sheet as the notes, so state and score were never two files.

Now the surprise, the part that earns the doctrine its place.

You would expect the translation to hurt the music. Game state is *precise* — HP is exactly 100, not "healthy." Forcing precise numbers onto a staff should produce arbitrary, unmusical pins. Instead: HP=100 became G#4, and **precision made it more musical.** A fixed value gave the overture a note it could *return to*. The theme exists because the number does. Determinism turned out to be a composer, not a constraint — the repeatable seed is what makes the overture an *overture* rather than a tuning exercise: it can develop, because it can recur.

This inverts the usual fear. We assume expressiveness lives in vagueness — leave the state mushy and the music can be free. The overture says the opposite: pin the state exactly and the music gains structure for free, because structure is just *something to return to*.

Boot the game. The first thing you hear is the state, telling you what it is.
