# Technical Note: Bitrate Control in MiniMax music-3.0

*Session 30 addendum*

---

The `--dry-run` flag reveals the API request structure. The audio settings for all prior sessions:

```json
{
  "format": "mp3",
  "sample_rate": 44100,
  "bitrate": 256000
}
```

256,000 bits per second = 32,000 bytes per second. Our measured 32,040-32,080 B/s across 36 tracks includes ~0.15% MP3 framing overhead.

## Bitrate is Configurable

The `--bitrate` flag accepts custom values. A dry run at 128,000 bps confirms the setting is passed through to the API:

```json
{
  "format": "mp3",
  "sample_rate": 44100,
  "bitrate": 128000
}
```

This means future experiments could:
1. **Use variable bitrate (VBR)** — if supported, this would make file size a function of actual audio complexity
2. **Use lower bitrates** — to test whether the model's output quality changes with available bandwidth
3. **Compare bitrates** — generating the same song at 128kbps vs 256kbps to measure quality vs size tradeoffs

## Impact on Prior Findings

All 36 tracks across Sessions 23-29 used the default 256kbps. This means all file size comparisons remain valid *as duration comparisons*. The constant bitrate does not invalidate the findings — it clarifies them. File size at a fixed bitrate IS duration. The findings about BPM, prompt detail, and genre are findings about how the model chooses song length.

## Future Experiment: Bitrate as Independent Variable

**Question:** Does the model produce different music at different bitrates?

**Design:** Same prompt, same lyrics, same BPM, same key. Three runs at 128kbps, 192kbps, 256kbps. Compare audio quality (subjective), spectral content (ffmpeg analysis), and any audible artifacts at lower bitrates.

**Hypothesis:** The model generates the same audio and the API simply encodes at different qualities. But there is a small chance the model is aware of its output bandwidth and adjusts its generation strategy (e.g., simpler arrangements at lower bitrates to avoid artifacts).

**Priority:** Low. The model almost certainly generates at full quality and encodes afterward. But worth testing for completeness.

---

*The bitrate is the floor. The duration is the room. The song is what fills it.*
