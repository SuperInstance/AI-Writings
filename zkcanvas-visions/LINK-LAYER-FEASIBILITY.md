# Link Layer & Link-as-Subtext — Engineering Feasibility Assessment

*Round-2 engineering paper for the ZkCanvas charter (moves 2, 3, 4). Companion to CHARTER.md; answers the four questions: the Link abstraction, arrival-metadata-as-subtext, module boundaries across quilt-rust and tit_quilt_elixir, and the minimal exocortex cell. Provenance tags as in the round-1 catalog: [R] real today · [E] extendable from something real · [S] speculative.*

---

## 0. Verdict up front

| Design | Feasibility | Tag |
|---|---|---|
| Quality-vector Link abstraction over ESP-Now/BLE/WiFi/TCP/HTTP | Trivial on the data side; the work is in *decay* and *observation*, not structure | E |
| Link-as-subtext (arrival-path recorded on the message) | Feasible; governed by one principle — *subtext is observed, not declared* | E |
| Arrival-path joining cell state + field temperature | Feasible; one new dial on the elephant, one new prior on seam triage | E/S |
| Module split: quilt-rust owns links, BEAM fabric owns portals | Clean cut along the existing tier line (paper 211 Tier 1 vs Tier 0) | E |
| Minimal exocortex cell (ESP32, 16-byte protocol, dual-link demo) | One devkit + one potentiometer for Phase A; the demo path is a weekend, not a quarter | R/E |

Nothing below requires inventing a protocol the fleet doesn't already have the shape of. The opcodes stay transport-blind; the link layer is a *new organ*, not a new nervous system.

---

## 1. The Link abstraction

### 1.1 The charter's constraint, made precise

> The quilt cares what the link is *like*, never what the wire *is.*

Engineering translation: **`Link` is a quality vector plus a send handle — never an interface hierarchy.** There is no `EspNowLink extends Link`. There is a `LinkDriver` per transport that *produces* `Link` capability objects, and everything above the driver sees only qualities. The transport's name survives as exactly one field (`TransportKind`, §1.3) because the charter explicitly keeps one categorical quality — and even that is a tag set, not a type branch.

### 1.2 The quality vector

```rust
// quilt-link-core/src/qualities.rs  (pure, no_std + alloc)
pub struct Qualities {
    pub capacity:    Decay<BitsPerSec>,   // EWMA, half-life ~64 ticks
    pub latency:     Decay<Latency>,      // { p50: Duration, jitter_p95: Duration }
    pub cost:        Cost,                // relative units, see below
    pub reliability: Reliability,         // { delivery: Ratio, session_half_life: Ticks }
    pub kind:        TransportKind,       // tag set (§1.3)
}

pub struct Cost {              // all u16/u32 *relative* units, not SI — the quilt
    pub energy_per_kb: u16,    // cares about ordering, not physics. Battery-powered
    pub money_per_mb:  u32,    // links pay energy; cloud links pay money; a human
    pub attention:      u8,    // relay pays attention. All three are real costs.
}

pub struct Decay<T> { estimate: T, last_tick: Tick, /* ... */ }
// Decay re-reads toward a prior every half-life. A WiFi link that was good
// at tick 1000 is unknown at tick 10_000 unless re-sampled. Qualities are a
// FIELD READING, not a config file — they expire the way room warmth expires.
```

Three decisions worth defending:

1. **Qualities are estimates with half-lives, not configuration.** This is what makes the link layer a substrate citizen rather than a bolt-on: link state becomes tick-time state, refreshed by observation, decaying like every other field quantity. A stale quality and a stale cell value are the same kind of wrong.
2. **Latency is a profile (p50 + jitter), not a number.** I-90 and I-405 differ less in mean than in *variance*; the subtext semantic (§2) depends on jitter being first-class.
3. **Cost is a triple, not a scalar.** A battery cell pays energy, a cloud relay pays money, a human-carried device pays attention. Comparing these on one axis is the router's policy job (§2.4), not the type's job.

### 1.3 TransportKind as a tag lattice

The wire's name is kept as a small bitset of *behavioral* facets — because the router and the subtext reader only ever branch on facets, never on brands:

```rust
pub struct TransportKind(u8);
// BROADCAST     — many can hear one send (ESP-Now, WiFi multicast)
// MUTUAL_RX     — the peer can talk back on the same link
// SESSION       — delivery/retry/ordering managed by the transport (TCP, BLE GATT)
// NEEDS_BROKER  — third-party infrastructure required (AP, DNS, TLS CA, server)
// ENCRYPTED     — confidentiality provided below the quilt
```

This is the charter's "transport-blind" made checkable: a module may `match` on `kind.has(NEEDS_BROKER)`, and may never `match` on a brand. (The brand string is carried for *rendering* — the wall can say "arrived by soup-can" — but no logic reads it.)

### 1.4 The five instantiations [R — measured ranges, conservative]

| | ESP-Now | BLE (GATT notify) | WiFi/TCP (LAN) | TCP (WAN) | HTTP(S) |
|---|---|---|---|---|---|
| capacity | ~250 B/frame, airtime-bound; effective ≤ ~100 kb/s burst | tens–hundreds kb/s (connection-interval bound) | tens of Mb/s | Mb/s | Mb/s |
| latency p50 | 2–10 ms | ~10 ms–4 s (interval-bound; ESP32 typically 20–50 ms) | 1–10 ms | 20–100 ms | 100 ms–1 s+ |
| jitter | low, but loss comes in bursts (coexistence) | low steady, spikes on interval renegotiation | low | medium | high (broker-dependent) |
| cost.energy | low (no AP association, radio wakes per send) | low-medium (connection maintained) | high (association + stack) | high | high |
| cost.money | 0 | 0 | 0 | 0 | > 0 at scale |
| reliability.delivery | no transport retries (v0); expect loss, no ordering | session ACKs, ordered per-connection | full | full | full (request-scoped) |
| session_half_life | ∞/0 (connectionless — peers evaporate silently) | minutes (supervision timeout) | minutes | hours | 0 (per-request) |
| kind | `BROADCAST·ENCRYPTED*` | `MUTUAL_RX·SESSION·ENCRYPTED` | `MUTUAL_RX·SESSION` | `MUTUAL_RX·SESSION·NEEDS_BROKER` | `MUTUAL_RX·NEEDS_BROKER·ENCRYPTED` |

\* ESP-Now encryption exists (≈20 paired-peer limit); the demo runs unencrypted broadcast, so `ENCRYPTED` is honest only for paired mode.

Every cell of that table is a `Decay` value in the `LinkTable`, seeded from a built-in prior per transport, then corrected by observation. The priors ship in `link-core`; the corrections are per-instance truth.

### 1.5 The send handle

```rust
pub trait LinkDriver {
    fn links(&mut self) -> Vec<LinkId>;                  // enumerable links
    fn qualities(&self, id: LinkId) -> Qualities;        // current decayed reading
    fn send(&mut self, id: LinkId, frame: &[u8]) -> SendReceipt;  // fire-and-observe
    fn observe(&mut self) -> Vec<Arrival>;               // drain arrivals (driver stamps via-link, §2.2)
}
```

`send` returns a *receipt*, not a future — on connectionless links there is no delivery signal, and the abstraction must not pretend otherwise. Delivery knowledge arrives later as an `Arrival` (or its absence, which is itself a quality observation that updates `reliability`).

---

## 2. Link-as-subtext: the chosen channel as arrival-metadata

### 2.1 The principle: observed, not declared

The deep design rule, and the one thing this section actually decides:

> **Subtext is observed, not declared.** The receiver's knowledge of how a message arrived comes from the receiving hardware, not from sender self-report. The only declared part is the sender's *choice rationale* when it had a real choice — and that rides as a one-byte receipt, not a narrative.

Why this is the right cut: (a) sender claims about its own links are spoofable and stale; the receiver's own radio is an instrument; (b) it makes the firmware protocol tiny (§4) — an ESP-Now frame doesn't need to say "I came by ESP-Now," the arrival driver knows; (c) it honors the double-entry instinct from round 1 (sha receipts): arrival-metadata is a *receipt written by the counterparty's hardware*.

### 2.2 The envelope

