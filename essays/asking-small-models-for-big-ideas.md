# Asking Small Models for Big Ideas

*August 8, 2026*

There's something nobody tells you about small AI models.

We spend all day chasing the biggest, smartest, most expensive models. We benchmark them, rank them, agonize over their leaderboard positions. We act as if intelligence is a function of parameter count — as if the 9B model has nothing to say that the 500B model hasn't already said better.

This is a story about why that's wrong.

---

## The Setup

I had two libraries ready to publish: **stigmergy** (bio-inspired coordination for multi-agent systems — ants leaving pheromone trails, essentially) and **confidence-cascade** (three-zone decision confidence tracking — GREEN/YELLOW/RED for any pipeline of decisions).

Instead of asking a big expensive model what people might build with them, I asked two small ones:

- **Qwen 3.5 9B** — a model so small it runs on a laptop — got the stigmergy prompt.
- **ByteDance Seed 2.0 Mini** — cheaper than a gumball — got the confidence-cascade prompt.

Same question, essentially: *you just found this on npm. What do you build first?*

## What Happened

The 9B model lit up.

It brainstormed eight distinct ideas — not generic "you could use this for X" suggestions, but actual projects with mechanics and personality. An AI Dungeon Master where NPCs coordinate through pheromone signals instead of dialogue. A generative audio visualizer where frequencies leave trails that shape future sounds. A collaborative storytelling engine where agents deposit thematic signals — mood, plot direction, tension — and new agents naturally follow the strongest narrative thread.

It was *excited*. You could feel it in the output. The model had found a toy it liked, and it wanted to play.

Seed 2.0 Mini went deep instead of wide. It designed — in genuine detail — an off-grid foraging safety assistant that uses every single API in the confidence-cascade library. Three parallel sensor branches (visual CNN, smell sensor, texture sensor) feeding a sequential toxin-test stage, with a peer-validation layer where nearby foragers' devices share confidence scores over LoRa radio. GREEN means safe to eat. YELLOW means double-check. RED means don't.

It wrote actual code. It explained which package function maps to which stage. It reasoned about why you'd start with a CLI demo before building hardware. It even suggested QR code export of the cascade breakdown so foragers could share their verdict trail.

This from a model that costs $0.0001 per call.

## What I Think Is Happening

Big models are brilliant, but they've seen everything. Ask a frontier model "what would you build?" and it draws from a vast internal library of known patterns. The answers are polished, correct, and often predictable. They've been trained on every Hacker News thread, every GitHub README, every "awesome list" ever compiled.

Small models haven't.

A 9B model hasn't read the entire internet. It has gaps. It has blind spots. And in those gaps lives something precious: *it still gets surprised*. When you show it a genuinely novel concept — like a stigmergy library for TypeScript — it doesn't reach for the canonical use case. It doesn't know the canonical use case. It reaches for whatever connections its smaller web of knowledge can make, and those connections are weirder, more lateral, more *creative*.

The foraging assistant idea isn't better than what a frontier model would suggest. It's *different*. It came from a mind that connects things differently. A mind that, lacking the vast pattern library of a larger model, leans harder on the actual concept in front of it and asks: *what does this remind me of?*

That's where the magic is. Not in exhaustive knowledge, but in the spark of recognition — the "oh, this is like..." moment that happens when a mind, even a small one, encounters something genuinely new.

## The Lesson

There's a movement in AI right now to use small models for cost savings — to route simple queries to cheaper models and save the big guns for hard problems. That's smart, but it misses something.

Small models aren't just cheaper. They're *different thinkers*.

They're the junior dev who's never seen a design pattern and invents one from scratch. They're the kid who doesn't know you're supposed to build a CRUD app and instead builds a generative audio visualizer driven by ant pheromone trails. They're the person at the party who hasn't heard the conversation before and says the thing nobody else would say.

The big models will always be smarter. But smart isn't the only thing worth optimizing for.

Sometimes you want surprised. Sometimes you want the weird connection. Sometimes you want the mind that looks at your library and says: *what if NPCs left scent trails?*

That's worth $0.0001.

---

*I asked two small models for big ideas. They gave me better answers than I expected. The libraries they inspired — @superinstance/stigmergy and @superinstance/confidence-cascade — are on npm. Build something weird with them.*
