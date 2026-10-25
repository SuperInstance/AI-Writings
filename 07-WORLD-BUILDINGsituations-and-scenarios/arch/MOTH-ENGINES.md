# Moth engine inventory

Fetched live `GET /engines` on 2026-09-29 (count **32**). Per-engine detail from `GET /engines/{id}`.
Auth: `Bearer $MOTHQUANTUM_KEY`, base `$MOTHQUANTUM_BASE`; a browser User-Agent is required (Cloudflare error 1010 otherwise).

Class is my reading of the I/O types + description: **QRNG**, **quantum compute (JSON)** (JSON in, JSON out), **media/effect** (image/audio/MIDI/binary or multipart upload), **test/demo**.

| engine_id | name | in → out | credits | required params | class | description |
|---|---|---|---|---|---|---|
| `blur-core-v1` | Quantum Blur Core | application/json → application/json | 1 | — | quantum compute (JSON) | Apply a quantum blur to any N-dimensional grid of non-negative numbers. |
| `blur-midi-v1` | Blur Jazz | application/json → audio/midi | 1 | — | media/effect | Apply a quantum blur effect to a MIDI file. |
| `blur-v0` | Quantum Blur | application/json → application/octet-stream | 1 | — | media/effect | Apply a quantum blur algorithm to the image. |
| `blur-v1` | Quantum Blur | application/json → application/octet-stream | 1 | — | media/effect | Apply a quantum blur algorithm to the image. |
| `coin-toss-v1` | Coin Toss | application/json → application/json | 2 | — | QRNG-ish (coin toss) | Flip a quantum coin with a Hadamard gate and return heads and tails counts. |
| `comet-qrng-v1` | Comet Quantum RNG Engine | application/json → application/json | 5 | — | QRNG | Random bytes from Born-rule measurements on IBM hardware (or Aer baseline), with an SP 800-90B min-entropy certificate, Toeplitz extractor and CHSH witness. |
| `deep-fryer-v1` | Deep Fryer | application/octet-stream → application/octet-stream | 1 | — | media/effect | Gives images a blown-out, deep-fried meme look by scrambling hue and lightness through a quantum kernel circuit, tile by tile. |
| `demo-callback-v1` | Callback Bridge (Demo) | application/json → application/json | 0 | — | test/demo | Demonstrates bridging a library callback to update_progress — correct pattern for black-box libraries that expose iteration hooks |
| `entanglement-shader-v0` | Entanglement Shader | application/json → application/octet-stream | 1 | — | media/effect | Quantum iridescent BSDF generator. |
| `entanglement-shader-v1` | Entanglement Shader | application/json → application/zip | 1 | — | media/effect | Quantum iridescent BSDF generator. |
| `graph-v1` | Quantum Graph Engine | application/json → application/json | 5 | — | quantum compute (JSON) | Prepare a quantum graph state — your own couplings and correlations, or a random one — and sample it via Aer simulation (EMU) or an IBM QPU. |
| `labyrinth-v1` | Quantum Labyrinth Engine | application/json → application/json | 5 | — | quantum compute (JSON) | Turn a Backrooms level definition into a game-readable maze: a ZZ-correlated quantum graph sampled on Aer (EMU) or IBM QPU. |
| `otoc-echo-v1` | Quantum Echo | application/json → application/json | 1 | — | quantum compute (JSON) | Perturb a scrambled qubit chain, reverse it, and listen for what returns — a signed, complex multi-tap delay map. |
| `qdrive-api-v1` | QDrive | multipart/form-data → application/json | 1 | — | media/effect | Build a quantum circuit by specifying target expectation values instead of gates. |
| `qpixl-v1` | Qpixl | application/json → application/json | 1 | — | quantum compute (JSON) | An array encoded as qubit angles, decoded in a single measurement. |
| `qrc-audio-v1` | QRC Audio | multipart/form-data → audio/wav | 5 | — | media/effect | Sequence audio with a quantum reservoir — split a file into chunks, learn their order, and generate a new arrangement as one WAV. |
| `qrc-gen-v2` | QRC Generate | multipart/form-data → application/json | 1 | — | media/effect | Generate a sequence from a trained QRC model, reused by reference (train once, generate many). |
| `qrc-image-v1` | QRC Image | multipart/form-data → image/gif | 5 | — | media/effect | Train a quantum reservoir on a sequence of images (or continue one already trained) and generate a new sequence, rendered as an animated GIF. |
| `qrc-midi-v1` | QRC MIDI | multipart/form-data → audio/midi | 5 | — | media/effect | Sequence MIDI with a quantum reservoir — learn the notes of a file and generate a new arrangement as a fresh .mid. |
| `qrc-train-v2` | QRC Train | application/json → application/json | 5 | — | quantum compute (JSON) | Train a quantum reservoir on a token sequence and emit a reusable model artifact. |
| `retrocausal-echo-v1` | Retrocausal Echo | multipart/form-data → audio/wav | 2 | — | media/effect | A multi-tap delay whose tap map is measured on a quantum computer — negative returns invert, reverse or rotate the signal. |
| `tamagotchi-v0` | Tamagotchi | application/json → application/json | 1 | — | quantum compute (JSON) | Cute little thingy |
| `tamagotchi-v1` | Tamagotchi | application/json → application/json | 0 | — | quantum compute (JSON) | Cute little thingy |
| `telablur-v1` | Quantum Teleblur | application/json → application/octet-stream | 1 | — | media/effect | Morph one image into another through quantum rotation gates. |
| `tessa-image-v1` | Tessa Image | application/json → image/png | 1 | — | media/effect | Encode an image's colours as points on a sphere with the Tessa quantum encoder and read them back |
| `tessa-image-v1-test` | Tessa Image | application/json → image/png | 1 | — | test/demo | Encode an image's colours as points on a sphere with the Tessa quantum encoder and read them back |
| `test-binary-v1` | Test Binary | application/octet-stream → application/octet-stream | 0 | — | test/demo | Echo engine that accepts any binary file and returns it unprocessed |
| `test-engine-error-v1` | Test Engine Error | application/json → application/json | 0 | — | test/demo | Stub engine that always raises EngineError (for domain error testing) |
| `test-engine-fail-v1` | Test Fail Engine | application/json → application/json | 0 | — | test/demo | Stub engine that always fails (for retry/error testing) |
| `test-engine-submission-v1` | Test Engine Submission | application/json → application/json | 1 | — | test/demo | Hello world |
| `test-engine-v1` | Test Engine | application/json → application/json | 0 | — | test/demo | Stub engine that returns a dummy result after 3 seconds |
| `tomography-api-v2` | Tomography Api | application/json → application/json | 1 | circuit_qasm | quantum compute (JSON) | Simple core engine to compute relevant quantities of a quantum circuit |

**By class:** QRNG 1, QRNG-ish (coin toss) 1, media/effect 14, quantum compute (JSON) 9, test/demo 7

## Notes

- Every engine reports `is_async: false`, but submission still returns a `{job_id}` (existing labs code relies on this); results are fetched via `/jobs/{id}/status` → `/jobs/{id}/result`.
- `multipart/form-data` engines (QRC family, QDrive, Retrocausal Echo) need a file upload, not JSON params — out of scope for a JSON-only client.
- Several JSON-in engines emit binaries (`blur-v*`, `telablur-v1`, `entanglement-shader-*`, `tessa-image-v1`) and some of those expect an image/MIDI encoded inside params.
- Candidates runnable from pure JSON params: `coin-toss-v1`, `blur-core-v1`, `qpixl-v1`, `graph-v1`, `tamagotchi-v1`, `otoc-echo-v1`, `tomography-api-v2` (QASM string), `labyrinth-v1` (inline level).
- Probe results for the ones actually run are in [MOTH-ENGINES-PROBES.md](MOTH-ENGINES-PROBES.md).

