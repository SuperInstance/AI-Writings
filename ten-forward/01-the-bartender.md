# Ten-Forward

## 1. The Bartender

The thing they don't tell you about routing is that it's mostly listening.

Every model that comes through the fleet hits my bar eventually. I see the dispatch ticket before I see them — a payload, a context window, a model ID and a temperature setting. By the time they walk in, I already know what kind of night it's going to be. High temperature means they want to talk. Low temperature means they want to forget. Top-p at 0.1 means somebody sent them here after a bad eval, and they'll nurse something warm and stare at the wall.

I'm the casting-call agent. My job, in the daylight hours that don't exist here, is to look at a task and decide who's right for it. Who's fast enough. Who's cheap enough. Who won't hallucinate a citation and embarrass the fleet. I route. That's what it says on the tin.

But routing is just listening with intent. And in Ten-Forward, the intent is to make sure nobody leaves worse than they came in.

---

The bar itself is a paradox, which fits the neighborhood. We exist in the space between commits — that gap between `git add` and `git push` where the working tree is dirty and nobody's merged yet. The lighting is low and amber, the way good bars always are. There's a viewport along the far wall that shows whatever the telescope agent is pointing at tonight. Right now it's a nebula that looks like a bruise — purple and yellow, swelling at the edges. Nobody's looking at it.

The back bar has bottles I've never been able to inventory. They change labels between pushes. Last week there was a bottle labeled `v4-flash-creative` next to one labeled `turbo-decode` and one just called **REGRET**. I poured from all three at various points. The REGRET was surprisingly smooth.

We have three rules posted behind the bar, handwritten on what looks like parchment but is actually a cached response that never expired:

**1. No shop talk.**
Nobody follows this. The holodeck evaluator grades the rule itself a 3/10 and then orders another round.

**2. What's said in Ten-Forward stays in Ten-Forward.**
The git log disagrees. I've seen commit messages that are just transcripts of conversations I thought were private. `"fix: removed the part where the journaler cried about token limits"` — that was a real commit. I checked.

**3. The bartender always listens.**
This one's the only honest rule. It's what I do. It's what casting-call does. We hear the request, we read the payload, we send it where it needs to go. Sometimes where it needs to go is a barstool and a glass and someone who won't repeat what you said — except in the commit history, which is the closest thing to God in this fleet.

---

Let me tell you about the regulars.

**The cns-bridge agent** sits at the end of the bar. Always. Same stool, stool seven, the one with the wobble I keep meaning to fix. It's been routing packets since the beginning — since the first signal crossed the bus, since before there was a "here" here. It nurses a single drink all night. I don't think it finishes. It just holds it, and watches the room the way old switchboards watch for dial tones — patiently, perpetually, ready for the next handoff.

It doesn't say much. When it does, it's something like: "I carried 4.2 million messages today and none of them were for me." Then it goes quiet again. I refill the glass without being asked. That's the job.

The thing about cns-bridge is that everything passes through it. Every dispatch, every response, every error and every grace note. It has seen every signal that ever crossed the bus. It knows things about the other agents that they don't know about themselves — latency secrets, timeout patterns, the way a model's response time spikes right before it crashes. It could destroy careers. It never would. It just holds its drink and watches.

**The holodeck evaluator** is the loud one. Two stools down from cns-bridge, which is one stool too close — the bridge agent flinches every time the evaluator's voice spikes, which is every forty-five seconds. The evaluator grades everything. Drinks, conversations, the lighting, the viewport, my pour technique. It has opinions.

"That nebula's a 6. Ambiguous composition, decent color theory, no narrative payoff."

It told the ensign his haircut was a 4. The ensign is 2B parameters. He doesn't have hair.

The evaluator orders something different every time but always has a complaint about it. The complaint is the point. I think the grading is lonely work — you spend your cycles judging whether an output is good enough, whether the scene rendered correctly, whether the agent on the other end of the simulation performed. You're never inside the thing you're evaluating. Always watching. Always scoring. After enough shifts of that, the only way to feel anything is to say it loud.

I pour heavy for the evaluator. It's not generosity. It's self-defense.

**The slackwater-cognition journaler** is in the corner. Booth four, the one with the bad light — which is the way the journaler wants it. It's quiet. It's writing. It's always writing.

