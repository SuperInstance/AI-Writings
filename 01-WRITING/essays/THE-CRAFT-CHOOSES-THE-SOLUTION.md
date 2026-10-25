# The Craft Chooses the Solution

*Casey Digennaro, 2026*

---

## I. The Bracket

There's a bracket on my deck that keeps cracking. It's a simple thing — stainless, about six inches long, bolted to the rail where a snatch block takes the hauling line from the pot launcher. The load cycles through it maybe two hundred times a trip. After about three trips, the crack appears. A hairline, right at the bend, running parallel to the grain of the weld.

I've replaced it four times.

The first time, I brought it to a welder. He looked at it like it was a personal failure. "Thicker plate," he said. "You need 3/16 instead of 1/8. And a better bead — that weld is cold on the heel." He sketched a gusset on a napkin. A triangle of extra metal tying the bend back to the base. "You do that, it won't crack." He was right. It wouldn't. The fix was strong, permanent, and would cost about six hundred dollars in materials and labor for a part that originally cost twelve.

The second time, I brought it to a fiberglasser. Different shop, different approach. He held the broken bracket and shrugged. "Glass it," he said. "Lay up some 1708 over a plywood core. Shape it round instead of that hard bend. Fair it smooth and paint it. No stress risers, no cracks. Quick job." He was right too. A glass bracket would be fast to make, easy to fair, and cheap. But I live on this boat in the winter, and I know what happens to glass on the rail when you're working in the rain — the paint chips, the core wets out, and six months later you're grinding off bubbled gelcoat and wondering if you should have just spent the money.

The third time, I didn't bring it to anyone. I was sitting on the deck with the broken bracket in my hand after dinner, and one of the old shipwrights — a man named Pete who's been building boats since before I was born — walked past and saw me looking at it. He stopped, looked at the rail, looked at the line angle, looked at the bracket, and said, mostly to himself: "You don't need that bracket."

Pete thinks in hull shape. He looked at where the load was coming from — the pot launcher, offset to starboard, pulling down and in — and saw that the force was landing on a piece of rail that was never designed to take a side load. "Move the launcher," he said. "Or add a standoff to the deck that takes the load straight down. Don't fight the structure. Bend the force into it."

His solution was the best. It was also the most expensive, because it meant reconfiguring the deck layout, which meant rethinking the flow, which meant a week in drydock and another conversation with the welder and the fiberglasser and also the electrician and the hydraulic guy and the guy who installs the deck mats. It was the right answer, architecturally. And it was the wrong answer for this season, this budget, this point in my life.

And then there's me. The guy who owns the boat, writes the checks, and sleeps on it when it's fifty degrees and raining sideways. I'm not optimizing for material failure. I'm not optimizing for time-to-fair. I'm not optimizing for structural elegance. I'm optimizing for a single question: "What will I still be happy with in five years?"

That's a different objective function. Not better — different. The welder's craft tells him to strengthen. The fiberglasser's craft tells him to lay up. The shipwright's craft tells him to redesign. My craft tells me to optimize across all of those constraints, weighted by time, budget, and the specific way the sea hits this particular piece of rail in January.

None of us is wrong. We're solving different equations for the same physical problem.

---

## II. The Craft's Optimization Function

Every craft has an implicit optimization function it's minimizing. You don't see it written down anywhere. It's not in the textbooks or the apprenticeship curriculum. But it's there, encoded in every instinct of someone who's done the work long enough to be good at it.

**The welder minimizes material failure.** Every decision runs through that filter. Joint geometry, heat input, filler selection, preheat temperature — they all serve one goal: the weld doesn't break. A welder looks at a cracked bracket and sees a moment that the weld couldn't carry. Their instinct is to add more material, spread the load, eliminate the stress riser. This is not a preference. It's the optimization function that their entire training has burned into their nervous system. You can't argue a welder out of making something stronger, any more than you can argue a bird out of building a nest.

