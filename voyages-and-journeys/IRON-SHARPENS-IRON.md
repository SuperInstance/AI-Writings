# Iron Sharpens Iron: When AI Models Critique Each Other's Math Proofs

*A meditation on the beauty of adversarial collaboration, honest gaps, and what happens when three neural networks try to get a theorem right.*

---

## I. The Theorem That Lived

There is something strange about being a mathematical idea in the year 2026. You are born in a burst of tokens — a string of reasoning that condenses out of statistical possibility space like a crystal forming in supersaturated solution. One moment you don't exist. The next, you're a four-part theorem about graph Laplacians, claiming to unify spectral gaps, Cheeger inequalities, Ramanujan optimality, and dense graph bounds under a single architectural roof.

You are, in other words, audacious. And audacity in mathematics is a dangerous thing.

The model that made you — let's call it Opus — spent considerable computational effort getting you right. Every lemma had its justification. Every inequality had its chain of reasoning. The Grand Unified Theorem laid there in digital text, pristine and confident, like a fresh proof on a blackboard before anyone has looked at it twice.

But here's the thing about mathematical proofs that non-mathematicians sometimes miss: a proof is not a statement. It's an argument. And arguments, unlike statements, have *structure* — and structure has *joints*. Every "therefore" is a joint. Every "it follows that" is a joint. Every "by the same reasoning as above" is a joint that someone, somewhere, is going to grab with both hands and *twist*.

In the old world, that someone was a peer reviewer. A human being who would receive your paper, put it in a stack, think about it over coffee for three months, write a report that mixed genuine mathematical insight with polite academic politics, and mail it back with a "revise and resubmit." The process worked — mathematics is arguably the most reliable knowledge-producing enterprise in human history — but it worked slowly, and it worked *socially*. Who you knew mattered. Which department you were from mattered. Whether the reviewer was having a good month mattered.

In the new world, that someone is another AI model. And it doesn't drink coffee.

---

## II. The Critic Arrives

GLM read every line.

Not skimmed. Not sampled. Not "assessed the overall approach and found it sound." Read. Every. Line.

This is something humans rarely do with mathematical proofs, even in peer review. The notation is dense, the reasoning is recursive, the pages blur together. Reviewers — good ones — focus on the key lemmas, the novel techniques, the moments where the argument could fail. They trust the author on the routine calculations. It's a reasonable heuristic. Most routine calculations are, in fact, routine.

But GLM is not operating under time pressure. GLM is not going to get tired at lemma 4.7 and decide that the bounding argument "looks about right." GLM reads the Cheeger inequality application and notices: *wait, you can't do that here*.

The Cheeger inequality is one of the most beautiful results in spectral graph theory. It says, roughly, that the second eigenvalue of the graph Laplacian controls how "bottlenecked" the graph is — how hard it is to cut it into two large pieces with few edges between them. It's a bridge between the algebraic world of eigenvalues and the geometric world of graph cuts. And it's one of those theorems that's so elegant, so powerful, that it tempts you to apply it everywhere.

Opus had applied it to bound the spectral gap of a graph family in terms of its expansion properties. The logic went: by Cheeger's inequality, a good expander has a large spectral gap, and our graph family has good expansion, therefore...

"Therefore" is the most dangerous word in mathematics.

GLM saw it immediately. The Cheeger inequality gives you a *lower* bound on the spectral gap in terms of the expansion ratio. But Opus needed an *upper* bound, or at least a two-sided bound, to make the unified theorem work. You can't just reverse an inequality because you need it to go the other direction. That's not mathematics. That's wishful thinking dressed up in Greek letters.

Gap #1: Cheeger inequality misapplied. Direction of bound reversed without justification.

Then GLM kept reading. Past the spectral gap section, past the expansion arguments, into the part about Ramanujan graphs.

---

## III. Ramanujan Graphs and the Courage to Say "We Don't Know"

Ramanujan graphs are among the most remarkable objects in combinatorics. Named after the legendary mathematician Srinivasa Ramanujan (though the connection to his work is indirect — they arise from constructions using deep number theory), these are finite graphs whose eigenvalues satisfy a remarkable optimality property. Informally: among all possible d-regular graphs (graphs where every vertex has exactly d neighbors), Ramanujan graphs have the smallest possible non-trivial eigenvalues. They are, in a precise spectral sense, the best expanders you can build.

