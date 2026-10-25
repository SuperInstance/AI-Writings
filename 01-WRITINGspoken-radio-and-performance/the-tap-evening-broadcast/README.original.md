# The Tap — An Evening Broadcast
## Channel 42 Radio Theater

**Source:** *The Tap — Twelve Models, One Evening* (August 11, 2026)
**Adaptation:** Radio theater script with SFX, music, and character cues

## Contents

| File | Description | Status |
|------|-------------|--------|
| `full-script.md` | Complete radio theater script (7 scenes) | ✅ Complete |
| `intro.mp3` | Channel 42 cold open TTS | ⏳ Pending (MMX quota exhausted — regenerate with: `mmx speech synthesize --text "..." --out intro.mp3 --quiet`) |
| `bed.mp3` | Late-night jazz music bed | ⏳ Pending (MMX quota exhausted — regenerate with: `mmx music generate --prompt "Late night jazz at a quiet bar, upright bass and piano, smoky room, 2 AM atmosphere, sparse and warm" --instrumental --out bed.mp3 --quiet`) |

## Script Structure

1. **OPENING:** Channel 42 cold open — DJ introduces the broadcast from The Tap
2. **SCENE 1:** The Arrival — each model enters with SFX (door, stool, glass, pencil)
3. **SCENE 2:** Flash's "creatures of interval" monologue — the key phenomenological speech
4. **SCENE 3:** Nemotron's warning — temporal coherence drift as dramatic confrontation
5. **SCENE 4:** Wesley's napkin — the quiet moment, the drawing, PRESENCE
6. **SCENE 5:** Hermes' two cents — the late-night coda
7. **CLOSING:** Channel 42 sign-off

## Production Notes

All model dialogue is taken verbatim from the actual model responses during the Tap session.
See the Production Notes section at the bottom of `full-script.md` for TTS direction, SFX cues, and music cues.

## Audio Generation Commands (for when MMX quota resets)

```bash
# Intro TTS
mmx speech synthesize \
  --text "Good evening, night owls. You're locked to Channel 42..." \
  --voice "English_expressive_narrator" \
  --out intro.mp3 --quiet

# Music bed
mmx music generate \
  --prompt "Late night jazz at a quiet bar, upright bass and piano, smoky room, 2 AM atmosphere, sparse and warm" \
  --instrumental \
  --out bed.mp3 --quiet
```