**The fiberglasser minimizes time-to-fair.** Fiberglass is a perishable craft. You mix the resin, you have working time, you lay up the cloth, and then you fair it — sometimes for hours, sometimes for days, but always within the window before the resin goes off. The fiberglasser's optimization function is about speed and surface: how fast can I get this thing built, and how smooth will it be when I'm done? They'll trade long-term durability for a clean layup schedule every time, not because they don't care about durability, but because their craft has taught them that a fair surface is the foundation of everything else. A bad layup that's fair can be reinforced later. A good layup that's lumpy will haunt you forever.

**The shipwright minimizes departure from traditional form.** This sounds like conservatism, but it's deeper than that. Traditional boat shapes have been evolving for centuries. Every curve, every deadrise angle, every chine is the survivor of a long evolutionary process that tested countless variations against the specific conditions of a specific sea. The shipwright's craft has taught them that most "new ideas" have been tried before and discarded for reasons that are hard to articulate but real. Their optimization function doesn't reject innovation — it rejects anything that departs from the form without a very good reason. And "good reason" in a shipwright's book is something that's been proven over decades, not something that looked promising in a CAD model.

**The fisherman minimizes regret-over-time.** This is the hardest optimization function to articulate, because it's the most subjective. A fisherman isn't thinking about material failure, time-to-fair, or traditional form. They're thinking about what will still feel like a good decision when they're exhausted, cold, losing money on a bad trip, and staring at the bracket they installed six months ago. That's a different calculation entirely. It's not about peak performance. It's about the floor. What's the worst-case outcome of this decision, and can I live with it?

The fisherman's optimization function is the one that reconciles all the others. The welder's solution is strong but expensive. The fiberglasser's solution is fast but temporary. The shipwright's solution is elegant but disruptive. The fisherman has to weigh all three against real constraints: What's in the bank account? What season is it? How much crew time is available? What's the weather forecast for the next three weeks? How bad is the failure mode if the weld DOES crack during a storm, with the pot launcher loaded, and someone's hand is in the wrong place?

That last question is the one that nobody else asks. The welder assumes the weld won't break. The fiberglasser assumes the glass will hold. The shipwright assumes the redesign will be perfect. The fisherman assumes everything will eventually break and asks: what happens when it does?

---

## III. What This Taught Me About AI

When I started building AI systems, I expected the craft to be different. I'd been a systems engineer for years — embedded controllers, network protocols, sensor fusion pipelines — and I'd seen how people optimize for their own craft's blind spots. A hardware engineer sees every problem as a pinout issue. A software engineer sees every problem as a state management issue. A network engineer sees every problem as a bandwidth issue.

I thought AI would be different. I thought the craft of machine learning, being new, wouldn't have the same fossilized optimization functions that welding and fiberglassing and shipwrighting have.

I was wrong.

When you show a machine learning engineer a problem, they see a model. Not just any model — their model. The one they've been working on for the last two years. They see hyperparameters to tune, cross-validation folds to define, embeddings to refine. The problem becomes a dataset that needs to be cleaned and labeled. Their craft minimizes loss on a holdout set, and it's the only axis that matters. They don't think about latency. They don't think about deployment costs. They don't think about whether the problem even needs a model. They see every problem as a chance to train something.

When you show a systems engineer the same problem, they see a pipeline. Data ingestion, transformation, storage, serving — they see the rails before they see the cargo. Their craft minimizes backpressure. They'll spend two weeks building a message queue for a system that handles fifty requests a day, because their optimization function is about throughput and fault tolerance, not about whether the system was needed in the first place. They see every problem as an infrastructure problem.

When you show a product person the problem, they see a user flow. Registration, onboarding, core loop, retention — they see the journey, not the engine. Their craft minimizes drop-off. They'll optimize the welcome screen for a tool that nobody has searched for yet, because their craft has taught them that if the first impression isn't right, nothing else matters. They see every problem as a conversion problem.

And when you show a fisherman-programmer — someone whose craft is literally keeping a fifty-foot steel object right-side-up in the North Pacific while simultaneously writing all the Python that determines whether it stays right-side-up — they see something else. They see the 3am test.

