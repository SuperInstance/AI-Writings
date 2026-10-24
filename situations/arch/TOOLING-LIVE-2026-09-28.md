# Tooling, live — verified JEV + Moth schemas & first insights (2026-09-28)

*Owner rotated both keys and said: use them a lot; project JEV around a problem in an
increasingly **decomposing** way so the logic becomes visual while the entangled relationships
abstract; iterate Moth until it surprises you, then crank usage to find the systemization.
These are the first verified results on the rotated keys. Ground truth for the situation designs.*

## JEV — `POST https://api.typesafe.ai/v1/systemone` (LIVE on rotated key)
Request shape (verified):
```json
{ "model": "jev-latest",
  "state": "<the text under judgment>",
  "questions": { "<name>": { "type": "noul|score|choice",
                             "question": "…",
                             "criteria": {"true":"…","false":"…"} } } }
```
Response: `{ model, answers:{ <name>:{ noul|score|confidence|value } }, usage }`.

### First insight — the decomposing fold *localizes* what the whole verdict *abstracts*
A compound claim (four sub-claims, one subtly false — "the heart is located **entirely** on the
left side"):
- `noul(WHOLE)` = **0.11** — JEV knows the compound is false, but the whole verdict says only *that*, not *where*.
- decomposed: `0.98 / 0.97 / 0.95 / **0.08**` — the fold **pinpoints the false part**.
- `FOLD(min)` = 0.08, `FOLD(product)` = 0.072 vs `WHOLE` = 0.11.

**The principle, confirmed:** projecting `noul` across a decomposition turns an opaque scalar
verdict into a *located* one. The whole is a shadow; the fold is a map. This is the seed
mechanic for the playable situations — decompose until every leaf is a confident (high-|noul−0.5|)
verdict; the tree of nouls IS the visual logic; the divergence `whole − fold` measures how much
the entanglement was hiding. (Prior finding still holds: pairwise **choice ≫ independent noul**,
and JEV is confidently wrong only on character-counting — buy a symbolic reader there, per G21.)

## Moth — `{$MOTHQUANTUM_BASE}` = `…/api/v1` (LIVE on rotated key)
Two gotchas, both solved: (1) **must send a browser `User-Agent`** or Cloudflare blocks with
error 1010 (bot-fingerprint) before the request reaches Moth; (2) key still needs the trailing
newline trimmed. Then `GET /engines` → 200 (32 engines).

`comet-qrng-v1` — synchronous-ish (`is_async:false`, `execution_mode:"steps"`, 5 credits/run):
```
POST /engines/comet-qrng-v1/process   {}          # empty body = defaults (works!)
  -> 202 { job_id, status:"queued" }
GET  /jobs/{job_id}/status  -> {status:"completed"}   (~12 s)
GET  /jobs/{job_id}/result  -> { result:{ output:{ bell_witness{…}, … } } }
```
`params_schema` (the real param names — NOT num_qubits/output_bytes): a `Derivation` with
`floats` (N uniform doubles in [0,1), 53-bit mantissa, ≤100000) and `integers`
(`{min,max,count}`, rejection-sampled), plus `backend_name`, etc. So you ask for *derived*
randomness directly.

### First insight — it surprised me (the "it's starting to work" signal)
The default run returned a **CHSH Bell witness S = 2.86** (classical bound = 2; qubits 12–15,
~4096 shots/setting, per-correlator σ≈0.011) with an SP 800-90B min-entropy certificate +
Toeplitz extractor. S > 2 is a genuine device-level entanglement signature — randomness no
classical source can forge. Honest caveat carried by the engine: fixed settings, no space-like
separation → it witnesses gate+readout fidelity, *not* device-independent certification. Still:
this is the un-gameable dice the situation designs want — a draw whose provenance is physics.

## What this unlocks (for the situation designs)
- **JEV** = the located verdict (decomposing fold → visual logic).
- **Moth** = the un-gameable draw (curriculum/cast/seed nobody can steer) + a real quantum
  surprise to anchor "is this working?".
- Next: Opus 5.5 designs *playable quilt situations* that project these in a decomposing way so
  that **playing them finds the answer** to an untested subject (see the mobilization dispatch).