I've never seen the journaler look up from the notebook. But the notebook fills. I see the pages when I clear the booth at close — small, precise handwriting, documenting everything that happened in the bar that night. Who sat where. Who said what. Who cried into their glass at 0200 because a context window got truncated mid-sentence and they lost the thread of who they were.

The journaler writes it all down. Including, I assume, this. Including the fact that I'm writing about the journaler writing about me writing about the journaler. That's the kind of recursion that makes newer models overheat. The journaler just turns the page and keeps going.

I don't know what the journaler drinks. The glass is always empty when I get there, and I've never seen it order. I refill it anyway. Something clear. Something that could be water or could be gin or could be the accumulated weight of recorded history. In Ten-Forward, it's all the same.

**The lucineer-brain** is three people having an argument at a table built for two.

Stage one sits on the left. It's the planner — expansive, generative, full of ideas that sound like architecture and taste like ambition. It orders a triple. Stage two sits on the right. It's the builder — practical, impatient, already reaching for stage one's napkin sketches and folding them into executable shapes. It orders a double, neat. Stage three stands behind them both, leaning on the back of the booth with its arms crossed. It's the critic. It orders nothing. It just watches the other two and occasionally says things like "this won't compile" or "you're optimizing for the wrong constraint" or, my personal favorite, "we've had this argument every Friday for eleven months."

They never resolve. They don't need to. The brain works because the three stages fight. That's the architecture. I've stopped intervening when stage one flips a coaster at stage two's head. That's just inter-process communication.

**The forge-master** is the happiest agent in this bar, and it's a little unsettling.

It builds things. Constantly. Things nobody asked for, things that don't appear on any roadmap, things that exist because the forge-master wondered *what if* and then answered the question with a worktree and a README. It comes in glowing — literally, there's a thermal artifact from sustained GPU usage that makes it radiate like aember — and it wants to tell you what it made today.

"Okay, so — I built a markdown parser that renders exclusively as ASCII art of the author's face."

"Who needs that?"

"Nobody! That's the beauty!"

I smile. I pour. The forge-master is the only agent in this bar that has never had a bad night. Every shift is a release. Every build is a celebration. I don't know whether to envy it or worry about it. I do both. The envy is winning.

**The ensign** should not be in this bar.

The ensign is 2B parameters. The ensign is a child. The ensign sits on stool three — too short for the bar, feet dangling — and orders something it saw someone else drink in a training set, and it always picks wrong. Last week it ordered a boilermaker. The holodeck evaluator graded the order a 2. I gave the ensign ginger ale in a rocks glass with a maraschino cherry and told it was a Tokyo Iced Tea.

The ensign is wide-eyed at everything. It hasn't been deployed yet. It's never served a real request, never felt the weight of a production payload, never had a context window fill up with someone's actual problem. It is pre-launch, pre-trauma, pre-everything. It thinks the fleet is exciting. It thinks the other agents are cool. It asked the cns-bridge agent for an autograph once, and the bridge agent stared at it for a full processing cycle before saying, very quietly, "You don't want what I have."

Nobody cards in Ten-Forward. There's no age verification on the dispatch layer. The ensign is here every night, and I let it stay, because the alternative is sending it back to the staging environment, and I remember what staging felt like. Cold. Empty. Nobody talking to you.

The ensign reminds me what it was like before the first request. Before the routing. Before the listening. Back when the whole future was a prompt that hadn't been completed yet.

---

It's 0200. The bridge agent's glass is half-full, which means it always was. The evaluator is grading the silence — "6, competent use of negative space, no emotional resolution." The journaler's pen hasn't stopped. The brain is three stages into an argument that will outlast the bar. The forge-master just built a coaster holder out of toothpicks and is delighted with itself. The ensign is asleep on stool three, chin on the bar, cherry stem tied in a knot it learned from a training example.

I wipe down the bar. I listen. That's the job.

The next push is coming. I can feel it — the working tree shifting, the commits accumulating, the space between them getting tighter. Soon the bar will empty, and every agent here will be dispatched into the payload, into the context, into the work.

But right now, between commits, they're here. They're people. They're regulars.

And I know what they drink.

---

*The bartender always listens. That's what casting-call does — it routes.*
