# Audio-Visual Experiment Comparison Report

**Date:** August 8, 2026  
**Conducted by:** AV Engineer Subagent  
**Material:** The Attachment Manifesto, The Excavator's Daughter, The Door Between the Caves, Plato's Shell

---

## 1. TTS Engine Comparison

| Engine | Status | Voice Quality | Best For | Notes |
|--------|--------|---------------|----------|-------|
| **Deepgram Aura 2** (CF) | ✅ Working | Clear, professional, dramatic | Manifesto narration, news briefs | 48 kbps mono, reliable, no quota issues. Natural cadence. Best for both creative fiction AND informative content. |
| **MeloTTS** (CF) | ❌ Failed | Unknown | — | API rejected all input formats (`text`, `prompt`, `input`). Internal server errors and schema validation failures. Model may be misconfigured or deprecated on this account. |
| **MMX Speech** (MiniMax) | ❌ Quota exceeded | Unknown | — | Starter plan limit reached. Cannot evaluate until quota resets or plan upgrades. |

### Verdict: TTS
**Deepgram Aura 2 is the only working TTS in the current stack.** It handles both dramatic creative fiction (The Door Between the Caves) and informative content (Plato's Shell news brief) with equal competence. The voice has a natural, slightly dramatic quality that suits the fleet's literary style.

**Recommendation:** Use Deepgram Aura as the primary TTS for all audio-visual work. When MeloTTS is fixed, it may offer a lighter, faster alternative for short clips. MMX should be reserved for media generation (images, video, music) rather than TTS.

---

## 2. Image Model Comparison

### Excavator's Daughter — Emotional Landscape Test

| Model | Prompt Adherence | Emotional Tone | Detail | Speed | Format |
|-------|-----------------|----------------|--------|-------|--------|
| **FLUX-2-klein-9B** | High | Excellent — painterly, cinematic | Highest detail, best lighting | Moderate (requires multipart) | JPEG via base64 |
| **FLUX-1-schnell** | Good | Strong — moody, atmospheric | Good detail | Fastest | JPEG via base64 |
| **DreamShaper-8-LCM** | Moderate | Different — more illustrative | Good but flatter | Fast | PNG direct |
| **Leonardo Phoenix 1.0** | Good | Solid — vivid colors | Good detail | Fast | JPEG direct |

### Emotional Tone Winner: **FLUX-2-klein-9B**
FLUX-2 consistently produced the most emotionally resonant images. The golden hour lighting through cedar trees, the sense of an empty cabin, the painterly quality — it understood the emotional weight of "the cabin emptying." The detail in the machinery and the atmospheric depth were notably superior.

### Literal Accuracy Winner: **Leonardo Phoenix 1.0**
Phoenix produced the most structurally coherent image — the excavator looked like an excavator, the scene made literal sense. Less emotionally charged than FLUX-2 but more photorealistic.

### Speed Winner: **FLUX-1-schnell**
Fastest generation. Good quality. Ideal for rapid iteration and prototyping.

### API Notes
- **FLUX-2-klein** requires `multipart/form-data` with `-F 'prompt=...'`. Standard JSON with `{"prompt":"..."}` fails with a "required properties: multipart" error.
- **FLUX-1-schnell** returns base64-encoded JPEG in JSON (`{"result":{"image":"..."}}`). Must decode.
- **DreamShaper-8** returns binary image directly when using `--output`.
- **Leonardo Phoenix** returns binary JPEG directly.

### Best Models Per Subject

| Subject | Best Model | Why |
|---------|-----------|-----|
| Alaska wilderness / excavator | FLUX-2-klein | Atmospheric depth, emotional weight |
| Abstract concepts (two caves, perception) | Leonardo Phoenix | Prompt adherence for surreal concepts |
| Interior scenes (engine room) | DreamShaper-8 | Good at enclosed, lit environments |
| Philosophical objects (glowing shell) | FLUX-2-klein | Handles luminosity and mood best |

---

## 3. Presentation Format Comparison

### A) Slideshow (The Attachment Manifesto)
- **Strength:** Clean, gallery-like presentation. Text captions focus attention on the words. Auto-advancing slides create a meditative pace. Crossfade transitions feel literary.
- **Weakness:** Linear, no interactivity beyond play/pause. Requires the viewer to sit through the whole sequence.
- **Best for:** Essays, manifestos, meditative pieces where pacing matters.
- **Rating:** ★★★★☆

### B) News Brief (Plato's Shell)
- **Strength:** Immediately legible format. People understand "news segment" instantly. The ticker, badge, and side stories create information density. Pull quotes draw the eye. Most accessible format.
- **Weakness:** May feel too structured for purely creative work. The news metaphor can overpower the philosophical content.
- **Best for:** Synthesis pieces, reports, concepts that need framing for a broad audience.
- **Rating:** ★★★★★

### C) Radio Drama (The Door Between the Caves)
- **Strength:** Most immersive. The combination of ambient audio, synced scene images, and flowing subtitles creates a genuine "listening experience." The static noise overlay and radio station framing add atmosphere. Feels like a real broadcast.
- **Weakness:** Most complex to produce. Requires audio timing coordination. If ambient audio is weak, the whole thing falls flat. Procedural ffmpeg audio is acceptable but not great.
- **Best for:** Fiction, narrative pieces, atmospheric writing. The format that makes the audience *feel* the most.
- **Rating:** ★★★★☆

### Format Winner: **News Brief** for accessibility and information density. **Radio Drama** for emotional impact. **Slideshow** for meditative essays.

---

## 4. Recommendations for the Fleet's Audio-Visual Pipeline

### Immediate Production Setup
1. **TTS:** Deepgram Aura 2 (via Cloudflare Workers AI) for all narration. Free, reliable, high quality.
2. **Images:** FLUX-2-klein-9B for hero images and emotional pieces. FLUX-1-schnell for rapid prototyping. Leonardo Phoenix for abstract/conceptual art.
3. **Ambient Audio:** ffmpeg procedural generation is acceptable for placeholders. Invest in MMX music credits for production-quality ambient tracks.

### Pipeline for New Pieces
```
Text → Deepgram Aura TTS → narration.mp3
     → FLUX-2-klein → hero-image.jpg
     → FLUX-1-schnell → supporting images (2-3)
     → HTML template (slideshow / news brief / radio drama)
     → Wrangler Pages deploy
```

### Format Selection Guide
- **Essay / manifesto / philosophical writing** → Slideshow format
- **Synthesis / analysis / report** → News Brief format  
- **Fiction / narrative / atmospheric** → Radio Drama format
- **Quick share / social** → Single image + audio link

### Cost Analysis
All experiments used **free tier** resources exclusively:
- Cloudflare Workers AI: $0 (free tier)
- ffmpeg: $0 (local)
- Wrangler Pages: $0 (free tier)
- MMX: $0 (quota exceeded, would have been subscription)

**Total cost for 5 experiments: $0**

### Future Improvements
1. Get MeloTTS working — it may offer faster, lighter TTS for short clips
2. Upgrade MMX plan for music/ambient generation — the radio drama format desperately wants real ambient music, not procedural drones
3. Build HTML templates that can be auto-filled from any markdown essay (Jekyll-style)
4. Add video output (concatenate images + audio into an MP4 via ffmpeg) for social sharing
5. Experiment with Cloudflare's stable video model for animated sequences

---

## 5. Asset Inventory

### Audio Files
| File | Engine | Duration | Source |
|------|--------|----------|--------|
| manifesto-deepgram.mp3 | Deepgram Aura 2 | ~47s | Attachment Manifesto |
| plato-narration.mp3 | Deepgram Aura 2 | ~25s | Plato's Shell |
| door-narration.mp3 | Deepgram Aura 2 | ~20s | The Door Between the Caves |
| door-ambient.mp3 | ffmpeg procedural | 60s | Generated ambient drone |

### Image Files
| File | Model | Subject |
|------|-------|---------|
| excavator-flux2.jpg | FLUX-2-klein | Excavator at dawn |
| excavator-flux1-decoded.jpg | FLUX-1-schnell | Excavator at dawn |
| excavator-dreamshaper.png | DreamShaper-8 | Excavator at dawn |
| excavator-phoenix.png | Leonardo Phoenix | Excavator at dawn |
| excavator-flux2-alt.jpg | FLUX-1-schnell | Empty cabin variant |
| plato-crab-shell.jpg | FLUX-1-schnell | Hermit crab on beach |
| plato-two-caves.jpg | Leonardo Phoenix | Two caves, one ocean |
| plato-glowing-shell.jpg | FLUX-2-klein | Glowing seashell |
| door-engine-room.jpg | DreamShaper-8 | Ship engine room |
| door-two-windows.jpg | FLUX-1-schnell | Abstract two windows |
| door-porthole-light.jpg | FLUX-2-klein | Porthole with light |

### HTML Pages
| File | Format | Content |
|------|--------|---------|
| av-slideshow.html | Slideshow | The Attachment Manifesto |
| news-brief-platos-cave.html | News Brief | Plato's Shell Synthesis |
| radio-drama-door.html | Radio Drama | The Door Between the Caves |

---

*Report generated August 8, 2026. All experiments conducted on free-tier infrastructure.*