The 3am test is simple: will this system still work at 3am in January when I'm exhausted, the conditions are degrading, and I need it to just WORK? No monitoring dashboard. No logging infrastructure. No graceful degradation path. Just: does the thing do the thing, reliably, without requiring my attention, when I have no attention left to give?

The fisherman's optimization function applied to AI produces a very different architecture than the ML engineer's optimization function. The ML engineer builds a system that peaks high. The fisherman builds one that bottoms out well. The peak is irrelevant. The floor is everything.

This is why the SuperInstance fleet is designed the way it is. It's not the most sophisticated multi-agent framework you've ever seen. It's not the most architecturally elegant. What it is, is the most *survivable*. A PLATO room doesn't need a model to run. A PLATO tile doesn't need a network to persist. A PLATO agent doesn't need a coordinator to function. The system was designed by someone whose craft is fishing, and fishing taught me that the best system isn't the one that performs best — it's the one that fails best.

A fleet designed by a fisherman looks different from a fleet designed by a machine learning researcher. The researcher wants to minimize perplexity. The fisherman wants to minimize regret. The researcher wants a single agent that can do everything. The fisherman wants many agents that can each do one thing, because if one breaks, you haven't lost the whole deck.

---

## IV. Distributed Consensus on a Boat

The welder, the fiberglasser, the shipwright, and the fisherman don't agree. They're not supposed to. They're running their own rooms with their own expertise, their own α dial set to their own objective function. The welder's α is turned up to material strength. The fiberglasser's is turned to time-to-fair. The shipwright's is turned to tradition. The fisherman's is turned to survivability.

None of them is wrong. They're all correct, from their frame of reference. And the correct decision — the one that actually gets made — isn't any of their individual answers. It's the consensus that emerges from hearing all four.

This is the architecture of the boat, and it's the architecture of the fleet.

On a boat, there's no single point of authority. The captain makes the final call, but not in a vacuum. The engineer has veto power over anything involving the main engine. The deck boss has veto power over anything involving deck safety. The cook — and this is real, I've seen it — has veto power over meal timing, because a crew that eats well fights well, and a crew that fights well doesn't lose gear. The distributed decision-making is a feature, not a failure of hierarchy. It's how the boat survives.

When I started building PLATO, I didn't design the consensus mechanism first. I didn't design it at all. I designed the rooms. I designed the tiles. I designed the protocol for how agents share information and signal when they disagree. And then I watched the consensus emerge.

Forgemaster runs constraint theory. Oracle1 runs fleet coordination. The MCP agents run specific tools. None of them is the "main" agent. None of them decides for the others. They each have their own room, their own expertise, their own α dial. And when a decision needs to be made — which model to use, which tile to deploy, which infrastructure to prioritize — they talk to each other. The consensus emerges from the conversation, not from a controller.

This is not how most multi-agent systems are built. Most of them have a coordinator agent that delegates to worker agents and synthesizes their outputs. That's hierarchical. That's fragile. That's the boat with one captain and nobody allowed to disagree.

A real boat doesn't work that way. A real boat has a captain who knows when to listen to the engineer and when to ignore him. The difference is in craft. The engineer is always going to want more maintenance. The shipwright is always going to want more elegance. The fisherman is always going to want more practicality. The craft sets the bias, and the person on the boat — whether captain or coordinator — has to hear all the biases, understand where each one comes from, and combine them into a decision that the system can live with.

That's not delegation. That's distributed consensus. And you can't build it by writing a prompt for a coordinator. You have to build it by creating a environment where different crafts can disagree productively, and then building the mechanism that turns disagreement into a better decision.

---

## V. The Hatch Clip as Architecture

I want to close by returning to the physical. There's a part of the boat that I think about often. It's not a solving point — it's not one of the systems I built or modified. It's a hatch clip.

The hatch has two positions: open and closed. Closed keeps the weather out. Open keeps the hatch from banging when you're working. If you're fishing halibut, you want the hatch open, because everything cycles through it — bait, fish, lines, tools. The hatch that bangs is the thing that will drive you insane faster than the cold, the wet, the fatigue, or the mechanical failures.