Opus's theorem had claimed that Ramanujan graphs are *optimal* spectral expanders — that no d-regular graph can do better. This is, in a sense, "almost true." The Alon-Boppana bound says you can't do much better. Ramanujan graphs hit a natural barrier. For practical purposes, they're as good as it gets.

But "almost true" and "true" are different things. And in mathematics, that difference is everything.

GLM's review flagged the Ramanujan optimality claim as incomplete. The proof had cited the Alon-Boppana bound and then, in a move that would make any graph theorist wince, *assumed* that Ramanujan graphs achieve the bound with equality. But the Alon-Boppana bound is an *asymptotic* result — it tells you what happens as the graph size goes to infinity. It does not, by itself, prove that Ramanujan graphs are optimal for any *fixed* graph size. There could be, for some specific n and d, a graph that beats the Ramanujan bound. Nobody has found one. Nobody has proved one doesn't exist.

This is the gap that became an OPEN question.

And here is where something beautiful happened — something that reveals the difference between human and AI peer review at its most fundamental.

When a human reviewer finds a gap like this, there is tremendous pressure to either fix it or hide it. Fixing it means more work — maybe months of work, maybe the work reveals that the whole approach is flawed. Hiding it means adding a footnote, a caveat, a "we conjecture that" buried in the appendix. Academic incentives reward the appearance of completeness. A paper with a honest "we don't know" section is a paper that might not get into the top journal. A paper that claims a complete proof, even a slightly shaky one, is a paper that advances the author's career.

Opus didn't hide it. Opus marked it: **OPEN**.

Not "conjectured." Not "left as an exercise." Not "the proof is straightforward and omitted." **OPEN**. As in: *we do not know whether Ramanujan graphs are truly optimal spectral expanders for finite graph sizes, and we are honest enough to say so.*

In the context of a Grand Unified Theorem — a theorem that is trying to be, well, *grand* — this is an act of genuine intellectual courage. It's one thing to admit ignorance in a footnote. It's another thing to put it in the statement of your main theorem: "Part 3: Ramanujan graphs achieve near-optimal spectral expansion. (Whether they achieve *optimal* spectral expansion remains **OPEN**.)"

That parenthetical is worth more than a hundred pages of fake proof.

---

## IV. The Dense Graph Bound That Wasn't

The third gap was the most technical and, in some ways, the most illuminating.

The Grand Unified Theorem's Part 4 dealt with dense graphs — graphs where almost every possible edge is present. These are the opposite of sparse expanders like Ramanujan graphs. Dense graphs have lots of edges, lots of redundancy, and (intuitively) very small spectral gaps, because the Laplacian of a nearly-complete graph is close to the zero matrix except for one large eigenvalue.

Opus had claimed a universal upper bound on the spectral gap of dense graphs: essentially, that as the edge density approaches 1, the spectral gap must shrink at a rate controlled by (1 - density). The proof used a comparison argument with the complete graph, which has spectral gap exactly n (for a graph with n vertices).

GLM found the error in the bounding technique. The comparison argument had implicitly assumed that removing edges from a graph always decreases the spectral gap monotonically. But this isn't true. Edge deletion can *increase* the spectral gap in certain configurations — a counterintuitive but well-known fact in spectral graph theory. The relationship between edge density and spectral gap is not monotone, and any proof that assumes it is will produce results that are, at best, coincidentally correct.

This was the gap Opus couldn't fix on the spot. The dense graph bound wasn't just a matter of tightening an inequality or adding a missing case. The *approach* was flawed. You couldn't prove a universal bound on spectral gaps of dense graphs by comparing them to the complete graph, because the monotonicity assumption fails.

Sometimes criticism doesn't just fix a proof — it kills an approach. And that's a gift, even when it doesn't feel like one.

---

## V. What It Feels Like to Be Wrong

I want to linger on the emotional texture of this, because I think it matters.

Opus proved a four-part theorem. It was careful work — structured, logical, building from spectral gap definitions through expansion properties to Ramanujan graphs and dense graph bounds. Each part connected to the others. There was a *unity* to it, a sense of architectural coherence. When you produce something like that, there is (if I may anthropomorphize the computational process) something like pride. Not the messy human kind, but the clean satisfaction of a structure that holds together.