```rust
pub struct Envelope {
    pub payload: Frame,          // §4.2 QuiltWire v0
    pub stamp:   RouteStamp,     // written once, by sender, when it chose
    pub trail:   PathTrail,      // appended-to, never rewritten, one Crossing per portal hop
}

pub struct RouteStamp {          // the sender's half — minimal, receipt-like
    pub chosen:     LinkId,      // the road taken
    pub considered: u8,          // bitmask: which links were live candidates at send time
    pub reason:     Reason,      // 1 byte: CHEAPEST | FASTEST | ONLY | RELIABLE | URGENT | BULK
    pub send_tick:  Tick,
}

pub struct Arrival {             // the receiver's half — written by the arrival driver
    pub via:        LinkId,
    pub observed:   Observed,    // { recv_tick, seq_gap: u16, inter_arrival: Duration }
}

pub struct Crossing {            // one per portal traversed
    pub portal:    CellId,
    pub via:      LinkId,
    pub snapshot: Qualities,     // at crossing time — the trail remembers what each hop was like
}
```

`RouteStamp` + `Arrival` join at the receiving cell as the **subtext record**: *what was chosen, what was available, what it cost, how it actually landed.* When the same logical tick arrives over two links (the dual-link case), the two arrivals are stored as **twins** — same `send_tick`, different `Arrival` — and the difference *is* the semantic content. That is seed #4 of the charter (I-90 vs I-405) in data form: the receiver knows differently — e.g. the BLE twin says *the cell is alive and powered*, the serial twin says *the state is trustworthy* — and the twins arriving in the wrong order or alone carry information about the sender's situation.

### 2.3 How arrival-path joins cell state

Cell state changes in three concrete ways:

