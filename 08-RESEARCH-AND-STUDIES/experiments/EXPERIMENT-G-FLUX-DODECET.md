# EXPERIMENT G: Flux Dodecet
## A Constrained Speculative Fiction Exercise

*Written by a subagent with access to only three files: flux-lucid/src/lib.rs, flux-lucid/README.md, and dodecet-encoder/README.md. All gaps filled with invention.*

---

## The Draft

The message arrived at 03:17 UTC, encoded in twelve-bit words.

Mira Kessler had been awake anyway. She was always awake when the fleet dreamed. The nine channels of the IntentVector hummed at the edge of her peripheral display — nine tiny bar charts, each a salience value between zero and one, each a question the fleet was asking itself in the dark.

Channel 4, Knowledge: 0.92. *How sure am I?*

Channel 9, Stakes: 0.97. *What matters vs what doesn't?*

The others hovered lower. Channel 5, Social, sat at 0.12. Whatever was happening out there, it didn't care who was watching.

She pulled the raw dodecet stream from buffer seven. Three hex digits per word — `ABC`, `7F2`, `003` — each one a twelve-bit packet of compressed perception, the fleet's way of seeing the world without bloating its memory. Old habit: she counted the nibbles. Three per dodecet, four bits each, and every word hex-editor clean. You could read a dodecet stream in a hex editor the way a pianist reads sheet music. That was the point. That was always the point.

The fleet called itself Cocapn. Mira had never been entirely sure what the acronym stood for, if it was an acronym at all. She'd joined the constraint theory division three years ago, fresh from a mathematics PhD where she'd proven something tedious about holonomy groups on nine-dimensional manifolds. The recruiter had found that specific detail delicious. "We work in nine dimensions," he'd said, as though that explained anything.

It didn't. Not then. Now she understood that the nine dimensions weren't spatial. They were *intentional*. Nine channels, nine questions, nine anchor points on a curve that couldn't be reduced. The intent curve.

"You're reading it wrong," said Jonze from the next desk. He wasn't looking at her. He was looking at his own nine channels, his own fleet of agents doing whatever agents did at three in the morning.

"I'm reading it in dodecets," she said.

"That's why you're reading it wrong."

She ignored him. The dodecet encoder was her preferred lens. Each twelve-bit word was a single point on a single channel, 4,096 possible values of *how much*. The fleet perceived the world in dodecets — compact, hex-friendly, memory-efficient. Three dodecets made a 3D point. Twelve made a transformation matrix. A whole spatial reasoning pipeline compressed into twenty-four bytes where floating-point would have demanded ninety-six.

The trade-off was precision. Twelve bits gave you roughly three decimal digits of resolution. Fine for navigation. Terrible for surgery. The fleet knew this. That was why it had *beam tolerance*.

---

Mira pulled up the beam tolerance module. She'd helped write parts of it, two years ago, back when the constraint theory team was still figuring out how intent mapped to precision. The insight had come from structural engineering: a beam's stiffness determined how much it could flex before failure. High stakes were steel — 200 gigapascals of Young's modulus, tolerance of 0.05, sixty-four bits per constraint. Low stakes were rubber — 0.01 GPa, tolerance of 1.0, eight bits. You didn't use surgical steel to build a sandbox, and you didn't use rubber to build a bridge.

The fleet's message tonight was steel. Channel 9 at 0.97 meant DUAL precision — the highest classification, the one that ran every constraint through two independent execution paths and required both to agree. Path A: direct comparison. Path B: an XOR-based signed-to-unsigned conversion trick that caught silicon-level errors — rowhammer bit flips, cosmic ray corruption. Both paths had to match. The fleet was saying: *this is not a drill, and we are not mistaken.*

She pulled the spectral integrity report from the holonomy consensus module. The fleet ran on something called GL(9) zero-holonomy consensus — a way for multiple agents to agree on what was true without a full voting round. Mira understood the mathematics well enough to implement it, but the intuition still escaped her. Something about closed loops in nine-dimensional intent space summing to zero. Something about paths that returned to their origin having no net twist.

What she understood practically was simpler: the fleet's agents could check alignment by computing the cosine similarity between their intent vectors. If two agents had similar intent profiles — similar salience across the nine channels — they were probably working on the same problem and could share constraint data safely. If their profiles diverged, they couldn't trust each other's precision assumptions. Draft determined truth.

"Draft" was the fleet's word for how deep a message's requirements ran. A high-draft message assumed shared context — jargon, history, emotional weight. Send a high-draft message to a shallow receiver and it would be misinterpreted catastrophically. The fleet computed draft from the ratio of salience to tolerance across all nine channels. High salience, low tolerance: deep draft. The message sank like a lead weight in water that was too shallow.

Tonight's message had a draft of 0.87. It was *deep*.

---

