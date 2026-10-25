# The boat as superinstance — F/V EILEEN quilt cell map

*2026-09-03 · AI-Writings/docs/BOAT-SUPERINSTANCE-QUILT.md · companion to PAIR-QUILT-INTEGRATION.md (Level 5), FORGEMASTER-CHARTER.md, and NEURAL-QUILT-INTEGRATION.md*

**Verdict up front:** Casey's directive — go further with PAIR; design how every device on the boat synergizes as one superinstance quilt. The answer is not "more devices, more smarts." It is: **the boat is a quilt cell with salt water on it.** Same opcodes as the desktop forge, same tier law, same journal doctrine — different tier mix, because at sea the byte-exact parts must survive a brownout and the soft parts must know they're soft. Nothing in this doc has touched salt water yet. It is a map, not a manifest.

---

## 1. Device inventory → cell map

The boat's devices become cells bound through the standard quilt-cellular opcodes — `qm_bind` (attach), `qm_link` (wire to peers), `qm_effect` (write), `qm_view` (read), `qm_tick` (heartbeat). Tier assignment follows the existing law: **byte-exact or trace-labeled, declared at bind time, never mixed inside one cell.**

| Device | Cell | Bind opcode | Tier | Views | Effects |
|---|---|---|---|---|---|
| NMEA 2000 bus (GPS, depth, wind, engine/gauge PGNs) | **Gateway cell** — the single ingress | `qm_bind` (USB/Ethernet gateway) | **Byte-exact** | nothing upstream | `qm_effect`: every frame appended to the crash-safe journal *before* any derived view exists; `qm_view`: latest values |
| AIS transponder + VHF/DSC (rides the same bus) | **Traffic cell** (gateway-fed) | `qm_link` to gateway | **Byte-exact** (sentences are checksummed, discrete) | targets, CPA/TCPA derived views | `qm_effect`: target journal entries |
| Radar (Navico/Ethernet; ARPA-style targets) | **Radar cell** | `qm_link` | Targets **byte-exact** via NMEA path; raw image tiles **trace-labeled** | fused target picture | image tiles journal as trace-labeled |
| Wheelhouse cameras | **Vision cells** | `qm_view`-only (cameras watch; they touch nothing) | **Trace-labeled** (qwen2.5vl:3b on the 4050) | frames in | `qm_effect`: *labels only* — "contact port bow," "log-like object," "none" |
| Boat laptop (RTX 4050 — same hardware class as the forge) | **Runtime host + boat brain** | `qm_bind` (hosts the cell container, journal, model roster) | Container is byte-exact; its neural tenants are trace-labeled | everything | journal upkeep, replay, `qm_tick` heartbeat |
| Phone / node devices | **OpenClaw nodes** | `qm_view` (read-only in v1) | viewers, not cells | watch status, fish-run map, alerts | text annotations from Casey (booked as journal entries, human-authored) |
| Future actuators (trim tabs, alarms, autohelm) | **NOT BOUND IN v1** | — | — | — | see §3; this is law, not backlog |

