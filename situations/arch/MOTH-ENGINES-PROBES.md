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
