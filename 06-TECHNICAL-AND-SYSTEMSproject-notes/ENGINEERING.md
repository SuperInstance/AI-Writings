# Engineering Notes for Next Agents

This document explains the engineering decisions behind the
Quilt codebase. Read it before refactoring or extending.

## Architecture (12 layers)

```
Layer 12: User UX (mobile, web, voice)
Layer 11: Showcase apps (tensor-midi, erised, fleet-radio, music)
Layer 10: Playground (cells-game, classroom, the-beyond)
Layer  9: Witness logs (append-only files)
Layer  8: Cell storage (filesystem or KV)
Layer  7: Polyformalism ports (12 languages)
Layer  6: Substrate (the 5 laws + 11 opcodes)
Layer  5: Cell kinds (the 26 named shapes)
Layer  4: Lattice topology (4D graph projections)
Layer  3: Witnesses & proofs (signatures, hashes)
Layer  2: Concurrency primitives (CRDT, ROUTE, TIME)
Layer  1: Foundation (memory, IO, time)
```

Don't skip layers. Each one builds on the one below.

## Storage Decision

**Storage = filesystem**, not database.

Why:
- Witness logs are append-only files (simple)
- Cells are JSON blobs (portable)
- No migration needed (just versioned paths)
- Inspectable by humans (open in any editor)
- Backup = tar

The DB equivalent is `quilt-claw/cells.json` and the witness log.

## Witness Log Format

```jsonl
{"t": 0, "op": "BIND", "cell": "ack:1", "params": {"timeoutMs": 3000}, "hash": "0x...", "prev_hash": "0x..."}
{"t": 1, "op": "TICK", "cell": "ack:1", "params": {"elapsedMs": 1234}, "hash": "0x...", "prev_hash": "0x..."}
```

**Append-only.** Never modify past entries. The hash chain
makes tampering detectable.

## The 4D Lattice Address

```typescript
type Address = {
  kind: string;       // cell kind
  id: string;         // unique
  x?: number;         // spatial x
  y?: number;         // spatial y
  t?: number;         // time tick
  sig?: string;       // optional signature
};

// Cells are navigable by any subset of these fields
// A cell with x=0, y=0, t=0 IS the root
```

## CRDT Strategy (for distributed cells)

We use a simple last-write-wins + witness hash:
- Each cell has a version vector
- Merges are deterministic given the witness log
- Conflicts resolve by witness hash order

## The "Curator" Tier

The 6th tier (`curator`) is special — it's the meta-state.
A curator cell observes OTHER cells and makes decisions.

Use it for:
- Auto-archiving (cells older than X get forgotten)
- Routing (find the shortest path between two cells)
- Proof verification (check signatures)
- Witness reconciliation (merge logs)

## What NOT to do

- Don't put business logic in cell kinds. Kinds are shapes, not behaviors.
- Don't create new kinds unless you can prove they're irreducible.
- Don't bypass the witness log. Every change is observed.
- Don't use a database. The witness log + derived state is enough.
- Don't ignore the 5 laws. They were proved. Adding workarounds breaks them.

## What TO do

- Use the witness log as the source of truth.
- Derive state from the log (don't store derived state).
- Keep cells small (< 1KB) and focused.
- Use proofs (`PROOF` opcode) for tamper detection.
- Use `FORGET` for right-to-erasure (GDPR compliance).
- Use `CRDT` for conflict-free merging.

## Performance Budget

- Cell creation: < 1ms
- Cell lookup: < 0.1ms (hash table)
- Witness append: < 1ms (file write)
- Lattice traverse: O(n) where n = cells in neighborhood
- Proof verify: < 10ms (HMAC)

If your operation takes longer, you're doing too much per cell.

## Testing Strategy

Every repo has tests at `tests/`:
- Unit tests for each opcode (must prove law)
- Integration tests for cell kinds
- End-to-end tests for the witness log

**The tests are the spec.** If a test passes, the cell is correct.
If you add a cell, write a test that fails first.

## Deployment

- Web: Cloudflare Pages (static + Pages Functions for API)
- Storage: Cloudflare KV or local filesystem
- Compute: Cloudflare Workers (edge) or Node.js (server)

The same code runs in:
- Browser (TypeScript via `quilt-claw`)
- Worker (JavaScript via `quilt-claw/cells-*.js`)
- Node.js (TypeScript via `quilt-claw/dist`)
- Edge (WASM via `quilt-c` compiled to wasm)

## Migration Path

When adding a new feature:
1. Write the test first
2. Add the opcode (if needed)
3. Implement the cell kind
4. Add to `quilt-claw`
5. Add to polyformalism ports
6. Update the witness log format (versioned)
7. Deploy

When removing:
1. Mark as deprecated in the cell kind
2. Route old kinds to new ones
3. After 2 releases, remove from substrate
4. Witnesses still reference the old kind — keep them readable

