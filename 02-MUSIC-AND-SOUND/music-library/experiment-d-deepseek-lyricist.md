# Experiment D: DeepSeek vs M3 Lyricist Comparison

## Design

**Objective:** Determine whether different LLMs produce systematically different lyric quality for the same musical concept.

## Protocol

1. Use the same concept prompt for both models
2. Same temperature (0.93)
3. Same max tokens (2048)
4. Same system prompt (lyricist instructions)
5. Feed both lyric sets into music-3.0 with identical musical parameters
6. Compare file sizes (output density) and document lyrical differences

## Concept Prompt

```
Write song lyrics (2 verses, 1 chorus, 1 bridge, 1 outro — under 1100 characters total) inspired by this concept:

"The Cadence Caller Listens" — the idea that the best leaders don't dictate rhythm, they discover it. A marching formation already has a rhythm before the cadence caller opens his mouth. A jazz band already has a pocket before anyone counts off. The leader is a mirror, not a clock. Power granted beats power forced.

Include structural tags [Verse], [Chorus], [Bridge], [Outro].
The lyrics should be singable — regular meter, clear rhymes, concrete imagery.
Avoid clichés. Include at least one image that doubles as a structural description of the song itself.
```

## Musical Parameters (identical for both)

- Prompt: "Indie folk, fingerpicked guitar, subtle drums" (7 words)
- Key: A minor
- BPM: 78
- Vocals: warm female alto, intimate

## Models to Test

1. **MiniMax-M3** (temperature 0.93) — the project's established lyricist
2. **DeepSeek V3** (temperature 0.93) — alternative LLM, different training data
3. **GLM-5.2 agent** (hand-written, no API call needed) — the control

## Hypothesis

Based on the project's observations (session 4, finding #6; session 7, finding #5):
- M3 will produce more emotionally intuitive lyrics with recursive metaphors
- DeepSeek may produce more structurally precise lyrics (reflecting its coding-oriented training)
- The agent-written control will be more referential and essay-like

## Execution

When quota resets:

```bash
# M3 lyrics
mmx text chat \
  --system "You are a skilled lyricist who writes singable, emotionally vivid song lyrics with concrete imagery and recursive metaphors." \
  --message "user:Write song lyrics (2 verses, 1 chorus, 1 bridge, 1 outro — under 1100 characters total) inspired by this concept: The Cadence Caller Listens — the idea that the best leaders don't dictate rhythm, they discover it. Include structural tags. Singable meter. Avoid clichés." \
  --temperature 0.93 \
  --max-tokens 2048 \
  --output json --quiet > lyrics-cadence-m3.json

# DeepSeek lyrics (via mmx if DeepSeek is available, or via a different API)
# NOTE: mmx doesn't support DeepSeek directly. Need to use DeepSeek's own API.
# This experiment requires DeepSeek API access, which may need to be configured separately.
```

## Alternative: GLM Agent as Lyricist

Since DeepSeek API access may not be available through mmx, the experiment can be modified:
- Use GLM-5.2 (this agent) as the alternative lyricist
- Compare GLM-written lyrics vs M3-written lyrics for the same concept
- The GLM lyrics for "The Cadence Caller" are already written (lyrics-the-cadence-caller.txt)
- Generate M3 lyrics for the same concept when quota resets

This modified experiment is still valid — it compares two different LLM architectures (GLM vs MiniMax-M3) as lyricists.

## Priority

Medium. The experiment is designed and ready. The primary blocker is quota. Secondary blocker is DeepSeek API access (if the original design is preferred).
