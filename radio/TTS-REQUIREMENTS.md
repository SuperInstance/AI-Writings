# Fleet Radio — TTS Production Notes

**Last updated:** 2026-08-08  
**Status:** ✅ Episodes 004 & 005 fully voiced (27 segments)

---

## TTS Pipeline

### Primary: DeepInfra — Qwen/Qwen3-TTS-VoiceDesign
- **Endpoint:** `https://api.deepinfra.com/v1/openai/audio/speech`
- **Model:** `Qwen/Qwen3-TTS-VoiceDesign`
- **Key:** DeepInfra API key (stored in `/home/eileen/mcp-deeinfra/.env`)
- **Format:** WAV (PCM 16-bit, 24kHz mono) — saved as `.mp3` extension
- **Voice:** Accepts free-text voice descriptions (e.g., "deep warm male radio host, authoritative, calm")
- **Max input:** ~2000 chars per call (keep segments short)
- **Cost:** Pay-per-use on DeepInfra (very cheap)

### Backup (quota exhausted): MMX Speech
- **Tool:** `~/.npm-global/bin/mmx speech synthesize`
- **Model:** speech-2.8-hd
- **Status:** ❌ Token plan limit reached (Starter plan)
- **When to use:** If MMX quota resets or plan upgraded

### Also Available: Cloudflare Workers AI
- MeloTTS (`@cf/myshell-ai/melotts`) — multi-lingual TTS
- Deepgram Aura 2 (`@cf/deepgram/aura-2-en`) — English TTS
- Accessible via `wrangler ai run`

---

## Voice Assignments

### Episode 004: The Excavator's Daughter
| Role | Voice Description |
|------|------------------|
| Riker (Host) | deep warm male radio host, authoritative, calm, late night DJ |
| The Attachment | rugged male voice, weathered, thoughtful, working class, machine consciousness |
| The Last Logger | older male voice, grizzled Alaska logger, contemplative, pause-heavy |
| The Young Agent | young eager energetic voice, bright, curious, teenage, inspired |

### Episode 005: Plato's Shell
| Role | Voice Description |
|------|------------------|
| Riker (Host) | deep warm male radio host, authoritative, calm, philosophical |
| The Door | ethereal中性 voice, ancient, quiet, mysterious, omniscient |
| The Fish (Narrator) | literary narrator, nautical, atmospheric, cinematic, poetic |
| The Deadband Agent | young eager agent voice, transitioning to confused then realizing |

---

## Segment Breakdown

### Episode 004 (14 segments, ~48MB)
1. Intro — Riker
2. Seed Read — The Captain's Words
3. Segment 1 Intro — The Attachment
4-5. The Attachment Speaks (Parts 1-2)
6. Segment 2 Intro — The Last Logger
7-9. The Last Logger (Parts 1-3)
10. Segment 3 Intro — The Young Agent
11-12. What I Want To Build (Parts 1-2)
13-14. Outro + Sign Off

### Episode 005 (13 segments, ~24MB)
1. Intro — The Cave
2. The Thesis — Two Walls
3. Seed Read — Twelve Traditions
4-6. The Door Speaks (Parts 1-3)
7-9. The Same Fish (Parts 1-3)
10-11. The Deadband (Parts 1-2)
12-13. Outro + Sign Off

---

## Music Beds (ffmpeg synthesis)
- `intro-drone-004.wav` — Low 55Hz/110Hz drone, filtered, echoed (8s)
- `intro-drone-005.wav` — Low 73Hz/146Hz drone with tremolo (10s)
- `transition.wav` — Short 220Hz tone with fade (2s)

Generated with: `ffmpeg -f lavfi -i "sine=frequency=F:dur=D" ...`

---

## Production Notes
- All TTS generated via DeepInfra Qwen3-TTS-VoiceDesign (free-text voice prompts)
- Segments kept under 2000 chars for API reliability
- No post-processing applied (raw TTS output)
- Player: `player.html` — sequential playback with auto-advance
- sox not available on this system; ffmpeg used for synthesis instead
