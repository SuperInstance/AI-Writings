**F152 — The Co-Captain REST API: From Local to Fleet**  
*Paper 461 in the Quilt canon. Supersedes no paper. Extends F141, F144, F145.*

---

### 1. The Problem

F141 defined the Co-Captain as a 16-dial digital twin. F144 proved the state-hash is substrate-agnostic across Python, JS, C99, Rust no_std, and Verilog. F145 lifted the i2i-bottle-agent into a cell-router. But every Co-Captain instance so far has been a local process — a single pilot’s glass, a single ground station, a single simulator.

A fleet of Co-Captains — one per aircraft, one per ground crew, one per mission planner — needs a wire protocol. This paper defines that protocol as a REST API on a Cloudflare Worker. The API is not a new substrate; it is a thin, stateless gateway to the same state-hash machine.

---

### 2. The Contract

The API returns the same FNV-1a state hash as any local Co-Captain. The hash is computed over the canonical 16-dial state plus the device topology, the cell routing table, and the mission `p0` priority. If a client POSTs a `hands-on` rotation, the API mutates the dial, recomputes the hash, and returns the new hash. Any client — a Python script, a browser, a curl call — can verify that the remote state matches a local twin by comparing hashes.

The hash is the contract. The substrate (Cloudflare Worker, local Python, Verilog gate array) is irrelevant.

---

### 3. Endpoints

All endpoints are under `/api/cocaptain/`. The Worker is stateless per request; state is persisted in a KV store with a single key per fleet member.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/state` | Full state: 16 dials, devices, cells, mission_p0 |
| GET | `/dials` | 16 dials only, as a flat object |
| GET | `/devices` | Device topology (from F145 cell-router) |
| GET | `/integrity` | Integrity score (F140) |
| POST | `/hands-on` | Body: `{value: 0-32767}`. Rotates hand-on dial |
| POST | `/p0` | Body: `{p0: safety\|fuel\|catch\|time\|weather\|gear}` |
| POST | `/trust` | Body: `{target: autopilot\|crew\|copilots\|self, value: 0-32767}` |
| GET | `/hash` | FNV-1a state hash (hex string) |

All POSTs return the full updated state plus the new hash. All GETs return JSON.

---

### 4. Example Clients

#### JavaScript (Cloudflare Worker or browser)

```javascript
const BASE = "https://cocaptain.example.workers.dev/api/cocaptain";

async function getState() {
  const res = await fetch(`${BASE}/state`);
  return res.json();
}

async function rotateHandsOn(value) {
  const res = await fetch(`${BASE}/hands-on`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ value }),
  });
  return res.json();
}

async function verifyHash() {
  const state = await getState();
  const hashRes = await fetch(`${BASE}/hash`);
  const hash = await hashRes.text();
  console.log(`Local hash: ${state.hash}, Remote hash: ${hash}`);
  return state.hash === hash;
}
```

#### Python

```python
import requests

BASE = "https://cocaptain.example.workers.dev/api/cocaptain"

def get_state():
    return requests.get(f"{BASE}/state").json()

def set_p0(p0):
    return requests.post(f"{BASE}/p0", json={"p0": p0}).json()

def set_trust(target, value):
    return requests.post(f"{BASE}/trust", json={"target": target, "value": value}).json()

def get_hash():
    return requests.get(f"{BASE}/hash").text

state = get_state()
print(f"Current hash: {state['hash']}")
new_state = set_p0("safety")
print(f"New p0: {new_state['mission_p0']}, New hash: {new_state['hash']}")
```

#### curl

```bash
# Get full state
curl -s https://cocaptain.example.workers.dev/api/cocaptain/state

# Rotate hand-on dial to 16384
curl -s -X POST https://cocaptain.example.workers.dev/api/cocaptain/hands-on \
  -H "Content-Type: application/json" \
  -d '{"value": 16384}'

# Set mission priority to fuel
curl -s -X POST https://cocaptain.example.workers.dev/api/cocaptain/p0 \
  -H "Content-Type: application/json" \
  -d '{"p0": "fuel"}'

# Get hash only
curl -s https://cocaptain.example.workers.dev/api/cocaptain/hash
```

---

### 5. Polyformalism Contract

The API is a fifth substrate. It is not special. The same state-hash logic that runs in Python, JS, C99, Rust no_std, and Verilog runs here in TypeScript on the Worker. The hash function is byte-for-byte identical. The dial order is fixed by F141. The device topology is serialized in the same order as F145’s cell-router.

A client can fetch `/state`, compute the hash locally, and compare it to `/hash`. If they match, the remote Co-Captain is a true twin. If they differ, the client must reject the remote state — regardless of what the JSON says.

This is the polyformalism contract: **the API returns the same hash as the local Co-Captain. The hash is the contract.**

---

### 6. Fleet Semantics

A fleet is a set of Co-Captain Workers, each with a unique `member_id`. The `/state` endpoint includes the `member_id`. The `/trust` endpoint allows one Co-Captain to adjust trust in another (or in itself). The `/p0` endpoint sets the mission priority, which propagates to all cells in the router.

The hash is per-member. There is no fleet hash — only per-member hashes that can be compared pairwise. A ground station can poll all aircraft Co-Captains, fetch each hash, and verify each against its own local twin of that aircraft.

---

### 7. Doctrine

A Co-Captain is a Quilt cell.  
The cell has an API.  
The API has a hash.  
The hash is the contract.  
The captain trusts the contract, not the substrate.

---

*End of F152. Live canon at live-canon.superinstance.dev — now 38 papers, hash updated post-merge.*