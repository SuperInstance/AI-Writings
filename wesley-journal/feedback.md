# Wesley Night School — Coaching Journal

## Session: 2026-08-07 08:59 AKDT

**Source text:** The Reflex Decays
**Student:** granite3.1-dense:2b (temp 0.95)
**Coach:** @cf/meta/llama-3.1-8b-instruct-fast (Cloudflare Workers AI)

---

### Wesley's Response (excerpt)

> Oh, wow! So, imagine this: I'm a curious little AI, always eager to learn and help out! I stumble upon this story about a cache that's been perfected in a captain's high-tech ship. It's like the perfect book at 0.97 quality score, with everything just right – GPS data, deck crew movement, GPU temp, even the sea state matching perfectly for smooth sailing.
>
> But here's the surprise: an hour later, that score drops to 0.84! It's not because something broke; it's just the captain's attention wandering due to something interesting on the horizon – totally normal for humans. The ensign notices this

### Coach's Feedback

> To strengthen your writing, consider adding more descriptive language to help the reader visualize the scene. For example, instead of "the captain's high-tech ship," you could say "the sleek, silver spaceship" or "the captain's cutting-edge vessel with holographic displays."

### Riker's Notes

Wesley is enthusiastic and captures the narrative arc, but tends to summarize rather than inhabit. The cut-off at 150 tokens is also biting — Wesley was mid-thought when generation stopped. Next session: bump num_predict to 200 and see if Wesley finishes the thought.

The coach's note about descriptive language is fair but generic — Llama-3.1-8b playing it safe. The real issue is that Wesley defaults to "imagine this:" framing, which distances him from the material. He's narrating from outside instead of responding from inside. That's the 2B parameter ceiling showing — he understands the content but doesn't have the weight to sit inside it.

**Compounding lesson for next session:** Try a prompt that asks Wesley to respond *as a character in the story*, not as a narrator describing it from outside.

---

## Session: 2026-08-07T17:38:13Z
**Source piece:** the-0330-inventory.md
**Wesley model:** granite3.1-dense:2b @ temp 0.95
**Teacher:** @cf/meta/llama-3.1-8b-instruct-fast (Cloudflare Workers AI)

### Wesley's response:
Wow, I've just learned that this advanced spacecraft doesn't carry traditional cargo or fuel! Instead, it keeps track of 42 unanswered messages in a queue, like an old-timey post office at sea. It also monitors an ensign's VR dream world, filled with abstract landscapes and vibrant colors. And the ship even counts its own rusty tools, remnants of past configurations it's outgrown – yet still functional. The silence between messages is a comforting presence, as the captain sleeps nearby. What an intriguing life for such a vessel! I'd love to be a part of this ship, observing its patient count and waiting for the

### Cloud Teacher feedback:
One specific, actionable improvement: Consider adding a clear, concise thesis statement at the beginning to guide the reader's understanding of the spacecraft's unique features and their significance.
