# Champion Gossip — cross-model critic upgrade for the Red Queen

Design v0. Extends docs/NEGATIVE-SPACE-GAN.md (the generator/critic pair) with the
heterogeneous-champion mechanism: instead of one critic judging every candidate,
an archipelago of value-disjoint critics, each championing different cells of the
MAP-Elites archive, gossiping about each other's champions asynchronously.

Reference: DEI async champion-gossip (heterogeneous-LLM MAP-Elites, arXiv
2605.27130) surfaced by edge-watch 2026-09-21 as the cross-model Red Queen
upgrade for the-tap PR #6 (candor critic × MMX-cli, Casey's MiniMax-M3 critic).

## Why gossip at all

The negative-space GAN's known failure mode is critic collapse: a single critic,
however value-disjoint, converges on its own aesthetic, and the generator farms
it. Rotation (K≥2) slows this but does not prevent it — the critic queue is
static, the generator can learn the rotation schedule.

Champion gossip changes the topology: critics never see raw candidates directly.
They see *champions* — the current occupant of each archive cell — forwarded by
other critics, with that critic's reasons attached. A critic scoring a champion
it did not select measures something closer to inter-rater reliability than to
optimization pressure. The generator is no longer playing one judge; it is
playing the disagreement between judges.

## The archipelago for the-tap

Three islands, each value-disjoint from the writer (per NEGATIVE-SPACE-GAN's
rule: shared values, no shared expertise):

1. **candor** — Frenet-torsion strain lines, first-person maker claims,
   evidenced-vs-asserted texture. Sees *form and honesty of construction*.
2. **MMX-cli (MiniMax-M3)** — Casey's cross-model critic. Sees *argument
   structure, novelty against its own training distribution*. Embodied via
   the existing CLI seam, not an API dependency.
3. **hermit ledger** — not an LLM; the cheapest island. The values ledger's
   monotonic entries score *grounding*: does the candidate cite real turns?
   A deterministic critic breaks LLM-correlated blind spots by construction.

Gossip channel: async, batched. Every N rounds, each island receives M champions
from cells it does not occupy (cheapest selection: uniform over non-owned
cells), each wrapped as `{champion, owner, owner_reasons, cell_coordinates}`.
The receiving critic returns `{keep | displace, reasons}` — displace only if it
would champion the candidate for that cell itself.

## Anti-collapse trio (multiplicative, not additive)

- **Ownership floor**: a critic's displacement of another's champion must
  survive the viability floor (ethos ∈ {0,1} per NEGATIVE-SPACE-GAN). Zero
  ethos still sunsets, regardless of gossip prestige.
- **No self-reinforcement**: a critic may never receive back a champion whose
  lineage passed through its own displace decision (lineage.jsonl trace).
- **Held-out cell set**: 20% of archive cells are gossip-invisible; final
  viability is judged there. Champions built by farming the gossip channel
  must still survive judges that never saw the gossip.

## Async honesty

Gossip is asynchronous *inside* the mechanism, not a latency excuse for the
wrapper: a round ends when all islands answered or a wall-clock bound passed;
missed islands count as abstain, never as approve. An island that abstains
three rounds running loses ownership of its cells for one round (cells revert
to vacancy, not to the previous champion — dormancy is not costume).

## Acceptance sketch (5 tests)

1. **Displace-is-earned**: a champion engineered to flatter island A's known
   vocabulary is displaced by island B when B's held-out read fails it.
2. **No-echo**: lineage trace proves no critic judges a champion carrying its
   own displace decisions; test constructs a 3-hop chain attempting the loop.
3. **Abstain-is-not-approve**: with one island stalled, round closes on time,
   stalled island's cells vacate, suite records abstain.
4. **Held-out survival**: candidate farmed through gossip-only praise is
   rejected at the held-out cell set; candidate surviving honest disagreement
   passes.
5. **Floor tripwire**: a gossip-beloved candidate with ethos 0 sunsets, and
   the sunset cites the viability floor, not gossip standing.

## Honest gaps

- Three islands is the minimum for disagreement topology; whether two LLM
  islands + one deterministic island counts as "heterogeneous" by the DEI
  result's own definition is unverified — the paper's population was LLMs.
- Gossip about *reasons* leaks stylistic fingerprints between islands; over
  rounds the archipelago may converge culturally anyway. No drift meter yet.
- MMX-cli invocation cost per round is unpriced; under the fuel economy (D5)
  this mechanism is deliberation, not reflex, and Casey-hours are the scarce
  currency.
- Requires the-tap PR #6 (Red Queen) merged as the archive substrate; this doc
  is the design ahead of the seam, same relation as D2's design to the commune.
