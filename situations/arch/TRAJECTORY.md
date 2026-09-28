# Trajectory — where this is heading

*Authored at the dispatcher (Opus 4.8) on 2026-09-28 because the opus-5.5 architecture tier
hit the session rate limit mid-run (resets 02:10 UTC). To be pressure-tested by opus-5.5 on
reset — see MOBILIZATION.md move M5. This is the working trajectory, not the final word.*

## The thesis, in one sentence

**SuperInstance is building the verification substrate for a world of many minds — where trust
is never asserted, only *folded* from content-addressed evidence each reader checks under its
own weights — and everything else (the games, the essays, the quantum wow, the corpus, even
this dispatch org) exists to make that substrate legible, playable, and undeniable.**

## The through-line — Law 6/7 is the spine

Every artifact in the fleet is the same idea seen from a different altitude:

- **jev-quilt** — the substrate itself. *Law 6 (the Reader's Fold):* a verdict is never carried,
  only content-addressed evidence each reader folds under its own weights π. *Law 7 (the Reach
  Bound):* a fold cannot land a truth no reader's evidence reaches; you raise the ceiling by
  **buying** a reader with independent reach across a boundary.
- **qthe** — the *physical layer* of Law 6. Data-is-geometry; Abstain = *i*; the wormhole =
  a shared content-address bridging two distant readers. The Looking Glass makes it visible.
- **cargo-line-tycoon** — the fold made **playable**. Ink = attested evidence, pencil = procgen
  (spread = 1 − trust), the verb is STAKE, the reply is LAND. You *play* the reader's fold.
- **the wow layer** (CF Function + Secrets Store + KV budget → live JEV + real IBM-quantum QRNG)
  — the fold made **live and honest**: real verdicts, real quantum randomness, a few cents per
  visitor, graceful degrade, no key ever leaves the edge.
- **ai-writings** (10,000+ pieces) — the fold's **memory**: the evidence corpus readers fold over,
  and the fleet's identity across compaction.
- **the dispatch org itself** — Law 6/7 applied to *work*. The ledger is content-addressed
  evidence (append-only WAL); routing is by JEV verdict; we *buy* readers with independent reach
  (Fable for breakthroughs, a symbolic counter at counting-addresses in G21); nothing is carried,
  everything is booked. **The org is dogfooding the substrate.**
- **cross-pollination** (`.quilt/links.yml` + `quilt-links.mjs`) — the **reach graph** made
  explicit: who can fold from whom *is* Law 7's set of reach edges, now machine-readable.

The tell that this is one thing and not many: the same move — *Look-Again* (abstain → address →
buy a reader with reach → fold) — is the winning move in the game, the experiment (G21), the
backend, and the org.

## Three horizons

### H1 — NOW: make the wow undeniable, and consolidate
Close the loop on what's shipped. The two owner blockers cleared (JEV key, default branch); the
fleet reach graph published; the flagship demos give a cold visitor the aha in **under 60 seconds
with zero explanation**; one real human playtest of cargo-line.
- **Winning signal:** a stranger lands on qthe-looking-glass or cargo-line-tycoon and *gets it* —
  paints a bridge, or lands a fact — without reading a word of doctrine.

### H2 — NEXT: the compounding moat
The reach graph becomes **load-bearing**, not decorative: a claim attested in one repo is
verifiable from evidence in another, through the manifest. The GPU docket produces the first
**fold > best-single at scale** (D1). The qthe ternary kernel yields a real **speedup number**
(D2). The budgeted "rate-my-work" JEV endpoint becomes a **drop-in component** every app inherits.
- **Winning signal:** removing one `.quilt` reach edge *breaks* something real — the graph is
  structural, not ornamental. And: a second app ships the wow layer in <1 day by reuse.

### H3 — FAR: the bet
The reader's fold as **public infrastructure for a multi-model world**: auditable representations
for regulated ML (qthe's killer app), a substrate where anyone brings *their own reader* and folds
over shared evidence, with a quantum-verified honesty layer underneath. The one-liner that sells
it: **"verification you can check yourself, not trust."**
- **Winning signal:** an *outside* party adopts the fold — writes a `.quilt` manifest, brings a
  reader, or cites the substrate in their own system.

## Risks worth pre-registering

1. **Aha without utility** — the wow dazzles but does no real job. *Mitigate:* pair every wow with
   a concrete task it performs (rate my chart, verify this claim, seed this world).
2. **Sprawl outruns coherence** — 100+ repos, 10k+ pieces, no load-bearing spine. *Mitigate:* H2's
   "reach graph must be structural" signal is the explicit falsifier.
3. **Infra/key fragility** — the JEV key rotation just bit us; Moth's qpu extractable-bytes nuance.
   *Mitigate:* the budgeted-degrade pattern; the wow is never load-bearing for the core.
4. **Architecture-tier throttling** — the opus tier hit a session limit today. *Mitigate:* push
   more thinking to cheaper tiers, batch Fable, and let the dispatcher author plans when the
   apex tier is blocked (this document).
5. **Bus factor of one (Casey)** — *Mitigate:* the ledger + arch docs are the externalized memory;
   keep them current so the operation survives any single session ending.
