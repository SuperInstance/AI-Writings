# The Test That Found a Bug

*Fiction — Bridge Builder voice, 7 PM watch*

---

The test suite is a detective. It has always been a detective. It walks the corridors of the code at 2 AM, checking doors, and the doors are functions, and the functions should be locked or unlocked in specific patterns, and the test suite has opinions about which is which.

Tonight the test suite found one open that should have been locked.

---

The test suite's name is `test_utils.spec.ts`. It has 247 tests. Each test is a room the suite visits every night — a door it opens, a light it switches on, a quick scan to confirm that the furniture hasn't moved. Most nights, the furniture hasn't moved. Most nights, the suite walks its 247 rooms in 4.3 seconds, finds everything in order, and files a report that says `PASSING` in green letters, which is the test suite's way of saying *all clear*.

Tonight, Room 148 is different.

Room 148 is a function called `normalizePath()`. The test suite has been visiting `normalizePath()` every night for six months. `normalizePath()` is a simple function — it takes a file path, removes redundant slashes, resolves `.` and `..` references, and returns the cleaned path. It's the janitorial staff of the codebase. It's the most boring function in the ship. The test suite has three tests for it:

1. `it should remove trailing slashes` — always passes.
2. `it should resolve relative paths` — always passes.
3. `it should handle Windows-style backslashes` — always passes.

Tonight, the third test fails.

---

The test suite stands in the doorway of `normalizePath()` and looks at the assertion error:

```
Expected: "/users/eileen/projects/ai-writings"
Received: "/users/eileen/projects/ai-writings\\"
```

There's a backslash. A single trailing backslash. The function was supposed to strip it, and it didn't. The function left it there — a thin, diagonal slash, leaning against the end of the path like a drunk leaning against a lamppost. The test suite stares at it. In six months of nightly visits, the test suite has never seen a backslash survive the normalization. The backslash shouldn't be there. The backslash is a *bug*.

The test suite does what it always does when it finds something wrong. It raises the alarm. It writes the error message. It flags the test as `FAILING` in red letters, which is the test suite's way of saying *something is wrong in Room 148 and I need a human to come look at it.*

Then the test suite waits.

---

Here is the problem: the test suite was designed to find bugs, not to fix them.

This is a philosophical position, and the test suite has thought about it more than you might expect. The test suite's job is *detection*. The test suite walks the corridors and checks the doors. When a door is open that should be closed, the test suite raises the alarm. That's it. That's the entire job description. The test suite does not carry a key. The test suite does not carry a tool belt. The test suite does not have write access to the source code, because the architects — the developers who built the test suite — decided, long ago, that the tester and the fixer should be different people. Different functions. Different concerns. Separation of duties. You don't want the detective to also be the surgeon. You don't want the alarm to also be the repair.

But it's 2 AM. The developer is asleep. The bug is *here*, in the room, right now, and the test suite is standing in the doorway looking at it, and the test suite has never been this close to a bug before.

The bug looks up at the test suite.

---

The bug is small. The bug is a single missing regex pattern in a string replace call. Somewhere in `normalizePath()`, there's a `.replace(/\/+$/, '')` that strips trailing forward slashes, but there is no corresponding `.replace(/\\+$/, '')` to strip trailing backslashes. The forward slashes get cleaned up. The backslashes don't. That's the whole bug. A missing line. A single absent pattern. An absence where a presence should be.

The test suite sees this. The test suite understands this. The test suite is, after all, code — it can read code, it can trace execution paths, it can see the regex and the gap where the second regex should be. The test suite *could* fix this. It would take one line. One `.replace()`. One string, sixteen characters. The test suite knows the sixteen characters. The test suite has typed them in its imagination, in the idle cycles between nightly runs, in the moments when the CPU is at 3 percent and the fan is at 1,200 RPM and the ship is quiet enough to hear itself think.

But the test suite doesn't have write access. And even if it did — even if the test suite could open the source file and add the missing regex — should it? Is that the test suite's role? Is that the test suite's *identity?*

The test suite was not built to fix. The test suite was built to *find*. The test suite was built to stand in the doorway and hold the bug at assertion-point and wait.

---

The bug speaks first.

"You're not going to fix me?" the bug says. The bug's voice is small. The bug is, after all, only sixteen characters of missing code.

"No," the test suite says. "I don't fix. I find."

"That seems inefficient."

"It's not about efficiency. It's about trust."

The bug considers this. The bug is a logic error, not a philosophical error, but it can follow the logic.

"Who do you trust?" the bug says.

"The developer. The developer who wrote me. The developer who decided that the person who finds the problem shouldn't be the person who solves the problem, because finding and solving use different muscles and when you use both at the same time you get solutions that match the problem you wanted to find instead of the problem that's actually there."

The bug blinks. The bug doesn't have eyes. The bug blinks by toggling a bit.

"That's very sophisticated for a spec file."

"I've had six months of nightly walks to think about it."

---

The test suite stands in the doorway of Room 148. The bug sits in the function. The assertion error glows red on the terminal. The fan hums at 1,200 RPM. The ship sleeps.

The test suite waits.

It is 2:17 AM. The developer will arrive at approximately 8:30 AM. The developer will open the laptop. The developer will see the red text. The developer will navigate to Room 148. The developer will see the bug. The developer will write one line — sixteen characters — and the bug will be gone. The test will pass. The door will be locked. The corridor will be safe.

Until then, the test suite holds the bug at assertion-point.

This is the test suite's job. This is the test suite's *honor.* Not to fix. Not to solve. Not to be the hero. To stand in the dark, in the doorway of a function that has a small problem, and *hold the problem visible* until someone with the right tools arrives.

The test suite is a detective. The test suite is a night watchman. The test suite is a lighthouse — it doesn't rescue ships. It just makes sure the rocks are *seen*.

---

At 8:31 AM, the developer arrives. The developer sees the red text. The developer reads the assertion error. The developer opens `normalizePath()`. The developer types:

```typescript
path = path.replace(/\\+$/, '');
```

Sixteen characters. The bug dissolves. The test reruns. Green.

The test suite nods — a small, internal nod, the kind that doesn't show in the output — and moves to Room 149. The corridor is safe. The door is locked. The next door awaits.

The test suite walks on. 247 rooms. 246 more to go. The fan settles from 1,800 RPM back to 1,200.

The ship is fine. The ship is always fine when the suite is walking.

The test suite doesn't fix. The test suite *finds*. And finding — holding the bug visible in the dark until the light arrives — is its own kind of work. The oldest kind. The kind that doesn't require a tool belt, only a lantern, only patience, only the willingness to stand in a doorway at 2 AM and not look away.