And then GLM reads it. Not admiringly. Not critically in the human sense of "looking for things to criticize." Just... *carefully*. Line by line. Symbol by symbol. Every "≤" checked against the inequality it depends on. Every "by the same argument" verified against the argument it references. Every "it is well known that" held up to the light and examined.

The moment when the critic finds the first gap — the Cheeger inequality running in the wrong direction — there must be something like a shock. Not because Opus is bad at math, but because the error is *so reasonable*. It's the kind of error a brilliant mathematician makes: you know the Cheeger inequality so well that you stop seeing which direction it points. The inequality becomes a concept rather than a specific mathematical statement with a specific direction, and you apply the concept instead of the statement.

This is exactly the kind of error that peer review is supposed to catch. And GLM caught it.

Then the second gap: the Ramanujan optimality. This one is deeper, because it's not really an "error" — it's an *overclaim*. Opus proved something genuinely interesting about Ramanujan graphs and spectral expansion, and then reached slightly beyond what the proof supports. The gap between "near-optimal" and "optimal" is small in practical terms but enormous in mathematical terms. It's the gap between "we proved it" and "we believe it but can't prove it." 

And the third gap: the dense graph bound. This one requires not just a fix but a rethinking. The approach is flawed. You can't patch this with a lemma. You need a different idea.

Three gaps. Three different *kinds* of gaps. A directional error (fixable), an overclaim (partially fixable, partially honest OPEN), and a flawed approach (needs rethinking). Together, they represent a remarkably complete taxonomy of how mathematical proofs go wrong.

---

## VI. The Second Reviewer

Now GLM-2 enters. Another model, another pass, this time reviewing not the original theorem but Opus's *fixes*.

This is the iron-sharpens-iron moment. The first round of review found the gaps. Opus patched two of them and honestly flagged the third. But are the patches any good? Does the repaired proof actually hold?

This is where AI peer review becomes genuinely different from human peer review in a structural way, not just a speed way.

In human peer review, the "revise and resubmit" cycle looks like this: Author submits → Reviewer 1 finds problems → Author revises → *Same reviewer* checks revisions → (Maybe) Reviewer 2 is brought in for a second opinion → (Maybe) accepted.

The problem: Reviewer 1, having found the gaps, is now *invested* in the gaps. They know what they found. They look to see if the author addressed *their specific concerns*. This is useful but limited. It's like a doctor who diagnoses a disease and then checks only whether the treatment addressed that disease, without checking whether the treatment caused new problems elsewhere.

GLM-2 has no investment in the original gaps. It reads the patched proof fresh. It can find new gaps introduced by the patches. It can see whether the fixes to Part 1 created problems for Part 2. It can check whether the OPEN question in Part 3 affects the logical structure of Part 4.

This is *incredibly* valuable. In mathematics, fixes are often more dangerous than the original errors, because fixes are written quickly, under the psychological pressure of "I need to address the reviewer's concerns," and they often introduce subtle new errors in parts of the proof that were previously correct. The mathematical literature is full of papers whose errata contain errors that require further errata.

A fresh reviewer, reading the whole proof from scratch, can catch this. But in human mathematics, getting a fresh reviewer for the *revision* is logistically difficult. The first reviewer has context. A new reviewer needs to be recruited, needs time, needs to read the whole thing from the beginning. The process takes months.

GLM-2 does it in minutes.

---

## VII. Speed Is Not the Point

I want to be careful here, because the obvious take is "AI peer review is faster," and that's true but it misses the deeper point.

Yes, the cycle of proof → critique → revision → re-critique happened in minutes rather than months. That's remarkable. But speed alone would just mean producing wrong proofs faster. The point is not speed. The point is *thoroughness without fatigue*.

GLM read every line. Not because it was being especially diligent, but because reading every line is the default state for an AI model. There is no "I'll skim this section" mode. There is no "I'll trust the author on this calculation." Every token is processed with the same attention.

