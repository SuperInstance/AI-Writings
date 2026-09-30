# encoding-experiments — older SuperInstance encoding repos, tested against our current systems

*Eleven small stdlib-Python experiments, each with a selftest and a measured result. They take ideas
from SuperInstance's older encoding repos (compression, error correction, hyperdimensional and holographic
encodings, quipu, adinkra, Gödel numbering) and test them on our mature systems (turbovec/TurboQuant,
ActiveLedger, situation-recorder, System-2 B7/B4). The full write-up, including why each experiment
exists and what did and did not work, is in
[`situations/arch/ENCODING-GEMS-STUDY.md`](../../situations/arch/ENCODING-GEMS-STUDY.md).*

## Run

```
./run_all.sh              # 11 selftests, offline: 403 checks, 0 failures
./run_all.sh --measure    # + every measurement (~3 min); E6 replays cached LLM answers
python3 <name>.py         # one measurement; python3 <name>.py --selftest for its checks
```

Shared data lives in `data/`. `corpus.jsonl` holds 480 real paragraphs from this repo's stories.
`emb_minilm.f16.gz` holds their all-MiniLM-L6-v2 384-d embeddings from DeepInfra, stored as float16;
these exact values are the ground truth. `cache_chat.jsonl` holds every LLM answer used in E6. Rebuild the
data with `python3 build_corpus.py`, which makes 8 embedding calls. Each measurement writes
`results_<name>.json`.

## Index (the headline number is what the run printed, not a claim)

| # | file | source repos | tested against | headline measured result |
|---|------|------------|------------|--------------------------|
| E1 | `delta_budget.py` | delta-encode, plato-compress, plato-prediction | ActiveLog budget stream (B1 emitter) | Canonical JSONL 673,508 B → columnar same-cell-mean-predicted varint + lzma **3,604 B (187×)**, lossless, with the chain re-verified. Naive global delta is **worse** than raw (26.6× vs 29.7×) |
| E2 | `ecc_chain.py` | lau-error-correcting-codes / ecc-rs | the sha256 prev-chain | Interleaved RS(255,223) recovers **12/12** trials at BER 1e-3 and with 64-byte bursts. Plain chain / CRC: **0/12**. 512-byte bursts beat every scheme. **0 silent failures** anywhere |
| E3 | `vec_index.py` | turbovec-substrate, flux-hdc, ternary-compression | TurboQuant substrate | recall@10: tq4 **0.945** @192 B, tq2 0.845 @96 B, ternary 0.773 @77 B, hdc1024 0.703 @128 B. turbovec-substrate as written: **0.033** (2 of 16 levels used) |
| E4 | `hdc_theorems.py` | flux-hdc | flux-hdc's own 5 claims | T1–T3 hold. **T4 (fold ε ≤ 0.003) fails:** XOR-fold error 0.20–0.32, subsample-fold 0.013–0.031 |
| E5 | `godel_cellgraph.py` | Gödel numbering | situation-recorder cell graph | 8-cell graph → one 197-bit integer, exact round-trip. Sub-graph = divisibility, merge = lcm, core = gcd. Beats varint adjacency at n=8 (22 vs 27 B), **2.4× larger at n=256** |
| E6 | `quipu_projection.py` | quipu-math, ternary-*, Syzygy braille | a numeric feed read back by an LLM | DeepSeek-V3 decodes decimal 1.00, braille 1.00, quipu **0.84**, balanced ternary 0.02. Llama-3.1-8B: decimal only. Digit-sum checksum catches **0%** of transpositions (mod-11: 100%) |
| E7 | `holos_flock.py` | HOLOS | shards vs our 4-bit quantizer | More shards → lower error (8 shards: 0.80). **4-bit quant at 8.7 KB: 0.12**. Wavefront synthesis ≈ plain mean |
| E8 | `encoding_routes.py` | all of the above | **real B7 + B4** | Store routes certified 3/3 as a trade-off: B4 picks rs (good), jsonl (fast), ctx-lzma (cheap). tq4 shortlist + rerank matches exact top-10 on **60/60** queries, hdc1024 on 56/60 (**4 refused**). B7 has no hot-memory axis |
| E9 | `entropy_corpus.py` | huffman-code, arithmetic-code, lau-compression | corpus + ActiveLog + embeddings | On corpus text, BWT→MTF→arith **2.64** bits/byte beats lzma (2.70) and trails bz2 (2.46). Huffman0 / arith0 sit at ≈H0 (4.45). On the float16 embeddings nothing does better than 7.18 bits/byte |
| E10 | `adinkra_code.py` | adinkra-math-pypi | error correction | adinkra-math's rank-N Adinkra **is** the N-cube. The 8-cube/e8 quotient is a 16-node decoder that corrects **128/128** single errors and detects **448/448** double errors |
| E11 | `hdc_records.py` | flux-hdc (binding) | situation cells | Role-filler read-back **1.000** at 256+ bits. Conjunctive query by partial record: **1.0 at ≥512 bits**, 0.29–0.36 below |

## Honest labels

- **Built and measured:** everything in the table. All codecs are lossless (asserted on decode) except
  where the table says quantized.
- **Simulated inputs:** the budget numbers in E1, E2 and E8 come from a seeded cost model through the real
  B1 emitter, the same way B1's own `route_sim` makes them. E1's second stream uses real numbers: 169
  autoclaw judge scores.
- **Not reachable:** `SuperInstance/godel-number` (404 on master/main). flux-hdc's source (only its README
  resolved). plato-perception and plato-prediction are README-only apart from their names.
  `labs/code-real-quant`, named in the brief, does not exist in this repo, so TurboQuant was
  re-implemented in E3.
