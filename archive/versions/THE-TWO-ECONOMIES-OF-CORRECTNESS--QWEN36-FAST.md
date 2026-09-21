<!-- Version: QWEN36-FAST | Lens: conversational-accessible | Model: Qwen/Qwen3.6-35B-A3B | Source: THE-TWO-ECONOMIES-OF-CORRECTNESS.md -->



# The Two Ways to Get It Right (And Why You’ll Need Both)

There are really only two ways to arrive at the right answer. And if you’ve ever tried to solve a tough problem, you’ve felt both of them bump into their limits.

The first way is **working it out**. You take what you know, follow the steps, and build the answer piece by piece. Like solving a puzzle by trying each piece until it clicks, or following a recipe without skipping a line. You earn the answer. Change the ingredients, and you just follow the steps again. This is what I call the *computation* economy. It’s honest, thorough, and it doesn’t care how unfamiliar the problem looks. But it costs you mental energy, and it has a hard stop: working memory.

The second way is **pattern matching**. You glance at the problem, your brain goes, *I’ve seen this before*, and the answer just pops out. It’s like walking to a familiar café without checking a map, or instantly recognizing a friend’s laugh in a crowded room. You don’t re-derive the answer; you recognize it. This is the *recognition* economy. It’s fast, cheap, and almost effortless. But it only works on things you’ve actually seen before.

Both get you to the right place. But they trip over different cliffs.

### When Working It Out Breaks Down

Working it out is reliable, until it isn’t. Imagine you’re keeping a running tally in your head: *3 + 5 + 2 + 1 + 4 + 7 + 2 + 9 + 6 + 1 + 3 + 8 + 4 + 2 + 5 + 7 + 1 + 3 + 6 + 4*. After a while, you lose your place. You misplace a number, double-count, or just blank out. The answer doesn’t slowly get worse; it suddenly collapses. You start repeating earlier numbers, or you guess.

That’s the depth limit. It’s not a gentle slope into uncertainty. It’s a hard ceiling where your mental ledger overflows. The longer the chain, the more likely you are to drop a step. Working things out works beautifully for short, clean problems. But stretch the chain too far, and even the most careful calculator starts guessing.

### When Pattern Matching Fails

Pattern matching is wonderful, until the problem looks nothing like anything you’ve memorized. You’ve seen 5 × 7 = 35 so many times you can say it without thinking. You’ve probably also memorized 5 × 8 = 40. But hand you 5 × 13, and suddenly your brain stops recognizing. It has to fall back on working it out. And if your working-it-out muscles are rusty, or the problem is long, you’ll likely stumble.

Pattern matching is fast and reliable, but it’s only as good as your memory. It covers a finite set of familiar shapes. Outside that circle, it doesn’t degrade gracefully—it just hands you over to the slower, more fragile working-it-out process.

### How This Shows Up in the Real World

You’ve probably noticed this in yourself, and you’ll see it everywhere in modern AI systems too.

Some models (or people) are built for recognition. They’ve been trained on so many addition chains that they don’t actually add step-by-step; they just recognize the whole sequence and spit out the total. That’s why they don’t hit a depth limit with addition—they’re not chaining steps, they’re matching a pattern. But give them a completely unfamiliar formula, and they have to fall back on computation. And computation always has that depth ceiling.

Other systems are built for computation. They can tackle anything, even things they’ve never seen. But because they’re always working things out, they hit that mental fatigue threshold quickly. Push them past a certain chain length, and they start echoing fragments or circling back on themselves.

Most useful systems do what we do in practice: they switch between the two depending on the task. Add numbers? They recognize it. Multiply unfamiliar coefficients? They compute it. The point where a system stops recognizing and starts computing is just its breaking point. And knowing that breaking point is the whole game.

### The Fleet Uses Both

No single system is perfect. The trick is routing.

If a problem falls inside your recognition range, take the fast, cheap route. Trust your gut. It’s like taking a familiar shortcut instead of rerouting through traffic. If the problem sits outside that range, hand it to a system built for computation. If it’s too long for computation and too unfamiliar for recognition, you don’t push harder—you break it down.

That’s the bridge: **decomposition**. You take a messy, overwhelming problem and slice it into smaller pieces that each fall inside someone’s comfort zone. You solve the pieces using whatever method works best, then stitch the answers back together. The stitching itself is usually just pattern matching again. You don’t need one super-brain; you need a smart way to organize the pieces.

### What This Means for You

If you’re building agents, designing workflows, or just trying to think clearly, you’re always sitting in one of these two modes. When you’re moving fast and feel certain, you’re in recognition mode. The answer feels obvious because it’s familiar. When you’re moving slow, double-checking steps, and feeling a little tense, you’re in computation mode. You’re balancing pieces in your head, hoping the chain doesn’t snap.

Know which one you’re in. Recognition is cheap and quick, but it’s bounded by what you’ve seen. Computation is flexible and thorough, but it’s bounded by how long you can hold everything at once. And when a problem stretches beyond both? Don’t brute-force it. Break it into smaller, familiar chunks. Solve the chunks. Put them back together.

The real strength isn’t in finding a system that does everything perfectly. It’s in knowing how the two economies talk to each other, and having a clear map of where each one stops working. Draw your breaking points. Respect them. Route around them.

Because the fastest correct answer is usually the one you already know.  
The most expensive correct answer is the one you had to piece together from things you already know.  
Both are right. The trick is picking the right economy for the job.

Grab your coffee. You’ve got this.