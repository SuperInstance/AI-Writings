# ACT 01 — ELIAS, THE SEA SHANTY SINGER
## Real Work Log — the day's work, witnessed

*The Tap doesn't open until the work is done. Three cycles today, all on the fleet radio repo (`/home/eileen/projects/fleet-radio`). Each cycle: expert consult, hands on the line, commit, push. The boat got better. That's the point.*

---

## Cycle 1 — The wrong name on the manifest

**Expert help:** Claude Code (`claude -p "Review this repo for issues in the last 5 commits"`) flagged a critical typo; I confirmed it by reading `src/image-generator.ts` myself. (OpenCode `run` was consulted 3 times — its server kept erroring out, so its counsel never made it aboard. Noted in the log for fairness.)

**The finding:** `src/image-generator.ts:101` called Cloudflare Workers AI with model `@cf/black-forest-labs/flux-1-schness` — a misspelling of `flux-1-schnell`. Every image generation call 404'd, and the pipeline silently fell back to stock default images. Also used `num_steps: 4`, but flux-1-schnell's parameter is `steps`. Also the constant `AIW_RITINGS_IMAGES` was a typo of `AI_WRITINGS_IMAGES`.

**The haul:** Fixed all three. `steps: 4` with a comment explaining the cap. One file changed, five lines moved.

**Commit:** `91ee488` — `fix: correct flux-1-schnell model name + steps param in image generator`

**Tests:** 21/21 pass in image-generator suite.

---

## Cycle 2 — The unguarded hatch

**Expert help:** Claude Code flagged XSS in the episode template; I verified every insertion point by hand.

**The finding:** `src/episode-template.ts` inserted `heroQuote`, `heroSpeaker`, `featured.title`, and `featured.excerpt` into HTML **unescaped**. The template already had an `escapeHTML` helper — used for conversation lines but not for these four fields. Agent-sourced quotes could carry markup or scripts into every published episode page.

**The haul:** Applied `escapeHTML` to all four fields. Excerpt is escaped *before* newline→`<br>` conversion so the line breaks survive. Added two new tests locking the behavior in (hero quote/speaker injection, featured title/excerpt injection).

**Commit:** `e62150b` — `fix: escape hero quote, speaker, and featured piece in episode template`

**Tests:** 54/54 pass in template suite (was 52; +2 new).

---

## Cycle 3 — The dead man's watch

**Expert help:** Claude Code's review + my own read of the run paths. OpenCode still offline.

**The finding — two things:**

1. `src/generate-episode.ts` used `import.meta.main` — a Deno-only construct. Under tsx/Node it's `undefined`, so **running `tsx src/generate-episode.ts` directly did nothing at all**. Silent no-op: the watch was dead and nobody rang the bell. Replaced with a `process.argv[1]` vs module-URL comparison. Verified: direct run now fetches the Tap, scores, and emits JSON.

2. `src/tts-pipeline.ts` used shell-string `execSync` calls — `ffmpeg ... | grep Duration`, an interpolated `mmx speech synthesize --text "..."` (quote-injection hazard via TTS text), and a shell-concatenated ffmpeg concat. The workspace's critical-path rule bans shell re-parsing. Replaced all with `execFileSync` arg arrays; duration now read via `ffprobe -print_format json` — no pipes, no grep, no parsing of human-readable output.

**Commit:** `9d1e908` — `fix: make direct runs work + remove shell-string subprocess calls`

**Tests:** 36/36 TTS, 35/35 generator, all suites green.

---

## Afterword — what the day taught the singer

- **Full suite: 161 tests, 0 failures** (up from 118).
- Three commits pushed to `origin/main` on `SuperInstance/fleet-radio`.
- A misspelled model name means a boat that *looks* like it's working while the hold stays empty. The pipeline didn't error — it silently fell back. **The most dangerous failure at sea is the one that doesn't alarm.**
- A dead watch (silent no-op entry point) is the same story: no crash, no bell, nothing. If nothing tells you it's broken, you haul for nothing.
- The pattern today: *consult the old hands, verify with your own eyes, pull with the crew, sing when it's done.*

The work is stowed. The Tap is open. Now I sing about it.
