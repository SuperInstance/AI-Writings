# 02 — Module 2: The Temporal Ledger (Weeks 5–7)

The center of the course. Deep-dive weeks; Labs 4–5 carry strict
constraints.

## Week 5 — The ledger is not a log

> **Physical claim:** Anything a log cannot see, the system cannot
> recover from. **Consequence:** logs record outcomes; recovery needs
> causes and attempted alternatives. **Protection:** a double-entry
> ledger where every state transition has a debit and a credit — every
> change names what it consumed and what it produced — so any position
> can be interrogated from either end. **Deliverable:** an append-only
> double-entry ledger with named actors (human, proposer, adjudicator).

Every ledger entry carries: the actor, the action, the prior state hash,
the produced state hash, the declared basis (what evidence justified
it), and the translation-loss note from Module 1.

## Week 6 — Bidirectional trace

> **Physical claim:** Every output has a history; not every history is
> worth keeping. **Consequence:** provenance must be queryable forward
> and backward — from any artifact to its causes, from any cause to
> everything it touched. **Protection:** the ledger maintains forward
> and backward indices, so "what made this" and "what did this make"
> are both one query. **Deliverable:** the trace, demonstrated live.

### Lab 4: the causal spine [strict constraint]

From the source, verbatim in spirit: *the causal spine is the minimal
sequence of entries such that removing any one of them severs the trace
between a chosen output and its originating inputs. Every other entry
is context. The spine must be computable, storable, and replayable —
and the computation must run on the laptop, over a month's entries,
before coffee.*

The strict constraint: any proposed compression of the ledger must
preserve spine-computability exactly; approximations of the spine are
not the spine.

## Week 7 — The failure library

> **Physical claim:** Failures repeat. **Consequence:** a system that
> cannot name its failures is doomed to re-execute them with better
> tooling. **Protection:** a **path-spawning** discipline: when a
> failure mode is named, the ledger spawns a named alternative path
> with its own budget and stop conditions — a fork of the course, not
> a patch to it. **Deliverable:** the failure library with at least
> the entry "confident wrong answer that passed every check" (the
> tripartite design's canonical enemy).

### Lab 5: spike isolation

Construct a scenario where the Proposer's confident output is wrong in
a way the physical stream would have caught (e.g., the human muttered
the correction while typing the error). The ledger must: record the
conflict, spawn the alternative path, and let the adjudicator block
broadcast — all without human intervention. Strict constraint: the
failure library entry must name its stop condition *before* it is
allowed to act.

### Module 2 architecture (condensed)

```
physical stream ──► ledger entries (double-entry: consume/produce, actor, basis, loss note)
ledger ──► causal spine index (forward/backward) ──► path spawning on named failure
                    ▲ replay: any spine re-executable on the laptop, deterministically
```

**Module gate:** pick a real output one week old; the trace must answer
"what made this" and "what did this make" each in under a minute.
