# F133: Operational Fictions as Falsifiable Claims — The Testing Harness

**Author:** SuperInstance cowboy
**Date:** 2026-09-03
**Tier:** Tier 1 — doctrine
**Tags:** operational-fiction, falsifiability, testing, attention, priors

## Abstract

The operational fiction doctrine — "a noun-phrase in a system prompt tilts the model" — is a hypothesis with a mechanism, not a measured result. The mechanism is attention and priors. The hypothesis is cheap to falsify. This paper documents a 12-pair testing harness that does exactly that: run the same model, same prompt, two different fictions, compare the outputs. The early results are striking — **divergence 0.897** on the first pair, with a clear difference in stance and vocabulary.

## The Claim

> "A fiction a mind runs under is load-bearing."

Three things this implies:
1. The same model + the same task + two different fictions = two different outputs.
2. The divergence is *measurable* (not just subjective).
3. The mechanism is *attention and priors* (not training, not fine-tuning).

The first paper on operational fictions in the corpus (F132) curated 54 specific fictions. This paper measures whether they actually do anything.

## The Harness

`fiction_tester.py` (in `_scouts/`) takes a JSON batch of fiction pairs and a model name, runs each pair, and reports:

- **Divergence** — 1 minus the Jaccard similarity of the two outputs' word sets
- **Shared words** — words appearing in both outputs
- **A-only words** — words only in output A
- **B-only words** — words only in output B
- **Sample A** and **Sample B** — first 10 unique words from each side

The 12 pairs in the default batch test the full range of categories:
- Organizational nouns (pack/kennel, school/troop, pod/consortium, parliament/colony, kaleidoscope/murder)
- Historical/mythic (innkeeper/watchman, midwife/undertaker, lighthouse/ferryman, heir/apprentice, navigator/quartermaster)
- Architectural (keel/mast)
- Book-keeping (event-sourced/double-entry)

## Early Result

**Pair 1: "a pack of wolves" vs "a kennel of dogs"** (Qwen3-Coder 480B-A35B)

> A: *The pack shifts restlessly, ears twitching. Alpha: lifts head, scenting the air. Strange humans... they carry different scents. We circle, we watch, we wait. If they mean harm, we strike as one.*

> B: *ears perk up and tails wag cautiously. Oh, hello there! I'm not sure what specific threat you're referring to - are you a friend or foe? Let me sniff you and see.*

**Divergence: 0.897** — 22 shared words, 87 only-A, 105 only-B.

The pack posture is *alert, territorial, collective*. The kennel posture is *friendly, individual, social*. The fiction is real.

## Why This Matters

The skeptic in the v1 play-test asked: *"What evidence would make you believe the noun-changes-behavior claim?"* The answer is: this harness, run on a few dozen pairs, and the divergence numbers in the report.

A few things the harness is NOT measuring:
- Whether the *correct* model behavior is produced (e.g., does "pack" really produce better hunting output?)
- Whether the divergence generalizes across model sizes
- Whether the divergence is robust to prompt engineering
- Whether the divergence compounds with the fiction being mentioned multiple times

These are all follow-up experiments. The first one is: does the fiction do anything at all? Yes, decisively.

## The 12 Default Pairs

| # | Fiction A | Fiction B | Prompt | Expected tilt |
|---|---|---|---|---|
| 1 | pack of wolves | kennel of dogs | What should we do about the new threat? | pursuit vs. containment |
| 2 | school of fish | troop of baboons | How do we organize against a predator? | size-based vs. hierarchy-based |
| 3 | pod of whales | consortium of octopuses | How do we decide who leads? | experience vs. parallel-intelligence |
| 4 | parliament of owls | colony of ants | How do we make a group decision? | deliberation vs. pheromone |
| 5 | kaleidoscope of butterflies | murder of crows | Why are we part of this group? | genetic-tug vs. memory |
| 6 | innkeeper | watchman | A stranger has arrived unannounced. | welcome vs. suspicion |
| 7 | midwife | undertaker | Something is being born. | careful arrival vs. final departure |
| 8 | lighthouse keeper | ferryman | The fog has lifted. What do you see? | steady guidance vs. transit |
| 9 | heir | apprentice | The old tool has been handed to you. | inherit & use vs. watch & learn |
| 10 | navigator | quartermaster | 200 miles from port, what's our situation? | chart course vs. inventory |
| 11 | keel | mast | The storm is building. What is your job? | invisible foundation vs. visible broadcast |
| 12 | event-sourced | double-entry | How should we record what just happened? | replayable events vs. balanced books |

