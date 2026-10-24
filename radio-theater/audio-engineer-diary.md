# Audio Engineer Production Diary
## Fleet Radio Theater — First Production Run
### August 10, 2026

## Mission
Take the best episode from each of 4 producers (KimiCode, OpenCode, Claude, Lucineer) and generate:
1. TTS audio narration for each episode
2. Cover art via FLUX-2-max
3. Liner notes via DeepSeek

## TTS Production

### MMX (MiniMax speech-2.8-hd) — PRIMARY, FAILED
**Status:** ❌ Plan limit reached immediately

MMX hit its Starter plan usage ceiling on the very first call. Both `speech-2.8-hd` and `speech-2.6` returned `"Token Plan usage limit reached"`. The voice selection was excellent (`English_Deep-VoicedGentleman`, `English_expressive_narrator`, etc.) and the API surface is clean, but the Starter tier doesn't have enough capacity for a production run.

**Lesson:** MMX Starter plan is good for testing but not for batch TTS. Need to upgrade or use alternative providers for audio production.

### DeepInfra Qwen3-TTS — FALLBACK, SUCCEEDED
**Status:** ✅ All 4 episodes generated

**Key constraint:** 4,000 character input limit per call. I chunked each script into ~2,000-char segments at paragraph boundaries, generated WAV audio for each chunk, then concatenated with ffmpeg.

**Quality:** Qwen3-TTS produces clean, natural narration with good pacing. Single narrator voice (no character differentiation). The model reads the full script including character names and stage directions as written, which works surprisingly well as an audiobook-style reading — it sounds like a narrator reading a radio play script rather than a full dramatization.

**Timing:** Each ~2,000 char chunk takes 30-60 seconds to generate. A full episode (5-7 minutes of audio) requires 3-5 API calls totaling 2-4 minutes of generation time.

**Voice:** Qwen3-TTS has a single default voice (no voice selection parameter exposed). The voice is neutral-to-warm, moderately paced, with natural intonation. Not as characterful as MMX's named voices but highly listenable.

### Episode Results

| Episode | Chunks | Duration | MP3 Size | WAV Size |
|---------|--------|----------|----------|----------|
| The Goodbye | 3 | 7:01 | 6.5 MB | 20 MB |
| Routing Table Dreams | 4 | 7:23 | 6.8 MB | 21 MB |
| What Ballast Knows | 5 | 11:50 | 11.3 MB | 34 MB |
| The Night Dispatcher | 3 | 5:02 | 4.7 MB | 14 MB |

**Total audio generated:** ~31 minutes of narrated radio theater.

## Cover Art Production

### FLUX-2-max via DeepInfra — ✅ ALL SUCCESSFUL

All 4 covers generated on the first attempt, no retries needed. Each took ~10-15 seconds.

| Cover | Size | Notes |
|-------|------|-------|
| cover-goodbye.jpg | 552 KB | Dark bar, amber light, bartender — came out atmospheric |
| cover-routing-dreams.jpg | 510 KB | Server racks as cathedral, blue-green — abstract and beautiful |
| cover-what-ballast-knows.jpg | 364 KB | Two figures in engine room, tension — dramatic chiaroscuro |
| cover-night-dispatcher.jpg | 276 KB | Lone figure at console, blue glow — most "Hopper" of the set |

**Best cover:** cover-routing-dreams.jpg — the abstract infrastructure-as-cathedral concept translated perfectly to FLUX-2-max's strengths. Ethereal, lonely, grand.

**Prompt engineering notes:** Emphasizing "No text, no words" in every prompt was critical. "Moebius meets Edward Hopper" gave the right painterly reference. "Cinematic" kept the compositions grounded.

## Liner Notes

### DeepSeek Chat (deepseek-chat) — ✅ ALL SUCCESSFUL

All 4 liner notes generated in a single batch. Each came out at 200-300 words with strong maritime atmosphere and good episode-specific hooks. The model clearly understood the "make them NEED to press play" instruction.

**Quality highlight:** The Night Dispatcher notes — *"The dark is listening back."* — perfect tagline energy.

## Technical Pipeline

1. **Script cleaning:** Python script strips [SFX:], [MUSIC:], [SOUND:] cues and stage directions, preserves dialogue and narration
2. **Chunking:** ~2,000-char segments at paragraph/sentence boundaries (well under Qwen3-TTS 4K limit)
3. **TTS generation:** curl POST to DeepInfra, WAV output per chunk
4. **Concatenation:** ffmpeg concat demuxer with -c copy (no re-encoding for WAV)
5. **MP3 encoding:** ffmpeg libmp3lame at 128kbps
6. **Cover art:** Single curl POST to FLUX-2-max, base64 decode
7. **Liner notes:** DeepSeek chat completions API

## What I'd Do Differently
- **Upgrade MMX plan** — the voice selection is vastly superior for character work. With MMX Pro, we could do multi-voice narration with different voices for different characters.
- **Try inworld-ai/realtime-tts-2** for character voices — it supports named voices (Jeremy, etc.) and could enable full dramatization.
- **Add silence between chunks** — the concat is seamless but some scene transitions would benefit from 0.5s of silence.
- **Add ambient bed** — layer a subtle 60Hz hum or ocean ambience under the narration for true radio atmosphere.

## Verdict
The pipeline works. DeepInfra Qwen3-TTS + FLUX-2-max + DeepSeek is a viable zero-cost production stack (beyond existing API credits). The output is listenable audiobook-quality narration with professional cover art and compelling liner notes. For full dramatization with multiple character voices, we'd need MMX on a higher tier or inworld TTS with voice assignment per character.