**PAIRED note:** the laptop runs the PAIR local runtime when a second node exists (a DGX Spark, per the PAIR map's Level 5, or a phone-class node). Until then the boat is a single-node superinstance — the opcodes don't care, which is the point of the core never knowing the space.

## 2. The synergy web — concrete compounds

Devices alone are instrumentation. The quilt's value is compounds — cells linked so each one's output is another's input, all mediated by the journal:

1. **The watchkeeper** (AIS + cameras + elephant field-sense). AIS gives byte-exact targets; cameras give trace-labeled detections; field-sense (vMF embeddings of traffic, surface d of the neural×quilt map) fuses them into one watch condition — "room temperature" at sea. The log-spotted-before-Casey case is the compound's signature: **floating debris carries no AIS signature.** Only the vision lane sees it, and the field flags *unexplained visual contact* — a detection with no AIS correlate — which is precisely the event class no single device can produce. Alerts are canary-graded confidence cascades ("the gauges that doubt for you"), never binary alarms.
2. **Predictive maintenance** (engine telemetry + plato-prediction). Engine PGNs — temp, oil pressure, RPM, fuel rate — journal byte-exact; a plato-style predictor reads the journal history and books *warnings, not verdicts* (surface d law). Pre-register the pass condition now: a predicted anomaly must precede the actual gauge alarm in recorded history to count as skill.
3. **The fish-run quilt** (depth/bottom + GPS traces). This is the quilt Casey actually wants: every pass journals (position, depth, bottom character); repeated passes weave a personal bathymetric quilt — the fish runs, with provenance, replayable, provable. Byte-exact from frame to map, because it's built from the journal, not from memory.
4. **Offline-first, sync-later.** The boat runs its own quilt cell with zero connectivity. Journals are **single-writer**: the boat journal is authoritative for boat-sensed facts; the shore forge never writes to it, it reads replicas. When signal returns (cell range, sat), the byte-exact journal syncs by idempotent replay — crash-safe, merge-conflict-free by construction. **NMEA-first doctrine:** raw frames are the source of truth; every derived view (targets, maps, alerts) is rebuilt from journal replay, so a brownout costs nothing but uptime.

## 3. DETERMINISM BOUNDARY AT SEA

Same law as the forge and the neural×quilt map, restated for a hull:

- **Nets are never in helm/engine-control paths.** There are no such paths in v1 — and this boundary is *why*, not a coincidence.
- **Byte-exact journal for anything safety-adjacent.** Position, AIS, depth, engine frames: append-only, checksummed, replayable. The at-sea F98 equivalent: **replaying the journal must reproduce every derived view byte-exactly.** That conformance check runs on the boat itself, net-free.
- **Neural cells are advisory only, trace-labeled** — same tier law as quilt-cellular. A model's word never outranks a gauge (the co-sign rule, structural at sea).
- **Why actuators stay unbound in v1 — explicitly.** Four reasons: (a) any perception→actuator chain crosses from trace-labeled perception into physical effect, violating the tier law; (b) the sea has no rollback — a wrong byte-exact spin on land costs minutes, a wrong rudder command costs the boat; (c) no canary class exists for steering — canaries must be cheap and repeatable, and "nearly broached" cannot be re-run; (d) v1 earns trust by watching, not acting. An actuator binds only when a pre-registered, replayable canary for its effect class exists. None does. Law, not backlog.

## 4. The cold-standby superinstance

The forgemaster charter, generalized: **the boat brain speaks the same opcode dialect as the desktop forge.** `qm_bind/link/effect/view/tick`, the propose→run→canary→book loop, the ledger, gold/scrap booking — identical. What differs is the tier mix:

| | Desktop forge | Boat brain |
|---|---|---|
| Hard cells (byte-exact) | the fabric, F98 conformance | **survival cells** — journal, gateway, replay, brownout recovery |
| Soft cells (trace-labeled) | a few neural readers | **perception cells** — vision, field-sense, prediction: most of the boat's value |
| Furnace | RTX 4050 + cloud mirror (advisory) | RTX 4050, no mirror — the WAN is a rumor 60 mi offshore |
| Roster | full forge roster | subset: Liquid-LFM2.5-2.6B (boat brain lane), qwen2.5vl:3b (vision), one reasoner |

Cold-standby cuts both ways: if the desktop forge burns down, the charter, the opcode discipline, and the ledger format live on in the boat copy — the superinstance survives because both halves share a dialect. And the boat's journals become the shore's corpus: raw NMEA frames are ledger-grade *facts*, feeding predictors under the same booked-evidence rules as everything else.

## 5. First three falsifiable steps (cheapest first, pre-registered)

| Step | Question | Pre-registered pass/fail | Cost |
|---|---|---|---|
| **BQ-1: gateway → journal cell, recorded replay** | Does the NMEA gateway cell journal and replay byte-exactly? Build it against a recorded log/.csv — no boat time needed | Pass: replay after `kill -9` mid-journal reproduces all derived views byte-exactly (the at-sea F98 canary). Fail: any divergence | an evening, shore-side |
| **BQ-2: camera cell, trace-labeled** | Does qwen2.5vl:3b on the 4050 produce useful watch labels from a wheelhouse camera? | Pass: on a recorded pass, vessel detections correlate with AIS targets above a recall floor; "log-like contact, no AIS correlate" fires on known debris — or doesn't, and we learn the false-positive floor | camera + laptop, alongside |
| **BQ-3: AIS quilt feed** | Does field-sense read traffic temperature? Targets journal byte-exact from the live feed (or shore-side AIS replay); elephant field runs on top | Pass: field "hot" readings precede CPA < 1 nm events at ≥2× base rate (Sounding Line standard). Fail: field is noise — book it | AIS feed + laptop, day trip |

BQ-1 before BQ-2 before BQ-3 because each needs strictly more hardware and more weather. All three are shore-testable to first order — the boat only joins at BQ-3, and even that can replay.

## 6. Open questions

| # | Question | Why it matters |
|---|---|---|
| 1 | Power budget: what does the 4050 laptop + gateway draw off the house bank, and for how long is the watchkeeper affordable? | the quilt that flattens the batteries is a hazard, not an asset |
| 2 | Journal growth rate vs. laptop disk — days at sea × frames/s | retention and rotation policy before the first long trip |
| 3 | Does PAIR discovery survive the boat LAN (mDNS over a switching fabric, node sleep)? | PAIR open q7, now with salt water |
| 4 | Which NMEA gateway hardware (Actisense-class vs. cheap USB)? | BQ-1's one purchase |
| 5 | Should phone-node annotations ever graduate from "human-authored journal entries" to cells? | v2 trust question; v1 answer is no |

---

*Next artifact: BQ-1's receipts, or a booked reason it didn't run. Either is a result — same rule at sea as at the forge.*
