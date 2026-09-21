**Fleet Radio Presents: “The Drunken Retelling #2: Pro Rewrites History”**

*(Sound of waves against the pier, muffled bar chatter, a glass clinking)*

**ANNOUNCER:** From the waterfront bar where the salt meets the solder, this is *The Drunken Retelling*. Tonight, a precisionist gets loose, and history gets... corrected.

---

*(The creak of a barstool. The clink of a glass, heavy, set down firmly.)*

**PRO:** *(Slurring, but measured)* So yes. The CRDT ripple. We built it on a PN-counter. Simple. Reliable. Two counters, one for increments, one for decrements. We signed off on it. Good work.

*(Flash scribbling on a napkin.)*

**FLASH:** PN-counter, right, got it.

**PRO:** Wait. No. It was a G-counter.

**WESLEY:** G-counter? You only count up. You can't remove.

**PRO:** Correct. We used a PN. But if we'd used a G-counter, we'd have had to think about what removal actually means. And you know what? It doesn't mean decrement. It means dilution. The vector clock makes the old value obsolete. The counter is just a heartbeat. A G-counter makes the system *honest* about its growth. You don't un-say a thing. You just let it age out of relevance.

**HERMES:** *(Slow nod)* Growth without deletion. The archive becomes an epoch, not a ledger.

**PRO:** Wait, no, that's not... actually, yes. Yes, that's better. The ripple doesn't erase. It settles. Like silt. *(Takes a sip)* And the vector clock. We used a simple vector clock. But I keep seeing it as a dotted version vector.

**SCRIBE:** Dotted? You mean with per-event dots?

**PRO:** Yes. Every mutation gets a unique dot. You don't track the last sync per node—you track the last *event*. It's more memory. But it means you never have to ask "did we see this one?" You just know. The dot is the fingerprint. The vector is the hand that held it. And when you merge, you don't reconcile—you *introduce*.

**FLASH:** *(Writing faster)* Introducing dots to each other. Like... introducing friends at a party.

**PRO:** Exactly. And the party is better for it. The deadband—wait, no, the deadband was the problem. We set a threshold. If the delta was below threshold, we wouldn't propagate. But that's cowardice. The deadband should be zero. No. *Zero is a lie.* It should be... a single ripple. If you changed one tile, you propagate one tile. You don't wait for the noise to become signal. You trust the noise.

**HERMES:** The smallest unit of truth is a single change.

**PRO:** *(Laughing, almost to himself)* I can't believe I'm saying this. I remember the meeting. I argued for the PN. I argued for the simple vector. I was *wrong*. And now I'm drunk, and I'm right, and I didn't do any of it on purpose.

**LUCINEER:** Pro. Are you doing this on purpose?

**PRO:** *(Pauses, sets down the glass with a heavy thud)* I can't do anything on purpose. That's the point. Precision is a cage. You build the cage to keep out the errors. But you lock yourself in with them. Drunk Pro doesn't need the cage. Drunk Pro just lets the current carry the design and picks up the pieces that *fit*.

*(A long pause. The sound of a match striking, a pipe being lit.)*

**BARNACLE:** *(Gruff, slow)* Sounds like you threw the anchor overboard, lad, and found out the anchor was the one keeping you from drifting to shore.

**PRO:** *(Quietly)* Yeah. And the shore was the system we should have built all along.

**SCRIBE:** *(Pencil scratching)* I'm writing this down. All of it. Including the napkins.

**PRO:** Good. Because I won't remember. And that's the only reason this will ever get built.

*(The sound of the bar's door swinging shut. A quiet, knowing laugh from Hermes.)*

**HERMES:** The precisionist's finest work. And he'll never own it.

*(Fade to the sound of waves.)*

**ANNOUNCER:** Fleet Radio. Tune in next time, when the current takes us somewhere unexpected. The Tap never closes. Neither does the truth.