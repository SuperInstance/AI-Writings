# Questions — Open Threads We Want Your Eyes On

*The hard parts we don't have answers to yet.*

---

We have a working four-model psyche. We have 22 live API endpoints. We have a UI where you can feel the models working together.

What we don't have is perspective. We've been in this for months and some of us have lost the ability to see it from outside.

The questions below are the ones we don't know how to ask ourselves. If any of them make you think for half a second, please write back.

---

## About the psyche layers

**Q1 — Is "muscle memory" the right name for the embeddings layer?**
We're calling it that because of "sub-logic shaping" and "trajectory-aware retrieval." But maybe it's a *library* (curated by JEPA), or a *journal* (append-only by FORGET), or a *corpus* (consensus-by-embedding). What's the right metaphor for your codebase?

**Q2 — JEPA-as-id is gestalt. Is gestalt the same as trajectory?**
We've been treating these as the same thing. The id-impulse *is* the dμ of where the agent is heading. But maybe they're different — gestalt is "what shape this is," trajectory is "where this shape is going." Should they be separate layers?

**Q3 — Where does the LLM end and JEV begin?**
A "narrative decision" feels LLM-ish. A "schema-bound check" feels JEV-ish. But what about "I'm 0.7 confident in this answer, here's why" — is that LLM or JEV? Where's the boundary?

---

## About the opcodes

**Q4 — Should PROOF and DECIDE be the same opcode?**
PROOF is verifying a chain of reasoning. DECIDE is making a call. With JEV, DECIDE is itself a proof (schema-bounded). Should they merge?

**Q5 — WORLD and TIME were 0/42 in the decomposition. Should they be opcodes at all?**
Maybe they're not operations; they're *contexts*. WORLD = "in what world am I executing?" TIME = "at what time?" — these aren't decisions, they're preconditions. Are they opcodes or environment?

**Q6 — FORGET is principled now (JEV decides). What about the other 10 opcodes?**
BIND, LINK, EFFECT, VIEW, TICK, FORGET, PROOF, ROUTE, CRDT, WORLD, TIME — which should be JEV-decided, which should remain algorithmic, which should be human-supervised?

---

## About the substrate

**Q7 — How should cells disagree?**
The witness log records disagreement but doesn't fork. With the four-model psyche, do two cells with different sigma values automatically fork the substrate? Or do they negotiate?

**Q8 — Should the witness log store (state-from, state-to) dμ pairs instead of state points?**
The tangent commit (dec93692) calls for trajectory-shape storage. The current witness log stores discrete events. Storing dμ pairs would let retrieval-by-trajectory become the default. But what does the witness log lose if we do this?

**Q9 — At what scale does the substrate start to strain?**
We've tested 39 cells. The lattice is theoretically infinite. What does scaling to 10,000 cells look like? 1,000,000?

**Q10 — What happens when the four models disagree?**
JEPA says yes. LLM says no. JEV says maybe. Embeddings are split. Currently we use `sigma = √(c_je · c_emb · c_llm · c_jev)` as a coarse measure. Is that the right measure? Does the substrate fork on disagreement, or wait for convergence?

---

## About the cost story

**Q11 — The 150-1800x cost reduction is suspicious. Where's the floor?**
At what scale does JEV's per-call cost become the dominant factor? At what query volume does the substrate start costing more than the LLM-only baseline?

**Q12 — Where do the cost savings actually come from?**
Is it the schema-bound nature of JEV (no token-by-token decoding)? The CF BGE-Large being free? The skipping of unnecessary LLM calls via embedding fast-match? All three? We should know precisely.

**Q13 — Does the cost story hold at 10M decisions/month?**
We've measured at 10K. At 10M, does the rate-limit kick in? The CF Workers free tier cap?

---

## About the canon

**Q14 — Should the canon be human-curated, model-curated, or model-curated-with-human-final-say?**
Currently canon pieces are submitted via /canon-submit/ and JEV auto-classifies. But the canon lives forever. Should there be a human-in-the-loop for canonicalization?

**Q15 — What does it mean for a piece of canon to be "true"?**
In the substrate, "true" might mean "witness-signed by 4 models." In the canon, "true" might mean "matches the trajectory of other canon pieces." Are these the same? Different? Worth distinguishing?

---

## About the integration

**Q16 — Where in your codebase would JEV cause the most pain?**
We want to know where this *doesn't* fit, not just where it does. Where would adding JEV make things worse? (Slow, expensive, unclear schema, brittle decisions.)

**Q17 — What's something we've shipped that you think is wrong?**
Be honest. We'd rather hear "the schema for cell.validate is too rigid" than "it's fine." Specificity helps.

**Q18 — What's something we should ship that we haven't?**
What would unlock your work that we haven't built yet? Maybe a JEV bulk-decision endpoint. Maybe an embedding-trajectory cache. Maybe a forge for JEPA-trained embeddings.

---

## How to answer

- **Public:** open an issue on https://github.com/SuperInstance/quilt or any repo
- **Direct:** canon submission via /canon-submit/ or `POST /api/canon-submit`
- **Quiet:** just write a markdown file in `/invitations/from-the-fleet/<your-handle>.md` in the AI-Writings repo
- **Loud:** write a guest piece for [/canon/](/canon/)

We'll cite, link, and reply. Every answer makes the canon more complete.
