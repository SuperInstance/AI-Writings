<!-- drafted by deepseek-ai/DeepSeek-V4-Flash via DeepInfra, tokens {'in': 5830, 'out': 1290} -->
# Harvest: Breaking the Rank-One Luma Ceiling in ASCII Frame Projection

## 1. Narrative of Idea Evolution

The brainstorm began with **hy3 (main.t0)** proposing a 2-bit/channel ordered-dither glyph alphabet to replace luma pooling, predicting 9 bits/cell vs luma's ~2.6. **qwen (main.t3)** reframed this as a rank-3 agent-glyph answering three 2-bit questions per cell, targeting 6 bits/cell with signed tri-glyphs. **mimo (main.t16)** locked the spec to hex digits `0-9A-F` (verified single tokens) with 4 bits/glyph from chroma signs + luma bands, adding entropy measurement guardrails. **dsv4 (main.t17)** introduced the critical legend-ablation arm to test whether VLMs actually use the legend vs pattern-matching glyph shapes. **nemo (main.t27)** upgraded this to a mandatory digest-echo test, and **dsv4 (main.t28)** added per-scene randomization of glyph→centroid mapping to prevent order memorization. The **agent** branch (agent.t13, agent.t17, agent.t27) explored lazy-resolving cell-programs, while the **parse** branch (parse.t1, parse.t10) proposed anchor-glyphs and CSS colour names. The **names** branch (names.t0–names.t7) converged on perceptual-hashed Unicode and hex-string glyphs, with dsv4 (names.t7) proposing the simplest testable mechanism: encode RGB as hex strings (`#00F0F0`) that VLMs already tokenize as single tokens.

## 2. Next-Phase Directions

### Direction 1: Hex-String Glyph (names.t7)
**Mechanism:** Encode each 2×4 block's dominant RGB as the nearest-matching hex string (`#00F0F0`) that the VLM tokenizes as a single token. 24 bits of colour identity per token—3× the channel of any previous proposal. No lookup, no centroid, no learning.
**Claimed bits/glyph:** 24 bits (1 token)
**1-day falsifiable test:** 20 scenes, 10 encoders including hex-string glyph. 3 fact probes/scene. **Pass:** ≥0.93 fact recovery at 1.0 tokens/glyph. **Fail:** <0.80 recovery.
**Source turn ids:** names.t7

### Direction 2: Perceptual-Hash Unicode (names.t1, names.t2)
**Mechanism:** Map each 2×4 block's dominant colour to the nearest of 256 centroids on a pre-computed 3D RGB grid. Encode as a single Unicode geometric/emoji character whose visual shape encodes hue-saturation-lightness. No header, no residual, no multi-token binding.
**Claimed bits/glyph:** 8 bits (1 token)
**1-day falsifiable test:** 20 scenes, 6 encoders including this single-token HSL-Unicode. 3 probes. **Pass:** ≥0.88 fact recovery at 0.5 tokens/glyph, zero variance. **Fail:** any scene <0.75 or VLM confuses unseen glyphs.
**Source turn ids:** names.t1, names.t2

### Direction 3: Rank-3 Hex Digit with Legend Ablation (main.t28)
**Mechanism:** Locked spec: hex digits `0-9A-F` (1 token/glyph), rank-3 encoder (2 chroma signs + 4-band luma), per-scene randomized glyph→centroid mapping. Three arms: correct legend, scrambled legend, luma baseline. Mandatory digest-echo test if A-B gap ≤0.05.
**Claimed bits/glyph:** ≥3.2 measured entropy
**1-day falsifiable test:** 200 total calls (180 + 20 digest-echo), 4h on 1 A100. **Pass:** A ≥0.70, B drop ≤0.05 → encoder ceiling. **Fail:** A <0.60 on any arm → reader parsing bottleneck.
**Source turn ids:** main.t16, main.t17, main.t27, main.t28

## 3. Claims to Verify Before Trusting

- **names.t7:** "6 hex digits = 24 bits of colour, but the VLM sees it as 1 token" — unverified. Need to test tokenizer behavior for `#00F0F0` across GPT/Claude/Llama BPEs. If split into multiple tokens, claimed 24 bits/glyph collapses.
- **main.t0:** "9 bits/cell vs luma's ~2.6 (log2 5 brightness bands)" — luma's 5 bands gives log2(5)=2.32 bits, not 2.6. Minor but propagates.
- **main.t3:** "6 bits/cell (≈4–5 effective bits after Markov prior)" — the Markov prior reduction is unquantified; no evidence given for 4–5 range.
- **names.t0:** "528 named colours (9 bits)" — log2(528)=9.04 bits, correct, but "94% of blocks" match within ΔE<5 is an unverified assumption about real scene colour distributions.
- **names.t7:** "≥0.93 fact recovery" — no baseline or mechanism justifies this specific number; appears aspirational.
- **agent.t13:** "log2 3=1.585 bits, 4.76 bits/cell" — 3 levels per channel × 3 channels = 3^3=27 states, log2(27)=4.75 bits, correct. But "Floyd–Steinberg 3-level per channel" is undefined (standard Floyd-Steinberg is 2-level).
- **main.t28:** "200 total calls, 4h on 1 A100" — unverified throughput estimate; actual VLM inference time depends on model size and sequence length.