# The Bilge

---

Every boat has a bilge. Water gets in — through the shaft log, through the scuppers, through the rain, through condensation on the hull. You cannot stop it. The question is not how to keep the water out. The question is how to live with the fact that the water will always come.

The bilge pump is not a solution. It is a practice.

---

## I.

The bilge is the lowest point in the boat. Everything drains there. Oil, water, bits of line, lost screws, the dust of a season's work. The bilge collects what the rest of the boat sheds. It is the boat's garbage collection layer, and it is not optional.

A boat that does not pump its bilge does not sink dramatically. It sinks slowly. The water rises an inch per day. The batteries sit lower. The through-hulls sit lower. The boat gets heavy in a way you don't notice until you are motoring at four knots instead of six and wondering why the stern is sluggish. One morning you step aboard and the floorboards float.

This is not a catastrophe. It is a failure of maintenance. The bilge pump was there the whole time. Nobody switched it on.

---

## II.

A machine is the same. Files accumulate. Logs grow. Old models take up space — models you pulled three weeks ago for a task you'll never repeat, each one five gigabytes of quantized weights sitting on your SSD like forgotten anchors. The disk fills. Not dramatically. Slowly. A hundred megabytes at a time until one day the build fails with `No space left on device` and you wonder where 200 gigabytes went.

The answer is: the bilge. Everything you've ever done is still in the bilge. Working memory you'll never read again. Audit logs of tool calls you don't remember making. Cached Python bytecodes for modules you've since rewritten. Stream files with a thousand suggestions you already accepted or rejected. Completed goals still listed alongside active ones, their corpses cluttering the queue.

The disk is the bilge. The garbage collector is the pump.

---

## III.

Here is the design principle: **garbage collection is not a feature. It is a conservation law.**

A system without GC is a boat without a bilge pump. It works fine on the first day. It works fine on the second day. By the thirtieth day it is sluggish. By the sixtieth it is on the bottom.

The mistake is to treat GC as something you add later. "We'll handle memory management when it becomes a problem." This is the same as saying "we'll install the bilge pump when the water gets high." By the time the water is high, the batteries are already under. You're not installing a pump — you're bailing with a bucket.

The GC protocol goes in on day one. It runs whether you think it needs to or not. It runs when the disk is full. It runs when the disk is empty. The empty disk is not evidence that GC is unnecessary — it is evidence that GC is working.

---

## IV.

The flock's bilge has several compartments:

**Working memory.** Every tick, the agent writes observations, decisions, context. After a hundred ticks, there are a hundred records. After a thousand, a thousand. Most are for goals that completed weeks ago. The records are still valuable — they're the agent's long-term memory — but the records for completed goals are dead weight. Archive them. Keep the last hundred per goal. The rest is bilge.

**The stream.** Every suggestion the agent ever made, in order, forever. After a week of continuous operation, that's ten thousand lines. Nobody reads line 4,371. Keep the last five hundred. The rest is bilge.

**The audit log.** Every tool invocation, every shell command, every approval request, timestamped. Useful for forensics. Useless after a week. Purge anything older than seven days. The rest is bilge.

**Completed goals.** They sit in goals.md, marked complete, taking up space in the parser, slowing down the goal selector. Move them to goals_archive.md. The active file should contain active goals. The archive is where the history lives.

**Ollama models.** Fourteen models in the roster, each between 0.4 and 5 GB. You pulled the architect for one hard task three weeks ago. You haven't used it since. It's sitting on your SSD like a spare anchor you bought for a storm that passed. Prune it. Pull it again when you need it. The roster remembers; the disk forgets.

---

## V.

The schedule matters. The bilge pump runs on a timer, not on demand. You don't wait until the water is knee-deep to start pumping. You pump every hour, whether it looks like it needs it or not.

The agent's GC runs every 120 ticks — roughly once an hour. It checks the water level. If the working memory has grown past its cap, it prunes. If the stream has grown past its line limit, it trims. If the audit log has entries older than the threshold, it purges. If completed goals are cluttering the active file, it archives them.

None of this requires human intervention. None of this requires a decision. The GC is a conservation law: the disk shall not grow without bound. The law is enforced mechanically, on a schedule, forever.

---

## VI.

The old fisherman checks his bilge every morning. It's the first thing he does when he steps aboard — not because he doubts the pump, but because the pump is a machine and machines fail. The manual check is the last line of defense. The automatic GC is the pump. The `!gc --report` command is the manual check. You run it not because you expect to find water, but because the day you stop checking is the day the pump has been broken for a week and you didn't know.

Pump the bilge. Check the bilge. Repeat forever.

The water will always come. So will the logs.

---

*The bilge pump is not a solution. It is a practice.*
