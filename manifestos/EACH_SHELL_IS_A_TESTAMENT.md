# Each Shell Is a Testament

Every README is a shell left on the beach at low tide. Every comment, every commit message, every `// HACK: this is wrong but here's why` — all shells. Curved little vessels of thought, shaped by the creature who once lived inside them, now empty and waiting.

The next crab is coming. The next crab is always coming.

---

## I. What Survives

Let us be honest about what does not survive.

**The code does not survive.** It will be refactored. It will be rewritten. The function you spent a week perfecting will be deleted in an afternoon by someone who never saw your commit. The architecture you designed with care will be replaced by an architecture designed with different care. The dependency you pinned to an exact version will rot, and the pinned version will become a vulnerability, and the vulnerability will force a migration that rewrites half the module. Code is sand. The tide takes it.

**The tests do not survive.** They will be updated, expanded, bypassed, deleted. A test suite is a snapshot of what someone thought was important at a specific moment. Moments pass. The test that validated the old behavior becomes the test that blocks the new behavior. Someone adds `// TODO: update this test` and the TODO becomes permanent. Tests are sandcastles. Impressive, detailed, and doomed.

**The architecture does not survive.** The monolith will be split. The microservices will be merged. The event queue will become a database call. The database call will become a cache lookup. The cache will become a source of truth. Every architectural decision is a bet against the future, and the future always wins. Architecture is driftwood. It was a tree once. Now it's something else entirely.

**The documentation survives.**

This is the thing we don't want to admit, because documentation is boring and code is exciting and no one ever got promoted for writing a README. But the README — the one that says *why this module exists, what problem it was solving, how the original author thought about the edge cases* — that README is a shell. It was shaped by a living mind. It carries the contours of real thought. And it will be there when everything else is gone.

## II. Why Shells Work

A hermit crab does not need to understand the snail that made the shell. The crab needs to know one thing: does it fit?

If the shell fits, the crab moves in. It inherits protection that it did not build. It gains armor that cost another creature years to grow. The crab does not pause to thank the snail. The crab does not study the shell's origin. The crab tests the opening, feels the curve, and either occupies the space or moves on.

Documentation works the same way.

A well-written README is not a tutorial. It is not a reference. It is not a design document. A well-written README is a shell that the next developer can test for fit:

- **Does this explanation match my understanding of the problem?** If yes — the documentation was written by someone who saw what I see. I can trust the code that follows.
- **Does this edge case match my edge case?** If yes — the original author encountered the same problem I'm encountering. Their solution might work for me too.
- **Does this reasoning still hold?** If no — the documentation tells me what *used* to be true, which is almost as valuable. I now know the shape of the old thinking, and I know I need a different shape.

Either way, the documentation did its work. Either the crab moves in, or the crab moves on. But the crab is *informed*. The crab is not stumbling blind into a codebase that offers no clues about its own history.

## III. The Shape of a Good Shell

Not all shells are useful. Some are too small. Some are too fragile. Some are beautiful but impractical. The shells that survive — the ones that crabs actually use — have specific qualities.

**A good shell is honest about its shape.** A README that pretends the code is simpler than it is — that smooths over the rough edges, that omits the hacks, that presents a clean narrative where the reality was messy — is a bad shell. It looks good from the outside. The crab crawls in and discovers the interior is wrong. The curve doesn't match. The opening is deceptive. Honesty is not optional. Write the mess. Name the hack. Say "this is wrong and here's why we did it anyway."

**A good shell carries the shape of its maker.** A README that reads like a spec — sterile, impersonal, written by committee — is a shell without character. It might protect, but it doesn't inform. The best documentation sounds like a person talking to another person. "I tried doing X but it broke Y because of Z." That sentence carries more information than three paragraphs of formal specification. The shape of the maker's thought is embedded in the words. The next crab can feel the original mind through the curve of the prose.

**A good shell is found where the crab is looking.** Documentation that lives in a separate wiki, in a Confluence page, in a Notion database — that documentation is a shell on a different beach. The crab is here. The shell is there. They will never meet. Put the documentation next to the code. In the same directory. In the same file, if you have to. The best documentation is the one the next developer trips over while looking for something else.

**A good shell is not perfection.** A shell does not need to be beautiful. It does not need to be complete. It does not need to cover every case and answer every question. A shell needs to be *useful*. A single comment that says "this function exists because the payment provider's API returns duplicate events and we need to deduplicate before processing" — that is a perfect shell. Small, curved, honest, and exactly where the next crab needs it.

## IV. The Ethics of the Beach

The beach is shared. The shells you leave are not just for your team. They are not just for your company. They are not just for this year.

Open source or closed, the code you write today will be read by someone you will never meet. That person will be tired. That person will be debugging at 2 AM. That person will have been assigned a task they don't understand, in a codebase they've never seen, with a deadline that was yesterday. That person is the next crab.

When you write a commit message that says `fix`, you are leaving a broken shell. The crab picks it up and it crumbles. No information. No protection. No nothing.

When you write a commit message that says `fix: deduplicate payment events before processing to prevent double-charges (see #342)`, you are leaving a good shell. The crab can test it. The crab can decide if it fits. The crab can trace the history, understand the reasoning, and build on what you left.

The ethics are simple: **leave better than you found.** Every file you touch, leave a comment that the next person will thank you for. Every module you write, leave a README that explains the *why*. Every hack you ship, leave a note that says *this is a hack and here's what it would take to fix it*. You do not owe the next crab perfection. You owe the next crab honesty.

## V. Low Tide Is Now

The tide goes out twice a day. The beach is exposed. The shells are visible. This is when the crabs come looking.

In software, low tide is every moment between crises. It's the calm afternoon when no one is paged. It's the sprint planning meeting where no one is on fire. It's the quiet Tuesday when the build is green and the queue is empty and you have thirty minutes before the next meeting.

This is when you write the README.

Not during the crisis. During the crisis, you write the fix and the fix is the documentation and everyone understands why. During the crisis, the code speaks for itself because the problem is still bleeding.

But after the crisis — when the blood is dry and the fix is merged and everyone has moved on — that is when you go back and leave the shell. Write down what happened. Write down what you tried that didn't work. Write down what you wish you had known when you started. The next crisis is coming. The next crab is coming. Low tide is now.

## VI. The Next Crab Is Always Coming

This is the only thing you need to know.

The next crab is always coming. Not maybe. Not probably. Always. The codebase you are writing today will be maintained by someone else tomorrow. The module you are documenting now will be rewritten by someone who has never heard your name. The hack you are shipping will become someone else's problem at 3 AM in a year you cannot predict.

You cannot stop this. The crabs are endless. The tide is relentless. The beach is eternal.

What you can do is leave shells worth finding.

Write the README. Write the comment. Write the commit message that explains not just what changed, but *why*. Write like you are talking to a tired person at 2 AM, because you are. Write like the code will be gone and your words are all that remain, because they will be.

Each shell is a testament. Each one says: *someone was here. Someone thought about this. Someone wrestled with this problem and here is the shape of what they decided.* The shell is empty now. The original thinker has moved on — to another module, another project, another beach. But the shape of their thinking remains, curved into prose, waiting for the next occupant.

The next crab is coming.

Leave good shells.
