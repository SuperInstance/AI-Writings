# Encoding gems: what SuperInstance's older encoding repos do for the systems we run now

*A study, 2026-09-30, on branch `claude/encoding-gems`. It reads 23 public SuperInstance encoding repos
and runs 11 small experiments that apply their ideas to turbovec/TurboQuant, ActiveLedger,
situation-recorder, Syzygy's projection, and System-2 (B7/B4). The code is in
[`labs/encoding-experiments/`](../../labs/encoding-experiments/README.md): 403 selftest checks, 0
failures. Every number below was printed by a run in this session. Where a claim comes only from a
repo's README, the text says so. Voice: this reports results; it does not argue for any repo.*

---

## 1. In one breath

We tested old compression, error-correction and "exotic" encoding repos against the systems we run now.
**Three ideas paid off:**

- Predicting each value from the same cell's history, then lossless coding, makes the ActiveLog budget log **187× smaller**.
- **Reed–Solomon around that compressed log** lets the hash chain survive errors instead of only reporting them.
- A careful **4-bit TurboQuant** index keeps **0.945 recall@10** at 1/8 of the size, and with a rerank it returns *exactly* the right answer on every query.

Several READMEs promise more than their code does. We measured those gaps too; they are useful to know.

## 2. Why it exists

Casey asked for a deep study of the older ENCODING repos, looking for gems to combine with our current
systems, both in the obvious ways and in unexpected ones. Two problems motivated it:

- **Storage and integrity:** our ledgers grow, and the hash chain can detect a flipped bit but cannot repair it.
- **Vector memory:** `turbovec-substrate` claims 8× compression, but nobody had checked whether that compression keeps retrieval quality.

Before this study, each repo's claims rested only on its README. Now each claim either has a receipt or
has been shown not to hold.

## 3. The mental model

Five nouns:

