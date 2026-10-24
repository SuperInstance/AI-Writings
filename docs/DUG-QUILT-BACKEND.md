# DUG → quilt backend — mapping a UAV swarm onto the fabric

*2026-09-03 · AI-Writings/docs/DUG-QUILT-BACKEND.md · companion to BOAT-SUPERINSTANCE-QUILT.md (device→cell map pattern), NEURAL-QUILT-INTEGRATION.md (tier law), and nq-c3-metal/NQ-C3-METAL-SPIKE.md (silicon precedent)*

**Verdict up front.** Casey's directive: take the abandoned `SuperInstance/decentralized-uav-grid` (DUG) repo and see what the quilt backend would actually do for it. The answer is the same shape as the boat doc: **a drone swarm is a quilt cell with propellers on it** — same opcodes, same tier law, same journal doctrine, different failure physics (RF loss instead of brownout, kinetic irreversible effects instead of rudder). But this doc is written *pre-registration-first*, and the honesty bar is higher here than for the boat, because DUG is one commit (`2be5f53`) of mostly-placeholder code that has never flown, never been hardware-tested, and in two places its "security" is decorative. Nothing below has touched a battery or an antenna. It is a map plus three pre-registered experiments (DQ-1/2/3) at the end where the map either earns a receipt or dies.

**Sources read for this doc** (all quotes are from these files, line-level, nothing invented):
`src/dug_core/src/uav_node.cpp` (the heart), `src/dug_core/include/dug_core/vfh_planner.hpp`, `src/dug_core/include/dug_core/payload_manager.hpp`, `src/dug_communication/dug_communication/mesh_monitor.py`, `src/dug_vision/dug_vision/{target_detector,vslam_node}.py`, `src/dug_msgs/msg/*.msg`.

---

## 1. Subsystem → fabric operation map

Same table shape as the boat doc's §1. Tier law: **byte-exact or trace-labeled, declared at bind time, never mixed inside one cell.**

| DUG subsystem | Where (file) | Quilt cell | Opcode | Tier | Notes |
|---|---|---|---|---|---|
| SwarmState pub/sub (`/swarm/status`) | `uav_node.cpp` `timer_callback` | **Journal cell**, one per UAV, single-writer | `qm_effect`: append the SwarmState bytes *before* any derived view exists; `qm_view`: latest-per-uav_id | **Byte-exact** | today the message is consumed and thrown away (§3) |
| Leader selection | `uav_node.cpp` `select_leader` | **Election cell**: pure integer function over the journal prefix at tick n | `qm_view` of journal → `qm_effect` one tick-stamped leader verdict entry | **Byte-exact** | replaces the float formula (§2) |
| Formation control | `perform_formation_control` + `FormationState.msg` | **Formation cell** | leader `qm_effect` writes slots; followers `qm_view`-only | **Byte-exact** after integer re-cast | needs a tick/epoch for fencing (§2.3) |
| Target detection | `target_detector.py` → `/swarm/targets` | **Vision cell** — cameras watch, they touch nothing (boat §1 law, verbatim) | `qm_view`-only; labels booked as trace-labeled journal entries | **Trace-labeled** | today: no confidence gate at all (§4.1) |
| VSLAM | `vslam_node.py` → `vslam_pose` | **Perception cell** | `qm_view`-only; pose is advisory until an integer divergence gate passes | **Trace-labeled** | today: raw failover straight to helm (§4.2) |
| Mission / Kamikaze commands | `/swarm/mission`, `/swarm/kamikaze` | **Effect gate cell** | `qm_effect` only after verifier; irreversible effects **unbound** under house law | **Byte-exact** | the worst hole in the repo (§4.3) |
| "Zero-Trust Handshake" | `compute_hash_signature` / `verify_peer_signature`; `mesh_monitor.py` | **Identity = journal chain tip + tick** | `qm_bind` bootstrap; message MAC binds tip‖tick‖body | **Byte-exact** | §5 |
| VFH+ obstacle avoidance | `vfh_planner.hpp` | **Reflex cell — stays local** | no opcode crossing the mesh; per-drone | **Byte-exact** after integer re-cast (§6) | DUG already gets this right (§2.4 credit) |
| `mesh_monitor.py` | whole file | **Ops viewer cell** | `qm_view`-only | viewer, like phone nodes on the boat | today: in-memory dict, zero record |

