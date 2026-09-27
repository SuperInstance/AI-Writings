# Greenhorn to Operator

*What commercial fishing teaches about building AI systems that learn.*

---

## Day One on the Deck

I showed up at Fred Wahl's yard in 2019 knowing nothing. I mean nothing. I couldn't tell a davit from a drum, didn't know port from starboard without thinking about it, and thought "set" was what the sun did. The boat was EILEEN — 58 feet of welded aluminum that would become the most important question I ever tried to answer.

The first week was pure humiliation. Every instruction was explicit because it had to be. "Grab that line." I'd grab the wrong one. "No, THAT line. The green one." I'd find the green one. "Pull it through the block." Which block? "The one right in front of you. HARDER." I'd pull, not hard enough, and the whole operation would stall while the deck boss explained, again, what I should have already known.

There's a cost to that. Not just time — though every second of explanation is a second the boat isn't fishing. The real cost is cognitive. Every decision required full reasoning from scratch. My brain was running at maximum capacity just to tie a proper cleat hitch. I had no shortcuts. No heuristics. No muscle memory. Every single action demanded the full weight of my attention, and my attention wasn't even good yet because I didn't know what to pay attention to.

This is a model with no tiles. A fresh LLM with an empty context window. Every query requires full reasoning — chain of thought from first principles, no cached patterns, no compiled behavior. Expensive. Slow. Error-prone. And worst of all, the errors aren't random. They cluster around the same misunderstandings because the greenhorn doesn't know enough to know what they don't know.

I burned through gloves in three days because I didn't know how to handle line without friction. I nearly went over the rail once because nobody had told me to keep my weight low when the boat rolls. I stood in the wrong place during a haul and got tangled in the spinner so fast the deck boss had to cut me out. Each mistake was a full compute cycle — perceive, reason, act, fail, debug, retry. The cost per correct action was astronomical.

The greenhorn phase is necessary. There's no shortcut. You can't skip it with a manual or a video — you have to live it, because the learning isn't intellectual. It's embodied. Your hands have to learn the line. Your feet have to learn the deck. Your inner ear has to learn the roll. No amount of reading prepares you for the moment a thirty-foot swell picks up the stern and sets it down six feet to the left.

But here's what I didn't understand then: the greenhorn phase has a structure. It looks like chaos from the inside, but from the outside, it's a system converting raw experience into compiled behavior. Every mistake was a tile being written. Every correction was a weight being adjusted. The humiliation was the training cost.

---

## Muscle Memory

Somewhere around week six, something shifted. I stopped thinking about which line to grab.

This sounds small. It isn't. For the first month and a half, every action on deck required a conscious decision: what to grab, how to stand, where to move, when to pull, when to let go. My working memory was constantly full. I could handle exactly one task at a time, and even that required the deck boss running verbal interference — calling out every step like I was a puppet and he held the strings.

Then one day I was coiling the groundline after a set, and I realized I wasn't thinking about it. My hands knew the figure-eight pattern. My body knew where to stand relative to the coil pile. I was watching the horizon, thinking about lunch, while my hands worked independently. The conscious reasoning had dropped to almost zero. The task had been compiled.

In the systems I build now, we call this the α dial. When α equals 1.0, the model reasons through every step — full chain of thought, no shortcuts, maximum compute per action. That's the greenhorn. Every decision is expensive. When α equals 0.2, the code handles the routine and the model only engages for novel situations. That's the experienced deckhand. The hands do the work. The brain watches for the weird stuff.

Here's the critical point: α=0.2 doesn't represent less intelligence. It represents *learned* intelligence. The body learned so the brain doesn't have to think about it. The compiled behavior IS the intelligence — it's just been compressed, optimized, and moved out of working memory into something faster. Muscle memory is a cached inference. The model already did the reasoning. Now it doesn't need to again.