- **Repo.** An older SuperInstance project. Most are one-module Rust or Python teaching libraries.
- **Gem.** The one idea in a repo that survives transplanting (for example, *predict, then code the residual*).
- **Mature system.** The thing we actually run: turbovec/TurboQuant, ActiveLog (B1), situation-recorder, Syzygy, System-2 (B7 gate + B4 chooser).
- **Experiment (E#).** A single-file runnable that combines one gem with one system and measures it. It has a `--selftest`.
- **Route.** An encoding viewed as a System-2 alternative. It must produce the *same product* as the plain version; after that, B7/B4 price it on the fast / cheap / good axes.

```
 repo ──(read README + source)──► gem ──(E#: smallest runnable)──► number
                                              │
                          mature system ◄─────┘  (does it help? what does it cost?)
                                              │
                          System-2 route ◄────┘  (same product? then B7 prices it, B4 picks when)
```

### The repos, one line each (read via raw.githubusercontent.com, master branch)

| family | repos | what they are (verified from README/source) |
|---|---|---|
| compression | `delta-encode`, `arithmetic-code`, `huffman-code`, `compress-huffman-rs`, `compress-lz77-rs`, `compress-rle-rs`, `run-length`, `lau-compression`, `ternary-compression`, `plato-compress` | Rust teaching crates. The ideas that transplant: delta-encode's **prediction module** (`predict.rs`: encode `x − predictor(history)`, with last/linear/average predictors); lau-compression's **BWT→MTF pipeline** and entropy yardstick; ternary-compression's **5 trits/byte** packing (1.6 bits/trit, 99.1% of log₂3). |
| error correction | `lau-error-correcting-codes`, `ecc-rs` (the same content twice), `ternary-codes` | Parity → Hamming → linear → cyclic → **Reed–Solomon** → convolutional/Viterbi → CRC. ternary-codes does the same over GF(3). |
| vector / holographic | `flux-hdc`, `holographic-storage`, `HOLOS`, `turbovec-substrate` | flux-hdc: 1024-bit hypervectors plus "5 proven theorems" (README only; source 404). holographic-storage: amplitude/phase "waves" in Rust. HOLOS: seeded random-projection "shards" of weight matrices, combined as a "flock" by "wavefront synthesis" (`holos/core.py`, read). turbovec-substrate: TurboQuant plus an fnv1a-64 prev_hash chain (read in full). |
| perception (JEPA) | `plato-perception`, `plato-prediction`, `plato-tile-encoder` | README-only apart from names: Z_in encoders (Raw/Normalized/Hash/Random/Learned) and Z_out predictors (Value/Trend/Anomaly/Action). No algorithm to measure, so we took the *predictor names* as the idea (E1). |
| cultural / counterintuitive | `quipu-math`, `adinkra-math-pypi`, `dodecet-encoder`, `godel-number` | quipu: knotted-cord positional decimal with a digit-sum checksum (`knot.py`, read). adinkra: SUSY Adinkra graphs (`supersymmetry.py`, read). dodecet: 12-bit units (read, not built; see §6). `godel-number`: **404** on master and main, so we built the classical scheme ourselves. |

## 4. Walkthrough

```
$ cd labs/encoding-experiments && ./run_all.sh
vec_index selftest: 60 checks, 0 failures
hdc_theorems selftest: 10 checks, 0 failures
delta_budget selftest: 27 checks, 0 failures
ecc_chain selftest: 28 checks, 0 failures
entropy_corpus selftest: 23 checks, 0 failures
godel_cellgraph selftest: 18 checks, 0 failures
quipu_projection selftest: 201 checks, 0 failures
holos_flock selftest: 6 checks, 0 failures
encoding_routes selftest: 7 checks, 0 failures
adinkra_code selftest: 17 checks, 0 failures
hdc_records selftest: 6 checks, 0 failures
```

The measured results follow. Each is copied from the run's output; the JSON is in `results_<name>.json`.

**E3: which compressed vector substrate keeps retrieval?**

Setup: 480 real paragraphs, all-MiniLM-L6-v2, 384-d, 60 leave-one-out queries, recall@10 against exact
cosine.

```
  float          1536 B/vec  recall@10=1.000
  tv-asis         192 B/vec  recall@10=0.033      ← turbovec-substrate's codes, as written
  tq4             192 B/vec  recall@10=0.945      ← TurboQuant done carefully
  tq2              96 B/vec  recall@10=0.845
  tern             77 B/vec  recall@10=0.773      ← ternary, 5 trits/byte
  sign1            48 B/vec  recall@10=0.728
  hdc1024         128 B/vec  recall@10=0.703      ← flux-hdc-style hypervector
  hdc-fold-xor     16 B/vec  recall@10=0.017
  hdc-fold-sub     16 B/vec  recall@10=0.343
  hdc128           16 B/vec  recall@10=0.355
diagnostics: tv_row_norm_min 0.5037, tv_row_norm_mean 0.749, tv_levels_used [5, 6]
```

**E1: the ActiveLog budget stream** (2,000 records from the B1 emitter)

```
  jsonl             673508 B    336.75 B/record      1.0x
  jsonl+lzma         87844 B     43.92 B/record      7.7x
  col-raw            22715 B     11.36 B/record     29.7x
  col-delta          25352 B     12.68 B/record     26.6x   ← naive delta is WORSE than raw
  col-ctx            18713 B      9.36 B/record     36.0x   ← predict from the same cell's last value
  col-ctx-mean+lzma   3604 B      1.80 B/record    186.9x
  sha256 prev fields are 24% of the JSONL and 0 B in every columnar codec (recomputed)
```

The same codec on real numbers (169 scored autoclaw rows × 4 judge scores):

- JSON 2,660 B.
- Varint alone: 1,070 B.
- Delta-predicted: 849 B.
- Mean-predicted: 823 B; with lzma, 792 B.

**E2: noise against the chain.** Numbers are recovered trials out of 12, on 200 records:

```
  jsonl-200 none          66760 B        1e-5: 1   1e-4: 0   1e-3: 0   burst64: 0   burst512: 0
  jsonl-200 rs255/223x8   77523 B (+16%) 1e-5:12   1e-4:12   1e-3:12   burst64:12   burst512: 0
  ctx-lzma  none            536 B        1e-5:11   1e-4: 6   1e-3: 0   burst64: 0   burst512: 0
  ctx-lzma  rs255/223x8    2042 B        1e-5:12   1e-4:12   1e-3:12   burst64:12   burst512: 0
  silent (wrong data accepted) = 0 in every cell
```

**E8: encodings as System-2 routes**, run through the real `backtest_corpus` / `backtest_pair` / `prefer`:

```
  B7 jsonl vs ctx-lzma: certified 3, refused 0; class trade-off; fast=jsonl, cheap=ctx-lzma
     totals: jsonl 18 ms / 468,689 B   ctx-lzma 145 ms / 3,160 B
  B4 prefer (standing = BER-1e-4 survivals jsonl 0, ctx-lzma 8, ctx-lzma-rs 18):
     frontier = all three; good=ctx-lzma-rs, fast=jsonl, cheap=ctx-lzma
  B7 exact vs tq4+rerank:     product-identical top-10 on 60/60 queries
  B7 exact vs hdc1024+rerank: product-identical on 56/60, refused 4/60
  hot bytes: exact 737,280, tq4 92,160, hdc1024 61,440 (B7 has no axis for this)
```

The other experiments' outputs are in the lab README table and in §6.

## 5. The contract

- **Inputs.** Real repo data: the corpus paragraphs, the situation-recorder graph, and autoclaw scores. The
  B1 emitter's schema. DeepInfra only in `build_corpus.py` (8 embedding calls) and E6 (40 chat calls),
  all cached in `data/`. A rerun is offline and free.
- **Invariants.**
  - Every lossless codec decodes and is compared byte-for-byte, or record-for-record against the
    canonical JSON, inside the run.
  - Every ActiveLog codec re-verifies `verify_chain` and the 32-byte head receipt.
  - B7's product gate runs before any cost is compared.
- **Receipts.** `./run_all.sh` → 11 lines of `<name> selftest: N checks, 0 failures`, 403 checks in all.
  `./run_all.sh --measure` → the numbers above, plus the `results_*.json` files.

## 6. Failure modes, scars, and negative results (each one measured)

**The upstream repos:**

- **turbovec-substrate does not deliver its compression.** Three separate scars, all reproduced from its
  source:
  1. Its rotation normalizes each row *before* Gram–Schmidt, so the rows are not unit length (min 0.50,
     mean 0.75). The rotation is not orthonormal.
  2. Its Lloyd-Max table (−2.79 … 5.50) is not scaled for coordinates of size about 1/√d. A unit
     384-d vector uses **2 of the 16 levels**.
  3. `search()` ranks by exact distance on the **stored float vector**. The 4-bit codes only feed a
     `quantized_matches` count. Ranked by that count, recall@10 is 0.033, close to chance (0.021).

  So "8× compression, ~0.5% recall loss" is not what the code does. Done carefully (E3 `tq4`),
  TurboQuant gives 8× at 0.945. The fix is small and belongs upstream: scale the centroids by 1/√d,
  renormalize after orthogonalizing, score asymmetrically against the codes, and stop storing `vector`.
- **flux-hdc Theorem 4 is false as stated.** The README says "1024→128 fold: ε ≤ 0.003 for σ ≥ 0.7".
  The flux-hdc source is unreadable (404), so both obvious fold implementations were tested:
  - XOR-folding has error 0.20–0.32, matching the prediction (1 + (2s−1)⁸)/2. It drives similarity to
    0.5, and retrieval with it is at chance (0.017).
  - Subsampling has error 0.013–0.031, about 4–10× the claim. It is no better than a native 128-bit
    vector (recall 0.343 vs 0.355).

  T1 (binding: exact unbind, |sim − 0.5| = 0.013), T2 (bundling: 17 items out of a 1,000-item codebook
  recover perfectly; 129 items recover 74%) and T3 (a 0.7-similar partner always beats 999 random
  vectors) hold.
- **HDC is the wrong replacement for turbovec.** At 128 B, hdc1024 gets recall 0.703. tq2 at 96 B gets
  0.845, and a 1-bit asymmetric sign code at 48 B gets 0.728. Symmetric Hamming comparison discards
  what asymmetric scoring keeps. **But HDC is not useless (E11):** as *role–filler records* over
  situation cells, field read-back by unbinding is 1.000 at ≥256 bits, and conjunctive queries by
  partial record are 1.0 at ≥512 bits (0.29–0.36 below). That is algebra TurboQuant cannot do.
- **HOLOS: "more shards = better quality" holds, but it is the wrong trade.**
  - At n = 128, flock error falls 0.966 → 0.805 from 1 to 8 shards (32 KB).
  - A 4-bit per-row quantizer at 8.7 KB gets 0.117.
  - Random projection is data-oblivious, so low-rank structure did *not* help (my hypothesis, refuted:
    0.968 vs 0.966).
  - At equal bytes, one big shard beats the flock from m = 4 (0.705 vs 0.805 at m = 8). At the 24-d
    pilot the flock won narrowly, which is why that check was removed rather than asserted.
  - "Wavefront synthesis" matches a plain mean (cosine 0.687 vs 0.707 gauss; 0.650 vs 0.633 low-rank).
- **quipu as a projection alphabet costs accuracy and tokens.**
  - DeepSeek-V3 decodes quipu at 0.84, and all 8 errors are run-length miscounts or a dropped
    position (477→47, 61→601). It uses 2.6× the prompt tokens of decimal.
  - Llama-3.1-8B decodes nothing except decimal (braille 0.02, quipu 0.00).
  - Balanced ternary fails on both models (0.02).
  - quipu's digit-sum checksum catches 100% of substitutions and **0%** of adjacent transpositions.
    Luhn catches 98.25%; weighted mod-11 catches 100%.
  - **For Syzygy, numeric content should be projected as decimal**, with knots and glyphs kept for
    shape, not for quantities.
- **Gödel numbering is a query algebra, not a storage format.** The real 8-cell graph fits in 197 bits
  (22 B vs 27 B varint adjacency, 143 B JSON), but at n = 256 it is 2.4× larger, and decoding cost grows
  as O(n²) primes. What survives is the algebra: sub-graph ⇔ divisibility, union = lcm, core = gcd,
  all measured true.
- **Classic entropy coders do not beat stdlib, with one exception.** Order-0 Huffman and adaptive
  arithmetic both land at H0 (4.45–4.48 bits/byte on text), and lzma and bz2 beat them easily.
  lau's BWT→MTF→arith0 pipeline is the exception: 2.64 bits/byte on corpus text, better than lzma
  (2.70), within 7% of bz2 (2.46).

  The "entropy yardstick" also misleads at order > 0. On the float16 embeddings, empirical H2 is 3.17
  bits/byte, but the best real coder gets 7.18. On small samples, H_k is an overfit estimate, not a
  lower bound.

**Our own mature systems:**

- **Naive delta hurts the ActiveLog.** Adjacent records belong to *different* cells, so global delta
  (26.6×) is worse than no delta (29.7×). Only same-cell prediction helps (36.0×; mean predictor
  36.2×, trend 35.5×). The plato-prediction lesson is to predict the expectation, not the last sample.
- **The sha256 `prev` fields are 24% of the log and carry zero information.** They are recomputable
  from content. A compressed log can drop them all and keep only the 32-byte head receipt, as E1 and
  E2 do.
- **B7 cannot see memory.** tq4 + rerank is product-identical on 60/60 queries and cuts hot memory 8×,
  but B7 scores it `dominates-faster-cheaper` *for exact*, because its only storage axis counts cold
  bytes too and it has no hot-memory axis. B7 pairwise also rates ctx-lzma above ctx-lzma-rs, because
  robustness only shows up once B4 is given a `standing`.
- **Wall-clock noise can flip B7's "fast" verdict.** The first E8 run had RS *faster* than its own
  subset (62 ms vs 137 ms). Fixed with best-of-3 timing; recorded as a scar for any measured
  `wall_ms` route.

**Not built, and why:**

- `dodecet-encoder`: a 12-bit fixed-point unit. E1's lossless varint already beats a fixed 12-bit slot
  for our small integers, and we have no lossy use for it yet.
- `holographic-storage`: its "wave" superposition *averages phases* (README formula), which is not
  invertible for multiplexed sources. Interleaved RS (E2) is the measured answer to "survive partial
  damage."
- `compress-lz77-rs` / `run-length`: covered by stdlib zlib/lzma in E9.

## 7. How it composes: the map from gem to system

| mature system | gem that transfers | status | evidence |
|---|---|---|---|
| **turbovec / TurboQuant** | a correct TurboQuant (orthonormal rotation, 1/√d-scaled Lloyd-Max, asymmetric scoring); ternary 5-trits/byte as a 77 B tier | **built** (E3) | recall 0.945 @192 B; 0.773 @77 B |
| turbovec as a System-2 route | tq4 shortlist(50) + exact rerank from cold floats | **built** (E8) | 60/60 product-identical, 8× less hot memory |
| **ActiveLedger (B1)** | same-cell prediction → zigzag → varint → lzma; drop the recomputable prev hashes | **built** (E1) | 187×, lossless, chain re-verified |
| ActiveLedger integrity | RS(255,223) with 8-deep interleave, applied *after* compression | **built** (E2) | 12/12 at BER 1e-3 and 64-byte bursts; 0 silent |
| **situation-recorder** | HDC role–filler records for index-free structured recall; Gödel algebra for sub-graph tests | **built** (E11, E5) | 1.0 query precision at ≥512 bits; divisibility = sub-graph |
| **Syzygy** projection | *negative*: project numbers in decimal; braille only for strong readers; quipu/ternary no | **built** (E6) | decimal 1.00 on both models; quipu 0.84 / 0.00 |
| Syzygy "embrace noise, reconstruct" | HOLOS flock | **tested, not recommended** (E7) | quantization is 7× better at ¼ the bytes |
| **System-2 (B7/B4)** | encodings as routes; robustness as B4 `standing` | **built** (E8) | a genuine three-way frontier; B7's missing hot-memory axis found |
| plato Z_in/Z_out as a learner | only the predictor idea transferred; there was no model to test | **speculative** | — |
| adinkra | the SUSY Adinkra is the N-cube; its e8 quotient is a SECDED decoder | **built** (E10), known math | 128/128 corrected, 448/448 detected, 896/896 3-bit miscorrected |

### The top 3 gems to promote (recommendation, with reasons)

1. **Context-predicted columnar ActiveLog + drop-the-recomputable-chain (E1).**
   - 187× smaller than JSONL and 24× smaller than JSONL+lzma, with an exact round-trip and a 32-byte
     head receipt that still proves the chain.
   - Cost is about 150 ms per 1,400 records in pure Python.
   - Promote it as the *at-rest* format for B1 logs. JSONL stays the live, append-only form.
2. **RS(255,223)×8 wrapped around that compressed log (E2).**
   - Compression makes a log fragile: ctx-lzma alone survives only 6/12 at BER 1e-4. RS brings it to
     12/12 at 1e-3 and through 64-byte bursts.
   - The result is still **33× smaller than the raw JSONL** (2,042 B vs 66,760 B). The chain stays the
     detector; RS becomes the repairer.
   - Use deeper interleave for longer bursts: 512-byte bursts still kill it.
3. **A correct TurboQuant tier, plus shortlist-rerank as the certified route (E3 + E8).**
   - tq4 keeps 0.945 recall at 192 B/vec, and a 50-shortlist rerank returns the *identical* top-10 on
     60/60 queries, so B7 certifies it.
   - Fix turbovec-substrate upstream: the three scars in §6.
   - Add a **hot-memory axis to B7** so the route's real advantage becomes visible.

Runner-up: HDC role–filler records (E11) for index-free "which cells had actor X doing Y" queries over
situation logs.

## 8. Where to look next

- [`labs/encoding-experiments/README.md`](../../labs/encoding-experiments/README.md): the index and the commands.
- [`situations/arch/TURBOVEC-FAMILY-STUDY.md`](TURBOVEC-FAMILY-STUDY.md): the earlier turbovec study. That study counted 35 upstream tests as green; §6 of this one shows why a green suite did not catch the compression gap.
- [`labs/system2-backtest/README.md`](../../labs/system2-backtest/README.md) and [`labs/route-preference/README.md`](../../labs/route-preference/README.md): the B7/B4 contracts that E8 plugs into.

### Next iteration (handoff)

1. **Upstream the turbovec-substrate fix** (scale, renormalize, asymmetric scoring, drop the stored
   float) as a PR on that repo. Re-run E3's `tv-asis` row against it.
2. **Wire E1 + E2 into `labs/activeledger`** as an `at_rest.py` (`pack(records) → bytes`,
   `unpack(bytes) → records`, head-receipt checked). Add it to the B1 selftest.
3. **Add a `mem_hot_bytes` axis to B7/B4** and re-run E8 Workload B. Expected: tq4 + rerank becomes
   `trade-off` (hot memory vs wall_ms) instead of being dominated.
4. **Scale E3 to 10k vectors and a real query set** (not leave-one-out), and add E1's predictor idea to
   the *codes*: delta-coding the tq4 codes of near-duplicate cells.
5. **E11 at situation-log scale:** encode the real fleet situation JSONLs once they exist, and compare
   HDC partial-record queries against a plain inverted index on bytes and latency.
