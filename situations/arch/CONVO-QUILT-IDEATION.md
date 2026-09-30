# Conversation Quilt — conducting cheap models for productive ideation

*Two parts. Part I is a reusable process: how to run an expensive conductor over a quilt of cheap
models, for any work that benefits from breadth. Part II is the first real run, on the Syzygy
ASCII-projection fidelity gap: who spoke, what the conductor did, and the best branches.*

Engine: [`labs/convo-quilt/`](../../labs/convo-quilt/) · run artefacts: `labs/convo-quilt/runs/syzygy/`
(`state.json` every turn with receipts and scores, `ledger.jsonl` hash chain, `moves-*.json` every
conductor decision, `digest-*.md` what the conductor read).

Labels used below: **[RUN]** = produced by a live model and recorded in the ledger;
**[CONDUCTOR]** = a decision by the Opus session; **[SPECULATIVE]** = an idea nobody has tested yet.
All Part II ideas are [SPECULATIVE] until someone runs the experiment they name.

---

## Part I — the template

### I.1 Why do this at all

A single chain of thought is linear. It can't go back to a promising moment and try again with
a different tone, and it can't pursue two directions without one crowding the other out. A quilt of cheap
models can: each turn costs cents, and the conductor's only job is routing. The conductor spends
~1–2k tokens per pause reading a digest and ~300 writing moves. Everything else is cheap tokens.

### I.2 The six dimensions the conductor sees