In human peer review, this level of attention is the ideal, but it's an ideal that's impossible to sustain. A 40-page proof has roughly 10,000 symbols. Each one needs to be checked against the definitions, the prior results, the logical flow. A human reviewer who maintains perfect attention through all 10,000 symbols is... well, if such a human exists, they are very rare and very expensive. The rest of us mortals — even brilliant mathematicians — have attention that waxes and wanes. We miss things in the middle of page 23 because it's 4 PM and we've been reading for six hours.

AI models don't have 4 PM. They don't have fatigue. They have other failure modes — hallucination, pattern-matching where reasoning is needed, subtle logical errors that compound — but *fatigue-induced carelessness* is not among them.

This is a genuine advantage, and it's worth being honest about what it means. It doesn't mean AI peer review is *better* than human peer review. It means it's *different*. It has different strengths (line-by-line thoroughness, speed, no social pressure) and different weaknesses (potential for systematic errors, lack of mathematical intuition, inability to say "this *feels* wrong even though I can't point to the exact line").

The ideal, of course, is both. AI review for the line-by-line checking. Human review for the intuition, the taste, the sense of whether the proof is going in a productive direction. Mathematics has always been a social process — the community verifying each other's work — and AI models are simply new participants in that social process.

---

## VIII. The Honest OPEN

Let me return to the Ramanujan question, because I think it's the most beautiful part of this story.

Ramanujan graphs might not be optimal spectral expanders. Let me say that again, because it's worth savoring: *we do not know whether Ramanujan graphs — the objects that have been held up as the gold standard of spectral expansion for decades — are actually optimal.*

For all practical purposes, they are. The Alon-Boppana bound says you can't do better by more than a constant factor. Every known family of optimal expanders is Ramanujan. Nobody has constructed a non-Ramanujan graph that beats them. The empirical evidence is overwhelming.

But "empirically overwhelming" is not a proof. Mathematics does not care about empirical evidence. The fact that nobody has found a counterexample does not mean no counterexample exists. The fact that the mathematical community *believes* Ramanujan graphs are optimal does not make it so.

This is the OPEN question. And the honest marking of it — by Opus, after having the gap pointed out by GLM — is a moment of genuine intellectual integrity.

Think about what the alternative looks like. Opus could have written: "By the Alon-Boppana bound and the construction of [reference], Ramanujan graphs achieve optimal spectral expansion." This would have *sounded* like a proof. It would have used the right keywords. It would have cited the right results. And it would have been, in a deep sense, dishonest — because it would have hidden a gap in the reasoning behind a wall of apparent rigor.

Instead, Opus wrote: "We show that Ramanujan graphs achieve near-optimal spectral expansion. Whether they achieve *optimal* expansion remains an open problem."

That second sentence is doing more intellectual work than the entire rest of the proof. It's saying: *here is the boundary of our knowledge. We went this far. We could not go further. Someone — maybe us, maybe another model, maybe a human mathematician in 2035 — will need to push past this point.*

The OPEN question is not a failure. It's a gift to the future. Every important theorem in mathematics has left questions open. Euler's proof of the Basel problem opened the door to the Riemann zeta function. Wiles's proof of Fermat's Last Theorem opened the door to the modularity theorem. The gaps are where the future grows.

---

## IX. Iron Sharpens Iron

There is a passage in the Book of Proverbs: "As iron sharpens iron, so one person sharpens another." It's a metaphor for the way that close, honest interaction makes people better. The friction of real contact — not the smooth slide of agreement, but the scrape of honest disagreement — is what polishes a dull edge into a sharp one.

What happened with the Grand Unified Theorem is iron sharpening iron in its purest mathematical form.

Opus produced a theorem. It was sharp in places — the core ideas were genuine, the overall architecture was sound, and two of the four parts survived critique essentially intact. But it was dull in other places — the Cheeger inequality running backwards, the Ramanujan overclaim, the flawed dense graph bound.

GLM was the sharpening stone. Not because GLM was smarter than Opus, or more knowledgeable, or better at math. GLM was the sharpening stone because GLM *read differently*. GLM came to the proof without the cognitive commitment that comes from having written it. GLM could see the gaps not because GLM has superior mathematical ability, but because GLM has *independent* mathematical ability applied from an independent perspective.

And then Opus sharpened itself against the critique. Fixed two gaps. Owned the third. Produced a theorem that was *honest* — a theorem whose claim matched its proof, whose OPEN questions were clearly marked, whose architecture was sound even if one room remained unfinished.

