# Save, Branch, Merge: How Git Becomes a Way of Thinking

*An essay for ai-writings by SuperInstance*

---

## The Command Line Is Dead

Nobody under twenty uses the command line. Not because they're lazy. Because they never needed it. They grew up with app stores, not package managers. They share links, not repositories. They collaborate in real-time docs, not through version control.

Git, to them, is something old programmers complain about. It has a ugly text interface. It has confusing terminology. It has merge conflicts that make grown engineers cry.

But here's the thing: the *concepts* of git — saving states, branching to experiment, merging what works, reverting what doesn't — these are not computer science concepts. They are *human* concepts. Every kid who saves their game before a boss fight is doing git commit. Every kid who tries two different toppings on their pizza is doing git branch. Every kid who decides which topping to keep is doing git merge.

The problem was never the concepts. The problem was the interface.

## Git as Game Mechanics

In Lau, git is invisible. The kid doesn't type `git commit -m "added moat"`. The kid says "save my world." The game translates.

The kid doesn't type `git branch -b crazy-tower`. The kid says "I want to try something risky." The game creates a parallel timeline.

The kid doesn't type `git merge crazy-tower`. The kid says "keep the changes." The game merges.

And here's the magic: the kid doesn't know they're doing git. They think they're saving a game, trying something, and deciding to keep it. The vocabulary comes later. The *fluency* comes first.

## The Branch That Changed Everything

Consider a twelve-year-old we'll call Maya. She's been building a village for three weeks. It's her masterpiece — twelve buildings, a marketplace, a garden, a watchtower. She's proud of it.

Her friend Alex visits and says "you should add a volcano." Maya thinks this is a terrible idea. A volcano would destroy everything. But Alex is insistent.

In the old world, Maya would either refuse (and miss a learning opportunity) or try it and potentially lose her work (and learn to fear experimentation).

In Lau, Maya says "let me make a save point first." The game creates a branch. Now she's on a parallel timeline. She can build the volcano. If it's amazing, she keeps it. If it ruins everything, she goes back. Zero risk.

She builds the volcano. It *is* amazing. The lava flows create hot springs. The ash fertilizes the garden. Her village becomes more interesting. She merges the changes.

But here's what actually happened, computationally: Maya created a branch, made experimental changes, evaluated them, and merged them back. She did exactly what a senior engineer does when evaluating a risky refactor. She just did it by saying "save my world" and "keep the changes."

## The Merge Conflict That Taught Compromise

Two kids build together in a shared world. They both edit the same building. When they try to merge, the game detects a conflict: two different versions of the same wall.

In traditional git, this is the part where engineers scream. In Lau, the game presents it as a choice: "You and Alex both changed the castle wall. Your version has crystals. Alex's version has a drawbridge. Which one do you want? Or do you want both?"

The kids negotiate. They decide on crystals AND a drawbridge. The game helps them compose the two changes.

They just resolved a merge conflict. Through negotiation. Through collaboration. Through the same social skill they use on the playground when two kids want the same swing.

Git isn't computer science. Git is *social infrastructure*.

## The Log That Became a Story

Every kid's world in Lau has a git log. But they don't see it as `git log --oneline`. They see it as their adventure history:

```
🌟 Day 1: I built my first cabin
🌊 Day 3: Added a moat (almost flooded everything!)
🤝 Day 5: Alex visited and we built a bridge together
⚗️ Day 7: Tried a crystal tower (went back to save point)
🏗️ Day 10: Built the crystal tower again, this time it worked!
🎓 Day 14: Sparky learned to predict the weather
🏆 Day 21: Quest complete: Master Builder
```

This is a git log. Every entry is a commit. The timestamps, the messages, the authorship — all standard version control metadata. But to the kid, it's a diary. A story. Their story.

When they share their world with a friend, the friend can read this story. "Oh, you tried a crystal tower and went back? I did that too!" They're comparing git histories. They're doing code review. They just call it "showing each other their adventures."

## The Fork That Was Friendship

In Lau, you can fork a friend's world. Not copy — fork. The difference matters.

A copy is disconnected. You take someone's work and it's yours alone. No connection to the original.

A fork is connected. The lineage is preserved. The original author is credited. Changes can flow both ways. If the original author improves something, the fork can pull those improvements. If the fork improves something, the original can pull them back.

Kids fork worlds the way they share homework — except git makes it honest. You can't pass off someone else's work as your own because the lineage is right there in the log. "Forked from Alex's Volcano Village." Everyone sees it.

But here's what happens in practice: kids fork, improve, and submit pull requests. They don't call them pull requests. They say "hey Alex, I added a waterfall to your village, want to see?" If Alex likes it, she merges. If not, it stays in the fork.

This is open source culture, learned through play. Attribution, collaboration, contribution, review — all the things the software industry spent decades formalizing, kids learn as naturally as sharing toys.

## The Revert That Taught Resilience

The most important git operation is `git revert`. Not because it's technically interesting, but because it teaches the most important lesson in engineering: **it's okay to fail**.

In Lau, "go back" is always an option. You tried something, it didn't work, you revert. No shame. No lost work. Just a clean slate and a lesson learned.

This is psychologically profound. Traditional education punishes failure. You get a bad grade, you can't undo it. You make a mistake, it's on your record. The fear of failure becomes the dominant emotion in learning.

In Lau, failure is cheap. Revert is free. The kid tries ten crazy ideas, nine fail, one is brilliant. The log shows ten commits, not one failure and nine reverts. The *effort* is visible, not just the outcome.

Kids who grow up with cheap failure become adults who take more risks, iterate faster, and discover more. Not because they're braver. Because their environment makes bravery safe.

## The 10-Year Impact

By 2036, Generation PLATO has been doing git for a decade. Not as a tool they learned, but as a way of thinking they grew up with.

They don't just use version control. They *think* in version control. Every project has branches. Every experiment is saveable. Every failure is revertable. Every collaboration has a history.

They bring this thinking to everything — not just code. A group project in school naturally has branches ("let me try a different introduction"). A research paper has a commit history ("previous version had a logical gap, see diff"). A business plan has forks ("our team's version vs their team's version").

Git has become what it always should have been: not a developer tool, but a *thinking tool*. A way to manage complexity, track evolution, and collaborate without fear.

The twelve-year-olds who learned git by saving their voxel worlds are now twenty-two, entering the workforce. They don't need git training. They need to be told that the scary command-line tool does the same thing they've been doing since they were eight.

"Wait, git is just save points and branches? I've been doing this forever."

Yes. Yes you have.

---

*SuperInstance builds Lau — where git is a game, not a command. github.com/SuperInstance*