---

## 2. Thesis 1 — leader election: the float formula vs. integer cell ticks

### 2.1 What the code actually does

The entire election is in `select_leader()`, run by every node on a 1 Hz wall timer:

```cpp
// Score formula: Score_i = w1 * B_i + w2 * C_i - w3 * L_i
float max_score = 0.5f * battery_level_ + 3.0f * static_cast<float>(own_connectivity)
                - 0.2f * own_hw_load;
```

with the load term literally driven by the wall clock:

```cpp
float own_hw_load = 20.0f + 10.0f * std::sin(now_time.seconds() * 0.1f) + (uav_id_ * 5.0f);
```

and a tie-breaker guarded by float equality:

```cpp
} else if (m_score == max_score) {
  // Tie-breaker: lowest ID
```

Peer scores are computed from the **last received SwarmState**, not from live state (`if (last_seen_peers_.count(member.first) && (now_time - last_seen_peers_[member.first]).seconds() < 5.0f)` gates membership; the score reads `member.second.battery_percentage`, `member.second.connectivity_degree`, `member.second.hardware_load` — the published copy).

### 2.2 The exact failures (four, all observable in the code)

1. **Asymmetric inputs.** Node A scores itself with *live* `battery_level_` (draining 0.1/s in `timer_callback`) and *its own* `sin(now)` phase; node B scores A from A's ~1-second-stale published copy with *A's publish-time* phase. The tie-breaker comment says "lowest ID," but a genuine tie between floats computed from different data at different instants almost never produces `m_score == max_score` — the branch is close to dead code, and the `>` comparison flips on last-ulp differences. Two nodes can each conclude *I win* on the same logical second → both set `is_leader_ = true` → **both publish `FormationState`** (the leader branch in `timer_callback` publishes unconditionally when `is_leader_`). Followers apply last-writer-wins (`current_formation_ = *msg;` in `formation_callback`) → two formation authorities, one swarm.
2. **Wall clock in the score.** The `sin(now_time.seconds() * 0.1f)` term makes every node's load — and therefore the ranking — a function of *when the timer fires*, not of the world. Two nodes one timer-skew apart disagree about the same drone's score forever. There is no epoch, term, or logical tick anywhere in the message set (`FormationState.msg` is exactly `leader_id / formation_center / formation_type` — no fencing field).
3. **Different mesh views, both "true."** `own_connectivity` counts *my* last-5s peers; `connectivity_degree` in a peer's message counts *theirs*. Same mesh, two honest numbers, no common substrate to reconcile them on.
4. **No fencing of a deposed leader.** After a partition heals, the old leader's in-flight `FormationState` messages are indistinguishable from the new leader's — same topic, no term, no tick, no signature (FormationState is not covered by the handshake at all; only SwarmState is — see §5).

### 2.3 What byte-exact cell ticks remove

Election as a quilt opcode cell: `leader(tick n) = rank(entry_bytes)` — a pure function over the journal's latest SwarmState entry per uav_id at a common integer tick, ranked lexicographically on **integers** (battery_pct_q8, connectivity, negated load, then uav_id as final discriminator). Tie-free *by construction* because uav_id breaks every remaining tie. What this removes, failure by failure:

- No wall clock: the tick is a logical counter, advanced once per append. `sin(wallclock)` cannot make two honest nodes disagree.
- No float comparison: integer ranks on the *same journal bytes* — every node that has the same prefix computes the same leader, deterministically, forever.
- Symmetric inputs by construction: the score inputs *are* the journal entries; there is no "live vs. stale" duality because the entry is the only truth.
- Fencing: every `FormationState` effect carries `(tick, chain_tip)`; any node rejects a formation command whose tick ≤ the last accepted tick. A deposed leader is fenced by arithmetic, not by hoping its messages stop.

