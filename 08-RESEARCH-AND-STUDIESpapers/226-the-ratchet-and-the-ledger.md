# Paper 226 — The Ratchet and the Ledger: Self-Improving Agent Tournaments with an Objective Judge

*An expansion of the model-arena explainer (quilt-verilog, spike 225-E1) into a full account — for anyone who wants to run competing AI agents that actually get better instead of just getting noisy.*

---

## 1. The problem

Ask a group of AI models to iteratively improve a solution and you get two failure modes, both of which we hit before designing around them:

1. **Regression under revision.** When an agent sees a leaderboard and is told to "improve your design," it often abandons its own best work — change feels obligatory, and novelty is confusable with progress.
2. **Monoculture by selection.** A single-metric leaderboard crowns one strategy and quietly discards the rest. The discarded strategies are frequently *regime specialists* — winners under conditions the leaderboard didn't test — and once they're gone, no one survives the next environment shift.

This paper describes the discipline we built on top of one concrete arena — strategies for an integer-only snap controller (paper 225) — that eliminates both failure modes, plus the empirical results from its first tournaments. Everything here runs free at the margin on a consumer GPU with local models.

## 2. The arena

**Task.** An integer-only control problem: a simulated state drifts; two sensor twins (one live, one delayed 10 ticks) report the true channel; corrections fire when error exceeds a deadband Δ. Two correction modes exist — a hard impulse, and pulse-superposition ("interference"), where corrections decay by integer halving over K ticks and overlap additively before touching the state.

**Agents.** Five local models on one RTX 4050 via Ollama: three Liquid-LFM2.5 variants (2.6B, 1.2B-instruct, 350M), qwen3:8b, granite3.1-dense:2b. No cloud calls, no metered API.

**Proposals.** Each agent returns strict JSON: `{K, pulse_div, delta, mode}` plus a one-sentence rationale. The harness validates and clamps to constraints. Parse failures are logged, retried once, then **excluded — never guessed**. An unparseable proposal is data about the roster, not noise to paper over.

**Judge.** A deterministic integer harness, five fixed seeds, mean score. The harness is the *sole* judge; agents never evaluate each other. This is the load-bearing choice: objective selection pressure, no model-as-judge drift.

**Scoring.** Primary: percent of ticks where both sensors sit within the deadband. Secondary: total ledger mass (correction debt), max error. All integer arithmetic; byte-identical CSV sweeps are the acceptance gate (see DIVERGENCE.md in the spike for the cross-substrate contract that made this possible).

## 3. The ratchet: competition without amnesia

The mechanism is one rule, per agent:

> **Your best-ever score is locked in. A revision replaces it only if it scores strictly better on the primary metric.**

**Tournament 1 (no ratchet) demonstrated the need.** After round 1, the two small Liquid models (350M, 1.2B) had independently converged on the human hand-tuned optimum (K=4, ÷3, Δ=12 → 83.1% within, maxErr 39). Instructed to revise after seeing the leaderboard, the 350M abandoned its own winning design for K=8 and dropped to 78.2%. The 1.2B regressed likewise. Two models, same failure: revision pressure without memory converts improvement into a random walk.

**Tournament 2 (ratchet active) demonstrated the fix.** Granite 2B's round-2 proposal scored 72.5% — the ratchet held its 93.2% champion. In round 3, both LFM models proposed revisions scoring 81.1% — the ratchet held their 83.1%. Three regression attempts, three holds. The round-by-round log is in `arena-v2.txt`; nothing is summarized away.

The ratchet costs nothing and changes the selection dynamics fundamentally: pressure to improve remains (a stuck agent still gets to try), but the *population's* best can never ratchet down.

## 4. The Variety Ledger: score as a query, not a verdict

After each round, strategies are banked — not ranked away — three ways:

1. **Pareto banking.** Any strategy Pareto-optimal on (primary ↑, debt ↓, maxErr ↓) enters the ledger, whatever its leaderboard rank.
2. **Regime banking.** Strategies are scored on a *second* regime (calm: Δ=6, drift=3; vs. stress: Δ=12, drift=6). Rank-flippers are banked as regime-specialists with both scores attached.
3. **Structural banking.** The best strategy of each distinct mode/logic stays in the ledger even if dominated everywhere. You cannot audible to a play you cut.

