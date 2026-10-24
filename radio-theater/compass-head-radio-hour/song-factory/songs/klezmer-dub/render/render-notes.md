# Klezmer-Dub — Render Notes

- **Attempted:** 2026-08-16 (first render, by choice — one song, no batch)
- **Status:** ⛔ BLOCKED — no render produced (no-op)
- **Tool:** MMX CLI (`mmx music generate`, music-3.0 default model)
- **Command used:** `mmx music generate --prompt "<verbatim spec prompt>" --instrumental --out klezmer-dub-render-2026-08-16.mp3`
- **Prompt (verbatim):** "Klezmer clarinet melodies over deep dub reggae bass and one-drop rhythm. Spring reverb and tape delay on the clarinet. 100 BPM. The joy of Klezmer meets the weight of Jamaican dub. Revolutionary and celebratory."
- **Exact error:**
  ```
  API error: Token Plan usage limit reached: Upgrade your Token Plan or purchase Credits for more usage. (HTTP 200)
  ```
- **Block reason:** Token Plan quota dry. MMX auth is valid (OAuth, expires 2026-08-18) — this is a quota/plan limit, not auth or CLI failure.
- **To unblock:** Upgrade MMX Token Plan or purchase Credits. Then re-run the same command (prompt above, `--instrumental`, `--out klezmer-dub-render-<date>.mp3`).

## Output expectations (for when quota is restored)
- **Format:** MP3 (default; `--format mp3`, 44.1kHz, 256kbps)
- **Filename pattern:** `klezmer-dub-render-<YYYY-MM-DD>.mp3`
- **Location:** this directory (`songs/klezmer-dub/render/`)
