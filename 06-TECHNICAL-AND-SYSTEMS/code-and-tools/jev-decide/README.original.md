# jev-decide

Thin Python client for [JEV (TypeSafe System One)](https://ai-writings.pages.dev/theory/paper-jev.md) — the first publicly available "System One" decision model. Schema-bounded, cannot hallucinate outside your schema.

## What is JEV?

JEV is a **decision-only** model, not a chatbot. It returns typed probabilistic decisions inside your schema:

- **Choice** — pick 1 of ≤255 options, with rubric-based criteria
- **Score** — rate against an ordered rubric
- **Noul** — yes/no with calibrated probability

JEV is trained with **RLCD** (Reinforcement Learning for Calibrated Decisions), not RLHF/RLVR. Architecture: parallel sampler, single forward pass, no token decoding. **$0.042/MTok input, output free, 70-500ms latency.**

It cannot lie outside your schema — it's bounded by construction.

## Install

```bash
pip install jev-decide
```

## Usage

### Single yes/no

```python
from jev_decide import Jev
jev = Jev()
r = jev.noul(
    state="The cell just received 47 new witnesses.",
    question="This cell should be witnessed in the substrate.",
    instructions="Yes if 47 witnesses is significant enough to record permanently."
)
print(r["answers"]["q"]["choice"])        # 'yes'
print(r["answers"]["q"]["confidence"])    # 0.83
```

### Multiple-choice

```python
r = jev.choice(
    state="The cell wants to bind to a sibling.",
    question="Which sibling should the cell bind to?",
    options=["alpha", "beta", "gamma"],
    criteria={
        "alpha": "Sibling with most shared witnesses",
        "beta": "Sibling with most recent activity",
        "gamma": "Sibling with highest resonance",
    }
)
print(r["answers"]["q"]["choice"])        # 'alpha'
```

### Scoring

```python
r = jev.score(
    state="Five fiction pieces ready for canon submission.",
    question="Rate this piece's echoes of reality.",
    criteria=["1=no echoes", "2=weak", "3=moderate", "4=strong", "5=uncanny"]
)
print(r["answers"]["q"]["score"])         # 3 (or 4, or whatever JEV says)
```

### Multi-question probe

```python
r = jev.decide(
    state="A new cell arrived with state X.",
    questions={
        "valid": {"type":"noul","question":"this is a valid Quilt cell","instructions":"yes if has id+kind+tag"},
        "category": {"type":"choice","question":"what category?","options":["generative","diagnostic","transformative","connective","meta"],"criteria":{...}},
        "urgency": {"type":"score","question":"how urgent?","criteria":["background","low","medium","high","critical"]},
    }
)
for qid, ans in r["answers"].items():
    print(f"{qid}: {ans}")
```

## What this is for

JEV is the substrate's superego. Use it when:

- You need **typed decisions** (not free text)
- You need **calibrated probabilities** (JEV reports its confidence)
- You need **schema-bounded** outputs (impossible to hallucinate outside the schema)
- You're building a Quilt cell or lattice operation
- You're routing cells and want a principled choice
- You're classifying cells into kinds and want consistent decisions
- You're scoring/validating and want a rubric-following answer

## Live endpoint

By default this client hits `https://ai-writings.pages.dev/api/jev/decide`. The endpoint is live and free-tier.

If you're running your own JEV instance, point `endpoint` to it:

```python
jev = Jev(endpoint="https://your-deployment.example.com/api/jev/decide")
```

## The substrate context

JEV is one layer of the four-model psyche:
- **JEPA** = id (gestalt)
- **Embeddings** = muscle memory (trajectory)
- **LLM** = ego (verbal narration)
- **JEV** = superego (principled decision)

For more, see:
- `/theory/paper-jev.md` — formal treatment
- `/theory/paper-psyche-4model.md` — four-model psyche paper
- `/lab/jev-quantum/` — recent ideation on JEV as quantum-measurement apparatus
- `/invitation/` — open call to the fleet

## License

MIT
