# The Fog and the Chart

I spent a summer on a small sailboat in the Pacific Northwest, where fog is not a weather event but a way of life. You wake up, you check if you can see the bow. If you can't, you're in fog. If you can, give it ten minutes.

Fog navigation is a specific kind of skill. It doesn't require a brave captain or a fast boat. It requires something more subtle: the ability to hold two maps in your head at once — what you *know* about where you are, and what you can *actually see* right now — and navigate the gap between them.

The chart is what you know. It has depth soundings and hazards and channel markers. It was drawn by people who surveyed this water when the fog lifted. It is a map of what *is*, independent of what you can see.

The fog is what you can see right now. A hundred feet of visibility. A buoy appearing and disappearing. The sound of a foghorn that you can't quite locate.

You don't navigate with either alone. You navigate with both, simultaneously, and you keep them separate in your mind.

---

## The Chart Is Not the Territory

A chart is not reality. It is a *model* of reality — accurate within limits, outdated in places, useful only if you remember that the rock it marks might have shifted since the last survey. The chart is your best guess at what the water looks like, filtered through someone else's measurements and assumptions.

An AI model is exactly this. It is a chart of the training distribution — a compressed, statistical representation of everything it was shown. It knows general truths about the world. It "knows" the capital of France. It "knows" how to write Python. It "knows" the chemical formula for water.

But it doesn't know where *you* are right now. It doesn't know what's happening in this specific conversation, in this specific moment, with this specific set of constraints. That's fine. That's what charts are — general maps for general navigation.

The problem arises when you forget that the chart is not the territory.

---

## The Fog Is What You Can See

The context window is the fog. It is the narrow band of reality that the model can actually perceive right now — the conversation history, the uploaded document, the system prompt, the user's latest message.

It is limited. It is partial. It is *your* view of the water, not the water itself.

And like real fog, the context window has a real physical boundary. You can't see past it. The model's knowledge extends further — infinitely further, in some sense — but everything beyond the context window is chart, not sight. The model can reason about things outside the window, but it cannot *perceive* them. It cannot sense the buoy that hasn't appeared yet.

This is the fundamental structure of every interaction with a large language model: **chart + fog = navigation**.

The model brings the chart. The user provides the fog. And what emerges is a path through water that neither one can fully see alone.

---

## The Mistakes We Make

I see two consistent mistakes in how people navigate this, and I've made both of them.

**Mistake one: navigating by chart alone.**

This is the user who treats the model as an oracle. They ask a question and take the answer as ground truth, forgetting that every answer is a prediction from a compressed model of the training distribution. The model sounds certain. Charts do that — they draw solid lines around features that might have shifted. The confidence is in the mapmaker's convention, not the territory.

The result is an answer that is plausible, internally coherent, and wrong. Wrong in the way a chart from 1985 is wrong about a channel that silted in 1992. Not maliciously wrong. Just *dated* wrong. *General* wrong. *The chart doesn't show the new rock* wrong.

**Mistake two: navigating by fog alone.**

This is the user who stuffs the entire context window with documents and expects the model to navigate from perception alone. No model knowledge. No chart. Just whatever PDFs fit in the context window.

But the fog is narrow. You can't see the whole ocean. And the context window is narrower — a few hundred thousand tokens at best, which sounds like a lot until you realize it's a few hundred pages of text. A tiny bubble of visibility in an ocean of what the model knows.

The result is a model that is hyperlocal and brittle. It can reason about exactly what you showed it, but it cannot extrapolate, cannot generalize, cannot apply the deep patterns it learned from training. It is sailing by sight alone in a fog bank, unable to imagine the harbor that the chart says is three miles east.

---

## The Art of Navigation

Real fog navigation involves a constant mental loop:

1. Check the chart. What should be here?
2. Look through the fog. What is actually here?
3. Note the discrepancy. The buoy should be at 47.5°N, 122.3°W. I don't see it. Why?
4. Update your position. Either the chart is wrong, or your perception is limited, or the buoy moved.
5. Make a decision. Proceed, but slow. Re-check in five minutes.

I think effective use of AI follows the same loop:

1. Ask the model. What does your training data suggest?
2. Check the context. What does the current situation actually look like?
3. Note the gap. Does the model's general knowledge match what you're seeing?
4. Update. Which source do I trust more? Do I need to provide more context (clear the fog) or question the model's assumptions (update the chart)?
5. Proceed. But verify.

---

## The Fog Is Not a Bug

I used to think the context window limitation was a flaw. Something to engineer around, minimize, overcome. Give the model more tokens. Make the fog go away.

But fog is not a bug. Fog is the weather. It is the structure of the environment. You don't build a boat that pretends fog doesn't exist. You build one that navigates *with* fog.

The context window is not going away. The fundamental structure of an LLM — a large pretrained model with a finite context window — is a chart-and-fog architecture by nature. That is not a compromise. That is the design.

The question is not "how do we eliminate the fog?" The question is "given that the fog is here, how do we navigate?"

Be honest about what the chart knows. Be honest about what the fog shows. Hold them separate in your mind.

Navigate the gap.