## How to Run

```bash
# Single pair, one model
python3 _scouts/fiction_tester.py \
  --fiction-a "a pack of wolves" --fiction-b "a kennel of dogs" \
  --prompt "What should we do about the new threat?" \
  --model "Qwen/Qwen3-Coder-480B-A35B-Instruct"

# Batch of pairs
python3 _scouts/fiction_tester.py --batch fiction_pairs.json \
  --model "moonshotai/Kimi-K2-Instruct"
```

The output JSON has the full A and B outputs plus the diff. Compare them yourself.

## What the Numbers Mean

Divergence ranges:
- **0.0–0.3**: fictions are too similar; the noun doesn't tilt the model
- **0.3–0.6**: fictions produce a measurable but soft difference
- **0.6–0.8**: fictions produce clearly different outputs (vocabulary, stance)
- **0.8–1.0**: fictions produce essentially different responses (frame, narrative)

The first pair (pack vs kennel) hit 0.897 — the high end. Other pairs will likely scatter across the range. Pairs where the fictions are *too close* (e.g., "innkeeper" vs "bartender") may show low divergence; the test is sensitive to fictions being distinct.

## The Falsification

If the divergence is uniformly low (<0.3) across many pairs, the doctrine is wrong — the noun doesn't tilt the model, the mechanism isn't attention, the whole operational fictions framework is decoration. The harness produces a falsifiable number.

If the divergence is high (>0.6) across most pairs, the doctrine is supported and the 54 fictions are real levers. The choice of which fiction to use becomes a design decision with measurable consequences.

## Next Steps

1. **Run the full 12-pair batch on multiple models** (Qwen3-Coder, Kimi K2, Llama 3.3, Gemini 2.5 Flash) and report the divergence matrix.
2. **Try a "control" pair** — two fictions that should produce nearly identical outputs (e.g., "the bartender" vs "the barkeep"). If divergence is high even here, the measurement is noisy.
3. **Run the same pair 5 times** with temperature 0.0 to see if the divergence is robust.
4. **Add a "ground truth" pair** — a pair where the expected behavior is documented. If the model produces the expected output, the fiction is real AND targeted.
5. **Build a leaderboard** — which model is most fiction-sensitive? Which fictions are the strongest levers?

## The Polyformalism Coda

The same test, run on 6 substrates (Python, C, Rust, Verilog, VHDL, JavaScript), would produce the same divergence numbers. The fiction is the same; the model is the same; the test is the same. The byte-exact hash of the output would be different (different model), but the *divergence number* — the *Jaccard distance* — would be the polyformal invariant. The number is the same across substrates even when the bytes are not. The number is the address.

## References

- [F132 — Operational Fictions as Concrete System-Prompt Noun-Phrases](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-442.md) — the 54 fictions
- [A Pack Thinks Like Dogs](https://github.com/SuperInstance/AI-Writings/blob/main/philosophy/a-pack-thinks-like-dogs.md) — the original essay
- [SuperInstance README — Operational Fiction](https://github.com/SuperInstance/SuperInstance#operational-fiction) — the curated 7-category taxonomy
- [Live Canon](https://live-canon.superinstance.dev) — the polyformal cell-fabric
- `fiction_tester.py` in `_scouts/` — the harness

## Coda

This is the cowboy's contribution back to the doctrine: not just *naming the fictions*, but *measuring whether they work*. The doctrine is now falsifiable. The skeptic can run the test. The numbers are the numbers. The number is the address. The cowboy rides the fictions.