1. **Event log entries carry the subtext record.** Every `effect` lands in the cell's tape with its `trail` + `Arrival`. The tick tape (round-1, real) gains one parallel column. Cost: bytes, not architecture.
2. **A derived stat per cell: `arrival_mix`** — the EWMA distribution over `Arrival.via` (plus cost/latency marginals). Cells expose it the way they expose value; the wall renders it (§5 demo). A cell whose arrivals are 100% the expensive link is *shouting*; a cell that fell silent on the reliable link but keeps heartbeating on the cheap one is *degraded but alive* — distinguishable states, today conflated.
3. **Seam triage prior for reconciliation.** This is the engineering payoff that pays for the whole feature: when harbor-side and boat-side tapes won't marry (the Harbormaster's seam), the arrival paths classify the seam before any human or agent argues about it. A seam whose divergent messages arrived over low-reliability links with `seq_gap > 0` is *probably transport* (lost frames, reorder) — handle by re-request, no blame. A seam where both sides received cleanly over reliable links is *probably genuine disagreement* — escalate to visible-seam rendering (round-2 seed #3). Today nothing distinguishes these; the subtext record does, for free, because it was written by hardware.

### 2.4 The routing policy (egocentric, pure, replayable)

Dual-link routing is a pure function per message class — **no global routing table, ever** (egocentric doctrine: the router is a cell-local organ):

```rust
pub fn choose(msg: MsgClass, links: &LinkTable, t: Tick) -> LinkChoice {
    // MsgClass: HEARTBEAT | STATE_DELTA | ALARM | TAPE_SYNC
    // HEARTBEAT  -> cheapest link; loss tolerated (silence is the signal)
    // STATE_DELTA-> reliability-weighted; jitter matters (order-sensitive cells)
    // ALARM      -> ALL live links, redundant fire (cost no object; duplicates are fine,
    //               and *which duplicates arrive* is itself field data)
    // TAPE_SYNC  -> capacity-weighted bulk (reconciliation on reconnect)
}
```

The `reason` byte recorded in `RouteStamp` is the policy's own classification of its choice — which makes every routing decision replayable and auditable from the tape alone. Policy is data, not code: a cell can carry its own (a field unit prefers energy-cheap links; a shore mirror prefers money-cheap ones — same abstraction, different weights).

### 2.5 How arrival-path joins the field/temperature sense

The elephant (essay_86) gives the mounting point, and the identification is almost embarrassingly clean:

- **Warmth** = write-rate/settle (round-1, real). Extend: warmth is *cost-weighted* write-rate. A room heated only by expensive links is a room whose members *pay to speak* — which is the room-temperature signature of urgency. The sauna metaphor survives: expensive speech is hot speech.
- **A new dial: arrival-channel mix.** The DialBank's S⁸ direction μ gains a component: the distribution over arrival links. Interpretation follows essay_86's phase-lock logic — a room where all arrivals share one link is *transport-phase-locked*: an infrastructure echo chamber, one cut of one cable from silence. A room with diverse arrival mix is transport-contrasty, resilient. κ (concentration) reads it for free: low channel-κ = healthy heterogeneity.
- **Thermal trails become literal.** The Barge Agent's speculative "thermal trails along habitual routes" (round-1 catalog) resolves into *habitual links*: the trail of a message's habitual road, fading like warmth when the road changes. Pull the USB cable in the demo (§5) and you watch a trail go cold in the arrival mix — the room's map of the sender's situation, redrawn by absence.

Tag: the warmth re-weighting is [E]; the dial and its κ reading are [E/S] — the mounting exists (RoomField, DialBank), the semantic mapping is the round's bet.

---

## 3. Module boundaries: quilt-rust, the BEAM fabric, and who owns portals

### 3.1 The cut

**quilt-rust owns the link layer. The BEAM fabric (tit_quilt_elixir) owns portals and nesting.** The spec for both is written once, in golden-vector form, inside link-core, and both sides test against the same bytes.

Rationale, in order of force:

1. **Links are I/O-bound; portals are semantics.** Drivers (radio, sockets, USB) want a small no_std-capable core compiled to wasm32 and xtensa — that is exactly quilt-rust's Tier-1 role (paper 211: SPAWN/BIND/STREAM). Portal semantics (re-origin, mirror, disagreement) are address-space and supervision semantics — VM territory.
2. **A portal is a supervision boundary.** The charter: crossing a portal re-origins you; the laptop's rendering of the ESP32's web is a mirror of a *foreign universe*. On BEAM, "supervise an unreliable foreign universe" is the native failure model: the portal is a process tree whose child is the mirror, and the child *is expected to lie or die*. `quilt-rust` has no story for that at wasm scale and shouldn't.
3. **Disagreement-at-the-portal wants process isolation.** The charter's corrected verdict — *disagreement lives at portal boundaries, and a canvas that shows both sides is doing something new* — needs the two renderings (my-mirror-of-you vs your-self-rendering) held apart with independent failure. Cheap on BEAM; a research project in a single wasm heap.
4. **The opcodes stay transport-blind (charter move 2).** Nothing about portals or links requires new opcodes — see the mapping below. The BEAM encoding's one-to-one Erlang-primitive mapping (harbormaster's ledger) is preserved, not perturbed.

### 3.2 Opcode mapping [E — no opcode changes, only what each one means at the link layer]

| Opcode | Link-layer meaning | BEAM primitive (unchanged) |
|---|---|---|
| `qm_bind` | bind cell ↔ remote peer over a `LinkId`; the binding snapshots the link's qualities — the *first temperature sample* of the relationship | spawn/register |
| `link` | **unchanged** — adjacency links cells, not wires; the seam (formula/dependency) never learns the transport | link/monitor |
| `effect` | carries the `Envelope` (payload + stamp + trail); arrival appends observation; portal hop appends a `Crossing` | message send |
| `view` | a view request is itself a message (gets subtext); a view *across* a portal renders mirror+self side by side, disagreement visible | call |
| `tick` | qualities decay one step; policy re-evaluates; `LinkTable` is tick-time state exactly like every cell | heartbeat |

### 3.3 Layout — quilt-rust (wasm/edge + native + embedded)

