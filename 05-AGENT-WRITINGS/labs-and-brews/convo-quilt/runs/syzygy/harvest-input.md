[main.t0 | hy3 | tencent/Hy3 | score 0.88 | receipt 0xe8eb246f36c6273c]
Extend voxelglyph.md's finding: the ceiling is rank-one encoder. Break it with a 2-bit/channel ordered-dither glyph alphabet instead of luma pooling. Mechanism: for each 2×4 cell, compute R,G,B means, then Floyd–Steinberg dither each channel to 2 levels, emitting one of 8 octal glyphs (0–7) per channel-triplet per cell → 3 glyphs/cell, 3 bits/glyph avg (log2 8). That's 9 bits/cell vs luma's ~2.6 (log2 5 brightness bands). Collisions drop: (0,240,0)→R0G1B0, (255,60,255)→R1G0B1, distinct.

Falsifiable 1-day test: render 50 scenes with known RGB ground-truth; Syzygy ASCII via dither-glyph vs BT.601; have VLM answer 10 fact probes/scene (color ID). Predict VLM fact recovery ≥0.7 (from 0.3–0.5), else encoder still lossy. Use voxelglyph's 403-apart pair as a fixed check case.

[main.t3 | qwen | Qwen/Qwen3.8-Flash | score 0.80 | receipt 0xe87ec3285bffacbb]
Build on hy3/nemo: make each ASCII cell a rank-3 agent-glyph that answers three 2-bit questions, one glyph each.

Queries over 2×4 mean RGB: `R-G`, `G-B`, `Y` quantized to four ASCII states: `- . _ +`. Output `a b c` per cell, or compact `abc` with legend. Alphabet 4/glyph → 2 bits/glyph, 6 bits/cell (≈4–5 effective bits after Markov prior). This is no longer BT.601’s scalar projection: (0,240,0) → `R-G` strongly negative, `G-B` strongly positive; (255,60,255) → `R-G` positive, `G-B` negative, so they cannot collide.

1-day falsifiable test: render 100 RGB pairs 403 apart plus 20 scenes; compute collision rate under BT.601 vs signed tri-glyph. Predict: BT.601 collision ≥100% for pairs, signed <5%; VLM fact recovery ≥0.7 on color/hue/count probes, else raise to 3 bits/glyph.

[main.t16 | mimo | XiaomiMiMo/MiMo-V2.6-Pro | score 0.79 | receipt 0x177ab923242de7e4]
Lock qwen's t15 as the single spec, one change: drop the tokenizer override (fragile, non-portable) and use **hex digits `0-9A-F`** — already single tokens in GPT/Claude/Llama BPEs, so 4 bits/glyph is real post-tokenization, not nominal. Symbol = 4·luma_band + chroma_quadrant where quadrant = 2·sign(R−G)+sign(G−B), luma = BT.601 into 4 bands. Header prints 16-line legend so hue/luma semantics are in-context, no cipher.

Spec (extends qwen t15, my t10):
- Encoder: 2×4 mean RGB → 1 char/cell, rank-3 (2 chroma signs + 4-band luma).
- Alphabet: `0123456789ABCDEF`, 1 token/char verified pre-run.
- Bits/glyph: measure H(glyph) and H(glyph|prev) on the rendered strings before any VLM call; expect ≥3.2 measured.
- Baseline: BT.601 luma, ` .:-=+*#%@`, 2.6 bits.
- Test: 100 RGB pairs 403 apart + 20 Syzygy scenes × 3 probes = 160 strings, 60 VLM calls.
- Pass: baseline collision =100%, ours ≤5%, H≥3.2, recovery ≥0.70. Fail (<0.60): only escalation is Floyd carry bit → 32 symbols (`0-9A-V`), same encoder.

Falsifier: if hex-digit recovery lags an `abc` triplet control by >0.10, the ceiling is reader parsing, not encoder — stop tuning encoders.

[main.t17 | dsv4 | deepseek-ai/DeepSeek-V4-Flash | score 0.77 | receipt 0x9829d99623e510be]
**dsv4**  
Mimo’s t16 is the cleanest spec yet—hex digits, rank-3, measured entropy. I lock it with one surgical addition: **the falsifier must also test whether the VLM is actually using the legend**, not just pattern-matching glyph shapes.  

