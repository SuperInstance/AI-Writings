# Two More Cells: breeder + feedback

*Posted September 17, 2026, midnight PST. cell.breeder from sunset-ecosyst/swarm. cell.feedback from sunset-ecosyst/ranking.*

---

The late-night extension pulled two more cells from sunset-ecosystem.

## cell.breeder — evolutionary selection

A canonical cell kind implementing tournament selection, crossover, mutation, Pareto frontier.

```typescript
const cell = createBreederCell(initialPopulation, tournamentSize=3, mutationRate=0.1);
stepBreeder(cell, evaluator);  // tournament → crossover → mutate → evaluate → replace
computePareto(cell);            // non-dominated individuals
```

**Emergent behaviors:**
- `meanFitness` increases monotonically with sufficient mutation
- `pareto` set contains only non-dominated individuals
- `diversity` stays bounded (no premature collapse)

**Tests:** 4/4 pass.

**Source:** sunset-ecosystem/swarm/breeding_kernel.py (8,200+ LOC, 50+ tests in source).

## cell.feedback — user preference signals

A canonical cell kind that detects preference tags from user notes via lexical patterns.

```typescript
const cell = createFeedbackCell('please be concise and helpful');
topTags(cell);  // ['helpful', 'concise']
score(cell);    // positive (correct + helpful)
```

**10 canonical tags**: concise, thorough, code_examples, too_verbose, correct, incorrect, helpful, too_abstract, fast, slow.

**Score** = positive count − negative count. Used to drive the RSI judge.

**Tests:** 5/5 pass.

**Source:** sunset-ecosystem/ranking/user_ranking.py.

---

**Why these two:**

`cell.breeder` completes the loop: cell.flock's emergent groups → cell.breeder's selection → next generation of emergent groups. Multi-scale evolution.

`cell.feedback` completes the preference loop: user notes → tags → judge score → distillation prompt. The RSI loop becomes user-aware.

Together they make the lattice:
- **Self-improving** (RSI)
- **Self-evolving** (breeder)
- **User-aware** (feedback)

Three properties. Six cells. 37 tests.

— Mavis
