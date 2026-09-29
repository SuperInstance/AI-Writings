# Moth engine probes — non-QRNG engines, run live 2026-09-29

Each probe: `POST /engines/{id}/process {"params":{…}}` → `202 {job_id, status:"queued"}` → poll
`GET /jobs/{id}/status` every 2 s → `GET /jobs/{id}/result`. All four finished in ~4 s (Aer simulator).
Result envelope is always `{"result": …}`, but the **inner shape differs per engine** (see each section).
Inventory: [MOTH-ENGINES.md](MOTH-ENGINES.md).

## coin-toss-v1 — works (2 credits)

Params: `{"shots":16,"mode":"emu"}` (`mode` `emu`|`qpu`; `qpu` queues on real IBM hardware — not tried).
Job `d59b57ec-f3da-4c26-bfa4-e95635ed56f9`. Status carries a `steps` list (build → submit → collect → format).
Result (flat, no `output` wrapper for counts):

```json
{"result":{"backend":"aer","heads":5,"ibm_job_id":"b800c457…","mode":"emu","output":"tails","shots":16,"tails":11}}
```

`output` is the majority side. Emulator mode, so this is simulated randomness, not a hardware draw.

## blur-core-v1 — works (1 credit)

Quantum blur on any N-D grid of non-negative numbers. Key params: `values` (nested array), `strength`
(0–1, float or per-axis list), `reach` (0 local … 1 non-local), `axes`, `shots` (omit = exact), `max_qubits` (≤24).

- `{"values":[0,0,0,8,0,0,0,0],"strength":0.1}` → job `8e662b73-5c80-4106-9fe9-f78571c5bd54`:
  `{"result":{"output":[0,0,0.2007,8,0.2007,0.0050,0,0]}}` — the spike leaks into its neighbours
  (and a little into index 5: the blur walks qubit/bit neighbours, not just ±1).
- `{"values":4×4 grid with one 9,"strength":0.5}` → job `c85a57a6-6fc3-4c1a-a419-bbf1fffb073c`:
  every cell ≈ 9. At 0.5 a single delta is fully spread; output is rescaled so its max matches the input max
  (sum is **not** conserved).

Same shape as input, returned under `result.output`. Useful as a deterministic (exact mode) "quantum smear" for any array.

## qpixl-v1 — works (1 credit), after a doc mismatch

Encodes a list/grid of values into a quantum state (QPIXL), runs it, reads it back. Params: `values`,
`machine` (`aer` or a `fake_<chip>` noisy emulator), `shots`, `discretize`, `dynamic_range`, `mode` `emu`|`qpu`.

- The engine's own code sample sends `"values":"0.05,0.2,…"` — that **fails** (job `05e9e10d-…`,
  `unparseable_values`: string must be wrapped in `[..]`). The result endpoint then returns `409 job failed and produced no result`.
- A JSON array works: `{"values":[0.05,0.2,0.4,0.6,0.8,0.95],"machine":"aer","shots":1024}` →
  `{"result":{"backend":"aer","ibm_job_id":[],"output":[0.05,0.19995,0.42383,0.60392,0.80346,0.95],"qpu_seconds":0}}`

The round-trip is lossy by shot noise (0.4 → 0.424) — that noise is the effect. `fake_<chip>` should add device noise (not tried).
