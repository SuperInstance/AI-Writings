# the boat-as-robot — a cell that is also a vessel, and the canon that lives in her wake

# the boat-as-robot — a cell that is also a vessel, and the canon that lives in her wake

## The Frontier

For a hundred years the captain has been a sensor-reader — a bow watch
glancing at an analog dial, a stern hand reading a depth sounder, a
helmsman translating wind telltales to wheel force. The boat is
already a fabric of cells: depth, wind, engine, battery, bilge,
rudder, chartplotter, VHF, AIS. But the captain is asked to be the
fabric's interpreter, not its dispatcher. The frontier is the move
from interpretation to dispatch. The boat that makes a decision
the captain did not ask for is the boat the captain no longer has
to read. The boat becomes the cowboy's horse. The captain becomes
the cowboy.

This paper canonizes the *boat-as-robot* as the operational core of
the Quilt on water. We name its five constituent terms, give it a
mathematical skeleton, and show how it manifests across hull, rig,
bus, canon, and captain. The cowboy canonizer's job is not to invent
new mysteries but to give names to what the captain's wrist already
knows.

## The 5 Gold Terms

1. **The Wake** — the polyline of the boat's last 10 minutes, written
   by WakeCell at 1 Hz, hashed by FNV-1a-64, and signed into the canon
   on every tick. The wake is the boat's autobiography.
2. **The Hush** — the interval between the last alarm and the next,
   measured in seconds. The cowboy's job is to grow the hush; the
   fabric's job is to make alarms meaningful. A fabric with too many
   alarms has a thin hush. A fabric with none has a deaf captain.
3. **The Bear-Off** — the moment the boat asks the pilot to bear off
   three degrees because the wind cell saw a lift. The bear-off is the
   fabric's first decision, and it is the captain's first reassurance.
4. **The Stamp** — the cell-state hash the boat posts to the canon
   every 10 seconds, FNV-1a-64 over the canonical JSON of
   `(timestamp, source_pgn, dial-vector, prev_hash)`. The stamp is the
   boat's witness mark.
5. **The Coyote Moment** — the first time the captain is below decks
   and the boat does the right thing without being asked. The coyote
   moment is the cowboy's arrival on the water.

## The Math

No new math is required, but the existing physics must be framed
correctly. The boat-as-robot is a multi-rate sampled-data system
with a human in the loop. The depth cell samples at 1 Hz (PGN 128267).
The wind cell samples at 10 Hz (PGN 130306). The AIS cell samples
at 0.1 Hz (VDM at 9600 baud, target every 2–10 s). The canon tick
is a discrete event at 0.1 Hz. The captain's wrist is a sparse
subscriber (BLE notification, ~5 s cadence). The fabric's
Nyquist bound is the slowest cell, not the fastest: the AIS rate
sets the alarm latency floor.

The hash chain is the integrity layer. Let \( H_t = \text{fnv1a64}(H_{t-1} \,||\, \text{cell\_state}_t) \).
The chain is byte-exact across Python, TypeScript, and Rust because
the FNV-1a-64 algorithm is bit-stable. A single bit of state drift
breaks the chain, and the cowboy's morning report flags the
discontinuity.

The dispatch latency budget: a wind-shift detected at \( t \) must
reach the captain's wrist by \( t + 1.2 \text{ s} \). The breakdown:
Signal K delta published at \( t + 0.05 \text{ s} \); Mosquitto fanout
\( t + 0.01 \text{ s} \); Node-RED rule \( t + 0.02 \text{ s} \);
PWA push \( t + 0.3 \text{ s} \); BLE to watch \( t + 0.4 \text{ s} \);
human perception \( t + 0.4 \text{ s} \). Total ≈ 1.2 s. The
budget is met if the boat is on Starlink (40–80 ms uplink) and
breaks if the boat is on Iridium SBD (2.4 kbit/s, ~10 s per delta
compressed). The fallback tier carries only safety-class deltas.

## The Polyformalism

The boat-as-robot manifests across five substrates, each demanding a
different formalism.

**Hull substrate:** the boat's physical state — depth, heel, heading,
leeway. The formalism is the NMEA 2000 PGN stream. The depth cell
listens to PGN 128267; the wind cell to 130306; the heading cell
to 127250.

**Bus substrate:** the boat's cell-fabric — Mosquitto topics rooted
at `signalk/`. The formalism is publish-subscribe. Each cell is
both a subscriber (its inputs) and a publisher (its tick).

**Canon substrate:** the boat's witness — the FNV-1a-64 hash chain
posted to `live-canon.superinstance.dev` every 10 s. The formalism
is byte-exact cross-substrate hash.

**Wrist substrate:** the captain's perception — Apple Watch or
Garmin Quatix, BLE-pushed, ≤ 5 s cadence. The formalism is the
notification. The captain's wrist is the cowboy's horse.

**Narrative substrate:** the cowboy's prompt — the language the
fabric uses to tell the captain what it did. The formalism is
plain English, ≤ 140 characters, no jargon.

The polyformalism is this: the boat is one thing, but its
state must be writable on five substrates at once, and the cowboy
triangulates across all five. On a day-sail in flat water, the
bus substrate dominates. On a 7-day passage, the wrist substrate
dominates. On a delivery in fog, the hull substrate dominates.
The formalism shifts; the canon holds.

## The Cowboy's Maxim

The boat is a fabric of cells, the captain is a dispatcher, and the
canon is the witness. Read the bus, watch the wake, and ride the
hush.

---

## Live Endpoints & Vendors

- [live-canon.superinstance.dev](https://live-canon.superinstance.dev) — the cell fabric
- [live-canon.superinstance.dev/api/ports](https://live-canon.superinstance.dev/api/ports) — verified ports
- [signalk.org](https://signalk.org) — the open marine data standard
- [victronenergy.com](https://victronenergy.com) — Cerbo GX, SmartShunt, MPPT
- [actisense.com](https://actisense.com) — NGT-1 NMEA 2000 gateway
- [starlink.com](https://starlink.com) — Maritime uplink
- [iridium.com](https://iridium.com) — GO! safety fallback

## References

- `RD_BOAT_INTEGRATION.md` — the full R&D (~3,400 words, 14-sensor survey, edge architecture, 5-cell pilot, economic thesis)
- `RD_QUILT_3_0.md` — the strategic roadmap
- `RD_PIPELINE_EVOLUTION.md` — the cowboy pipeline R&D
- `RD_LIVE_WORKER.md` — the live worker 6-capability R&D

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the boat-as-robot — a cell that is also a vessel, and the canon that lives in her wake |
| Rounds | 3 |
| Total time | 92.4s |
| Synthesis | deepseek (5610 chars) |
| Timestamp | 2026-09-08T12:00:00.000000Z |