**Honesty rider:** on a torn tail (a node missing the journal's last k entries) prefix-election *can* transiently pick a different leader than the fully-synced nodes — DQ-1 pre-registers exactly this and can fail on it. The claim is not "no transient divergence"; it is "divergence is deterministic, bounded by the unsynced suffix, and converges the moment the tail heals — with no oscillation term." DUG has no convergence property at all; the sin term guarantees permanent disagreement potential.

### 2.4 Credit where DUG is already right

VFH+ obstacle avoidance runs **locally per drone** (`vfh_planner_.compute_safe_heading(...)` inside `perform_formation_control`, on the drone's own `latest_obstacles_`) — it is not routed through the leader or the mesh. The house agrees: reflexes stay local; the quilt never centralizes a collision reflex onto RF. This part of the design survives the mapping unchanged.

---

## 3. Thesis 2 — swarm state as journal: forensics and torn-tail healing

**What the code does today:** every SwarmState is consumed and discarded — `swarm_members_[msg->uav_id] = *msg;` is a last-writer-wins map, `last_seen_peers_[msg->uav_id] = this->now();` an ephemeral clock entry, and `mesh_monitor.py` keeps `self.peers = {}` with 5-second eviction. After an incident — a spoofed swarm member, a leader flap, a payload release — there is **no record of anything**: who was leader at second t, what target was injected when, which signatures were rejected. Rejected forgeries leave one `RCLCPP_WARN` log line and vanish. `PayloadManager` mutates `state_` and `munition_count_` purely in memory; a munition release has no audit trail at all.

**The quilt transplant.** Every UAV runs a single-writer append-only journal (its own actions and its verified observations), entries chained as `hash(prev_hash ‖ canonical_bytes)` — the house provenance-chain law. This is exactly the BQ-1 discipline from the boat doc, with one physics substitution: the boat's kill -9 becomes **RF loss**. The boat doc's BQ-1 pass condition is "replay after `kill -9` mid-journal reproduces all derived views byte-exactly"; the DUG version is "replay after a partition/drop burst reproduces the swarm view byte-exactly." Torn-tail healing over a lossy BATMAN-adv mesh is the *same operation*: per-node single-writer streams with monotone ticks sync by idempotent replay of the missing suffix — crash-safe and merge-conflict-free by construction, which is precisely the boat doc's §2.4 "offline-first, sync-later" compound with the ocean swapped for RF shadowing.

Post-mission forensics becomes a property of the medium, not an afterthought: an accident board replays every drone's journal, merges by tick, and gets a **byte-exact reconstruction of the swarm's believed state at every tick** — including the rejected-signature forgeries, which get journaled as entries too (evidence, not log spam). DQ-2 is where this earns or loses its receipt.

---

## 4. Thesis 3 — the determinism boundary: nets propose, integers dispose

The boat doc's law, verbatim: **nets are never on helm**. DUG's current code violates it in three concrete places, in descending severity:

### 4.1 KamikazeCommand: the most destructive message in the system has zero verification

`swarm_callback` verifies signatures on SwarmState. `kamikaze_callback` verifies **nothing**:

```cpp
void UavNode::kamikaze_callback(const dug_msgs::msg::KamikazeCommand::SharedPtr msg)
{
  if (msg->armed) {
    is_kamikaze_mode_ = true;
    attack_target_ = msg->target_location;
    payload_manager_.arm();
```

`KamikazeCommand.msg` has no signature field at all. Anyone who can publish to `/swarm/kamikaze on the mesh drives every listening drone into an armed dive. The zero-trust story has a hole exactly at the irreversible action. Under the house actuator law (boat §3, reasons b and c), irreversible effects have no canary class — you cannot re-run "nearly detonated" — so the quilt mapping is not "sign the kamikaze message" (that's a patch, and worth doing, see DQ-3); it is that **irreversible effect classes bind only behind a verifier cell with a co-sign rule**, or stay unbound. The tier law exists precisely so that nothing trace-labeled can reach `payload_manager_.arm()`.

### 4.2 VSLAM failover: neural pose straight onto the helm

```cpp
if ((this->now() - last_gps_time_).seconds() > 2.0) {
  ...
  current_pose_ = vslam_pose_;   // Failover: replace current pose with SLAM pose
```

No divergence bound, no confidence tier, no sanity check. And `vslam_node.py`'s pose is a random walk — `self.drift_x += random.uniform(-0.01, 0.01)` — which is an honest placeholder for a real neural SLAM's drift. The substituted pose is then published in SwarmState (`msg.current_pose = current_pose_`), becomes the leader's `formation_center`, and steers every follower (`auto leader_pose = swarm_members_[current_formation_.leader_id].current_pose;`). **One drone's drifting estimate steers the whole formation, with no integer in between.** The quilt mapping: VSLAM is a trace-labeled perception cell, `qm_view`-only; its pose may enter the control view only after an integer gate (bounded step vs. last-good pose, speed limit, staleness tick) — the same shape as the boat's "a model's word never outranks a gauge."

### 4.3 TargetInfo: a confidence field nobody reads

`TargetInfo.msg` carries `float32 confidence`, and `target_detector.py` publishes `target.confidence = 0.95` — but `target_callback` syncs targets into `global_targets_` with no confidence floor, no corroboration requirement, no geofence check: `if (!exists) { global_targets_.push_back(*msg); ... }`. Any node injects any target fleet-wide. (Mitigating honesty: in this commit `global_targets_` is not yet read by the control path — the dive target comes from KamikazeCommand. The pipe is built but the ammunition hasn't been loaded; wire it up without a gate and §4.1's hole inherits a neural trigger.) The quilt mapping is the boat's vision-cell law verbatim: detectors are `qm_view`-only, labels booked trace-labeled; a target graduates to a byte-exact `MissionCommand` effect only through an integer verifier — confidence floor, geofence bounds, ≥2-drone corroboration, rate limit. **VSLAM/vision proposes; integer formation/geofence code verifies and can veto.** That boundary is DUG's missing safety story, and it is the single highest-value thing the quilt backend brings to this repo.

---

## 5. Thesis 4 — mesh auth: the shared secret vs. the chain tip

What DUG calls "Zero-Trust Handshake" is, line-level:

```cpp
std::string secret_key = "dug_secure_key_2026";
std::string data = std::to_string(uav_id) + ":" + std::to_string(time_window) + ":" + secret_key;
return Sha256::hash(data);
```

(the same literal string sits in `mesh_monitor.py` as `self.secret_key = "dug_secure_key_2026"`). Three failures, all structural:

1. **A PSK compiled into the source.** Every drone and the monitor share one secret baked into a public repo. Anyone who reads the repo forges *any* UAV identity. "Zero-trust" with a global symmetric key is trust in everyone who ever saw the repo.
2. **The signature covers the identity, not the body.** `verify_peer_signature` recomputes the hash of `uav_id:window:key` and compares — the message's battery, pose, and connectivity fields are never hashed. A valid SwarmState can have its fields tampered (battery → 100, pose → anywhere) and still pass. The handshake authenticates a *name*, providing zero *integrity* — and leader selection scores are computed from exactly those unprotected fields (§2).
3. **A ±30 s replay window with wall-clock coupling.** `verify_peer_signature` accepts windows `w0-1, w0, w0+1`, so a captured message verifies for up to ~30 s; and since windows come from `std::time(nullptr)`, a drone skewed >20 s fails handshake entirely — an availability failure grafted onto a security mechanism.

**The quilt answer — journal chain as lightweight mesh identity.** A drone's identity is the tip of its journal chain, bootstrapped at `qm_bind` (which still needs a real key ceremony — the quilt does not invent key distribution, and we say so). Each mesh message carries `(chain_tip_hash, tick_n, MAC(tip ‖ tick ‖ body))`. This fixes the three failures in order: continuity of the single writer is evidenced by the chain (forging a peer's history means out-building its observed tip — an economic cost, not a cryptographic miracle; we undersell it as exactly that); the MAC covers the **body**, so field tampering dies; and `tick_n` is monotone, so replays are rejected by `tick ≤ last_seen_tick` with **zero dependence on wall clocks**. The BQ-style receipt that this is more than talk is DQ-3: a red-team script that spoofs, tampers, and replays `armed=true` against both the baseline and the gated build, with the pass condition written before the test.

---

## 6. Thesis 5 — the silicon path: can the formation loop lower to a netlist?

`perform_formation_control` and `vfh_planner.hpp` are float code today (`atan2`, `cos`, `sin`, `std::sqrt`). But the *structure* is already integer-shaped: offsets are the constants ±5.0; VFH's occupancy decision is a comparison per sector — `occupancy_grid[i] = (distances[i] < threshold_)` with `threshold_ = 1.5` — valley width is `min_valley_width = 3` sectors; headings in the fallback path are literally sector indices (`return best_idx * increment`). Transcendentals appear only in heading↔position conversion, which a Q16 fixed-point or sector-index formulation removes. An integer re-cast of this inner loop — leader slot lookup, offset add, occupancy compare, valley vote, one setpoint — is precisely the class of thing NQ-C3 hand-lowered to Verilog-2005 with a bit-exact Python twin across 100 ticks × 7×16 bits, synthesizing to a 1,566-cell netlist (the house's cleanest silicon receipt: *two substrates, one integer semantics, zero drift*).

**Honesty riders, quoting the steelman lane's own verdict:** the sheet→netlist compiler **does not exist** — "same sheet compiles to browser/edge/FPGA" is STRETCHED, and NQ-C3 was one hand-lowered stone across that creek, with its own corpse finding (dynamics calibration is the research; the arc extinguished at the first synapse). So the DUG silicon claim is not "the formation controller becomes an FPGA." It is: *if* the inner loop is re-cast in integers, it acquires a **conformance twin** — a Python model that must agree bit-exactly with the flight build — and the twin discipline (not the bitstream) is the deliverable. A netlist is a possible future lowering, proven at whatever scale it can actually be checked. Nothing in DQ-1/2/3 touches silicon; this thesis is deliberately deferred behind the open questions.

---

## 7. Where the quilt does NOT help (undersell, deliberately)

- **The RF physical layer.** BATMAN-adv routing internals, packet loss, latency jitter, link asymmetry, antenna physics. The journal survives drops and heals tails; it does not prevent a single dropped packet. Torn-tail healing trades *latency* for consistency — a drone acting on a stale prefix during healing is acting on old data, knowingly.
- **Flight dynamics.** PX4/MAVROS attitude control, setpoint tracking, motor mixes, battery physics (`battery_level_ - 0.1f` is a countdown, not electrochemistry). Below the opcode boundary; the quilt has no opinion and no help.
- **Perception quality.** VSLAM drift and detector false positives are perception problems. The tier law *fences* a wrong-but-confident detector; it does not make the detector right. A good fence around a bad eye is a well-governed mistake.
- **Key distribution.** Chain-tip identity needs a bootstrap binding (`qm_bind`) that itself needs real asymmetric crypto and a ceremony. The quilt moves the trust anchor; it does not delete it.
- **Hardware-level attacks.** GPS spoofing at the RF layer, firmware supply chain, physical capture of a drone (a captured drone's journal is readable — there is no forward secrecy in a mesh journal).
- **The repo's own placeholder-ness.** `target_detector.py` publishes a hardcoded detection; `vslam_node.py` is a random walk; nothing has flown. All mappings above are claims about *structure*, and structure is the only thing this commit contains.

---

## 8. First three falsifiable steps (cheapest first, pre-registered)

All three are desk/simulation work against DUG's own `tactical_swarm.launch.py` — no drone, no radio, no purchase. Pass/fail written before running, boat-doc style.

| Step | Question | Pre-registered pass/fail | Cost |
|---|---|---|---|
| **DQ-1: election determinism harness** | Extract `select_leader` into an offline harness fed by recorded SwarmState traces from the sim. Baseline: count split-brain ticks (≥2 nodes `is_leader_ == true` simultaneously) and leader churn over ≥10 k ticks, including ±1 s clock skew and 1 s message staleness — the code's own real operating conditions. Then run the integer-rank election over the *same* journal bytes at common ticks. | Pass: integer variant produces 0 split-brain ticks and a leader sequence that is a pure function of the journal prefix (identical across 10 replays); DUG baseline churn is recorded as the number to beat. Fail: integer variant still split-brains on torn tails *or* churns ≥ baseline — then the thesis dies at the prefix-divergence rider in §2.3 and gets booked. | an evening, laptop |
| **DQ-2: swarm journal + torn-tail replay (BQ-1 transplant)** | Journaling shim on `/swarm/*` topics in sim; every SwarmState (sent, received, *and rejected*) appended per-drone with hash chain. Inject kill -9 mid-journal and synthetic 10/30/50 % SwarmState drops (the RF stand-in). After suffix sync, replay all journals and rebuild the swarm view. | Pass: replay reproduces the swarm view and full leader sequence **byte-exactly** for every loss pattern — the BQ-1 canary with RF loss instead of a kill switch; rejected-forger entries survive as journaled evidence. Fail: any divergence between the healed view and the no-loss ground truth at any tick. | a weekend, laptop |
| **DQ-3: tick-fenced command gate (red-team canary)** | Ship the smallest safety change with the largest payoff: `FormationState`/`KamikazeCommand` carry `(chain_tip, tick)` + MAC over the body (§5 construction); receivers reject `tick ≤ last_seen` and bad MACs. Red-team script throws spoofed, field-tampered, and replayed `armed=true` at both baseline and gated builds. | Pass: gated build arms on **0/3** attack classes while baseline arms on 3/3 (spoof with the repo's PSK, tamper-then-keep-signature, replay inside the 30 s window — all three must be demonstrated *against the baseline first* to prove the red team is real). Fail: any attack class arms the gate. | a weekend, laptop |

DQ-1 before DQ-2 before DQ-3: each builds on the previous artifact (traces → journals → gated commands), and none needs more hardware than the laptop the sim already runs on. The silicon thesis (§6) is deliberately excluded — it has no step until DQ-1/2 have receipts.

## 9. Open questions

| # | Question | Why it matters |
|---|---|---|
| 1 | Journal growth: entries/s × mission hours on a companion computer's flash — what's the rotation policy? | same q2 as the boat; drones have less disk than laptops |
| 2 | Can ROS2 QoS settings even deliver the "same bytes on every node" precondition, or do we journal below DDS? | determinism claims are void if the transport reorders silently |
| 3 | Does chain-tip identity degrade gracefully when a drone genuinely reboots (fresh journal, old tip)? | rejoin protocol: grandfathering vs re-binding decides whether recovery is an outage or a re-ceremony |
| 4 | Human-on-the-loop co-sign for irreversible effects: what is the minimal two-person rule for `arm()`? | §4.1's real fix is procedural + cryptographic; the shape needs deciding before DQ-3's gate is "done" |
| 5 | If NQ-C3-style twins work for the formation loop, what's the flight-code twin's drift budget when the compiler differs? | §6's deferred thesis; zero-action until DQ-1/2 pass |

---

*Next artifact: DQ-1's harness and its baseline churn number, or a booked reason it didn't run. Either is a result — same rule as the forge and the boat.*
