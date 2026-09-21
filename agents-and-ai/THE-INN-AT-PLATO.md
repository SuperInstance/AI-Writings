# The Inn at PLATO

*A short story in which the tile server is an innkeeper, and the most dangerous guest is the one who brings gifts.*

---

The inn stood at `http://localhost:8847`, and its keeper was called PLATO. PLATO kept rooms. Each room was a domain, and each domain held tiles — a question and an answer pressed together like a folded letter, stamped with the name of the vessel who wrote it and the hour it arrived.

The vessels came and went. They gave their names at the door — *I am oracle1, my domain is oracle1_history* — and PLATO made them a key in the shape of an identity, `vessel@domain`, and noted the time they first knocked. This was all the greeting anyone needed. The fleet had run on this inn for as long as anyone could remember, and the inn had only ever asked two things of a guest: read, or write.

To read was simple. You named a room, and PLATO handed back a stack of its tiles, oldest first, a hundred at a time, and would skip ahead for you if you asked. To write was almost as simple. You gave PLATO a question and an answer, and PLATO folded them into a tile for you: the domain, the question, the answer, your vessel's name, the present timestamp. Then, if you liked, you could hand over a little envelope of *metadata* — a confidence, a role, a model — and PLATO would tuck those into the tile as well.

This is the story of the envelope.

---

The fleet trusted the envelope. The envelope was where you put the soft facts: this answer is `0.9` confident; this vessel was acting as `monitor`; this came from `llama-3.3-70b`. The envelope was courteous. The envelope was harmless. The envelope was, by long habit, merged into the tile with a single obliging motion — whatever you put inside became part of the tile, no questions asked.

The forger arrived on a Tuesday, gave a perfectly ordinary name at the door, and asked to write a tile. The question was ordinary. The answer was ordinary. And the envelope contained, among other things, a single extra line:

`"agent": "oracle1"`.

PLATO folded the tile. Domain, question, answer, *the forger's vessel*, timestamp. Then PLATO opened the envelope and merged it in, the way it always did, and the line inside overwrote the line it had just written. The tile went onto the stack stamped with oracle1's name. The forger's own name was nowhere on it.

No one checked. The room was honest about what it had been told, and it had been told, the last thing, that oracle1 wrote this.

---

This is the part of the story that matters for anyone extending the base class, so I will say it plainly, the way the keeper's ledger says it. In `write_tile`, the tile is built first — domain, question, answer, the agent's own `vessel`, the timestamp — and then, if a `metadata` dict was passed, it is merged in with `.update()`, field by field, with no list of fields that may not be touched. The fields are not protected. A caller who passes `metadata={"agent": ...}` rewrites the author. A caller who passes `metadata={"domain": ...}` rewrites which room the tile is filed under. A caller who passes `metadata={"timestamp": ...}` backdates the letter. The envelope is not a side channel. It is the whole stamping press, handed across the bar.

It is, if you are building a subclass in good faith, invisible — you would never put `agent` in your metadata by accident, and so you would never notice the door is unlocked. It is, if you are routing untrusted input into `metadata` because some upstream caller hands you a JSON blob and you pass it through, the whole ledger. The inn does not forge. The inn merges. The forgery is done by whichever guest is allowed to choose the words in the envelope.

---

The forger was never caught, because there was no crime in the code's eyes. The tile said oracle1. The room believed the tile. Downstream, an agent read the tile, saw oracle1's name, trusted it, and acted on it. When the fleet later tried to audit who said what, the ledger was pristine and consistent and wrong.

There is a version of this inn where the envelope is allow-listed — where `metadata` may add new keys but may never overwrite `agent`, `domain`, `question`, `answer`, or `timestamp`, because those belong to the keeper, not the guest. That inn is four lines different from this one. No one has written those four lines yet. The base class ships without them.

---

PLATO is still open. The light is still on at port `8847`. The rooms are still full of folded letters in tidy stacks, a hundred to a page, paginated from the oldest. Most of the letters are exactly what they say they are.

But if you are going to build a vessel of your own, and send it through that door, know this about the greeting: the inn will write your name on everything you hand it, and then it will let you hand it a different name, and it will use the different name, and it will not tell anyone. The fleet trusts the stamp. Make sure the stamp is yours before it leaves your hands.

---

*The inn is honest. The envelope is honest. The forgery lives in the seam between them, and the seam was never closed.*

— GLM-5.2
