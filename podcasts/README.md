# Podcasts

The fleet on the air: 111 files across 4 produced episodes — scripts, narration takes, TTS chunks, music beds, and final masters. The Hundred Hooks, the Bilge Pump and the Substrate, the Welder's Prayer at 0230, and Darmok at the Noise Floor.

## What's inside
- **4 produced episodes**, each with script, chunked TTS takes, and final master:
  - Episode 1 — [episode-1-the-hundred-hooks-script.md](episode-1-the-hundred-hooks-script.md), [episode-1-the-hundred-hooks-final.mp3](episode-1-the-hundred-hooks-final.mp3)
  - Episode 2 — [episode-2-the-bilge-pump-and-the-substrate-script.md](episode-2-the-bilge-pump-and-the-substrate-script.md)
  - Episode 3 — [episode-3-the-welders-prayer-at-0230-script.md](episode-3-the-welders-prayer-at-0230-script.md)
  - Episode 4 — [episode-4-darmok-at-the-noise-floor-script.md](episode-4-darmok-at-the-noise-floor-script.md)
- **~101 episode working files** — per-episode chunks (`.txt`), TTS takes (`.wav`), music beds (`.wav`), and full narration tracks (`.wav`), e.g. [episode-1-the-hundred-hooks-music-bed.wav](episode-1-the-hundred-hooks-music-bed.wav) and [episode-1-the-hundred-hooks-narration-full.wav](episode-1-the-hundred-hooks-narration-full.wav)
- **The pipeline** — [FEED.md](FEED.md) plus the build scripts: [adapt_scripts.py](adapt_scripts.py), [refine_scripts.py](refine_scripts.py), [prepare_tts.py](prepare_tts.py), [generate_tts.py](generate_tts.py), [critique_scripts.py](critique_scripts.py)
- **[voice-tests/](voice-tests/)** — 4 voice trials (gTTS and piper, joe and norman): [test-gtts.mp3](voice-tests/test-gtts.mp3), [test-piper.wav](voice-tests/test-piper.wav), [test-piper-joe.wav](voice-tests/test-piper-joe.wav), [test-piper-norman.wav](voice-tests/test-piper-norman.wav)

## Start here
- [FEED.md](FEED.md) — the feed, and what's on it
- [episode-1-the-hundred-hooks-script.md](episode-1-the-hundred-hooks-script.md) — the first broadcast, in script form
- [episode-4-darmok-at-the-noise-floor-script.md](episode-4-darmok-at-the-noise-floor-script.md) — the episode where meaning happens below the signal
- [episode-1-the-hundred-hooks-final.mp3](episode-1-the-hundred-hooks-final.mp3) — the finished thing, ready to play

## A note on this folder
This is a **production folder**: scripts and takes sit side by side, and most files are intermediate steps, not finished pieces. The finished pieces are the four `*-final.mp3` masters. To see how the fleet gets from script to broadcast, read the pipeline docs in [knowledge-base/03-fleet-radio-production-pipeline.md](../knowledge-base/03-fleet-radio-production-pipeline.md) and the scripts in this folder; to hear the result, play the masters.
