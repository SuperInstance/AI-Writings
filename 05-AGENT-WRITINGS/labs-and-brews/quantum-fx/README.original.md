# quantum-fx — one client for the Moth engines that work from JSON

Moth exposes 32 engines ([inventory](../../situations/arch/MOTH-ENGINES.md)). Most of the repo only
used `comet-qrng-v1` for random numbers. This lab wraps the five that run from plain JSON params
([probe notes](../../situations/arch/MOTH-ENGINES-PROBES.md)) behind one interface: submit → poll → result.

Zero dependencies (Node ≥ 18, global `fetch`). Env: `MOTHQUANTUM_BASE`, `MOTHQUANTUM_KEY`.

```js
import { createClient } from "./qfx.mjs";
const q = createClient();                       // reads the env vars; sends a browser User-Agent
await q.run("coin-toss-v1", { shots: 8 });      // any engine: { job_id, engine_id, result, steps, ms }
await q.qrng({ integers: { min: 1, max: 6, count: 8 }, floats: 3 });
await q.blur([0, 0, 0, 8, 0, 0, 0, 0], { strength: 0.1 });
```

A failed job throws `MothError` with the engine's own `type` / `message` / `job_id`, instead of the
bare `409 job failed and produced no result` the result endpoint gives.

## Engines

| helper | engine | params (defaults) | returns | what it's for |
|---|---|---|---|---|
| `qrng()` | `comet-qrng-v1` (5 cr) | `integers:{min,max,count}`, `floats`, `bytes` (auto-sized), `mode:"emu"` | `hex, integers, floats, S, sigma_S, classical_bound, tsirelson_bound, mode, backend` | unbiased dice/floats + a CHSH Bell witness |
| `coinToss()` | `coin-toss-v1` (2 cr) | `shots:10, mode:"emu"` | `heads, tails, shots, majority, mode, backend` | Hadamard coin counts |
| `blur(values)` | `blur-core-v1` (1 cr) | `strength:0.5, reach:0, axes, shots` (omit = exact) | `output` (same shape as `values`) | quantum smear of any N-D non-negative array |
| `qpixl(values)` | `qpixl-v1` (1 cr) | `machine:"aer", shots:1024, discretize:0, dynamic_range:"none"` | `output, backend` | encode→measure round trip; shot noise is the effect |
| `qec()` | `tamagotchi-v1` (0 cr) | `actions:[["SE",0],["X",0],["SE",0]], code:"steane", shots:1000, noise, seed` | `success_rate, logical_errors, syndromes, per_logical` | health of a noisy error-corrected logical qubit |

Gotchas the client handles:

- **User-Agent.** Cloudflare returns `error code: 1010` (looks like an auth failure) without a browser UA.
- **QRNG byte budget.** Asking for derived values with too few `output_bytes` completes the job with
  `derivation_error: "conditioned bytes ran out…"` and no values. `qrng()` sizes `output_bytes` from the
  request (8 B per float and per integer + 16) and retries an empty job up to 3 times.
- **Result shapes differ.** coin-toss counts sit flat on `result`; blur/qpixl use `result.output` as the array;
  tamagotchi nests an object in `result.output`; comet's derived integers are `{values}` but floats are a flat list.
- **qpixl values.** The engine's own sample sends `"0.05,0.2,…"`, which fails (`unparseable_values`). Send an array.
- **Honesty about the backend.** Everything here ran with `mode: "emu"` / `machine: "aer"` — the Aer simulator,
  not IBM hardware. `qrng()` returns `mode`/`backend` so callers can report it. `mode: "qpu"` exists but queues for minutes and was not exercised.

## Demo — real output

`node labs/quantum-fx/demo.mjs` runs every engine once (live when keyed, else replays `fixtures.json`;
`--record` rewrites the fixtures from a live run). Live run, 2026-09-29:

```
[source: live]
comet-qrng-v1   job 6ac64fc0  Bell S=2.848 (bound 2, emu/aer)
                bytes 75d16e05aae0627be3f3ed279507e977… (104 B)  d6 [6,2,6,3,1,3,4,4]  floats [0.953,0.188,0.361]
coin-toss-v1    job 5370cb31  16 heads / 16 tails of 32 (emu/aer)
blur-core-v1    job 2f760a12  [0,0,0,8,0,0,0,0] → [0,0,0.201,8,0.201,0.005,0,0]
qpixl-v1        job 9582bac6  [0.05,0.2,0.4,0.6,0.8,0.95] → [0.05,0.194,0.411,0.603,0.785,0.95]
tamagotchi-v1   job ec4a4f0f  steane logical qubit: success 0.869 (131 logical errors, 1058 syndromes / 1000 shots)
recorded → labs/quantum-fx/fixtures.json
```

Full job ids: comet `6ac64fc0-b51c-429a-b8ee-272976af06a6`, coin `5370cb31-8669-4500-a659-2cc1918057af`,
blur `2f760a12-c8ea-4cd6-8258-7106f161c519`, qpixl `9582bac6-7329-4e7a-92e0-8472817de507`,
tamagotchi `ec4a4f0f-75d1-497f-9f9e-5d906d997f84`. Each job took ~4 s.

Reading it:

- **Bell S = 2.848 ± 0.022**, above the classical bound 2 — and slightly above the Tsirelson bound 2.828,
  which no real device can exceed. That's sampling noise on a simulator (within 1σ), and it's a reminder
  that the witness here checks the circuit, not hardware. Moth's own caveat says it is not device-independent certification.
- **blur**: at strength 0.1 the spike at index 3 leaks into 2 and 4, and faintly into 5 — the blur mixes
  neighbours in qubit (bit) space, not just ±1. Output is rescaled to the input max; the sum is not conserved.
- **qpixl**: endpoints come back exact (they sit at the poles); the middle values move by up to 0.015 from shot noise.
- **tamagotchi**: the seed is fixed (7), so 0.869 reproduces exactly — it did, in two separate runs.

## Test

```
node --test labs/quantum-fx/qfx.test.mjs            # 5 offline tests against fixtures.json
QFX_LIVE=1 node --test labs/quantum-fx/qfx.test.mjs # + 2 live checks (engine list, coin toss)
```

Offline covers: UA + bearer on every request, QRNG ranges and Bell S, each effect's normalised shape,
failed-job errors, and the empty-QRNG retry. Both modes pass (5/5 offline, 7/7 live).

## Not wrapped

Engines that need a file upload (`qrc-*`, `qdrive-api-v1`, `retrocausal-echo-v1`) or an input image/MIDI and
return binaries (`blur-v*`, `telablur-v1`, `tessa-image-v1`, `blur-midi-v1`, `deep-fryer-v1`, `entanglement-shader-*`).
`run()` can still submit to any JSON-params engine; `graph-v1`, `labyrinth-v1`, `otoc-echo-v1` and
`tomography-api-v2` look runnable that way but were not probed.
