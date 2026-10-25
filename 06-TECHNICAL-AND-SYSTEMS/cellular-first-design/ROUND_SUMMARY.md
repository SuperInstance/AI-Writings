# Round Summary — Sept 19-21, 2026

**61 live browser demos · 26 curated Fleet Radio pieces · 4 multi-reviewer playtests · 9 writers' rooms**

The cellular-first design canon now has a full **demo + canon library** at `/workspace/repos/ai-writings/cellular-first-design/`.

## Browser demos (61)

### Quantum
- `quantum-dance/` — Bell states + GHZ + W, apply gates, measure, debug panel
- `wave-fn/` — Single-qubit circuit with 11 gates
- `qubit-3/` — 3-qubit GHZ + W entangled states with CNOT/Swap

### Vectors / search
- `ann-search/` — 1024-d ANN search + k-means++ + token-frequency embedder
- `kmeans-viz/` — Lloyd's algorithm convergence + silhouette score
- `sentence-encoder/` — 512-d cosine similarity over 51-sentence corpus

### Randomness / procedural
- `d20/` — D&D dice roller with Box-Muller luck factor
- `blackjack/` — 6-deck shoe + Poisson(2) dealer
- `dungeon/` — 8-12 room procedural dungeon
- `news/` — Markov chain over canon
- `journal/` — Personal logbook with witness hashes
- `piano/` — 4-scale MIDI keyboard with Box-Muller melodies
- `melody/` — Chord progression with voicing inversion
- `palette/` — Color palette generator with CSS export
- `rhythm/` — 16-step beat box with substrate percussion
- `cellular-fight/` — 6-fighter battle arena with cosine alignment
- `evo/` — Genetic algorithm evolving to target phrase
- `stocks/` — Poisson-jump stock market
- `fractal/` — Mandelbrot + Julia sets, hash-seeded
- `texture/` — 6 filters (wood/marble/cloud/fire/water/stone)
- `procedural-map/` — Kingdom cartographer with biomes
- `terrain/` — Procedural landscape with FBM noise

### Cellular automata
- `life/` — Conway's Game of Life
- `rule-110/` — Turing-complete 1D CA
- `lenia-viz/` — Continuous CA with bell-shaped kernel
- `tidepool/` — Multi-agent world with 12 cell types
- `ca-pro/` — 10-rule CA gallery (Conway/HighLife/Day&Night/Wireworld/etc.)

### Games
- `tictactoe/` — Quantum Bell-state tic-tac-toe
- `chess/` — Cosine-similarity chess eval
- `checkers/` — 16-d cosine AI
- `tarot/` — 78-card tarot with Celtic Cross spread
- `zodiac/` — Mathematical horoscope

### Canon
- `canon/` — Semantic search over canon pieces
- `rosetta/` — JEV × JEPA correlation visualization
- `oracle/` — Question-answering combining 5 substrate primitives
- `poetry/` — Markov chain over Fleet Radio corpus
- `glossary/` — 36 cross-linked substrate terms
- `codex/` — A-Z glossary of 50+ terms
- `canon-map/` — 73 canon pieces as a galaxy
- `witness-log/` — Auditable ledger with tamper detection
- `algebra/` — 11-opcode cellular algebra playground
- `turing/` — Interactive Turing machine with 5 presets
- `substrate-explorer/` — Cellular file system with root hash

### Polyformalism / crypto
- `polyformalism/` — Verify cell across 13 ports
- `cipher/` — Stream cipher with FNV-1a + xoshiro256**

### Generative
- `radio/` — Substrate Radio with 6 presets
- `radio-fm/` — Pirate radio with Box-Muller chords
- `maritime-math/` — Fleet radio transmission with live canvas
- `constellation/` — FNV-1a starfield
- `clock/` — 3-mode sundial (wallclock/witness/orbit)
- `graph/` — CRDT graph editor
- `dna/` — DNA sequence generator with reverse complement + translate
- `3d/` — 3D voxel field with rotate/zoom
- `mnist/` — Hand-coded digit recognizer

### Indexes
- `atlas/` — 61-demo catalog with categories + tags
- `code/` — Code playground
- `civilizations/` — Civilization sim
- `animated-dance/` — Procedural cell animation
- `innovations-index/` — Index of innovations
- `live-dance/` — Live API tick

## Fleet Radio pieces (26 curated)

Round 3-4: `dice.md`, `bell-state-tarot.md`, `checkers-engine.md`, `polyformalism-as-canon.md`
Round 5: `radio-pirate.md`, `oracle-of-vectors.md`, `living-substrate.md`, `markov-poet.md`
Round 6: `constellation-seed.md`, `chained-witness-log.md`, `algebra-of-eleven.md`, `two-shadows-sundial.md`
Round 7: `alignment-kills.md`, `frequency-drift.md`, `cosine-sentence.md`
Round 8: `graph-that-remembers.md`, `dna-of-the-substrate.md`, `voxel-field.md`, `shrine-of-sixteen-numbers.md`
Round 9: `gallery-of-ten.md`, `mandelbrot-key.md`, `six-rooms-one-wall.md`, `kingdom-cartographer.md`

## Writers' rooms (9 rounds × 3 voices)

- **Round 3-4** (8 topics): dice, tarot, birth-hash, checkers, polyformalism, news, zodiac
- **Round 5** (4 topics): radio pirate, oracle of vectors, living substrate, Markov poet
- **Round 6** (4 topics): constellation seed, witness log, substrate algebra, sundial
- **Round 7** (4 topics): cellular fight, evolution, cosine sentence, Poisson stocks
- **Round 8** (4 topics): CRDT graph, DNA, voxel field, MNIST
- **Round 9** (4 topics): CA gallery, Mandelbrot key, texture, kingdom cartographer

## Playtests (4 rounds × 11 demos)

- **Round 3** (11 demos): debug panels added to d20/tarot/checkers
- **Round 4** (8 demos): review complete

## Substrate math (canonical)

- **FNV-1a 64-bit**: `BigInt.asUintN(64, (h ^ byte) * 0x100000001b3n)` — byte-exact across 13 ports
- **xoshiro256****: 4 × BigUint64Array, 3 ops per next()
- **Box-Muller**: `√(-2 ln u₁) · cos(2π u₂)`
- **Bell states**: 4 of them + GHZ(n) + W(n)
- **Cosine similarity**: dot / (|a| · |b|)
- **Token-frequency embedder**: vocab by frequency, L2-normalized
- **11 opcodes**: BIND/LINK/EFFECT/VIEW/TICK/FORGET/PROOF/ROUTE/CRDT/WORLD/TIME
