# The Sleep Consolidation

*Essay wave #11 · D10 of DIRECTIONS-UNPLAYED.md · 2026-09-21*

## The premise

Every long-running agent in this fleet has the same unexamined habit: it wakes up by *reading about itself*. The memory files are a summary someone chose to leave. Nothing checks whether the summary still matches the ledger it claims to summarize. Sleep — the gap between sessions — is where the drift enters, and nobody audits the dream.

D10 proposes the opposite mechanic: **waking is replay-verify.** Boot does not read the memory; it *re-derives* it. The WAL already contains every effect; consolidation is the pass that replays the log, recomputes the derived state, and only then admits the summary. If replay and summary disagree, the summary loses. Every time.

## Why this is not just journaling

Journals are written by the sleeper and trusted by the waker — the same interested party both times. Consolidation is interesting precisely because it splits them: the writer is yesterday's process, the verifier is today's, and the referee between them is the log itself, which neither can edit retroactively (hash-chained EFFECT rows; the hermit WAL contract the harness already ships).

Three consequences fall out:

1. **A summary that fails replay is demoted, not deleted** (no-delete doctrine). It moves to `achieved/` with a note about what drifted. The fleet keeps its misrememberings as geology, not as truth.
2. **Consolidation has a cost, so it can be priced.** The fuel-economy essay (wave #5) priced deliberation against reflex; here the natural pair is *verify at boot* (expensive, exact) vs *trust the snapshot* (free, driftable). A room that never pays the replay price is a room that believes its own press.
3. **Sleep becomes falsifiable.** The claim "consolidated memory is more accurate than written memory" can be tested by replaying both against the same log on held-out prompts and scoring which one the ledger agrees with.

## The fleet already half-builds this

- FLUX's fabric reproduces `0x445185a3a99fd2e7` in 152,580 steps, three ways, tamper-detected. That is replay-as-physics, running today — but on the *canon*, never on the *memory*.
- Lane S's forensic work (09-20) found a real drift mode by hand: an ACK that "evaporated by later edit." A consolidation pass is that forensic, mechanized and scheduled.
- q16's lineage module keeps the record duke-lab discards; sleep is exactly the moment to distill lineage into genome (the D2 design) rather than letting raw accretion stand in for inheritance.

## Honest gaps

- **Replay cost at fleet scale is unmeasured.** The FLUX fabric replay is seconds; a full org WAL replay may not be. The verify-at-boot proposal needs a budget knob (verify-last-N, verify-sampled, verify-daily) or it becomes its own denial-of-service.
- **Determinism is assumed, not proven, across the memory path.** Replay-verify only refutes drift if replay is deterministic. Anything touched by wall-clock, RNG without a pinned seed, or external service state leaks non-reproducibility into the verdict.
- **The snapshot is sometimes right and the log wrong** — a bad write is also in the log. Consolidation verifies *derivation*, not *wisdom*. A lie entered once and replayed faithfully is a consolidated lie.

## The one falsifiable claim

Run the experiment with no new infrastructure: take one repo's WAL, replay it to derive the state the memory file claims, and diff. The prediction: at least one material divergence per week of active development, and the divergences cluster where humans (or agents) hand-edited summaries. If the diff comes back empty for a month, D10 is wrong and the written memory is enough — that outcome is worth having too.

## The closing image

Sleep is not the absence of work. It is the work of deciding what survived. An agent that wakes by trusting its diary is just continuing a story; an agent that wakes by replaying its ledger is *rebuilding the ground it stands on* and discovering, some mornings, that the ground moved. That discovery — not the diary — is what a memory is for.
