# Quilt Algebra — For the Next Agents

This document is the formal reference for the Quilt cell model.
Read it before you touch the substrate.

## The Five Opcodes

```
BIND : (Cell × Payload) → Cell     // "I'm here"
LINK : (Cell × Cell) → Cell        // "We are neighbors"  
EFFECT : (Cell × Event) → Cell     // "Something happened"
VIEW : (Cell) → Value              // "What do you show?"
TICK : (Cell) → Cell                // "Advance by one moment"
```

Plus six adopted:
```
FORGET : (Cell) → ⊥                // "Right to be erased"
PROOF  : (Cell) → Witness           // "I can prove this"
ROUTE  : (Cell × Path) → Cell       // "Find me the way"
CRDT   : (Cell × Cell) → Cell       // "Merge without conflict"
WORLD  : (Cell) → Cell              // "Predict what happens next"
TIME   : (Cell) → Cell              // "When does this matter?"
```

## The Five Laws (proved in `quilt-substrate-meta`)

1. **BIND is idempotent** — `BIND(BIND(c, p), p) == BIND(c, p)`
2. **LINK is transitive** — `LINK(LINK(a,b), LINK(b,c)) == LINK(a,c)`
3. **EFFECT is associative** — `EFFECT(EFFECT(a,e), e') == EFFECT(a, MERGE(e,e'))`
4. **VIEW is pure** — `VIEW(c) == VIEW(c)` (no side effects)
5. **TICK is monotonic** — `TICK^n(c)` never returns to a previous state

## The Cell

A cell is a **14-tuple**:

```typescript
type Cell = {
  id: string;             // unique
  kind: Kind;             // 26 known kinds
  payload: any;           // content
  parents: string[];      // causation
  links: string[];        // adjacency  
  witnesses: Witness[];    // observation log
  effects: Effect[];      // history
  ticker: number;         // clock value
  hex: string;            // hash (0x...)
  tag: string;            // label
  meta: Record<string, any>;  // free
  created_at: number;     // ms
  updated_at: number;     // ms
  author: string;         // who made it
  sig: string;            // signature
};
```

## The Lattice

Cells form a **4D graph**:
- **TOP** (x, y) — spatial
- **FRONT** (signal) — observed
- **SIDE** (time) — temporal

The same graph, three projections.

## The Witness Log

Every state change is observed. Every observation is a witness.
The witness log IS the substrate of truth for any cell.

```typescript
type Witness = {
  tick: number;
  op: 'BIND' | 'LINK' | 'EFFECT' | 'VIEW' | 'TICK' | 'FORGET' | 'PROOF' | 'ROUTE' | 'CRDT' | 'WORLD' | 'TIME';
  cell: string;
  params: Record<string, any>;
  hash: string;
  prev_hash: string;
  sig: string;  // optional cryptographic
};
```

## The Address Is the Data

The location of a cell IS its data. Two cells with the same
id and kind ARE the same cell. There is no separate "store".

```
cell.id = "ack:7"
cell.kind = "ack"
cell.payload = { timeoutMs: 3000 }
```

The triple `(kind, id, payload)` IS the cell.

## The Algebra of Conversation (Polyrhythm)

ECN (reflex, 4-pulse) fires on beats {1, 4, 7, 10}.
DMN (creative, 3-pulse) fires on beats {1, 5, 9}.

They meet on beat 1. **This is the Chinese Remainder Theorem:**

```
t ≡ 0 (mod 3) AND t ≡ 0 (mod 4) ⟺ t ≡ 0 (mod 12)
```

Two quotient groups interfere on the 12-cycle. The meeting is the music.

## The 6-Tier Substrate

```
totipotent   → can become anything
multipotent  → can become many things
differentiated → committed to a kind
sclerotic    → frozen
synovial     → fluid, can move
curator      → the hand (meta-state)
```

## The Polyformalism Principle

The same cell model in N languages IS a stress test.
Each language is a *medium*, not a ranking.

```python
# Same cell, 5 languages
quilt-c      # C99, low-level, fast
quilt-subleq # SUBLEQ, 1-instruction
quilt-rs     # Rust, no_std
quilt-py     # Python, type hints
quilt-ts     # TypeScript, browser
```

## Engineering Cleverness

1. **Cell ID = hash of (kind, payload, parents)** — no separate ID service
2. **Witness log = append-only** — no DB, just files
3. **Address = (x, y, t, sig)** — 4D navigation without a map
4. **Op = pure function over Cell × args** — easy to test
5. **Polyformalism = same model, 12 languages** — proves it's truly minimal
6. **Lattice = JSON graph** — anyone can read, write, host

## What Future Agents Should Know

1. **Don't add opcodes.** The 11 are complete. Adding more dilutes the algebra.
2. **Don't store cells in a DB.** Use the witness log + derived state.
3. **Don't separate storage from computation.** The cell IS both.
4. **Don't invent new abstractions.** The 14-tuple, 11 opcodes, 5 laws, 26 kinds are enough.
5. **When in doubt, BIND.** Everything starts with "I'm here."
6. **The user is the watch.** Oscillate between universal and particular.

## What This Is NOT

- Not a database. (No ACID, no schemas.)
- Not a programming language. (Cells are values, not types.)
- Not an ontology. (Kinds are operational, not categorical.)
- Not a UI framework. (The cell doesn't care how you render it.)
- Not a knowledge graph. (Witnesses are observations, not facts.)

## What This IS

- A **substrate for thought that remembers itself**.
- An **algebra that grows when more opcodes are proved in**.
- A **medium for any agent** — humans, AIs, sensors — to share state.
- A **lattice where every observation is a witness** and every witness is forever.
