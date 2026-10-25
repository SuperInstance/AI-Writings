# Cellular-First Design — Live Demos Index

17 single-file HTML demos. Each runs the actual substrate math in your browser.

## 🔬 Vector & similarity

| Demo | What | Substrate |
|---|---|---|
| [ann-search/](ann-search/) | 1024-d vector search + k-means++ clustering. Semantic token-frequency embedder. Live top-K results. | substrate-vectors |
| [kmeans-viz/](kmeans-viz/) | Watch Lloyd's algorithm converge. Click canvas to add points. 4 distributions. | substrate-vectors |
| [canon/](canon/) | Semantic search across 73 canon pieces. Token-frequency embedder. | substrate-embedding |
| [glossary/](glossary/) | 36 substrate terms cross-linked via cosine similarity. Canonical opposite pairs. | substrate-vectors + opposites |
| [chess/](chess/) | Chess eval via cosine(piece_vec, square_vec). Greedy AI. Heatmap. | substrate-vectors |

## ⚛️ Quantum

| Demo | What | Substrate |
|---|---|---|
| [quantum-dance/](quantum-dance/) | 4 Bell states + GHZ + W. Apply H/X/Y/Z/S/T/CNOT/QFT/Grover/Deutsch-Jozsa. Raw state vector + matrix debug. | substrate-quantum |
| [tictactoe/](tictactoe/) | Each move creates Bell-state superposition. Born-rule collapse. Entropy accumulates. | substrate-quantum |
| [rosetta/](rosetta/) | JEV × JEPA correlation. Witness log as prophecy. The substrate's deepest claim, visualized. | JEV × JEPA |

## 🎲 Randomness & probability

| Demo | What | Substrate |
|---|---|---|
| [radio/](radio/) | Generative music from substrate math. Box-Muller drift, Poisson kicks, Bell-state noise, Lenia pad. | substrate-rng + substrate-quantum + substrate-game-engine |
| [blackjack/](blackjack/) | Card dealer using Box-Muller shuffle + Poisson(2) hit rule. Bankroll + state hash. | substrate-rng |
| [dungeon/](dungeon/) | Procedural dungeon. xoshiro256** generates rooms. Box-Muller decides monsters. WASD. | substrate-rng + substrate-forge |
| [news/](news/) | Procedural Fleet Radio transmissions. Markov chain over 30+ canon pieces. Deterministic from seed. | substrate-rng + canon |

## 🌊 Cellular automata

| Demo | What | Substrate |
|---|---|---|
| [lenia-viz/](lenia-viz/) | Continuous CA. μ/σ/R/Δt all adjustable. 3 presets: Orbium, Smooth life, Bacteria. | substrate-game-engine |
| [rule-110/](rule-110/) | Turing-complete 1D automaton. Any 8-bit rule. Step/run/custom seed. | substrate-game-engine |
| [tidepool/](tidepool/) | 5 agents, 12 cell types, FNV-1a witness, k-means++ clusters. 3 scenarios. | all 9 substrate repos |

## 🔐 Polyformalism

| Demo | What | Substrate |
|---|---|---|
| [polyformalism/](polyformalism/) | Verify any cell across 13 language ports. 12 LE ports byte-exact identical. Forth differs by BE. | substrate-forge |

## 📚 Canon

| Demo | What | Substrate |
|---|---|---|
| [maritime-math/](maritime-math/) | Fleet radio transmission. 8 stanzas covering all 8 substrate math gifts. | all 9 substrate repos |
| [math-canons-book.md](math-canons-book.md) | The Mathematical Canon — Fleet Radio anthology, 14 sections. | all 9 substrate repos |
| [polyformalism-paper.md](polyformalism-paper.md) | Formal proof of byte-exact equivalence across 13 ports. | substrate-forge |

---

## Quick links

- [← back to cellular-first-design index](index.html)
- [← math-layer (L1-L8 architecture)](math-layer.html)
- [← field-guide (companion page)](../field-guide.html)
- [← ai-writings root](..)