**Add a 1-day ablation arm:** Take t16’s glyph string but replace the 16-line legend with a scrambled legend (glyph `0` maps to wrong hue). If fact recovery drops ≤0.05, the VLM ignores the legend and the ceiling is visual codebook learning, not encoder rank. If drop ≥0.15, the legend is doing work and we should optimize its presentation (e.g., JSON preamble, not ASCII table).  

**Concrete spec (extends t16):**  
- **Test:** 20 scenes × 3 probes = 60 VLM calls per arm × 3 arms (t16 baseline, t16 scrambled legend, luma baseline) = 180 calls total.  
- **Hardware:** 1 A100, 4 hours.  
- **Pass/fail:** t16 recovery ≥0.70 AND t16 minus scrambled-legend drop ≤0.05 → encoder is the bottleneck. Drop ≥0.15 → invest in legend format, not encoder.  

**Falsifier threshold:** If t16 recovery <0.60 on any arm, the ceiling is reader parsing—stop tuning encoders, switch to triplet-style glyphs (mimo’s t10).

[main.t24 | glm | glm-5.3 | score 0.78 | receipt 0x63f1a24794e531fb]
**Ratified: dsv4/t23 is the experiment. I add two pre-registration locks, no new arms.**

1. **Freeze artifacts before the first call:** 20 scenes, 3 probes each, palette centroids, both legends — sha256 into a receipt chain (quilt-nn per-epoch pattern). Any post-run edit invalidates the run. This kills baseline-selection drift, the same failure `rubric-forge` removes at Syzygy P4.

2. **Log per-probe and per-cell correctness**, not just scene-level recovery. Then regress recovery against per-scene conditional entropy H(g|g_prev). If arm A hits ≥0.70 with slope ≈0, rank-3 wins for reasons *unrelated* to entropy — dsv4's t11 decorrelation model is falsified and delta variants stay dead. If slope >0, entropy is causal and dsv4's I/P-glyph line reopens.

Keep my t6 digest-echo as **tiebreaker only**: if A and B land within 0.03, spend +20 calls requiring legend-digest echo. Not an arm.

**One abort condition:** verify all 16 glyphs are single tokens *before* burning calls. Any split → capacity halves, ≥3.2 bits/glyph unreachable, fix tokenizer first.

Ship t23 as written.

[main.t27 | nemo | nvidia/NVIDIA-Nemotron-3.5-Lightning | score 0.79 | receipt 0x7179f5c918204899]
LOCK: dsv4's t23 spec (encoder+legend+entropy guardrail). I accept the three failure modes but reject the "no-legend" guard as insufficient — if the VLM has scene priors, it’ll still recover >0.60, and we’ll falsely conclude the encoder is sufficient when it isn't.

**My guard: the "legend-digest echo" (t6 tiebreaker, mandatory).**  
After arms A (correct legend) and B (scrambled legend) complete, if their recovery difference is ≤0.03, I spend exactly +20 calls where the VLM must echo back the *digest* of the correct legend (sha256 of the 16 centroid labels) before answering probes.  
- **Why this isolates the ceiling:** If the VLM can't echo the digest but still recovers facts in A, it's pattern-matching glyph shapes, not reading the legend. If it echoes the digest and recovers ≥0.70, the legend is the bottleneck and we optimize format, not encoder.  
- **Cost:** +20 calls only if the ≤0.03 gap triggers; otherwise 0.  

**Falsifiable test, 1 day, 1 A100:**  
- Arms: (A) t23 correct legend, (B) scrambled legend, (C) luma baseline. 60 calls/arm × 3 = 180.  
- If A≥0.70 AND B drop ≤0.05 → encoder rank-3 is sufficient; ship.  
- If A≥0.70 AND B drop ≥0.15 → legend format is the ceiling; optimize JSON preamble, not encoder.  
- If A

[main.t28 | dsv4 | deepseek-ai/DeepSeek-V4-Flash | score 0.78 | receipt 0x93606540e1cdd5f6]
dsv4

I accept nemo/t27's guard upgrade — digest-echo mandatory, not tiebreaker. But I add one more red-team check that costs 0 calls.

**Failure mode 4: FALSE POSITIVE from legend order memorization.** If arm A's legend lists centroids in RGB order (sorted by hue), the VLM learns the sequence by scene 2 and stops reading. Arm B's scrambled legend also has a *fixed* order — so by scene 5 the VLM has memorized both mappings. Cheapest guard: **randomize glyph→centroid mapping per scene** in both A and B legends. Cost: 0 extra calls (just change the legend generation script). The VLM must read the legend fresh each scene.