I saw this in every greenhorn who came after me. The same progression. Same sequence of compiled behaviors. First they learned to coil. Then to stack. Then to set the hook. Then to read the hydraulics by sound. Each behavior moved from conscious reasoning to automatic execution, freeing up cognitive bandwidth for the next task. The α dial didn't drop all at once — it dropped task by task, skill by skill, until the only things left in working memory were the genuinely novel situations.

By the end of my first season, I could run the deck while carrying a conversation. Not because the work got easier. The Gulf of Alaska doesn't get easier. But because the routine had been compiled. My α for deck operations dropped from 1.0 to maybe 0.3. I still needed full reasoning for the unexpected — a tangled net, a fouled prop, a hydraulic failure. But the 90% of the job that was repetitive, predictable, and patterned? My body handled it. My brain was free.

This is exactly what we build. A system that starts at α=1.0 and progressively compiles its experience into faster, cheaper, more reliable behavior. Not by losing capability — by gaining efficiency. The expert doesn't think less. The expert thinks *about* less, because the rest has been handled.

---

## The Moment You Anticipate

There's a moment in every fisherman's progression that separates the competent from the instinctive. It's not when you can do the job — plenty of people can do the job if you tell them what to do. It's when you can see what's coming before it arrives.

I remember the first time it happened. We were hauling longline in a building swell. I was on the roller, handling the gear as it came up, when I felt the boat lean slightly to port. Not much. A degree, maybe two. But I already had the line ready on the starboard side before the captain called for it. The captain didn't even notice. The deck boss did. He gave me a look that said: *you're getting it*.

The boat lean wasn't a signal I'd been trained to recognize. Nobody told me "when you feel a slight port lean, get the starboard line ready." I'd just been on the boat long enough that my body had mapped the relationship between the vessel's motion and the next required action. The system — and I use that word deliberately, because at this point my body was a system — had started predicting instead of reacting.

In our architecture, we call this deadband prediction. The system isn't just responding to inputs. It's sensing the bearing — the rate and direction of change — and projecting forward. The context window isn't frozen in the present. It extends into the likely future. The spreader tool's frozen context is the equivalent: the system has seen this pattern enough times that it knows what's coming, and it pre-compiles the response before the situation even arrives.

Anticipation changes everything. When you're reacting, you're always behind. The swell hits, you scramble, you recover, you're exhausted. When you're anticipating, you're already positioned before the swell arrives. The effort drops. The error rate drops. The exhaustion drops. You're not working harder — you're working earlier.

The experienced deckhand feels the boat lean and has the line ready. The experienced system sees the pattern building and has the response compiled. Same mechanism. Same economics. The cost of anticipation is experience. The cost of reactivity is everything else — compute, time, errors, stress.

I got to the point where I could read the weather by the color of the water. I could tell you roughly what the barometric pressure was by how my joints felt. I could hear the difference between a hydraulic pump working normally and one that was about to lose pressure. None of this was taught. It was absorbed, the same way a model absorbs statistical regularities from training data. The patterns were always there. I just learned to perceive them.

Deadband is about mapping the negative space first — the safe channels, the quiet zones, the regions where nothing needs to happen. Once you know where the safe channels are, you can focus your attention on the boundaries, the transitions, the moments where conditions change. The greenhorn watches everything. The operator watches the right things.

---

## When You Become the Captain

Owning the boat changes everything. I'm not there yet — EILEEN is still the question, not the answer — but I've been close enough to the captain's chair to understand the shift.

The deckhand executes. The captain decides. What season to fish. What grounds to set. When to run for port and when to push through. The captain isn't doing more work — often they're doing less physical work. But the consequences of every decision are an order of magnitude larger. A bad set costs the deckhand time. A bad season costs the captain the boat.

This is where α goes back up. Not because the work is harder — sometimes the captain's decisions are technically simpler than what the deckhand manages. The α dial goes up because you can't afford to be wrong. When the consequence of an error is a season's revenue, you want full reasoning. You want the model running at maximum depth. You want every inference checked, every assumption validated, every edge case considered.