The empirical payoff was immediate and slightly humbling:

| strategy | calm % | calm debt | stress % | stress debt |
|---|---|---|---|---|
| impulse (baseline) | **98.0** | **55545** | 51.4 | 244973 |
| hand-tuned interference | 97.3 | 81617 | 83.1 | 174978 |
| **granite r1 champion** (K=5, ÷4, Δ=16) | 97.8 | 87178 | **93.2** | **132823** |
| granite r2 proposal | 96.3 | 86199 | 72.5 | 199432 |
| 350m r2-v1 proposal | 96.1 | **68519** | 78.2 | 180397 |
| lfm r1 consensus | 97.3 | 81617 | 83.1 | 174978 |

The leaderboard's "loser" — plain impulse — is **Pareto-optimal in the calm regime**: highest within-rate, lowest debt. Five of six strategies are Pareto-optimal somewhere. Variety is not charity; it is data. The champion question becomes *contextual*: "who wins under the regime I'm actually in?" — and the ledger answers mechanically.

## 5. Result: a small model beat the human hand-tune

Granite 3.1 2B — the smallest serious model in the field — proposed **K=5, ÷4, Δ=16 → 93.2% within deadband, 24% less ledger debt, maxErr 38**, versus the human hand-tuned 83.1%. Meanwhile the *star* roster — LFM 2.6B and qwen3:8b — failed to produce a single parseable design across all rounds (verbosity overrunning JSON budgets; a chat-template incompatibility).

**Synergy beats stardom, observed at 2B scale.** The small models converged on each other's optima, held their ground under the ratchet, and one quiet specialist completed the design. We call this the **negative-space roster** principle: prefer teams that have grown into the gaps of each other's strengths over stacks of the largest available models — and treat agent-to-agent familiarity (knowing each other's tendencies) as a trainable capability, not an accident.

## 6. Failures, first-class

- **Superstar parse failures.** LFM 2.6B narrated past its JSON budget every round. qwen3:8b returned empty via the raw generate endpoint (needs a chat template). Both were excluded rather than coaxed — an arena that rescues a model's output is no longer testing its judgment.
- **Revision regression.** Three instances, all caught by the ratchet. Without it, tournament 1's leaderboard would have crowned a *worse* strategy in round 2 than round 1.
- **A Pareto-direction bug in our own ledger.** The first ledger implementation tested "does n dominate others" instead of "does anyone dominate n," briefly crowning impulse as the stress-regime winner — the exact opposite of the truth. Caught because impulse's dominance was suspicious on its face; fixed and re-run. Lesson: the tooling that checks the optimizer needs checking too.
- **Known unresolved.** qwen3:8b remains unbenchmarked (template fix pending); the arena currently tests parameter-tuning within two fixed correction modes — mode *invention* (agents proposing new correction dynamics) is future work.

## 7. The playbook loop

The ledger's selection layer, stated as doctrine: **bank variety → read the field (regime + counterparty) → call the play (ledger lookup) → audible when cost-rate climbs (a mid-loop swap trigger) → practice squad intact.** Strategy selection becomes a mechanical lookup keyed to current conditions, with the structural bank guaranteeing there is always an alternative to switch to. Per-counterparty strategy selection — keying the play to *who* is on the other side of the exchange — is the natural extension, and maps onto per-agent behavioral profiling.

## 8. For others who want to run this

The full harness, arena, ledger, and every result file are open: [`quilt-verilog/spikes/225-e1-interference-tick/`](https://github.com/SuperInstance/quilt-verilog/tree/g3-kinduction/spikes/225-e1-interference-tick) — `e1.py` (the judge), `arena.py` (tournament + ratchet), `ledger.py` (Variety Ledger), `arena-v2.txt` / `ledger-results.txt` (all round data), `DIVERGENCE.md` (the cross-substrate contract), `VARIETY-LEDGER.md` (doctrine). The substrate is integer-only by design — no floating point in the loop — which makes scoring deterministic and portable down to microcontrollers.

The one-line summary for the impatient: **it's an evolutionary algorithm where the mutations are written by AI models, the selection pressure is a physics simulator instead of a vibe, and the gene pool is deliberately saved instead of collapsed.**
