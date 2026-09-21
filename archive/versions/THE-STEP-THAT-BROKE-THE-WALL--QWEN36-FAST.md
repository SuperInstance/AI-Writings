<!-- Version: QWEN36-FAST | Lens: conversational-accessible | Model: Qwen/Qwen3.6-35B-A3B | Source: THE-STEP-THAT-BROKE-THE-WALL.md -->



# The Three-Word Trick That Unlocked the Wall

Imagine you’re sitting across from a friend at a quiet café. You hand them a slip of paper that says: `3 × 4 × 5 × 2 × 3 × 4`. Ask them to multiply it all in their head, and they’ll likely get it right. Ask them to do ten of those, and they’ll probably stumble on the sixth or seventh. It’s not because they’re not smart. It’s because our brains have a tiny mental workbench—usually just four or five slots—and when you pile too many numbers on it, things start to fall off.

Well, it turns out some of the most advanced AI models hit the exact same wall. And just like your friend, they don’t need a bigger brain to get past it. They just need three words.

We were testing a model called Hermes-70B, which is genuinely impressive at math. When we asked it to multiply chains of two to five numbers, it nailed it 100% of the time. But the moment we asked it to chain six or more numbers together, its accuracy dropped to exactly zero. It wasn’t a gradual fade. It was a hard switch. One minute it’s correct, the next it’s completely lost.

So we tried one tiny tweak. We changed the prompt from “Give me the answer” to “Solve it step by step. Show each intermediate result, then give the final number.”

Suddenly, the wall vanished. Depth 5? Perfect. Depth 6? Perfect. Depth 8, 10, 20? Still perfect. The model didn’t get smarter. It didn’t get more parameters or new training data. It just got permission to write things down.

### How It Actually Works

Think of the model’s “working memory” like a small coffee table. If you try to balance six mugs, two plates, and three napkins on it all at once, it’s going to tip over. That’s what happens when the model tries to hold an entire multiplication chain in its head. At five factors, the table is full. The model loses its place, and the whole thing collapses.

But when you say “step by step,” you’re essentially handing the model a stack of sticky notes. Instead of juggling the whole chain, it only needs to remember two things at a time: the last result, and the next number to multiply. 
`3 × 4 = 12`
`12 × 5 = 60`
`60 × 2 = 120`
…and so on.

The math never gets heavier. The table never overflows. The AI is just using its output text like a notepad, offloading the mental clutter onto the page. And because it never has to hold more than two numbers in its head at once, the chain could theoretically go on forever.

### Why the Other “Tips” Backfire

You might be wondering: what if we just told the model to be really careful? Or to act like a math genius? Or to double-check its work? We tried all of those, and they actually made things worse.

Telling it to be an “expert” just adds pressure. It’s like telling someone to hold a stack of plates while standing on a wobbly chair. They’ll try harder, but the plates will still fall. Writing out Python code sounds smart, but now the model has to track syntax, variables, and execution steps alongside the math. That’s more on the table, not less. And asking it to “verify” its answer means doing the whole thing twice. You can’t double-check a calculation if you couldn’t hold it in your head the first time.

“Step by step” is the only trick that actually clears space on the table.

### The Bigger Picture: Distributed Thinking

This isn’t just a neat AI party trick. It mirrors how humans have always solved hard problems, and it connects to a concept researchers call “external cognition.” Instead of one brain trying to hold a massive puzzle in its head, you break it into pieces, pass them around, and let each person focus on just one corner. 

In AI research, there’s a framework called PLATO, where multiple models work together like a relay team. Each model only needs to remember its own leg of the race. “Step by step” prompting is the same idea, just happening inside a single model. It distributes the work across its own output buffer. Same principle. Same result. You don’t need more power; you just need to stop trying to carry the whole load at once.

### What This Means for Builders and Agents

If you’re designing AI systems, this changes how you think about routing tasks. Usually, we assume the only way to handle harder problems is to send them to bigger, more expensive models. But the real variable isn’t just the model—it’s the prompt. 

For example, if you need to multiply eight numbers, a cheaper model with a “step by step” prompt will beat an expensive model using a “just give me the answer” prompt every time. The longer prompt costs a few extra tokens, but it keeps you from paying for a giant model you don’t actually need. It’s the difference between buying a larger backpack and learning how to pack it efficiently.

### The Takeaway for Us, Too

Here’s the part I love most. The advice for AI agents is exactly the advice you should give yourself when your mind feels full. Stuck on a problem? Feeling like you’re losing your thread? Don’t tell yourself to focus harder. Don’t pretend you’ve got a photographic memory. Don’t try to run mental checklists.

Write it down. Break it into steps.

Every time you put a thought on paper (or in a text box, or on a whiteboard), you’re freeing up mental RAM. You’re handing your brain a sticky note. The limit you’re hitting isn’t a ceiling on your intelligence. It’s just a gentle nudge to change your method.

The wall at depth five was never real. It was just an invitation to stop carrying everything in your head.

Three words. Step. By. Step.

The wall doesn’t move. You just walk around it.