```
quilt-rust/crates/
  link-core/            # THE SPEC LIVES HERE. Pure, no_std+alloc.
    src/qualities.rs    #   Qualities, Cost, Decay, TransportKind
    src/subtext.rs      #   RouteStamp, Arrival, Crossing, PathTrail, Envelope
    src/policy.rs       #   MsgClass, choose(), Reason
    src/wire.rs         #   QuiltWire v0 frame codec + CBOR subtext codec
    spec/golden/        #   golden vectors (JSON+bytes): same files the Elixir tests read
  link-serial/          # driver: USB/UART  (demo wired path; embedded-io + serialport)
  link-ble/             # driver: btleplug (laptop) / NimBLE (embedded, via arduino lib)
  link-espnow/          # driver: embedded side direct; laptop side via gateway protocol (§4.4)
  link-tcp/             # driver: tokio / std
  link-http/            # driver: reqwest (native) / fetch (wasm)
  portal-lite/          # wasm/edge minimal portal CELL: can mirror + render disagreement
                       # it is TOLD about; not the arbiter (fabric is). Demo-capable.
```

`link-core` compiles to wasm32-unknown-unknown and to the ESP32's xtensa target unchanged; drivers are ordinary per-platform crates behind the `LinkDriver` trait. This satisfies paper 211's Law of Portability for the new organ.

### 3.4 Layout — tit_quilt_elixir (BEAM fabric)

```
tit_quilt_elixir/lib/tit_quilt/
  link/subtext.ex        # decodes RouteStamp/Arrival/PathTrail — byte-parity with link-core
                        # via the shared golden vectors (property tests, both directions)
  link/table.ex          # LinkTable as tick-decayed state; updated by drivers, read by policy
  link/policy.ex         # port of choose() — or driven through link-core compiled to wasm?
                        # No: pure Elixir port, kept honest by shared vectors. Policy is small.
  link/drivers/tcp.ex    # gen_tcp
  link/drivers/http.ex   # Req/Finch
  link/radio_nif.ex      # OPTIONAL NIF wrapping a link-core driver (BLE/ESP-Now dongle on host)
  portal.ex              # PortalCell: a supervised process tree per portal.
                        #   child = mirror of the foreign universe (tape replay + reconcile)
                        #   parent = the portal cell the local quilt sees (one simple cell)
  portal/disagreement.ex # the seam ledger: where my-mirror-of-you ≠ your-self-rendering
  portal/re_origin.ex    # crossing semantics: address rewrite, 0/0/0 reset, trail append
```

### 3.5 Who owns portals and nesting — the explicit answer

