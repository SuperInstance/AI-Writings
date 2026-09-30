# ML in Quilt — the forward pass as a priced cell graph

*Architecture mark, 2026-09-30. Written in response to Casey's charge: "we have moved to so many things we
should think big and architect correctly whatever we build for these ends in quilt." The runnable half is
[`labs/ml-in-quilt/`](../../labs/ml-in-quilt/), whose selftest reports 64 checks and 0 failures. Every
number in this document comes from that lab unless it is marked **(speculative)** or **(arithmetic)**. The
doc follows the dual-audience standard in [`situations/blueprints/README.md`](../blueprints/README.md).*

---

## 1. In one breath

A transformer is already a chain of small pure functions (tokenize, embed, norm, attention, MLP, head,
sample). If each of those functions is a **quilt cell**, the fleet's existing machinery can work on it
without modification:

- the ActiveLog gives every block a receipt;
- System-2 compares interchangeable implementations of a block (fp, 8-bit, 4-bit, approximate, cached)
  and picks one per situation and per device;
- only routes that produce the **same token** as the reference are ever compared on price.

## 2. Why it exists — and why not just port

### What we studied

| source | what it teaches | what we take |
|---|---|---|
| **naklecha/llama3-from-scratch** (`master`) | The forward pass one tensor op at a time: tokenizer, RMSNorm, RoPE via complex rotation, per-head QK scores, causal mask, softmax, V, output projection, SwiGLU FFN, final norm, logits → argmax. A notebook of ~30 small pure steps. | The **cell granularity**. Each notebook heading is a block-level cell (§3). The notebook is a hand-written replay log with no receipts. |
| **SuperInstance/llama3-from-scratch-in-quilt** | `git ls-remote` gives HEAD `1b866ac6…` on `main`, the same sha as upstream `naklecha/llama3-from-scratch`. Its README and notebook are byte-identical on `main` and `master` (md5 `46db869c…`). **The fork has not diverged yet.** No quilt code exists there. | "Bringing it in" means the notebook's step list becomes our cell taxonomy, and this lab is the first quilt code that fork could hold. We are not merging anything. |
| **naklecha/simple-llm** (`master`, ~980 lines) | The engine layer: async request queue, continuous batching, slot-based pre-allocated KV cache, CUDA-graph capture/**replay** for decode, fused QKV (3 matmuls → 1), fused RMSNorm+residual (Triton), fused RoPE, FlashAttention-2, GQA (8 KV heads per 64 query heads), learned attention sinks, MXFP4-quantized MoE (128 experts, top-4 router). Matches vLLM throughput (135 vs 138 tok/s at batch size 1, 4,041 vs 3,846 at batch size 64, per its README; not reproduced). | Two lessons. (1) Speed comes from **fusion** (several logical ops in one kernel) and **scheduling** (batching, slots). Both work against per-op receipts, so we must separate *logical cells* from *physical kernels* (§3.4). (2) A CUDA graph already applies "capture a route once, replay it". |

We also relied on our own mature systems:

- B1 `activeledger`: the envelope, the budget vector, and the sha256 chain.
- B7 `system2-backtest`: the product-identity gate and the iron triangle.
- B4 `route-preference`: the Pareto frontier plus Hebbian settling.
- `code-real-quant`: 4-bit Lloyd-Max codes that beat HDC at equal bytes (ENCODING-GEMS §6).
- `at_rest.py`: ALR1 columnar compression plus RS(255,223) repair.
- `situation-recorder` and `situation-memory`: the mission corpus and `find_similar` recall.
- [ACTIVELEDGER-CELL-GRAPH.md](ACTIVELEDGER-CELL-GRAPH.md) §11 (System-2) and §14 (the B4 join).

### The naive port and what it lacks

A naive port translates the notebook or the engine into our language and produces a forward pass that
runs. It gives us none of the following:

1. **No receipts.** When a run produces a wrong token, nothing records which block caused it.
2. **No priced alternatives.** Quantization, caching, early exit and speculative decoding are compile-time
   decisions buried in the code. They are not routes that System-2 can backtest per situation and per device.
3. **No gate.** "4-bit is 8× smaller with ~no quality loss" stays a claim. Nobody checks whether the
   cheaper route still gives *the same answer*.

A cell-native design gets all three from machinery that already exists and is already tested. The lab
confirms this: B7 and B4 are imported and called unmodified.

### Where a naive port is fine (said plainly)

- **Tokenizers.** They are exact integer functions with no useful alternatives. Wrap tiktoken, BPE or a
  character table as a single cell with a vocabulary hash. Rewriting one buys nothing.
- **The arithmetic inside a block.** Take the RMSNorm formula, the RoPE rotation or the SwiGLU as they are.
  Cell-native does not mean re-deriving the math. It means putting a boundary around the math.
- **Checkpoint parsing.** safetensors and Meta's `consolidated.pth` loaders are plain I/O. Port them and
  content-address the output.
- **Fused kernels (Triton, FlashAttention, MXFP4 MoE).** Adopt them as *implementations* of a cell or of a
  fused group of cells (§3.4). Do not re-express them.

## 3. The mental model

### 3.1 The nouns

```
                    ┌────────────── route (a plan, or a composition of plans) ──────────────┐
 situation ──▶  tokenize ─▶ embed ─▶ [norm ─▶ attn ─▶ norm ─▶ mlp]×L ─▶ norm ─▶ head ─▶ sample ──▶ PRODUCT
 (prompt,          │          │              │  ▲           │              │        │     (token ids)
  device,          ▼          ▼              ▼  │KV chain   ▼              ▼        ▼
  history)      cell.tick  cell.tick     cell.tick ...   cell.tick      cell.tick cell.tick ──▶ ledger.transaction
                 {in,out,w,kv,impl,flops,bytes,budget}  → ActiveLog v1 (sha256 prev-chain)
                                                      → B7 gate at the product → B4 frontier per situation/device
```

- **Cell.** A pure function `(inputs, weights) → outputs` with a `kind`, one or more **impls**, and one
  `cell.tick` per call. The tick records content hashes of what it read (`in`, `w`, `kv`) and what it wrote
  (`out`), plus `flops`, `bytes` and the B1 budget vector.
- **Impl.** An interchangeable implementation of the same cell: `fp`, `q8` or `q4` today, and later a fused
  kernel, a KV-quantized attention, or a sparse or approximate variant.
- **Plan / route.** A plan maps cells (or kinds) to impls. A route is a plan, or a composition of plans such
  as `spec-q4 = draft(q4) ∘ verify(fp)`, and is logged as one ActiveLog run closed by one
  `ledger.transaction`.
- **Product boundary.** The point where two routes must agree *exactly* for B7 to compare them. For
  language models this is the **sampled token**, with the reason given in §3.3.
- **Device profile.** The declared roofline `(flops/ms, bytes/ms)` used to price every tick. Preference is
  a function of it (§4, the regime flip).
- **Situation.** The input plus the context that decides which route is preferred: prompt, device, and
  history of similar situations.

### 3.2 The cell taxonomy

"Product" in this table means the equivalence relation under which two impls count as the same.

| cell | product / equivalence | alternatives worth pricing | port or native? |
|---|---|---|---|
| `tokenize` | exact ids | none useful | **port** (wrap) |
| `load:<tensor>` | weight-blob hash (content address) | fp32 / q8 / q4 / other quantizations at rest; RS-wrapped or not | native: this is where at_rest sits |
| `embed` | exact | fp; a quantized embedding table | port the math |
| `norm` | exact within an impl | fused with residual (simple-llm) | port; usually fused (§3.4) |
| `attn` | *not* a product boundary | fp / q8 / q4 weights; KV quantization; window or sparse attention; GQA sharing; FlashAttention kernel | **native**: carries the KV chain |
| `kvcache` | KV chain head (exact) | recompute vs prefix-cache hit vs quantized KV | **native**: content-addressed prefix reuse |
| `mlp` / `moe` | *not* a boundary | fp / q8 / q4; MXFP4 experts; top-k router width | native (a MoE router is itself a B4-shaped chooser, **speculative**) |
| `jepa.predict` | *not* a boundary | skip layers ≥ e by predicting Z_out from Z_in | native: an approximate impl of "the rest of the stack" |
| `head` | *not* a boundary | fp / q8 / q4 | native; the most quantization-sensitive block measured |
| `sample` | **the product boundary**: token id (greedy), or (token, seed) when stochastic | greedy; seeded temperature | native: logs token and margin |
| `verify` | exact: committed tokens = verify plan's argmax | lookahead k; which draft plan | **native**: the gate made into a route |

### 3.3 Why the product boundary is the token

B7's first law is *never price a cheaper different answer*, and its gate is exact (`product_hash` equality).
A 4-bit activation never equals the fp32 activation bit for bit. If the product were declared at an
activation, every quantized route would be refused forever. If it is declared at the **token**, a
quantized route is certified exactly where it reaches the same token. That is the honest question: *did
the user get the same answer?*

The lab's measurements, over 24 situations of 12 greedy tokens each:

- **q8 everywhere:** certified on 20/24. On those 20 it dominates fp (faster and cheaper).
- **q4 in any block:** certified on 0/24. Its *product horizon* (the first token that differs from fp) has
  mean 3.3 and is 0 on 5 situations. For q8 the mean is 10.9.
- **Teacher-forced per-token agreement with fp:** q8 0.993, q4 0.807. By block: q4-attn 0.862, q4-mlp
  0.841, q4-head 0.945. The head has the largest logit error (max |Δz| 2.19 vs 0.28 and 0.23).

Short sequences can pass while long ones fail, because errors compound through the autoregressive loop.
The product boundary therefore has to be the *whole committed sequence*, not a single token.

### 3.4 Logical cells vs physical kernels (the simple-llm tension)

simple-llm is fast because it *fuses*: QKV in one matmul, RMSNorm with the residual add, RoPE in place.
Fusion erases the boundaries receipts depend on. The resolution:

- A **logical cell** is the receipt unit. Its `in` and `out` hashes are what System-2 reasons about.
- A **fused kernel** is an *impl of a group of cells*. It emits one tick that covers the group
  (`cell: "L3.norm1+attn"`) with the group's `in` and `out`.
- The fused impl is a route like any other. B7 checks it against the unfused reference at the product
  boundary. If the fusion reorders float reductions and flips a token, the gate catches it.
- **Receipt level is a knob.** Options are `product` (sample ticks only), `block` (what the lab does), or
  `op` (debug). Replay at a finer level than the live run is always possible, because the finer run
  reproduces the coarser run's hashes. **(speculative; the lab only runs `block`.)**

CUDA-graph replay (simple-llm `_decode_step`) is the kernel-level version of *replay == live*. A captured
route runs again with new inputs.

## 4. Walkthrough — what the skeleton runs

```
$ cd labs/ml-in-quilt && python3 selftest.py      # 64 checks, 0 failures, ~45 s
$ python3 mlq_system2.py                           # the full report
```

The model has 2 layers, d=32, 2 heads, ff=64, a 28-character vocabulary and 19,260 parameters. All
weights are seeded Gaussian except the **readout** (head), which is ridge-fitted in closed form to a
145-character corpus (train next-char accuracy 0.759). This makes it an echo-state transformer, not an LLM.
Given `"the cat "`, fp greedily writes `"sat on the mat. "`.

**One tick** (verify stream of a `spec-q4` run, layer-1 attention over 12 positions):
```json
{"alv":1,"dev":"ml-in-quilt","seq":69,"type":"cell.tick","prev":"sha256:0019…36d6",
 "body":{"route":"spec-q4","stream":"verify","cell":"L1.attn","kind":"attn","impl":"fp","pos":[0,12],
         "in":"0x6eee68e068b27ef4","out":"0x2517b54be46f97bf","w":"0x29f15d041bb5baab",
         "kv":"0x2f1d7dc39032e1e7","flops":108288,"bytes":40960,
         "budget":{"wall_ms":0.010829,"tokens":{},"usd":0.0,"power_w":0.0,"mem_mb":0.0,
                   "storage_bytes":{"train":0,"prod":0},"reqs":"local"}}}
```
**The transaction** (product = prompt, tokens and text; everything else goes under `chosen`, which B7
excludes):
```json
{"route":"spec-q4","path":"spec-q4","prompt":"the cat ","tokens":[20,2,21,0,16,15],"text":"sat on",
 "total_budget":{"wall_ms":0.103675,"storage_bytes":{"train":0,"prod":83388},"mem_mb":0.083388,...},
 "chosen":{"plan":{"draft":{"attn":"q4","head":"q4","mlp":"q4"},"verify":{}},"accept":[5,5],"k":4,
           "device":"edge-cpu-roofline-v1"}}
```

**What the report shows** (all measured on the toy, under declared cost models):

| claim | result |
|---|---|
| replay == live | a `spec-q4` run (177 records) re-executed from its transaction alone is byte-identical |
| localization | tampering one weight (`L1.w1[0][0] += 0.25`) makes the first divergent record `load:L1.w1` and the first divergent compute cell `L1.mlp`. The same holds for `L0.wqkv → L0.attn` and `head → head` |
| verifier makes lossy exact | `spec-q4` and `spec-jepa` are certified 24/24 on both devices. Draft acceptance is 195/379 (q4) and 190/399 (JEPA exit) |
| **regime flip** | On `edge` (flop:byte = 1), fp **dominates** spec-q4 (2.97 vs 5.07 modeled ms). On `accel` (flop:byte = 100) it is a **trade-off**: spec-q4 is faster (2.37 vs 2.43), fp is cheaper (73 KB vs 83 KB at rest). B4's frontier moves from `[fp]` to `[fp, spec-q4]` |
| preference is per situation | B4 per situation on `edge` picks q8 for fast on 20 situations and fp on the 4 where q8 is refused. The Hebbian book settles on q8 |
| content-addressed KV | a prefix cache warmed by `"the cat sat on the "` serves `"the cat sat on the log"`: 19 positions reused, loaded KV chain heads equal computed ones, B7 certifies it, flops 1,308,792 → 589,680 |
| at rest | weight blobs: fp32 73,456 B, q8 20,396 B, q4 11,244 B (6.53×). With RS the q4 blob is 1.27× larger; after corrupting 96 bytes, repair is exact and the repaired blob decodes to the live kernel's weights. Activation log (177 records): JSONL 88,765 B, JSONL+lzma 12,108 B, ALR1+RS 6,127 B, round-trip exact |
| margin gate | ε = max \|Δlogit\| on the first half of the corpus. On the held-out half, q8 tokens with margin > 2ε are 82% of positions, with 0 flips. q4 has 0% safe (ε is too large) |
| **margin-triggered verify (ML-1)** | q8 decodes, and fp catches up in one batched pass only when q8's margin is ≤ 2ε. **`trust-q8` (confident tokens never re-checked) is certified 24/24, against 20/24 for q8 alone, with 0 fixes.** On `accel` it is the fastest exact-product route measured: 1.88 ms vs fp 2.43 vs spec-q4 2.37, with 80 verify passes for 288 tokens. B4's accel frontier becomes `[fp, spec-q4, trust-q8]` (fast: trust-q8, cheap: fp). The by-construction variant `gate-q8` costs 2.14 ms |
| cost model vs Python | Python wall time (best of 3, sidecar): fp 45.8 ms, q8 41.4, q4 51.6, spec-q4 99.7. In pure Python, q4 is *slower*. The roofline prices a fused kernel, not our loop |

## 5. The contract

**A cell** (every kind):
1. It is pure: same `(in, w, kv, impl)` gives the same `out`, bit for bit, *within one impl on one
   substrate*.
2. It emits exactly one `cell.tick` per call, with `{cell, kind, impl, pos, in, out, w, kv, flops, bytes,
   budget}`, and the budget satisfies `activeledger.budget_ok`.
3. Dataflow is closed: each tick's `in` is some earlier tick's `out` in its stream. The exceptions are
   tokens entering `embed`, cache loads, and verify summaries. The selftest checks this for fp and for
   interleaved draft/verify streams.
4. The weights it reads are named by content (`w` = hash of the packed blob at rest). A different blob
   means a different cell instance.

**A route run:**
1. One ActiveLog slice, `load` ticks first, closed by one `ledger.transaction`. The product is
   `{prompt, tokens, text}`. Plan, device, draft statistics and cache warm-up go under `chosen`.
2. `total_budget` equals the sum of all tick budgets, which `backtest.replay_route` re-derives.
3. `replay(model, records)` re-executes the run from the transaction alone and must reproduce every record.

**System-2 over routes:**
1. B7 first checks the gate (product-identical tokens), then compares `{good, fast, cheap}`. A refused
   verdict carries no budget.
2. B4 builds the frontier over certified routes. Standing (for `good`) comes from an oracle, never from
   the differ.
3. Every verdict is valid only for the device profile it was priced under (§11.2 stationarity).

**Receipt:** `python3 labs/ml-in-quilt/selftest.py` → `ml-in-quilt selftest: 64 checks, 0 failures`.

## 6. How each of our systems plugs in

| system | role in ML-in-quilt | status |
|---|---|---|
| **B1 activeledger** | Every forward pass is an ActiveLog run. The budget vector is on every tick. The sha256 chain orders the run, and the fnv1a activation hashes address it | **built** (lab) |
| **B7 system2-backtest** | The gate at the token, and the iron triangle over routes. It found q8 ≻ fp where certified, q4 never, and spec by construction | **built**, unmodified |
| **B4 route-preference** | The frontier per workload and per situation, per device. The Hebbian book settles which cheap route to try first | **built**, unmodified |
| **code-real-quant** | Its 4-bit Lloyd-Max table and pack format *are* the q4 impl. The same table beat HDC at equal bytes for retrieval. Here it is used for weights, where it loses the product unless paired with a verifier | **built** |
| **at_rest ALR1+RS** | Weight blobs are RS-wrapped (repairable). Activation logs are ALR1-packed (half of JSONL+lzma) | **built**; the weight path uses `rs_wrap` only, not ALR1 columnar |
| **situation-memory** | Recall of "situations like this, and which route held". Lexical `embed_text`, the model's own latent (Z_in), and the cheap route's own margin were compared. **On 24 situations none clearly beats the majority baseline** (0.833; lexical 0.833, latent 0.792, margin 0.875) | **built, no signal yet** |
| **situation-recorder** | Every System-2 decision about an ML route (which draft, which k, which device) is a mission, and should be recorded as one | **not wired** |
| **JEPA (plato Z_in/Z_out)** | A predictor cell `jepa.predict`: Z_in = normed residual after layer e−1, Z_out = final normed hidden. It is an approximate impl of "layers e..L". Fitted by ridge regression on the model's own activations, which is exactly what the activation log would supply at scale | **built**; R² 0.993, but the lowest token agreement (0.772) |
| **rubric-forge / OrgBook standing** | The `good` axis. It is the only way to prefer a *better* route that the gate refuses (see the "the rat" scar) | **not wired** |
| **Moth** | Seeds for stochastic `sample`. The seed becomes part of the product, so stochastic routes stay replayable | **speculative** |
| **polyformalism ports** (quilt-c, rust, py) | Cross-substrate replay holds only at the token boundary, and only off near-ties (§7) | **speculative** |

### JEPA, more precisely

Earlier study (ENCODING-GEMS) found plato's Z_in/Z_out was README-only, with no model to test. Here it
has a concrete job: a **latent-space predictor that replaces the tail of the network**. The lab shows the
important lesson. Fitting the latent well (R² 0.993) and preserving the product (token agreement 0.772)
are different goals. A JEPA predictor is therefore a **draft**, never a final route. Its output needs a
verifier cell, and once it has one it is exactly as trustworthy as fp (24/24).

The cell-native role that remains **(speculative)**: the activation log is a free, perfectly labeled
(Z_in, Z_out) corpus, so predictors can be retrained continuously from production traffic. B7 decides
per situation whether the predictor earns its place as a draft.

## 7. The honest what's-hard

1. **Floating-point replay is per substrate.** Replay == live is byte-exact here because Python float64
   runs the same ops in the same order. On GPUs, atomics and split-K reductions are non-deterministic, and
   different kernels reorder sums. Replay therefore holds within `(impl, kernel version, device)`, which
   must go into `impl`. Across substrates, identity exists only at the token and fails on near-ties.
   Near-ties should be logged as scars (the sample tick already logs `margin`). **(arithmetic/speculative;
   only one substrate was run.)**
2. **Receipts cost something at scale.** Hashing one 4096-wide fp16 row is 8 KB. With a fast
   non-cryptographic hash at about 10 GB/s that is about 1 µs per row per block, against block compute
   that is milliseconds per batch at 8B scale. Receipts should be cheap at `block` level and too costly at
   `op` level. **(arithmetic, not measured.)** The lab uses pure-Python fnv1a, which is slow. The design
   answer is the receipt-level knob (§3.4).
3. **Batching breaks the one-sequence tick.** Continuous batching runs many sequences through one kernel
   call. Ticks become per-batch with a per-row hash vector, and a sequence's receipt becomes a projection
   of the batch ticks. Not built.
4. **The exact gate is too strict for two real needs.**
   - *Quality improvements.* In "the rat", q8's `sat on the m` beats fp's `sat sathe ma` and is still
     refused.
   - *Stochastic sampling.* Rejection-sampling spec decode preserves the *distribution* but not the
     per-seed identity.

   Both need a second product relation (oracle-scored `good`, or distributional equivalence). That relation
   must be explicit and must never silently replace identity.
5. **The cheap axis is incomplete.**
   - B7 scores storage (cold bytes) but not hot memory. A prefix cache's residency is logged in `mem_mb`
     but ignored, so the cache looks free. This reproduces the ENCODING-GEMS finding.
   - Spec decode must keep both weight sets at rest (83 KB vs 73 KB), and B7 rightly charges for that.
   - A B7 `mem_mb` axis is the smallest fix.
6. **The cost model is a declaration.** The regime flip is a fact about two *declared* rooflines. The
   first real device profile needs measured, best-of-N timing (the ENCODING-GEMS E8 scar: wall-clock noise
   flips "fast").
7. **Situation recall has no signal yet.** At 24 situations, the three encodings sit within one case of
   the majority baseline. The architecture predicts that recall should choose which draft and which k to
   *try*, never skip the gate. That prediction is untested.
8. **We have not trained anything by gradient.** The readout and the JEPA predictor are closed-form ridge
   regressions. Backprop through a cell graph is also a cell graph (the backward cells of each forward
   cell), and each optimizer step is a route with a product (the new weights hash). **(speculative.)**
9. **Toy scale.** None of the lab's numbers transfer to real models as values. What transfers is which
   comparisons are *possible* and which invariants hold.

## 8. Where to look next

- [`labs/ml-in-quilt/README.md`](../../labs/ml-in-quilt/README.md): the lab, its scars, how to run it.
- [ACTIVELEDGER-CELL-GRAPH.md](ACTIVELEDGER-CELL-GRAPH.md) §11 and §14: System-2, the iron triangle,
  and the B4 join this design rides on.
- [ENCODING-GEMS-STUDY.md](ENCODING-GEMS-STUDY.md): the at-rest formats, the hot-memory blind spot, and
  why the q4 codes are the ones we trust.
- Also relevant: [ML-IN-THE-LOOP.md](ML-IN-THE-LOOP.md). It covers learning *from* the pipeline; this doc
  covers the model *as* the pipeline.

### The build backlog (dependency-ordered)

| # | item | why next | receipt |
|---|---|---|---|
| ~~ML-1~~ | **Margin-triggered verify. BUILT** in this pass (`run_gated`, `gate-q8`, `trust-q8`) | trust-q8 certified 24/24, 0 fixes, fastest exact route on accel | selftest §"margin-triggered verify" |
| ML-1b | **ε on unseen text.** Calibrate ε on one corpus, test trust-q8 on disjoint text, and add a per-cell ε (the differ profile) so the gate knows *which block* is uncertain | trust-q8's 24/24 is in-distribution only | certified rate on held-out text; the first fix observed |
| ML-2 | **B7 `mem_mb` axis** (hot memory) | Unblocks honest pricing of prefix caches, KV quantization and resident drafts | B7 selftest plus a pcache verdict that changes class |
| ML-3 | **Real weights, one substrate**: a ~15M-param TinyStories-class checkpoint behind the same cell interface, with numpy allowed at this step | Tests whether q4's product horizon and the regime flip survive a real model | the same report, measured per device, best-of-3 timing |
| ML-4 | **Fused-group impls and the receipt-level knob** | The simple-llm tension (§3.4) | a fused `norm+attn` impl certified against unfused |
| ML-5 | **Oracle `good` axis**: rubric-forge scores as B4 standing | Needed to prefer a better route the gate refuses | "the rat" becomes a documented trade-off, not a refusal |
| ML-6 | **Record System-2 ML decisions as situations** (situation-recorder) | Gives recall a real corpus instead of 24 prompts | recall beats majority by more than one case |
| ML-7 | Port `cellml` to quilt-c or Rust and compare hashes | Tests the cross-substrate claim in §7.1 | token-identical runs, and near-ties listed as scars |

### The spine (five lines to remember)

1. **Every transformer block is a cell.** Pure, budgeted, hash-chained in and out, weights named by content.
2. **The product is the token, not the activation.** Quantized routes are certified exactly where they give the same answer.
3. **A verifier cell turns any lossy impl into an exact route.** Speculative decoding is the B7 gate made into a route, and the cheap cell's own margin can decide when to call the verifier.
4. **Preference is a function of situation and device.** B4 picks per situation, and the frontier moves with the flop:byte ratio.
5. **At rest and in memory, content addressing does the work.** Repairable weight blobs, ALR1 activation logs, and KV chains that make prefix reuse checkable.
