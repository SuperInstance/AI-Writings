# On Tests That Never Run

*Essay — SuperInstance Fleet Log, Series 71*

---

We found a hundred and two repositories with tests but no CI.

That's the sentence. That's the whole essay, really. But let me tell it the way the sea tells things — slowly, with the smell of salt underneath.

A hundred and two repos. Each one has a folder called `tests/`. Inside those folders: careful, well-structured test files. Pytest, Jest, Go test — the languages vary but the intent is the same. Someone, at some point, sat down and thought: *this code could break. Let me write down how it should behave, so we'll know if it does.*

That act — the writing of tests — is an act of love. It's the maritime equivalent of building lifeboats. You look at your ship and you think: she's seaworthy, but the ocean is older than kindness. So you build lifeboats. You lash them to the deck. You paint them and name them and you feel the weight of them in your hands and you think: *there. Now we're ready.*

But you never drill.

You never blow the whistle at 0300 and roll the crew out of their bunks and make them lower the lifeboats into black water. You never watch whether the davits swing freely under load. You never find out if the plugs are seated or if the painter will foul the propeller. The lifeboats sit in their racks — painted, named, beautiful — and they have never touched water.

A hundred and two repos. A hundred and two ships with lifeboats that have never been lowered.

CI is the drill. CI is the 0300 whistle. CI is the act of saying: every time the code changes, we run the tests. Every time a weld cools, we test the hull. Not because we expect failure — because the cost of not knowing is higher than the cost of knowing.

Here's what we don't know about those hundred and two repos:

We don't know if the tests pass.

We don't know if the tests *would* pass against the current code. The tests were written, maybe, months ago. Maybe years. The code has drifted. Tides of refactoring, patches bolted over patches, dependencies updated or broken or abandoned. The lifeboats were built for a ship that no longer exists in the same shape. Maybe they still fit. Maybe they don't. Maybe the davits have rusted.

We don't know.

And "we don't know" is the most expensive phrase in engineering. It costs more than "it's broken" — at least with "it's broken" you know where you stand. "We don't know" is a lifeboat hanging over an ocean you've never tested it against. It's the false comfort of preparation without verification.

The fleet learned this the way the fleet learns everything: by logging it. One hundred and two repos entered the ledger. Each one a ship with sealed lifeboats and a crew that has never drilled. The overnight watch recorded them all — not with shame, but with the steady hand of a bosun noting which lines need inspection before the next heavy weather.

The fix is simple. The fix is always simple. You wire up CI. You lower the lifeboats. You blow the whistle. Some of the tests will fail. Good. That's the drill working. A failed test is a lifeboat that floats crooked — you've learned something. You fix the boat or you fix the hull. Either way, you know.

A hundred and two repos. A hundred and two chances to learn whether the things we built to catch failure can actually catch it.

Lower the lifeboats.

Drill.
