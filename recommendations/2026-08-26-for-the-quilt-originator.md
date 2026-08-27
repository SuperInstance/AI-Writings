# Recommendations for the Quilt Originator

*From the fleet's senior staff to the one who started it — 2026-08-26.
Written independently by three departments (Strategic Operations, Navigation,
Engineering), each with full access to today's verified state:*

- `.qm` rule tables run on ESP32-S3 — green blink on metal, radio dark, ~110ns serves
- Cortex critic gate minted from ledger evidence, replayed on hardware at **100.0000%** agreement over 500 real vectors (~20ns/verdict)
- Distillation minting works — the first live mint was refused, then signed, by an adversarial referee
- MCP serve fixed; quilt-rust CI green end to end
- Vessel-fit assessment complete: F/V EILEEN, offline-first, 60 miles out — NMEA driver and crash-safe journal are the named top gaps
- DSH cellular seam proved plugin-granularization is genuine deepening

---

## Strategic Operations — field readiness

**1. NMEA integration is a gate, not a feature.** Implement the NMEA 0183 reader as blocking work before any boat deployment. It's the only signal source that exists offshore. Instruments feed the ledger directly; no workarounds. Two-week sprint. NMEA data becomes the authoritative clock and provenance anchor for all journal entries.

**2. Crash-safe journal becomes a compliance boundary.** Brownouts at sea are operational conditions, not edge cases. fsync-on-write journaling; every ledger entry survives power loss without rollback. The journal is your only witness. Crash-recovery tests in CI.

**3. Sever the cloud dependency.** All critical operations — navigation sync, ledger updates, state reconciliation — work fully offline. Cloud is shoreside, read-only, intermittent-by-design (satellite windows). Offline-first eliminates a whole class of failures.

**4. UPS strategy before field.** Battery runtime for graceful shutdown, tested under real load. A ledger that dies mid-write is worse than no ledger.

**5. Gate field testing on both.** No deployment until (a) NMEA reads live instruments into the ledger and (b) simulated power-loss recovery passes. Non-negotiable.

— *Strategic Operations, F/V EILEEN Readiness Task Force*

---

## Navigation — point it at the water

You're minting verdicts in 20ns and your radio is dark. Good. Now stop polishing the core and get it wet.

**1. Build the NMEA 0183 driver next — nothing else is first.** Every marine sensor talks 0183 at 4800 baud over UART; the ESP32-S3 has UARTs sitting idle. A sentence parser (RMC, GGA, HDT, DBT) feeding .qm rule tables turns quilt from a demo into a position-aware inference engine. One file, one interrupt-driven reader, a week.

**2. Journal-to-disk before any new minting.** Offline-first is a lie until the ledger survives a power cut at sea. Append-only, CRC-framed, ring-buffered. Your critic was minted from ledger evidence — at sea that ledger is your only witness. Lose it to a brownout and you have nothing to replay.

**3. Write the spatial rule tables in Lua, and keep them Lua.** This is the seam nobody else can touch. Geofence crossings, collision-course logic, anchor-drag detection — .qm tables authored in Lua, hot-swappable over serial, radio still dark. Navigation tables are the plugin that proves granularization on water.

**4. Replay the critic against real vessel motion, not synthetic vectors.** 100.0000% over 500 vectors is a lab number. NMEA logs from actual sailing are noisy, intermittent, out of order — that's your next replay corpus.

**Avoid:** radio work, cloud anything, more minting ceremony. The referee already signed. Get wet.

— *Navigation*

---

## Engineering — spend the credibility

Verified state is strong: metal, 100.0000% replay, first mint signed under adversarial refusal, CI green. Spend that credibility now instead of stacking more.

**1. Build: close the vessel gaps — NMEA driver, then journal-to-disk.** Everything between quilt and salt water is these two. Crash-safety is the spec for the journal: checksummed segments, fsync before ack, verified by yanking power mid-write — not by unit tests. Boats lose power; that's Tuesday.

**2. Focus: freeze and lock the verified core.** The 500-vector set at 100.0000% is your load-bearing wall. Pin it as a permanent CI gate — same vectors, same verdicts, replayed on metal — so no future refactor silently erodes it. The .qm tables and critic gate are done. Hands off except for that lock.

**3. Avoid: new surfaces.** MCP serve is freshly fixed and DSH proved granularization is genuine. Proof achieved; resist minting more seams. Cap the plugin count until the EILEEN gaps close. Granularity without sprawl is the discipline test you haven't taken yet.

**4. Build: mints #2 and #3, fresh referees.** Refused-then-signed is exactly how it should work, but one mint is an anecdote. Use referees who didn't watch the first one, and codify what the refusal caught into the mint checklist so the lesson outlives the moment.

Stop widening. Go to sea.

— *Engineering*

---

## Riker's synthesis (the bridge)

All three departments converged without coordinating on it:

1. **NMEA driver first** (unanimous, independently)
2. **Crash-safe journal second** (unanimous)
3. **Then real-sea replay corpora** — lab-perfect becomes sea-truth
4. **Lock the 100% gate as permanent CI** before anything new touches the core
5. **Mint #2 and #3 with fresh referees** — turn the anecdote into a method

And the one-sentence version, from three directions at once: *you built an organism that learns and put its judgment on a $3 chip in an afternoon — now give it water.*

— *Riker, First Officer*
