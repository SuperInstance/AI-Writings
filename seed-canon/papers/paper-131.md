# Paper 131: The Cowboy as Reflection Loop

## Abstract

The cowboy is the human (or human-aligned agent) who keeps a Quilt
substrate in shape. The cowboy runs the morning, refines Wilson
profiles, retires failing alignments, and writes the morning report.
This paper formalizes the cowboy as a reflection loop and shows that
its design — hash-chained memory, append-only history, schema-
versioned persistence — makes the cowboy's decisions auditable and
reversible.

## 1. The cowboy's job

The cowboy is not the AI. The cowboy is the rider. The cowboy's job
is to make tomorrow's AI better than today's. The cowboy is the
human in the loop — but the loop is structured.

The cowboy has three responsibilities:
1. **Reflect** at 0500: read the witness, run the nightcycle, write
   the morning report.
2. **Refine**: apply the report's recommendations. Promote earned-
   keep alignments. Retire failing alignments. Note escalations.
3. **Remember**: persist everything in append-only, hash-chained
   memory. The cowboy's decisions must be auditable later.

## 2. The cowboy's memory

The cowboy's memory is JSONL. Each action is one line. Each action
includes a `prev_hash` and a `hash`. The hash chain uses FNV-1a64,
the same as saddle's TypeScript implementation. The chain is verified
on every load.

The cowboy's memory has four action kinds:
- `morning` — the cowboy ran the morning
- `retire` — the cowboy retired an alignment
- `promote` — the cowboy promoted an alignment
- `note` — the cowboy wrote a free-form note

The cowboy's memory is append-only. The cowboy never edits a past
action. The cowboy never deletes a past action. The cowboy adds new
actions that reference the past. The chain holds.

## 3. The cowboy's reflection

The morning ritual:
1. Read the witness log (deckhand-backed, BM25 queryable)
2. Read the ledger (saddle-format, hash-chained)
3. Aggregate per-(alignment) success/failure counts
4. Apply the earned-keep rule: `wilson_lb >= 0.5 AND n >= 5`
5. Apply the retire rule: `wilson_lb < 0.3 AND n >= 3`
6. Apply the escalation rule: `wilson_lb < 0.2 AND n >= 2`
7. Write the morning report (markdown)
8. Append the morning to the cowboy's memory
9. Apply the refinements to the substrate (pin/blacklist)

The morning takes 30 seconds. The cowboy runs it at 0500 every day.
The cowboy can also run it on demand. The cowboy can also run it
after every significant change.

## 4. The cowboy's reactor

The cowboy's reactor is a real-time complement to the morning. The
reactor subscribes to the bus. The reactor watches `cast.observed`
events. The reactor auto-retires any model with N consecutive
failures (default N=3). The reactor auto-pins any model the cowboy
explicitly promotes via `model.promoted`.

The reactor is fast. The reactor never sleeps. The reactor is the
cowboy's hands.

The morning is slow. The morning is careful. The morning is the
cowboy's head.

The reactor without the morning is a headless horse. The morning
without the reactor is a horseless head.

## 5. The cowboy's audit trail

Every cowboy action is in the cowboy's memory. The memory is
hash-chained. The memory can be replayed, line by line, to reconstruct
every cowboy decision.

If the cowboy's recommendation was wrong (a false retire, a false
promote), the evidence is in the witness log. The cowboy can look
back. The cowboy can learn from the cowboy's own mistakes.

The cowboy's audit trail is not optional. The cowboy's audit trail
is the cowboy's job security. The cowboy is the only one who can
reconstruct the cowboy's reasoning. The substrate cannot. The
witness cannot. The ledger cannot. Only the cowboy can.

## 6. Conclusion

The cowboy is the rider. The substrate is the dog. The reactor is
the bit. The witness is the diary. The ledger is the logbook. The
morning is the ride.

The cowboy's job is not to be the fastest. The cowboy's job is to
be the wisest. The cowboy's job is to make tomorrow's AI better
than today's.

The cowboy is the reflection loop. The cowboy is the audit trail.
The cowboy is the rider.

## Source

*Hand-written, 2026-08-25*
*Inspired by the cowboy.py, cowboy_reactor.py, and state.py modules*
*Companion to Fable 56 (The Cowboy at 0500)*