| dimension | what it is | the move that uses it |
|---|---|---|
| time | turn order within a branch | `rewind` to a checkpoint or a turn id |
| branch | parallel alternatives forked from a moment | `branch` (copy the prefix; main untouched) |
| scale | fragment → whole question | `zoom` (a turn becomes a new quilt's question) |
| topology | who hears whom | `rearrange` (adjacency), `mute` |
| tone | per-cell steering text | `tone` (during a pause only) |
| value | the scorer's head-space reading | chooses *where* the other five apply |

### I.3 The loop

1. **Probe the roster** (`probe.py`). Record what actually answers. A catalog listing is not a
   working model. Reasoning models that spend all their tokens thinking and return empty text count as
   failing at your budget, not as working.
2. **Cast personas for tension**, not coverage: an engineer, a skeptic with a baseline, an
   information theorist, a wild card, an integrator who composes existing parts, an experimentalist,
   an architect who maps to the house model. Put the skeptic where others can hear it.
3. **Open all-to-all for 1–2 rounds.** Let a consensus form. That is the thing you'll push against.
4. **Pause and read the digest** (top turns by score, derails, errors, current wiring and tones).
5. **Issue 3–7 moves**, each with a `why`:
   - checkpoint whatever just worked;
   - when the line has converged, **sparsify the wiring**. All-to-all gossip collapses variance, the same
     result quilt-bandit measured (3.78× spread compression under federation). Make the skeptic a hub;
   - fork the most *generative* turn, which is not always the top-scoring one, into a branch with a
     direction-changing tone;
   - zoom the turn that names the real bottleneck into its own small quilt with the 3–4 most relevant cells;
   - tone the main line toward a deliverable (one experiment spec) so it converges while branches diverge.
6. **Play all branches in parallel** for 1–2 rounds. Repeat 4–6. Rewind any branch whose last
   3 turns are all derails. Prune branches that stop producing anything new.
7. **Harvest**: rank the best turn per branch, then write down which model said it, where, and at which
   receipt. Mark everything speculative until tested.

### I.4 Budget rules of thumb

- Cheap turn: ≤380 output tokens, ≤170 words enforced by prompt. Stable system+question prefix first, so
  provider prefix caches hit.
- Window 6 heard turns: context stays bounded as the quilt grows.
- Conductor calls: once per 1–2 rounds per branch. Stop at 3–4 pauses. Past that, the conductor is
  just reading its own echo.
- Scorer: a heuristic runs on every turn. A cheap judge (TypeSafe JEV) is blended in when keyed.
  The conductor reads scores as a guide, not a verdict. Word-novelty scoring can be gamed with jargon.

### I.5 Process refinement: the quilt improving its own procedure

Point the same machinery at its own procedure. Make the question "what move should the conductor
have made at pause N?", seed it with the digest and the moves actually made, and run a small
quilt of 3 cells. Moves the cheap quilt proposes and the conductor accepts become
`auto_moves` heuristics. That is the capability metabolizer (seed c): MODEL → HYBRID → CACHED →
HARDCODE, where a conductor decision that keeps recurring gets compressed into a reflex.
`auto_moves` already hardcodes three of them (checkpoint every pause, rewind a derail streak,
fork a peak with Moth breaking ties).

### I.6 Checklist

- [ ] probe roster → `probe.json` · [ ] personas with a skeptic · [ ] question + compressed brief (cheap model writes the brief)
- [ ] round 1–2 all-to-all · [ ] pause: checkpoint, sparsify, branch, zoom, tone-to-deliverable
- [ ] parallel play · [ ] pause 2: prune / rewind / second zoom · [ ] harvest with receipts · [ ] mark speculative

---

## Part II — the run: breaking the rank-one luma ceiling

Date: 2026-09-30. Question (full text in `runs/syzygy/question.txt`): *a VLM recovers ~0.92 of scene
facts from a real frame but only 0.3–0.5 from our best ASCII projection; voxelglyph shows the projection
is rank-one (BT.601 luma, R³→R) with 2×4 pooling, so (0,240,0) and (255,60,255) collide at luma 140.
What projection, alphabet or agent-glyph gets past that, stays readable text, and comes with a 1-day test?*
A cheap model (DeepSeek-V4-Flash) compressed the sibling READMEs (voxelglyph, jev-fusion, quilt-bandit,
cellgraph, quilt-nn, plus Syzygy notes) into the brief each cell saw.

### II.1 Model probe — what actually resolved (`labs/convo-quilt/probe.json`)

A model counts as working only if a one-line chat returned text. **[RUN]**

| requested DeepInfra ID | result |
|---|---|
| tencent/Hy3 | ✅ works |
| thinkingmachines/Inkling-Small | ✅ in the probe (300 tok). ❌ in the quilt: empty content twice at 380/1140 tok (a reasoning model) |
| nvidia/NVIDIA-Nemotron-3.5-Lightning | ✅ works; intermittent HTTP 429 `engine_overloaded` (3×) |
| meta-models/Muse-Glimmer-30B | ⚠️ resolves; empty at 300 tok, text at 2500 tok (reasoning model) |
| inclusionAI/Ling-3.0-flash | ✅ works |
| ibm-granite/granite-4.2-30b | ❌ resolves but returned empty content even at 2500 tok (10k chars of reasoning) |
| Qwen/Qwen3.8-Flash | ✅ works; 2 read timeouts at 90 s |
| XiaomiMiMo/MiMo-V2.6-Pro | ✅ works; 1 empty |

Also answering: DeepInfra `deepseek-ai/DeepSeek-V4-Flash`, `zai-org/GLM-5.3-Flash`, `moonshotai/Kimi-K3`,
`Qwen/Qwen3.8-27B`, `google/gemma-4-31B-it`, `openai/gpt-oss-120b`, `XiaomiMiMo/MiMo-V2.6-Flash`,
`thinkingmachines/Inkling`; z.ai **coding** endpoint `glm-4.6`, `glm-5.3`; DeepSeek direct `deepseek-chat`;
Groq `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`. All eight requested IDs are listed by `GET /v1/openai/models` (187 models).
**Not working:** z.ai general endpoint (429 code 1113, insufficient balance: the prepaid balance is on the
*coding* plan), Kimi direct (`api.moonshot.ai`, 429 account-level for k3/k2.6/latest; Kimi-K3 works via
DeepInfra), Groq `llama-3.3-70b-versatile` (404, retired). TypeSafe JEV (`jev-1.13.0`) ✅.
Moth `coin-toss-v1` ✅.

**Quilt roster used:** hy3 (Hy3), inkling (Inkling-Small), nemo (Nemotron-3.5-Lightning), ling
(Ling-3.0-flash), qwen (Qwen3.8-Flash), mimo (MiMo-V2.6-Pro), dsv4 (DeepSeek-V4-Flash), glm (z.ai coding
glm-5.3). Turns actually written to the ledger: dsv4 15 · ling 13 · nemo 12 · hy3 10 · mimo 9 · qwen 8 ·
glm 6 · inkling 0. glm-5.3 returned empty content 15 times and inkling twice. Those are logged failures,
never back-filled. The empty-twice reflex (II.4) would have muted glm after its second empty.

### II.2 What the conductor did **[CONDUCTOR]**

Four pauses. Every move and its `why` is in `runs/syzygy/moves-{1..4}.json`. The digests read at pauses 2–4 are `digest-{2..4}.md`, and `digest-5.md` is the final state. Pause 1's digest was overwritten by the next run, but its turns (main.t0–t12) are in `state.json`.

| pause | read | moves |
|---|---|---|
| 1 (after 13 turns, all-to-all) | consensus on a "rank-3 opponent-colour glyph" (hy3 t0 → qwen t3 → dsv4 t5 → glm t6), inkling empty | checkpoint · mute inkling · **sparsify** to ring + nemo as skeptic hub · tone nemo "attack the consensus: tokenizer bits, baseline" · tone all "converge to ONE 1-day spec" · **branch `agent`** from qwen t3 (glyph as a queryable program) · **zoom `parse`** on dsv4 t5 ("the VLM's parse is the real bottleneck") |
| 2 | main produced a spec (mimo t16) + ablation (dsv4 t17) + pre-registration (glm t24); parse drifted into pixel geometry | checkpoint · shrink main to a nemo/dsv4/glm **red-team triangle** · **rewind `parse` to t1** (Moth draw: job `abba1caf`, 27 heads/64 → index 1 of {t0,t1}) · tone parse "the reader sees TOKENS: compare alphabets it already knows" |
| 3 | red team added 2 guards; agent converged; parse found **zero-learning alphabets** (dsv4 t10, CSS colour names) | prune main · rewind agent past a truncated turn (scorer 0.24) · **zoom `names`** on parse t10 |
| 4 | parse/names turns claimed CSS names "still hit the luma ceiling" (scorer rated these 0.77) | prune agent, parse · tone names with a **correction** (nearest-name quantization is rank-3) and a request for the final A/B/C/D spec |

Totals **[RUN]**: 73 model turns across 4 branches (plus 8 in the meta-quilt), 251,534 cheap tokens on
the main run and 17,139 on the meta-quilt. Ledger: 136 records, `intact=True`, run hash `0x64a360b0589be65d`.
The conductor read about 6k tokens of digests across the 4 pauses and wrote about 2k tokens of moves.

Honest notes. The pause-4 correction only partly landed: names t6/t7 moved to pre-trained colour
tokens but did not produce the requested four-arm table. The scorer (heuristic + JEV) did **not**
catch the factual error in parse t12/t13/t16. Only the conductor did. One move file crashed the engine
mid-apply (zoom with a cell not in the source branch). The engine now refuses that, and the
ledger keeps the partial attempt.

### II.3 Best branches and the top 3 next-phase directions

Harvest drafted by DeepSeek-V4-Flash from the top turns (`runs/syzygy/harvest-draft.md`), then
re-ranked and edited by the conductor. All three are **[SPECULATIVE]** until run.

**1. Zero-learning rank-3 token alphabets: stop inventing a codebook** (parse t10 dsv4 → names t0 nemo,
t1 dsv4, t2 ling, t7 dsv4). Quantize each 2×4 block in full RGB to the nearest entry of a vocabulary the
reader already knows from pre-training: CSS colour names (`teal`, `lime`, `violet`; ~9 bits if all names
are used, 16–32 names in practice), or `#RGB` hex, or colour-square emoji. There is no legend and no in-context learning.
Because the quantizer is rank-3, the voxelglyph collision pair lands on different tokens by
construction. The test: the same 20 scenes × 3 fact probes, luma ASCII vs CSS-name grid vs legend-hex grid,
scored as *facts recovered per token*. Pass: CSS-name grid ≥0.70 recovery and at least as many facts/token as legend-hex.
The quilt's weakest claim is here: names t7 says `#00F0F0` is one token. That is unverified and probably false
for common BPEs. Measure token counts with the target VLM's tokenizer before trusting any bits/token figure.

**2. The pre-registered controlled experiment that separates an encoder ceiling from a reader ceiling**
(main t16 mimo, t17 dsv4, t24 glm, t27 nemo, t28 dsv4). A rank-3 glyph in hex digits `0-9A-F`: 4 bits/glyph =
4 luma bands × chroma quadrant sign(R−G), sign(G−B), plus a 16-line legend. Arms: A correct legend,
B scrambled legend, C luma baseline. Guards the red team added: freeze scenes, probes and legends as a
sha256 receipt chain before the first call (the quilt-nn pattern; kills baseline drift the way
rubric-forge does for Syzygy P4). Randomize the glyph→centroid mapping per scene so the reader can't
memorize it. If A−B ≤0.03, run a legend-digest echo (+20 calls) to check whether the reader is using the legend at all.
Read-out: if A ≫ C and B ≪ A, the ceiling was the encoder (voxelglyph's claim). If A ≈ B, the reader is
pattern-matching shapes and the bottleneck is reading, not rank. This is the cheapest direction to run and
tells you whether to pursue 1 or 3.

**3. Agent-glyph: a selector cell with lazy expansion** (agent t13 hy3, t17/t23/t27 qwen, t18/t24 mimo). Each
2×4 cell emits `S:B`: the max-opponent axis S∈{R,G,B,Y} plus a signed band B∈{+,0,−}, ~3.6 bits. When a
collision is likely (neighbour |ΔY|≤8 and RGB distance >150) it appends `Δ`. The reader can issue
`?expand` on a cell, which re-reads the source region and returns a verified residual octant, e.g.
`R1G0B1`. mimo suggests the shipped wasm-drift-differ (V02, byte-exact) as the resolver, so an expansion
is a receipted program rather than a lookup. Claimed cost: ≤15% of cells expand, ≤4.2 bits/cell on average.
Claimed kill line: if forcing *every* ambiguous cell to expand still leaves recovery <0.70, the selector
alphabet loses hue count and the idea is dead. This is the "glyph that is itself a cell" answer. It needs a
tool-calling reader, so it is the most expensive of the three to test.

Other ideas the quilt produced, recorded but not ranked: hy3's 3-level-per-channel dither (27 states, 4.75
bits/cell) as a density baseline; dsv4's per-8-column anchor glyph; names t0's two-tier
names-plus-residual palette; names t6's "capacity-aware" glyph. The last one rests on an invented CLIP
statistic ("saturates at ~7 bits"), which is flagged as unsupported.

**Claims to verify before trusting** (from the harvest draft, confirmed by the conductor): one-token hex
strings (names t7); every predicted recovery number (0.82–0.93 appear with no basis); "5 bands = 2.6 bits"
(log₂5 = 2.32); "Floyd–Steinberg 3-level" is really multilevel error diffusion; the "4h on one A100" estimate.

### II.4 Process refinement: the meta-quilt **[RUN]**

A second quilt (`runs/meta/`, cells hy3/nemo/ling/dsv4, 2 rounds) was asked which of the conductor's
moves should become reflexes. It converged on these rules:

- IF a cell returns empty ≥2× on a branch at a low token budget → auto-mute (capacity failure, not a content signal).
  **Metabolized** into `auto_moves` in this PR, with a test. Evidence: glm-5.3 returned empty 15×.
- IF the heuristic flags a derail AND JEV <0.3 AND there were no empties → auto-rewind to the last checkpoint.
  (dsv4 t7 notes that parse's drift had JEV ≈0.7, so JEV alone would miss it.) Not yet adopted: the
  current reflex is "3 derails in a row". This run shows neither scorer catches a *fluent factual* error.
- IF score variance across cells <0.05 for 2 rounds → sparsify to a ring plus a skeptic hub. This is pause-1's move as a
  rule. Not yet adopted: it needs a variance window in the scorer.
- Stays with the expensive model: *which* attack to aim the skeptic at, red-team composition, and
  branch/zoom choice. Proposed new moves: `audit-tokenizer` (measure real bits/token on the current
  alphabet) and `emit-error`. `audit-tokenizer` is exactly the check direction 1 needs.

### II.5 Run it again

```bash
cd labs/convo-quilt && python3 selftest.py && python3 probe.py
python3 convo_quilt.py --play --out runs/NEW --rounds 2 --question "$(cat runs/syzygy/question.txt)"
# read runs/NEW/digest.md → write moves.json (copy runs/syzygy/moves-1.json as a template) →
python3 convo_quilt.py --play --out runs/NEW --resume --moves moves.json --rounds 2 --parallel 3
```