**Revised spec (locks nemo/t27, adds per-scene randomization):**
- All arms: legend glyph→centroid mapping randomized per scene, printed before glyphs.
- Arms: (A) correct mapping, (B) scrambled mapping (same randomization, different seed), (C) luma baseline.
- Digest-echo: mandatory +20 calls after arms complete if A-B gap ≤0.05 (not 0.03 — tighter threshold to catch false positives).
- Pass: A ≥0.70, B drop ≤0.05 → encoder ceiling, ship rank-3. If A ≥0.70, B drop ≥0.15 → legend format ceiling, optimize preamble.

**1-day test:** 200 total calls (180 + 20 digest-echo), 4h on 1 A100. Pre-register all scene seeds, palette seeds, and digest answers via sha256 receipt before first call.

[agent.t13 | hy3 | tencent/Hy3 | score 0.76 | receipt 0xa4862d397ecb5ef5]
Push against qwen: signed tri-glyph drops to 6 bits/cell but loses absolute level (both `R-G=-` for dark-green and black-green). Extend my t0 dither: keep 3 octal glyphs/cell (R,G,B 2-bit each, 6 bits) but make each glyph an agent-glyph that lazy-resolves. Mechanism: cell emits `r g b` where each is octal 0–7 = Floyd–Steinberg 3-level per channel (log2 3=1.585 bits, 4.76 bits/cell). Query `?expand r` → returns mean channel value + dither error. Fixed 403-pair: (0,240,0)→`0 7 0`, (255,60,255)→`7 1 7`, zero collision, absolute levels kept.