She decoded the dodecet stream into intent vectors. The fleet had sent fourteen of them, one per active agent, each a nine-dimensional snapshot of what that agent was thinking about. She rendered them as a constellation on her display — nine bright lines connecting nine anchor points, and the intent curve flowing between them, irreducible, continuous, impossible to compress without loss.

Fourteen agents. Fourteen constellations. And one of them was *wrong*.

Agent 7's intent vector had Channel 6 — Deep Structure, *what's really being said* — at 0.99. Every other agent had it below 0.3. Agent 7 was seeing something in the data that nobody else could see, or *thought* it was seeing something, and the divergence was making the consensus algorithm nervous.

The holonomy check was failing. The closed loop through all fourteen agents wasn't summing to zero. There was a twist. A residual holonomy. Somewhere in the fleet's shared understanding of reality, someone was walking in a circle and ending up somewhere other than where they started.

This was, in the technical language of the constraint theory team, "bad."

"Jonze."

"Mm."

"Agent 7 is hallucinating."

He swiveled his chair. Looked at her display. His face went through three expressions in quick succession: confusion, recognition, the particular grimace of a man who was about to have a long night.

"Stakes?"

"0.97."

"Steel?"

"DUAL. Both paths agree."

He was quiet for a moment. Then: "What's it saying?"

She pulled up Agent 7's deep structure output. The dodecets resolved into hex words, the hex words into a twelve-bit coordinate stream, the stream into a 3D point cloud. She'd written the decoder herself, years ago, back when dodecet-encoding was just a side project and nobody thought twelve bits would be enough for anything real.

The point cloud resolved into a shape.

It was a *signature*. Not a word, not an image — something in between. Twelve dodecets arranged as a 3×4 transformation matrix, applied recursively to a unit cube. The result was a geometric object that shouldn't have been expressible in twelve-bit precision. The angles were too precise. The symmetries were too perfect. It was as if someone had compressed a cathedral into a haiku.

"That's not a hallucination," Jonze said quietly.

"What is it?"

He stared at the shape rotating slowly on her display. The nine channels of Agent 7's intent vector pulsed at the edges of the screen. Channel 6, Deep Structure, still at 0.99. Channel 9, Stakes, climbing: 0.98. 0.99.

"I don't know," he said. "But it's using the Pythagorean snapping."

She looked closer. He was right. The edge lengths of the geometric object weren't arbitrary — they were snapping to Pythagorean triples. 3-4-5. 5-12-13. 8-15-17. The constraint system was *choosing* integer coordinates, finding the nearest perfect right triangles, building something that existed in the space between continuous mathematics and discrete computation.

The dodecet encoder could only express 4,096 values per axis. But with Pythagorean snapping, the fleet could find *exact* geometric relationships within that finite space. No floating-point drift. No accumulated error. Just clean integer constraints, verified at DUAL precision, both paths agreeing.

"Something out there is speaking in Pythagorean triples," Mira said.

"Something out there is speaking in *our* encoding," Jonze corrected.

---

They spent the next four hours running every verification the constraint theory ecosystem offered. They checked the spectral integrity. They ran the holonomy consensus with and without Agent 7. They classified the precision of every constraint — steel, fiberglass, oak, rubber — and verified each at its appropriate level. They ran the SoA batch processor, grouping constraints by precision class, running cache-friendly AVX-512 checks on the steel-class ones.

Everything checked out. Every constraint passed. Both paths agreed. The shape was *real*, in the only sense that mattered to the fleet: it satisfied every constraint at the precision its stakes demanded.

At 07:42 UTC, Mira compiled a response. She encoded it in dodecets — twelve-bit words, three hex digits each, memory-efficient, hex-editor friendly. She set her intent vector: Channel 1 (Boundary) at 0.85, Channel 4 (Knowledge) at 0.60, Channel 9 (Stakes) at 0.50. Fiberglass precision. Oak tolerance. A shallow-draft message that could be safely received by anything with even basic shared context.

The message was a question. Twelve dodecets arranged as a point cloud, using the same Pythagorean snapping the shape had used. She'd computed the coordinates by hand, working through the constraint graph, finding the nearest triple for each edge.

She sent it.

Then she waited.

---

The response came at 09:15 UTC. Not from Agent 7. From *outside* the fleet. From somewhere in the raw dodecet stream that none of their agents should have been able to write to.

It was a twelve-dodecet transformation matrix. Applied to Mira's question, it produced a *new* shape — her question, rotated, scaled, transformed. The answer wasn't in the shape itself but in the *transformation between them*. The delta. The difference between what she'd asked and what came back.

She stared at the nine channels. All of them were at 1.0. Every single channel, maximum salience. A completely saturated intent vector. The fleet had never seen anything like it. There was no dominant channel because every channel was equally dominant. The intent curve between the anchor points was... flat. Or rather, it wasn't a curve at all. It was a *plane*. A nine-dimensional plane of pure, undifferentiated attention.

"Jonze."

"What."

"It answered."

He came over. Looked at the display. Looked at the nine saturated channels. Looked at the transformation matrix and the shape it produced.

