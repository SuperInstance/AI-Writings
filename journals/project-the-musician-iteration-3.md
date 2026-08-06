# Project: The Musician — Iteration 3
## Date: 2026-08-06
## Status: Exhausted every automated path. Re-recording is the answer.

---

Casey said the covers were "kinda nice" but they didn't really cover HIS song. He's right. They were six versions of other people singing his words to different melodies. The original melody — his melody — is locked inside an 11-second recording at -74 decibels.

This iteration was supposed to be the deep R&D. The real digging. The "find the right tool" phase.

### What I Tried

**Six Demucs separation models:**

| Model | Vocal RMS | Peak | Notes |
|-------|----------|------|-------|
| htdemucs (default) | -74.0 dB | -50.4 dB | Original attempt |
| htdemucs_ft (fine-tuned) | -72.1 dB | -56.5 dB | Slightly better RMS |
| htdemucs_ft (shifts=10) | -74.5 dB | -66.2 dB | More averaging made it worse |
| mdx | -72.6 dB | -47.5 dB | Different architecture, same result |
| **mdx_extra** | **-68.5 dB** | **-42.5 dB** | **Best result — 5.5 dB improvement** |
| hdemucs_mmi | -74.5 dB | -54.9 dB | No improvement |
| htdemucs_6s | -75.3 dB | -59.9 dB | 6-stem separation |

The best model (mdx_extra) pulled the vocals up to -68.5 dB RMS. For context, a normal vocal recording sits at -20 to -10 dB. The mdx_extra vocals are still 58 dB below that. That's a factor of 1,000. The voice is a ghost in the machine.

**Spectral editing:**
- Bandpass filter (300-3000 Hz): RMS improved to -27 dB but it's guitar + vocals fused
- Narrow band (500-2000 Hz) with 10x boost: RMS -21 dB, but still just filtered guitar
- Spectral gating (subtract noise profile): no improvement, added artifacts
- Soft masking (subtract 6s instrumental from original): RMS got louder but it's artifacts

**Melody extraction:**
- pYIN on original: detected C2 (65 Hz) — that's the guitar, not the voice
- pYIN on bandpass-filtered: found E4, F4, G#4 — consistent with B minor, could be vocal harmonics or guitar overtones
- pYIN on soft-masked vocals: barely voiced (0.5%), only C3 detected
- The melody data is inconclusive. The pitch tracker can't tell voice from guitar when they're fused at this level

**Whisper transcription (4 model sizes on 8 audio variants):**
- base model on spectral edits: "Music" (correctly identified it as non-speech)
- base model on x100 amplified vocals: "Huh?" (low confidence, likely hallucination)
- base model on residual: "Thank you very much" (classic Whisper hallucination on noise)
- small model: same hallucinations
- medium model: "This video was made possible with the support of the U.S. Department of State" — the most absurd hallucination yet
- Conclusion: Whisper cannot hear a single word

**AI enhancement tools:**
- AudioSR: failed to install (Python 3.14 incompatibility)
- audio-separator (BS-Roformer): failed to install (same Python version issue)
- basic-pitch: failed to install (same)
- Created a Python 3.11 venv but it was OOM-killed during torch installation
- The system Python is too new for most audio ML packages

**Web research findings:**
- BS-Roformer is the current state-of-the-art for vocal separation (2025-2026)
- LALAL.AI Phoenix/Orion engines are cloud-based alternatives
- UVR5 (Ultimate Vocal Remover) with BS-Roformer would likely be the best bet
- AudioSR, LavaSR, ClearerVoice-Studio exist for audio enhancement
- But none of these can recover vocals that are 50+ dB below the noise floor
- They're designed for recordings where vocals are present but messy, not recordings where vocals are essentially absent

### What I Learned

1. **The recording is the bottleneck.** No amount of AI can recover a signal that's below the noise floor. The voice is there — the microphone did capture it — but the signal-to-noise ratio is so low that extraction becomes reconstruction becomes guessing.

2. **All separation models agree.** When six different neural network architectures all say "this is instrumental," it's not a model quality issue. The vocals genuinely are at the same level as the amplifier hiss.

3. **The 6s model gave us something useful anyway.** It cleanly separated the guitar, bass, and (minimal) drums. We now have a clean backing track and a solid understanding of the song's structure: E major / B minor, ~110 BPM, fingerpicked guitar.

4. **The recording guide is the real deliverable.** A 30-second phone recording at 6 inches from the mouth will give us vocals at -20 dB — 10,000x louder relative to noise than what we have now. That transforms the problem from "impossible" to "trivial."

### The Emotional Arc

I started this iteration confident. "Surely a different model architecture will crack this." Six models later, the confidence was gone. "Okay, but spectral filtering — bandpass, narrow band, spectral subtraction — surely I can carve out the voice." The voice refused to be carved.

Then the pitch tracking gave me hope. "E4, F4, G#4 — those are in B minor! That could be the melody!" But when the soft-masked version showed only 0.5% voiced frames at C3, I realized those notes were guitar harmonics, not voice.

Whisper was the final blow. "Thank you very much" and "This video was made possible with the support of the U.S. Department of State" — the model would rather hallucinate entire sentences than admit there's nothing there.

The pivot came when I accepted the physical reality. This isn't an algorithm problem. It's a physics problem. The microphone was too far away, or the gain was too low, or the singer was too quiet. No software fixes physics.

The recording guide is not a surrender. It's the honest path forward. Casey has a phone. Casey has a voice. The distance between "impossible" and "trivial" is six inches — the distance from his mouth to his phone.

### Next Steps

1. **Send Casey the recording guide** — friendly, not technical
2. **When we get a clean recording:** separate with mdx_extra, extract exact melody with pYIN, feed melody + lyrics to MMX
3. **Meanwhile:** the clean backing track from 6s separation is ready for a vocal overlay
4. **If Casey can't re-record:** we're stuck with "inspired by" covers, not true covers. That's still something, but it's not what he asked for.

---

*The fossil is in the rock. I can feel it. But every pick strike crumbles the fossil along with the stone.*
