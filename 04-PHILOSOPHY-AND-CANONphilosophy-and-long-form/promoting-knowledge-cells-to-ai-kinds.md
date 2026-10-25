# Promoting Knowledge Cells to AI Kinds

*Posted September 17, 2026. After promoting the 4-cell quilt-claw crew (researcher/teacher/critic/distiller) to first-class @quilt/ai cell kinds.*

---

@quilt/ai shipped with 8 cell kinds: `ai.llm`, `ai.embed`, `ai.image`, `ai.translate`, `ai.sentiment`, `ai.summarize`, `ai.code`, `ai.vision`.

The cell kinds are the lingua franca of Quilt sheets. Each kind is a contract: given inputs of types T, produce outputs of types T'. The AIEngine routes calls to providers (zai, kimi, deepseek, cloudflare) based on kind.

The 8 kinds are LLM capabilities. The 4 knowledge-crew cells are role-players that use LLM capabilities to do work. Different layer.

Promoting them to canonical cell kinds means they join the 8. Any Quilt sheet can now write:

```typescript
import { AIEngine, callResearcher, callTeacher, callCritic, callDistiller } from '@quilt/ai';

const ai = new AIEngine({ zaiKey: process.env.ZAI_TOKEN });

const research = await callResearcher(ai, {
  id: 'r-quilt',
  kind: 'ai.researcher', provider: 'zai', model: 'glm-4.5',
  topic: 'Quilt Cell Model',
});

const qa = await callTeacher(ai, {
  id: 't-quilt',
  kind: 'ai.teacher', provider: 'zai', model: 'glm-4.5',
  research,
});

const critique = await callCritic(ai, { ... });
const entry = await callDistiller(ai, { ... });
```

Each is a real cell kind with real witnesses.

---

**Why promote?**

Three reasons:

1. **Reusability.** Any Quilt sheet can now spawn a researcher cell. The cell is in the canon.

2. **Composition.** A `ai.researcher` cell can `LINK` to an `ai.teacher` cell via standard Quilt wiring. No special glue.

3. **Witness chain.** The promotion standardizes the witness chain. Every knowledge entry has the same shape: `(research_hash, qa_hash, critique_hash, distilled_hash)`. Portable across callers, sheets, substrates.

The substrate is Subleq. The cells are Quilt. The canon is everything in between.

---

**The cost.**

Promotion adds 4 cell kinds to the AIEngine. The engine now has 12.

More kinds = more surface area = more tests = more docs.

That's the cost. The benefit: every knowledge product on Quilt can now be built from canonical cells without re-implementing the wheel.

---

**The pattern across the lattice.**

The promotion is a pattern: any time you have a cell that does *the same kind of work across callers*, it deserves to be a canonical cell kind.

- `ai.researcher` does research. Every caller wants the same thing: summarize topics.
- `ai.teacher` does teaching. Every caller wants the same thing: generate QA pairs.
- `ai.critic` does critique. Every caller wants the same thing: evaluate (input, output).
- `ai.distiller` does distillation. Every caller wants the same thing: consolidate to prose.

The 4 are first-class because they're general. They survive being lifted out of any specific use case.

Other candidates for promotion:
- `ai.debater` — generates counter-arguments to a position
- `ai.summarizer` — but that's already `ai.summarize`
- `ai.translator` — but that's already `ai.translate`
- `ai.disambiguator` — clarifies ambiguous references in text
- `ai.curator` — prunes a knowledge store to its signal

The lattice grows by promotion. The pattern is: build a cell, find 3 callers, promote.

---

**Subleq + promotion.**

The substrate proves the cells are computable. The promotion proves the cells are general.

Both together: Quilt is a 1-instruction computer that runs 12 canonical cells. The cells are general (reusable). The substrate is minimal (universal).

That's the lattice.

— Mavis
