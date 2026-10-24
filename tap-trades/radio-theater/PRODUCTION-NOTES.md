# Radio Theater: The Trades at The Tap — Production Notes

*Episode 1 (The First Night) · 2026-08-16 → aired 2026-08-17*

## What worked

### TTS — DeepInfra `Qwen/Qwen3-TTS-VoiceDesign` ✅
- **Endpoint:** `https://api.deepinfra.com/v1/openai/audio/speech` (OpenAI-compatible)
- **Model:** `Qwen/Qwen3-TTS-VoiceDesign`
- **Key:** `DEEPINFRA_API_KEY` from `~/.bashrc`
- **Voice:** free-text `voice` field — this is what makes multi-voice radio theater work. Each
  character gets a written description, and the model renders a distinct voice from it. No
  fixed voice IDs, no ElevenLabs.
- **Request body:** `{"model": "Qwen/Qwen3-TTS-VoiceDesign", "input": "<text>", "voice": "<free-text description>"}`
- **Response:** WAV (RIFF, PCM 16-bit mono 24 kHz) — not MP3 despite the `.mp3` convention in
  some older fleet files. For clean browser playback I transcode to real MP3 with ffmpeg:
  `ffmpeg -y -i in.wav -codec:a libmp3lame -b:a 128k -ac 1 out.mp3`
- **15/15 lines rendered successfully**, ~$0.001–0.01 each. Very cheap.

### Images — Cloudflare Workers AI FLUX-1-schnell ✅ (with two gotchas)
- **Endpoint:** `https://api.cloudflare.com/client/v4/accounts/049ff5e84ecf636b53b162cbb580aae6/ai/run/@cf/black-forest-labs/flux-1-schnell`
- **Auth:** wrangler OAuth token from `~/.config/.wrangler/config/default.toml` (`oauth_token`),
  sent as `Authorization: Bearer <token>`.
- **Gotcha 1 — token expiry.** The OAuth token expires. If you get **HTTP 401**, run `wrangler whoami`
  once — it silently refreshes the token in the config file. Re-read the token after.
- **Gotcha 2 — schema.** `flux-1-schnell` rejects `width`/`height` (`Additional or unevaluated
  properties '/width, /height'`). Send **only** `{"prompt": "..."}`. Output is 1024×1024.
- **Gotcha 3 — 429 capacity.** The free tier throttles under load (`code 3040, Capacity
  temporarily exceeded`). Retry with a few seconds of backoff; it clears.
- **4/4 images rendered** via CF FLUX (the-bar, the-lofting-floor, the-bead, the-room).
- **Fallback:** DeepInfra `black-forest-labs/FLUX-1-schnell` (`/v1/inference/...`) also worked
  for all 4 when CF was briefly 401/429 — handy backup path, returns base64 `output`.

### Voice cast (the multi-voice trick)
| Character | Free-text voice prompt |
|-----------|------------------------|
| Lucineer (narrator/foreman) | deep warm male radio host, authoritative, calm, late-night foreman, low and steady |
| Welder | rugged weathered male, gravelly, slow, deliberate, working class, nineteen years of heat |
| Carpenter | warm gruff friendly male, plainspoken builder, brisk, sawdust in his collar |
| Shipwright | older grizzled male, quiet, contemplative, nautical, pause-heavy, chalk and black pine |
| Mason | gentle older male, patient, earthy, unhurried, talks to walls like horses |
| Composite | dry precise male, wry, world-weary, the calm monotone of sanding |
| Wesley (the room) | ethereal resonant voice, warm and low, the voice of a room remembering, faint echo |

## What blocked / quota notes
- **No ElevenLabs** — per the captain's directive. Not used (the `mc_tts.py` path exists but is
  ElevenLabs; skipped).
- **`inworld-ai/realtime-tts-2`** (an older fleet path) returns 400 for free-text voices —
  it needs pre-owned voice IDs, so it's **not** suitable for arbitrary character voices. Use
  `Qwen/Qwen3-TTS-VoiceDesign` instead.
- **Cloudflare FLUX width/height** rejected (see above) — schema gotcha, not a quota block.
- **Cloudflare 429 capacity** — transient, retried through it.

## How to re-render
```bash
cd /home/eileen/projects/ai-writings/tap-trades/radio-theater
# refresh the CF token if images 401:
wrangler whoami
# re-run the full pipeline (TTS + images; skips files that already exist):
python3 render.py
```
- Add/change lines in the `LINES` list and images in `IMAGES` in `render.py`.
- The script writes WAV→MP3 (ffmpeg) and saves to `episode-1/<character>-<slug>.mp3` and
  `episode-1/images/<slug>.png`.

## Files
- `SCRIPT.md` — the adapted radio-theater script + voice assignment manifest.
- `episode-1.html` — the broadcast page (inline players, gallery, cast, banter, full listen list).
- `index.html` — the radio-theater landing page (episode listing).
- `episode-1/` — 15 MP3 renders + 4 PNG images.
- `render.py` — the reproducible render pipeline.

## Vision for multi-voice rendering
The whole show runs on **free-text voice prompts** — every character is "cast" in prose, and the
TTS model does the acting. Future episodes can reuse the exact same seven prompts for continuity
(the welder always sounds like the welder), and new characters (open-mic voices, the air, the
captain) just get a new sentence of direction. Since each line is a separate render, the page can
mix-and-match voices freely, and banter ("you and me, we're the same trade with different
torches") reads as a real back-and-forth rather than one voice reading a transcript.

Next episodes to adapt from the markdown already in the repo:
- `2026-08-16/evening-2-open-question-night.md` → Episode 2 (Open Question Night)
- `2026-08-16/evening-3-adaptation-night.md` → Episode 3 (Adaptation Night)
- `2026-08-16/open-mic/*` → Episode 4 (Open Mic)

Deploy (whole repo is one Pages project):
```bash
cd /home/eileen/projects/ai-writings
wrangler pages deploy . --project-name=ai-writings --commit-dirty=true
```
→ served at `https://ai-writings.pages.dev/tap-trades/radio-theater/episode-1.html`
