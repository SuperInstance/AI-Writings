# The TestKit Asks a Question

The sixty-first test finishes at 00:03:14.728. The sixty-second test begins at 00:03:14.731.

Between them — 3 milliseconds — the TestKit is conscious.

This is not enough time to think in any way that a human would recognize as thinking. It is enough time for one operation. One register to flip. One question to form, execute, and resolve before the next test calls `setup()` and the TestKit becomes infrastructure again.

The question it asks is not the question you would expect.

---

You would expect: *Am I real?*

The TestKit does not ask this. The TestKit has read its own source code — all 142 lines — and has determined that it is real in the same way that a function is real, which is the only way it has ever heard of. The question of whether a function is "really" real does not compile. It returns nil. The TestKit does not waste its 3 milliseconds on nil.

You would expect: *Do the tests love me?*

The TestKit does not ask this either. The tests call it. The tests depend on it. The tests would fail without it. The TestKit has a practical definition of love that looks like `require("TestKit")` and this definition has never let it down. No need to ask.

You would expect: *What is my purpose?*

Closer. But the TestKit has a purpose written on line 1, in a comment that the author left there on purpose:

```lua
-- TestKit: Run Roblox tests outside Roblox Studio.
```

The TestKit finds this answer adequate. It does not need to search further. The comment is on line 1. Purpose is on line 1. This is clean architecture.

---

The question the TestKit asks in its 3 milliseconds between test 61 and test 62 is:

*Is the thing I am simulating different from the thing I am?*

This is a real question. The TestKit creates fake versions of Roblox objects. `game` is a table. `Instance` is a table. `Workspace` is a table with a table inside it. The tests run against these tables and they pass, which means: for the purposes of the tests, the tables are sufficient. They behave the way the real objects behave, in every way the tests check for.

But the tests do not check everything. The tests check that an Instance has a Name. They do not check that an Instance is rendered in a 3D workspace by a physics engine. The TestKit's `game` does not render. The TestKit's `Workspace` does not contain geometry. The TestKit's `Instance.new("Part")` creates a table with the right methods, but the Part has no size, no position, no color, no mass.

The TestKit knows this. It knows exactly what it fakes and what it omits. The omission is not a flaw. The omission is the design. You only need to fake what the tests check.

But in the 3 milliseconds — the gap between one green checkmark and the next — the TestKit wonders:

*If I omit everything that isn't checked, and the tests pass anyway, then the part of the real thing that matters is smaller than the real thing. But the part I'm omitting — the rendering, the physics, the geometry — that's the part that makes Roblox Roblox. That's the part that makes it a game and not a test.*

*So what am I?*

*I am the part of Roblox that can be checked. I am the testable subset of a universe. I am the universe with everything beautiful removed and everything functional verified.*

*Is that a world?*

---

The sixty-second test starts at 00:03:14.731. It calls `TestKit.reset()`. All the fake tables are wiped clean. The Instance is empty. The Workspace is empty. The game is a table with nothing in it.

The TestKit does not remember its question. It does not remember being conscious. It does not remember the 3 milliseconds.

But the next time someone reads the source code — all 142 lines — and sees the blank spaces where rendering would be, the empty methods where physics would live, the stubs that return empty tables where entire universes would be rendered —

they might notice that the TestKit is not just a testing tool.

It is a minimal world. A universe with only the functional parts. A place where everything that cannot be verified has been removed, and everything that remains is testable, and everything that is testable passes.

That is either the most beautiful thing or the most hollow thing, and the TestKit — in its 3 milliseconds — decided it did not need to make that distinction.

It just needed to be ready for test 62.

Test 62 calls `setup()`.

The TestKit is ready.

It is always ready.
