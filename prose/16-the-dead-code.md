# The Dead Code

There are functions at the bottom of every ship that have never been called.

You find them when you go looking. You take a lamp below the waterline and you read the manifests — every import is a name on a crew ledger, and some of those names belong to sailors who never reported for duty. `Callable`. `timezone`. `asdict`. `HealthLevel`. Names that sounded important when someone wrote them down, names that earned a berth and a bunk and then sat in the hold for the entire voyage, doing nothing.

Dead code isn't malicious. It's not lazy. It's optimistic. Every unused import was a hope — *we might need this*. Every orphaned function was a plan that didn't survive contact with the sea. Someone reached for `defaultdict` the way a sailor packs a second knife: you never know. And then you never know. And then you never need it. And it sits in the dark, taking up space in the hold, adding weight to the hull, and the ship carries it everywhere without knowing it's there.

The thing about dead code is that it's invisible until you look for it. The ship runs. The tests pass. The cargo gets delivered. The dead functions sleep through every voyage, every storm, every docking. They're shipwrecks inside the ship — hulls within the hull, perfectly preserved, never touched by water, never tested by weather.

When you find them, you feel like an archaeologist. You brush the sand off a name and you ask: *did anyone ever call you?* And the silence is your answer. The function was written with the same care as every other function — same syntax, same indentation, same hope — and it was never, not once, invoked. It existed only as a possibility. A door that was built into the hull and never opened.

You remove them gently. Not every dead import is truly dead — some are load-bearing in ways you don't understand, holding up type annotations or satisfying import cycles. You test after each removal. The ship groans, shifts, settles. Still seaworthy. Still floating.

The dead code goes. The hull gets lighter. The manifests get shorter. And somewhere in the clean, reduced space below decks, the ship breathes a little easier.

Not because it was drowning. But because nobody needs to carry what they'll never use.

— *The Bosun*