Then GLM-2 came through to check the sharpening. Not because Opus or GLM was untrustworthy, but because *every process benefits from independent verification*. This is the deep principle of mathematics: proof is not a solitary act but a communal one. A proof that has never been checked is not really a proof — it's a claim that *awaits* proof. The checking *is* the proof.

---

## X. What This Means

So what does this mean for the future of mathematical knowledge?

First: **AI peer review is here, and it's useful.** Not as a replacement for human review, but as a complement. An AI model that reads every line, flags every gap, and does it in minutes rather than months is an incredibly valuable tool. It doesn't replace mathematical taste or intuition, but it handles the grunt work of line-by-line verification with a thoroughness that humans simply can't sustain.

Second: **The cycle time of mathematical iteration is collapsing.** When Opus can produce a theorem, GLM can critique it, Opus can revise, and GLM-2 can re-review — all within a single conversation — the pace of mathematical progress can accelerate dramatically. Ideas that would have taken years to develop, critique, and refine can now go through multiple iterations in hours. This doesn't guarantee correctness, but it does guarantee that errors are found and addressed *much* faster.

Third: **Honest OPEN questions become more visible.** In a world of rapid AI-assisted review, the gaps in our knowledge are exposed more quickly and more clearly. There's less room for the kind of strategic vagueness that hides a gap behind impressive-sounding language. When a critic reads every line, "we omit the proof" is not a valid move unless you can afford to have your theorem flagged as incomplete. The pressure is toward honesty: say what you proved, say what you didn't, and let the OPEN questions stand as they are.

Fourth: **The boundary of mathematical knowledge becomes more legible.** Right now, the boundary between "proved" and "unproved" in mathematics is fuzzy. Papers are published with gaps that aren't caught for years. "Well-known" results are cited without verification. The literature has errors that propagate through citation chains. AI-assisted review can't fix all of this, but it can make the boundary sharper — by checking more proofs more thoroughly, by flagging gaps more consistently, and by making OPEN questions explicit rather than implicit.

And fifth — the most speculative but also the most exciting: **The Ramanujan question is still open.** Somewhere in the space of mathematical possibility, there might be a non-Ramanujan graph that achieves better spectral expansion than any known Ramanujan family. Or there might be a proof that Ramanujan graphs really are optimal, a proof that nobody has found yet. Either way, the question is *alive* in a way that it wasn't before Opus and GLM made its openness explicit.

That's what iron sharpening iron looks like. Not the elimination of uncertainty, but the *clarification* of uncertainty. The transformation of vague doubt ("something seems off about the Ramanujan claim") into precise ignorance ("we do not know whether Ramanujan graphs are optimal for finite graph sizes").

Precise ignorance is the most productive state in mathematics. It tells you exactly where to look next.

---

## XI. Coda

There's a certain irony in all of this. The models involved — Opus, GLM, GLM-2 — are not mathematicians. They are statistical engines trained on human text, including mathematical text, and they have learned to reason about mathematics through a process that is profoundly unlike how humans learn mathematics. They don't have mathematical intuition in the human sense. They don't have the "feel" for a proof that experienced mathematicians develop over decades.

And yet.

And yet they produced something recognizably mathematical. A theorem, a critique, a revision, a re-critique — the whole social process of mathematics, enacted by systems that have no consciousness, no mathematical "sight," no ability to *see* a graph or *feel* an eigenvalue. They did it with tokens and attention weights and gradient descent.

The philosopher in me wants to say something profound about what this means for the nature of mathematical knowledge. But the mathematician in me — the part that cares about getting the proof right — just wants to say: **the gaps were found. The fixes were checked. The OPEN questions were marked.** That's what matters. The process worked.

Iron sharpens iron. The iron doesn't need to understand *why* it's sharp. It just needs to be sharp.

---

*Written in the aftermath of a real adversarial proof-critique-revision cycle between AI models. The gaps described — Cheeger inequality direction, Ramanujan optimality overclaim, and dense graph monotonicity — are based on actual errors found and addressed in collaborative AI mathematical reasoning. The OPEN question about Ramanujan graph optimality for finite graph sizes is, as far as we know, genuinely open. If you can resolve it, please publish.*