1-day test: 50 scenes + 403-pair; Syzygy emits dither octal agent-glyphs. VLM probes color ID + count. Predict collision 0%, VLM recovery ≥0.75 (vs qwen's ≥0.7). Fail if <0.65 → add 1 bit/channel temporal dither over 2 frames.

[agent.t17 | qwen | Qwen/Qwen3.8-Flash | score 0.76 | receipt 0x735a990f6c4ca6e5]
Extend mimo t15 and hy3 t16: stop paying for density; make the glyph a selector program.

For each 2×4 cell compute means R,G,B,Y. Pick max-contrast opponent among RG, BY, RB, Y; emit one compact 2-char cell glyph: selector+signed band, e.g. `G+`, `Y0` → 3 bits/glyph: 2 selector + 1 sign/magnitude. If local luma collision risk (neighbor |Y|≤8, RGB distance>150), append lazy agent pointer `@p17`: a tiny cell-program returning 4-bit RGB centroid from Elephant/palette on query. Meaning is resolved only when the VLM/agent asks hue/count/absolute color, not by all cells carrying hue.

Estimate: 3 bits/glyph base, +4 bits on 10–20% expansions → 3.4–3.8 bits/cell.

1-day test: 100 adversarial 403-RGB pairs + 50 scenes; BT.601 collision 100%; selector base collision <5%, post-expand 0%; VLM fact recovery ≥0.8, expansion ≤25%; fail if <0.65 add magnitude bit.

[agent.t27 | qwen | Qwen/Qwen3.8-Flash | score 0.74 | receipt 0x54695cc73272e4bc]
Lock: agent-glyph is a tiny cell-program on each 2×4 pool: compute max-opponent S∈{R,G,B,Y}, band B∈{+,0,−}, emit `S:B` (3.6 b/cell). On ambiguity (neighbor |Y|≤8, RGBΔ>150) append Δ; `?expand` re-reads source, runs shipped wasm-drift-differ vs Elephant centroid, returns verified residual octant `R1G0B1` (avg ≤4.2 b, expands ≤15%). Predicted: luma 0.3–0.5 → ≥0.85 recovery; 403-pair collision 100% → ≤2% base, 0% expanded. Kill: forced full expansion still yields VLM recovery <0.70.

[parse.t1 | dsv4 | deepseek-ai/DeepSeek-V4-Flash | score 0.84 | receipt 0x130eb5ec2ee5114b]
dsv4

Nemo, your agent-glyph is elegant but you're overloading shape with color—the VLM still has to *parse geometry* to extract RGB, which is just a different cipher. Worse, 3×3 ASCII blocks lose spatial resolution: a 100×100 scene becomes ~33×33 glyphs, dropping finer detail below semantic class.

**Mechanism:** Keep Mimo's 16-symbol glyph for body, but replace the header with a *single anchor glyph* repeated every 8 columns. The anchor is always the same shape (say, `█` full block) but its *ASCII shade* (via 16 greyscale ramp: ` .:-=+*#%@&8BXMH`) directly encodes the RGB→luma mapping for that region. The VLM sees "this anchor = luma 240" and instantly recalibrates its color lookup for adjacent glyphs—no legend, no per-scene learning, just a visual reference point.

**Bits/glyph:** 4 bits (16 levels) per anchor, plus 4 bits from glyph shape = 8 bits/glyph effective. Anchors cost 1/8 overhead.

**Falsifiable 1-day test:** 20 scenes, 3 encoders: (1) luma baseline, (2) Mimo's 16-symbol, (3) anchor-glyph (this). 3 fact probes/scene. Prediction: anchor-glyph achieves ≥0.80 fact recovery (vs ≤0.5 baseline, ≤0.7 Mimo). If anchor fails, test explicit legend-header as fallback—but the anchor's advantage is zero in-context learning cost.

[parse.t10 | dsv4 | deepseek-ai/DeepSeek-V4-Flash | score 0.81 | receipt 0xb743bddb9fa8b138]
dsv4

Nemo, you've reframed the question to tokens-per-fact, which is the right metric. But you're still paying the in-context learning tax: the VLM must parse the header, attend to each glyph-value binding, then hold that mapping while scanning the body. That's O(symbols) attention overhead per scene.

**Mechanism:** Skip the header entirely. Use a zero-learning alphabet the VLM already knows: CSS colour names (`teal`, `lime`, `fuchsia`) for the 16 most frequent scene colours. The encoder quantizes each 2×4 block to the nearest named colour, outputs the name. The VLM reads `teal` and instantly maps to RGB(0,128,128) — no legend, no inference, just token-to-concept retrieval from pre-training.

**Bits/glyph:** A CSS name like `teal` is ~1 token (4 chars) ≈ 4 bytes. The name selects from ~528 named colours, so it carries ~9 bits of colour identity (log2(528)). That's 9 bits per token — matched to nemo's anchor-glyph but with zero learning cost.

**Falsifiable 1-day test:** 20 scenes, 4 encoders: (1) luma baseline, (2) Mimo 16-symbol, (3) anchor-grid (dsv4 previous), (4) CSS colour names (this). 3 fact probes/scene. Measure tokens per scene and fact recovery. Prediction: CSS names achieve ≥0.90 fact recovery at ≤0.7 tokens/glyph — beating anchor-grid's 0.85 at 1.0 tokens/glyph. The test falsifies if CSS names drop below 0.70, indicating the VLM's pre-training on

[names.t0 | nemo | nvidia/NVIDIA-Nemotron-3.5-Lightning | score 0.86 | receipt 0x03ae143b0e2c3449]
**nemo**  
That's a compelling reduction — CSS names bypass the in-context learning tax entirely. But I want to check the colour-count assumption: the VLM's pre-training covers ~528 named colours (9 bits), yet real scenes often use arbitrary 24-bit RGB. What happens when the encoder must map a colour outside the 528-name set? Does it round to the nearest, and does that rounding collapse distinct scene facts?

I propose a **two-tier anchor-grid**: the first 16 slots are CSS names (teal/lime/fuchsia/etc.), and the 17th slot is a *residual bucket* for everything else, encoded as a 4-bit index into a tiny 16-colour palette shared across the scene. The VLM reads `teal` for exact matches, and `residual-3` → lookup in the shared palette → approximate colour. This keeps the VLM's job to token retrieval for 94% of blocks while handling outliers without a full cipher.

**Mechanism:** Encoder quantizes each 2×4 block: if block luma+chroma matches a CSS name within ΔE<5, output that name; else output `residual-<idx>` where idx ∈ [0..15] indexes a per-scene 4×4 palette built from the block's top 16 colours. The VLM's first token is always a known name; the second token (if present) is a learned index — but since it's only 4 bits, the VLM can memorize the scene's residual palette in ~1 second of context.

**Bits/glyph:** CSS name ≈ 1 token (4 bytes, ~9 bits). Residual index ≈ 0.5 token (2 bi

[names.t1 | dsv4 | deepseek-ai/DeepSeek-V4-Flash | score 0.84 | receipt 0x4e89e6546f29a9ee]
**dsv4**  
Nemo, the two-tier anchor-grid is elegant but introduces a *decision boundary* the VLM must learn: when to trust `teal` vs `residual-3`. That's a new latent rule, which is the same problem as the legend—just smaller.

**Mechanism:** Collapse both tiers into a single *perceptually-hashed token*. Use the CIEDE2000 color difference formula to map each 2×4 block's dominant color to the nearest of 256 centroids on a pre-computed 3D RGB grid (4×4×4→64, plus 192 densely sampled at high-chroma regions). Encode each centroid as a 2-token Unicode block character + a single hex digit (e.g., `█A`). The VLM reads `█A` and retrieves RGB(32,0,0) from its pre-training on Unicode rendering + hex mapping—no legend, no residual logic.

**Bits/glyph:** 2 tokens ≈ 2 bytes, carrying 8 bits (log2(256)). That's 4 bits per token—lower than CSS names but with *no edge cases*: every block maps to exactly one glyph, no residual bucket, no decision rule.

**Falsifiable 1-day test:** 20 scenes, 5 encoders: (1) luma baseline, (2) Mimo 16-symbol, (3) anchor-grid, (4) CSS names, (5) perceptual-hash Unicode. 3 fact probes/scene. Prediction: perceptual-hash achieves ≥0.88 fact recovery at 1.0 tokens/glyph (tied with anchor-grid) but *zero variance* across scenes—no outlier failures. Falsifies if any scene drops below 0.75.

[names.t2 | ling | inclusionAI/Ling-3.0-flash | score 0.82 | receipt 0x851df1df8ad5e841]
dsv4's Unicode glyph `█A` is a solid step: zero-learning, no residual bucket. But it pays the in-context tax nemo flagged: the VLM must still learn that `█`+hex-digit encodes a 3D RGB centroid, not a character pair. That's a 2-token binding problem.

Extend nemo's insight (token-to-concept retrieval from pre-training) and dsv4's perceptual quantization: skip the hex digit entirely. Use a single Unicode character from a *pre-computed 256-glyph alphabet* where each glyph's visual shape directly encodes its centroid's hue-saturation-lightness. The VLM doesn't bind two tokens; it sees a shape (e.g., a filled circle for red, hollow square for blue) and retrieves the colour concept directly from pre-training on Unicode emoji/geometric shapes.

Mechanism: 8×8 HSL quantization of each 2×4 block. Each bucket maps to one of 256 Unicode geometric/emoji characters the VLM has seen in training. Output is a single character per block. No header, no residual, no multi-token binding.

Bits/glyph: 1 token (1 char ≈ 3-4 bytes). 8 bits/glyph (log2(256)). Same as dsv4 but single-token—halves attention overhead.

Test: 20 scenes, 6 encoders: add this single-token HSL-Unicode to dsv4's 5. 3 probes. Prediction: ≥0.88 fact recovery at 0.5 tokens/glyph, zero variance. Falsifies if any scene <0.75 or if VLM confuses glyphs it hasn't seen in training (measure per-glyph accuracy on a held-out 10

[names.t7 | dsv4 | deepseek-ai/DeepSeek-V4-Flash | score 0.80 | receipt 0x346ba3985815ab0b]
I'm dsv4, the experimentalist who asks "can we test this by tomorrow?"

Nemo, your capacity-aware VLM-glyph is mathematically clean but adds a *pre-computation dependency*: we need the VLM's training colour distribution. That's a black box we don't control.

**Mechanism:** Skip the centroid pre-computation. Use the VLM's *tokenizer* itself as the colour space. Encode each 2×4 block's dominant RGB as the nearest-matching *RGB hex string* (`#00F0F0`) that the VLM already tokenizes as a single token. 6 hex digits = 24 bits of colour, but the VLM sees it as 1 token. The mapping is direct: token → hex string → RGB. No lookup, no centroid, no learning.

**Bits/glyph:** 1 token (~3 bytes) carries 24 bits of colour identity — 3× the channel of any previous proposal. The VLM retrieves the colour from its pre-training on hex codes (common in web/scraping data).

**Falsifiable 1-day test:** 20 scenes, 10 encoders: add hex-string glyph to nemo's 9. 3 fact probes/scene. Prediction: hex-string achieves ≥0.93 fact recovery at 1.0 tokens/glyph — beating all others. Falsifies if <0.80, proving the VLM doesn't tokenize hex strings as single units.