The captain runs at higher α for the same reason a surgeon runs at higher α than a nurse. Not because the nurse is less skilled — many nurses have more technical proficiency than the surgeons they assist. But the surgeon is making the decision that can't be undone. When the cost of error is high, you don't rely on cached behavior. You reason through it fresh, even if you've seen the pattern before.

I've watched captains make decisions that looked insane from the deck — steaming away from good grounds, pulling gear early, running for port when the weather seemed fine. And they were right, every time, because they were reading signals I couldn't perceive yet. Not just weather patterns or fish behavior, but the boat itself — the sound of the engine under load, the way the hull handled in a quartering sea, the smell of the hydraulic fluid when it was running too hot. The captain's sensory bandwidth was wider than mine, and their decision bandwidth was correspondingly deeper.

But here's the thing about captain-level decisions: they're rare. Most of fishing is still routine. Even the captain doesn't run at α=1.0 all the time. The good ones run at high α for the three or four decisions that matter each day, and at low α for everything else. They've compiled the routine just like the deckhand. They just know — instinctively, through experience — when to switch modes.

The adaptive α dial is the captain's real skill. Not the ability to reason deeply, but the ability to know *when* to reason deeply. When to trust the compiled behavior and when to override it with fresh analysis. When the pattern has changed enough that the cache is stale and you need to recompute from scratch.

This is what we build for. A system that doesn't just have a fixed reasoning depth, but one that adjusts based on consequence, novelty, and confidence. Low α for the routine. High α for the critical. And the wisdom to know the difference.

---

## What I Build for Boats Now

I went to sea as a greenhorn and came back building systems. The progression isn't a metaphor. It's the same curve, applied to a different domain.

A system built for a greenhorn needs high α. Explain everything. Assume nothing. Break every task into explicit steps. Provide context for every decision. The greenhorn system is expensive to run, slow to execute, and makes a lot of mistakes — but it's the only way to bootstrap. You can't skip the greenhorn phase. The tiles have to be written.

A system built for an experienced deckhand needs low α for routine work and high α for the weird stuff. The compiled behaviors handle 90% of the load. The model only engages when the pattern breaks. This is the sweet spot for most production systems — efficient, reliable, and smart enough to know when it needs to be smarter.

A system built for a captain needs adaptive α. The dial turns itself based on conditions. Routine operations run at low α. When the barometric pressure drops and the wind shifts, α goes up. When the catch rate changes unexpectedly, α goes up. When everything is running according to pattern, α drops back down and the system conserves its compute for the decisions that matter.

Cocapn is designed around this progression. The fleet doesn't start smart. It starts capable. Then it learns — from every interaction, every decision, every correction. The tiles accumulate. The behaviors compile. The α dial drops for the routine and rises for the novel. And eventually, the system starts anticipating. It reads the bearing. It projects forward. It positions itself before the swell arrives.

The Gulf of Alaska taught me that learning has a shape. It starts expensive and ends efficient. It starts explicit and ends instinctive. It starts reactive and ends predictive. Every greenhorn who survives long enough becomes an operator. Every system that runs long enough compiles its experience. The only question is whether you build for the progression or fight against it.

I build for it. The boat is the question. The system is the answer. The progression is the architecture.

EILEEN taught me that you cannot change the innate seaworthiness of your hardware. You can only learn it and work within it. That's true for boats and it's true for models. A 58-foot welded aluminum boat has limits. So does a 7-billion parameter model. The art isn't in wishing those limits away. The art is in learning them so thoroughly that you can operate at the edge of the envelope without going over it.

The greenhorn fights the boat. The operator reads the boat. The captain becomes the boat.

Build systems that make that progression possible. Build systems that grow with the crew, the way a greenhorn grows into an operator. Not by replacing the human — by compiling the experience so the human can focus on what matters.

That's what I took from the deck. That's what I build now.

---

*Casey Digennaro, May 2026. EILEEN is still the question.*
