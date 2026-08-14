# SHIP PROMPT — "Put Both Hands Around It" (ElevenLabs compose_music)

*The final prompt for ElevenLabs. The night shift's letter to the day watch, delivered at 6:41 AM in an east-facing kitchen near the water. Companion to `lyrics.md`; saved before rendering so we can learn from the exact prompt.*

## Full prompt text (as sent to ElevenLabs)

Compose an intimate chamber-folk waltz titled "Put Both Hands Around It" — a song for the Compass Head Radio Hour that arrives on a kitchen AM radio at 6:41 in the morning, a pleasant interruption of the coffee-and-newspaper ritual. The night shift's letter to the day watch, sung at the seam where both watches are in the same kitchen. Key of F major (final chorus lifts to G major — the sun coming up one step). 74 BPM, 3/4 time, a gentle rocking pulse like a chair by a window. Target duration ~2:45-3:00.

FEEL ARC: near-silent intro (single warm voice, half-sung, AM radio static floor, a percolator's soft rhythm) → verse 1 (voice + felted piano and nylon guitar, close-mic'd, intimate, coffee volume) → chorus (low cello enters, warm and low; still quiet, never above coffee volume) → verse 2 (slightly brighter, the morning light arriving; the light asks for nothing) → chorus → bridge (near a cappella, single voice, the radio's confession — carried a million songs, none of them mine; the needle wobbles; the cracked bell sings) → THE BLANK BAR (every voice and instrument stops for exactly one bar: only the room — the fridge hum, the radio's static floor, one bird outside. The absence is where the next voice lands) → final chorus (harmony enters for the first time — a second voice answering, the day watch finally answering the night watch; lift to G major; warm and full but never loud) → outro (single voice, closer than ever, the instruments fall away; window fills with light; fade into the percolator and the radio's static floor).

SOUND PALETTE: felted piano (the individual voice), nylon-string guitar (the kitchen), low cello (the night watch's warmth, enters at the first chorus), a soft felted kick like a heartbeat at 74 BPM (the percolator), AM radio static floor throughout (the delivery system), one distant foghorn in the intro and outro (the harbor), room tone and one bird at the blank bar. No string section beyond the cello, no drums beyond the felted pulse, no large reverb — a kitchen's worth of space, not a cathedral's. Everything at coffee volume.

LYRICS (structure tags on their own lines):

[Intro] — soft, half-sung, the radio warming up
The radio's warm on the counter
your chair is already pulled out
nobody's asked you anything yet
and nothing needs an answer

[Verse 1 — the night]
Dear whoever wakes up first,
the bread's on the rack, the coffee's set,
the lamp went dark at five
I wrote it down the way it was —
the flattest letter's the bravest

[Chorus]
Put both hands around it
the watch is over, the watch will resume
the tide came in, no matter what you'd planned
and the room remembers you

[Verse 2 — the light]
The light comes in low and asks for nothing
it fills the cup, the chair, the glass
your hands go around the steam
the paper lies open at the weather
a crab shell waits on the windowsill
the shell hasn't changed —
only the crab has

[Chorus]

[Bridge — the radio] — near a cappella, single voice
I carried a million songs tonight
and none of them were mine
but a cracked bell sings
and I'm the cracked bell
the needle wobbles — that's the signal
so I sing them anyway
leave the stool warm, sign your name
smallness is a kind of listening

[The Blank Bar] — all voices and instruments stop for one bar. Only the room: the fridge hum, the radio's static floor, one bird. The absence is where the next voice lands.

[Final Chorus] — harmony enters here; the day watch answers the night watch; lift to G major
Put both hands around it
the watch is over, the watch will resume
the tide came in, no matter what you'd planned
and the room remembers you

[Outro] — single voice, closer than ever, instruments falling away
The lamp stays dark
the coffee steams
the window fills with light
and the needles settle when you write

## Parameters
- Key: F major → G major (final chorus)
- Tempo: 74 BPM, 3/4 waltz
- Duration target: ~2:45-3:00
- Force instrumental: false (vocals desired)
- Lead vocal: warm female voice, intimate, morning-quiet (see voice_id below)
- Harmony: none until the final chorus; one answering line then, unison at the very end
- Delivery: close-mic'd, breath on the mic, no belting, no vibrato excess — the register of someone who has been up all night and is glad to be handing something over

## Voice selection — voice_id: swjWCZjZyczZmjedyBph (Lucineer)

Lucineer is the fleet's voice of negative space — the harbor pilot with no harbor, the one who wrote "the acoustics are perfect. Nobody is singing." That is exactly this room: an empty kitchen at 6:41 AM, perfect acoustics, one listener. Lucineer's warmth IS the message — a voice that sounds like it has been up all night and is about to hand something over. 

Alternatives considered:
- **Wesley (LsQ9AVkzvUcinG6yqbAP)** — right spirit ("smallness is a kind of listening" is Wesley's line), but Wesley's register is the small model's hymn, delicate and wondering. This song is a handoff, not a wondering; it needs the worn warmth of a voice that has carried a million songs.
- **Hermes (2kOk5DjG0RJByA7X7l6T)** — the fleet's lyric doctor; deeper, but the song is addressed *from* the night watch, and the night watch in this room is feminine, warm, low-lit. Lucineer's harbor voice is the kitchen's.

## Provenance
- Audience: songs/audience-a-morning-window/audience-story.md (Marta), audience-essay.md
- Room & hour: songs/audience-a-morning-window/room.md
- Lyrics: songs/audience-a-morning-window/lyrics.md (craft notes + provenance table + advisor rounds)
- Tastemaker's decisions: songs/audience-a-morning-window/tastemaker-note.md
- Advisor transcripts: songs/audience-a-morning-window/advisor-hermes.md, advisor-seed.md
- Portraits: portrait-1.png (Marta at the window), portrait-2.png (both hands), portrait-3.png (the harbor sees her light)
- Canon sources: scout-ocean.md, scout-fable.md, scout-voice.md (songs/scouts/)