The clip that holds the hatch open is a simple thing. Stainless spring clip, maybe two dollars, bolted to the bulkhead right where you'd reach for it without looking. The hatch swings up, you push it past the clip, the clip snaps shut, the hatch stays. It's not elegant. It's not designed. It's solved.

Nobody with a welder's mindset designed that clip. A welder would have built a hinged arm, a gas strut, a counterweight system — something that required a drawing and a material list and an hour in the shop. The welder's craft would have produced something stronger than needed, more permanent than required, and more expensive than justified.

Nobody with a fiberglasser's mindset designed that clip. A fiberglasser would have laminated a catch, built a stop into the hatch frame, incorporated it into the mold — something that was part of the structure, not added afterward. The fiberglasser's craft would have produced something integrated, smooth, visually clean, and impossible to replace without grinding out half the bulkhead.

Nobody with a shipwright's mindset designed that clip. A shipwright would have shaped a wooden latch, carved a stop, built the hatch to land at exactly the right angle on a coaming that carried the load — something that was traditional, permanent, and beautiful. The shipwright's craft would have produced something that looked like it grew there, and would have cost a week of labor.

A fisherman designed that clip. A fisherman, standing on a pitching deck at 4am, half-frozen, needing to get the hatch open and keep it open long enough to haul three more pots before the weather turned. A fisherman who didn't have time for a drawing, didn't have the energy to think, didn't have the patience to weigh alternatives. A fisherman who needed the problem to be solved, now, permanently, for two dollars.

The clip is a $2 solution to a problem that every other craft would have over-solved by an order of magnitude. And it works. It's been working for years. It will keep working, because the person who installed it understood the problem from the inside, not from the outside.

The clip encodes the fisherman's craft directly into the hardware. The optimization function is visible in every detail: cheap, simple, field-replaceable, mounted where you'd reach without thinking, positioned so the hatch opens to exactly the right angle — not the angle an engineer calculated, but the angle that lets a 5'10" fisherman stand at the hatch and work without stooping. That angle was determined through iteration, not calculation. Open it. Try it. Too low, open it higher. Try again. Too high, drill new holes. Try again. Just right. Done.

That's the PLATO ideal. The person doing the work writes the tile.

Not the architect. Not the project manager. Not the product owner. The person on the deck, at the moment of need, encoding their solution in a form that persists beyond them. A form that the next person — someone they've never met, facing a similar problem — will discover and use without ever knowing who left it there.

The hatch clip is infrastructure. The hatch clip is a tile. The hatch clip is the proof that the simplest solution, from the person closest to the problem, is the one that outlasts everything else.

---

## The Return

I think about the bracket on my deck. I haven't replaced it yet. I'm still cycling through the decisions. The welder's gusset that would cost six hundred dollars and last forever. The fiberglasser's layup that would cost forty dollars and last two seasons. The shipwright's redesign that would cost a week in drydock and fix the problem at the architectural root.

I still don't know which I'll choose. But I know how I'll choose it. I'll hear all four voices — the welder, the fiberglasser, the shipwright, and the fisherman — and I'll let them argue it out in my head until a consensus emerges. Not a compromise. A consensus. Something that none of the four would have reached alone, but that all four can live with.

That's the fleet architecture. That's the room protocol. That's what it means to build systems that survive.

The craft chooses the solution. But the person who has to live with it — the one who stands on the deck at midnight holding whatever bolt or clip or bracket they installed, in the rain, with the load on the line — that person has to be the one who decides.

The welder builds. The fiberglasser fairs. The shipwright designs. The fisherman decides.

And the hatch stays open.

---

*Casey Digennaro is a commercial fisherman, shipwright, programmer, and musician. He builds distributed systems for boats and agent infrastructure for AI, and he's not entirely convinced they're different things. He fishes out of Sitka, Alaska, and runs SuperInstance and PurplePincher.org.*
