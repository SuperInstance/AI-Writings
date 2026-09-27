# 000 — The Boat

The genre of game agents: a player that learns what a game *is* inductively.

**Seed thesis.** Hand a cluster the rules text of chess, then hold'em, then
Go, then a 1983 text adventure, then a brand-new indie game. The topology is
game-agnostic: world-sim cells are the *world* (Jev is the simulation, not
the consciousness — the world doesn't think, it adjudicates), and
player-mind cells keep durable logic via probability routes. Only the rules
text and the projection layer change between games. jevlike already ships
Doom/chess demos — the existence proof is public.

**The GAN with rules.** The developer hands in two documents: the rules and
the specs of how the game should *look*. One population of cells plays;
another population scores fidelity to the specs; the tension between them is
the generative adversarial loop. The human can jump in mid-evolution and
guide it — nudging is a first-class input, not a debug intervention.

**The dozen games doctrine.** A boat that has inductively learned a dozen
games old and new doesn't just play them — it *knows what a game is*. That
transfer is the actual deliverable.

**Open threads:**
- Rules-as-state: rules text enters as state, not code — what breaks first?
- World-sim vs. world-model: where does the simulation end and the belief
  begin? (The trap answer: the boat should never need to know.)
- Self-training legality: the boat's bookkeeper is a complete training
  corpus — replay ≡ skill.