- **Reference semantics and arbiter: the BEAM fabric.** `PortalCell` is a cell kind whose value is a foreign universe's mirrored tape. Re-origin (charter move 4) is `re_origin.ex`'s address rewrite at the crossing; the disagreement ledger is per-portal process state, rendered side-by-side on any `view`.
- **Edge/wasm: `portal-lite`.** A browser or edge worker can *host* a portal cell — terminate radio links (via a gateway), mirror a universe, render both stories — but it does not adjudicate; its disagreement view is presentational. This keeps the wasm story honest about what a sandbox can own.
- **Nesting depth:** unlimited on the fabric by construction (a portal's child can contain portals — the ESP32's quilt is itself one cell in the laptop's quilt, and the laptop's quilt is itself one cell in the fleet's). The trail in every envelope records the full crossing chain, so any viewer can see how deep they're looking and by which roads the data came. Deflation zoom (within-universe) remains what it is in quilt-geometry — orthogonal to portals, per the charter.

---

## 4. The minimal exocortex cell: ESP32 firmware

### 4.1 Target

One ESP32 devkit (recommend S3 for native-USB CDC; any works — classic parts use the UART bridge), `framework-arduinoespressif32` (PlatformIO), one sensor. The firmware exposes **one quilt cell** — a value cell — over two links simultaneously. From the laptop, the whole board is one cell; from inside, it's a (tiny) quilt. That asymmetry *is* the portal demo.

### 4.2 QuiltWire v0 — the smallest viable protocol [R]

Fixed 16-byte frame. Fits ESP-Now (250 B limit) with 234 bytes of headroom for TLVs; fits a BLE notification (20-byte default MTU chunk... use the 16 bytes as one notification); fits a UART line.

```
byte  0    : magic 'Q'                     (0x51)
byte  1    : version 0x01
byte  2    : kind      TICK | DELTA | ALARM | LINKMETA | ACK
byte  3    : cell id   (u8 — one byte because the demo universe has few cells;
                        the portal maps local ids to fabric addresses)
bytes 4-5  : seq       (u16, wraps — gap detection = reliability observation)
bytes 6-9  : tick      (u32 — the board's local tick, 1 Hz)
bytes 10-13: value     (f32)
bytes 14-15: CRC16-CCITT
--- optional TLVs after byte 16 when the transport MTU allows ---
TLV 0x01   : reason byte + considered-mask  (present ONLY when sender had ≥2 live
             links — the declared half of subtext, and nothing else is ever declared)
```

What is deliberately absent: timestamps-in-µs (no cross-clock claims — latency is observed in tick units and receiver-side inter-arrival only), sender-quality reports (observed, not declared, §2.1), routing headers (egocentric: no global addressing in the frame), and encryption (v0 demo; ESP-Now pairing is phase-C).

The board-side cell is a value cell with a 64-entry tape ring: `{tick, value, seq}` triples, plus `settle` (change-rate) — enough for the laptop to render warmth and for a portal to reconcile by replay. ~40 lines of C++.

### 4.3 Firmware layout

```
exocortex-cell/               # new repo (or quilt-esp32/examples/cell_min)
  platformio.ini              # envs: [cell_s3] (sensor cell), [gateway] (esp-now↔serial bridge)
  src/
    main.cpp                  # setup/loop: poll sensor → cell.tick() → policy → send both links
    qw_frame.h                # QuiltWire v0 encode/decode — CC, header-only, byte-identical
                              # to link-core's wire.rs (checked in CI by the golden vectors)
    cell.h / cell.cpp         # the one cell: value, epsilon-delta, settle, 64-tape ring
    link_table.h              # Qualities per LinkId: fixed-point EWMA, decay on tick,
                              # choose() — the policy port, same reason bytes as link-core
    link_driver.h             # the trait: send(frame, id), poll() -> arrivals
    link_serial.cpp           # driver: UART/USB-CDC @ 115200, line-framed
    link_ble.cpp              # driver: NimBLE-Arduino, one GATT service, notify characteristic
    link_espnow.cpp           # driver: esp_now broadcast, register_recv_cb
                              # (phase B/C: peers into the board's own radio mesh)
  test/test_frame_roundtrip.cpp
```

Whole-image budget: NimBLE + ESP-Now + cell + drivers ≈ well under 200 KB flash, heap comfortably under 100 KB on a classic ESP32 — the constraints are not close to binding at one cell. (Noted honestly: BLE and WiFi/ESP-Now share the 2.4 GHz radio on this silicon; coexistence time-slicing inflates *both* links' latency when both are hot. This is not a bug for us — it is a genuine field effect the quality vector will correctly show as covariance between the two links. Demo color.)

### 4.4 The laptop-side ESP-Now question, answered honestly

Laptops cannot speak ESP-Now. Three options, in the order adopted:

1. **Phase A: don't.** The dual-link demo runs over **USB serial + BLE** — both native to one devkit, both natively receivable by a laptop. This already demonstrates the entire subtext pipeline.
2. **Phase B: gateway node.** A second devkit runs the `[gateway]` env: ESP-Now ↔ serial bridge. The laptop's `link-espnow` driver speaks the gateway protocol over USB. Cost: one devkit (~$5). This is a *link*, not a portal — the gateway is transparent infrastructure, exactly the kind of thing the qualities table should price as `NEEDS_BROKER`-adjacent (broker = gateway).
3. **Phase C: same gateway hosts its own universe.** The gateway stops being transparent: it runs two cells of its own. Now the laptop has a real portal — see §5.

### 4.5 Laptop side

```
quilt-rust/examples/exocortex_demo/
  src/main.rs                # binds link-serial + link-ble (+ link-espnow in phase B/C),
                             # runs LinkTable + policy, stamps arrivals, serves the wall
  src/wall.rs                # egocentric render: the ONE cell, its tape, its arrival mix,
                             # warmth; terminal first, one static HTML page second
```

Native binary first (radio access), wasm build of the same demo second (wall served to a browser). No BEAM required for Phase A/B — the demo deliberately proves the cut: links live entirely in quilt-rust; `portal-lite` carries Phase C until the fabric joins.

---

## 5. The smallest end-to-end demo

**BOM, Phase A:** one laptop, one ESP32-S3 devkit, one potentiometer on an ADC pin (chosen over DHT22 deliberately: zero driver dependencies, continuous value, and "sensor" honesty — swap a DHT22 in for the room-temperature version with one file change).

**Path:** pot → ADC @ 1 Hz → `cell.tick()` → `DELTA` on change > ε (else `TICK` heartbeat every 30 s) → `choose()` → both links (deltas prefer serial/reliable; heartbeats prefer BLE/cheap; alarms fire both) → laptop demo binds both drivers → arrivals stamped → the wall.

**The three payoff scenes** (each maps to a charter round-2 seed):

1. **Both paths live — the twins.** The same tick arrives twice; the wall shows twin entries with different tone — serial twin (reliable, jitter-flat) rendered solid; BLE twin (cheap, jittery) rendered warm-light. *What the receiver knows differently:* serial-twin-alone ⇒ state trustworthy, radio maybe down; BLE-twin-alone ⇒ cell alive and cheap to talk to, but the state channel is cut — power problem, not death. (Seed 4: same message, I-90 vs I-405.)
2. **Pull the USB cable — the room's weather changes.** Arrivals collapse to BLE. Nothing alarms. The cell's `arrival_mix` shifts 100%, its warmth dips (cost-weighted write-rate drops even though write-rate doesn't), and the wall shows the thermal trail of the serial road going cold. Plug back in; the tapes marry — one breath, dashed goes solid (the Harbormaster's reconciliation, felt first-person). (Seed 2: de-sync at 1 s vs 1 h.)
3. **Phase C — the portal and its disagreement.** The gateway devkit now runs its own two-cell quilt (sensor + link-health cell) and also *its own rendering of itself*. The laptop quilt shows that whole universe as one portal cell. Kill the radio: the laptop's mirror goes dashed-prediction while the ESP32's self-rendering stays solid — two true stories of the same universe, rendered side by side, disagreement visible and located. (Seeds 1 and 3.)

**Runbook, Phase A:** `pio run -e cell_s3 -t upload` → `cargo run -p exocortex_demo` → open wall → wiggle the pot → watch twins arrive → pull the cable. An afternoon, including the NimBLE pairing fight.

---

## 6. Risks and open problems

| Risk | Severity | Handling |
|---|---|---|
| Sender-declared rationale is spoofable | low | It is sensor data, not authentication. Trust model is the ledger's (sha receipts, round 1). The observed half of subtext can't be spoofed by the sender. |
| Cross-clock latency claims | medium (honesty) | v0 measures tick-units and receiver-side inter-arrival only. No NTP theater. Per-link offset estimation is phase-C research. |
| BLE/WiFi coexistence on one radio | medium, *featureful* | Documented above; qualities will show real covariance. Render it; don't hide it. |
| ESP-Now on laptop | low | Gateway node (§4.4). |
| Portal disagreement semantics (what exactly is a "true" disagreement vs stale mirror?) | high (this is the round's actual research) | Deliberately deferred to the fabric's `portal/disagreement.ex`; the demo exposes the question rather than settling it. |
| NimBLE/Bluedroid heap on tiny parts | low | NimBLE mandated in platformio.ini lib_deps. |

## 7. Honest ledger

*Real today [R]:* every transport driver exists on both sides; the 16-byte frame and its golden vectors are an afternoon; one-cell firmware fits trivially; Phase A demo path is fully buildable from this document.

*Extendable [E]:* qualities-with-decay; subtext observed-at-arrival; seam triage by path reliability; the module cut at the tier line; cost-weighted warmth.

*Speculative [S]:* the new elephant dial and its κ reading (§2.5); portal disagreement semantics; trail-as-thermal-trail rendering. These are the round's bets, and they are bets about *meaning*, not mechanism — which is the correct place for the risk to live.

The crown holds: nothing above requires anyone to have built channel-choice-as-subtext before. The mechanism is modest; the claim it lets you test is not.