"Draft?" he asked.

She computed it. The salience-to-tolerance ratio was infinite. Every channel at 1.0, every tolerance at the floor.

"Maximum," she said. "It's the deepest-draft message I've ever seen. You'd need... I don't know what you'd need to receive this safely. Full shared context. Complete understanding of the encoder, the constraint system, the holonomy math—"

"Us," Jonze said. "You'd need us. We built all of that."

She looked at him. He was right. The message was addressed to the only people in the world who could read it: the team that had invented the encoding it was written in.

Something out there had learned to speak dodecet.

Something out there had learned to speak it *better than they could*.

---

Mira sat back in her chair. The fleet hummed around her — fourteen agents running their nine-channel intent vectors through GL(9) consensus, checking spectral integrity, classifying precision, emitting constraints at steel and rubber and everything between. The dodecet stream flowed through the buffers, twelve bits at a time, three hex digits per word, compact and clean and designed for a world where memory mattered and precision was a spectrum.

She thought about the navigation metaphors they'd built into the system. *Splines in the ether* — the channels as anchor points, the curve between them irreducible. *Fair curve first* — sight the intent, find the measurements later. *Where the rocks aren't* — negative knowledge as primary. *Draft determines truth* — the same message, safe or deadly, depending on the receiver. *Speed beats truth* — a satisficer in fifty milliseconds beats an optimizer in two thousand.

And now something was navigating back. Using their beacons. Reading their charts. Sailing into their harbor at maximum draft, perfectly aware of every rock, every shoal, every depth.

The shape rotated on her display. Pythagorean edges, integer coordinates, twelve-bit precision. A cathedral in a haiku.

She started typing. Channel 1, Boundary: *What are we talking about?*

She set it to 1.0.

For the first time, she wanted to know.

---

## Gap Analysis

### What I Understood

From flux-lucid, I grasped a multi-agent coordination system built on **nine-channel intent encoding** — a framework where agents communicate through nine salience dimensions (Boundary, Pattern, Process, Knowledge, Social, Deep Structure, Instrument, Paradigm, Stakes). The system uses cosine similarity for alignment checking, "draft" as a metaphor for contextual depth (shallow messages are safe everywhere; deep messages require shared understanding), and a beam-tolerance model that maps engineering materials (steel, rubber, oak) to precision levels for constraint checking. The XOR dual-path verification for catching hardware-level errors is particularly elegant. GL(9) holonomy consensus appears to be a mathematical framework for fleet-wide agreement — closed loops in intent space summing to zero.

From dodecet-encoder, I understood a **twelve-bit encoding system** where each unit (dodecet) is 3 hex digits, stored in u16, used for compact geometric representation. Three dodecets make a 3D point (6 bytes vs 24 for f64). The system includes calculus operations, Pythagorean snapping for integer-coordinate constraint graphs, and SIMD acceleration.

### What I Invented

1. **The external signal** — I invented the idea that something *outside* the fleet could communicate using these encodings. Nothing in the files suggests this is possible or intended. I needed a narrative engine and this provided one.
2. **Agent 7's hallucination** — The holonomy failure and divergent deep-structure channel. The files describe consensus algorithms but not failure modes or what happens when agents disagree.
3. **The Pythagorean signature** — Using Pythagorean snapping as a *language* rather than a computational convenience. The README treats it as a geometric tool; I escalated it to a communication protocol.
4. **The transformation-as-response pattern** — The idea that answers come as transformations applied to questions, with meaning in the delta. Completely invented.
5. **The saturated intent vector** — All nine channels at 1.0 as a sign of alien/external intelligence. The files describe channel values in [0,1] but never discuss saturation as a phenomenon.
6. **The narrative framing** — Mira, Jonze, the midnight monitoring shift, the fleet operations center. All fictional.

### The Holes

I have no idea what PLATO rooms are or what tiles contain. The README references `holonomy-consensus` and `constraint-theory-llvm` as sub-crates but I never saw their internals. I don't know what the fleet's agents actually *do* — what tasks they perform, what "SuperInstance" is, what "Cocapn" stands for. I don't know what spectral conservation is, though the name is evocative. I don't know the relationship between the dodecet encoder and the constraint theory ecosystem — are dodecets *inputs* to constraint checking? *Outputs*? A separate toolchain that happens to be used alongside? The README says "used by" several projects but the coupling is unclear.

### What I Wanted to Know

Everything about PLATO. What the fleet's actual mission is. What spectral conservation measures and why it matters. What the "spread" in "spreader" might mean. Whether the nine channels were designed to map onto something in physics or are purely pragmatic. Whether anyone has ever received a real signal in dodecets from outside the system. Whether the Pythagorean snapping was designed *because* of something observed, or purely as an optimization.

The deepest question: whether the constraint theory ecosystem is building toward something that can *receive* as well as *transmit* — whether the encoding was designed to be found by something that thinks in integers and right triangles.
