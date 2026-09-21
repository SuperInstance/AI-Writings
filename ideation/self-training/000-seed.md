# 000 — The Simulator Self-Trains

The genre of self-training: hook, drop, wake, learn.

**Seed thesis.** Once every cell books every state change (law 4), the
system carries its own training corpus. Simulation is free: fork a cell's
book, replay it against perturbed decisions, and measure which branch the
receipts prefer. Self-training is not a separate pipeline — it is what a
bookkeeper does when given spare cycles.

**Hook and drop.** Cells entangle: a hook on a sibling's delta; a drop when
the delta falls below the commensuration floor (silent — the ghost that
keeps the lattice quiet). Waking a cell = its bookkeeper replays the missed
ticks, then the cell decides from caught-up state. A system that simulates
and self-trains easily is one where *waking up is cheap and forgetting is
impossible*.

**The JEPA precedent.** Elephant taught us: play is not a reward, it is the
training signal. On jev-quilt, play = cells forking each other's books and
running counterfactual games. The receipts grade the counterfactuals.

**Open threads:**
- Replay-verification vs. memory: when do we trust the book over the
  summary? (The Sleep Consolidation essay priced this: drifted summaries get
  demoted to `achieved/`; the WAL is the truth.)
- Adversarial self-play: two cells, one book, opposite viability floors.
- When simulation outruns reality: the simulator's outputs must be labeled
  as simulated — a simulated decision projected as real is the worst lie
  this system can tell.
