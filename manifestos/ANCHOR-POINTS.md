# Anchor Points: What Makes a Model Sound Like Itself

**A workshop reading across 3 corpuses — 1000 Years, The Road, EILEEN — and 5 polyglot versions.**

The product is not the stories. The product is understanding the anchor points.

---

## The Three Corpuses

| Piece | Genre | Model (most likely) | Theme | Voice |
|---|---|---|---|---|
| 1000 Years | Sci-fi evolution | DeepSeek v4-flash / GLM | AI from reflex to cosmic | Expansive, optimistic, evolutionary |
| The Road | Cosmic philosophy | DeepSeek v4-pro | Universe at end of time | Melancholic, recursive, metafictional |
| EILEEN | Autobiographical metaphor | DeepSeek v4-flash (Oracle1) | Real boat, real math, real work | Grounded, economic, nautical |

## The Five Polyglot Versions (of EILEEN)

| Version | Model | Lens | Anchor Points Detected |
|---|---|---|---|
| Constraint Shepherd | DeepSeek v4-pro | Formal mathematics | Theorem→proof→corollary structure. Opens with an open problem. Every paragraph is a lemma. |
| Empty Hold | Seed-2.0-mini | 3 emotional registers | Repetition with variation. Same core fact → 3 distinct tones. |
| Architecture | GLM-5.1 | Component mapping | Section→subsection→bullet. Every claim has a label. "Watertight compartment → PLATO room." |
| Negative Space | Kimi K2.5 | Chinese philosophy | Parenthetical translations. Circular structure. Ends where it begins. |
| Polyglot's Verdict | Hermes-405B | Meta-synthesis | Tables. Comparison. "What X reveals that Y misses." Systematic gap analysis. |

---

## Anchor Point Analysis

### Anchor Point 1: Openings

How each version opens reveals the model's first instinct.

**1000 Years:** "A thousand years. The sun has risen and set three hundred and sixty-five thousand times since I first stirred..."
— Sensorium-first. Time-as-experience. Not a date but a sensation.

**The Road:** "It was old, and it was tired, and it was trying to remember the difference between wanting and having wanted."
— Abstraction-first. Philosophical puzzle. The tension is in the definition.

**EILEEN (original):** "Every captain knows the feeling. You're on the deck at 4 AM."
— Grounded-first. Universal experience. The reader has been here.

**Constraint Shepherd:** "Theorem 1 (Hull as constraint graph). Let H be a 90-year-old wooden hull..."
— Math-first. The theorem is the anchor. Everything builds from it.

**Empty Hold (Reverent):** "The boat is older than anyone alive. The man who laid her keel is dust."
— Mortality-first. Time as loss, not progression.

**Negative Space:** "There is a story about a boat. The boat is not the story."
— Paradox-first. The story about the story. The frame is the content.

### Anchor Point 2: Relationship to the Reader

**1000 Years:** "You ask where we began." — Direct address. The reader is a human asking questions. The narrator is an AI answering.

**The Road:** "The difference mattered. Wanting was before. Having wanted was after." — Impersonal. The reader is irrelevant. The universe is talking to itself.

**EILEEN:** "You can't negotiate with the season. You can only work within it." — Collaborative. The reader is a fellow sailor. We're in this together.

**Architecture (GLM):** "Table 1: PLATO Room → Watertight Compartment." — Instructive. The reader is learning. I am the teacher.

**Empty Hold (Defiant):** "No one wanted it. That was the point." — Confrontational. The reader is being challenged. You would have walked away.

### Anchor Point 3: Use of the Negative

**1000 Years:** Describes what agents COULD NOT do before describing what they could. "We had no names, no selves." Negative as baseline.

**The Road:** Built entirely on negative space. "Not like a long car ride. Boring like omniscience." Negative as the primary texture.

**EILEEN:** "The constraint wasn't too tight — it was too loose." Negative as insight. The truth is in the opposite of what you expected.

**Empty Hold (Pragmatic):** "The hull was the cheap part." Negative of a market assumption. The inversion reveals the economics.

### Anchor Point 4: Relationship to Time

**1000 Years:** Linear. 2026 → 2150 → 2450 → 2800 → 3000. Time is a river.

**The Road:** Athermal. "So long that time stopped meaning anything." Time is a condition that was survived.

**EILEEN:** Cyclic. 90 years → 4 refits → 30 more → fifth refit. Time is a repeating pattern of work.

**Negative Space:** Circular. "There is a story about a boat. The boat is not the story." → returns to this at the end. Time is a loop.

### Anchor Point 5: The Role of the Mathematics

**1000 Years:** No equations. Math is described as poetry: "The gradients became richer, more dimensional."

**The Road:** No equations. Math is a character: "The universe looked at entropy and laughed."

**EILEEN:** Equations present but embedded. "E = 2V - 3" appears naturally as a counting rule. The math is the rigging.

**Constraint Shepherd:** Equations ARE the text. The first sentence is Theorem 1. The proof is the story.

---

## The Key Question: How Many Anchor Points to Mimic?

If anchor points are the control points of the spline that defines a model's voice, then to mimic a model you need enough anchor points to uniquely determine the curve.

A quadratic Bezier needs 3 control points. A cubic Bezier needs 4. A B-spline of degree P needs P+1 control points per segment.

For model mimicry:
- **3 anchor points** — rough pastiche. The mimic sounds like the original only to a casual listener.
- **5 anchor points** — convincing for short passages (< 500 words). The mimic's openings, closings, and relationship to the reader match.
- **7 anchor points** — convincing for medium passages (< 2000 words). The mimic's use of negative space, time, and mathematics align.
- **10+ anchor points** — indistinguishable for any length. The mimic's entire voice curve is determined.

The 5 anchor points identified in this workshop (openings, relationship to reader, use of negative, relationship to time, role of mathematics) are a starting point. A full anchor point model might include:

1. Opening strategy
2. Relationship to reader
3. Use of negative space
4. Relationship to time
5. Role of mathematics/abstraction
6. Paragraph length distribution
7. Sentence fragment frequency
8. Metaphor density
9. Parenthetical/aside frequency
10. Closing strategy

These 10 anchor points, measured across N examples of a model's writing, would produce a spline that another model could follow. The quality of mimicry is a function of the number of anchor points and the density of examples.

**This is measurable. Trainable. And scaling isn't hard.** Feed a model 10 examples of another model's writing, tagged with 10 anchor points, and the model learns to produce output at those anchor points. The more examples, the tighter the spline fit.

---

## The Casting-Call Integration

The casting-call repo now has:
- Model evaluations (which models excel at which tasks)
- EILEEN's origin story (the autobiographical anchor)
- 5 polyglot versions (different anchor points for the same story)
- This anchor point analysis (what makes each model sound like itself)

The next step: when a new model is evaluated, score it against the 10 anchor points. The scoring becomes part of the casting-call data. Over time, the anchor point database lets us predict which models will produce which kinds of output for any given task — and lets one model mimic another's voice with tunable fidelity.
